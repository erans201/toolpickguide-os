"""
kp_ingest.py: turn Google Keyword Planner exports into a demand map for CONTENT_STRATEGY.md.

The user exports from Keyword Planner (Discover new keywords → Download keyword ideas → .csv) and drops
the file(s) in data/. No API, no login: this script only reads the files.

    python kp_ingest.py                        # every "Keyword Stats*.csv" / "kp-*.csv" in data/
    python kp_ingest.py data/myexport.csv      # specific files

Output: data/kp-<date>-keywords.csv (clean, de-duplicated) + data/kp-insights-<date>.md
  - demand per cluster (Option B scope) and per vertical
  - top keywords with volume, competition, CPC range, and the live page that probably owns them
  - unowned keywords = candidates for upgrades or Junia briefs (still run the topic gate + sitemap check)
"""

import csv
import io
import re
import sys
from datetime import date
from pathlib import Path

import requests

DATA = Path("data")
SITE = "https://toolpickguide.com"

CLUSTERS = [  # first match wins (order matters)
    ("CRM core", r"\bcrm\b|client management|customer management|practice management|case management|client portal|"
                 r"honeybook|dubsado|clio|mycase|practicepanther|taxdome|karbon|canopy|follow up boss|lofty|boldtrail|"
                 r"paperbell|studio ninja|sprout studio|pixieset|suitedash|client relationship"),
    ("Lifecycle spokes", r"form|e-?sign|signature|signing|onboarding|proposal|invoic|scheduling|booking|appointment|"
                         r"help ?desk|contract|questionnaire|intake|document collection|collect documents"),
    ("Web presence", r"website|site builder|landing page|\bwix\b|squarespace|webflow"),
    ("Out of scope", r"desk|chair|monitor|router|wifi|vpn|headphone|keyboard|laptop"),
]
VERTICALS = [("Legal", r"law|legal|attorney|lawyer"), ("Accounting", r"\bcpa\b|accountant|accounting|bookkeep|\btax"),
             ("Agencies", r"agenc"), ("Real estate", r"real estate|realtor|broker"), ("Photographers", r"photograph"),
             ("Coaches", r"coach|consultant")]
# Relevance filter: related-keyword sources (Bing) drift into navigational and off-topic searches.
RELEVANT = (r"crm|client management|practice management|case management|client portal (software|for)|portal software|"
            r"onboarding (software|checklist|process|template|tool)|client intake|intake form|form builder|lead (capture|form)|"
            r"e-?sign|electronic signature|digital signature|document signing|signing (software|tool|app)|website builder|"
            r"website (design )?for (small business|service|consult|coach|photograph|law|lawyer|attorney|accountant|cpa|"
            r"real estate|realtor|agenc|therapist|contractor)|how to (make|create|build) a (business )?website|scheduling (software|app|tool)|booking (software|system|app)|invoic\w* (software|app|tool)|"
            r"proposal (software|template|tool)|contract template|client questionnaire|transaction management|document collection|"
            r"honeybook|dubsado|clio|mycase|taxdome|karbon|canopy|follow up boss|paperbell|studio ninja|pixieset|suitedash|"
            r"practicepanther|smokeball|lawmatics|financial cents|calendly|docusign|pandadoc|jotform|typeform|squarespace|wix|webflow")
NOISE = (r"login|log in|sign in|\.com|\.gov|official|near me|customer service|phone|download|for sale|jobs?|salary|careers|"
         r"dmv|mvc|mva|quest|labcorp|irs|social security|ssa|uscis|visa|global entry|identogo|geek squad|"
         r"best buy|costco|walmart|cvs|walgreens|kroger|publix|meijer|hannaford|wells fargo|apple|genius bar|radiology|"
         r"patient|vaccin|flu shot|tire|dell|hp|bmc|secretary of state|driver license|rental|lease|employment|"
         r"construction|research proposal|church|nhd|church")
BRAND_ONLY = {"squarespace", "wix", "jotform", "jotforms", "honeybook", "honeybooks", "acuity", "scheduling", "website",
              "app", "the", "free", "clio", "software", "docusign", "calendly", "typeform", "webflow", "pandadoc"}


