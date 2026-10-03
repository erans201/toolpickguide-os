"""
update_categories.py: apply approved category changes on toolpickguide.com.

Two independent actions, both driven by wordpress/CATEGORY-PAGES.md:
  --renames   B1: rename categories (names only; slugs/URLs never change)
  --content   Part A: category description (intro HTML) + Rank Math SEO title/description

Default is a DRY RUN (public read-only lookups, no login, nothing changed).

    python update_categories.py --renames                 # preview renames
    python update_categories.py --renames --apply         # do it (backup first)
    python update_categories.py --content                 # preview content
    python update_categories.py --content --apply         # do it (backup first)
    python update_categories.py --restore backups/categories-<time>.json

Safety:
  - Backs up every targeted category (name, slug, description, visible SEO title/description) before any change.
  - Never sends a slug or parent, so URLs and hierarchy cannot change. Verifies slug after each write.
  - Only touches category IDs listed in RENAMES / CATEGORY-PAGES.md.
  - Never runs from the scheduler.
"""

import argparse
import html as html_lib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
PACK = Path("wordpress/CATEGORY-PAGES.md")
BACKUP_DIR = Path("backups")

# B1 (approved 2026-09-28): id -> (expected current name, new name)
RENAMES = {
    109: ("BEST FOR LAW FIRMS", "Legal Software"),
    108: ("CLIENT ONBOARDING", "Client Onboarding"),
    6: ("CRM OPERATIONS", "CRM & Operations"),
}


def parse_pack():
    """{id: {"seo_title", "seo_description", "description_html"}} from CATEGORY-PAGES.md Part A."""
    text = PACK.read_text(encoding="utf-8")
    part_a = text.split("## ⚠️ PART B")[0]
    plan = {}
    for block in re.split(r"^### \d+\. ", part_a, flags=re.MULTILINE)[1:]:
        cat_id = re.search(r"· ID (\d+) ·", block.splitlines()[0])
        title = re.search(r"\| Rank Math SEO Title \| (.+?) \|", block)
        desc = re.search(r"\| Rank Math Description \| (.+?) \|", block)
        body = re.search(r"```html\n(.+?)```", block, flags=re.DOTALL)
        if cat_id and title and desc and body:
            plan[int(cat_id.group(1))] = {
                "seo_title": title.group(1).strip(),
                "seo_description": desc.group(1).strip(),
                "description_html": body.group(1).strip(),
            }
    if not plan:
        sys.exit(f"ERROR: No category blocks found in {PACK}.")
    return plan


def public_category(cat_id):
    resp = requests.get(f"{SITE}/wp-json/wp/v2/categories/{cat_id}", timeout=30,
                        params={"_fields": "id,name,slug,parent,description,link"})
    if resp.status_code != 200:
        sys.exit(f"ERROR: Category {cat_id} not found (HTTP {resp.status_code}).")
    return resp.json()


def visible_seo(link):
    page = requests.get(link, timeout=30, headers={"User-Agent": "ToolPickGuide-Backup/1.0"}).text
    t = re.search(r"<title>(.*?)</title>", page, flags=re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', page)
    return (html_lib.unescape(t.group(1)).strip() if t else None, html_lib.unescape(d.group(1)) if d else None)


def backup(ids):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    snap = []
    for cat_id in ids:
        c = public_category(cat_id)
        title, desc = visible_seo(c["link"])
        snap.append({"id": c["id"], "name": html_lib.unescape(c["name"]), "slug": c["slug"], "parent": c["parent"],
                     "description": c["description"], "link": c["link"],
                     "rank_math_visible": {"title": title, "description": desc}})
    path = BACKUP_DIR / f"categories-{datetime.now():%Y%m%d-%H%M%S}.json"
    path.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                "categories": snap}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"💾 Backup saved: {path}")
    return path, {s["id"]: s for s in snap}


def write_category(session, cat_id, payload, expected_slug):
    from upload_draft import wp

    result = wp(session, "POST", f"{SITE}/wp-json/wp/v2/categories/{cat_id}", f"Could not update category {cat_id}.", json=payload)
    if result["slug"] != expected_slug:
        sys.exit(f"SAFETY ERROR: category {cat_id} slug changed to '{result['slug']}'. Restore from the backup now.")
    return result


