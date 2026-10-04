# 🧠 DYNAMIC AGENT MEMORY & COMPETITOR LOG

## 📍 CURRENT_SESSION_CONTEXT
- **Active Sprint:** Sprint 1: Affiliate program lookup (Accounting + Coaches), completed 2026-09-29, QA signed off
- **Current Executor:** PM Agent (6-agent org per `MANDATE.md`; Content Writer OFF-DUTY)
- **System Status:** 4 live vertical pages upgraded; categories updated; post 508 retire pending. See `LOOP.md` → Current State

## 🔍 COMPETITOR INTELLIGENCE & SPY LOG
*(This is where the SEO Agent will log discovered competitor URL structures, keyword gaps, and layout strategies)*

### Phase 1 Run — 2026-09-27 (SEO Agent)

**Sources used:** Google Autocomplete (US, `hl=en`), live Google SERP top ~9 per vertical, comparison/review articles surfaced for Reddit-style "X vs Y" queries.
**Not yet available:** Search volume, CPC, keyword difficulty (needs Ahrefs/Semrush/GKP export). Google Trends not queried (no reliable automated access). Reddit/Quora threads were not read directly — "vs" queries returned vendor/affiliate comparison pages instead. All intent notes below are qualitative.

---

#### 🧭 Cross-Vertical SERP Patterns
- **Vendor blogs dominate BoFu SERPs.** Tools rank "best X software" listicles on their own domains (MyCase, TaxDome, Canopy, Financial Cents, Plutio, Agiled, Paperbell, Nutshell, Pipedrive, Close). Each ranks itself #1 → trust gap for an independent reviewer.
- **Independent publishers present:** Lawyerist (legal), Software Advice / Capterra / G2 (all), Zapier (real estate), The Close + HousingWire (real estate). These are the real editorial competitors.
- **Year-stamped titles are standard** ("… in 2026"). Autocomplete already surfaces `2026` and even `2025` modifiers → titles must carry the year and be refreshed annually.
- **`reddit` modifier appears in autocomplete** for legal, real estate, and photographers → buyers distrust listicles and want peer opinions. Opportunity: "honest / tested / no-affiliate-bias" framing plus first-hand setup notes.
- **"X vs Y vs Z" 3-way comparisons** (Practiq, SuperDupr, US Tech Automations) rank for head-to-head queries — MoFu/BoFu gap for our Decision Engine.
- **Market changes competitors get wrong** (freshness gap to exploit):
  - Practice.do has **shut down** (coaching).
  - Copilot **rebranded to Assembly** (Sept 2025) (agency portals).
  - kvCORE is now **BoldTrail** (real estate).
  - HoneyBook had a **price hike** — "HoneyBook alternatives" is an active query angle.

---

#### ⚖️ 1. Legal Tech (Case Management & CRM)
| Signal | Findings |
|---|---|
| Autocomplete (head) | best legal case management software · best legal practice management software · best law practice management software for solo · best attorney case management software · best law firm crm · law practice crm |
| Autocomplete (modifiers) | reddit · for small firms · for solo · uk / australia (geo — exclude) |
| Weak autocomplete | "client intake software for law firms" returns almost no suggestions → low volume or phrased differently ("legal intake software") — verify with volume tool |
| SERP competitors | mycase.com, lawyerist.com, softwareadvice.com, softwarefinder.com, caretlegal.com, quickbase.com, legalsoft.com, thelegalpractice.com |
| Tools repeatedly cited | Clio, MyCase, PracticePanther, Lawcus, Rocket Matter, CosmoLex, Actionstep |
| Buyer intent pattern | Solo / 2–5 attorney firms choosing between Clio (integrations, billing depth) vs MyCase (client portal, simplicity) vs PracticePanther (price). Regret driver: choosing on feature checklists, switching within ~18 months |
| Content gap | "practice management" terminology dominates; CRM/intake-specific BoFu (Lawmatics, Clio Grow) is thin in top SERP |

#### 🧾 2. Accounting & CPA Practices
| Signal | Findings |
|---|---|
| Autocomplete (head) | best accounting practice management software · best practice management software for small accounting firms · best bookkeeping practice management software · cpa client portal software · tax client portal software |
| Weak autocomplete | "tax document collection software" → no expansions (verify volume; may be long-tail with high intent) |
| SERP competitors | clinked.com, taxdome.com, financial-cents.com, figsflow.com, getcanopy.com, xenett.com, cpacharge.com, finlens.app |
| Tools repeatedly cited | TaxDome, Canopy, Karbon, Financial Cents, Pascal Workflow, TPS Cloud Axis, Basil |
| Buyer intent pattern | Decision framed by bottleneck: portal/document collection → TaxDome; team email workflow → Karbon; tax resolution → Canopy |
| Content gap | SERP is almost entirely vendor-owned. An independent "by bottleneck" comparison matches our brand angle ("won't collect tax files") |

