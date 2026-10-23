"""
kw_harvest.py: continuous keyword harvesting with DataForSEO (paid, read-only data) → data/keyword-bank.csv +
data/kw-insights-<date>.md. User decision 2026-10-13: "an ongoing process in which the robot discovers new keywords,
provides insights over those keywords and spies competitors to facilitate the blog content strategy; do the same with
existing keywords" (defaults approved: approved scope only, US/English, robot adds topics itself, $10/month).

    python kw_harvest.py --discover     # new keyword ideas from rotating seeds (our focus keywords + bank)     1 request
    python kw_harvest.py --ours         # every keyword toolpickguide.com ranks for (rank tracking)               1 request
    python kw_harvest.py --spy          # what each domain in data/competitors.txt ranks for                    1 per domain
    python kw_harvest.py --competitors  # who else wins the bank's biggest keywords (new-competitor candidates)  1 request
    python kw_harvest.py --all          # all four, then the insights report
    python kw_harvest.py --report       # free: rebuild the insights report from the bank

The bank keeps one row per keyword: Google volume, 3-month trend, CPC, difficulty, intent, our rank/URL, the page that
owns it, the best competitor, sources, first/last seen. Owner page: the URL we rank with, else data/target-keywords.csv,
else a live page cannibal_check.py says covers it (STRONG). Only keywords inside our scope (kp_ingest.relevant) are kept.
Autopilot (TPG_AUTOPILOT=1): the guard stops the run if the month's DataForSEO spend would pass the cap.
"""

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

import cannibal_check as cc
import dfs_pull as dfs
import kp_ingest as kpi
from autopilot import guard

DATA = Path("data")
BANK = DATA / "keyword-bank.csv"
FIELDS = ["keyword", "vertical", "volume", "trend_3m_pct", "cpc", "difficulty", "intent", "our_rank", "our_url",
          "prev_our_rank", "owner_page", "best_competitor", "competitor_rank", "sources", "first_seen", "last_seen"]
EST_USD = 0.06  # cautious per-request estimate for DataForSEO Labs (task fee + returned items)
SEEDS_PER_RUN = 20
# Outside the client-operations scope even when kp_ingest.relevant() matches (e.g. "employee scheduling software")
OFF_SCOPE = re.compile(r"employee|staff|workforce|shift|payroll|\bhr\b|human resource|project management|inventory|"
                       r"\bpos\b|restaurant|school|church|medical|dental|clinic|health ?care|patient|hospital|"
                       r"construction|field service|warehouse|fleet|manufactur")
LIMIT = 300


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def trend(monthly):
    """% change of the last 3 months vs the 3 before (monthly = DataForSEO monthly_searches, newest first)."""
    vals = [m.get("search_volume") for m in sorted(monthly or [], key=lambda m: (m.get("year", 0), m.get("month", 0)),
                                                       reverse=True) if m.get("search_volume") is not None]
    if len(vals) < 6 or sum(vals[3:6]) == 0:
        return ""
    return round(100 * (sum(vals[:3]) - sum(vals[3:6])) / sum(vals[3:6]))


def facts(kd):
    """Keyword facts from a DataForSEO Labs keyword object (keyword_ideas item or ranked_keywords keyword_data)."""
    info, props = kd.get("keyword_info") or {}, kd.get("keyword_properties") or {}
    return {"keyword": (kd.get("keyword") or "").lower().strip(), "volume": info.get("search_volume") or "",
            "trend_3m_pct": trend(info.get("monthly_searches")), "cpc": round(info["cpc"], 2) if info.get("cpc") else "",
            "difficulty": props.get("keyword_difficulty") or "",
            "intent": (kd.get("search_intent_info") or {}).get("main_intent") or ""}


def load_bank():
    if not BANK.exists():
        return {}
    return {r["keyword"]: r for r in csv.DictReader(BANK.open(encoding="utf-8")) if not OFF_SCOPE.search(r["keyword"])}


