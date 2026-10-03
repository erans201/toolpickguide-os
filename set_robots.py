"""
set_robots.py: switch posts to noindex (or back to index) through Rank Math. Links on the page stay followed.

    python set_robots.py --noindex 85 82 87 103 105 110 112            # dry run: shows the current robots tag per post
    python set_robots.py --noindex 85 82 87 103 105 110 112 --apply    # do it (backup first, then verify live)
    python set_robots.py --restore backups/robots-<time>.json          # undo: back to index

Rank Math drops noindexed posts from its sitemap automatically. The page stays live at the same URL;
only Google is told not to list it. Status, slug, and content are never touched.
Dry run by default. Never runs from the scheduler. The user runs --apply.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

SITE = "https://toolpickguide.com"
API = f"{SITE}/wp-json/wp/v2"
BACKUP_DIR = Path("backups")
ROBOTS = re.compile(r'<meta name="robots" content="([^"]*)"')
NO_CACHE = {"Cache-Control": "no-cache", "Pragma": "no-cache"}


def live_robots(link):
    m = ROBOTS.search(requests.get(link, headers=NO_CACHE, timeout=30).text)  # plain URL, no query string
    return m.group(1) if m else "(no robots tag)"


def apply(session, ids, robots):
    from upload_draft import wp
    for pid in ids:
        r = session.post(f"{SITE}/wp-json/rankmath/v1/updateMeta", timeout=60,
                         json={"objectType": "post", "objectID": pid, "meta": {"rank_math_robots": robots}})
        if r.status_code >= 400:
            sys.exit(f"ERROR: Rank Math refused post {pid} (HTTP {r.status_code}). Stopped; earlier posts are done.")
        p = wp(session, "GET", f"{API}/posts/{pid}", f"Could not load post {pid}.", params={"context": "edit"})
        wp(session, "POST", f"{API}/posts/{pid}", f"Could not re-save post {pid}.", json={"title": p["title"]["raw"]})  # purges LiteSpeed
        print(f"   ✓ post {pid} → {', '.join(robots)}")


def verify(posts, want):
    time.sleep(3)
    bad = 0
    for p in posts:
        now = live_robots(p["link"])
        ok = want in now and not (want == "index" and "noindex" in now)
        bad += not ok
        print(f"   {'✅' if ok else '⚠️ '} {p['id']} /{p['slug']}/  →  {now}")
    if bad:
        print("   ⚠️  Some pages still show the old tag. Purge LiteSpeed + Hostinger cache, then re-check the plain URL.")


def main():
    ap = argparse.ArgumentParser(description="Set noindex/index via Rank Math (dry run by default).")
    ap.add_argument("--noindex", type=int, nargs="*", default=[])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", metavar="BACKUP.json")
    a = ap.parse_args()
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: set_robots never runs from the scheduler.")

    if a.restore:
        from upload_draft import make_session
        data = json.loads(Path(a.restore).read_text(encoding="utf-8"))
        session, _ = make_session()
        print(f"Restoring index on {len(data['posts'])} post(s) from {a.restore}")
        apply(session, [p["id"] for p in data["posts"]], ["index"])
        verify(data["posts"], "index")
        return

    if not a.noindex:
        sys.exit("Nothing to do. Use --noindex IDS or --restore BACKUP.json")
    posts = []
    for pid in a.noindex:
        p = requests.get(f"{API}/posts/{pid}", params={"_fields": "id,slug,status,link"}, timeout=30).json()
        if p.get("status") != "publish":
            sys.exit(f"ABORT: post {pid} is not a published post.")
        p["robots_before"] = live_robots(p["link"])
        posts.append(p)
        print(f"  {pid} /{p['slug']}/  now: {p['robots_before']}  →  noindex, follow")
    if not a.apply:
        print("\nDRY RUN: nothing changed. Add --apply.")
        return

    from upload_draft import make_session
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"robots-{datetime.now():%Y%m%d-%H%M%S}.json"
    backup.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "posts": posts},
                                 indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n💾 Backup: {backup}")
    session, _ = make_session()
    apply(session, a.noindex, ["noindex"])
    print("\nLive check:")
    verify(posts, "noindex")
    print(f"\n   Undo: python set_robots.py --restore {backup}")


if __name__ == "__main__":
    main()
