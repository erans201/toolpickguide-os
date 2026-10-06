# Local queue: live-page changes for the evening robot

The cloud robot can't change live pages. When it prepares one (price update in an upgrade file, image swap), it adds a row here with Status **TODO**. The local robot (`tpg-browser-ops`, daily 20:00 Israel time) runs each TODO row: dry run first, then the same command with the write flag, then it checks the page and sets Status to `DONE <date> · undo: <command>` (or `FAILED <date>: <reason>`).

**Allowed commands only:** `python upload_draft.py knowledge/upgrade-<ID>-<slug>.md --upload --replace-live <ID> --force-replace [--refresh-image]` and `python media_fix.py --post-id <ID> ... --apply`. Anything else stays TODO and is reported. Max 3 rows per day.

| Added | By | Page | What and why | Command | Status |
|---|---|---|---|---|---|
