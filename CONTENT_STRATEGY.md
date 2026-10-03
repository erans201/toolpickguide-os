# 🧭 CONTENT STRATEGY: Site Scope & Cross-Niche Analysis

- **Status:** ✅ APPROVED 2026-10-01: Option B (see section 5). Demand data pending (Keyword Planner).
- **Owner:** PM Agent (runs the process) · SEO Agent (data) · Affiliate Agent (monetization) · QA (gate) · **User (approves)**
- **Created:** 2026-10-01 · **Next review:** 2027-01-01 (quarterly)
- **Why:** the post-32 upgrade (website builders) showed the site has no written scope rule. Without one, every topic decision is ad hoc.

---

## 1. 🔁 The process (run quarterly, or when a new niche is proposed)

| Step | What | Who | Input | Output |
|---|---|---|---|---|
| 1 | **Inventory:** every live URL from `sitemap_index.xml`, grouped into topic clusters | Onsite | sitemap | cluster map (section 2) |
| 2 | **Performance:** impressions, clicks and position per cluster, plus the trend vs last quarter | SEO | `gsc_pull.py` → `data/` | cluster scorecard |
| 3 | **Market demand:** search volume, difficulty and CPC per cluster's head terms | SEO | Semrush / Ahrefs / Keyword Planner export in `data/` | demand column (**currently missing**) |
| 4 | **SERP and competitors:** who ranks (vendors vs editorial), AI Overview citations | SEO | live SERP review | difficulty notes |
| 5 | **Monetization:** affiliate programs, commission and cookie terms per cluster | Affiliate | program pages | money column |
| 6 | **Score** each cluster on the 6 criteria in section 4 | PM + QA | steps 1–5 | ranked clusters |
| 7 | **Decide** a role per cluster: **Core / Expand / Maintain / Freeze / Exit** | **User** | scorecard | approved scope (section 5) |
| 8 | **Translate** into an updated `VERTICAL_MATRIX.md`, a quarterly calendar (Junia briefs + live upgrades) and Sheet tasks | PM | decision | plan |

**Topic gate (every new article or upgrade, between reviews).** Ask 5 questions. A "no" on Q1 or Q2 means out of scope.
1. Is the reader our ICP (owner or partner of a service business: law, CPA, agency, real estate, photo, coaching)?
2. Is the topic in an approved cluster (section 5)?
3. Can it link naturally **to** a CRM-core page, and receive a link **from** one?
4. Is the intent free (no cannibalization, sitemap checked)?
5. Does it earn (affiliate) or support a page that earns (TOFU feeding a BOFU)?

---

## 2. 📊 Current state: cross-niche inventory (2026-10-01)

Positioning (`brand-discovery-worksheet.md`): *B2B software reviews for professional services: **CRM, client portals and onboarding workflows**, for 6 verticals.*

| Cluster | Live URLs | GSC impressions (90 days) | Share | Clicks | Fits positioning? |
|---|---|---|---|---|---|
| **CRM core** (vertical CRM / practice management + CRM explainers) | 10 posts + 4 category pages | 64 | 10% | 0 | ✅ Yes, it *is* the positioning |
| **Client lifecycle tools** (forms, e-sign, onboarding, help desk) | 5 posts + 1 category | 196 | 30% | 0 | ✅ Mostly (onboarding is named; forms and e-sign are part of intake) |
| **Web presence** (website builders) | 1 post (32) | 241 | 37% | 0 | ⚠️ Not named in the positioning; same ICP |
| **Home office / gear** (desk, chair, monitor, router, VPN, notes, cloud storage) | 7 posts | 101* | 16% | 1 | ❌ No: different reader intent, different monetization |
| Site / deleted pages | — | 46 | 7% | 0 | — |

\* Includes `/essential-gear-for-freelancers…/`, which **already returns 404** (as does `/navigating-the-world-of-b2b-software…/`). Their impressions will fade on their own.

**What the data says:**
- **67% of Google's impressions come from non-CRM pages.** Google currently sees the site as "tools for service businesses" more than "CRM for professionals".
- The CRM-core pages are the newest (upgraded 2026-09) and barely indexed yet. 64 impressions is an early reading, not a verdict.
- 648 impressions in total is too little data to choose a niche on its own. **Market demand (step 3) is the missing piece.**

---

## 3. 🧩 Strategic options

