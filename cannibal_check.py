"""
cannibal_check.py: read-only check that no new article competes with a live page or with another brief for the
same search intent (CLAUDE.md "No cannibalization"; user rule 2026-10-09: "avoid the situation of articles
competing each other").

    python cannibal_check.py                          # every brief that is not live yet, against live pages + other briefs
    python cannibal_check.py --brief knowledge/briefs/junia/<slug>.md

How it compares: the brief's focus keyword (and its secondary keywords) become a set of meaning words (plurals
folded, filler words like "best", "software", "2026" dropped, "crm" = "client management"). Each set is compared
with every live page (title + slug, plus the focus keyword in its knowledge/upgrade-* file) and every other brief.
  STRONG  same words (overlap >= 0.67, or the new topic's words all inside an existing page's): the topic competes. Skip, merge or
          re-angle it. publish_draft.py refuses to publish a STRONG match with a live page.
  REVIEW  overlap >= 0.5, the new topic is a narrower spoke of a page, or a secondary keyword is a STRONG
          match: judge by intent.
A judged pair that is fine goes into knowledge/cannibal-ok.txt as "slug-a slug-b  # reason"; it is then skipped.
Exit code 1 when an unresolved STRONG match exists.
"""

import argparse
import re
import sys
from pathlib import Path

import requests

import junia_draft as jd

SITE = jd.SITE
OK_FILE = Path("knowledge/cannibal-ok.txt")
FILLER = {"best", "top", "software", "tool", "tools", "app", "apps", "platform", "guide", "the", "a", "an", "for",
          "and", "or", "of", "to", "in", "on", "with", "your", "you", "what", "is", "how", "vs", "versus", "2025",
          "2026", "2027", "compared", "ranked", "picks", "review", "reviews", "free", "small", "business",
          "businesses", "s"}
SYNONYMS = {"crm": ["client", "management"], "pm": ["practice", "management"], "lawyer": ["law"], "attorney": ["law"],
            "legal": ["law"], "realtor": ["real", "estate"], "accountant": ["accounting"], "cpa": ["accounting"]}


def stem(w):
    if len(w) > 6 and w.endswith("ing"):  # coaching = coach, onboarding = onboard (same on both sides)
        return w[:-3]
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and re.search(r"(ch|sh|x|ss)es$", w):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def words(text):
    out = set()
    for w in re.findall(r"[a-z0-9]+", (text or "").lower().replace("-", " ")):
        w = stem(w)
        for x in SYNONYMS.get(w, [w]):
            if x not in FILLER:
                out.add(x)
    return out


def level(a, b):
    """a = the new topic, b = an existing page or brief. a fully inside b = b already covers it (STRONG);
    b inside a = a is a narrower spoke of b (REVIEW: usually fine, link it up to b)."""
    if not a or not b:
        return None, 0.0
    j = len(a & b) / len(a | b)
    if j >= 0.67 or (len(a) >= 2 and a <= b):
        return "STRONG", j
    if j >= 0.5 or (len(b) >= 2 and b <= a):
        return "REVIEW", j
    return None, j


def ok_pairs():
    pairs = set()
    if OK_FILE.exists():
        for line in OK_FILE.read_text(encoding="utf-8").splitlines():
            parts = line.split("#")[0].split()
            if len(parts) >= 2:
                pairs.add(frozenset(parts[:2]))
    return pairs


def live_pages():
    """[(slug, label, word sets)] for every published post and page."""
    focus = {}
    for f in Path("knowledge").glob("upgrade-*.md"):
        t = f.read_text(encoding="utf-8")
        s = re.search(r"^\| Slug \| `?/?([a-z0-9-]+)/?`? \|", t, re.M)
        k = re.search(r"^\| Focus keyword \| (.+?) \|", t, re.M)
        if s and k:
            focus[s.group(1)] = k.group(1)
    pages = []
    for kind in ("posts", "pages"):
        n = 1
        while True:
            r = requests.get(f"{SITE}/wp-json/wp/v2/{kind}", params={"per_page": 100, "page": n,
                             "_fields": "slug,title"}, timeout=60)
            if r.status_code != 200 or not r.json():
                break
            for p in r.json():
                title = re.sub(r"<[^>]+>|&[#a-z0-9]+;", " ", p["title"]["rendered"])
                sets = [words(title), words(p["slug"])]
                if p["slug"] in focus:
                    sets.append(words(focus[p["slug"]]))
                pages.append((p["slug"], title.strip(), sets))
            n += 1
    return pages


def brief_sets(b):
    return words(b["focus"]), [words(s) for s in b.get("secondary", [])]


def conflicts(brief, pages, briefs, oks=None):
    """[(level, kind, other slug, label, overlap)] for one parsed brief."""
    oks = ok_pairs() if oks is None else oks
    main, secondary = brief_sets(brief)
    out = []
    targets = [("live page", s, label, sets) for s, label, sets in pages]
    targets += [("brief", o["slug"], o["focus"], [brief_sets(o)[0]]) for o in briefs]
    for kind, slug, label, sets in targets:
        if slug == brief["slug"] or frozenset((slug, brief["slug"])) in oks:
            continue
        rank = {"STRONG": 2, "REVIEW": 1, None: 0}
        best_lv, best_j = None, 0.0
        for ws in sets:
            lv, j = level(main, ws)
            if (rank[lv], j) > (rank[best_lv], best_j):
                best_lv, best_j = lv, j
            if best_lv is None and any(level(sec, ws)[0] == "STRONG" for sec in secondary):
                best_lv = "REVIEW"
        if best_lv:
            out.append((best_lv, kind, slug, label, round(best_j, 2)))
    return sorted(out, key=lambda c: (c[0] != "STRONG", -c[4]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief")
    a = ap.parse_args()
    pages = live_pages()
    live = {s for s, _, _ in pages}
    all_briefs = [jd.parse_brief(str(p)) for p in sorted(Path("knowledge/briefs/junia").glob("*.md"))]
    open_briefs = [b for b in all_briefs if b["slug"] and b["slug"] not in live]
    todo = [jd.parse_brief(a.brief)] if a.brief else open_briefs
    strong = 0
    for b in todo:
        found = conflicts(b, pages, open_briefs)
        print(f"\n{b['slug']}  (focus: {b['focus']})")
        if not found:
            print("   ✅ no competing page or brief")
        for lv, kind, slug, label, j in found:
            strong += lv == "STRONG"
            print(f"   {'❌' if lv == 'STRONG' else '⚠️ '} {lv:6} {kind}: /{slug}/  \"{label}\"  overlap {j}")
    print(f"\n{len(todo)} brief(s) checked against {len(pages)} live pages · {strong} STRONG match(es)")
    sys.exit(1 if strong else 0)


if __name__ == "__main__":
    main()
