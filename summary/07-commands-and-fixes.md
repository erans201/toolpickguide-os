# 07 · Commands and known fixes (2026-10-12)

**Since Oct 6 the robots run these for you.** Keep this page for emergencies, or when the agent asks you to run one.

**How to run a command:** Windows key → type `PowerShell` → Enter → type `cd C:\Users\User\Documents\saas` → Enter → paste the command → Enter.
Without `--upload` or `--apply`, every tool only shows what it *would* do. Live changes always back up first.

## Useful commands
| Command | Does |
|---|---|
| `python publish_draft.py --post-id <ID> --unpublish --apply` | takes a published post back to draft (undo a publish) |
| `python upload_draft.py --restore backups/<file>.json` | undoes a page replace |
| `python inject_links.py --restore backups/<file>.json` | undoes a link |
| `python media_fix.py --restore backups/<file>.json` | undoes an image fix |
| `python set_robots.py --noindex <IDs> --apply` | hides posts from Google |
| `python cannibal_check.py` | checks new briefs don't compete with live pages (read-only) |
| `python junia_draft.py --export-all` | saves drafts + QA reports (read-only) |
| `python dfs_pull.py --check` | DataForSEO balance (other options cost money) |
| `python -m autopilot.healthcheck` | checks every page loads |

## Known problems and fixes
| Problem | Fix |
|---|---|
| A change doesn't show on the site | purge LiteSpeed **and** Hostinger's cache (hPanel → Websites → Advanced → Cache Manager → Purge All), then LiteSpeed again |
| Uploads fail with login errors | keep the auth-bridge plugin installed |
| Rank Math can't make a redirect | add it to the redirects plugin and re-upload |
| The cloud robot can't send mail directly | it emails through the owner-mail plugin |
| The cloud robot can't read Search Console | it has no Google key; Google numbers come from your PC |
| Junia ignored a pasted brief | fill it field by field |
| Junia publishes publicly by default | Mode = draft every time (the robot checks) |
| Chrome freezes when hidden | keep it visible; taskbar shortcut has fix flags |
| Quora or Junia freezes while typing | the agent inserts the whole text at once |
| No robot tool can open Reddit | you pick the threads (page 10) |
| A draft would compete with a live page | `publish_draft.py` refuses it; the topic is merged or re-angled |
| The agent's safety check blocks an action | it becomes your click, or you add a permission rule; never retried |
