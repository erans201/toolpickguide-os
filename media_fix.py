"""
media_fix.py: fix images in a WordPress post, and purge stale LiteSpeed cache by touching posts.

    python media_fix.py --post-id 558 --remove-img d8e70f5f --remove-img photo-1523437237164 --rehost \
        --featured-from-content --alt "Photography client questionnaire: ..." --touch 492 372          # dry run
    ... --apply                                                                                    # do it
    python media_fix.py --restore backups/media-558-<time>.json

  --remove-img PATTERN   remove every content image whose src contains PATTERN (its whole image block/figure)
  --rehost               copy external images (e.g. images.unsplash.com) into the Media Library and point
                         the post at the local copy (Unsplash license: free to use, no credit required)
  --alt TEXT             alt text for the remaining content images and the featured image
  --featured-from-content  make the first remaining content image the featured image
  --touch IDS            re-save these posts without changing content (LiteSpeed purges a post's cache on save)

Safety: dry run by default; full backup of the post before writing; never changes status, slug, or title text;
`--restore` puts the content and featured image back. Never runs from the scheduler.
"""

import argparse
import html as html_lib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
API = f"{SITE}/wp-json/wp/v2"
BACKUP_DIR = Path("backups")
IMG = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', re.S)


def image_spans(content):
    """[(start, end, src)] for each image, widened to its wp:image block, else its <figure>, else the <img> tag."""
    spans = []
    for m in IMG.finditer(content):
        s, e, src = m.start(), m.end(), html_lib.unescape(m.group(1))
        blk_open = content.rfind("<!-- wp:image", 0, s)
        blk_close = content.find("<!-- /wp:image -->", e)
        if blk_open != -1 and blk_close != -1 and "<!-- /wp:image -->" not in content[blk_open:s] and not IMG.search(content, e, blk_close):
            s, e = blk_open, blk_close + len("<!-- /wp:image -->")
        else:
            fig_open, fig_close = content.rfind("<figure", 0, s), content.find("</figure>", e)
            if fig_open != -1 and fig_close != -1 and "</figure>" not in content[fig_open:s] and not IMG.search(content, e, fig_close):
                s, e = fig_open, fig_close + len("</figure>")
        spans.append((s, e, src))
    return spans


def plan(content, patterns):
    keep, remove = [], []
    for s, e, src in image_spans(content):
        (remove if any(p in src for p in patterns) else keep).append((s, e, src))
    return keep, remove


def remove_spans(content, spans):
    for s, e, _ in sorted(spans, reverse=True):
        content = content[:s] + content[e:]
    return re.sub(r"\n{3,}", "\n\n", content)


def is_external(src):
    return src.startswith("http") and "toolpickguide.com" not in src


def refuse_in_scheduler():
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: media_fix never runs from the scheduler.")


