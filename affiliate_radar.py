"""
affiliate_radar.py: which tools we recommend that could earn us money, and how much people search for them (free,
read-only). User decision 2026-10-23: "add the affiliate step ... combined with the keyword research process, both
should communicate with each other back and forth" (AUTOPILOT.md 5.2 step 2e).

    python affiliate_radar.py            # crawl live pages → data/affiliate-radar.csv + data/affiliate-radar-<date>.md

What it does:
  1. Reads every live URL from the sitemaps and collects the outside sites each page links to (vendor candidates),
     counting pages per domain and pages where the link is already an affiliate link (rel="sponsored").
  2. Demand: sums the Google volume of data/keyword-bank.csv keywords that contain the brand (from the keyword harvest).
  3. Keeps the hand-filled columns (brand, status, program, commission, ...) from the previous data/affiliate-radar.csv,
     so the robot's research survives every run. New domains start as status "new".
  4. Priority = demand + 300 x pages, for rows still worth researching (new / program-found / owner-to-apply / rejected-retry).

The other direction: kw_harvest.py reads this file and seeds "<brand> review / pricing / alternatives" for brands
with a program, so the keyword research finds content topics where we can earn.
Statuses: new · not-a-vendor · no-program · program-found · owner-to-apply · applied · approved · link-placed · rejected-retry
"""

import csv
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests

SITE = "https://toolpickguide.com"
DATA = Path("data")
RADAR = DATA / "affiliate-radar.csv"
BANK = DATA / "keyword-bank.csv"
FIELDS = ["domain", "brand", "pages", "sponsored_pages", "demand", "priority", "status", "program_url", "network",
          "commission", "cookie", "checked", "notes", "example_page"]
KEEP = ["brand", "status", "program_url", "network", "commission", "cookie", "checked", "notes"]
RESEARCH = {"new", "program-found", "owner-to-apply", "rejected-retry"}
# Sources and platforms we cite or embed, never vendors we could earn from
SKIP = re.compile(r"(^|\.)(gov|edu|wikipedia|google|youtube|youtu|linkedin|facebook|twitter|x|instagram|pinterest|"
                  r"reddit|quora|pexels|unsplash|pixabay|wordpress|wp|gravatar|rankmath|schema|w3|github|forbes|"
                  r"nytimes|cnbc|investopedia|americanbar|nar|irs|clarity|cloudflare|gstatic|googleapis|whatsapp|"
                  r"telegram|tumblr|toolpickguide)\.[a-z.]+$|\.gov$|\.edu$")
UA = {"User-Agent": "Mozilla/5.0 (ToolPickGuide affiliate radar)"}


def live_urls():
    urls = []
    for sm in ("post-sitemap.xml", "page-sitemap.xml"):
        xml = requests.get(f"{SITE}/{sm}", headers=UA, timeout=60).text
        urls += re.findall(r"<loc>(https://toolpickguide\.com/[^<]+)</loc>", xml)
    return [u for u in dict.fromkeys(urls) if not re.search(r"\.(jpg|png|webp)$", u)]


def article_html(html):
    m = re.search(r'<div class="entry-content[^"]*"[^>]*>(.*?)<footer', html, re.S)
    return m.group(1) if m else html


def domain_of(url):
    host = urlparse(url).netloc.lower().split(":")[0]
    parts = host.split(".")
    return ".".join(parts[-3:] if len(parts) > 2 and parts[-2] in ("co", "com") else parts[-2:])  # vendor root domain


def brand_guess(domain):
    label = domain.split(".")[-2] if domain.count(".") >= 1 else domain
    return re.sub(r"^(get|try|use|go)(?=[a-z]{4,})", "", label)


def main():
    old = {r["domain"]: r for r in csv.DictReader(RADAR.open(encoding="utf-8"))} if RADAR.exists() else {}
    bank = list(csv.DictReader(BANK.open(encoding="utf-8"))) if BANK.exists() else []
    found = {}
    urls = live_urls()
    for u in urls:
        try:
            html = article_html(requests.get(u, headers=UA, timeout=60).text)
        except requests.RequestException:
            continue
        seen = {}
        for tag in re.findall(r"<a\s[^>]*href=\"https?://[^\"]+\"[^>]*>", html):
            d = domain_of(re.search(r'href="([^"]+)"', tag).group(1))
            if not d or SKIP.search(d):
                continue
            seen[d] = seen.get(d, False) or "sponsored" in tag
        for d, spons in seen.items():
            r = found.setdefault(d, {"domain": d, "pages": 0, "sponsored_pages": 0, "example_page": u})
            r["pages"] += 1
            r["sponsored_pages"] += int(spons)
    rows = []
    for d in sorted(set(found) | set(old)):
        r = {f: "" for f in FIELDS} | old.get(d, {}) | found.get(d, {"pages": 0, "sponsored_pages": 0})
        for k in KEEP:
            r[k] = old.get(d, {}).get(k, "")
        r["brand"] = r["brand"] or brand_guess(d)
        r["status"] = r["status"] or "new"
        if r["sponsored_pages"] and r["status"] in RESEARCH | {"applied", "approved"}:
            r["status"] = "link-placed"
        b = r["brand"].lower()
        r["demand"] = sum(int(float(k["volume"] or 0)) for k in bank if b and b.replace(" ", "") in k["keyword"].lower().replace(" ", ""))
        r["priority"] = (r["demand"] + 300 * int(r["pages"])) if r["status"] in RESEARCH else 0
        rows.append(r)
    rows.sort(key=lambda r: (-int(r["priority"]), -int(r["pages"]), r["domain"]))
    with RADAR.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    today = date.today().isoformat()
    todo = [r for r in rows if int(r["priority"]) > 0][:15]
    L = [f"# Affiliate radar · {today}", "",
         f"- {len(urls)} live pages crawled; {len(rows)} outside domains; {sum(r['status'] == 'link-placed' for r in rows)} with affiliate links placed.",
         "- Priority = keyword demand (data/keyword-bank.csv) + 300 x pages that link to the vendor. How the weekly robot uses it: AUTOPILOT.md 5.2 step 2e.",
         "", "## Research next (highest priority first)", "",
         "| domain | brand | pages | demand | priority | status | example page |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r['domain']} | {r['brand']} | {r['pages']} | {r['demand']} | {r['priority']} | {r['status']} | {r['example_page']} |" for r in todo]
    ready = [r for r in rows if r["status"] == "owner-to-apply"]
    L += ["", "## Ready for the owner to apply (account + terms are the owner's)", ""]
    L += [f"- {r['brand']}: {r['program_url']} ({r['commission'] or 'commission n/a'}; {r['network'] or 'direct'})" for r in ready] or ["(none)"]
    out = DATA / f"affiliate-radar-{today}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {len(urls)} pages · {len(rows)} domains → {RADAR} + {out}")


if __name__ == "__main__":
    main()