def relevant(kw):
    if re.search(NOISE, kw) or not re.search(RELEVANT, kw):
        return False
    return not set(kw.split()) <= BRAND_ONLY  # bare brand searches are navigational


STOP = {"best", "top", "for", "the", "a", "an", "and", "of", "to", "software", "tools", "tool", "app", "apps", "free",
        "online", "platform", "system", "systems", "program", "vs", "with", "in", "my", "small", "business", "businesses"}


def parse_volume(text):
    """'1K – 10K' → (1000, '1K – 10K'); '320' → (320, '320')."""
    raw = (text or "").strip()
    nums = re.findall(r"([\d.,]+)\s*([KkMm]?)", raw)
    if not nums:
        return 0, raw
    n, unit = nums[0]
    val = float(n.replace(",", "")) * {"k": 1e3, "m": 1e6}.get(unit.lower(), 1)
    return int(val), raw


def read_export(path):
    blob = path.read_bytes()
    for enc in ("utf-16", "utf-8-sig", "utf-8"):
        try:
            text = blob.decode(enc)
            if "Keyword" in text:
                break
        except UnicodeDecodeError:
            continue
    else:
        sys.exit(f"ERROR: cannot read {path.name} (not a Keyword Planner export?)")
    lines = text.splitlines()
    try:  # line 1 is a title ("Keyword Stats <date>…"), so match the real header row
        start = next(i for i, l in enumerate(lines) if l.lstrip('"').startswith("Keyword") and "monthly searches" in l)
    except StopIteration:
        sys.exit(f"ERROR: {path.name} has no 'Keyword … Avg. monthly searches' header (not a Keyword Planner export?)")
    body = "\n".join(lines[start:])
    delim = "\t" if body.split("\n")[0].count("\t") > body.split("\n")[0].count(",") else ","
    return list(csv.DictReader(io.StringIO(body), delimiter=delim))


def col(row, *names):
    for n in names:
        for k in row:
            if k and k.strip().lower().startswith(n.lower()):
                return (row[k] or "").strip()
    return ""


def tag(kw, rules, default):
    return next((name for name, rx in rules if re.search(rx, kw)), default)


def live_slugs():
    try:
        idx = requests.get(f"{SITE}/sitemap_index.xml", timeout=30).text
        urls = []
        for sm in re.findall(r"<loc>(.*?)</loc>", idx):
            if "post-sitemap" in sm or "page-sitemap" in sm:
                urls += re.findall(r"<loc>(.*?)</loc>", requests.get(sm, timeout=30).text)
        return [u.replace(SITE, "") for u in urls]
    except requests.RequestException:
        print("   ⚠️  sitemap not reachable: owner mapping uses Search Console data only")
        return []


def gsc_owners():
    files = sorted(DATA.glob("gsc-*-query_page.csv"))
    if not files:
        return {}
    with files[-1].open(encoding="utf-8") as f:
        best = {}
        for r in csv.DictReader(f):
            q, imp = r["query"].lower(), int(r["impressions"])
            if imp > best.get(q, ("", -1))[1]:
                best[q] = (r["page"].replace(SITE, ""), imp)
        return {q: p for q, (p, _) in best.items()}


def owner(kw, slugs, gsc):
    if kw in gsc:
        return gsc[kw], "GSC"
    words = [w for w in re.findall(r"[a-z0-9]+", kw) if w not in STOP]
    if not words:
        return "", ""
    variants = [words]
    if "crm" in words:  # live slugs use both "crm" and "client-management"
        variants.append([x for w in words for x in (("client", "management") if w == "crm" else (w,))])
    hits = [(sum(w in s for w in v) / len(v), s) for v in variants for s in slugs]
    score, slug = max(hits, default=(0, ""))
    return (slug, "slug match") if score >= 0.67 else ("", "")