def save_bank(bank):
    DATA.mkdir(exist_ok=True)
    rows = sorted(bank.values(), key=lambda r: -(num(r.get("volume")) or 0))
    with BANK.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def upsert(bank, today, kw_facts, source, **extra):
    k = kw_facts["keyword"]
    if not k or not kpi.relevant(k) or OFF_SCOPE.search(k):
        return False
    row = bank.setdefault(k, {f: "" for f in FIELDS} | {"keyword": k, "first_seen": today})
    for key, val in kw_facts.items():
        if val not in ("", None):
            row[key] = val
    for key, val in extra.items():
        if val not in ("", None):
            row[key] = val
    row["vertical"] = kpi.tag(k, kpi.VERTICALS, "General")
    row["sources"] = " · ".join(sorted(set(filter(None, row.get("sources", "").split(" · "))) | {source}))
    row["last_seen"] = today
    return True


def competitors():
    return [l.strip() for l in (DATA / "competitors.txt").read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def seeds(bank):
    """Our own focus keywords first, then the bank's oldest-checked big keywords: the seed list rotates every run."""
    own = [r["keyword"] for r in csv.DictReader((DATA / "target-keywords.csv").open(encoding="utf-8"))]
    for f in Path("knowledge/briefs/junia").glob("*.md"):
        own.append(dfs_focus(f))
    own = brand_seeds() + own
    pool = list(dict.fromkeys(k for k in own if k))
    rest = sorted((r for r in bank.values() if r["keyword"] not in pool),
                  key=lambda r: (r.get("last_seen", ""), -(num(r.get("volume")) or 0)))
    pool += [r["keyword"] for r in rest]
    start = date.today().toordinal() // 7 * SEEDS_PER_RUN % max(len(pool), 1)  # rotate weekly
    return (pool[start:] + pool[:start])[:SEEDS_PER_RUN]


def brand_seeds(limit=3):
    """The affiliate radar's side of the loop (AUTOPILOT.md 5.2 step 2e): brands with a program we can earn from
    (program-found / owner-to-apply / applied / approved / link-placed) seed review, pricing and alternatives keywords,
    a few brands per week in rotation, so the harvest finds the content topics that pay."""
    f = DATA / "affiliate-radar.csv"
    if not f.exists():
        return []
    earn = {"program-found", "owner-to-apply", "applied", "approved", "link-placed"}
    brands = list(dict.fromkeys(r["brand"].strip().lower() for r in csv.DictReader(f.open(encoding="utf-8"))
                                if r.get("status") in earn and r.get("brand")))
    if not brands:
        return []
    start = date.today().toordinal() // 7 * limit % len(brands)
    pick = (brands[start:] + brands[:start])[:limit]
    return [f"{b} {s}" for b in pick for s in ("review", "pricing", "alternatives")]


QUESTION = re.compile(r"^(how|what|why|when|which|who|can|do|does|is|are|should|will)\b")


def dfs_focus(path):
    m = re.search(r"^\| Focus keyword \| (.+?) \|", path.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip().lower() if m else ""


def labs(creds, endpoint, body):
    res = dfs.call(creds, f"dataforseo_labs/google/{endpoint}/live",
                   [body | {"location_code": dfs.US, "language_code": dfs.EN}])
    return ((res[0] if res else {}) or {}).get("items") or []


def discover(creds, bank, today):
    items = labs(creds, "keyword_ideas", {"keywords": seeds(bank), "limit": LIMIT})
    return sum(upsert(bank, today, facts(i), "ideas") for i in items)


def ranked(creds, domain):
    return labs(creds, "ranked_keywords", {"target": domain, "limit": LIMIT})


def ours(creds, bank, today):
    for r in bank.values():  # keep last run's rank for the movement report
        r["prev_our_rank"] = r.get("our_rank", "")
        r["our_rank"], r["our_url"] = "", ""
    n = 0
    for i in ranked(creds, dfs.SITE):
        serp = (i.get("ranked_serp_element") or {}).get("serp_item") or {}
        n += upsert(bank, today, facts(i.get("keyword_data") or {}), "ours",
                    our_rank=serp.get("rank_group"), our_url=serp.get("relative_url") or serp.get("url"))
    return n


def spy(creds, bank, today):
    n = 0
    for dom in competitors():
        for i in ranked(creds, dom):
            serp = (i.get("ranked_serp_element") or {}).get("serp_item") or {}
            f = facts(i.get("keyword_data") or {})
            rank = serp.get("rank_group")
            cur = bank.get(f["keyword"], {})
            better = rank and (not num(cur.get("competitor_rank")) or rank < num(cur.get("competitor_rank")))
            n += upsert(bank, today, f, f"spy:{dom}",
                        **({"best_competitor": dom, "competitor_rank": rank} if better else {}))
    return n


def serp_competitors(creds, bank, today):
    top = sorted(bank.values(), key=lambda r: -(num(r.get("volume")) or 0))[:20]
    items = labs(creds, "serp_competitors", {"keywords": [r["keyword"] for r in top], "limit": 30})
    known = set(competitors()) | {dfs.SITE}
    out = [{"domain": i.get("domain"), "avg_position": i.get("avg_position"), "etv": i.get("etv"),
            "keywords": i.get("keywords_count")} for i in items if i.get("domain") not in known]
    write_csv(DATA / f"kw-competitor-candidates-{today}.csv", out, ["domain", "avg_position", "etv", "keywords"])
    return len(out)


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def assign_owners(bank):
    targets = {r["keyword"]: r["page"] for r in csv.DictReader((DATA / "target-keywords.csv").open(encoding="utf-8"))
               if r.get("page", "").startswith("/")}
    try:
        pages = cc.live_pages()
    except Exception:  # network trouble: keep last owners
        pages = []
    for r in bank.values():
        if r.get("our_url"):
            r["owner_page"] = "/" + r["our_url"].split("toolpickguide.com", 1)[-1].strip("/") + "/"
        elif r["keyword"] in targets:
            r["owner_page"] = targets[r["keyword"]]
        elif pages:
            # STRONG = the page covers it; REVIEW = a narrower variation of the page (expand that page, no new article)
            hit = cc.conflicts({"slug": "", "focus": r["keyword"], "secondary": []}, pages, [], set())
            r["owner_page"] = f"/{hit[0][2]}/" if hit else ""


def score(r):
    """Opportunity score: demand, weighted up by CPC (money) and down by difficulty."""
    v, c, d = num(r.get("volume")) or 0, num(r.get("cpc")) or 0, num(r.get("difficulty")) or 30
    return round(v * (1 + min(c, 50) / 10) / (1 + d / 20), 1)


def distinct(rows, limit):
    """One row per topic: variants with the same meaning words (cannibal_check.words) collapse into the biggest one,
    which lists how many variants it stands for."""
    seen, out = {}, []
    for r in rows:
        key = frozenset(cc.words(r["keyword"]))
        if key in seen:
            seen[key]["variants"] += 1
            continue
        r = dict(r, variants=1)
        seen[key] = r
        out.append(r)
    return out[:limit]


def report(bank, today, note=""):
    rows = list(bank.values())
    for r in rows:
        r["score"] = score(r)
    vol = lambda r: num(r.get("volume")) or 0  # noqa: E731
    rank = lambda r: num(r.get("our_rank"))  # noqa: E731
    new_opps = distinct(sorted([r for r in rows if not r.get("owner_page") and vol(r) >= 50],
                               key=lambda r: -r["score"]), 20)
    expand = distinct(sorted([r for r in rows if r.get("owner_page") and (not rank(r) or rank(r) > 20) and vol(r) >= 50],
                             key=lambda r: -r["score"]), 15)
    striking = sorted([r for r in rows if rank(r) and 11 <= rank(r) <= 30], key=lambda r: -vol(r))[:15]
    moves = sorted([r for r in rows if rank(r) and num(r.get("prev_our_rank"))
                    and abs(num(r["prev_our_rank"]) - rank(r)) >= 3],
                   key=lambda r: rank(r) - num(r["prev_our_rank"]))[:15]
    gaps = distinct(sorted([r for r in rows if r.get("best_competitor") and (num(r.get("competitor_rank")) or 99) <= 10
                            and not rank(r)], key=lambda r: -vol(r)), 15)
    questions = sorted([r for r in rows if QUESTION.search(r["keyword"]) and vol(r) >= 20], key=lambda r: -vol(r))[:15]
    rising = sorted([r for r in rows if (num(r.get("trend_3m_pct")) or 0) >= 25 and vol(r) >= 30],
                    key=lambda r: -(num(r.get("trend_3m_pct")) or 0))[:10]

    def table(title, items, cols):
        out = [f"## {title}", ""]
        if not items:
            return out + ["(none)", ""]
        out += ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        out += ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in items]
        return out + [""]

    cand = sorted(DATA.glob("kw-competitor-candidates-*.csv"))
    L = [f"# Keyword harvest insights · {today}", "",
         f"- Bank: {len(rows)} in-scope keywords ({sum(r.get('first_seen') == today for r in rows)} new today), "
         f"{sum(bool(r.get('our_rank')) for r in rows)} where we rank. {note}",
         "- Score = volume x (1 + CPC/10) / (1 + difficulty/20). Owner = the page that ranks or covers the keyword.",
         "- How the weekly robot applies this: AUTOPILOT.md 5.2 step 2d.", ""]
    L += table("1. New topic opportunities (no page owns them)", new_opps,
               ["keyword", "variants", "vertical", "volume", "cpc", "difficulty", "intent", "trend_3m_pct", "score"])
    L += table("2. Expand existing pages (the owner page doesn't rank top 20 yet)", expand,
               ["keyword", "variants", "owner_page", "volume", "difficulty", "our_rank", "score"])
    L += table("3. Striking distance (we rank 11-30)", striking, ["keyword", "our_rank", "our_url", "volume"])
    L += table("4. Rank moves since last run (3+ places)", moves, ["keyword", "prev_our_rank", "our_rank", "our_url"])
    L += table("5. Competitor gaps (a competitor is top 10, we don't rank)", gaps,
               ["keyword", "best_competitor", "competitor_rank", "volume", "owner_page"])
    L += table("6. Rising searches (+25% or more over 3 months)", rising, ["keyword", "trend_3m_pct", "volume"])
    L += table("6b. Questions people ask (FAQ answers on the owner page, or a TOFU topic when no page owns them)",
               questions, ["keyword", "volume", "owner_page", "our_rank"])
    if cand:
        c = list(csv.DictReader(cand[-1].open(encoding="utf-8")))[:8]
        L += table(f"7. New competitor candidates ({cand[-1].name})", c, ["domain", "avg_position", "etv", "keywords"])
    out = DATA / f"kw-insights-{today}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ Report → {out}")


