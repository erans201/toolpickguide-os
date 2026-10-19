# Price watch 2026-10-19 (autopilot Weekly Review, cloud)

- **Scope:** every live BOFU/price page with a facts file in `knowledge/`. That means the upgrade files for posts 368, 397, 412, 474, 487 and 492, plus seven Junia or in-house pages:
  - 586 `/best-real-estate-transaction-management-software/`
  - 601 `/honeybook-pricing/`
  - 603 `/best-crm-for-marketing-agencies/`
  - 618 `/pixieset-studio-manager-review/`
  - 647 `/clio-vs-mycase/` (`knowledge/articles/clio-vs-mycase.md`)
  - 651 `/follow-up-boss-vs-lofty/` (`knowledge/junia-651-follow-up-boss-vs-lofty.md`)
  - 670 `/capsule-crm-review/` (`knowledge/articles/capsule-crm-review.md`)
- **How it was checked:** each vendor's official pricing page was fetched on 2026-10-19, using curl first, then WebFetch, then a reader proxy for pages that block bots or load prices with JavaScript. Each live page was fetched too (public GET).
- **Dollar amounts match both ways.** Every dollar amount in each file also appears on the matching live page, and no live page has an amount the file lacks. The few file amounts that aren't on any vendor page are our own totals (year-one tables, × 12 math) or labeled third-party estimates.
- **Nothing was changed on the site.** Nothing in `knowledge/` was edited either, apart from this report, and no queue rows were added.

---

## 1. NEW changes queued

**None.** No vendor changed a price, plan limit or trial length that any of these 13 pages quotes. No upgrade file was edited, and no row was added to `knowledge/local-queue.md`.

## 2. Carried over from 2026-10-12, status today

| # | Item | Status 2026-10-19 |
|---|---|---|
| 1 | Sprout Studio USD price drop (487), queued 10-12 | ✅ **DONE 2026-10-13** (queue row closed; undo `backups/487-20261013-180125.json`). The live page reads "From $19/month". The official page is unchanged: USD 19 / 36 / 51 / 69, with the CAD figures 24 / 46 / 66 / 89 hidden, a 30-day trial, and the FAQ line "starting as low as $19/month USD". |
| 2 | Follow Up Boss trial + extra users (474), queued 10-12 | ✅ **DONE 2026-10-13** (undo `backups/474-20261013-180137.json`). The live page reads "14-day free trial, no contract, cancel anytime" and "Extra users: Grow is priced per user · Pro $49/month ($41 annual) · Platform $20/month ($17 annual)". The official page still says "14-day free trial, easy migration, no contracts" and shows the same prices. |
| 3 | Sprout stale figure on **post 572 `/photography-contract-template/`** (Junia page, no upgrade file) | ❌ **Still live.** The page reads "Sprout Studio: contracts included; plans from $24/month (pricing)". Exact edit: `plans from $24/month` → `plans from $19/month` (`knowledge/junia-572-photography-contract-template.md` L225). It needs a `--replace-content` or an editor fix; the parent decides. |
| 4 | Sprout "$24" in briefs and drafts | ❌ Still open: `knowledge/briefs/junia/photography-contract-template.md` L64 and L81, `knowledge/briefs/junia/photography-client-questionnaire.md` L62, and `knowledge/honeybook-alternatives-2026.md` L47, L58 and L243 (unpublished draft; L243 "Lite: $24/month" → $19). `knowledge/community-week3-drafts.md` no longer contains "$24". Fix these before the files are used. |
| 5 | WORDING: Clio "billed yearly" (397) | ❌ Still live: "…PracticePanther from $49 and MyCase from $50, each billed yearly (checked October 2, 2026)". It was not edited because clio.com still blocks every fetch (curl, WebFetch and the reader proxy all get 403 / Cloudflare), so it can't be re-confirmed. Keep it batched with the next 397 edit. |
| 6 | Optional polish (487 HoneyBook card fees, Dubsado team users, VSCO source URL; 586 DocJacket; 412 TaxDome source) | Still open, unchanged. The official facts are the same as last week. HoneyBook: "Card fees start at 2.7% + 10¢", plus 2.9% + 25¢ in the table. Dubsado: "Enjoy 3 additional users for free", then "4–10 users: $25/mo". DocJacket Pro: $29 early-customer pricing, $49 standard, $275/year, covering 2 seats. **TaxDome is now readable through the reader proxy:** Essentials $800, Pro $1,000, Business $1,200 per seat per year with a 1-year commitment ($750/$950/$1,150 for 2 years, $700/$900/$1,100 for 3 years). Seasonal seats are $100/month (Pro) and $500 per 4-month term (Business). These match 412, so 412's Pricing-verified row could cite taxdome.com/pricing instead of Portico at the next 412 edit. VSCO's page is blocked today (403), so the source-URL fix can't be checked. Fold these into T1.7 (487). |
| 7 | Canopy Premium "COMING SOON" (412) | Unchanged: the label still sits right before the Premium card ($149). |

## 3. No change (official page matches file + live)

- **368 / 397 legal:**
  - MyCase: $50/$100/$130 per user per month annual, $60/$120/$150 monthly; 10-day trial; MyCase Accounting $39; extra 5,000 Discovery pages $30.
  - PracticePanther: $49/$69/$89/$114 annual, $59/$79/$99/$124 monthly; 7-day trial.
  - Smokeball, Lawmatics and Filevine: no public prices.
