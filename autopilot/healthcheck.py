"""
autopilot/healthcheck.py: daily site health check (AUTOPILOT.md §5.1 step 2). Read-only, public requests only.

    python -m autopilot.healthcheck                  # check, print a summary, record today's sitemap count
    python -m autopilot.healthcheck --init-baseline  # save today's robots tags as the baseline (after a planned change)

Checks:
  - HTTP 200 for the homepage, sitemap_index.xml, and every URL in the sitemaps (no redirects followed)
  - robots meta tag of every sitemap URL unchanged versus autopilot/baseline-robots.json
  - sitemap URL count versus the last recorded run (autopilot/health.json keeps 90 days)
Exit code 1 when there is an ALERT (site or page down, robots tag changed), so the routine can flag it.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
HERE = Path(__file__).resolve().parent
BASELINE = HERE / "baseline-robots.json"
HISTORY = HERE / "health.json"
KEEP_DAYS = 90
ROBOTS = re.compile(r'<meta name="robots" content="([^"]*)"')
LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
HEADERS = {"Cache-Control": "no-cache", "Pragma": "no-cache", "User-Agent": "ToolPickGuide-HealthCheck/1.0"}


def get(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=30, allow_redirects=False)
    except requests.RequestException as e:
        return type("Failed", (), {"status_code": f"error ({type(e).__name__})", "text": ""})()


def sitemap_urls(index_xml):
    urls = []
    for child in LOC.findall(index_xml):
        r = get(child)
        if r.status_code == 200:
            urls += LOC.findall(r.text)
    return sorted(set(u for u in urls if not u.endswith(".xml")))


def check():
    alerts, notes, robots = [], [], {}
    for url in (f"{SITE}/", f"{SITE}/sitemap_index.xml"):
        r = get(url)
        if r.status_code != 200:
            alerts.append(f"{url} returned {r.status_code}")
    index = get(f"{SITE}/sitemap_index.xml")
    urls = sitemap_urls(index.text) if index.status_code == 200 else []
    for url in urls:
        r = get(url)
        if r.status_code != 200:
            alerts.append(f"{url} returned {r.status_code}")
            continue
        m = ROBOTS.search(r.text)
        robots[url] = m.group(1) if m else "(no robots tag)"
    return urls, robots, alerts, notes


def compare_robots(robots, alerts, notes):
    if not BASELINE.is_file():
        notes.append("No robots baseline yet: run  python -m autopilot.healthcheck --init-baseline")
        return
    base = json.loads(BASELINE.read_text(encoding="utf-8"))["robots"]
    for url, tag in robots.items():
        if url in base and base[url] != tag:
            alerts.append(f"robots tag changed on {url}: '{base[url]}' → '{tag}'")
        elif url not in base:
            notes.append(f"new in sitemap (not in baseline): {url} [{tag}]")
    for url in sorted(set(base) - set(robots)):
        notes.append(f"left the sitemap since the baseline: {url}")


def main():
    ap = argparse.ArgumentParser(description="Daily site health check (read-only).")
    ap.add_argument("--init-baseline", action="store_true")
    a = ap.parse_args()
    now = datetime.now(timezone.utc)
    urls, robots, alerts, notes = check()

    if a.init_baseline:
        if alerts:
            sys.exit("Not saving a baseline while there are alerts:\n  " + "\n  ".join(alerts))
        BASELINE.write_text(json.dumps({"saved_at": now.isoformat(timespec="seconds"), "robots": robots},
                                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"✅ Baseline saved: {len(robots)} URL(s) → {BASELINE.relative_to(HERE.parent)}")
        return

    compare_robots(robots, alerts, notes)
    history = json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.is_file() else []
    if history and history[-1]["sitemap_urls"] != len(urls):
        notes.append(f"sitemap count {history[-1]['sitemap_urls']} → {len(urls)} since {history[-1]['date']} "
                     "(expected only after a publish or noindex)")
    today = now.date().isoformat()
    history = [h for h in history if h["date"] != today]
    history.append({"date": today, "sitemap_urls": len(urls), "alerts": len(alerts)})
    HISTORY.write_text(json.dumps(history[-KEEP_DAYS:], indent=2) + "\n", encoding="utf-8")

    print(f"Health check {today}: {len(urls)} sitemap URL(s), {len(alerts)} alert(s)")
    for line in alerts:
        print(f"  ALERT {line}")
    for line in notes:
        print(f"  note  {line}")
    if not alerts:
        print("  ✅ all pages 200, robots tags unchanged")
    sys.exit(1 if alerts else 0)


if __name__ == "__main__":
    main()
