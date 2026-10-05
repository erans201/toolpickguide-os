"""
junia_draft.py: QA a Junia.ai WordPress draft against its brief, then apply Rank Math SEO + score fixes.

    python junia_draft.py --brief knowledge/briefs/junia/photography-client-questionnaire.md            # QA report (read-only)
    python junia_draft.py --brief knowledge/briefs/junia/photography-client-questionnaire.md --apply    # fix + SEO (stays a draft)
    python junia_draft.py --restore backups/junia-<id>-<time>.json
    python junia_draft.py --export-all     # read-only: every draft with a brief → knowledge/_preview/ (+ -qa.txt reports)
    python junia_draft.py --brief <brief> --replace-content <corrected.md>   # QA-corrected body (backup, stays a draft)

Finds the draft by the brief's focus keyword (or --post-id). Never publishes: refuses anything that isn't a draft
and verifies the status after writing.

QA report: title year, banned words, "tested" claims, $ amounts not in the facts sheet, required links,
keyword placement (title, first paragraph, subheadings, density), word count, long paragraphs.
External links Junia added on its own are allowed when the site is legit and trusted (user rule 2026-10-05): the
agent judges each new domain once and records it in knowledge/junia-link-domains.txt (trusted / blocked). The gate
fails while a link points to a blocked domain or to a domain nobody has judged yet.

--apply (after a full backup to backups/junia-*.json):
  - fixes a wrong year in the title, sets slug, excerpt, tags, category
  - Rank Math: SEO title, meta description, focus + secondary keywords, social title/description
  - copies Junia's stock photos (e.g. images.unsplash.com) into the Media Library and points the draft at the copies
    (faster, can't break if the source moves; Unsplash license: free to use); with no featured image, the first
    copy becomes the featured image
  - uploads our featured image (knowledge/images/junia-<slug>.png) only when the draft has none
  - Rank Math score fixes: puts the featured image in the content (keyword alt), adds the focus keyword to the
    FAQ heading if no subheading has it, adds missing required internal links, adds official-source links for
    tools mentioned without one
Autopilot (TPG_AUTOPILOT=1, AUTOPILOT.md): kill switch; --apply only when the QA gate is clean; max 3 draft
updates per day; each write is re-read and restored at once (plus a strike) if it doesn't match.
Rank Math recalculates the score when the draft is opened in the editor and saved.
"""

import argparse
import html as html_lib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from autopilot import guard

SITE = "https://toolpickguide.com"
API = f"{SITE}/wp-json/wp/v2"
BACKUP_DIR = Path("backups")
CURRENT_YEAR = str(datetime.now().year)
BANNED = ["delve", "testament", "furthermore", "in conclusion", "in today's fast-paced world", "unlock", "game-changer",
          "game changer", "seamless"]
TESTED = re.compile(r"\b(we tested|our testing|hands-on|in our tests|tested it)\b", re.I)
MONEY = r"\$\d+(?:,\d{3})*(?:\.\d+)?"  # "$1,188" yes; "$140," → "$140" (no trailing comma)
# Junia production notes / chatbot residue that must never reach a published page
LEFTOVERS = re.compile(r"images? to include|suggested wordpress image|image placements|draft for toolpickguide|"
                       r"if you tell me|i can point you|in one reply|\[insert|placeholder|in today's [a-z ]+ landscape|"
                       r"save this as a draft|save as draft|draft saved|as draft\b|come back to it|ptsd|"
                       r"i have seen the same|draft note|images you can add|images and screenshots you should add|"
                       r"recommended placements|tell me your|i will suggest|if you want, tell me", re.I)
LINK_DOMAINS = Path("knowledge/junia-link-domains.txt")  # agent's trusted / blocked verdicts on Junia's own links


def link_verdicts(path=LINK_DOMAINS):
    """{domain: "trusted" | "blocked"} from lines like 'trusted ftc.gov' (comments start with #)."""
    out = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split("#", 1)[0].split()
            if len(parts) >= 2 and parts[0].lower() in ("trusted", "blocked"):
                out[parts[1].lower().removeprefix("www.")] = parts[0].lower()
    return out