#### 🏢 3. B2B Agencies & Professional Services
| Signal | Findings |
|---|---|
| Autocomplete (head) | agency client portal software · marketing agency client portal · creative / design / web agency client portal · best crm for marketing agencies · best crm for small agencies |
| Noise to exclude | recruitment, staffing, travel, insurance, government agencies (different ICP) |
| Weak autocomplete | "client onboarding software for agencies" → zero suggestions |
| SERP competitors | softr.io, onesuite.io, assembly.com, clinked.com, thefusebase.com, agiled.app, moxo.com, zite.com, getzendo.io |
| Tools repeatedly cited | SuiteDash, Assembly (ex-Copilot), ManyRequests, Agiled, AgencyPro, Accelo, Basecamp, Moxo |
| Buyer intent pattern | Pricing model is the decision driver: flat-fee (SuiteDash) vs per-user (Assembly ~$39–89/user) vs productized-agency tooling (ManyRequests). Lock-in after ~20 clients onboarded |
| Content gap | "Client portal" is the winning term, not "CRM." Pricing-at-scale calculators (cost at 10/25/50 clients) are absent |

#### 🏠 4. Real Estate Agents & Brokers
| Signal | Findings |
|---|---|
| Autocomplete (head) | best crm for real estate agents · best crm for real estate agents free · best crm for real estate agents reddit · best real estate transaction management software · real estate transaction coordinator software · real estate broker transaction management software |
| Noise to exclude | India, Dubai, Dehradun, Canada, Australia (geo); commercial real estate |
| SERP competitors | close.com, theclose.com, zapier.com, housingwire.com, crm.org, marketleader.com, quickbase.com |
| Tools repeatedly cited | Follow Up Boss, Lofty (ex-Chime), BoldTrail (ex-kvCORE), Wise Agent, LionDesk, Real Geeks, HubSpot; transaction mgmt: dotloop |
| Buyer intent pattern | Solo agent vs team vs brokerage split. Price gap is large (FUB ~$58–69/user vs BoldTrail ~$500+/mo). Speed-to-lead and lead-source integrations are the key criteria |
| Content gap | Most competitive vertical (strong editorial publishers). Transaction management / TC software is a less crowded secondary cluster |

#### 📸 5. Photographers & Creative Studios
| Signal | Findings |
|---|---|
| Autocomplete (head) | best crm for photographers · best crm for photographers reddit · best crm for photographers free · best crm for wedding photographers · best crm for photography business · photography client management software |
| Sub-niches | wedding photographers, real estate photographers |
| SERP competitors | softwarefinder.com, plutio.com, aftershoot.com, blog.bloom.io, unscriptedphotographers.com, maroo.us, agiled.app, swellsystem.com, supabook.ai |
| Tools repeatedly cited | HoneyBook, Dubsado, Studio Ninja, Táve, Bloom, ShootQ, Sprout Studio, Unscripted, Plutio |
| Buyer intent pattern | HoneyBook (fast setup) vs Dubsado (deep customization, steep setup). HoneyBook price hike is driving switch intent |
| Content gap | "HoneyBook alternatives" / switching guides; wedding-specific BoFu page |

#### 🎯 6. Coaches & Consultants
| Signal | Findings |
|---|---|
| Autocomplete (head) | best crm for coaches · best crm for coaching business · best crm for life coaches · coaching client management software · coaching practice management software |
| Weak autocomplete | Short suggestion list → smaller volume than other verticals (verify) |
| SERP competitors | nutshell.com, pipedrive.com, fuzen.io, salesmate.io, plutio.com, simply.coach, delenta.com, bestcrmforcoaches.com (exact-match domain), businesscoachvas.com |
| Tools repeatedly cited | Paperbell, HoneyBook, Dubsado, HubSpot, GoHighLevel, Nutshell, Simply.Coach, Delenta; Practice.do (**defunct**) |
| Buyer intent pattern | Solo coaches want scheduling + packages + payments + portal in one; generic CRMs (Pipedrive, Nutshell) rank but don't fit the workflow |
| Content gap | "Practice.do alternatives" (displaced users); purpose-built vs generic CRM framing |

---

