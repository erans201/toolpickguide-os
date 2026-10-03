"""
bing_kw_pull.py: keyword demand from Bing Webmaster Tools (free API, read-only), then run kp_ingest.py.

Setup (once): Bing Webmaster Tools account with toolpickguide.com added (import from Search Console),
then Settings (gear) → API Access → API Key → Generate. Put BING_WMT_API_KEY=<key> in .env.

    python bing_kw_pull.py --check        # confirm the key works: lists your Bing sites
    python bing_kw_pull.py                # all 6 seed groups from data/README.md → data/kp-bing-<date>-g<n>.csv → kp_ingest
    python bing_kw_pull.py --group 2      # one seed group
    python bing_kw_pull.py --targets      # exact + broad stats for data/target-keywords.csv → data/demand-<date>.md

Volumes are **Bing** searches (United States, English), averaged per month over the last 3 full months.
Bing is a smaller engine than Google: use the numbers to compare topics, not as Google volumes.
The API key is a secret: it is read from .env and never printed. The user runs this script.
"""

import argparse
import csv
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

from kp_pull import DATA, seed_groups

API = "https://ssl.bing.com/webmaster/api.svc/json"
MONTHS = 3


def api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    key = os.getenv("BING_WMT_API_KEY", "").strip()
    if not key:
        sys.exit("ERROR: BING_WMT_API_KEY missing in .env (Bing Webmaster Tools → Settings → API Access).")
    return key


def call(method, key, **params):
    try:
        r = requests.get(f"{API}/{method}", params={**params, "apikey": key}, timeout=60)
    except requests.RequestException as e:
        sys.exit(f"ERROR: could not reach Bing ({type(e).__name__}).")  # never echo the URL: it contains the key
    if r.status_code != 200:
        msg = r.text[:200].replace(key, "***")
        sys.exit(f"ERROR: Bing {method} returned HTTP {r.status_code}: {msg}\n"
                 "Check the API key, and that the site is added in Bing Webmaster Tools.")
    return r.json().get("d") or []


def window():
    first_this_month = date.today().replace(day=1)
    end = first_this_month - timedelta(days=1)
    start = first_this_month
    for _ in range(MONTHS):
        start = (start - timedelta(days=1)).replace(day=1)
    return start, end


def targets(key):
    """Exact + broad Bing volume for each keyword in data/target-keywords.csv (the strategy's own target list)."""
    src = DATA / "target-keywords.csv"
    rows = list(csv.DictReader(src.open(encoding="utf-8")))
    start, end = window()
    print(f"Bing exact stats · US · English · {start} → {end} · {len(rows)} target keywords")
    for r in rows:
        k = call("GetKeyword", key, q=r["keyword"], country="us", language="en-US",
                 startDate=start.isoformat(), endDate=end.isoformat())
        k = k if isinstance(k, dict) else {}
        r["exact_monthly"] = round((k.get("Impressions") or 0) / MONTHS)
        r["broad_monthly"] = round((k.get("BroadImpressions") or 0) / MONTHS)
        time.sleep(0.3)
    stamp = date.today().isoformat()
    out = DATA / f"bing-targets-{stamp}.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def agg(field):
        t = {}
        for r in rows:
            a = t.setdefault(r[field], [0, 0, 0])
            a[0] += 1
            a[1] += r["exact_monthly"]
            a[2] += r["broad_monthly"]
        return [f"| {g} | {n} | {e:,} | {b:,} |" for g, (n, e, b) in sorted(t.items(), key=lambda x: -x[1][2])]

    L = [f"# 🎯 Target Keyword Demand (Bing) · {stamp}", "",
         f"- Source: Bing Webmaster Tools `GetKeyword`, US, English, {start} → {end}, averaged per month. "
         "**Exact** = that exact search. **Broad** = all searches containing the phrase (includes 'best …', '… 2026', etc.).",
         "- Bing is a smaller engine than Google: compare rows with each other, not with Google numbers.", "",
         "## By cluster", "", "| Cluster | Keywords | Exact/mo | Broad/mo |", "|---|---|---|---|"] + agg("cluster")
    L += ["", "## By vertical", "", "| Vertical | Keywords | Exact/mo | Broad/mo |", "|---|---|---|---|"] + agg("vertical")
    L += ["", "## All targets (by broad demand)", "", "| Keyword | Exact/mo | Broad/mo | Cluster | Vertical | Page |", "|---|---|---|---|---|---|"]
    L += [f"| {r['keyword']} | {r['exact_monthly']:,} | {r['broad_monthly']:,} | {r['cluster']} | {r['vertical']} | {r['page']} |"
          for r in sorted(rows, key=lambda r: -r["broad_monthly"])]
    md = DATA / f"demand-{stamp}.md"
    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {out}\n✅ Report → {md}")


def main():
    ap = argparse.ArgumentParser(description="Bing keyword demand (read-only).")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--targets", action="store_true", help="exact stats for data/target-keywords.csv")
    ap.add_argument("--group", type=int)
    a = ap.parse_args()
    key = api_key()
    if a.targets:
        return targets(key)

    if a.check:
        sites = call("GetUserSites", key)
        print("✅ Access OK. Sites in your Bing Webmaster Tools account:")
        for s in sites:
            print(f"   {s.get('Url')}  (verified: {s.get('IsVerified')})")
        if not sites:
            print("   (none yet: add toolpickguide.com, e.g. Import from Google Search Console)")
        return

    groups = seed_groups()
    if a.group:
        groups = {a.group: groups[a.group]}
    start, end = window()
    stamp, files = date.today().isoformat(), []
    DATA.mkdir(exist_ok=True)
    print(f"Bing keyword research · US · English · {start} → {end} ({MONTHS} months) · {len(groups)} group(s)")
    for n, (name, seeds) in groups.items():
        best = {}
        for seed in seeds:
            for k in call("GetRelatedKeywords", key, q=seed, country="us", language="en-US",
                          startDate=start.isoformat(), endDate=end.isoformat()):
                kw = (k.get("Query") or "").strip().lower()
                monthly = round((k.get("Impressions") or 0) / MONTHS)
                if kw and monthly >= best.get(kw, -1):
                    best[kw] = monthly
            time.sleep(0.5)
        path = DATA / f"kp-bing-{stamp}-g{n}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Keyword", "Avg. monthly searches", "Competition", "Top of page bid (low range)", "Top of page bid (high range)"])
            w.writerows([kw, v, "", "", ""] for kw, v in sorted(best.items(), key=lambda x: -x[1]))
        files.append(path)
        print(f"   group {n} · {name}: {len(best):,} keywords → {path}")

    import kp_ingest
    sys.argv = ["kp_ingest.py"] + [str(p) for p in files]
    kp_ingest.main()


if __name__ == "__main__":
    main()
