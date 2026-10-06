"""
publish_draft.py: publish a Junia draft that passes the QA gate (user decision 2026-10-06: "Articles on draft
status should be published by the agent"; permission rule added by the user). Dry run by default.

    python publish_draft.py --post-id 618                       # dry run: shows the checks, changes nothing
    python publish_draft.py --post-id 618 --apply               # publish (only if every check passes)
    python publish_draft.py --post-id 618 --unpublish --apply   # undo: back to draft

Checks before publishing (all must pass):
  - the post is a draft and has a Junia brief whose slug matches (knowledge/briefs/junia/*.md)
  - junia_draft's QA gate is clean (no unknown prices, banned words, long paragraphs, blocked links, missing tools …)
  - it has a featured image, and its slug is not already live in the sitemap (no cannibalization)
  - under the autopilot (TPG_AUTOPILOT=1): kill switch off and today's publish cap not reached
After publishing it verifies the page is public (REST 200 without login + the URL loads). If not, it sets the
post back to draft and records a strike.
"""

import argparse
import re
import sys
from pathlib import Path

import requests

import junia_draft as jd
from autopilot import guard

API, SITE = jd.API, jd.SITE


def brief_for(slug):
    for path in sorted(Path("knowledge/briefs/junia").glob("*.md")):
        b = jd.parse_brief(str(path))
        if b["slug"] == slug:
            return b
    return None


def live_slugs():
    idx = requests.get(f"{SITE}/sitemap_index.xml", timeout=60).text
    urls = []
    for sm in re.findall(r"<loc>(.*?)</loc>", idx):
        urls += re.findall(r"<loc>(.*?)</loc>", requests.get(sm, timeout=60).text)
    return {u.rstrip("/").rsplit("/", 1)[-1] for u in urls}


def checks(post, brief):
    """List of (ok, text). Publishing needs every ok to be True."""
    out = [(post["status"] == "draft", f"status is '{post['status']}' (must be draft)")]
    if not brief:
        return out + [(False, f"no Junia brief has slug '{post['slug']}'")]
    a = jd.analyze(post, brief)
    out.append((jd.gate_clean(a), "QA gate clean (details: python junia_draft.py --brief <brief> --post-id <ID>)"))
    out.append((bool(post.get("featured_media")), "has a featured image"))
    out.append((brief["slug"] not in live_slugs(), f"/{brief['slug']}/ is not already live"))
    return out


def main():
    ap = argparse.ArgumentParser(description="Publish a QA-clean Junia draft (dry run by default).")
    ap.add_argument("--post-id", type=int, required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--unpublish", action="store_true", help="undo: set a published post back to draft")
    a = ap.parse_args()
    guard.stop_if_paused()

    from upload_draft import make_session, wp
    session, _ = make_session()
    post = wp(session, "GET", f"{API}/posts/{a.post_id}", f"Could not load post {a.post_id}.", params={"context": "edit"})

    if a.unpublish:
        if not a.apply:
            print(f"DRY RUN: would set post {a.post_id} ('{post['status']}') back to draft. Add --apply.")
            return
        wp(session, "POST", f"{API}/posts/{a.post_id}", "Unpublish failed.", json={"status": "draft"})
        print(f"✅ Post {a.post_id} is a draft again.")
        return

    brief = brief_for(post["slug"])
    results = checks(post, brief)
    for ok, text in results:
        print(("✅ " if ok else "❌ ") + text)
    if not all(ok for ok, _ in results):
        sys.exit(f"NOT PUBLISHED: post {a.post_id} fails a check above.")
    if not a.apply:
        print(f"\nDRY RUN: post {a.post_id} would be published as /{brief['slug']}/. Add --apply.")
        return
    if guard.allowance("publishes", 1) < 1:
        sys.exit(f"AUTOPILOT: daily cap reached ({guard.DAILY_CAPS['publishes']} publishes per day). Not published.")

    wp(session, "POST", f"{API}/posts/{a.post_id}", "WordPress rejected the publish.", json={"status": "publish"})
    url = f"{SITE}/{brief['slug']}/"
    public = requests.get(f"{API}/posts/{a.post_id}", timeout=60).status_code == 200
    page = requests.get(url, timeout=60, headers={"User-Agent": "ToolPickGuide-Robot/1.0"}).status_code == 200
    undo = f"python publish_draft.py --post-id {a.post_id} --unpublish --apply"
    if not (public and page):
        wp(session, "POST", f"{API}/posts/{a.post_id}", f"REVERT FAILED: run {undo}", json={"status": "draft"})
        paused = guard.strike(f"publish {a.post_id}: not public after publishing (REST {public}, page {page})")
        sys.exit(f"⚠️ ALERT: post {a.post_id} did not verify as live; set back to draft." + (" Autopilot PAUSED." if paused else ""))
    guard.record("publishes", 1, target=f"post {a.post_id}", detail=url, undo=undo)
    print(f"✅ Published: {url}\nUndo: {undo}")


if __name__ == "__main__":
    main()