#### 🚩 SEO Agent Recommendations for the Gatekeeper (unapproved)
1. **Lowest-competition entry points:** Accounting (vendor-only SERP) and Coaches (weak editorial competition).
2. **Hardest:** Real Estate (The Close, HousingWire, Zapier). Consider entering via transaction management instead of the CRM head term.
3. **Terminology per vertical:** Legal → "practice management software"; Accounting → "practice management" + "client portal"; Agencies → "client portal"; Real Estate / Photographers / Coaches → "CRM".
4. **Freshness wedges:** Practice.do shutdown, Copilot→Assembly, kvCORE→BoldTrail, HoneyBook price hike.
5. **Before approval:** pull volume, CPC, and KD for every head term above.

## 💡 LEARNINGS, FACT EXTRACTION & SEO INSIGHTS
*(This is where agents append structured facts, high-intent phrases, and CPC estimates before Gatekeeper approval)*

### Gatekeeper Decision — 2026-09-27 (Website Manager) · PROVISIONAL
- **Approval type:** Provisional, pending measured volume/CPC/KD data. Full detail in `VERTICAL_MATRIX.md`.
- **Metrics source check:** `brand-discovery-worksheet.md` holds **no** CPC, volume, or intent metrics (positioning/ICP/voice only). All CPC values in the matrix are tagged `EST` (low confidence).
- **APPROVED - HIGH PRIORITIZATION:** 🧾 Accounting (`/best-accounting-practice-management-software/`), 🎯 Coaches (`/best-crm-for-coaches/`).
- **Priority order:** Accounting → Coaches → Photographers → Agencies → Legal → Real Estate (entry via transaction management).
- **Approved Top 5 per vertical:**
  - Legal: Clio, MyCase, PracticePanther, Lawmatics, Rocket Matter
  - Accounting: TaxDome, Karbon, Canopy, Financial Cents, Pascal Workflow
  - Agencies: SuiteDash, Assembly (ex-Copilot), ManyRequests, Agiled, Accelo
  - Real Estate: Follow Up Boss, Lofty, BoldTrail (ex-kvCORE), Wise Agent, LionDesk
  - Photographers: HoneyBook, Dubsado, Studio Ninja, Táve, Sprout Studio
  - Coaches: Paperbell, Simply.Coach, Delenta, HoneyBook, GoHighLevel
- **Locked (provisionally):** Flat slugs `/best-<category>-<vertical>/`, year in SEO title only via `%currentyear%`.

### Gatekeeper Decision: 2026-09-28 · No Cannibalization (User Directive)
- **Rule:** Never create articles that compete with existing live pages. One intent = one URL.
- **Legal vertical re-mapped to live pages:** pillar is now `/best-legal-case-management-software/` (live). `/best-crm-for-law-firms/` and `/legal-practice-management-software/` are also live.
- **Removed from plan:** `/best-legal-practice-management-software/`, `/best-practice-management-software-solo-attorneys/`, `/best-law-firm-crm/`.
- **Legal work going forward:** optimize the live pillar (practice-management secondary keyword + solo section), plus 2 new supporting pages: `/clio-vs-mycase-vs-practicepanther/` and `/law-firm-client-intake-process/`.
- **Registry:** `VERTICAL_MATRIX.md` → Live Page Registry (8 live URLs as of 2026-09-28).

### Photographers Expansion (SEO Agent) · 2026-09-29
- Full brief: `knowledge/briefs/photographers-expansion-brief.md` (QA ✅).
- **Top gap:** Pixieset Studio Manager (autocomplete: pricing, free, review, reddit, vs honeybook). Missing from 487.
- **Freshness edge:** competitors still say "Táve"; we say VSCO Workspace.
- **Studio Ninja (official, 2026-09-29):** $16/$27/$40 mo, $160/$270/$400 yr, 7-day trial; Starter has no booking forms or automation.

## 🤝 AFFILIATE PROGRAM LOG (Affiliate Agent)

