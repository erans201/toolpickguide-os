"""
patch_live.py: small, exact edits to a published post that has no knowledge/upgrade-* source file (Junia pages,
older pages). Built 2026-10-19 for the keyword-harvest page expansions (knowledge/page-expansions.md).

    python patch_live.py --post-id 651 --show "Pricing"                      # print the raw block around a phrase
    python patch_live.py --post-id 651 --replace "old exact text" "new text"  # dry run (exactly 1 match required)
    python patch_live.py --post-id 651 --insert-before "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">FAQ" snippet.html
    python patch_live.py --post-id 372 --meta-description "New Rank Math description"
    ... --apply                                                               # write (backup first)
    python patch_live.py --restore backups/patch-<id>-<time>.json
    python patch_live.py --post-id 276 --page --replace "old" "new"            # a WordPress page (e.g. the homepage)

Safety: dry run by default; every --replace / --insert-before anchor must match the raw content exactly once;
full backup (raw content, title, live meta description) before writing; refuses posts that have an upgrade file
(edit the Markdown and use upload_draft.py --replace-live instead); status and slug must be unchanged afterwards,
otherwise it restores at once; under the autopilot it counts toward the daily "uploads" cap.
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
API = f"{SITE}/wp-json/wp/v2"
BACKUP_DIR = Path("backups")


def upgrade_file_ids():
    return {int(m.group(1)) for f in Path("knowledge").glob("upgrade-*.md") if (m := re.match(r"upgrade-(\d+)-", f.name))}


def live_meta_description(link):
    h = requests.get(link, params={"nocache": datetime.now().timestamp()}, timeout=60).text
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    return html_lib.unescape(m.group(1)) if m else ""


def main():
    ap = argparse.ArgumentParser(description="Exact, backed-up edits to a published post without an upgrade file.")
    ap.add_argument("--post-id", type=int)
    ap.add_argument("--show", metavar="PHRASE")
    ap.add_argument("--replace", nargs=2, action="append", default=[], metavar=("OLD", "NEW"))
    ap.add_argument("--insert-before", nargs=2, action="append", default=[], metavar=("ANCHOR", "HTML_FILE"))
    ap.add_argument("--meta-description")
    ap.add_argument("--page", action="store_true", help="the ID is a WordPress page (e.g. the homepage), not a post")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", metavar="BACKUP.json")
    a = ap.parse_args()

    from upload_draft import make_session, wp
    session, _ = make_session()

    if a.restore:
        data = json.loads(Path(a.restore).read_text(encoding="utf-8"))
        wp(session, "POST", f"{API}/{data.get('kind', 'posts')}/{data['id']}", "Restore failed.", json={"content": data["content"]})
        if data.get("meta_description"):
            session.post(f"{SITE}/wp-json/rankmath/v1/updateMeta", timeout=60, json={
                "objectType": "post", "objectID": data["id"], "meta": {"rank_math_description": data["meta_description"]}})
        print(f"✅ Restored post {data['id']} from {a.restore}")
        return

    if not a.post_id:
        sys.exit("Use --post-id (or --restore).")
    kind = "pages" if a.page else "posts"
    if a.post_id in upgrade_file_ids():
        sys.exit(f"ABORT: post {a.post_id} has a knowledge/upgrade-{a.post_id}-*.md file. Edit it and use upload_draft.py --replace-live.")
    post = wp(session, "GET", f"{API}/{kind}/{a.post_id}", f"Could not load post {a.post_id}.", params={"context": "edit"})
    raw = post["content"]["raw"]
    print(f"Post {a.post_id} /{post['slug']}/ ({post['status']}) · {len(raw)} characters")

    if a.show:
        i = raw.find(a.show)
        print(raw[max(0, i - 300): i + 700] if i >= 0 else f"'{a.show}' not found")
        return

    new = raw
    for old, rep in a.replace:
        n = new.count(old)
        if n != 1:
            sys.exit(f"ABORT: --replace needs exactly 1 match, found {n}: {old[:80]!r}")
        new = new.replace(old, rep)
        print(f"  ✎ replace: {old[:70]!r} → {rep[:70]!r}")
    for anchor, html_file in a.insert_before:
        anchor = anchor.replace("\\n", "\n")
        n = new.count(anchor)
        if n != 1:
            sys.exit(f"ABORT: --insert-before needs exactly 1 match, found {n}: {anchor[:80]!r}")
        snippet = Path(html_file).read_text(encoding="utf-8").strip() + "\n\n"
        new = new.replace(anchor, snippet + anchor)
        print(f"  + insert {len(snippet)} characters from {html_file} before {anchor[:60]!r}")
    if a.meta_description:
        print(f"  ✎ meta description ({len(a.meta_description)} chars): {a.meta_description}")
    if new == raw and not a.meta_description:
        sys.exit("Nothing to change.")
    if not a.apply:
        print("\nDRY RUN: nothing changed. Add --apply.")
        return

    from autopilot import guard
    if guard.allowance("uploads", 1) < 1:
        sys.exit(f"AUTOPILOT: daily cap reached ({guard.DAILY_CAPS['uploads']} uploads per day). Nothing changed.")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"patch-{a.post_id}-{datetime.now():%Y%m%d-%H%M%S}.json"
    backup.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "id": a.post_id, "kind": kind,
                                  "content": raw, "title": post["title"]["raw"],
                                  "meta_description": live_meta_description(post["link"])}, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    print(f"\n💾 Backup: {backup}")
    undo = f"python patch_live.py --restore {backup}"
    if new != raw:
        result = wp(session, "POST", f"{API}/{kind}/{a.post_id}", "WordPress rejected the update.", json={"content": new})
        if result.get("status") != post["status"] or result.get("slug") != post["slug"]:
            wp(session, "POST", f"{API}/{kind}/{a.post_id}", f"RESTORE FAILED: run {undo}", json={"content": raw})
            sys.exit("SAFETY ERROR: status/slug changed; content restored.")
    if a.meta_description:
        rm = session.post(f"{SITE}/wp-json/rankmath/v1/updateMeta", timeout=60, json={
            "objectType": "post", "objectID": a.post_id, "meta": {"rank_math_description": a.meta_description}})
        print("   Rank Math description saved." if rm.status_code < 400 else f"   ⚠️ Rank Math description NOT saved (HTTP {rm.status_code})")
    guard.record("uploads", 1, target=f"post {a.post_id}", detail="patch_live", undo=undo)
    print(f"✅ Post {a.post_id} updated (status {post['status']}, same URL)\n   Undo: {undo}")


if __name__ == "__main__":
    main()
