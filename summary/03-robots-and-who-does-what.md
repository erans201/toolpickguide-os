# 03 · Robots and who does what (2026-10-12)

**Since Oct 6 everything runs by itself.** You keep only Quora/Reddit and the rare password, captcha, payment or tax step.

## The cloud robot (runs even when your PC is off)
| Routine | When (Israel time) | Job |
|---|---|---|
| Daily Ops | every day 07:00 | health check · fixes new drafts · adds internal and affiliate links · **Tue + Fri: writes our own test articles** · report + email |
| Weekly Review | Monday 08:00 | + 8 article briefs in 4 pairs · price check · Quora drafts · refreshes these summaries |
| Monthly Report | 1st, 09:00 | Google/Bing data · speed · scoreboard · decisions for you |

From Oct 25 (clock change) each runs one hour earlier. The daily routine uses the newest model (Opus 5.5, since Oct 9). You get each report as an **email**, a **Google Doc** (title ends OK / Needs you / ALERT) and **PM Tracker** updates.

## The PC robot "tpg-browser-ops" (every day 20:00)
Uses your Chrome. In order: makes queued live-page changes (max 3 a day) · uploads our own test articles as drafts with a stock photo · **publishes drafts that passed the check** (max 2 a day; 4 during the test) · asks Google to index new pages (max 5 a day) · Tue + Fri: has Junia write the week's drafts · pulls Clarity numbers once you set it up. It needs the PC on, with the Claude app and Chrome open and visible.

## Safety limits
- Max 6 links and 3 draft fixes a day. The cloud robot never publishes; only the PC robot does, and only clean drafts.
- A draft that would compete with a live page is refused (`cannibal_check.py`).
- DataForSEO at most $5 a month.
- Every change is backed up, checked, and undone if the check fails.
- Two failed checks in 7 days pause the robot automatically.

## 🛑 Emergency stop
GitHub repo → **Add file → Create new file** → name `AUTOPILOT_PAUSED` → **Commit changes**. Delete that file to restart.

## Who does what
| Robots and agents | Only you (~15 min a week) |
|---|---|
| research, briefs, half the articles | Quora: paste and click **Post** |
| Junia drafts, QA and fixes | Reddit: pick 1–2 threads, post the reply |
| publishing, indexing, links | passwords, captchas, payment, tax |
| live-page updates (backup first) | one-time setups (Clarity, page 09) |
| affiliate forms **and replies** | yes/no on big decisions |
| reports and emails to you | |

The agent may change LiteSpeed and Rank Math settings only with you present: one at a time, after your OK, logged with the undo.
