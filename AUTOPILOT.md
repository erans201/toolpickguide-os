# 🤖 AUTOPILOT: Autonomous Operations Policy

- **Status:** APPROVED in principle 2026-10-03 (user decisions below). Goes live after setup tasks T0.1–T0.9 in `TASKS.md`.
- **Runs in:** Anthropic cloud (Claude Code routines) against the private GitHub repo `toolpickguide-os`. Every run starts with zero memory, reads this file, does its job, then commits its log and reports back to the repo.
- **Priority:** for a scheduled cloud run, this file decides what may happen without the user. Anything not explicitly allowed here falls back to the normal rules in `CLAUDE.md` (the user runs it).

---

## 1. User decisions (2026-10-03)

| # | Decision |
|---|---|
| 1 | Tier B approved: internal links + QA fixes on Junia **drafts**, with backup, live verification and automatic undo |
| 2 | Publishing stays **Tier C** (the user approves every publish) |
| 3 | DataForSEO spend without asking: **≤ $5 per calendar month** |
| 4 | Reports go to Google Drive (Docs) and the Google Sheet tracker |
| 5 | Runtime: cloud agent on a private GitHub repo |
| 6 | Reddit/Quora runs in a separate, dedicated chat session (never posted by the agent) |

---

## 2. The four tiers

