# 🤖 03 · The robots and their schedule

There are three workers: the **cloud robot** (runs with your PC off), the **browser agent** (runs on your PC in your Chrome), and **you**.

## Cloud robot: 3 routines (claude.ai/code/routines, environment "robot")

| Routine | When (your time, Berlin) | What it does |
|---|---|---|
| **TPG Daily Ops** | every day 07:00 (06:00 after Oct 25) | site health check · checks new Junia drafts against their facts sheet and fixes them (drafts only) · adds internal links · writes the Daily Digest · emails you |
| **TPG Weekly Review** | Mondays 08:00 | the daily work, plus 4 new Junia briefs · price check of every live comparison page · 5–6 Quora/Reddit thread ideas with draft answers · weekly report |
| **TPG Monthly Report** | 1st of the month 09:00 | Search Console, GA4, Bing and DataForSEO data (≤ $5) · speed test · scoreboard vs targets · recommendations · decisions for you |

**Where you see the results:**
1. **Email** to cezaris.joe@gmail.com from eran@toolpickguide.com (since 2026-10-05). The cloud can't send mail directly, so it sends through the website plugin `toolpickguide-owner-mail.php`.
2. A **Google Doc** in Drive › ToolPickGuide OS › Reports. The title ends with **OK**, **Needs you** or **ALERT**.
3. The **PM Tracker** sheet rows it updates.

**Safety limits written into the code:**
- At most 6 internal links and 3 draft fixes a day; 0 publishes.
- DataForSEO at most $5 a month.
- Every website change is backed up, checked live, and undone automatically if the check fails.
- Two failed checks in 7 days pause the robot by themselves.

---

## 🛑 Emergency stop (kill switch)
1. Open https://github.com/erans201/toolpickguide-os
2. Click **Add file → Create new file**.
3. Name it `AUTOPILOT_PAUSED`, type the reason in the box, click **Commit changes**.
4. To restart: open that file on GitHub, click the **…** menu → **Delete file** → **Commit changes**.

---

## Browser agent (your PC): "tpg-browser-ops"
- **When:** Tuesday and Friday 10:00, only while your PC is on, the Claude app is open, and Chrome is open with the Claude extension.
- **What:** writes up to 2 Junia articles per run from the robot's briefs and saves them to WordPress **as drafts** (never published). Then asks Google to index pages that were newly published (max 5 per run).
- **Its notebooks:** `knowledge/junia-runbook.md` (exact clicks), `knowledge/junia-runs.md` (articles done), `knowledge/indexing-requests.md` (pages sent to Google).
- **Chrome tip:** keep Chrome visible (not minimized). Your taskbar shortcut has flags that keep it drawing in the background.

---

## How a normal week flows
- **Mon:** the robot writes 4 briefs and a Quora queue.
- **Tue + Fri:** the browser agent turns 2 briefs each into Junia drafts.
- **Next morning:** the daily robot checks and fixes each draft.
- **You:** open the draft, click Save Draft, read it, click Publish (about 1 minute).
- **Next browser run:** the agent requests Google indexing for the new page.
