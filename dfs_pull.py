"""
dfs_pull.py: DataForSEO API (paid, pay-per-request; read-only data) → data/ CSVs + data/dfs-insights-<date>.md

Setup (once): DataForSEO account with balance → app.dataforseo.com/api-access → copy API login + API password.
Put them in .env:  DATAFORSEO_LOGIN=...  DATAFORSEO_PASSWORD=...   (never in chat). The user runs this script.

    python dfs_pull.py --check                 # free: confirms login, shows balance
    python dfs_pull.py --volume                # Google search volume for data/target-keywords.csv (1 request)
    python dfs_pull.py --gap                   # competitor keyword gaps: data/competitors.txt vs toolpickguide.com (1 request per competitor)
    python dfs_pull.py --serp --top 15         # Google top 10 + AI Overview citations for the 15 biggest targets (1 request each)
    python dfs_pull.py --volume --gap --serp   # everything; the report combines what exists

US, English. Every run prints the number of paid requests first and the actual cost (from the API) at the end.
Autopilot (TPG_AUTOPILOT=1): refuses to start if the month's spend + this run's estimate would pass $5
(autopilot/ledger.json); the real cost of each request is added to the ledger.
"""

import argparse
import csv
import os
import sys
import time
from datetime import date
from pathlib import Path

import requests

from autopilot import guard

API ="https://api.dataforseo.com/v3"
DATA = Path("data")
SITE = "toolpickguide.com"
US, EN = 2840, "en"
# Only gap keywords in our scope (Option B); DataForSEO Labs supports RE2 regex filters.
SCOPE_RE = ("crm|client management|practice management|case management|client portal|onboarding|intake|e-?sign|"
            "electronic signature|form builder|website builder|honeybook|dubsado|proposal|invoic|scheduling software|"
            "booking software|transaction management|contract template|questionnaire")
spent = 0.0
# Cautious per-request estimates (USD), used only for the autopilot budget check before buying.
EST_USD = {"volume": 0.10, "gap": 0.10, "serp": 0.02}


def auth():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    login, pw = os.getenv("DATAFORSEO_LOGIN", "").strip(), os.getenv("DATAFORSEO_PASSWORD", "").strip()
    if not (login and pw):
        sys.exit("ERROR: DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD missing in .env (app.dataforseo.com/api-access).")
    return login, pw


def call(creds, path, body=None):
    global spent
    try:
        r = (requests.post(f"{API}/{path}", auth=creds, json=body, timeout=120) if body is not None
             else requests.get(f"{API}/{path}", auth=creds, timeout=60))
    except requests.RequestException as e:
        sys.exit(f"ERROR: could not reach DataForSEO ({type(e).__name__}).")
    if r.status_code == 401:
        sys.exit("ERROR: DataForSEO rejected the login. Use the API login/password from app.dataforseo.com/api-access "
                 "(not your website password).")
    j = r.json()
    spent += float(j.get("cost") or 0)
    guard.dfs_spent(float(j.get("cost") or 0))  # per request, so a run that stops early still counts
    task = (j.get("tasks") or [{}])[0]
    if j.get("status_code") != 20000 or task.get("status_code") not in (20000, None):
        sys.exit(f"ERROR: DataForSEO {path}: {task.get('status_message') or j.get('status_message')}")
    return task.get("result") or []


def targets():
    return list(csv.DictReader((DATA / "target-keywords.csv").open(encoding="utf-8")))


def write(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"   → {path} ({len(rows)} rows)")


def volume(creds, stamp):
    rows = targets()
    res = call(creds, "keywords_data/google_ads/search_volume/live",
               [{"keywords": [r["keyword"] for r in rows], "location_code": US, "language_code": EN}])
    by_kw = {x["keyword"].lower(): x for x in res}
    for r in rows:
        x = by_kw.get(r["keyword"].lower(), {})
        r.update(google_volume=x.get("search_volume") or 0, competition=x.get("competition") or "",
                 competition_index=x.get("competition_index") or "", cpc=x.get("cpc") or "",
                 bid_low=x.get("low_top_of_page_bid") or "", bid_high=x.get("high_top_of_page_bid") or "")
    write(DATA / f"dfs-volume-{stamp}.csv", rows,
          ["keyword", "google_volume", "competition", "competition_index", "cpc", "bid_low", "bid_high", "cluster", "vertical", "page"])