| Tier | Meaning | Allowed commands (exact) |
|---|---|---|
| **A: autonomous** | Read-only, or writes only inside the repo / Drive / Sheet | `python gsc_pull.py` · `python ga_pull.py` · `python bing_kw_pull.py --targets` · `python dfs_pull.py --check` · `python kp_ingest.py` · `python inject_links.py` (dry run) · `python junia_draft.py --export-all` · `python upload_draft.py <file>` (dry run) · public GETs (sitemap, pages, REST without auth) · writing files in the repo · Drive/Sheets updates |
| **B: autonomous with automatic undo** | Small reversible WordPress writes. Each one is backed up, verified live, and rolled back automatically if verification fails | `python inject_links.py --upload` (rows marked TODO in the roadmap, ≤ 3 links per post, ≤ 6 per day) · `python junia_draft.py --brief <b> --apply` and `--replace-content <f>` (**drafts only**, ≤ 3 drafts per day) · `python dfs_pull.py --volume/--gap/--serp` (only while the month's spend stays ≤ $5) |
| **C: the agent prepares, the user approves** | Ready-to-run, listed in the daily digest under "Waiting for you" | publishing a draft · `upload_draft.py --replace-live` · `set_robots.py --apply` · `retire_post.py --apply` · `media_fix.py --apply` · `update_categories.py --apply` · any price change on a live page · DataForSEO spend above $5/month |
| **D: never** | Out of bounds for any agent | passwords and account creation · posting/voting on Reddit or Quora · permanent deletes · theme, plugin and site settings · payments · sending emails or messages for the user |

**Draft QA standard for Tier B (`junia_draft.py`):** the agent may only `--apply` when the QA gate shows no unknown $ amounts, no excluded tools, no off-brief links and no leftovers. Otherwise it prepares a corrected version and lists it as Tier C.

---

## 3. Safety rails (enforced in code and by the run prompt)

1. **Kill switch:** if the file `AUTOPILOT_PAUSED` exists in the repo root, the run writes one line ("paused") to the log and stops. Create it from GitHub's web UI (Add file → Create new file → name `AUTOPILOT_PAUSED` → Commit) to stop everything instantly.
2. **Daily caps:** 6 contextual links, 3 draft updates, 0 publishes. Counted in `autopilot/ledger.json` (committed every run).
3. **Monthly budget:** DataForSEO ≤ $5.00 per calendar month, tracked in `autopilot/ledger.json` from the cost each run reports.
4. **Verify or undo:** after every Tier B write, re-fetch the page or draft. If the change isn't there, or the status/slug changed, restore from the backup at once and raise an alert.
5. **Two strikes:** two failed verifications in 7 days pause Tier B automatically (the agent creates `AUTOPILOT_PAUSED` with the reason) until the user removes it.
6. **No secrets in output:** passwords live only in the cloud environment's variables. They're never printed, committed, or written to Drive.
7. **Git hygiene:** the agent commits only its own files (`autopilot/`, `data/`, `reports/`, roadmap status cells, `LOOP.md`). It never force-pushes and never rewrites history.

---

## 4. Schedule (cron in UTC; Berlin is UTC+2 until 2026-10-25, then UTC+1)

| Routine | Cron (UTC) | Berlin time | Job |
|---|---|---|---|
| **TPG Daily Ops** | `0 5 * * *` | 07:00 (06:00 from Oct 25) | §5.1 |
| **TPG Weekly Review** | `0 6 * * 1` | Mon 08:00 (07:00 from Oct 25) | §5.2 |
| **TPG Monthly Report** | `0 7 1 * *` | 1st, 09:00 (08:00 from Oct 25) | §5.3 |

Model: `claude-sonnet-5-5` for Daily Ops; `claude-opus-5-5` for Weekly and Monthly (strategy and brief writing).

---

## 5. What each routine does (exact)

### 5.1 Daily Ops
1. `git pull`. If `AUTOPILOT_PAUSED` exists, log "paused" and stop.
2. **Health check:** `python -m autopilot.healthcheck` (exit 1 = ALERT). HTTP 200 for `/`, `sitemap_index.xml` and every URL in the sitemap. Robots tag unchanged versus `autopilot/baseline-robots.json`. Sitemap URL count unchanged versus yesterday (± explained by publishes). After a planned publish or noindex, the agent refreshes the baseline with `--init-baseline` and says so in the digest.
3. **Verify yesterday:** every Tier B action in `autopilot/ledger.json` from the last 24 h is still live and correct. `python -m autopilot.guard` prints today's counts, the month's DataForSEO spend and strikes for the digest's Numbers section.
4. **Drafts:** `python junia_draft.py --export-all`. Apply Tier B fixes to drafts that pass the gate; prepare corrected versions for the rest (listed as Tier C).
   - A draft that already has a QA-corrected body (`knowledge/junia-<ID>-*.md`) is never `--apply`'d alone: it waits for the user's `--replace-content` command in `TASKS.md` (T1.1). Repeat that command under "Waiting for you".
   - A brief with no draft is **not** a "Waiting for you" item when its slug is already live in the sitemap, or when the `TASKS.md` Content queue schedules it later. Mention it only once its week arrives.
5. **Links:** `python inject_links.py`. If the dry run is clean, `--upload` within the caps, then verify live.
6. **Ledger + log:** update `autopilot/ledger.json`; append one line per action to `LOOP.md` with its undo command.
7. **Digest:** create the Google Doc `Daily Digest YYYY-MM-DD` in Drive › ToolPickGuide OS › Reports, using sections Done · Waiting for you (Tier C, with exact commands/clicks) · Alerts · Numbers. Update the Sheet rows that changed status.
8. `git add autopilot data reports LOOP.md ONSITE_PLANS.md && git commit && git push`.

### 5.2 Weekly Review (Monday)
1. Everything in Daily Ops, plus:
2. **Content queue:** write the next 2 Junia briefs from `TASKS.md` §Content queue (sitemap check + topic gate + facts verified on official pages that week).
3. **Price watch:** re-check the pricing pages behind every live BOFU page's facts. Any change becomes a Tier C item with the exact edit.
4. **Community queue:** find 5–6 candidate threads per `COMMUNITY_MARKETING.md` §5 and write them into its §8 queue (no posting).
5. **Weekly report** Google Doc in Drive › Reports: KPIs vs `GROWTH_PLAN.md` targets, wins, problems, next week.

### 5.3 Monthly Report (1st of month)
1. `python gsc_pull.py`, `python ga_pull.py --property 551985779`, `python bing_kw_pull.py --targets`.
2. DataForSEO: `python dfs_pull.py --volume` + `--serp --top 15` (about 16 requests, ≈ $0.20) if the month's budget allows.
3. Update the KPI tab in the Sheet and `GROWTH_PLAN.md` §6 scoreboard.
4. Monthly report Google Doc + recommendations: re-rank the content queue, flag pages to refresh, propose roadmap rows (IL-…).
5. Quarterly (Jan/Apr/Jul/Oct): run the `CONTENT_STRATEGY.md` §1 process and list decisions for the user.

---

## 6. Reporting contract

| What | Where | When |
|---|---|---|
| Action log (one line per action + undo) | `LOOP.md` + `autopilot/ledger.json` | every run |
| Daily Digest | Drive › ToolPickGuide OS › Reports (Google Doc) | daily |
| Weekly Report | same folder | Mondays |
| Monthly Report + KPI update | same folder + Sheet tab `KPIs` | 1st of month |
| Alerts (site down, failed verification, budget reached, paused) | top of the Daily Digest, titled "ALERT …" | immediately (next run) |