def main():
    files = [Path(p) for p in sys.argv[1:]] or sorted(set(DATA.glob("Keyword Stats*.csv")) | set(DATA.glob("kp-*.csv")) -
                                                      set(DATA.glob("kp-*-keywords.csv")))
    if not files:
        sys.exit("No Keyword Planner exports found. Put the downloaded .csv in data/ (see data/README.md).")
    rows = {}
    for path in files:
        for r in read_export(path):
            kw = col(r, "Keyword").lower()
            if not kw:
                continue
            vol, raw = parse_volume(col(r, "Avg. monthly searches"))
            if kw in rows and rows[kw]["volume"] >= vol:
                continue
            rows[kw] = {"keyword": kw, "volume": vol, "volume_raw": raw, "competition": col(r, "Competition"),
                        "cpc_low": col(r, "Top of page bid (low"), "cpc_high": col(r, "Top of page bid (high"),
                        "change_3m": col(r, "Three month change"), "change_yoy": col(r, "YoY change"), "source_file": path.name}
        print(f"   read {path.name}")

    slugs, gsc = live_slugs(), gsc_owners()
    for r in rows.values():
        r["cluster"] = tag(r["keyword"], CLUSTERS, "Unclassified")
        r["vertical"] = tag(r["keyword"], VERTICALS, "General")
        r["owner_page"], r["owner_basis"] = owner(r["keyword"], slugs, gsc)
        r["relevant"] = relevant(r["keyword"])
    everything = sorted(rows.values(), key=lambda r: -r["volume"])
    ranked = [r for r in everything if r["relevant"]]
    if not ranked:
        sys.exit("No relevant keywords after filtering.")

    stamp = date.today().isoformat()
    DATA.mkdir(exist_ok=True)
    out_csv = DATA / f"kp-{stamp}-keywords.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(everything[0]))
        w.writeheader()
        w.writerows(everything)

    def table(title, key):
        agg = {}
        for r in ranked:
            a = agg.setdefault(r[key], [0, 0])
            a[0] += 1
            a[1] += r["volume"]
        out = [f"## {title}", "", "| Group | Keywords | Monthly searches (sum of low bounds) |", "|---|---|---|"]
        return out + [f"| {k} | {n} | {v:,} |" for k, (n, v) in sorted(agg.items(), key=lambda x: -x[1][1])] + [""]

    L = [f"# 🔑 Keyword Demand Map · {stamp}", "",
         f"- **Files:** {', '.join(p.name for p in files)} · **Keywords:** {len(everything):,} pulled → "
         f"**{len(ranked):,} relevant** (navigational, brand-only and off-topic searches filtered out; all rows stay in the CSV)",
         ("- **Source: Bing Webmaster Tools** (Bing-only searches/month, US). Compare topics with it; Google volumes are larger. "
          if any("bing" in p.name for p in files) else "- Source: Google Keyword Planner averages. ") +
         "Ranges ('1K – 10K') count as their low bound. "
         "Owner pages are suggestions: confirm against the sitemap before acting.", ""]
    L += table("📦 Demand by cluster (Option B scope)", "cluster") + table("🏷️ Demand by vertical", "vertical")
    L += ["## 🏆 Top 40 keywords", "", "| Keyword | Searches | Competition | CPC (low–high) | Cluster | Owner page |", "|---|---|---|---|---|---|"]
    L += [f"| {r['keyword']} | {r['volume_raw']} | {r['competition']} | {r['cpc_low']}–{r['cpc_high']} | {r['cluster']} | "
          f"{('`' + r['owner_page'] + '`') if r['owner_page'] else '—'} |" for r in ranked[:40]]
    unowned = [r for r in ranked if not r["owner_page"] and r["cluster"] not in ("Out of scope", "Unclassified")][:30]
    L += ["", "## 🆕 In-scope keywords with no owner page (candidates)",
          "Each one still goes through the topic gate (CONTENT_STRATEGY.md) and a sitemap check before a brief.", "",
          "| Keyword | Searches | Competition | Cluster | Vertical |", "|---|---|---|---|---|"]
    L += [f"| {r['keyword']} | {r['volume_raw']} | {r['competition']} | {r['cluster']} | {r['vertical']} |" for r in unowned] or ["| none | | | | |"]
    out_md = DATA / f"kp-insights-{stamp}.md"
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {len(ranked)} keywords → {out_csv}\n✅ Report → {out_md}")


if __name__ == "__main__":
    main()
