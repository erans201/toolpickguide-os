"""
inject_links.py: contextual internal links INSIDE existing sentences, driven by the roadmap in ONSITE_PLANS.md.

Reads the "CONTEXTUAL LINK ROADMAP" table in ONSITE_PLANS.md:
    | ID | Source post | Anchor phrase | Target | Status |
Rows with Status TODO are processed. For each, the first natural occurrence of the anchor phrase in a
paragraph or list item of the source post (not inside an existing link, heading, or script) becomes a link
to the target page.

    python inject_links.py                  # SAFE DRY RUN (default): public read-only checks + preview
    python inject_links.py --upload         # back up each post, then write to WordPress (the user runs this)
    python inject_links.py --only IL-7a     # one roadmap row (works with --upload)
    python inject_links.py --restore backups/inject-<id>-<time>.json

Credentials: WP_SITE_URL / WP_USERNAME / WP_APPLICATION_PASSWORD from .env (via upload_draft.make_session).

Safety:
  - Dry run unless --upload. One link per roadmap row; at most 3 new links per post per run.
  - Backs up each post's raw content to backups/ before writing; sends only "content"; verifies status/slug after.
  - Skips: target already linked from the post, self-links, phrase not found, target not live (HTTP 200).
  - Refuses posts that have a knowledge/upgrade-<ID>-*.md source file (edit the Markdown, then --replace-live),
    so this tool and the upgrade files can never overwrite each other. Block-style links stay with link_injector.py.
  - Never runs from the scheduler.
  - Affiliate rows (2026-10-05): a Target that is a full https:// URL is an approved affiliate link; it gets
    rel="sponsored nofollow noopener" and must resolve to HTTP 200.
  - Autopilot (TPG_AUTOPILOT=1, AUTOPILOT.md): kill switch, max 6 links per day across runs, and every write is
    re-read; if a link is missing or status/slug changed, the post is restored at once and a strike is recorded.
"""

import argparse
import glob
import html as html_lib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

from autopilot import guard

SITE = "https://toolpickguide.com"
API = f"{SITE}/wp-json/wp/v2"
ROADMAP_FILE = Path("ONSITE_PLANS.md")
ROADMAP_HEADING = "CONTEXTUAL LINK ROADMAP"
BACKUP_DIR = Path("backups")
MAX_PER_POST = 3
BLOCK = re.compile(r"<(p|li)\b[^>]*>(.*?)</\1>", re.S | re.I)


def refuse_in_scheduler():
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit("ABORT: inject_links never runs from the scheduler.")


def load_roadmap(only=None):
    text = ROADMAP_FILE.read_text(encoding="utf-8")
    head = re.search(rf"^##[^\n]*{ROADMAP_HEADING}", text, re.M)  # the heading line, not a mention in prose
    if not head:
        sys.exit(f"ERROR: no '## … {ROADMAP_HEADING}' section in {ROADMAP_FILE}.")
    section = text[head.start():]
    nxt = re.search(r"\n## ", section[3:])
    section = section[: nxt.start() + 3] if nxt else section
    rows = []
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"IL-\w+", cells[0]):
            continue
        rid, source, anchor, target, status = cells[:5]
        rows.append({"id": rid, "source": int(re.sub(r"\D", "", source)), "anchor": anchor.strip('"“”'),
                     "target": target.strip("` ") if target.strip("` ").startswith("http") else "/" + target.strip("`/ ") + "/",
                     "status": status.upper()})
    if only:
        rows = [r for r in rows if r["id"] == only]
    return rows


def upgrade_file_posts():
    return {int(m.group(1)) for f in glob.glob("knowledge/upgrade-*.md") if (m := re.search(r"upgrade-(\d+)", f))}