### Option A: Narrow CRM authority
*"The CRM and practice-management guide for professional services."*
- **In:** CRM core only (vertical CRM, practice management, client portals, CRM explainers, comparisons).
- **Out:** everything else is frozen or exits, including forms, e-sign, websites and home office.
- ➕ Clearest topical authority. Matches the brand worksheet word for word.
- ➖ Drops about 90% of current impressions. Small keyword universe per vertical. Head terms are dominated by vendor blogs and G2/Capterra.

### Option B: Client-operations stack, with CRM as the hub *(recommended)*
*"Every tool a service business runs its clients on, with the CRM at the center."*
- **Hub:** CRM / practice management per vertical (priority, as today).
- **Spokes:** tools along the **client lifecycle**, only when written for the same ICP:
  - get found (website, booking)
  - capture (forms)
  - sign (proposals, e-sign)
  - onboard (onboarding, client portals)
  - deliver and bill (scheduling, invoicing, help desk)
- Every spoke article is framed for service businesses, never generic, and links to the CRM hub. Example: "website builders that feed your CRM", not "best website builder".
- **Out:** home office and gear, which has a different reader and low-commission physical products.
- ➕ Keeps about 77% of current impressions. Natural internal-link paths (spoke → hub). More affiliate programs. Still one coherent reader.
- ➖ Broader scope means more competitors per spoke (general software publishers). Needs discipline: the topic gate Q3 is what keeps it coherent.

### Option C: Broad B2B / productivity
- **In:** everything, including home office.
- ➖ Two unrelated audiences, diluted topical signals, and the gear pages earn little. **Not recommended.**

---

## 4. 📐 Cluster scorecard (provisional; the Demand column needs data)

Scores: 1 (weak) to 5 (strong). **Demand: measured 2026-10-01. See section 7** (Google volumes via DataForSEO).

| Cluster | ICP fit | Hub adjacency | Current traction | Demand | Competition (5 = easy) | Monetization | Proposed role (Option B) |
|---|---|---|---|---|---|---|---|
| CRM core: Accounting, Coaches, Photographers | 5 | 5 | 2 | ? | 3–4 | 4 | **Core** |
| CRM core: Legal, Real Estate, Agencies | 5 | 5 | 2 | ? | 2 | 4 | **Core** (slower) |
| Onboarding / client portals | 5 | 5 | 3 | ? | 3 | 4 | **Expand** |
| Forms + e-sign (intake) | 4 | 4 | 3 | ? | 2 | 3 | **Maintain → Expand**, vertical-framed |
| Website builders (service business) | 4 | 3 | 4 | ? | 2 | 4 | **Maintain** (one strong page, no new cluster yet) |
| Scheduling / invoicing | 4 | 4 | — | ? | ? | 3 | **Candidate**: evaluate next review |
| Home office / gear | 1 | 1 | 2 | ? | 2 | 1 | **Freeze or Exit** |

Monetization scores are provisional. The Affiliate Agent has researched the Accounting and Coaches programs only.

---

## 5. ✅ Approved scope (user decisions, 2026-10-01)

**Scope: Option B, with the CRM hub and client-lifecycle spokes.** Calendar split: ~60% CRM core · ~30% lifecycle spokes · ~10% TOFU/support.

| Cluster | Role | Content allowed |
|---|---|---|
| CRM core: all 6 verticals | **Core** | New Junia briefs + live upgrades. Top of the calendar. |
| Onboarding / client portals | **Expand** | New briefs, vertical-framed |
| Forms + e-sign (intake) | **Maintain → Expand** | Upgrades now. New briefs once Keyword Planner data confirms demand. |
| Website builders (post 32) | **Maintain** | Upgrade approved, reframed as "website builders for service businesses that capture leads and feed your CRM". No new web pages. |
| Scheduling / invoicing | **Candidate** | Decide at the next review, with Keyword Planner data |
| Home office / gear (7 posts) | **Exit: noindex** | Pages stay live; noindexed through `set_robots.py` (the user runs it). No work. |

**Data sources (decision 4):** Google Search Console via `gsc_pull.py`, Google Analytics 4 via `ga_pull.py`, and Keyword Planner via manual export + `kp_ingest.py`. See `data/README.md`. The Demand column in section 4 gets filled after the first Keyword Planner run.

