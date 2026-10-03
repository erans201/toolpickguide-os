"""
retire_post.py: retire a duplicate post safely: 301 redirect it, then move it to the Trash.

    python retire_post.py --post-id 508 --redirect-to /best-practice-management-accountants/ --also-trash 509
    python retire_post.py ... --apply

Default is a DRY RUN (public checks only). With --apply:
  1. Backs up each post (full content, meta) to backups/retired-<id>-<time>.json
  2. Creates a Rank Math 301 redirect from the post's URL to --redirect-to (before trashing)
  3. Moves the post to the WordPress Trash (recoverable: Posts → Trash → Restore). Never force-deletes.
  4. --also-trash IDs: drafts only, no redirect needed (they were never public)
  5. Verifies the old URL now answers 301 → target

Never runs from the scheduler.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
API = f"{SITE}/wp-json/wp/v2"
BACKUP_DIR = Path("backups")


def refuse_in_scheduler():
    import os
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: retiring posts never runs from the scheduler. Run it yourself.")


def backup_post(session, post_id):
    from upload_draft import wp
    post = wp(session, "GET", f"{API}/posts/{post_id}", f"Could not load post {post_id}.", params={"context": "edit"})
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    path = BACKUP_DIR / f"retired-{post_id}-{datetime.now():%Y%m%d-%H%M%S}.json"
    path.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "post": post},
                               indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"   💾 Backup: {path}")
    return post


def trash(session, post_id):
    from upload_draft import wp
    result = wp(session, "DELETE", f"{API}/posts/{post_id}", f"Could not move post {post_id} to Trash.")  # no force → Trash
    if result.get("status") != "trash":
        sys.exit(f"SAFETY ERROR: post {post_id} is '{result.get('status')}' after delete request. Check WP admin.")
    print(f"   🗑️  Post {post_id} moved to Trash (restore: Posts → Trash → Restore)")


VERIFY_HEADERS = {"Cache-Control": "no-cache", "Pragma": "no-cache", "User-Agent": "ToolPickGuide-Verify/1.0"}


def redirect_ok(url, target_url):
    r = requests.get(url, timeout=30, allow_redirects=False, headers=VERIFY_HEADERS)
    loc = r.headers.get("Location", "")
    return r.status_code == 301 and loc.split("?")[0].rstrip("/") == target_url.rstrip("/"), r.status_code, loc


def trash_then_verify(session, post, target, target_url, explain_error, wp, attempts=6, wait=10):
    """Trash first (LiteSpeed purges the post's cache on status change), then prove the 301 works.
    If it doesn't, restore the post exactly as it was (status + slug), so the URL never stays broken."""
    import time

    full = backup_post(session, post["id"])
    # Best effort: create the redirect via Rank Math with a relative destination (Hostinger's firewall
    # blocked a full https:// URL before). If blocked, rely on the redirect the user created by hand.
    rm = session.post(f"{SITE}/wp-json/rankmath/v1/updateRedirection", timeout=60, json={
        "objectID": post["id"], "objectType": "post", "hasRedirect": True,
        "redirectionUrl": target, "redirectionType": "301"})
    print(f"   ↪️  Rank Math redirect via API: {'created' if rm.status_code < 400 else 'blocked (HTTP %s); using the one set by hand' % rm.status_code}")

    trash(session, post["id"])
    for i in range(1, attempts + 1):
        ok, code, loc = redirect_ok(post["link"], target_url)
        print(f"   check {i}/{attempts}: HTTP {code} {loc}")
        if ok:
            print(f"\n✅ Retired: {post['link']} → 301 {target_url}. Post {post['id']} is in the Trash (recoverable).")
            return
        time.sleep(wait)

    print("\n⚠️ The redirect didn't appear. Restoring the post so the URL keeps working…")
    restored = wp(session, "POST", f"{API}/posts/{post['id']}", "RESTORE FAILED: restore it from Posts → Trash now.",
                  json={"status": full["status"], "slug": full["slug"]})
    sys.exit(f"ROLLED BACK: post {post['id']} is '{restored.get('status')}' at /{restored.get('slug')}/ again.\n"
             "  The Rank Math redirect for this URL is missing or inactive. Add it in Rank Math → Redirections, then re-run.")


def main():
    parser = argparse.ArgumentParser(description="301-redirect a duplicate post, then move it to Trash.")
    parser.add_argument("--post-id", type=int, required=True, help="Published duplicate to retire")
    parser.add_argument("--redirect-to", required=True, help="Target path on this site, e.g. /best-practice-management-accountants/")
    parser.add_argument("--also-trash", type=int, nargs="*", default=[], help="Draft post IDs to trash (no redirect)")
    parser.add_argument("--redirect-already-set", action="store_true",
                        help="The 301 was created by hand (e.g. Hostinger's firewall blocks the API). Verify it works, then trash")
    parser.add_argument("--trash-then-verify", action="store_true",
                        help="When a stuck page cache hides the redirect: trash (purges the cache), verify the 301, "
                             "and automatically restore the post if the redirect doesn't work")
    parser.add_argument("--apply", action="store_true", help="Make the changes (default: dry run)")
    args = parser.parse_args()

    target = args.redirect_to if args.redirect_to.startswith("/") else "/" + args.redirect_to
    target_url = SITE + target

    # --- public checks (dry run and apply) ---
    pub = requests.get(f"{API}/posts/{args.post_id}", params={"_fields": "id,slug,status,link"}, timeout=30)
    if pub.status_code != 200:
        sys.exit(f"ABORT: post {args.post_id} is not publicly visible (HTTP {pub.status_code}). Already retired?")
    post = pub.json()
    if post["link"].rstrip("/") == target_url.rstrip("/"):
        sys.exit("ABORT: redirect target is the post's own URL.")
    t = requests.get(target_url, timeout=30, allow_redirects=False)
    if t.status_code != 200:
        sys.exit(f"ABORT: redirect target {target_url} answers HTTP {t.status_code}, not 200.")

    print(f"Retire post {args.post_id}: {post['link']}  (status: {post['status']})")
    print(f"  1. 301 redirect  → {target_url}  (target OK, HTTP 200)")
    print(f"  2. Move {args.post_id} to Trash (recoverable)")
    for d in args.also_trash:
        print(f"  3. Move draft {d} to Trash (drafts only; no redirect)")
    if not args.apply:
        print("\nDRY RUN: nothing changed. Add --apply to run.")
        return

    refuse_in_scheduler()
    from upload_draft import explain_error, make_session, wp
    session, _ = make_session()

    print(f"\n[{args.post_id}]")
    if args.trash_then_verify:
        trash_then_verify(session, post, target, target_url, explain_error, wp)
        return
    if args.redirect_already_set:
        # Rank Math redirects fire even while the post is still published, so this proves it works before trashing.
        # Plain URL (no query string: Rank Math "exact" redirects don't match URLs with ?params) + no-cache headers.
        chk = requests.get(post["link"], timeout=30, allow_redirects=False,
                           headers={"Cache-Control": "no-cache", "Pragma": "no-cache", "User-Agent": "ToolPickGuide-Verify/1.0"})
        loc = chk.headers.get("Location", "")
        if chk.status_code != 301 or loc.split("?")[0].rstrip("/") != target_url.rstrip("/"):
            sys.exit(f"ABORT: {post['link']} answers HTTP {chk.status_code} {loc or '(no redirect)'}, not 301 → {target_url}.\n"
                     "  Nothing was trashed. Check the redirect in Rank Math → Redirections (and purge LiteSpeed cache), then re-run.")
        print(f"   ↪️  Existing 301 verified: {post['link']} → {target_url}")
        backup_post(session, args.post_id)
    else:
        full = backup_post(session, args.post_id)
        rm = session.post(f"{SITE}/wp-json/rankmath/v1/updateRedirection", timeout=60, json={
            "objectID": args.post_id, "objectType": "post", "hasRedirect": True,
            "redirectionUrl": target_url, "redirectionType": "301"})
        if rm.status_code >= 400:
            sys.exit("ABORT: Rank Math redirect failed, so the post was NOT trashed.\n" + explain_error(rm) +
                     "\n  If the error is an HTML 'Access Denied' page, Hostinger's firewall blocked it: create the 301 by hand in"
                     "\n  Rank Math → Redirections, then re-run with --redirect-already-set.")
        print(f"   ↪️  Rank Math 301 created: /{full['slug']}/ → {target}")
    trash(session, args.post_id)

    for d in args.also_trash:
        print(f"\n[{d}]")
        draft = wp(session, "GET", f"{API}/posts/{d}", f"Could not load post {d}.", params={"context": "edit"})
        if draft["status"] != "draft":
            print(f"   ⚠️ Post {d} is '{draft['status']}', not a draft. Skipped (retire it with its own redirect).")
            continue
        backup_post(session, d)
        trash(session, d)

    old = requests.get(post["link"], timeout=30, allow_redirects=False)
    loc = old.headers.get("Location", "")
    ok = old.status_code == 301 and loc.rstrip("/") == target_url.rstrip("/")
    print(f"\nVerify: {post['link']} → HTTP {old.status_code} {loc}  {'✅' if ok else '⚠️ not redirecting yet (cache?). Re-check in a few minutes'}")


if __name__ == "__main__":
    main()
