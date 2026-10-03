"""
link_injector.py: add planned internal-link blocks to live posts (IL-1…IL-4 in ONSITE_PLANS.md).

Plan: wordpress/internal-link-plan.json. Each block is inserted just before the post's FAQ heading
(or at the end of the post), wrapped in <!-- tpg-links:ID --> markers.

    python link_injector.py                    # DRY RUN: public read-only checks + preview
    python link_injector.py --apply            # back up each post, then inject (user runs this)
    python link_injector.py --only IL-2        # limit to one plan ID (works with --apply)
    python link_injector.py --restore backups/links-<id>-<time>.json

Safety:
  - Backs up each post's full raw content to backups/ before writing it.
  - Sends only the "content" field: status, slug, title, and categories can't change. Verified after each write.
  - Idempotent: an existing marker block is replaced in place, never duplicated. Unchanged blocks are skipped.
  - Skips links the post already contains, and self-links. Aborts if a link target isn't live (HTTP 200).
  - Refuses posts that have a knowledge/upgrade-<ID>-*.md source (edit the Markdown, then --replace-live).
  - Never runs from the scheduler.
"""

import argparse
import glob
import html as html_lib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
API = f"{SITE}/wp-json/wp/v2"
PLAN = Path("wordpress/internal-link-plan.json")
BACKUP_DIR = Path("backups")
FAQ_H2 = re.compile(r"<h2[^>]*>(?:(?!</h2>).)*FAQ(?:(?!</h2>).)*</h2>", re.I | re.S)


def refuse_in_scheduler():
    import os
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: link injection never runs from the scheduler. Run it yourself.")


def load_plan(only=None):
    plan = json.loads(PLAN.read_text(encoding="utf-8"))["blocks"]
    jobs = [(pid, b) for b in plan if not only or b["id"] == only for pid in b["posts"]]
    if not jobs:
        sys.exit(f"ERROR: no plan entries{' for ' + only if only else ''} in {PLAN}.")
    return jobs


def upgrade_file_ids():
    return {int(m.group(1)) for f in glob.glob("knowledge/upgrade-*.md") if (m := re.search(r"upgrade-(\d+)-", f))}


def slug_of(href):
    return href.strip("/").split("/")[-1]


def build_block(block, existing_html, own_slug):
    """Marker-wrapped Custom HTML block. Returns (html, kept_links, skipped_links)."""
    body = re.sub(rf"<!-- tpg-links:{re.escape(block['id'])} -->.*?<!-- /tpg-links:{re.escape(block['id'])} -->", "",
                  existing_html, flags=re.S)
    kept, skipped = [], []
    for link in block["links"]:
        target = slug_of(link["href"])
        if target == own_slug:
            skipped.append((link["href"], "self-link"))
        elif re.search(rf'href="(?:{re.escape(SITE)})?/{re.escape(target)}/?"', body):
            skipped.append((link["href"], "already linked in the article"))
        else:
            kept.append(link)
    if not kept:
        return "", kept, skipped
    items = "\n".join(f'<li><a href="{l["href"]}">{html_lib.escape(l["anchor"])}</a>: {html_lib.escape(l["note"])}</li>'
                      for l in kept)
    inner = (f'<h3>{html_lib.escape(block["heading"])}</h3>\n<p>{html_lib.escape(block["intro"])}</p>\n<ul>\n{items}\n</ul>')
    html = (f"<!-- tpg-links:{block['id']} -->\n<!-- wp:html -->\n<div class=\"tpg-related-links\">\n{inner}\n</div>\n"
            f"<!-- /wp:html -->\n<!-- /tpg-links:{block['id']} -->\n\n")
    return html, kept, skipped


def insert(content, block_id, block_html):
    """Replace an existing marker block, else insert before the FAQ H2 (and its wp:heading comment), else append."""
    marker = re.compile(rf"<!-- tpg-links:{re.escape(block_id)} -->.*?<!-- /tpg-links:{re.escape(block_id)} -->\n*", re.S)
    if marker.search(content):
        return marker.sub(lambda _: block_html, content, count=1), "replaced existing block"
    faq = FAQ_H2.search(content)
    if faq:
        start = faq.start()
        heading_comment = content.rfind("<!-- wp:heading", 0, start)
        if heading_comment != -1 and not content[heading_comment:start].count("<!-- /wp:"):
            start = heading_comment
        return content[:start] + block_html + content[start:], "inserted before FAQ heading"
    return content.rstrip() + "\n\n" + block_html, "appended at end (no FAQ heading)"