- **412 accounting:**
  - TaxDome: as in §2 item 6.
  - Karbon: Team $59 annual / $79 monthly, Business $89 / $99.
  - Canopy: $74/$109/$149 per user per month; Tax Resolution $50; Tax Workflow from $34; Close Automation $10; KBA $1.25.
  - Financial Cents: Solo $19, Team $49/$69, Scale $69/$89; Month-End Close $5 per client; 14-day trial, no card.
  - Pascal: Unlimited $45.
- **474 real estate CRM:**
  - Follow Up Boss: Grow $69/$58, calling $39/$33; Pro $499/$416, extra users $49/$41; Platform $1,000/$833, extra users $20/$17; 14-day trial.
  - Wise Agent: $49 / $42 annual / $499 a year; WiseSocial $69 / $59 / $699; 14-day trial.
  - Real Geeks: $399/month or $3,990/year, $500 setup; Social $299; Search/Seller $599; Geek AI $49; extra users $25 (2–10 users).
  - Lofty and BoldTrail: no public prices.
- **487 photographers:**
  - Sprout Studio: as in §2.
  - HoneyBook: $29/$49/$109 billed yearly, $59/$129 monthly; 30-day trial; 60-day money-back guarantee. Promotional banners (25–50% off) were ignored.
  - Dubsado: $335/$525 a year; extra brand $10/month; 21-day trial.
  - Pixieset Studio Manager: Plus $12/$15, Pro $18/$24.
  - Studio Ninja: USD $16/$27/$40 per month, $160/$270/$400 per year; 7-day trial. The $24/$36/$53 figures on that page are the AUD toggle.
  - Bloom: Starter $14, Standard $34, Plus $66 (each advertised at 50% off); 1.5% fee on Starter.
- **492 coaches:**
  - Paperbell: $97 per month, $970 per year (was $1,164), 30-day money-back guarantee (via WebFetch).
  - Simply.Coach: annual US$9/29/49/69, "Save upto 52%", 14-day trial.
  - Delenta: $29/$49/$79 per month, $229/$469/$699 per year.
  - HighLevel: $97/$297/$497 per month, $970/$2,970/$4,970 per year; Starter has 3 sub-accounts; 14-day trial.
  - HoneyBook: as above.
- **586 transaction management:**
  - Dotloop: Premium $34.99/month or $344/year; 10 free transactions (via reader proxy).
  - SkySlope: from $340.
  - Open to Close (now at opentoclose.com/v2/pricing): $99/$199/$399; extra users $69; "Free 30 Day Trial".
  - Paperless Pipeline: $69 … $715; 14-day trial, no card.
  - DocJacket: as in §2 item 6.
  - Wise Agent: as above.
- **601 honeybook-pricing:**
  - HoneyBook: all plan prices; ACH 1.5%; instant deposit 1%.
  - Dubsado, Pixieset and Studio Ninja: as above.
  - Bonsai: Basic $9/$15, Essentials $19/$25.
  - 17hats: $60/month or $600/year; 7-day trial.
- **603 marketing-agency CRM:**
  - HubSpot: Starter $7/$20; Pro $90/$100 + $1,500 onboarding; Enterprise $150 + $3,500 onboarding.
  - monday CRM: $12/$18, $17/$25, $28/$41; 14-day trial.
  - Zoho: Standard $14, Professional $23, Enterprise $40.
  - Copper: Basic $23/$29, Professional $59/$69, Business $99/$134 (via WebFetch).
  - Close: Solo $9/$19, Essentials $35/$49, Growth $99/$109, Scale $139/$149.
  - ActiveCampaign: $15/$49/$79/$145.
  - Productive: Essential $10/$12, Professional $25/$29; 14-day trial.
- **618 Pixieset review:** Studio Manager Free / $12 ($15) / $18 ($24). Gallery plans $8/$16/$24/$40 annual ($10/$20/$30/$50 monthly). HoneyBook, Studio Ninja and Dubsado as above.
- **647 clio-vs-mycase:** all MyCase figures match (see 368/397). Clio's prices are intentionally not quoted on the page.
- **651 follow-up-boss-vs-lofty:** all Follow Up Boss figures match (see 474). Lofty publishes no plan prices.
- **670 capsule-crm-review:** Free $0 (250 contacts, max 2 users); annual US$18/$36/$54 (via reader proxy); contact limits 30,000 / 60,000 / 120,000; 14-day trial, no card; toggle "Save up to 18%", FAQ "up to 15% discount".

## 4. Could not check (no change claimed)

- **Clio (368, 397, 647):** clio.com/pricing returns 403 / a Cloudflare challenge to curl, WebFetch and the reader proxy. Check it in a browser.
- **VSCO (487):** vsco.co/subscribe/plans returns 403 (Cloudflare) on every route, so the VSCO One $499.99/year figure is unconfirmed this week.
- **Prices loaded by JavaScript and not shown to any fetch:**
  - Capsule monthly prices ($22/$40/$60) and Ultimate ($72/$75) (670). Only the annual Starter, Growth and Advanced prices could be read.
  - HoneyBook Starter monthly price, $36 (487/492/601/618).
  - Simply.Coach month-to-month prices, $19/$39/$59/$89 (492).
  - Zoho CRM monthly prices and Ultimate (603).
  - The annual prices that could be read all match.
- **Minor details not found in today's page text:**
  - Copper Basic's 2,500-contact limit (603).
  - ActiveCampaign's 1,000-contact basis for its listed prices (603).
  - Productive's 3-seat minimum (603).
  - 17hats' $5/month per extra user (601).
  - Zoho's trial page now says "15-day free trial". 603 doesn't quote a Zoho trial length, so this needs no edit.