def main():
    ap = argparse.ArgumentParser(description="Fix post images and purge stale cache (dry run by default).")
    ap.add_argument("--post-id", type=int)
    ap.add_argument("--remove-img", action="append", default=[], metavar="PATTERN")
    ap.add_argument("--rehost", action="store_true")
    ap.add_argument("--alt")
    ap.add_argument("--featured-from-content", action="store_true")
    ap.add_argument("--touch", type=int, nargs="*", default=[])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", metavar="BACKUP.json")
    a = ap.parse_args()
    refuse_in_scheduler()

    if a.restore:
        from upload_draft import make_session, wp
        session, _ = make_session()
        data = json.loads(Path(a.restore).read_text(encoding="utf-8"))
        wp(session, "POST", f"{API}/posts/{data['id']}", "Restore failed.",
           json={"content": data["content"], "featured_media": data["featured_media"]})
        print(f"✅ Restored post {data['id']} content and featured image from {a.restore}")
        return

    if a.post_id:
        pub = requests.get(f"{API}/posts/{a.post_id}", params={"_fields": "id,slug,status,content,featured_media"}, timeout=30).json()
        keep, remove = plan(pub["content"]["rendered"], a.remove_img)
        print(f"Post {a.post_id} /{pub['slug']}/ ({pub['status']})")
        for _, _, src in remove:
            print(f"  − remove image: {src[:95]}")
        for _, _, src in keep:
            print(f"  {'↻ re-host' if a.rehost and is_external(src) else '= keep   '} image: {src[:95]}")
        if a.featured_from_content:
            print(f"  ★ featured image ← first kept image{' (after re-hosting)' if a.rehost else ''}")
        if a.alt:
            print(f"  ✎ alt text: {a.alt}")
        if not keep and a.featured_from_content:
            sys.exit("ABORT: no image would remain to use as the featured image.")
    for t in a.touch:
        print(f"  ⟳ touch post {t} (re-save, no content change → LiteSpeed purges its cache)")
    if not a.apply:
        print("\nDRY RUN: nothing changed. Add --apply.")
        return

    from upload_draft import make_session, upload_image, wp
    session, _ = make_session()

    if a.post_id:
        post = wp(session, "GET", f"{API}/posts/{a.post_id}", f"Could not load post {a.post_id}.", params={"context": "edit"})
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup = BACKUP_DIR / f"media-{a.post_id}-{datetime.now():%Y%m%d-%H%M%S}.json"
        backup.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "id": post["id"],
                                      "content": post["content"]["raw"], "featured_media": post["featured_media"]},
                                     indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n💾 Backup: {backup}")

        content = post["content"]["raw"]
        keep, remove = plan(content, a.remove_img)
        content = remove_spans(content, remove)
        print(f"   − removed {len(remove)} image(s)")

        first_media = None
        for _, _, src in plan(content, [])[0]:
            new_src, media_id = src, None
            if a.rehost and is_external(src):
                r = requests.get(src, timeout=60)
                r.raise_for_status()
                ext = ".jpg" if "jpeg" in r.headers.get("Content-Type", "") or "unsplash" in src else ".png"
                tmp = BACKUP_DIR / f"rehost-{a.post_id}{ext}"
                tmp.write_bytes(r.content)
                media_id = upload_image(session, API, tmp, a.alt or "", f"{post['slug']}-photo")
                tmp.unlink()
                new_src = wp(session, "GET", f"{API}/media/{media_id}", "Could not read uploaded image.")["source_url"]
                content = content.replace(html_lib.escape(src, quote=True), new_src).replace(src, new_src)
                print(f"   ↻ re-hosted → media {media_id}")
            if a.alt:
                content = re.sub(rf'(<img\b[^>]*src="{re.escape(new_src)}"[^>]*?)\salt="[^"]*"', rf'\1 alt="{html_lib.escape(a.alt)}"', content)
                if f'alt="{html_lib.escape(a.alt)}"' not in content:
                    content = re.sub(rf'(<img\b)([^>]*src="{re.escape(new_src)}")', rf'\1 alt="{html_lib.escape(a.alt)}"\2', content, count=1)
                if media_id:
                    wp(session, "POST", f"{API}/media/{media_id}", "Could not set alt text.", json={"alt_text": a.alt})
            if first_media is None:
                first_media = media_id

        payload = {"content": content}
        if a.featured_from_content and first_media:
            payload["featured_media"] = first_media
        result = wp(session, "POST", f"{API}/posts/{a.post_id}", "WordPress rejected the update.", json=payload)
        if result.get("status") != post["status"] or result.get("slug") != post["slug"]:
            sys.exit(f"SAFETY ERROR: status/slug changed. Restore: python media_fix.py --restore {backup}")
        print(f"✅ Post {a.post_id} updated (status {result['status']}, same URL)"
              f"{f' · featured image → media {first_media}' if 'featured_media' in payload else ''}")
        print(f"   Undo: python media_fix.py --restore {backup}")

    for t in a.touch:
        p = wp(session, "GET", f"{API}/posts/{t}", f"Could not load post {t}.", params={"context": "edit"})
        wp(session, "POST", f"{API}/posts/{t}", f"Could not touch post {t}.", json={"title": p["title"]["raw"]})
        print(f"   ⟳ post {t} re-saved (cache purged)")


if __name__ == "__main__":
    main()