def verdict(domain, verdicts):
    d = domain.lower().removeprefix("www.")
    while d:
        if d in verdicts:
            return verdicts[d]
        d = d.partition(".")[2] if d.count(".") > 1 else ""
    return None


SOURCES = {  # verified official pricing pages (2026-09-29)
    "Pixieset": "https://pixieset.com/pricing-studio-manager/", "Studio Ninja": "https://www.studioninja.co/pricing/",
    "Sprout Studio": "https://getsproutstudio.com/pricing/", "Dubsado": "https://www.dubsado.com/pricing",
    "HoneyBook": "https://www.honeybook.com/pricing", "Bloom": "https://bloom.io/pricing",
    "TaxDome": "https://taxdome.com/pricing", "Karbon": "https://karbonhq.com/pricing/", "Canopy": "https://www.getcanopy.com/pricing",
    "Paperbell": "https://paperbell.com/pricing/", "Follow Up Boss": "https://www.followupboss.com/pricing",
}


# ---------------------------------------------------------------------------
# Brief parsing
# ---------------------------------------------------------------------------

def parse_brief(path):
    text = Path(path).read_text(encoding="utf-8")
    row = lambda label: (re.search(rf"^\| {re.escape(label)} \| (.+?) \|$", text, re.M) or [None, ""])[1].strip()  # noqa: E731
    cat_tags = row("Category / Tags")
    category, _, tags = cat_tags.partition(" · ")
    facts = text.split("FACTS SHEET", 1)[1] if "FACTS SHEET" in text else ""
    boxes = re.findall(r"```text\n(.+?)```", text, re.S)
    prompt = next((b for b in boxes if "INTERNAL LINKS" in b), boxes[0] if boxes else "")  # the box with the link lists
    internal = re.findall(r"^- (/[a-z0-9-]+/) with anchor \"([^\"]+)\"", prompt, re.M)
    external = re.findall(r"^- (https://\S+)", prompt, re.M)
    brief = {
        "slug": (re.search(r"[a-z0-9]+(?:-[a-z0-9]+)*", row("Slug")) or [""])[0], "focus": row("Focus keyword").lower(),
        "secondary": [s.strip() for s in row("Secondary keywords").split("·") if s.strip()],
        "seo_title": row("SEO title"), "meta_description": row("Meta description"), "h1": row("H1"),
        "category": [c.strip() for c in category.split(",") if c.strip()],
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "fact_amounts": set(re.findall(MONEY, facts)),
        "internal": internal, "external": external,
        # optional brief row: "| Required tools | A, B, C |" (BOFU lists) and "| Price-heavy | yes |"
        "required_tools": [t.strip() for t in row("Required tools").split(",") if t.strip()],
        "excluded_tools": [t.strip() for t in row("Excluded tools").split(",") if t.strip()],
        "price_heavy": row("Price-heavy").lower().startswith("yes"),
    }
    missing = [k for k in ("slug", "focus", "seo_title", "meta_description") if not brief[k]]
    if missing:
        sys.exit(f"ERROR: brief is missing {missing}")
    brief["image"] = Path("knowledge/images") / f"junia-{brief['slug']}.png"
    brief["image_alt"] = re.sub(r"\s*\(\d{4}\)", "", brief["h1"] or brief["seo_title"])
    return brief


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def text_of(html):
    return html_lib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))).strip()