def gap(creds, stamp):
    comps = [l.strip() for l in (DATA / "competitors.txt").read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    for comp in comps:
        res = call(creds, "dataforseo_labs/google/domain_intersection/live", [{
            "target1": comp, "target2": SITE, "intersections": False, "location_code": US, "language_code": EN,
            "item_types": ["organic"], "limit": 300, "order_by": ["keyword_data.keyword_info.search_volume,desc"],
            "filters": [["keyword_data.keyword", "regex", SCOPE_RE]]}])
        items = (res[0].get("items") if res else None) or []
        rows = []
        for it in items:
            kd, el = it.get("keyword_data") or {}, it.get("first_domain_serp_element") or {}
            rows.append({"keyword": kd.get("keyword"), "volume": (kd.get("keyword_info") or {}).get("search_volume") or 0,
                         "difficulty": (kd.get("keyword_properties") or {}).get("keyword_difficulty") or "",
                         "competitor_rank": el.get("rank_absolute") or "", "competitor_url": el.get("url") or ""})
        write(DATA / f"dfs-gap-{comp.replace('.', '_')}-{stamp}.csv", rows,
              ["keyword", "volume", "difficulty", "competitor_rank", "competitor_url"])
        time.sleep(5)  # API limit: 12 requests per minute


def refs(node, out):
    """Collect every cited domain inside an ai_overview item, whatever its nesting."""
    if isinstance(node, dict):
        if node.get("domain") and node.get("url"):
            out.append(node["domain"])
        for v in node.values():
            refs(v, out)
    elif isinstance(node, list):
        for v in node:
            refs(v, out)
    return out


def serp(creds, stamp, top):
    vol_files = sorted(DATA.glob("dfs-volume-*.csv"))
    rows = list(csv.DictReader(vol_files[-1].open(encoding="utf-8"))) if vol_files else targets()
    rows = sorted(rows, key=lambda r: -int(r.get("google_volume") or 0))[:top]
    out = []
    for r in rows:
        res = call(creds, "serp/google/organic/live/advanced", [{
            "keyword": r["keyword"], "location_code": US, "language_code": EN, "device": "desktop",
            "depth": 10, "load_async_ai_overview": True}])
        items = (res[0].get("items") if res else None) or []
        organic = [i for i in items if i.get("type") == "organic"]
        ours = next((i.get("rank_group") for i in organic if SITE in (i.get("domain") or "")), "")
        cited = sorted(set(refs([i for i in items if i.get("type") == "ai_overview"], [])))
        out.append({"keyword": r["keyword"], "our_rank": ours, "has_ai_overview": bool(cited) or any(i.get("type") == "ai_overview" for i in items),
                    "ai_overview_cites": " · ".join(cited), "we_are_cited": any(SITE in d for d in cited),
                    "top10": " · ".join(f"{i.get('rank_group')}. {i.get('domain')}" for i in organic[:10])})
        time.sleep(5)
    write(DATA / f"dfs-serp-{stamp}.csv", out, ["keyword", "our_rank", "has_ai_overview", "we_are_cited", "ai_overview_cites", "top10"])


def report(stamp):
    L = [f"# 📊 DataForSEO Insights · {stamp}", "", "- Google data via DataForSEO (US, English). Generated by `dfs_pull.py`.", ""]
    f = DATA / f"dfs-volume-{stamp}.csv"
    if f.exists():
        rows = sorted(csv.DictReader(f.open(encoding="utf-8")), key=lambda r: -int(r["google_volume"] or 0))
        def agg(field):
            t = {}
            for r in rows:
                t[r[field]] = t.get(r[field], 0) + int(r["google_volume"] or 0)
            return [f"| {k} | {v:,} |" for k, v in sorted(t.items(), key=lambda x: -x[1])]
        L += ["## 📦 Google demand by cluster (targets)", "", "| Cluster | Searches/mo |", "|---|---|"] + agg("cluster")
        L += ["", "## 🏷️ Google demand by vertical (targets)", "", "| Vertical | Searches/mo |", "|---|---|"] + agg("vertical")
        L += ["", "## 🎯 Targets by Google volume", "", "| Keyword | Searches/mo | Competition | CPC | Page |", "|---|---|---|---|---|"]
        L += [f"| {r['keyword']} | {int(r['google_volume'] or 0):,} | {r['competition']} | {r['cpc']} | {r['page']} |" for r in rows]
    for g in sorted(DATA.glob(f"dfs-gap-*-{stamp}.csv")):
        comp = g.name[8:-15].replace("_", ".")
        rows = list(csv.DictReader(g.open(encoding="utf-8")))[:20]
        L += ["", f"## 🕳️ Gap: top 20 in-scope keywords {comp} ranks for and we don't", "",
              "| Keyword | Searches/mo | Difficulty | Their rank |", "|---|---|---|---|"]
        L += [f"| {r['keyword']} | {int(r['volume'] or 0):,} | {r['difficulty']} | {r['competitor_rank']} |" for r in rows] or ["| none | | | |"]
    f = DATA / f"dfs-serp-{stamp}.csv"
    if f.exists():
        rows = list(csv.DictReader(f.open(encoding="utf-8")))
        cites = {}
        for r in rows:
            for d in filter(None, r["ai_overview_cites"].split(" · ")):
                cites[d] = cites.get(d, 0) + 1
        L += ["", "## 🤖 AI Overview citations (which sites Google's AI quotes)", "",
              f"- {sum(r['has_ai_overview'] == 'True' for r in rows)} of {len(rows)} keywords show an AI Overview. "
              f"We are cited on {sum(r['we_are_cited'] == 'True' for r in rows)}.", "", "| Cited domain | Times cited |", "|---|---|"]
        L += [f"| {d} | {n} |" for d, n in sorted(cites.items(), key=lambda x: -x[1])[:20]] or ["| none | |"]
        L += ["", "## 🏁 Who ranks (Google top 10)", "", "| Keyword | Our rank | Top 10 |", "|---|---|---|"]
        L += [f"| {r['keyword']} | {r['our_rank'] or '—'} | {r['top10']} |" for r in rows]
    out = DATA / f"dfs-insights-{stamp}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ Report → {out}")