def rank_math_term(session, cat_id, title, description):
    resp = session.post(f"{SITE}/wp-json/rankmath/v1/updateMeta", timeout=60, json={
        "objectType": "term", "objectID": cat_id,
        "meta": {"rank_math_title": title, "rank_math_description": description}})
    return resp.status_code < 400


def refuse_in_scheduler():
    import os
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: category changes never run from the scheduler. Run it yourself.")


def do_renames(apply):
    print("B1: RENAMES (names only; slugs stay the same)\n")
    todo = []
    for cat_id, (expected, new) in RENAMES.items():
        c = public_category(cat_id)
        current = html_lib.unescape(c["name"])
        if current == new:
            print(f"  [{cat_id}] already '{new}'. Skipping.")
        elif current != expected:
            print(f"  [{cat_id}] ⚠️ name is '{current}', expected '{expected}'. Skipping (changed by someone else?).")
        else:
            print(f"  [{cat_id}] '{current}' → '{new}'   (slug stays: {c['slug']})")
            todo.append((cat_id, new, c["slug"]))
    if not apply or not todo:
        print("\nDRY RUN: nothing changed." if not apply else "\nNothing to do.")
        return

    refuse_in_scheduler()
    from upload_draft import make_session
    path, _ = backup([t[0] for t in todo])
    session, _ = make_session()
    for cat_id, new, slug in todo:
        result = write_category(session, cat_id, {"name": new}, slug)
        print(f"  ✅ [{cat_id}] renamed to '{html_lib.unescape(result['name'])}' (slug unchanged: {result['slug']})")
    print(f"\nUndo: python update_categories.py --restore {path}")


def do_content(apply):
    plan = parse_pack()
    print("PART A: CATEGORY CONTENT (description + Rank Math SEO title/description)\n")
    for cat_id, p in plan.items():
        c = public_category(cat_id)
        words = len(re.sub(r"<[^>]+>", " ", p["description_html"]).split())
        print(f"  [{cat_id}] {html_lib.unescape(c['name'])}  ({c['slug']})")
        print(f"       SEO title : {p['seo_title']}")
        print(f"       SEO desc  : {p['seo_description']} ({len(p['seo_description'])} chars)")
        print(f"       intro     : {words} words, {p['description_html'].count('<a ')} links "
              f"(currently: {'EMPTY' if not c['description'].strip() else 'has text, will be replaced'})")
    if not apply:
        print("\nDRY RUN: nothing changed.")
        return

    refuse_in_scheduler()
    from upload_draft import make_session
    path, snap = backup(list(plan))
    session, _ = make_session()
    for cat_id, p in plan.items():
        write_category(session, cat_id, {"description": p["description_html"]}, snap[cat_id]["slug"])
        ok = rank_math_term(session, cat_id, p["seo_title"], p["seo_description"])
        print(f"  ✅ [{cat_id}] description updated · Rank Math {'saved' if ok else '⚠️ NOT saved: set it in the category editor'}")
    print(f"\nUndo: python update_categories.py --restore {path}")


def do_restore(path):
    refuse_in_scheduler()
    from upload_draft import make_session
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    session, _ = make_session()
    for c in data["categories"]:
        write_category(session, c["id"], {"name": c["name"], "description": c["description"]}, c["slug"])
        seo = c.get("rank_math_visible") or {}
        if seo.get("description"):  # had custom SEO before: put the visible values back
            rank_math_term(session, c["id"], seo.get("title") or "", seo["description"])
        else:  # had Rank Math defaults (no meta description): clear custom values so defaults return
            rank_math_term(session, c["id"], "", "")
        print(f"  ↩️ [{c['id']}] restored '{c['name']}'")
    print("Restore complete.")


def main():
    parser = argparse.ArgumentParser(description="Apply approved category changes (dry run by default).")
    parser.add_argument("--renames", action="store_true", help="B1: rename categories (names only)")
    parser.add_argument("--content", action="store_true", help="Part A: descriptions + Rank Math SEO")
    parser.add_argument("--apply", action="store_true", help="Actually make the changes (backup first)")
    parser.add_argument("--restore", metavar="BACKUP.json", help="Undo from a backup file")
    args = parser.parse_args()

    if args.restore:
        do_restore(args.restore)
    elif args.renames or args.content:
        if args.renames:
            do_renames(args.apply)
        if args.content:
            print()
            do_content(args.apply)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