def analyze(post, brief):
    raw = post["content"]["raw"]
    title = post["title"]["raw"]
    body = text_of(raw)
    words = body.split()
    lower = body.lower()
    focus = brief["focus"]
    paras = [text_of(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", raw, re.S)]
    first_p = next((p for p in paras if len(p.split()) > 8), "")
    heads = [text_of(h) for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", raw, re.S)]
    kw_count = lower.count(focus)
    density = round(100 * kw_count * len(focus.split()) / max(len(words), 1), 2)
    hrefs = re.findall(r'href="([^"]+)"', raw)
    internal_have = {h.replace(SITE, "") for h in hrefs if h.startswith("/") or SITE in h}
    external_have = [h for h in hrefs if h.startswith("http") and SITE not in h]
    amounts = set(re.findall(MONEY, body))
    years = set(re.findall(r"\((\d{4})\)", title)) | set(re.findall(r"\b(20\d\d|19\d\d)\b", title))
    tools_unlinked = [t for t in SOURCES if t.lower() in lower and not any(SOURCES[t].split("/")[2] in h for h in external_have)]
    return {
        "title": title, "words": len(words), "kw_count": kw_count, "density": density,
        "kw_in_title": focus in title.lower(), "kw_in_first_p": focus in first_p.lower(),
        "kw_in_heading": any(focus in h.lower() for h in heads),
        "wrong_years": sorted(y for y in years if y != CURRENT_YEAR),
        "template_vars": re.findall(r"%[a-z_]+%", title),  # e.g. Junia copied the SEO title's %currentyear% into the H1
        "banned": [b for b in BANNED if re.search(rf"\b{re.escape(b)}\b", lower)],
        "tested": sorted(set(m.group(0) for m in TESTED.finditer(body))),
        "unknown_amounts": sorted(a for a in amounts if a not in brief["fact_amounts"]),
        "amounts": sorted(amounts),
        "missing_internal": [p for p, _ in brief["internal"] if p not in internal_have and p.rstrip("/") not in internal_have],
        "missing_external": [u for u in brief["external"] if u not in hrefs],
        "external_count": len(external_have), "internal_count": len(internal_have),
        "long_paragraphs": [p[:90] for p in paras if len(re.findall(r"[.!?](\s|$)", p)) > 3],
        "has_image": "<img" in raw, "tools_unlinked": tools_unlinked, "status": post["status"],
        "leftovers": sorted(set(m.group(0) for m in LEFTOVERS.finditer(body))),
        "hotlinked_images": [s for s in re.findall(r'<img[^>]+src="([^"]+)"', raw) if SITE not in s and not s.startswith("/")],
        "offlist_external": sorted({h.split("/")[2] for h in external_have}
                                   - {u.split("/")[2] for u in brief["external"]} - {u.split("/")[2] for u in SOURCES.values()}),
        "missing_tools": [t for t in brief["required_tools"] if t.lower() not in lower],
        "no_disclosure": not any("ftc.gov" in h for h in hrefs),
        "faq_sections": len(re.findall(r"<h2[^>]*>[^<]*\bFAQs?\b", raw, re.I)),
        **judge_offlist(external_have, brief),
        "excluded_present": [t for t in brief["excluded_tools"] if t.lower() in lower],
        "source_lines": len(re.findall(r"\bSource:", body)),
        "claimed_n": int(m.group(1)) if (m := re.search(r"(\d+)\s+(?:questions|clauses|tips|tools|ways|templates)", title, re.I)) else None,
        "question_items": len(re.findall(r"<li[^>]*>(?:(?!</li>).)*\?(?:(?!</li>).)*</li>", raw, re.S)),
    }


def report(a, brief, post):
    ok = lambda b: "✅" if b else "❌"  # noqa: E731
    print(f"Draft {post['id']}: \"{a['title']}\"  (status: {a['status']}, slug: {post['slug']})\n")
    print("QA GATE")
    print(f"  {ok(not a['wrong_years'])} Title year {'OK' if not a['wrong_years'] else 'WRONG: ' + ', '.join(a['wrong_years']) + ' (fixed by --apply)'}")
    if a["template_vars"]:
        print(f"  ❌ Title shows raw Rank Math code {', '.join(a['template_vars'])}: visitors would see it (fixed by --apply)")
    print(f"  {ok(not a['banned'])} Banned words: {a['banned'] or 'none'}")
    print(f"  {ok(not a['tested'])} 'Tested' claims: {a['tested'] or 'none'}")
    print(f"  {ok(not a['unknown_amounts'])} $ amounts not in facts sheet: {a['unknown_amounts'] or 'none'}  (must be fixed by hand)")
    print(f"  {ok(not a['long_paragraphs'])} Paragraphs over 3 sentences: {len(a['long_paragraphs'])}")
    for lp in a["long_paragraphs"]:
        print(f"       → starts: \"{lp}…\"  (split into 2 paragraphs)")
    print(f"  {ok(not a['leftovers'])} Junia notes / chatbot residue: {a['leftovers'] or 'none'}")
    print(f"  {ok(not a['no_disclosure'])} Affiliate disclosure with the FTC link: {'missing' if a['no_disclosure'] else 'OK'}")
    print(f"  {ok(a['faq_sections'] <= 1)} FAQ sections: {a['faq_sections']} (exactly one allowed)")
    print(f"  ℹ️ Stock photos loaded from another site: {len(a['hotlinked_images'])}"
          f"{' (copied into the Media Library by --apply)' if a['hotlinked_images'] else ''}")
    print(f"  ℹ️ External links Junia added (allowed if the site is legit): {a['offlist_external'] or 'none'}")
    print(f"  {ok(not a['blocked_external'])} Links to untrusted sites (remove them): {a['blocked_external'] or 'none'}")
    print(f"  {ok(not a['unjudged_external'])} New sites to judge in {LINK_DOMAINS}: {a['unjudged_external'] or 'none'}")
    print(f"  {ok(not a['missing_external'])} Required source links missing: {a['missing_external'] or 'none'}")
    if brief["required_tools"]:
        print(f"  {ok(not a['missing_tools'])} Required tools missing: {a['missing_tools'] or 'none'}")
    if brief["excluded_tools"]:
        print(f"  {ok(not a['excluded_present'])} Excluded tools present: {a['excluded_present'] or 'none'}")
    if brief["price_heavy"]:
        need = max(len(brief["required_tools"]), 1)
        print(f"  {ok(a['source_lines'] >= need)} Price-heavy page: 'Source:' lines {a['source_lines']} (need {need}) · "
              f"$ amounts used: {len(a['amounts'])}")
    if a["claimed_n"] and "question" in a["title"].lower():
        print(f"  {ok(a['question_items'] >= a['claimed_n'])} Title promises {a['claimed_n']} questions; list items with a question: {a['question_items']}")
    print("\nRANK MATH CHECKS (score inputs)")
    print(f"  {ok(a['kw_in_title'])} Focus keyword in title")
    print(f"  {ok(a['kw_in_first_p'])} Focus keyword in first paragraph")
    print(f"  {ok(a['kw_in_heading'])} Focus keyword in a subheading{'' if a['kw_in_heading'] else ' (fixed by --apply)'}")
    print(f"  {ok(0.5 <= a['density'] <= 2.5)} Keyword density {a['density']}% ({a['kw_count']} uses; aim 0.5–2.5%)")
    print(f"  {ok(a['words'] >= 1500)} Content length {a['words']} words (Rank Math's top band starts at 2,500)")
    print(f"  {ok(a['has_image'])} Image in content{'' if a['has_image'] else ' (added by --apply, keyword alt)'}")
    print(f"  {ok(not a['missing_internal'])} Required internal links: missing {a['missing_internal'] or 'none'}{' (added by --apply)' if a['missing_internal'] else ''}")
    print(f"  {ok(a['external_count'] > 0 or a['tools_unlinked'])} External links: {a['external_count']}"
          f"{' (+ official sources for ' + ', '.join(a['tools_unlinked']) + ' by --apply)' if a['tools_unlinked'] else ''}")
    print(f"  ✅ SEO title / meta description / slug / focus keywords: set by --apply from the brief")


# ---------------------------------------------------------------------------
# Fixes
# ---------------------------------------------------------------------------

def insert_before_faq(raw, block):
    faq = re.search(r"(<!-- wp:heading[^>]*-->\s*)?<h2[^>]*>(?:(?!</h2>).)*FAQ", raw, re.I | re.S)
    return raw[:faq.start()] + block + raw[faq.start():] if faq else raw.rstrip() + "\n\n" + block


def fix_content(raw, a, brief, media):
    focus_title = brief["focus"].title()
    changes = []
    if media and not a["has_image"]:
        img = (f'<!-- wp:image {{"id":{media["id"]},"sizeSlug":"large"}} -->\n<figure class="wp-block-image size-large">'
               f'<img src="{media["url"]}" alt="{html_lib.escape(brief["image_alt"])}" class="wp-image-{media["id"]}"/></figure>\n<!-- /wp:image -->\n\n')
        m = re.search(r"</p>\s*(<!-- /wp:paragraph -->)?", raw)
        raw = raw[:m.end()] + "\n\n" + img + raw[m.end():] if m else img + raw
        changes.append("featured image added after the first paragraph (keyword alt)")
    if not a["kw_in_heading"]:
        new, n = re.subn(r"(<h2[^>]*>)((?:(?!</h2>).)*FAQ(?:(?!</h2>).)*)(</h2>)",
                         lambda m: f"{m.group(1)}FAQs About the {focus_title}{m.group(3)}", raw, count=1, flags=re.I | re.S)
        if n:
            raw = new; changes.append(f'FAQ heading → "FAQs About the {focus_title}"')
    if a["missing_internal"]:
        anchors = dict(brief["internal"])
        links = " · ".join(f'<a href="{p}">{html_lib.escape(anchors[p])}</a>' for p in a["missing_internal"])
        raw = insert_before_faq(raw, f"<!-- wp:paragraph -->\n<p><strong>Related reading:</strong> {links}</p>\n<!-- /wp:paragraph -->\n\n")
        changes.append(f"related links added: {', '.join(a['missing_internal'])}")
    if a["tools_unlinked"]:
        links = " · ".join(f'<a href="{SOURCES[t]}" target="_blank" rel="noopener">{t} pricing</a>' for t in a["tools_unlinked"])
        raw = insert_before_faq(raw, f"<!-- wp:paragraph -->\n<p><strong>Sources (checked September 2026):</strong> {links}</p>\n<!-- /wp:paragraph -->\n\n")
        changes.append(f"official source links added: {', '.join(a['tools_unlinked'])}")
    return raw, changes


IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_IMAGE_BYTES = 15 * 1024 * 1024


def rehost_images(session, raw, srcs, alt, slug, upload_image, wp):
    """Copies each external image into the Media Library and swaps the URL in the content. Returns (raw, media ids)."""
    import requests
    ids = []
    for i, src in enumerate(dict.fromkeys(srcs), 1):
        url = html_lib.unescape(src)
        if not url.startswith("https://"):
            print(f"   ! skipped (not https): {url[:80]}")
            continue
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        ext = IMAGE_TYPES.get(r.headers.get("Content-Type", "").split(";")[0].strip())
        if not ext or len(r.content) > MAX_IMAGE_BYTES:
            print(f"   ! skipped (not an image or too large): {url[:80]}")
            continue
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        tmp = BACKUP_DIR / f"rehost-{slug}-{i}{ext}"
        tmp.write_bytes(r.content)
        try:
            mid = upload_image(session, API, tmp, alt, f"{slug}-photo-{i}")
        finally:
            tmp.unlink(missing_ok=True)
        new = wp(session, "GET", f"{API}/media/{mid}", "Could not read uploaded image.")["source_url"]
        raw = raw.replace(src, new).replace(url, new).replace(html_lib.escape(url, quote=True), new)
        ids.append(mid)
        print(f"   ↻ stock photo copied into the Media Library → media {mid}")
    return raw, ids


def fix_title(title):
    title = title.replace("%currentyear%", CURRENT_YEAR).replace("%year%", CURRENT_YEAR)
    return re.sub(r"\((?:19|20)\d\d\)", f"({CURRENT_YEAR})", title)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def find_draft(session, brief, post_id):
    from upload_draft import wp
    if post_id:
        return wp(session, "GET", f"{API}/posts/{post_id}", f"Could not load post {post_id}.", params={"context": "edit"})
    found = wp(session, "GET", f"{API}/posts", "Could not search drafts.",
               params={"status": "draft", "search": brief["focus"], "context": "edit", "per_page": 10})
    if not found:
        sys.exit(f"No draft found matching \"{brief['focus']}\". Use --post-id.")
    exact = [p for p in found if brief["focus"] in p["title"]["raw"].lower()]
    if len(exact) == 1:
        return exact[0]
    if not exact:  # a body that merely mentions the keyword is not this brief's draft
        sys.exit(f"No draft title contains \"{brief['focus']}\". Use --post-id.")
    sys.exit("Several drafts match. Re-run with --post-id:\n" + "\n".join(f"  {p['id']}: {p['title']['raw']}" for p in exact))


def export(post, brief, a, brief_path):
    """Read-only: save the draft as Markdown + its QA report, so the agent can review without copy-paste."""
    import contextlib
    import io

    import html2text
    h = html2text.HTML2Text()
    h.body_width = 0
    out = Path("knowledge/_preview") / f"junia-{post['id']}-{brief['slug']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"# {post['title']['raw']}\n\n" + h.handle(post["content"]["raw"]), encoding="utf-8")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        report(a, brief, post)
    qa = out.with_name(out.stem + "-qa.txt")
    qa.write_text(f"Exported {datetime.now():%Y-%m-%d %H:%M} · brief {brief_path}\n\n" + buf.getvalue(), encoding="utf-8")
    print(f"📄 {out}\n📋 {qa}")


def export_all(session):
    """Export every WordPress draft that matches a Junia brief. Read-only; skips briefs with no or several drafts."""
    briefs = sorted(Path("knowledge/briefs/junia").glob("*.md"))
    print(f"Checking {len(briefs)} briefs for drafts…\n")
    for path in briefs:
        brief = parse_brief(str(path))
        try:
            post = find_draft(session, brief, None)
        except SystemExit as e:
            print(f"– {path.name}: skipped ({str(e).splitlines()[0]})")
            continue
        if post["status"] != "draft":
            print(f"– {path.name}: skipped (post {post['id']} is '{post['status']}')")
            continue
        print(f"✓ {path.name} → draft {post['id']}")
        export(post, brief, analyze(post, brief), str(path))
    print("\nDone. Nothing was changed in WordPress. Tell the agent the exports are ready.")


def judge_offlist(external_have, brief, verdicts=None):
    """Splits Junia's own external links into trusted / blocked / not yet judged domains."""
    verdicts = link_verdicts() if verdicts is None else verdicts
    own = sorted({h.split("/")[2] for h in external_have}
                 - {u.split("/")[2] for u in brief["external"]} - {u.split("/")[2] for u in SOURCES.values()})
    return {"blocked_external": [d for d in own if verdict(d, verdicts) == "blocked"],
            "unjudged_external": [d for d in own if verdict(d, verdicts) is None]}


def gate_clean(a):
    """True when no QA GATE item needs a human edit (AUTOPILOT.md: Tier B may only --apply clean drafts)."""
    short_of_claim = a["claimed_n"] and "question" in a["title"].lower() and a["question_items"] < a["claimed_n"]
    return not (a["unknown_amounts"] or a["banned"] or a["tested"] or a["long_paragraphs"] or short_of_claim
                or a["leftovers"] or a["no_disclosure"] or a["faq_sections"] > 1 or a["blocked_external"] or a["unjudged_external"] or a["missing_tools"]
                or a["excluded_present"] or a["missing_external"])


def undo_failed(session, backup, why):
    """Autopilot: restore the draft from its backup at once and record a strike."""
    from upload_draft import wp
    data = json.loads(Path(backup).read_text(encoding="utf-8"))
    wp(session, "POST", f"{API}/posts/{data['id']}", f"RESTORE FAILED: run python junia_draft.py --restore {backup}",
       json={"title": data["title"], "content": data["content"], "slug": data["slug"], "excerpt": data["excerpt"],
             "status": "draft"})
    paused = guard.strike(f"junia_draft {data['id']}: {why}")
    print(f"⚠️  ALERT draft {data['id']}: {why}. Restored from {backup}." + (" Autopilot is now PAUSED (2 strikes)." if paused else ""))


def refuse_in_scheduler():
    import os
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: junia_draft never runs from the scheduler.")


def main():
    parser = argparse.ArgumentParser(description="QA a Junia draft and apply Rank Math SEO fixes (dry run by default).")
    parser.add_argument("--brief", help="knowledge/briefs/junia/<slug>.md")
    parser.add_argument("--post-id", type=int)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--replace-image", action="store_true",
                        help="Replace Junia's featured image with our own one (in-content images are left alone)")
    parser.add_argument("--restore", metavar="BACKUP.json")
    parser.add_argument("--export", action="store_true",
                        help="Read-only: save the draft as Markdown in knowledge/_preview/ so the agent can review it")
    parser.add_argument("--replace-content", metavar="FILE.md",
                        help="Replace the draft's body with the agent's QA-corrected Markdown (implies --apply; backup first)")
    parser.add_argument("--export-all", action="store_true",
                        help="Read-only: export every draft that matches a brief in knowledge/briefs/junia/ (+ QA report files)")
    args = parser.parse_args()
    refuse_in_scheduler()
    guard.stop_if_paused()

    from upload_draft import explain_error, make_session, resolve_categories, resolve_tags, upload_image, wp
    session, _ = make_session()

    if args.restore:
        data = json.loads(Path(args.restore).read_text(encoding="utf-8"))
        post = wp(session, "POST", f"{API}/posts/{data['id']}", "Restore failed.",
                  json={"title": data["title"], "content": data["content"], "slug": data["slug"], "excerpt": data["excerpt"]})
        print(f"✅ Restored draft {post['id']} from {args.restore}")
        return
    if args.export_all:
        export_all(session)
        return
    if not args.brief:
        parser.error("--brief is required (or use --export-all)")

    brief = parse_brief(args.brief)
    post = find_draft(session, brief, args.post_id)
    if post["status"] != "draft":
        sys.exit(f"ABORT: post {post['id']} is '{post['status']}'. This tool only edits drafts.")
    original_raw = post["content"]["raw"]
    if args.replace_content:
        import markdown
        md = Path(args.replace_content).read_text(encoding="utf-8")
        post["content"]["raw"] = markdown.markdown(md, extensions=["tables", "sane_lists"])
        args.apply = True
        print(f"Body replaced with QA-corrected version: {args.replace_content}\n")
    a = analyze(post, brief)
    report(a, brief, post)
    if args.export:
        export(post, brief, a, args.brief)
    if not args.apply:
        print("\nDRY RUN: nothing changed. Add --apply to fix and inject SEO (the post stays a draft).")
        return
    if guard.active():
        if not gate_clean(a):
            sys.exit(f"AUTOPILOT: draft {post['id']} fails the QA gate (❌ items above). Not applied; listed as Tier C.")
        if guard.allowance("drafts", 1) < 1:
            sys.exit(f"AUTOPILOT: daily cap reached ({guard.DAILY_CAPS['drafts']} draft updates per day). Not applied.")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"junia-{post['id']}-{datetime.now():%Y%m%d-%H%M%S}.json"
    backup.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "id": post["id"],
                                  "title": post["title"]["raw"], "content": original_raw, "slug": post["slug"],
                                  "excerpt": post["excerpt"]["raw"]}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n💾 Backup: {backup}")

    rehosted = []
    if a["hotlinked_images"]:
        post["content"]["raw"], rehosted = rehost_images(session, post["content"]["raw"], a["hotlinked_images"],
                                                         brief["image_alt"], brief["slug"], upload_image, wp)
    media = None
    if rehosted and not post.get("featured_media") and not args.replace_image:
        m = wp(session, "GET", f"{API}/media/{rehosted[0]}", "Could not read the copied image.")
        media = {"id": rehosted[0], "url": m["source_url"]}
        print(f"   ★ featured image ← first copied stock photo (media {rehosted[0]})")
    elif brief["image"].is_file() and (not post.get("featured_media") or args.replace_image):
        mid = upload_image(session, API, brief["image"], brief["image_alt"], brief["slug"])
        m = wp(session, "GET", f"{API}/media/{mid}", "Could not read uploaded image.")
        media = {"id": mid, "url": m["source_url"]}
        print(f"   + featured image uploaded: media {mid}")
    elif post.get("featured_media"):
        m = wp(session, "GET", f"{API}/media/{post['featured_media']}", "Could not read featured image.")
        media = {"id": post["featured_media"], "url": m["source_url"]}

    content, changes = fix_content(post["content"]["raw"], a, brief, media)
    payload = {"title": fix_title(post["title"]["raw"]), "slug": brief["slug"], "content": content,
               "excerpt": brief["meta_description"], "tags": resolve_tags(session, API, brief["tags"]), "status": "draft"}
    cats = resolve_categories(session, API, brief["category"])
    if cats:
        payload["categories"] = cats
    if media:
        payload["featured_media"] = media["id"]
    result = wp(session, "POST", f"{API}/posts/{post['id']}", "WordPress rejected the update.", json=payload)
    if result.get("status") != "draft":
        if guard.active():
            undo_failed(session, backup, f"status became '{result.get('status')}'")
        sys.exit(f"SAFETY ERROR: post {post['id']} is now '{result.get('status')}'. Restore: python junia_draft.py --restore {backup}")
    if guard.active():
        check = wp(session, "GET", f"{API}/posts/{post['id']}", "Could not re-read the draft.", params={"context": "edit"})
        if check["status"] != "draft" or check["slug"] != brief["slug"] or len(check["content"]["raw"]) < len(content) * 0.9:
            undo_failed(session, backup, "re-read did not match what was written")
            sys.exit(f"AUTOPILOT: draft {post['id']} restored after a failed verification.")
        guard.record("drafts", 1, target=f"draft {post['id']}", detail=brief["slug"],
                     undo=f"python junia_draft.py --restore {backup}")

    keywords = [brief["focus"]] + [k for k in brief["secondary"] if k.lower() != brief["focus"]]
    rm = session.post(f"{SITE}/wp-json/rankmath/v1/updateMeta", timeout=60, json={"objectType": "post", "objectID": post["id"], "meta": {
        "rank_math_title": brief["seo_title"], "rank_math_description": brief["meta_description"],
        "rank_math_focus_keyword": ",".join(keywords[:5]),
        "rank_math_facebook_title": re.sub(r"\s*\(%currentyear%\)|\s*%currentyear%", "", brief["seo_title"]),
        "rank_math_facebook_description": brief["meta_description"], "rank_math_twitter_use_facebook": "on"}})

    print(f"\n✅ Draft {post['id']} updated (still a draft): \"{payload['title']}\" · /{brief['slug']}/")
    if rehosted:
        changes.insert(0, f"{len(rehosted)} stock photo(s) copied into the Media Library")
    for c in changes:
        print(f"   • {c}")
    print("   • Rank Math meta " + ("saved" if rm.status_code < 400 else "NOT saved:\n" + explain_error(rm)))
    if not gate_clean(a):
        print("\n⚠️ Still needs a human edit before publishing: see the QA GATE items marked ❌ above.")
    print("\nNext: open the draft in WordPress and click Save Draft. Rank Math recalculates the score on save.")
    print(f"Undo: python junia_draft.py --restore {backup}")


if __name__ == "__main__":
    main()