Roles:
- **Core:** new briefs and upgrades, top of the calendar.
- **Expand:** new briefs, vertical-framed.
- **Maintain:** upgrade existing pages only, no new pages.
- **Freeze:** no work; the page stays as is.
- **Exit:** noindex, or retire with a 301 via `retire_post.py` (the user runs it).

---

## 6. ❓ Decisions needed from the user

1. **Scope:** Option A, B or C (or a variation)?
2. **Website builders (post 32):** under B it becomes a **Maintain** spoke, upgraded and reframed as "website builders for service businesses that capture leads and feed your CRM". Under A it's Freeze or Exit. Which one?
3. **Home office (7 posts):** Freeze (leave as is), Exit by noindex (keep the pages, hide them from Google), or Exit by retire + 301? No 301 target fits naturally, so noindex is the gentler exit.
4. **Market data:** do you have or plan to get Semrush, Ahrefs or Google Keyword Planner access?
   - Without it, step 3 stays empty and the demand column stays "?".
   - Free fallback: Keyword Planner gives volume ranges with a free Google Ads account. You'd create it, since the agent never creates accounts.
5. **Calendar split** (proposal, under B): ~60% CRM core · ~30% lifecycle spokes · ~10% TOFU/support. Approve or change?

---

## 7. 📈 Demand data & re-prioritization (2026-10-01 · ✅ APPROVED 2026-10-02)

**User decisions 2026-10-02:** (1) priority order approved. (2) Legal funnel split decided by the agent: the TOFU page `/legal-practice-management-software/` owns the bare head term (9,900) as an explainer + buyer's guide; the BOFU page `/best-legal-case-management-software/` owns every "best …" and case-management variant and never uses the bare head term as title/H1/focus. Monitor in GSC; if Google ranks the BOFU page for the head term instead, revisit. (3) Rule conflict → **(b)**: new price-heavy BOFU pages go to **Junia with a strict facts sheet** (verified prices only), for now.

**Sources:** `data/dfs-insights-2026-10-01.md` (Google volume, competitor gaps, SERP + AI Overviews via DataForSEO) · `data/demand-2026-10-01.md` (Bing). Bing reports 0 for almost every niche term (it hides small volumes), so **Google numbers drive decisions**. Google groups close variants ("legal" = "law practice management software" = one 9,900), so totals below are de-duplicated by intent.

### 7.1 Google demand per vertical (main intents, searches/month, US)

| Vertical | Biggest intents | Demand | Avg CPC (value signal) | Competition evidence | Current matrix priority | Proposed |
|---|---|---|---|---|---|---|
| ⚖️ Legal | practice management software 9,900 · case management 1,900 · law firm website design 2,400 · law firm crm 390 · clio vs mycase 260 | **~14,000** | **$75–157** | Difficulty 10–36 (low). An independent publisher (lawyerist) ranks #3–4. Reddit and the Florida Bar are in the top 3. | 5 | **1** |
| 🏠 Real estate | real estate crm 4,400 · client management software real estate 2,900 · transaction management 2,400 · crm for agents 1,300 | **~11,000** | $30–49 | Difficulty 20–45. theclose ranks 18–34; the transaction-management top 10 is mostly vendors. | 6 | **2** |
| 📸 Photographers | honeybook pricing 1,600 · photography contract template 1,300 · questionnaire variants ~600 · honeybook vs dubsado 390 · honeybook alternatives 320 · pixieset studio manager 320 · crm for photographers 210 | **~4,700** | $3–35 | The top competitor (unscriptedphotographers) ranks only #6–30. Easy. | 3 | **3** |
| 🏢 Agencies | crm for agencies 1,000 · crm for marketing agencies 390 · portals ≤50 | ~1,400 | $50–92 | Not measured yet | 4 | 4 |
| 🧾 Accounting | practice management for accountants 590 · cpa practice management 110 · tax client portal 50 · tax document collection **0** | ~750 | $63–117 | Not measured yet | **1** | **5** (maintain page 412) |
| 🎯 Coaches | crm for coaches / coaching crm 110 · coaching client management 30 · practice.do / paperbell **0** | **~150** | $22–34 | bestcrmforcoaches.com ranks #3 | **2** | **6** (maintain page 492, no new pages) |