> **Corrections 2026-10-04 (verified on official pages in a browser; application kit: `knowledge/affiliate-applications.md`):**
> - **PracticePanther:** the open "Simple Referral" program is a lead-submission form, with no trackable web link. A trackable link comes only with Certified Preferred Partner status (needs 3 paying referrals per year). Not usable for the site yet.
> - **Canopy:** "Log in to Canopy to get your referral link". It's a customer program, and the $50 goes to the referred person, not the referrer. Not usable.
> - **TaxDome:** the publisher partner program is **gone** (verified 2026-10-04: marketing.taxdome.com does not resolve and taxdome.com/partner-program is a 404). taxdome.com/referral-program is customer-only: you need a TaxDome account; firm owners get a free seat-month and team members a $100 Amazon gift card per referral. Not usable for the site. Accounting has no usable program now (Karbon customer referral only; Canopy customer-only).
> - **Dubsado:** the basic affiliate program pays **$35 in Dubsado credit** (60-day retention). The **Ambassador program** pays **$75 cash via PayPal** with 30% off for referrals: https://www.dubsado.com/ambassador-program
> - **Pixieset (new):** $20 per paid signup, $20 off for the referred user, monthly PayPal (affiliates.mypixieset.com). Reviewed application for educators and brands.
> - **MyCase → 8am Affiliate and Creator Program (new 2026-10-04):** linked from mycase.com/partners as 'MyCase Affiliate Program' → https://www.8am.com/affiliate-program/. Runs on **impact.com**. Covers MyCase, LawPay, CasePeer, DocketWise, CPACharge. Eligibility: 'practitioners, educators, content creators, and review sites'. Commission on every new paid subscription (rate not published). Rules: no PPC on the 8am brand, no deceptive tactics. One Impact account can also join other brands on Impact.
> - **Follow Up Boss:** no affiliate program ("considering"). **SkySlope:** no public program (3P). Real estate needs sprint 3 (T1.5).

### Sprint 1: Accounting + Coaches Program Lookup · 2026-09-29 · QA: ✅ signed off (see bottom)

- **Scope:** the 10 approved tools in `VERTICAL_MATRIX.md` and the live pages 412 (Accountants) and 492 (Coaches).
- **Method:** each vendor's own affiliate/partner page first; third-party sources only where the official page lacks a detail, marked **(3P)**.
- **Not done by design:** no signups. Joining a program creates an account in the user's name, so **the user signs up**. Link formats are confirmed from each dashboard after joining.
- **Verification key:** ✅ official page · 🟡 official page, partial · 🔸 third-party only · ⛔ no public program found

---

#### 🧾 Accounting (live post 412)

| Rank | Tool | Program type | Commission | Cookie | Network / signup | Verified |
|---|---|---|---|---|---|---|
| 1 | **TaxDome** | Partner program (pre-approved) + Premium (application) | **$150 per referred company (3P/blog)**; Premium custom; 5% of sub-partners' earnings (3P) | **90 days** | Typeform signup: `taxdome.typeform.com/to/thXReJ6w` · PayPal monthly, **$100 min**, 30-day grace | 🟡 |
| 2 | **Karbon** | Affiliate program for creators (separate from customer referral) | Not published. Customer referral pays **$100 per new annual user** (3P summary of Karbon help doc) | Not published | Referral Factory: `karbon.referral-factory.com/PBFCna/` | 🟡 |
| 3 | **Canopy** | Affiliate/referral | **$50 per completed demo + 10% of subscription, capped at $2,500** | Not published | `referrals.getcanopy.com/v2/3/access` · page states "minimum contract value of $1,000 to apply" (unclear: confirm whether this applies to affiliates or to referred firms) | ✅ |
| 4 | **Financial Cents** | ⛔ No public affiliate program. Its "Partner Program" gives *accounting-firm customers* a promo code for their own clients | n/a | n/a | Ask Financial Cents directly | ⛔ |
| 5 | **Pascal Workflow** | ⛔ No affiliate or referral program found | n/a | n/a | Ask Pascal directly | ⛔ |

#### 🎯 Coaches (live post 492)

| Rank | Tool | Program type | Commission | Cookie | Network / signup | Verified |
|---|---|---|---|---|---|---|
| 1 | **Paperbell** | Affiliate (application reviewed) | **$100 one-time** per referral (monthly or annual plan), no cap | **365 days** | FirstPromoter: `paperbell.firstpromoter.com` · PayPal (USD), worldwide | ✅ |
| 2 | **Simply.Coach** | Affiliate | **1 month of the referred plan, up to $199**, paid on signup | Not published | FirstPromoter: `simplycoach.firstpromoter.com` | ✅ |
| 3 | **Delenta** | Affiliate | **20%+** per activated referral; higher partner tiers reported up to 40% (3P) | Not published | Form on `delenta.com/affiliate` | 🟡 |
| 4 | **HoneyBook** | Affiliate for creators/reviewers (application; distinct from member referrals) | **$50 per new subscriber**; audience gets **25% off first year**; paid **100 days** after signup if still active | Not published | Google Form: `forms.gle/L5XMJGtSKuQuns7FA` | ✅ |
| 5 | **GoHighLevel** | Affiliate | **40% recurring for the life of the account**; 5% second tier (3P) | 90 days (3P) | `affiliate.gohighlevel.com` · PayPal/check, $50 min (3P) | 🟡 |

