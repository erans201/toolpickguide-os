"""
clarity_pull.py: read-only daily pull of Microsoft Clarity behavior metrics per page (user decision 2026-10-09:
judge articles by user behavior too; knowledge/content-test.md).

    python clarity_pull.py            # yesterday's metrics per URL -> data/clarity-<date>.json + data/clarity-daily.csv
    python clarity_pull.py --check    # token test, prints only OK / error

Clarity's Data Export API returns only the last 1-3 days and allows 10 calls per project per day, so the daily
robot runs this once a day and the CSV accumulates the history. Token: CLARITY_API_TOKEN in .env (or the cloud
environment), never printed. Clarity → Settings → Data Export → Generate new API token.
"""

import argparse
import csv
import datetime as dt
import json
import os
import sys
from pathlib import Path

import requests

API = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
DATA = Path("data")


def token():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    t = os.environ.get("CLARITY_API_TOKEN", "").strip()
    if not t:
        sys.exit("ERROR: CLARITY_API_TOKEN is not set (.env or environment).")
    return t


def fetch(tok, days=1):
    r = requests.get(API, params={"numOfDays": days, "dimension1": "URL"},
                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, timeout=60)
    if r.status_code != 200:
        sys.exit(f"ERROR: Clarity API HTTP {r.status_code}: {r.text[:200].replace(tok, '[REDACTED]')}")
    return r.json()


def flatten(day, payload):
    """One CSV row per (metric, URL); every numeric field the API gives is kept as-is."""
    rows = []
    for block in payload if isinstance(payload, list) else []:
        metric = block.get("metricName", "")
        for info in block.get("information", []):
            url = info.get("Url") or info.get("URL") or info.get("url") or ""
            for key, val in info.items():
                if key.lower() == "url":
                    continue
                rows.append({"date": day, "metric": metric, "url": url, "field": key, "value": val})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    tok = token()
    payload = fetch(tok)
    if a.check:
        print("✅ Clarity API OK")
        return
    day = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    DATA.mkdir(exist_ok=True)
    (DATA / f"clarity-{day}.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
    rows = flatten(day, payload)
    out = DATA / "clarity-daily.csv"
    new = not out.exists()
    with out.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "metric", "url", "field", "value"])
        if new:
            w.writeheader()
        w.writerows(rows)
    print(f"✅ Clarity {day}: {len(rows)} rows -> {out}")


if __name__ == "__main__":
    main()