**Cross-vertical (lifecycle spokes):**
- electronic signature software 8,100 (vendors own it)
- website builder for small business 6,600 (vendors own it)
- crm for small business 4,400 (HubSpot/Zoho)
- proposal template 4,400 (Microsoft/Canva)
- form builder 2,900
- service contract template 2,400
- appointment scheduling 2,400
- invoicing 2,400
- client intake form 1,300 + template 480 (low competition)
- client portal software 720
- client onboarding software 480 (CPC $143)

### 7.2 What the SERP / AI Overview check shows (15 biggest targets)
- **We rank in the top 10 for none.** **13 of 15 show an AI Overview, and we are cited in 0.**
- The most-cited sources in AI Overviews are **YouTube (11×)**, HubSpot, Zapier, Clio, Zoho, **Reddit**, Lawyerist and the Florida Bar.
  - Community and video presence (the Marketing Agent's Reddit/Quora plan) feeds AI answers directly.
- **Reddit ranks #2–3 on most commercial SERPs.** That confirms the brand worksheet's "buyers distrust listicles" insight.

### 7.3 Problems the data exposed
1. **⚠️ Legal cannibalization risk:** Google treats "legal practice management software" and "law practice management software" as one 9,900 intent.
   - `/legal-practice-management-software/` (TOFU "what is") and `/best-legal-case-management-software/` (which has "practice management" as a secondary keyword) both touch it. One page must own it.
2. **Matrix priorities don't match demand:** Accounting (priority 1) has ~750 searches/month and Coaches (priority 2) ~150. Legal (priority 5) has ~14,000, at the highest CPCs.
3. **Several planned slugs have no demand:** `tax-document-collection-software`, `how-to-collect-tax-documents-from-clients`, `practice-do-alternatives`, `paperbell-vs-dubsado` and `coaching-client-onboarding-process` are all 0.
4. Post 32's exact target "best website builder for service business" is only 50/month. Its 241 impressions come from many small variants, so its upgrade priority drops.

### 7.4 Proposed next work (ranked; needs approval)
| # | Work | Type | Demand | Owner |
|---|---|---|---|---|
| 1 | **Legal intent consolidation + upgrade:** decide which page owns "legal practice management software" (9,900), then upgrade both legal pages | Live upgrades | ~11,800 | Onsite (in-house) |
| 2 | **Paste the photography contract template brief** (already written) | Junia | 1,300 | User → Junia |
| 3 | **New Junia brief: client intake form template** (cross-vertical, links to the vertical CRM pages; must not target the photography questionnaire) | Junia TOFU | 1,780 | SEO → Junia |
| 4 | **Upgrade 474 real estate:** add "real estate CRM" (4,400) to the title/H1/H2s | Live upgrade | ~7,300 | Onsite |
| 5 | **New page: real estate transaction management software** (2,400, difficulty 20) | BOFU, price-heavy | 2,400 | In-house (rule) |
| 6 | **Upgrade 558 questionnaire** for the variants ("photography questionnaire", "questionnaire for photography clients") | Live upgrade | ~600 | Onsite |
| 7 | **New page: HoneyBook pricing** (1,600; switch-intent hub with drafts 554/556) | Price-heavy | 1,600 | In-house (rule) |
| 8 | **Paste the Pixieset Studio Manager review brief** (already written) | Junia | 320 | User → Junia |
| 9 | **New page: best CRM for agencies** (1,000 + 390) | BOFU | 1,390 | In-house (rule) |
| 10 | **New Junia brief: service contract template** (2,400; no AI Overview on this SERP) | Junia TOFU | 2,400 | SEO → Junia |
| — | Post 32 website builders | Live upgrade | ~50 exact | Keep, but after #1–6 |
| — | Drop from the plan: tax document collection, practice.do alternatives, paperbell vs dubsado, coaching onboarding | — | 0 | — |

**Rule conflict (resolved 2026-10-02 → option b):** CLAUDE.md says price-heavy BOFU pages stay in-house, while MANDATE.md says no new long-form text is written in-house. Items 5, 7 and 9 are new price-heavy pages, so one rule has to give:
- **(a)** allow in-house drafting for new price-heavy BOFU pages, or
- **(b)** send them to Junia with a strict facts sheet.

**Off-page (Marketing Agent):** AI Overviews cite YouTube and Reddit most, so move the Reddit/Quora framework and posting schedule up the calendar.
