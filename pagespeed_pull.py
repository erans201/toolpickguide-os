"""
pagespeed_pull.py: mobile Core Web Vitals for the top 20 pages (Google PageSpeed Insights API, free, read-only).

    python pagespeed_pull.py               # top 20 URLs → data/psi-<date>.csv + summary
    python pagespeed_pull.py --top 5       # fewer URLs
    python pagespeed_pull.py --url https://toolpickguide.com/some-page/

Key: PAGESPEED_API_KEY in .env (or the cloud environment); never printed. Without a key Google's shared
quota usually runs out after a few calls.
URL order: pages with the most impressions in the newest data/gsc-*-pages.csv, then the rest of the sitemap.

Columns:
  field_* = real Chrome users over 28 days (CrUX); empty when the site has too little traffic, which is normal for us
  lab_*   = one Lighthouse run on a simulated mid-range phone
Good thresholds: LCP ≤ 2.5 s · INP ≤ 200 ms · CLS ≤ 0.1 (lab uses TBT ≤ 200 ms as the INP stand-in).
"""

import argparse
import csv
import os
import re
import sys
from datetime import date
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
PSI = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
DATA = Path("data")
FIELDS = ["url", "perf_score", "lab_lcp_s", "lab_cls", "lab_tbt_ms", "field_lcp_s", "field_inp_ms", "field_cls",
          "field_category", "verdict"]


def api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    return os.getenv("PAGESPEED_API_KEY", "").strip()


def top_urls(n):
    """Live sitemap pages only (noindexed or retired pages are skipped), most impressions first."""
    live = []
    index = requests.get(f"{SITE}/sitemap_index.xml", timeout=30).text
    for child in re.findall(r"<loc>([^<]+)</loc>", index):
        if "post-sitemap" in child or "page-sitemap" in child:
            live += [u for u in re.findall(r"<loc>([^<]+)</loc>", requests.get(child, timeout=30).text)
                     if not u.endswith(".xml")]
    impressions = {}
    gsc = sorted(DATA.glob("gsc-*-pages.csv"))
    if gsc:
        with gsc[-1].open(encoding="utf-8") as f:
            impressions = {r["page"]: float(r["impressions"] or 0) for r in csv.DictReader(f)}
    ordered = sorted(dict.fromkeys(live), key=lambda u: -impressions.get(u, 0))
    return ordered[:n]


def measure(url, key):
    params = {"url": url, "strategy": "mobile", "category": "performance"}
    if key:
        params["key"] = key
    try:
        r = requests.get(PSI, params=params, timeout=120)
    except requests.RequestException as e:
        return {"url": url, "verdict": f"error ({type(e).__name__})"}
    if r.status_code == 429:
        sys.exit("ERROR: PageSpeed quota used up. Add PAGESPEED_API_KEY (TASKS.md T0.11) and run again.")
    if r.status_code != 200:
        msg = (r.json().get("error") or {}).get("message", "") if "json" in r.headers.get("content-type", "") else ""
        return {"url": url, "verdict": f"HTTP {r.status_code} {msg[:80]}".strip()}
    j = r.json()
    audits = j["lighthouseResult"]["audits"]
    field = (j.get("loadingExperience") or {}).get("metrics") or {}

    def pct(name):
        return (field.get(name) or {}).get("percentile")

    row = {
        "url": url,
        "perf_score": round((j["lighthouseResult"]["categories"]["performance"]["score"] or 0) * 100),
        "lab_lcp_s": round(audits["largest-contentful-paint"]["numericValue"] / 1000, 2),
        "lab_cls": round(audits["cumulative-layout-shift"]["numericValue"], 3),
        "lab_tbt_ms": round(audits["total-blocking-time"]["numericValue"]),
        "field_lcp_s": round(pct("LARGEST_CONTENTFUL_PAINT_MS") / 1000, 2) if pct("LARGEST_CONTENTFUL_PAINT_MS") else "",
        "field_inp_ms": pct("INTERACTION_TO_NEXT_PAINT") or "",
        "field_cls": round(pct("CUMULATIVE_LAYOUT_SHIFT_SCORE") / 100, 3) if pct("CUMULATIVE_LAYOUT_SHIFT_SCORE") is not None else "",
        "field_category": (j.get("loadingExperience") or {}).get("overall_category", ""),
    }
    fails = [name for name, bad in (("LCP", row["lab_lcp_s"] > 2.5), ("CLS", row["lab_cls"] > 0.1),
                                    ("TBT", row["lab_tbt_ms"] > 200)) if bad]
    row["verdict"] = "pass" if not fails else "fix " + "+".join(fails)
    return row


def main():
    ap = argparse.ArgumentParser(description="Mobile Core Web Vitals via PageSpeed Insights (read-only).")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--url", action="append")
    a = ap.parse_args()
    key = api_key()
    if not key:
        print("⚠️  No PAGESPEED_API_KEY: using Google's shared quota (may stop after a few pages).")
    urls = a.url or top_urls(a.top)
    DATA.mkdir(exist_ok=True)
    out = DATA / f"psi-{date.today().isoformat()}.csv"
    rows = []
    for i, url in enumerate(urls, 1):
        row = measure(url, key)
        rows.append(row)
        print(f"  {i:>2}/{len(urls)}  {row.get('perf_score', '–'):>3}  {row['verdict']:<14} {url.replace(SITE, '')}")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    measured = [r for r in rows if "perf_score" in r]
    passing = sum(r["verdict"] == "pass" for r in measured)
    print(f"\n✅ {out}: {len(measured)} page(s) measured, {passing} pass all lab thresholds.")


if __name__ == "__main__":
    main()
