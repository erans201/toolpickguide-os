# ⌨️ 09 · Commands cheat sheet

**How to run any command:**
1. Press the **Windows key**, type `PowerShell`, press **Enter**.
2. Type `cd C:\Users\User\Documents\saas` and press **Enter**.
3. Paste the command and press **Enter**. Copy the output back to the agent if it asks.

Every tool below does a **dry run** (shows what it would do, changes nothing) unless you add `--upload` or `--apply`. Live changes always make a backup first.

## The ones you'll actually use

| Command | What it does |
|---|---|
| `python upload_draft.py knowledge/upgrade-<ID>-<slug>.md --upload --replace-live <ID> --force-replace` | replaces a live page's text with its upgrade file (backup first) |
| `python upload_draft.py --restore backups/<file>.json` | undoes a replace |
| `python inject_links.py --upload` | adds the TODO links from the link roadmap (e.g. `--only IL-9a`) |
| `python media_fix.py --post-id <ID> ... --apply` | image fixes (swap featured image, re-host, alt text) |
| `python junia_draft.py --export-all` | saves all Junia drafts + QA reports to `knowledge/_preview/` (read-only) |
| `python junia_draft.py --brief <brief> --post-id <ID> --replace-content <file>` | puts a corrected text into a Junia draft (stays a draft) |
| `python set_robots.py --noindex IDS --apply` | hides posts from Google (`--noindex-pages` for pages) |
| `python retire_post.py --post-id <ID> --redirect-to <path> --redirect-already-set --apply` | retires a duplicate: verifies the 301, then Trash |
| `python update_categories.py --apply` | updates category pages |

## Data pulls (read-only)
| Command | Output |
|---|---|
| `python gsc_pull.py` | Search Console queries/pages → `data/gsc-*` |
| `python ga_pull.py --property 551985779` | GA4 visitors → `data/ga-*` |
| `python bing_kw_pull.py --targets` | Bing keyword volumes (free) |
| `python dfs_pull.py --check` | DataForSEO balance (free). `--volume`, `--gap`, `--serp` **cost money** |
| `python pagespeed_pull.py` | mobile speed for the top 20 pages |

## Robot and mail tools
| Command | What it does |
|---|---|
| `python -m autopilot.healthcheck` | checks every sitemap page loads and robots tags are unchanged |
| `python -m autopilot.guard` | today's caps, DataForSEO spend, strikes |
| `python -m autopilot.notify_owner --subject "..." --file msg.txt` | emails you (fixed recipient) |
| `python mail_tool.py --inbox` | shows affiliate replies only (agent uses it) |
| `python -m unittest discover -s tests` | runs the safety tests (21 pass) |

## Never run these yourself unless the agent gives you the exact line
`auto_scheduler.py` (old Windows scheduler for READY FOR UPLOAD files), `kp_pull.py` (Google Ads: suspended), `make_cloud_env.py`, `make_cloud_key.py`.