def check_targets(jobs):
    bad = []
    for href in sorted({l["href"] for _, b in jobs for l in b["links"]}):
        code = requests.get(SITE + href, timeout=30, allow_redirects=False).status_code
        if code != 200:
            bad.append((href, code))
    if bad:
        sys.exit(f"ABORT: link targets not live: {bad}")


def run(apply, only):
    jobs = load_plan(only)
    refused = upgrade_file_ids()
    check_targets(jobs)
    print(f"Plan: {len(jobs)} post(s) · all link targets live (HTTP 200)\n")

    session = None
    if apply:
        refuse_in_scheduler()
        from upload_draft import make_session
        session, _ = make_session()
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for pid, block in jobs:
        if pid in refused:
            print(f"[{block['id']}] post {pid}: ⛔ refused: has a knowledge/upgrade-{pid}-*.md source. Edit that file instead.\n")
            continue
        if apply:
            from upload_draft import wp
            post = wp(session, "GET", f"{API}/posts/{pid}", f"Could not load post {pid}.", params={"context": "edit"})
            content, slug, status = post["content"]["raw"], post["slug"], post["status"]
        else:
            post = requests.get(f"{API}/posts/{pid}", params={"_fields": "slug,status,content"}, timeout=30).json()
            content, slug, status = post["content"]["rendered"], post["slug"], post["status"]

        block_html, kept, skipped = build_block(block, content, slug)
        print(f"[{block['id']}] post {pid} /{slug}/ ({status})")
        for href, why in skipped:
            print(f"   skip {href}: {why}")
        if not block_html:
            print("   nothing to add.\n")
            continue
        new_content, where = insert(content, block["id"], block_html)
        if new_content == content:
            print("   unchanged (block already up to date).\n")
            continue
        print(f"   + {len(kept)} link(s), {where}: {', '.join(l['href'] for l in kept)}")

        if not apply:
            print()
            continue
        backup = BACKUP_DIR / f"links-{pid}-{datetime.now():%Y%m%d-%H%M%S}.json"
        backup.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                      "id": pid, "slug": slug, "status": status, "content": content},
                                     indent=2, ensure_ascii=False), encoding="utf-8")
        result = wp(session, "POST", f"{API}/posts/{pid}", f"Could not update post {pid}. Live post unchanged.",
                    json={"content": new_content})
        if result.get("status") != status or result.get("slug") != slug:
            sys.exit(f"SAFETY ERROR: post {pid} changed status/slug. Restore: python link_injector.py --restore {backup}")
        print(f"   💾 backup {backup}\n   ✅ applied · undo: python link_injector.py --restore {backup}\n")

    print("DRY RUN: nothing changed. Add --apply to inject." if not apply else "Done. Re-crawl links to update ONSITE_PLANS.md.")


def restore(path):
    refuse_in_scheduler()
    from upload_draft import make_session, wp
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    session, _ = make_session()
    live = wp(session, "GET", f"{API}/posts/{data['id']}", f"Could not load post {data['id']}.", params={"context": "edit"})
    if live["slug"] != data["slug"]:
        sys.exit(f"ABORT: post {data['id']} slug is '{live['slug']}', backup is for '{data['slug']}'.")
    wp(session, "POST", f"{API}/posts/{data['id']}", "Restore failed.", json={"content": data["content"]})
    print(f"✅ Restored post {data['id']} content from {path}")


def main():
    parser = argparse.ArgumentParser(description="Inject planned internal-link blocks (dry run by default).")
    parser.add_argument("--apply", action="store_true", help="Back up, then write to WordPress")
    parser.add_argument("--only", metavar="IL-ID", help="Limit to one plan ID, e.g. IL-2")
    parser.add_argument("--restore", metavar="BACKUP.json", help="Undo from a backup file")
    args = parser.parse_args()
    if args.restore:
        restore(args.restore)
    else:
        run(args.apply, args.only)


if __name__ == "__main__":
    main()