---

#### 🔗 Link Structures & Upload Wiring

| Network | Tools | Link format | What the uploader needs |
|---|---|---|---|
| FirstPromoter | Paperbell, Simply.Coach (GoHighLevel: likely, per 3P) | Unique link issued in the dashboard; FirstPromoter tracks via the `_fprom_ref` cookie. Exact URL parameter **not documented publicly: copy from your dashboard** | Uploader auto-detects `?fpr=`; add the vendor domain to the article's `Affiliate domains` row as a backstop (e.g., `paperbell.com, simply.coach`) |
| Referral Factory | Karbon | Hosted link on `karbon.referral-factory.com/...` | Add `referral-factory.com, karbonhq.com` to `Affiliate domains` |
| Vendor-issued | TaxDome, Canopy, Delenta, HoneyBook | Issued after approval | Add each vendor domain to `Affiliate domains` once the real link format is known |

- **Rule reminder (brand voice + mandate):** payouts **never change rankings**. GoHighLevel's 40% recurring stays at #5 for coaches.
- **Disclosure:** every article already carries the affiliate disclosure under the H1. Keep it when links go in.

#### ✅ Next Actions
- [ ] **User:** sign up, starting with the top-ranked, clearest programs: TaxDome (pre-approved), Paperbell, Simply.Coach, HoneyBook (application), Canopy
- [ ] **User:** paste each approved link (or its format) back to the Affiliate Agent
- [ ] **Affiliate Agent:** record real link formats here, then hand `Affiliate domains` values to the Onsite Agent
- [ ] **Onsite Agent:** add links + `Affiliate domains` rows to upgrade files 412/492 → dry run → user runs `--replace-live --force-replace`
- [ ] **Affiliate Agent:** ask Financial Cents and Pascal Workflow about publisher programs (email template on request)