def insert_link(content, anchor, target):
    """Link the first natural occurrence of `anchor`. Returns (new_content, preview) or (None, reason)."""
    href_variants = (f'href="{target}"', f'href="{SITE}{target}"', f'href="{target.rstrip("/")}"')
    if any(h in content for h in href_variants):
        return None, "already linked from this post"
    phrase = re.compile(rf"(?<![\w-])({re.escape(anchor)})(?![\w-])", re.I)
    for m in BLOCK.finditer(content):
        inner = m.group(2)
        parts = re.split(r"(<[^>]+>)", inner)
        in_link = False
        for i, part in enumerate(parts):
            if part.startswith("<"):
                if re.match(r"<a\b", part, re.I):
                    in_link = True
                elif re.match(r"</a>", part, re.I):
                    in_link = False
                continue
            if in_link:
                continue
            hit = phrase.search(part)
            if not hit:
                continue
            attrs = ' rel="sponsored nofollow noopener" target="_blank"' if target.startswith("http") else ""  # affiliate row
            linked = part[: hit.start()] + f'<a href="{target}"{attrs}>{hit.group(1)}</a>' + part[hit.end():]
            new_inner = "".join(parts[:i] + [linked] + parts[i + 1:])
            s, e = m.start(2), m.end(2)
            new_content = content[:s] + new_inner + content[e:]
            plain = html_lib.unescape(re.sub(r"<[^>]+>", "", inner))
            k = plain.lower().find(hit.group(1).lower())
            preview = (plain[max(0, k - 70):k] + "[[" + hit.group(1) + " → " + target + "]]"
                       + plain[k + len(hit.group(1)):k + len(hit.group(1)) + 60]).strip()
            return new_content, preview
    return None, f'phrase "{anchor}" not found in a paragraph or list item (outside existing links)'


def target_live(target):
    try:
        if target.startswith("http"):  # affiliate link: must resolve to a working page
            return requests.get(target, timeout=30, allow_redirects=True).status_code == 200
        r = requests.get(SITE + target, timeout=30, allow_redirects=False)
        return r.status_code == 200
    except requests.RequestException:
        return False


def link_present(raw, target):
    return re.search(r'href="(?:' + re.escape(SITE) + r')?' + re.escape(target) + '"', raw) is not None


def undo_failed(session, pid, entry, backup, why):
    """Autopilot: put the original content back at once and record a strike."""
    from upload_draft import wp
    wp(session, "POST", f"{API}/posts/{pid}", f"RESTORE FAILED for post {pid}: run python inject_links.py --restore {backup}",
       json={"content": entry["original"]})
    paused = guard.strike(f"inject_links post {pid}: {why}")
    print(f"⚠️  ALERT post {pid}: {why}. Restored from {backup}." + (" Autopilot is now PAUSED (2 strikes)." if paused else ""))


def restore(path):
    from upload_draft import make_session, wp
    session, _ = make_session()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    post = wp(session, "POST", f"{API}/posts/{data['id']}", "Restore failed.", json={"content": data["content"]})
    print(f"✅ Restored post {post['id']} content from {path}")