def main():
    ap = argparse.ArgumentParser(description="Continuous keyword harvesting (DataForSEO, paid per request).")
    for flag in ("discover", "ours", "spy", "competitors", "all", "report"):
        ap.add_argument(f"--{flag}", action="store_true")
    a = ap.parse_args()
    if a.all:
        a.discover = a.ours = a.spy = a.competitors = True
    today = date.today().isoformat()
    bank = load_bank()
    jobs = [(a.discover, 1), (a.ours, 1), (a.spy, len(competitors()) if a.spy else 0), (a.competitors, 1)]
    n_req = sum(n for on, n in jobs if on)
    if not n_req and not a.report:
        sys.exit("Choose --discover, --ours, --spy, --competitors, --all or --report.")
    if n_req:
        print(f"Paid requests this run: {n_req} (estimate ${EST_USD * n_req:.2f})")
        guard.dfs_check(EST_USD * n_req)
        creds = dfs.auth()
        if a.ours:
            print(f"   ours: {ours(creds, bank, today)} keywords where we rank")
        if a.discover:
            print(f"   discover: {discover(creds, bank, today)} in-scope ideas")
        if a.spy:
            print(f"   spy: {spy(creds, bank, today)} in-scope competitor keywords")
        if a.competitors:
            print(f"   competitors: {serp_competitors(creds, bank, today)} candidate domains")
        assign_owners(bank)
        save_bank(bank)
        print(f"💲 Cost of this run (reported by DataForSEO): ${dfs.spent:.4f}")
    report(bank, today, note=f"Run cost ${dfs.spent:.2f}." if n_req else "")


if __name__ == "__main__":
    main()
