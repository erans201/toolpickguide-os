# 🚀 GROWTH PLAN: from A (today) to B (Oct 2027)

- **Owner:** PM Agent (cloud autopilot runs it; `AUTOPILOT.md`) · **User** approves Tier C and does the human-only tasks
- **Created:** 2026-10-03 · **Reviewed:** monthly (scoreboard §6) and quarterly (strategy)
- **Task list with exact instructions:** `TASKS.md`

---

## 1. Point A: where we are (measured 2026-10-01 → 10-03)

| Area | Today | Source |
|---|---|---|
| Indexable articles | **17** (+3 Junia drafts QA'd, not yet published) | sitemap re-crawl 2026-10-02 |
| Google impressions | **648 in 90 days** (~216/month) | Search Console |
| Google clicks | **1 in 90 days** | Search Console |
| Real organic visitors | ~1 session in 90 days (131 of 132 GA4 sessions were the owner) | GA4 |
| Rankings | **0 of 67 target searches in the top 10**; best positions ~51 | Search Console + DataForSEO |
| AI Overview citations | **0 of 15** tracked searches (13 show an AI Overview) | DataForSEO |
| Pages with no internal links in | 1 (`/photography-client-questionnaire/`) | crawl 2026-10-02 |
| Server speed | TTFB 0.26–0.83 s, LiteSpeed cache on, HTML 84–129 KB per page. **Core Web Vitals not measured yet** (T0.11) | curl 2026-10-03 |
| Backlinks | **Unknown** (not measured; T2.9) | — |
| Affiliate programs joined | **0 confirmed** (researched: accounting, coaching, legal) | MEMORY.md |
| Revenue | **$0** | — |

**What's already strong:** a clear niche (Option B), measured demand per vertical, verified-price content with sources, a QA pipeline for Junia, safe tooling, and a data stack (GSC, GA4, Bing, DataForSEO).

---

## 2. Point B: the goal (achievable, not a promise)

| KPI | Month 3 (2027-01-01) | Month 6 (2027-04-01) | **Month 12 (2027-10-01) = B** |
|---|---|---|---|
| Indexable articles | 30 | 45 | **70** |
| Google impressions / month | 3,000 | 15,000 | **50,000** |
| Google clicks / month | 40 | 300 | **1,500** |
| Target searches in top 10 | 2 | 10 (3 in top 3) | **40 (10 in top 3)** |
| Legal head term "legal practice management software" | top 50 | top 20 | **top 10** |
| AI Overview citations (of 15 tracked) | 0 | 1 | **3+** |
| Visitors from Reddit/Quora / month | 20 | 50 | **150** |
| Core Web Vitals (mobile, top 20 pages) | measured, fixes started | **all pass** | all pass |
| Affiliate programs live on pages | 6+ | 12+ | **20+** |
| Affiliate clicks / month | 5 | 30 | **150** |
| Revenue / month | $0 | $0–100 (first commissions) | **$250–650** |

**Why these numbers are realistic:**
- New, focused affiliate sites in low-difficulty B2B niches typically need **4–8 months** before Google trusts them. Months 1–3 are about foundations, so the targets stay small there.
- The demand exists: the main intents we target add up to **~32,000 Google searches/month** across verticals. Reaching 1,500 clicks a month means winning about **5%** of that.
- Legal (~14,000/mo, difficulty 10–36) and real estate (~11,000/mo, difficulty 20–45) carry most of the target, because the difficulty is low and an independent publisher (Lawyerist) already proves the SERP is winnable.

---

## 3. How earnings add up (model, with assumptions)

**Revenue = clicks to our pages × share that click an affiliate link × share that buy × average commission**

| Input | Month 6 | Month 12 | Basis |
|---|---|---|---|
| Google clicks/month | 300 | 1,500 | §2 targets |
| Share landing on BOFU ("best …") pages | 60% | 60% | content mix (60% CRM core) |
| Share clicking an affiliate link | 10% | 12% | typical for comparison pages with tables and CTA buttons |
| = Affiliate clicks/month | ~20 from Google + ~10 from Reddit/direct ≈ **30** | ~110 from Google + ~40 other ≈ **150** | |
| Share that sign up and pay | 2–4% | 3–5% | B2B software trials → paid |
| Average commission | ~$60 | ~$60–100 | PracticePanther ≈ $59 (10% of a $49 × 12 plan) · Lawmatics 10% of first-year contract · Paperbell $100 · HoneyBook $50 · TaxDome $150 |
| **Revenue/month** | **$0–100** (≈1 sale) | **$250–650** (4–7 sales) | the upper end needs the Phase 4 conversion work |

**Upside not counted above:** a 15–20% click-through on strong comparison pages, plus high-value programs (Lawmatics pays 10% of a first-year contract), could double month-12 revenue. That's why Phase 4 is conversion work.

**The biggest levers, in order:**
1. Join the programs and put links on the pages (today: $0 because there are no links at all)
2. Rank legal and real estate BOFU pages (highest search volume × CPC)
3. Conversion: comparison tables, "best for" boxes, clear CTA buttons
4. More programs per page, with honest rankings (payouts never change the order)

---

## 4. Strategy: five pillars

1. **Content (Option B, priorities Legal → Real estate → Photographers → Agencies → Accounting → Coaches).**
   - About 2 new articles a week through Junia + QA, plus 1 upgrade of a live page a week.
   - Monthly price checks; a refresh of every BOFU page each quarter.
2. **Onsite and technical.**
   - Core Web Vitals pass.
   - Every page gets ≥ 3 internal links in, from a contextual link roadmap updated monthly.
   - Clean schema (one FAQPage per page).
   - Fast indexing: Search Console requests plus IndexNow for Bing.
3. **Authority and trust (E-E-A-T).**
   - A real author identity and an honest "how we evaluate" page.
   - Linkable free templates (intake form, contract).
   - Community presence (Reddit/Quora, run in its own chat).
   - Optional YouTube walkthroughs: YouTube is the most-cited source in AI Overviews.
4. **Monetization.** Join programs, add links with FTC disclosure, track outbound clicks as GA4 key events, review earnings per page monthly.
5. **Autopilot and measurement.** Daily, weekly and monthly cloud routines (`AUTOPILOT.md`) report to Drive and the Sheet, so progress against §2 is visible every month.

---

## 5. Phases

| Phase | Dates | Goal | Exit criteria |
|---|---|---|---|
| **0: Infrastructure** | Oct 3–11, 2026 | Repo, cloud agent, secrets, baseline measurements | Daily Ops runs 3 days in a row with no errors; CWV baseline recorded |
| **1: Foundation** | Oct 12 – Nov 30 | Publish the 3 ready drafts; upgrade the real estate, photographer, questionnaire and law-firm CRM pages; join 6+ programs; E-E-A-T pages; technical fixes | 25 articles; all BOFU pages carry affiliate links + disclosure; 0 orphan pages; CWV fix list done |
| **2: Content velocity** | Dec 2026 – Feb 2027 | 2 articles/week; price watch; community 20 replies/month | 40 articles; 3,000+ impressions/month |
| **3: Authority** | Mar – May 2027 | Linkable templates, outreach (the user sends), refreshed pillars, AI-answer formatting | 10 top-10 keywords; first AI Overview citation; backlinks measured and growing |
| **4: Scale and conversion** | Jun – Sep 2027 | Conversion improvements on BOFU pages, agencies cluster, annual refresh | Month-12 targets in §2 |

---

## 6. Scoreboard (the monthly routine fills this in)

| Month | Articles | Impr./mo | Clicks/mo | Top-10 | AI cites | Aff. clicks | Revenue | Notes |
|---|---|---|---|---|---|---|---|---|
| Baseline (Oct 2026) | 17 | ~216 | ~0 | 0 | 0 | 0 | $0 | Point A |
| Nov 2026 | | | | | | | | |
| Dec 2026 | | | | | | | | |
| Jan 2027 | | | | | | | | target: 30 / 3,000 / 40 |
