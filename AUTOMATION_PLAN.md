# 🤖 AUTOMATION PLAN: A to Z (2026-10-05)

- **Goal (user, 2026-10-05):** automate the whole ToolPickGuide pipeline, including Junia article creation and Quora, using the user's own Chrome when it is open.
- **Three workers:**
  1. **Cloud robot:** scheduled routines (daily, weekly, monthly). Runs with no computer on. Can't see your browser.
  2. **Browser agent:** a local Claude session on your PC that drives your Chrome through the Claude extension, where you're already logged in to Junia, Quora, Search Console and WordPress. Runs only when the PC and Chrome are on.
  3. **You:** the few steps no agent may do (below).
- **Rule files that still apply:** `CLAUDE.md`, `AUTOPILOT.md` (tiers, caps, kill switch), `CONTENT_STRATEGY.md` (topic gate), `COMMUNITY_MARKETING.md` (posting rules).

---

## 1. The pipeline, step by step

| # | Step | Who | How | Status |
|---|---|---|---|---|
| A | Keyword and topic research | Cloud robot (monthly) | GSC, GA4, Bing, DataForSEO ≤ $5/month → re-ranked content queue in `TASKS.md` | ✅ running |
| B | Briefs with verified facts | Cloud robot (weekly, Mondays) | **4** field-by-field briefs per week (decision D3, 2026-10-05); facts from official pricing pages | ✅ running |
| C | **Article generation in Junia** | **Browser agent** | Opens Junia in your Chrome, fills each field from the brief (keyword, headline, outline, Background/Context, Writing style, settings), generates, saves to WordPress **as a draft** | ✅ built 2026-10-05 (first run: draft 618; local task "tpg-browser-ops", Tue + Fri 10:00) |
| D | QA and correction | Cloud robot (daily, Tier B) | Export, QA gate, judge new link sites, corrected body from the facts sheet, `--replace-content`, copy stock photos to the Media Library | ✅ live since 2026-10-05 |
| E | Image check | none needed for Junia images | Junia's images are generally safe (user 2026-10-05); only broken images (not loading, offensive, unrelated) are flagged | ✅ decided |
| F | **Publish** | **You** (1 minute per article) | Open the draft, Save Draft, read, Publish | Stays with you (decision D1) |
| G | Request indexing | Browser agent | Search Console URL inspection → Request indexing for each newly published URL | 🆕 add to §2 run |
| H | Internal links | Cloud robot (Tier B) + you | `inject_links.py --upload` for normal posts (robot); upgrade-file posts need `--replace-live` (you) | ✅ live / Tier C |
| I | Price watch and page upgrades | Cloud robot finds · you run | Weekly price check → exact edits → `--replace-live` | Tier C |
| J | **Quora answers** | Cloud robot drafts · **browser agent posts after your OK** | Robot finds threads and drafts answers (weekly). Browser agent opens each thread, checks it's still open and not already answered well, adapts the draft, pastes it into the answer box, shows you, and clicks Post only after you say "post" for that answer | 🆕 to build (§3) |
| K | Affiliate programs | Local session + you | Mailbox check for approvals; insert affiliate links into pages; account, password, captcha and tax steps are yours | ongoing |
| L | Reports | Cloud robot | Daily, weekly and monthly Docs with "Message for you" | ✅ running |
| M | Health and speed | Cloud robot | Daily health check; monthly PageSpeed | ✅ running |

---

## 2. Browser agent: Junia and indexing ("TPG Browser Ops")

- **When:** a local scheduled task on your PC, **Tuesday and Friday 10:00** (your time). It runs only if Chrome is open with the Claude extension connected; otherwise it skips and the next daily message says so.
- **Each run:**
  1. `git pull`; check the kill switch `AUTOPILOT_PAUSED`.
  2. **Junia:** for every brief in `knowledge/briefs/junia/` with no draft and no live page (max **2 per run**), fill Junia field by field from the brief's "JUNIA FIELD BY FIELD" section, generate, and send it to WordPress as a **draft**. Never publish.
  3. **Indexing:** list sitemap URLs published since the last run and request indexing for each in Search Console (max 5 per run; Google limits requests per day).
  4. Log every action in `LOOP.md` and the ledger, commit and push. The next morning, the cloud robot QAs and corrects the new drafts.