**Sources:** [TaxDome partner program](https://taxdome.unstack.website/) · [TaxDome program launch](https://blog.taxdome.com/the-taxdome-partner-program-officially-launched/) · [Karbon partnerships](https://karbonhq.com/partnerships/) · [Karbon referral help](https://help.karbonhq.com/en/s/articles/5518067-does-karbon-have-a-referral-program) · [Canopy affiliate](https://www.getcanopy.com/lp/affiliate-referral-sign-up/) · [Financial Cents terms](https://financial-cents.com/terms-of-use/) · [Paperbell affiliate info](https://paperbell.com/affiliate-information/) · [Simply.Coach affiliate](https://simply.coach/affiliate-program/) · [Delenta affiliate](https://www.delenta.com/affiliate) · [HoneyBook affiliates](https://www.honeybook.com/lp/affiliates) · [HighLevel affiliate](https://affiliate.gohighlevel.com/) · [GoHighLevel terms (3P)](https://thatmarketingbuddy.com/affiliate-programs/gohighlevel) · [FirstPromoter concepts](https://docs.firstpromoter.com/script-docs/concepts.md)

**QA sign-off (2026-09-29):** every row has a verification level; third-party figures marked (3P); no signups performed; no ranking changes; banned-word scan clean; all sources linked.

---

### Sprint 2: Legal Program Lookup · 2026-10-02 (user request) · posts 368 + 397

Same method and key as Sprint 1. No signups.

#### ⚖️ Legal (live posts 368 BOFU, 397 TOFU)

| Rank on 368 | Tool | Program type | Commission / reward | Eligibility for a review site | Signup | Verified |
|---|---|---|---|---|---|---|
| 1 | **Clio** | Customer referral ("Refer a Friend") + channel/consultant partner program | Referral: **$250 gift card** per referred firm that signs up (promo: $500 if the firm buys by 2026-08-31, now expired); referee gets 10% off. Channel partner terms not published | Referral link lives inside a **Clio Manage account** → not usable without being a customer. Channel program targets consultants: **ask Clio about publisher terms** | `clio.com/refer-a-friend/` · `clio.com/partnerships/channel-partners/` | 🟡 |
| 2 | **MyCase** | Consultant/partner referral program (PartnerStack) | Tier 1 (1–2 referrals) **10% of annual net payments** · Tier 2 (3–19) **15%** · Tier 3 (20+) **20% recurring**. Lower tiers: first-year fees only. Paid monthly ≤45 days after month end. **6-month** attribution window | ⚠️ Terms: "must be a Person engaged in the business of providing consulting services to law firms." **A review site likely doesn't qualify**: ask MyCase | `mycase.com/partners/consultant-program/` | ✅ |
| 3 | **PracticePanther** | Referral partner ("Simple Referral") + Certified Preferred Partner | **10%** (annual plans) / **5%** (monthly). Preferred Partner (after 3 paying referrals in a year): **12% / 7%** + co-branded landing page and trackable demo link. Earned after 30 days as a customer | No eligibility restriction stated. Payout timing and cookie not published | `practicepanther.com/affiliates/` · terms: `practicepanther.com/affiliate-program-terms-and-conditions/` | ✅ |
| 4 | **Smokeball** | Referral program (open to anyone) | **$300 eGift card** per referral that signs a contract; no limit; referral must not have been active in the last 90 days. California attorneys can't receive the card | Open to "anyone": fine for a publisher, but it's form-based (no tracked link) | `smokeball.com/referral-program` | ✅ |
| 5 | **Filevine** | Partner program (MSPs, consultants, implementation, integrations) + customer "Advocates" | **10% of first-year revenue** per referred paying customer **(3P)**; not confirmed on Filevine's own pages | Unclear: ask Filevine | `filevine.com/partners/` | 🔸 |
| 6 | **Lawmatics** | Affiliate partnership (open to consultants, clients, "anyone") | **10% of first-year annual contract value**, one-time, paid after the referral is an active customer for **90 days**. Customer referral program (customers only): $500 per firm | ✅ Open to anyone; free; dedicated rep | `lawmatics.com/partners/affiliate` | ✅ |

**Takeaways for the user (ranking never changes because of payouts):**
- **Clearly joinable as a publisher now:** PracticePanther (10% annual / 5% monthly) and Lawmatics (10% of first-year ACV). Smokeball's $300 referral is open but form-based.
- **Probably not open to review sites:** MyCase (consultants only per its terms) and Clio (customer referral needs an account). Email both and ask for publisher/affiliate terms.
- **Unconfirmed:** Filevine's 10% figure is third-party only.
- **Cookie lengths:** not published by any of the six.

**Sources:** [Clio referral](https://www.clio.com/refer-a-friend/) · [Clio channel partners](https://www.clio.com/partnerships/channel-partners/) · [MyCase consultant program](https://www.mycase.com/partners/consultant-program/) · [MyCase partner terms](https://www.mycase.com/partners-terms-conditions/) · [PracticePanther referral partners](https://www.practicepanther.com/affiliates/) · [PracticePanther affiliate terms](https://www.practicepanther.com/affiliate-program-terms-and-conditions/) · [Smokeball referral program](https://www.smokeball.com/referral-program) · [Filevine partners](https://www.filevine.com/partners/) · [Filevine affiliate (3P)](https://openaffiliate.dev/programs/filevine) · [Lawmatics affiliate](https://www.lawmatics.com/partners/affiliate)

**QA sign-off (2026-10-02):** verification level on every row; third-party figure marked (3P); no signups; rankings unchanged; sources linked.

### Sprint 3 (T1.5) · Real estate, photographers, forms/web, e-sign · 2026-10-04
Verification: ✅ official page read in a browser/fetch · 🟡 third-party only (3P) · ⛔ no publisher program. "Mentions" = times the tool appears on our live pages.

| Tool | Our pages (mentions) | Program | Pays | Network / apply | Verified |
|---|---|---|---|---|---|
| **Lofty** | real estate CRM (20) | Affiliate, "open to everyone" | **10% of monthly subscription for 24 months**; 20% if 10+ customers in a quarter | lofty.com/affiliate (signup via JS button) | ✅ |
| Follow Up Boss | real estate CRM (20) | none ("considering") | n/a | n/a | ⛔ |
| Wise Agent | real estate CRM (21), TM (15) | customer referral only (5 paying referrals = free base account); Brand Ambassador program (top agents) | n/a for publishers | n/a | ⛔ (3P summary) |
| dotloop | TM (20) | customer referral only ($250 Visa gift card) | n/a | n/a | ⛔ |
| SkySlope | TM (20) | no public program (3P) | n/a | n/a | ⛔ |
| Open to Close, Paperless Pipeline, DocJacket | TM (OtC 17) | nothing public found | n/a | ask by email later | ⛔ |
| **Sprout Studio** | photographers (18) | Affiliate (open invite) | **20% of subscription for the first 3 months** (+ limited $50 bonus); PayPal, $50 min | affiliates.trysproutstudio.com/signup?campaign=sprout-studio-ambassadors | ✅ |
| **Studio Ninja** | photographers (16) | Ambassador (selective) | **40% commission monthly**; readers get 50% off for 12 months; renewal needs 5 referrals per year | studioninja.co/ambassador-registration/ | ✅ |
| **Jotform** | form builders (11), intake template (3) | Affiliate (case-by-case; customer status not required) | **30% for the first 12 months**, paid monthly; 60-day paid-user rule; PayPal via Tremendous | jotform.com/partnership/affiliate/ (form; reviewed within 1 business day) | ✅ |
| **HubSpot** | form builders (18), e-sign (3), onboarding (3) | Affiliate (SaaS reviewers and blogs eligible) | **30% recurring up to 1 year**; 180-day cookie; $10 min | **Impact** (reviewed in 2–3 days) | ✅ |
| **Wix** | website builders (32) | Affiliate, "all types of creators" | per Premium conversion (amount shown after approval; 3P: $100 flat, 30-day cookie) | **Impact** (Wix.brand) | ✅ program / 🟡 amount |
| **Squarespace** | website builders (31) | Affiliate (relevant websites) | per conversion (amount after approval; 3P: $100–200, 45-day cookie) | **Impact**; worldwide, USD | ✅ program / 🟡 amount |
| **PandaDoc** | e-sign (13) | Affiliate partner track | **20–25% of year one** (tier) | eulerapp.com partner portal ("Apply as an affiliate") | ✅ |
| DocuSign | e-sign (20) | Affiliate via CJ (3P) | 3P: $25–100 per paid signup, 30-day cookie | CJ Affiliate (needs a CJ account) | 🟡 |

**Takeaways:** (1) Impact now covers 8am + HubSpot + Wix + Squarespace with one account. (2) Real estate has exactly one publisher program (Lofty); the TM tools on 586 have none, so that page earns through Lofty/CRM cross-links, not TM affiliates. (3) Highest value per signup: Studio Ninja 40% monthly, Lofty 10% × 24 months, HubSpot/Jotform 30% × 12 months.

### Sprint 4 · Every other tool featured on our live pages · 2026-10-04
Source: H2/H3 tool names across all live pages. ✅ official page read · 🟡 third-party summary (3P), verify before applying · ⛔ none / not for publishers.

| Tool | Our page(s) | Pays | Network | Verified |
|---|---|---|---|---|
| **Pipedrive** | law-firm CRM, CRM ops | 20% (30% at tier 2) of first 12 months; 90-day cookie; review in 1–2 weeks | **PartnerStack** | ✅ |
| **Zoho (CRM, Desk, People)** | law-firm CRM, CRM ops, free CRM, help desk, onboarding | 15% (18/20% tiers) of first 12 months; 90-day cookie; $100 min; PayPal/wire | own (zoho.com/affiliate) | ✅ |
| **Close** | CRM ops | 30% of first-year subscription ("lifetime available"); approval in 1–2 business days | own form | ✅ |
| **Fillout** | form builders | 30% recurring up to 1 year; 1-minute signup (account) | in-app | ✅ |
| monday.com (Sales CRM) | CRM ops | official PartnerStack page: online affiliates earn **CPL per sign-up**; partners up to 20% per closed deal; 90-day cookie; PayPal/Stripe. Join = mondaycom.partnerstack.com (needs a PartnerStack account) | PartnerStack | ✅ |
| Freshworks (Freshsales, Freshdesk) | CRM ops, free CRM, help desk | 3P: 15% MRR for 12 months (up to 25%) | PartnerStack (3P) | 🟡 |
| Capsule CRM | free CRM | 3P: 20% lifetime (25/30% tiers); 30-day window; PayPal £50 min | own | 🟡 |
| Insightly | CRM ops | 3P: 20% | ? | 🟡 |
| Agile CRM | free CRM | 3P: 20–30% | own | 🟡 |
| Help Scout | help desk | 3P: 30% of first year | ? | 🟡 |
| Zendesk | help desk | **15% of first-year sales**, open to media/publishers/content creators; no Zendesk partners/resellers; join: zendesk.partnerstack.com/?group=externalrecruitment | PartnerStack | ✅ |
| Typeform | form builders | 3P: $20 upfront + 15% monthly | ? | 🟡 |
| Tally | form builders | 3P: 20% up to $150 per referral; 30-day cookie | own | 🟡 |
| Formstack | form builders | 3P: 25% of first year; 30-day cookie; $100 min | (formstack.com/affiliates, Impact-tracked link seen) | 🟡 |
| Gravity Forms | form builders | 3P: 20–30% per sale; $10 min | own | 🟡 |
| WPForms | form builders | 3P: 20% per sale; 45-day cookie; $50 min | own | 🟡 |
| SignWell | e-sign | 3P: 25% recurring up to 1 year; 30-day cookie | own | 🟡 |
| Webflow | website builders | 3P: 50% of first year; 90-day cookie | ? | 🟡 |
| Shopify | website builders | 3P: up to $150 bounty per merchant | own | 🟡 |
| GoDaddy | website builders | 3P: $10–150 per sale; 45-day cookie | CJ (3P) | 🟡 |
| Smokeball | legal case mgmt | $300 eGift card per signed-up referral; "anyone" can refer (lead form, not a tracking link) | own | 🟡 |
| LEAP | law-firm CRM | Referral Partner: $80 per contracted user, max $2,000 per firm, after 90 days (for businesses that help law firms) | own | 🟡 |
| Real Geeks | real estate CRM | affiliate **invite-only** | Impact | 🟡 |
| Copilot (client portal) | onboarding | 3P: 20% of first 12 months via PartnerStack; copilot.com now resolves to Microsoft Copilot, so needs re-check | ? | 🟡 |
| Rocketlane | onboarding | customer referral only ($350 voucher) | n/a | ⛔ |
| Bitrix24 | free CRM | reseller program only | n/a | ⛔ |
| Salesforce, Filevine, GuideCX, Appcues, Pendo, WalkMe, ChurnZero, ClientSuccess, Intercom, Front, Dropbox Sign, Adobe Sign, Proposify, OneSpan, SuiteCRM | various | no public publisher program found | — | ⛔/unknown |

**Takeaways:** (1) A **PartnerStack** account would unlock Pipedrive + likely monday, Freshworks, Zendesk and Copilot in one place; Impact already covers HubSpot, Wix, Squarespace and 8am. (2) Highest-fit next applications: Zoho (5 pages), Pipedrive, Close, Fillout, Help Scout. (3) Everything marked 🟡 gets its official page read before applying.

## 📈 AGENT SELF-IMPROVEMENT & CAPABILITY LOG
*(Every agent must independently log here one professional optimization or prompt skill discovered during execution to improve team knowledge)*

- **2026-09-27 · SEO Agent:** Google's public autocomplete endpoint (`suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=...`) returns clean suggestion lists in bulk. A seed that returns **zero** suggestions is itself a signal (low volume or wrong phrasing), so log empty results rather than dropping them.
- **2026-09-27 · Website Manager / Content Agent:** Tag every unmeasured metric inline (`EST` + confidence level) at the moment it is written, and keep an "Open Items Before Promotion" checklist in the deliverable itself. Estimates then can't silently harden into "facts" when later agents reuse the file.
- **2026-09-27 · Content Agent:** Voice and accuracy are separate passes. Rewrite for voice first, then run a claims sweep: every "most users…", "within days", or "tested" line either cites a source or gets softened. Punchy tone makes unsupported claims *more* persuasive, so they need more checking, not less.
- **2026-09-29 · Affiliate Agent:** "Referral program" and "affiliate program" are different products at B2B SaaS vendors. Referral programs pay *existing customers*; affiliate programs pay *publishers*. Karbon, Financial Cents, and TaxDome all mix the terms, so always classify the program type before logging a commission, or a publisher will plan revenue around a customer-only reward.
- **2026-09-29 · Onsite Agent:** Crawl internal links from the REST API (`/wp-json/wp/v2/posts`, body HTML) rather than rendered pages. It isolates article-body links from menus and footers, so "0 inbound" means the article truly has no editorial links.

- **2026-09-29 · Onsite Agent:** Never add cache-busting query strings when verifying redirects. Rank Math "exact" redirects (and many CDN rules) only match the clean path, so `?nocache=` produces a false "no redirect". Use no-cache request headers instead.

## ❓ UNRESOLVED QUESTIONS & BLOCKERS
- [ ] Missing standalone historical spec files for the 6 verticals. (Note: Use `brand-discovery-worksheet.md` as the primary source for initialization).
- [ ] No search volume / CPC / keyword difficulty data. Needs an Ahrefs, Semrush, or Google Keyword Planner export from the user before Gatekeeper approval.
- [ ] Google Trends and direct Reddit/Quora thread reads not completed (no reliable automated access).