def main():
    ap = argparse.ArgumentParser(description="DataForSEO pulls (paid per request).")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--volume", action="store_true")
    ap.add_argument("--gap", action="store_true")
    ap.add_argument("--serp", action="store_true")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    creds = auth()
    if a.check:
        res = call(creds, "appendix/user_data")
        print(f"✅ Access OK. DataForSEO balance: ${(res[0].get('money') or {}).get('balance', 0):.2f}")
        return
    if not (a.volume or a.gap or a.serp):
        sys.exit("Choose --volume, --gap, and/or --serp (or --check).")
    n_comp = len([l for l in (DATA / "competitors.txt").read_text(encoding="utf-8").splitlines()
                  if l.strip() and not l.startswith("#")]) if a.gap else 0
    print(f"Paid requests this run: {int(a.volume) + n_comp + (a.top if a.serp else 0)}")
    guard.dfs_check(EST_USD["volume"] * a.volume + EST_USD["gap"] * n_comp + EST_USD["serp"] * (a.top if a.serp else 0))
    stamp = date.today().isoformat()
    DATA.mkdir(exist_ok=True)
    if a.volume:
        print("Search volume (Google Ads data)…")
        volume(creds, stamp)
    if a.gap:
        print("Competitor keyword gaps…")
        gap(creds, stamp)
    if a.serp:
        print(f"SERP + AI Overview for top {a.top} targets…")
        serp(creds, stamp, a.top)
    report(stamp)
    print(f"💲 Cost of this run (reported by DataForSEO): ${spent:.4f}")


if __name__ == "__main__":
    main()
