# 03 · Robots and who does what (2026-10-19)

**Since Oct 6 everything runs by itself.** You keep only Quora/Reddit and the rare password, captcha, payment or tax step.

## The cloud robot (runs even when your PC is off)
| Routine | When (Israel time) | Job |
|---|---|---|
| Daily Ops | every day 07:00 | health check · fixes and **publishes** clean drafts (since Oct 17, max 4 a day) · live-page updates · links · **Tue + Fri: writes our own test articles** · report + email |
| Weekly Review | Monday 08:00 | + keyword harvest (DataForSEO) · up to 8 article briefs in pairs · price check · Quora drafts · refreshes these summaries |
| Monthly Report | 1st, 09:00 | Google/Bing data · speed · scoreboard · decisions for you |

From Oct 25 (clock change) each runs one hour earlier. You get each report as an **email**, a **Google Doc** (title ends OK / Needs you / ALERT) and **PM Tracker** updates.

## The PC robot "tpg-browser-ops" (every day 20:00)
Uses your Chrome. It uploads our own test articles as drafts with a stock photo (the cloud can't pick photos yet: Pexels paused new keys) · asks Google to index new pages (max 5 a day) · Tue + Fri: has Junia write the week's drafts · Sundays: pulls Search Console + GA4 numbers · backup for publishing and live changes. It needs the PC on, with the Claude app and Chrome open and visible. **It last ran Oct 17.**

## Safety limits
- Max 6 links, 3 draft fixes and 4 publishes a day; only drafts that pass the check and the image check.
- A draft that would compete with a live page is refused (`cannibal_check.py`).
- DataForSEO at most $10 a month ($0.68 used in October so far).
- Every change is backed up, checked, and undone if the check fails.
- Two failed checks in 7 days pause the robot automatically.

## Emergency stop
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