- **First run together (required):** we do the first Junia article live while you watch, so I learn Junia's real screens and field names. Only after that does the task run on its schedule.
- **Credits:** each Junia article uses your Junia plan's credits. The task stops if Junia asks for an upgrade or a payment, and tells you.

---

## 3. Quora: what can and can't be automated

- **Automated:** finding threads, drafting answers (cloud robot, weekly), opening threads in your Chrome, checking they're still relevant, pasting the adapted answer, and showing it to you.
- **Not automated, ever:** clicking **Post** without your OK. Posting publishes under your name, so it needs your "post" for each answer, every time. A session looks like this: you say "Quora time", I prepare up to 5 answers in tabs, you reply "post 1, 3, 4", I post those three.
- **Account safety:** Quora watches for automated and promotional activity. Keep it to 3–5 answers a week, no links in a first answer, and a disclosure whenever ToolPickGuide is mentioned (`COMMUNITY_MARKETING.md`). Heavy automation risks a ban of your account.
- **Reddit:** same flow, but you pick the threads (Reddit blocks the cloud robot).
- **Tested 2026-10-05:** opening threads and checking them works in Chrome, but Quora's answer editor freezes the page when the agent types a long answer (twice, even with Chrome's occlusion fix). So the agent checks the threads and prepares the text; **the user pastes and posts** from the Quora Doc (about 2 minutes per answer). Answer W1-2 was posted (credential shows "Former Founder" until the user fixes the end date).

---

## 4. What stays with you (and why)

| Item | Why |
|---|---|
| Publishing an article (1 minute each) | Your decision D1. The agent never publishes |
| Each Quora/Reddit post ("post 1, 3") | Public content under your name needs your OK per post |
| `--replace-live`, `media_fix.py --apply`, settings | Changes to live pages; the agent's safety checks block it from running them |
| Accounts, passwords, login codes, captchas, payment and tax forms | The agent never enters or creates these |
| Spending beyond $5/month on DataForSEO | Your decision |

**Your weekly time once this is built:** about 20–30 minutes (publish 2–4 articles, approve Quora answers, run 1–3 commands).

---

## 5. Decisions for you

| # | Question | Recommendation |
|---|---|---|
| D1 | Should the agent publish approved drafts itself? | **No.** Keep the 1-minute publish click: it's your final check that nothing wrong goes live |
| D2 | Should the robot swap a draft's AI-art featured image for a real photo itself (drafts only, Tier B)? | **Yes:** low risk, fully reversible, and it would have caught the 601/603 images before publishing  **User decision 2026-10-05: NO.** The robot only flags AI-art main images; the user runs the swap (`media_fix.py --featured-media`). |
| D3 | Junia runs per week | **2 per run, 2 runs a week (4 articles)**, matching the robot's brief output (raise the robot to 4 briefs a week if yes) **User decision 2026-10-05: YES (4 a week).** |

---

## 6. Build order

1. ✅ Cloud robot live (daily and monthly routines updated 2026-10-05). Weekly routine: you remove the old practice block at claude.ai/code/routines (§7).
2. Connect Chrome: open Chrome with the Claude extension signed in (same Claude account).
3. ✅ First Junia run together (draft 618, 2026-10-05); local scheduled task `tpg-browser-ops` created (Tue + Fri 10:00, runs while the Claude app is open). Steps: `knowledge/junia-runbook.md`; done list: `knowledge/junia-runs.md`.
4. First Quora session together (§3).
5. If you say yes to D2, add the featured-image swap on drafts to Tier B (code + `AUTOPILOT.md`).

## 7. Weekly routine: remove the practice block (2 minutes)

1. Open https://claude.ai/code/routines and click **TPG Weekly Review**.
2. In the instructions, delete the block from `=== SHADOW MODE IS ON (practice week) ===` down to the line of `=====` signs.
3. In step 1, replace "python3 inject_links.py dry run" with "the Tier B draft fixes and inject_links.py --upload for TODO rows, as in Daily Ops".
4. Save.
