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
| 7 | **Live mode from 2026-10-05** (user: "it can start making changes on its own"): the practice week is over and the cloud robot runs Tier B itself. Daily and monthly routine prompts updated 2026-10-05; the weekly routine's prompt still carries the old practice block until the user removes it at claude.ai/code/routines (the agent's update was blocked), which is harmless because Monday's Daily Ops run makes the writes |

---

## 2. The four tiers

| Tier | Meaning | Allowed commands (exact) |
|---|---|---|
| **A: autonomous** | Read-only, or writes only inside the repo / Drive / Sheet | `python gsc_pull.py` · `python ga_pull.py` · `python bing_kw_pull.py --targets` · `python dfs_pull.py --check` · `python kp_ingest.py` · `python inject_links.py` (dry run) · `python junia_draft.py --export-all` · `python upload_draft.py <file>` (dry run) · public GETs (sitemap, pages, REST without auth) · writing files in the repo · Drive/Sheets updates |
| **B: autonomous with automatic undo** | Small reversible WordPress writes. Each one is backed up, verified live, and rolled back automatically if verification fails | `python inject_links.py --upload` (rows marked TODO in the roadmap, ≤ 3 links per post, ≤ 6 per day) · `python junia_draft.py --brief <b> --apply` and `--replace-content <f>` (**drafts only**, ≤ 3 drafts per day) · `python dfs_pull.py --volume/--gap/--serp` (only while the month's spend stays ≤ $5) |
| **C: the agent prepares, the user approves** | Ready-to-run, listed in the daily digest under "Waiting for you" | publishing a draft · `upload_draft.py --replace-live` · `set_robots.py --apply` · `retire_post.py --apply` · `media_fix.py --apply` · `update_categories.py --apply` · any price change on a live page · DataForSEO spend above $5/month |
| **D: never (for the cloud autopilot)** | Out of bounds for the scheduled cloud runs | passwords and account creation · posting/voting on Reddit or Quora · permanent deletes · theme, plugin and site settings · payments · sending emails or messages for the user · reading the owner's inbox |

**Site settings (2026-10-03):** performance and SEO plugin settings (LiteSpeed Cache, Rank Math) may be changed by the **local** agent with the user present, one at a time, logged in `wordpress/SETTINGS-LOG.md` and re-tested (rules in `CLAUDE.md`). The cloud autopilot never changes settings. If a daily health check or speed test shows a regression right after a logged change, it raises an ALERT that names the change and its undo.

**Draft QA standard for Tier B (`junia_draft.py`):** the agent may only `--apply` when the QA gate shows no unknown $ amounts, no excluded tools, no links to blocked sites, and no leftovers. Junia inserts internal and external links (user rule 2026-10-06): the robot fixes only the internal ones (`--apply` unlinks internal links that don't point to a live page and adds the brief's required ones); external links are usually fine, but the robot still judges each new domain once in `knowledge/junia-link-domains.txt` and blocks the occasional bad one. `--apply` also copies Junia's stock photos into the Media Library (part of the same draft fix, user decision 2026-10-05). Otherwise it prepares a corrected version and lists it as Tier C.

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
   - A draft that fails the gate gets a QA-corrected body (`knowledge/junia-<ID>-<slug>.md`) that keeps Junia's writing and fixes every gate item from the brief's facts sheet. Once that file passes the gate offline, the robot runs `--replace-content` on it itself (Tier B, counts toward the 3-draft cap). It never `--apply`s a failing draft without a corrected body.
   - A draft that passes is a "Waiting for you" item: open it, Save Draft, read, Publish (publishing stays Tier C).
   - A brief with no draft is **not** a "Waiting for you" item when its slug is already live in the sitemap, or when the `TASKS.md` Content queue schedules it later. Mention it only once its week arrives.
5. **Links:** `python inject_links.py`. If the dry run is clean, `--upload` within the caps, then verify live.
6. **Ledger + log:** update `autopilot/ledger.json`; append one line per action to `LOOP.md` with its undo command.
7. **Digest:** create the Google Doc `Daily Digest YYYY-MM-DD` in Drive › ToolPickGuide OS › Reports, using sections Done · Waiting for you (Tier C, with exact commands/clicks) · Alerts · Numbers. Update the Sheet rows that changed status.
8. `git add autopilot data reports LOOP.md ONSITE_PLANS.md && git commit && git push`.

### 5.2 Weekly Review (Monday)
1. Everything in Daily Ops, plus:
2. **Content queue:** write the next 4 Junia briefs (decision D3, 2026-10-05). If the `TASKS.md` Content queue has fewer than 8 items without a brief, add new candidates at its end from the newest `data/` insight files (each one must pass the `CONTENT_STRATEGY.md` topic gate and the sitemap check; note the evidence) from `TASKS.md` §Content queue (sitemap check + topic gate + facts verified on official pages that week). Every brief has the "JUNIA FIELD BY FIELD" section (keyword, headline, exact outline, Background/Context box with the facts sheet, Writing style box, settings) and the Required tools / Excluded tools / Price-heavy rows, like `knowledge/briefs/junia/honeybook-pricing.md`: Junia ignores one big paste (drafts 601/603). **No FAQ section in the brief's outline** (user decision 2026-10-06: Junia's own FAQ setting is ON and writes it); the Background box tells Junia that FAQ answers may use only numbers from the facts sheet.
3. **Price watch:** re-check the pricing pages behind every live BOFU page's facts. Any change becomes a Tier C item with the exact edit.
4. **Community queue:** find 5–6 candidate Quora threads per `COMMUNITY_MARKETING.md` §5 and write them into its §8 queue as `W<week>-<n>` rows with Status **Ready**, the full drafts in `knowledge/community-week<N>-drafts.md`, and one PM Tracker row each (`Community <ID> (Quora): <title>`, owner User, Status Open). No posting. Reddit: the weekly message includes a "Reddit picks" block with the 3 search links from §10 of that file and the two-step instruction (pick 1–2 threads, add a `Reddit pick` row to the PM Tracker).
5. **Copies for the owner's phone:** every new brief and the week's community queue + full draft answers go to Drive › Plans & Briefs as Google Docs (§6.2).
6. **Weekly report** Google Doc in Drive › Reports: KPIs vs `GROWTH_PLAN.md` targets, wins, problems, next week. Links to the §6.2 Docs.
7. **Refresh the owner summaries (user decisions 2026-10-05):** the summary is at most **10 topic pages, each one A4 page max** (`summary/01`–`10`), plus two child-simple picture pages (`summary/00-project-map.html`, `summary/11-agent-team.html`). Re-read the sources behind them (CLAUDE.md, AUTOPILOT.md, TASKS.md, LOOP.md since last Monday, affiliate-applications.md, ONSITE_PLANS.md, the live sitemap, etc.) and update every fact that changed: page list and IDs, affiliate statuses and links, open tasks, decisions, numbers, dates. Plain English, no secrets ever; keep each page to one page by cutting older detail, never by adding pages. For each changed file follow `autopilot/summary-drive-docs.md`: new Doc in Drive › Summary, the old Doc moved to Summary › Old versions (never trashed), new ID in the register. The weekly message lists which summaries changed (or "summaries unchanged"), and says "pictures need re-render" if 00 or 11 changed.

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
| **Daily message** | top of the Daily Digest Doc ("Message for you") + the run's final answer (§6.1) | every Daily Ops run |
| **Weekly message** | top of the Weekly Report Doc | Mondays (replaces that day's daily message) |
| **Monthly message** | top of the Monthly Report Doc | 1st of month (in addition to the daily message) |

### 6.1 Daily message protocol (user decision 2026-10-04: messages, no email)

**Channel:** no email. Each routine run leaves one message for the owner in two places:
1. **The first section of its Google Doc**, under the heading "Message for you". The Doc title carries the status, so the owner can see it in the Drive file list without opening anything: `Daily Digest YYYY-MM-DD · OK | Needs you | ALERT`, `Weekly Report YYYY-MM-DD · …`, `Monthly Report YYYY-MM · …`.
2. **The run's final answer**, the same message word for word, which the owner can read at claude.ai/code → Routines.

**Email copy (user decision 2026-10-05, replaces "no email"):** after creating the Doc, the run emails the same message to the owner only: write it to a text file and run `python3 -m autopilot.notify_owner --subject "<Doc title>" --file <file> --doc <Doc URL>` (recipient fixed to cezaris.joe@gmail.com; sender eran@toolpickguide.com). If it fails, say so in the Doc and carry on.

**Hard limits:** no other email, chat or outside messages, and never any passwords, keys or tokens in a message. Write in plain words for a non-technical owner. Name PowerShell explicitly for any command, and give exact clicks for any website step.

**Daily message (≤ 250 words), sections in this order:**
1. **Status:** one line. OK (nothing needs you), Needs you (tasks waiting), or ALERT (something broke).
2. **ALERTS** (only if any): what happened, what the robot already did (for example "restored post 404"), and what the owner should do.
3. **Today for you:** at most 3 tasks, most important first, taken from the PM Tracker / `TASKS.md` (overdue first, then due within 3 days, then waiting Tier C items). Each one: task ID, one-line why, the exact command or clicks, and about how many minutes it takes.
4. **Today for the robot:** what it did in this run (each write with its undo command) and what it plans for the next run.
5. **Numbers:** one line: pages up/total · links and drafts done today vs caps · DataForSEO spend this month vs $5 · days until the next milestone in `GROWTH_PLAN.md` §5.
6. **Good to know** (optional, max 3 bullets): only useful news, such as a new brief ready, a price change found, a page that moved into the top 50/20/10, a new Search Console query, or a deadline in the next 7 days.
7. **Links:** the PM Tracker sheet, and the previous Daily Digest Doc if anything in it is still open.
8. **Community today** (user rule 2026-10-06; not counted in the 250 words): the owner must never need another file to do a community task. Take at most 2 rows of `COMMUNITY_MARKETING.md` §8 with Status **Ready** (oldest first). Never list a row that is Posted or Skipped, and first copy any PM Tracker "Community …" row the owner set to Done into §8 as "Posted <date>". If none are Ready, write one line: "No community task today." For each item write, in this order:
   - **ID, platform and community**, the thread's title, and its full link.
   - **Why this one:** one line.
   - **The answer, word for word**, between the lines `----- copy from here -----` and `----- copy to here -----` (the full draft from `knowledge/community-week<N>-drafts.md`; no "see file").
   - **Steps:** Quora: 1. Open the link (signed in to Quora). 2. Read the answers already there; if one already says the same thing, skip it and set its PM Tracker row to Skipped. 3. Click **Answer** under the question. 4. Paste the text. 5. Click **Post**. 6. In the PM Tracker, set the row "Community <ID>" to **Done**. Reddit: the same, but in step 3 click the **"Add a comment"** box under the post and in step 5 click **Comment** (`COMMUNITY_MARKETING.md` §10).
   - (The agent can't fill in or post answers for you: the safety check blocks typing into Quora, and no agent tool can open Reddit, tested 2026-10-06.)
   - **Reddit picks:** before choosing items, turn every PM Tracker row with Task `Reddit pick` that has no draft yet into a draft: read the pasted question text, write the answer (`COMMUNITY_MARKETING.md` §3/§7 rules) as `R<week>-<n>` in `knowledge/community-week<N>-drafts.md`, add a §8 row with Status Ready, and rename the PM Tracker row to `Community R<week>-<n> (Reddit): <title>`.

**Weekly message (Mondays, ≤ 450 words)** has the daily sections plus:
- **KPIs vs targets** (`GROWTH_PLAN.md` §2), as a small table with an arrow per row.
- **Done last week:** the robot's work and the owner's work.
- **This week's plan:** the owner's tasks by day and the robot's tasks.
- **Ready for you:** new Junia briefs (titles + files), the community queue (number of threads), and price changes.

**Monthly message (1st, ≤ 600 words)** has:
- the scoreboard row for the month vs targets
- earnings (or "user to fill")
- top 3 wins and top 3 problems
- recommendations
- decisions needed from the owner (each with a recommended answer)
- next month's plan

**Paused or shadow mode:** a paused run still leaves a one-line daily message ("Robot paused: <reason>. To resume: delete AUTOPILOT_PAUSED in GitHub."). Shadow (practice) mode ended on 2026-10-05; if it is ever switched back on, every daily message says "Practice mode: nothing was changed on the website".

### 6.2 Copies of briefs and community drafts (user decision 2026-10-05)

- **Where:** Drive › ToolPickGuide OS › Plans & Briefs (`1uBQANu4CHTtmQfDL9ttHZdSbTMF5zGuw`), as Google Docs (upload HTML).
- **What, every Monday:** one Doc per new Junia brief with only its "JUNIA FIELD BY FIELD" section (`Junia fields: <topic> (YYYY-MM-DD)`) and one Doc with the week's §8 queue rows plus the full draft answers (`Quora queue + draft answers (week N, YYYY-MM-DD)`).
- **Format:** the "PASTE INTO JUNIA" box stays one block so it copies cleanly. Each Doc starts with "Snapshot from the toolpickguide-os repo, <date>. The repo file stays the working source."
- **Links:** the weekly message links each task that uses a brief or draft to its Doc.
- **Never uploaded:** secrets, `.env` values, backups, scripts.
- **First copies (local agent, 2026-10-05):** HoneyBook pricing brief, Best CRM for marketing agencies brief, Quora week 1 queue + drafts.
