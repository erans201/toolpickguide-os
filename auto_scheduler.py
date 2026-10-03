"""
auto_scheduler.py: hands-free uploader for ToolPickGuide drafts.

Designed to run from Windows Task Scheduler (via run_scheduler.bat). Each run:
  1. Scans knowledge/*.md for articles whose Publishing Meta "Status" row
     contains READY FOR UPLOAD (the opt-in gate: nothing else is touched).
  2. Skips anything already uploaded (tracked in upload_state.json).
  3. Runs `upload_draft.py <file> --upload` for each new READY file.
  4. Records the WordPress Post ID in upload_state.json, logs/auto_scheduler.log,
     and the Upload Log section of INDEX.md.

    python auto_scheduler.py            # real run (uploads READY files)
    python auto_scheduler.py --dry-run  # same scan, but upload_draft runs without --upload
    python auto_scheduler.py --retry-failed  # retry files that failed, even if unchanged
    python auto_scheduler.py --update-changed  # also push edits of already-uploaded files to their WP drafts

Safety:
  - upload_draft.py hard-codes status "draft" and refuses to overwrite an existing slug.
  - A file is uploaded at most once. If it changes after upload, it is skipped unless
    --update-changed is passed (never by the scheduled task). Updates only touch posts that
    are still drafts and haven't been edited in WordPress since the last upload.
  - A failed upload is not retried until the file changes (no hourly error spam).
  - A lock file prevents two runs overlapping.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
READY_MARKER = "READY FOR UPLOAD"
STATUS_ROW = re.compile(r"^\|\s*Status\s*\|(.+)\|\s*$", re.MULTILINE)
POST_ID = re.compile(r"Draft (?:created|updated): ID (\d+)")
MODIFIED = re.compile(r"modified_gmt: (\S+)")


def log(log_file, message):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {message}"
    print(line)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_ready(path):
    match = STATUS_ROW.search(path.read_text(encoding="utf-8"))
    return bool(match and READY_MARKER in match.group(1).upper())


def load_state(state_file):
    if state_file.is_file():
        return json.loads(state_file.read_text(encoding="utf-8"))
    return {}


def save_state(state_file, state):
    state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_index(index_file, rel_path, post_id):
    """Append a row under '## 📤 Upload Log' in INDEX.md (created by hand, never overwritten)."""
    if not index_file.is_file():
        return
    text = index_file.read_text(encoding="utf-8")
    row = f"| {datetime.now():%Y-%m-%d %H:%M} | `{rel_path}` | {post_id} | draft | auto_scheduler |\n"
    if "## 📤 Upload Log" not in text:
        return
    index_file.write_text(text.rstrip("\n") + "\n" + row, encoding="utf-8")


def run_upload(article, dry_run, extra=()):
    cmd = [sys.executable, str(ROOT / "upload_draft.py"), str(article), *extra]
    if not dry_run:
        cmd.append("--upload")
    # upload_draft prints emoji; force UTF-8 so a redirected Windows console doesn't crash.
    # TPG_SCHEDULER makes upload_draft refuse --replace-live/--restore (published pages are user-run only).
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "TPG_SCHEDULER": "1"}
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env, timeout=300)
    return result.returncode, (result.stdout + result.stderr).strip()


def main():
    parser = argparse.ArgumentParser(description="Upload READY articles in knowledge/ as WordPress drafts.")
    parser.add_argument("--dry-run", action="store_true", help="Scan and parse only. Nothing is sent to WordPress")
    parser.add_argument("--retry-failed", action="store_true", help="Retry previously failed files even if unchanged")
    parser.add_argument("--update-changed", action="store_true", help="Push edits of already-uploaded files to their WP drafts")
    parser.add_argument("--overwrite-wp-edits", nargs="+", default=[], metavar="FILE.md",
                        help="With --update-changed: replace these drafts even if edited in WordPress (e.g. editor autosave)")
    parser.add_argument("--knowledge-dir", default=str(ROOT / "knowledge"))
    parser.add_argument("--state-file", default=str(ROOT / "upload_state.json"))
    parser.add_argument("--log-file", default=str(ROOT / "logs" / "auto_scheduler.log"))
    parser.add_argument("--index-file", default=str(ROOT / "INDEX.md"))
    args = parser.parse_args()

    knowledge = Path(args.knowledge_dir)
    state_file, log_file, index_file = Path(args.state_file), Path(args.log_file), Path(args.index_file)
    lock = state_file.with_suffix(".lock")

    if lock.exists():
        log(log_file, "SKIP: another run is in progress (lock file present). Delete it if a run crashed.")
        return
    lock.write_text(str(os.getpid()), encoding="utf-8")

    try:
        state = load_state(state_file)
        mode = "DRY RUN" if args.dry_run else "LIVE"
        articles = sorted(p for p in knowledge.glob("*.md") if p.is_file())
        ready = [p for p in articles if is_ready(p)]
        log(log_file, f"--- {mode} run: {len(articles)} article(s) scanned, {len(ready)} marked {READY_MARKER} ---")

        for article in ready:
            key = article.name
            digest = file_hash(article)
            entry = state.get(key, {})

            if entry.get("status") == "uploaded":
                if entry.get("sha256") == digest:
                    continue
                if not args.update_changed:
                    log(log_file, f"SKIP {key}: changed after upload (post {entry.get('post_id')}). Run with --update-changed to push it.")
                    continue
                baseline = entry.get("modified_gmt") or datetime.fromisoformat(entry["uploaded_at"]).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
                extra = ["--post-id", str(entry["post_id"]), "--expect-modified", baseline]
                if key in {Path(f).name for f in args.overwrite_wp_edits}:
                    extra.append("--overwrite-wp-edits")
                    log(log_file, f"OVERRIDE {key}: --overwrite-wp-edits requested by user")
                code, output = run_upload(article, args.dry_run, extra)
                modified = MODIFIED.search(output)
                if args.dry_run:
                    log(log_file, f"DRY RUN {key}: update parse {'OK' if code == 0 else 'FAILED'} (exit {code})")
                elif code == 0 and modified:
                    entry.update({"sha256": digest, "modified_gmt": modified.group(1), "updated_at": datetime.now().isoformat(timespec="seconds")})
                    log(log_file, f"UPDATED {key}: WordPress draft ID {entry['post_id']}")
                    if "NOT saved" in output:
                        log(log_file, f"  NOTE {key}: Rank Math meta not saved. See output below.\n{output[-800:]}")
                    save_state(state_file, state)
                else:
                    log(log_file, f"UPDATE FAILED {key} (exit {code}). Output:\n{output[-800:]}")
                continue
            if entry.get("status") == "failed" and entry.get("sha256") == digest and not args.retry_failed:
                continue  # unchanged since last failure. Change the file or pass --retry-failed

            code, output = run_upload(article, args.dry_run)
            post = POST_ID.search(output)

            if args.dry_run:
                log(log_file, f"DRY RUN {key}: parse {'OK' if code == 0 else 'FAILED'} (exit {code})")
                if code != 0:
                    log(log_file, output[-800:])
                continue

            if code == 0 and post:
                modified = MODIFIED.search(output)
                state[key] = {"status": "uploaded", "post_id": int(post.group(1)), "sha256": digest,
                              "uploaded_at": datetime.now().isoformat(timespec="seconds"),
                              "modified_gmt": modified.group(1) if modified else None}
                log(log_file, f"UPLOADED {key}: WordPress draft ID {post.group(1)}")
                if "NOT saved" in output:
                    log(log_file, f"  NOTE {key}: Rank Math meta not saved. Set it in WP admin (see upload_draft output).")
                append_index(index_file, f"knowledge/{key}", post.group(1))
            else:
                state[key] = {"status": "failed", "sha256": digest, "failed_at": datetime.now().isoformat(timespec="seconds")}
                log(log_file, f"FAILED {key} (exit {code}). Will retry when the file changes. Output:\n{output[-800:]}")

            save_state(state_file, state)
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
