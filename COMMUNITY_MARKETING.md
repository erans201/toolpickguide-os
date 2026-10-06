# 💬 COMMUNITY MARKETING: Reddit & Quora (Authority Bridge)

- **Owner:** Reddit/Quora Marketing Agent (plans, finds threads, drafts replies) · **User** (posts from their own accounts) · QA (checks every draft)
- **Status:** ACTIVE plan for October 2026 · created 2026-10-02 (formalizes the framework delivered in chat on 2026-09-29)
- **Hard rule:** the agent **never posts, votes, creates accounts, or messages anyone**. "Autonomous" here means the agent prepares a ready-to-post queue every week; the user reviews and posts.

---

## 1. Why this channel, now (data)

- Google AI Overviews appeared on 13 of our 15 biggest target searches, and ToolPickGuide is cited on **0**. The most-cited sources are YouTube (11×) and Reddit, and **Reddit ranks #2–3 on most commercial SERPs** we checked (`data/dfs-insights-2026-10-01.md`).
- The brand worksheet already found buyers distrust listicles and add "reddit" to their searches. Being genuinely useful *where they ask* is both a traffic source and a trust signal for AI answers.
- GA4 currently shows 0 visits from Reddit or Quora (`data/ga-insights-2026-10-01.md`), so we start from a clean baseline.

---

## 2. The Authority Bridge method

1. **Listen:** find a real question from our ICP (a lawyer, agent, photographer, coach or accountant choosing or fixing software).
2. **Help in full, in the reply itself.** The answer must be complete without clicking anything: the decision, the reasoning, a practical next step.
3. **Bridge, only when it adds something:** at most one link, to the single page that goes deeper on *that exact question*, with a plain disclosure ("I run ToolPickGuide"). Often the right bridge is no link at all.
4. **Measure:** referral sessions from reddit.com / quora.com in GA4 (`ga_pull.py`, sources report), monthly.

**The 80/20 rule:** at least 4 of every 5 replies carry **no link**. Accounts that only drop links get banned, and that damages the brand for good.

---

## 3. Ground rules (QA checks every draft against these)

- **Disclose every time** you mention or link ToolPickGuide. Never pose as a customer or a neutral bystander.
- **Read each community's rules first.** Many subreddits ban or limit self-promotion, and some are profession-only. If links aren't allowed, help without one.
- **One account, your own.** No alt accounts, no asking anyone to upvote, no copy-paste of the same reply across threads.
- **No "tested" or "hands-on"** claims, no invented numbers. Prices only from our verified facts sheets, with "as of [month]".
- **No legal, tax or financial advice.** Talk about software and workflow; point to "check with your bar / CPA / broker" where it matters.
- **Voice:** `brand-voice-sample.md`: short paragraphs, direct, peer-to-peer, analogies. Banned: delve, testament, furthermore, in conclusion, unlock, game-changer, seamless.

---

## 4. Where to show up (priority order matches VERTICAL_MATRIX, approved 2026-10-02)

