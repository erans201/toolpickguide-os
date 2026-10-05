# 07 · Commands and known fixes

**How to run a command:** Windows key → type `PowerShell` → Enter → type `cd C:\Users\User\Documents\saas` → Enter → paste the command → Enter.
Without `--upload` or `--apply`, every tool only shows what it *would* do. Live changes always back up first.

## Commands you may be asked to run
| Command | Does |
|---|---|
| `python upload_draft.py <upgrade file> --upload --replace-live <ID> --force-replace` | replaces a live page's text |
| `python upload_draft.py --restore backups/<file>.json` | undoes that |
| `python inject_links.py --only IL-9a --upload` | adds one roadmap link |
| `python media_fix.py --post-id <ID> ... --apply` | image fixes |
| `python set_robots.py --noindex <IDs> --apply` | hides posts from Google |
| `python junia_draft.py --export-all` | saves Junia drafts + QA reports (read-only) |
| `python dfs_pull.py --check` | DataForSEO balance (other options cost money) |
| `python -m autopilot.healthcheck` | checks every page loads |

## Known problems and fixes
| Problem | Fix |
|---|---|
| A change doesn't show on the site | purge LiteSpeed **and** Hostinger's cache (hPanel → Websites → Advanced → Cache Manager → Purge All), then LiteSpeed again |
| Uploads fail with login errors | keep the auth-bridge plugin installed |
| Rank Math can't make a redirect | add it to the redirects plugin and re-upload |
| The cloud robot can't send mail directly | it emails through the owner-mail plugin |
| Junia ignored a pasted brief | fill it field by field |
| Junia publishes publicly by default | set Mode = draft every time |
| Chrome freezes when hidden | keep it visible; taskbar shortcut has fix flags |
| Quora or Junia freezes while typing | the agent inserts the whole text at once |
| The agent's safety check blocks an action | it becomes your click; never retried |