def main():
    ap = argparse.ArgumentParser(description="Contextual internal links from ONSITE_PLANS.md (dry run by default).")
    ap.add_argument("--upload", action="store_true", help="write to WordPress (backup first)")
    ap.add_argument("--apply", action="store_true", help=argparse.SUPPRESS)  # alias, matches the other tools
    ap.add_argument("--only", metavar="IL-ID")
    ap.add_argument("--restore", metavar="BACKUP.json")
    a = ap.parse_args()
    refuse_in_scheduler()
    if a.restore:
        return restore(a.restore)
    write = a.upload or a.apply
    guard.stop_if_paused()
    day_budget = guard.allowance("links", 10**6) if write else 10**6

    rows = load_roadmap(a.only)
    todo = [r for r in rows if r["status"] == "TODO"]
    print(f"Roadmap: {len(rows)} row(s) · {len(todo)} TODO · mode: {'UPLOAD' if write else 'DRY RUN'}\n")
    protected = upgrade_file_posts()
    session = None
    if write:
        from upload_draft import make_session, wp
        session, _ = make_session()

    per_post, posts = {}, {}
    for r in todo:
        tag = f"{r['id']}: post {r['source']} → {r['target']} on \"{r['anchor']}\""
        if r["source"] in protected:
            print(f"⏭️  {tag}\n    skipped: post {r['source']} has an upgrade file. Add the link in its Markdown and use --replace-live.\n")
            continue
        if not target_live(r["target"]):
            print(f"⛔ {tag}\n    skipped: target is not live (HTTP 200 required).\n")
            continue
        if sum(per_post.values()) >= day_budget:
            print(f"⏭️  {tag}\n    skipped: autopilot daily cap reached ({guard.DAILY_CAPS['links']} links per day).\n")
            continue
        if per_post.get(r["source"], 0) >= MAX_PER_POST:
            print(f"⏭️  {tag}\n    skipped: already {MAX_PER_POST} new links for this post in this run.\n")
            continue
        if r["source"] not in posts:
            if write:
                p = wp(session, "GET", f"{API}/posts/{r['source']}", f"Could not load post {r['source']}.", params={"context": "edit"})
                posts[r["source"]] = {"post": p, "content": p["content"]["raw"], "original": p["content"]["raw"]}
            else:
                p = requests.get(f"{API}/posts/{r['source']}", params={"_fields": "id,slug,status,link,content"}, timeout=30).json()
                posts[r["source"]] = {"post": p, "content": p["content"]["rendered"], "original": p["content"]["rendered"]}
        entry = posts[r["source"]]
        if f"/{entry['post']['slug']}/" == r["target"]:
            print(f"⏭️  {tag}\n    skipped: self-link.\n")
            continue
        new, info = insert_link(entry["content"], r["anchor"], r["target"])
        if new is None:
            print(f"⏭️  {tag}\n    skipped: {info}\n")
            continue
        entry["content"] = new
        entry.setdefault("ids", []).append(r["id"])
        entry.setdefault("targets", []).append(r["target"])
        per_post[r["source"]] = per_post.get(r["source"], 0) + 1
        print(f"✅ {tag}\n    …{info}…\n")

    changed = {pid: e for pid, e in posts.items() if e["content"] != e["original"]}
    if not write:
        print(f"DRY RUN: nothing changed. {sum(per_post.values())} link(s) would be added to {len(changed)} post(s). "
              "Run with --upload to write.")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for pid, e in changed.items():
        backup = BACKUP_DIR / f"inject-{pid}-{datetime.now():%Y%m%d-%H%M%S}.json"
        backup.write_text(json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "id": pid,
                                      "content": e["original"]}, indent=2, ensure_ascii=False), encoding="utf-8")
        result = wp(session, "POST", f"{API}/posts/{pid}", "WordPress rejected the update.", json={"content": e["content"]})
        if result.get("status") != e["post"]["status"] or result.get("slug") != e["post"]["slug"]:
            if guard.active():
                undo_failed(session, pid, e, backup, "status/slug changed")
                continue
            sys.exit(f"SAFETY ERROR: post {pid} status/slug changed. Restore: python inject_links.py --restore {backup}")
        if guard.active():
            check = wp(session, "GET", f"{API}/posts/{pid}", f"Could not re-read post {pid}.", params={"context": "edit"})
            missing = [t for t in e["targets"] if not link_present(check["content"]["raw"], t)]
            if missing:
                undo_failed(session, pid, e, backup, f"links missing after write: {', '.join(missing)}")
                continue
        undo = f"python inject_links.py --restore {backup}"
        guard.record("links", per_post[pid], target=f"post {pid}", detail=", ".join(e["ids"]), undo=undo)
        print(f"💾 {backup}\n✅ post {pid} updated ({per_post[pid]} link(s)). Undo: {undo}")
    print("\nNext: tell the agent. It verifies the live links and marks the roadmap rows DONE.")


if __name__ == "__main__":
    main()