| Priority | Vertical | Reddit (check rules before the first post) | Quora topics / question types | Bridge page (only if it truly fits) |
|---|---|---|---|---|
| 1 | ⚖️ Legal | r/LawFirm · r/smallbusiness (legal-ops threads) · profession-only subs: read-only unless you qualify | "Best practice management software for a small law firm?", "Clio vs MyCase?" | `/best-legal-case-management-software/` · `/legal-practice-management-software/` · `/best-crm-for-law-firms/` |
| 2 | 🏠 Real estate | r/realtors · r/RealEstateTechnology | "Best CRM for real estate agents?", "How do agents track deals contract to close?" | `/best-client-management-software-real-estate/` · transaction management page (after it's published) |
| 3 | 📸 Photographers | r/WeddingPhotography · r/photobusiness | "HoneyBook vs Dubsado?", "What should a photography contract include?" | `/client-management-software-for-photographers/` · contract template (after publish) |
| — | Cross-vertical | r/smallbusiness · r/Entrepreneur | "What should a client intake form ask?" | intake form template (after publish) |

Accounting and coaching are maintain-only this quarter: answer when a great thread appears, but don't hunt for them.

---

## 5. October 2026 deployment plan

| Week | Agent prepares (in §8 queue) | User does | Target |
|---|---|---|---|
| 1 (Oct 5–11) | Rules summary for each community above; 5 candidate threads, 5 drafts, **no links** | Set up profiles (bio: "I write software comparisons at ToolPickGuide"), read rules, post 3–5 no-link replies | Account history that's genuinely helpful |
| 2 (Oct 12–18) | 6 threads + drafts (legal-heavy); at most 1 with a link | Post 4–6 | 1 disclosed bridge |
| 3 (Oct 19–25) | 6 threads + drafts (real estate + photographers) | Post 4–6 | 1–2 disclosed bridges |
| 4 (Oct 26–Nov 1) | 6 threads + drafts; monthly report from GA4 referrals | Post 4–6; run `python ga_pull.py --property 551985779` on Nov 1 | Review what got replies and upvotes; adjust angles |

**How the agent finds threads (read-only):** Google searches like `site:reddit.com "clio vs mycase"`, `site:reddit.com best crm for realtors`, `site:quora.com legal practice management software`. Prefer threads under ~30 days old with real back-and-forth. Skip threads where the answer is already complete.

**Monthly cap:** about 20 replies total, at most 4 with a link. Quality over volume.

---

## 6. Response templates (adapt every time: never paste verbatim)

### Template 1: Legal case management debate
*Thread type: "3-attorney firm, choosing between Clio and MyCase. Which one and why?"*

> Honestly, both will run a small firm fine. The better question is what breaks first in *your* week.
>
> If it's intake and integrations, meaning you already use a bunch of tools and want them talking to each other, Clio tends to win. Its app ecosystem is the big draw.
>
> If it's adoption, meaning you need your paralegal and your least techy partner using it by Friday, MyCase usually gets there faster. The client portal is simple, and clients actually use it.
>
> Two things to do in either demo: make them walk through your real trust workflow (deposit → invoice → transfer → reconcile), and ask how you'd export everything if you ever leave. Those two answers tell you more than the feature list.
>
> Pricing changes a lot. As of October 2026, Clio's entry plan starts at $49/user/month and MyCase Basic at $50 billed yearly, but check their pricing pages. And run the trust-accounting side past your bar's rules, not just the vendor.
>
> (Disclosure: I write legal software comparisons at ToolPickGuide. I can link the side-by-side if it helps, but the demo test above matters more than which logo you pick.)

**Bridge, if allowed:** `/best-legal-case-management-software/`

### Template 2: Real estate workflow / CRM bottleneck
*Thread type: "My CRM is great for leads, but deals still fall apart between contract and close. What am I missing?"*

> You're probably asking your CRM to do a job it wasn't built for.
>
> A CRM is great at the *before* (leads, follow-up, nurture) and the *after* (past-client touches). The messy middle, from contract to keys, is transaction management: deadlines tied to the contract date, documents, signatures, and the broker's compliance file.
>
> The fix that works for most agents: keep the CRM for people, and run each deal from one checklist that keys every task off the contract date. Inspection, appraisal, financing, closing. When the date moves, the whole checklist moves.
>
> On tools: a lot of agents pair their CRM with something like Dotloop, which is free for your first 10 transactions. Others want it all in one place and use a CRM that includes transaction management. Wise Agent does both from $49/month as of October 2026. If you have a TC, ask what they already use. Don't make them switch for your sake.
>
> (Disclosure: I run ToolPickGuide and compared these tools in more depth. No link needed, though. The contract-date checklist is 80% of the fix.)

**Bridge, if allowed:** `/best-client-management-software-real-estate/` now; the transaction management page once it's published.

### Earlier templates (2026-09-29, kept for maintain-only verticals)
- **Accounting:** "Clients won't use our portal. Is TaxDome worth it?" Angle: the launch is usually the problem, not the portal; choose by bottleneck (documents → TaxDome; team email chaos → Karbon). Disclosed, link optional.
- **Coaching:** "Calendly + Stripe + Google Docs is a mess. Switch to Dubsado?" Angle: packages vs custom proposals; chain contract → payment → intake → welcome; export data quarterly. Disclosed, no link.

---

## 7. QA checklist (before any reply is posted)

- [ ] Answers the question completely without a click
- [ ] Disclosure present if ToolPickGuide is mentioned or linked
- [ ] ≤ 1 link, and only to the page that matches the question; community rules allow it
- [ ] Every price is from a verified facts sheet, with "as of [month]"
- [ ] No "tested" claims, no legal/tax advice, no banned words
- [ ] Not a copy of a previous reply

---

## 8. Weekly queue (agent fills; user posts)

**IDs and statuses (2026-10-06):** Quora items are `W<week>-<n>`, Reddit items `R<week>-<n>`. Status is one of **Ready** (draft done, waiting for the user) · **Posted YYYY-MM-DD** · **Skipped (reason)**. The daily email shows only **Ready** rows (at most 2 a day, oldest first, with the full answer text and exact clicks, `AUTOPILOT.md` §6.1 "Community today"). Each Ready row also has a PM Tracker row `Community <ID> (<platform>): <thread title>`; when the user sets it to Done, the robot changes the row here to "Posted <date>".

| Week | Platform / community | Thread URL | Angle | Draft (file or inline) | Link? | Status |
|---|---|---|---|---|---|---|
| 1 | Quora (legal) | https://www.quora.com/Are-there-any-specific-case-management-software-solutions-that-cater-well-to-small-or-solo-law-practices | Pick by what breaks first; demo your real trust workflow; trust rules come from the bar | `knowledge/community-week1-drafts.md` W1-1 | No | Posted 2026-10-05 (user) |
| 1 | Quora (real estate) | https://www.quora.com/What-is-the-best-CRM-for-real-estate-agents-to-track-their-deal-stages-and-contacts | Pre-contract stages = CRM; post-contract = checklist keyed off the contract date | W1-2 | No | Posted 2026-10-05 |
| 1 | Quora (legal intake) | https://www.quora.com/What-are-some-of-the-questions-that-legal-intake-professionals-should-ask-potential-clients | Conflict check first, then matter, dates, goals, fees; keep the form short | W1-3 | No | Posted 2026-10-05 |
| 1 | Quora (photographers) | https://www.quora.com/How-do-I-make-photography-contracts-for-clients | Clause checklist + one lawyer review; contract, retainer, questionnaire together | W1-4 | No | Posted 2026-10-05 |
| 1 | Quora (RE brokers) | https://www.quora.com/What-is-the-best-CRM-to-use-for-real-estate-broker-owners-who-want-to-see-what-their-agents-are-doing | Pipeline visibility, not surveillance; roles + transaction system for compliance | W1-5 | No | Posted 2026-10-05 (user clicked Post) |
| 1 | Reddit (§4 subs) | replaced by the Reddit plan in §10 | — | — | — | Skipped (plan changed 2026-10-06) |
| 2 | Quora (legal) · W2-1 | https://www.quora.com/Which-law-practice-management-software-do-law-firms-use | How firms really decide: size bracket, trust accounting, adoption, exit | `knowledge/community-week2-drafts.md` W2-1 | No | Ready |
| 2 | Quora (legal) · W2-2 | https://www.quora.com/unanswered/How-can-small-law-firms-implement-effective-practice-management-software | 6-step rollout for small firms (unanswered question) | W2-2 | No | Ready |
| 2 | Quora (real estate) · W2-3 | https://www.quora.com/Whats-the-best-transaction-management-software-for-real-estate | Pick by who does the transaction work; contract-date test | W2-3 | No | Ready |

---

## 9. Measurement

- **Monthly:** GA4 sessions + engaged sessions from `reddit.com` and `quora.com` (`ga_pull.py` sources report), and which bridged page received them.
- **Leading signals:** replies and upvotes on our answers; mentions of ToolPickGuide by others.
- **Review on Nov 1:** keep the angles that earned replies, drop the rest, and set November's targets.

---

## 10. Reddit plan (reorganized 2026-10-06)

**The hard fact (tested 2026-10-06):** no agent tool can open Reddit. The Chrome extension refuses reddit.com ("not allowed due to safety restrictions") and web search refuses it too. So **you** pick the threads (5 minutes a week); everything else is prepared for you.

**The weekly loop**

| Step | Who | When |
|---|---|---|
| 1. The Monday email has a "Reddit picks" block with 3 ready-made search links (below), sorted by New, past week | Weekly robot | Mondays |
| 2. Click a link, pick **1–2** threads: a real question, under 2 weeks old, not already answered well | You (5 min) | Monday or Tuesday |
| 3. Hand them over: in the PM Tracker, add a row with Task `Reddit pick`, the thread link in **File / command**, and the post's question text pasted in **Next action** (or paste link + text to the agent in the Claude app) | You (1 min) | same day |
| 4. The robot writes the answer as `R<week>-<n>` (full draft in `knowledge/community-week<N>-drafts.md`, §8 row Ready) | Daily robot | next morning |
| 5. The daily email shows it in "Community today" with the full answer and exact clicks; you post it and set the row to Done | You | when shown |

**Search links (the Monday email copies these):**
- r/smallbusiness: https://www.reddit.com/r/smallbusiness/search/?q=CRM%20OR%20onboarding%20OR%20intake&sort=new&t=week
- r/LawFirm: https://www.reddit.com/r/LawFirm/search/?q=software%20OR%20Clio%20OR%20MyCase%20OR%20intake&sort=new&t=week
- r/realtors: https://www.reddit.com/r/realtors/search/?q=CRM%20OR%20transaction%20OR%20dotloop&sort=new&t=week

**Pace and safety:** weeks 2–3: 1–2 comments a week, **no links**, start in r/smallbusiness. From week 4: 2–3 a week; at most 1 in 5 with a link and never where the rules ban self-promotion. Before your first comment in a subreddit, read its **Rules** box on the right side of the subreddit page (30 seconds): if it bans self-promotion, never mention ToolPickGuide there. If Reddit removes a comment for low karma, keep commenting in r/smallbusiness for a while first.

**How to post a Reddit comment (exact clicks):** open the thread link (signed in) → click the box **"Join the conversation"** / **"Add a comment"** under the post → paste the answer → click **Comment**. Then set its PM Tracker row to **Done**.
