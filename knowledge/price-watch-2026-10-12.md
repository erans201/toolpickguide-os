# Price watch 2026-10-12 (autopilot Weekly Review, cloud)

- **Scope:** every live BOFU/price page with a facts file in `knowledge/`: upgrade files for posts 368, 397, 412, 474, 487, 492, plus the Junia pages with corrected bodies 586 (`/best-real-estate-transaction-management-software/`), 601 (`/honeybook-pricing/`), 603 (`/best-crm-for-marketing-agencies/`) and 618 (`/pixieset-studio-manager-review/`). Each vendor's official pricing page was fetched on 2026-10-12 (curl, WebFetch, or a reader proxy for JavaScript or bot-blocked pages) and compared with the file. Each live page was also fetched (public GET). Every dollar amount in every file also appears on the matching live page, and no live page has an amount the file lacks, so the differences below are live right now.
- **Nothing was changed on the site.** Price changes on pages with an upgrade file go to `knowledge/local-queue.md` for the local robot (dry run first, then `--replace-live`). Junia pages without an upgrade file are described here only; the parent decides.
- The cloud dry run of `upload_draft.py` could not run (no `PIL` in the cloud sandbox). The local robot runs the dry run before each queue row.

---

## 1. NEW, QUEUED: Sprout Studio USD prices dropped (post 487, `/client-management-software-for-photographers/`)

**Official (https://getsproutstudio.com/pricing/, 2026-10-12):** the USD toggle shows Lite **19**/month, Basic **36**/month, Pro **51**/month, Unlimited **69**/month. The hidden CAD figures are 24 / 46 / 66 / 89. Those are the numbers our page shows as USD. The page's FAQ also says: "starting as low as $19/month USD". Plan limits are unchanged: 10 / 20 / unlimited active shoots, 50 GB / 100 GB / 200 GB / unlimited storage. The 30-day trial (no card) is unchanged. A pop-up mentions a "14-day trial" and "20% off" a friend's coupon; the main pricing block still says 30 days, so we keep 30. I confirmed the change twice, from the raw HTML (`price-usd` vs `price-cad` elements) and with WebFetch.

Edits made in `knowledge/upgrade-487-client-management-software-for-photographers.md`:
- L18 `Pricing verified` → starts `2026-10-12 Sprout Studio (USD) re-checked on getsproutstudio.com/pricing; …`
- L43 `From $24/month.` → `From $19/month.`
- L54 comparison table `$24/mo` → `$19/mo`
- L124 `**Lite:** $24/month` → `$19/month`
- L125 `**Basic:** $46/month` → `$36/month`
- L126 `**Pro:** $66/month` → `$51/month`
- L127 `**Unlimited:** $89/month` → `$69/month`
- L128 Source line `(checked September 2026)` → `(checked October 12, 2026)`
- L131 `pushes you onto Pro ($66)` → `Pro ($51)`
- L294 year-one table `Sprout Studio Pro (monthly) | $792` → `$612`. It stays the last row, so the table is still sorted.

**Queue row added (TODO):** `python upload_draft.py knowledge/upgrade-487-client-management-software-for-photographers.md --upload --replace-live 487 --force-replace`

**Same stale figure elsewhere (not in this week's scope, not edited):**
- **Post 572 `/photography-contract-template/` (Junia page, no upgrade file):** the live page says "Sprout Studio: contracts included; plans from $24/month". Exact edit: `plans from $24/month` → `plans from $19/month` (`knowledge/junia-572-photography-contract-template.md` L225). This needs a `--replace-content` or an editor fix; the parent decides.
- These briefs still carry "from $24/month" in their facts sheets: `knowledge/briefs/junia/photography-contract-template.md` (L64, L81) and `knowledge/briefs/junia/photography-client-questionnaire.md` (L62).
- These files also carry "from $24/month": `knowledge/honeybook-alternatives-2026.md` (an unpublished draft, L47 and L58) and `knowledge/community-week3-drafts.md` L74 (a Quora draft). Fix both before use.

## 2. CARRIED OVER, NOW QUEUED: Follow Up Boss trial + extra users (post 474, `/best-client-management-software-real-estate/`)

**Last week:** SHOULD FIX, folded into the T1.6 rewrite (due Oct 23). **Today:** still wrong on the live page ("7-day free trial, no contract, cancel anytime"; "Extra users: $49/month on Grow and Pro ($41 annual on Pro)").

**Official (https://www.followupboss.com/pricing, 2026-10-12):** "14-day free trial, easy migration, no contracts". Grow costs "$69 month/per user" ($58 billed annually); "Add calling for $39/user" monthly, $33 billed annually. Pro is $499/month for 10 users, "Additional users $49/month" ($41/month annual). Platform is $1000/month for 30 users, "Additional users $20/month" ($17/month annual). Today's new FUB brief (`knowledge/briefs/junia/follow-up-boss-vs-lofty.md`) independently records the same 14-day trial.

Edits made in `knowledge/upgrade-474-best-client-management-software-real-estate.md`:
- L18 `Pricing verified` → starts `2026-10-12 Follow Up Boss re-checked (followupboss.com/pricing: 14-day trial, extra-user prices); others 2026-09-28 …`
- L93 `7-day free trial, no contract, cancel anytime` → `14-day free trial, no contract, cancel anytime`
- L102 `**Extra users:** $49/month on Grow and Pro ($41 annual on Pro)` → `**Extra users:** Grow is priced per user · Pro $49/month ($41 annual) · Platform $20/month ($17 annual)`

**Queue row added (TODO):** `python upload_draft.py knowledge/upgrade-474-best-client-management-software-real-estate.md --upload --replace-live 474 --force-replace`. If the T1.6 rewrite ships first, it already contains these edits (it builds on this file), and the row can be closed with it.

---

## 3. Last week's items (2026-10-05 file)

| # | Item | Status 2026-10-12 |
|---|---|---|
| 1 | Paperbell $97 / $970 (492) | ✅ DONE since 10-06; live and official both still read "$97/ month" · "$1164 $970 / year". |
| 2 | **MUST FIX** Simply.Coach annual-billing labels (492) | ✅ **Live-fixed.** The live page reads "From $9/month billed annually ($19 month to month)", "Starter: $9/month billed annually ($19 monthly)", and has a "Simply.Coach Growth (annual)" table row. The official annual prices still read US$9 / 29 / 49 / 69, "Paid Annually", "Save upto 52%", with a 14-day trial. |
| 3 | SHOULD FIX FUB trial + extra users (474) | ❌ Still live and wrong → edited in the file and queued (§2). |
| 4 | WORDING: Clio "billed yearly" (397) | ❌ Still live: L249 "…each billed yearly" and L253 "…both from $49 per user per month billed yearly". Not edited: clio.com blocked every fetch today (403 / Cloudflare), so I couldn't re-confirm, and it's wording rather than a price change. Keep it batched with the next 397 edit (last week's exact replacements still apply). |
| 5 | Optional polish (487 HoneyBook card fees, Dubsado team users, VSCO source URL; 586 DocJacket; 412 TaxDome source) | Still open, unchanged. The official pages still show the same facts: HoneyBook "Card fees start at 2.7% + 10¢" plus "2.9% + 25¢" in the table. Dubsado "Enjoy 3 additional users for free", then "4–10 users: $25/mo". `vsco.co/workspace/pricing-plans` → `vsco.co/subscribe/plans` ($499.99 billed annually). DocJacket Pro is $29 early-customer pricing, $49 standard, $275/year. TaxDome is $800 / $1,000 / $1,200 per seat per year (1-year commitment). These can be folded into T1.7 (487, due Oct 23). |

---

## 4. No change (official page matches file + live)

- **368 / 397 legal:** MyCase $50/$100/$130 annual ($60/$120/$150 monthly), 10-day trial · PracticePanther $49/$69/$89/$114 annual ($59/$79/$99/$124 monthly), 7-day trial · Smokeball, Lawmatics, Filevine quote-only.
- **412 accounting:** TaxDome $800 / $1,000 / $1,200 per seat per year (2- and 3-year terms $50–$100 less), seasonal seats $100/month (Pro) and $500 per 4 months (Business) · Karbon $59/$89 annual, $79/$99 monthly · Canopy $74/$109/$149 billed annually, Tax Resolution $50, Tax Workflow from $34, Close Automation $10 (first 5 included), KBA $1.25 · Financial Cents Solo $19, Team $49/$69, Scale $69/$89, Month-End Close $5/client · Pascal Free (5 team members, 250 contacts), Unlimited $45 per team member per month.
- **474 real estate CRM:** Follow Up Boss prices (Grow $69/$58, Pro $499/$416, Platform $1,000/$833, calling $33 annual) · Wise Agent $49 / $42 annual / $499 a year; WiseSocial $69 / $59 / $699; add-ons $20 / $80 + $11 / $5; 14-day trial · Real Geeks $399/month (12-month) or $3,990/year, $500 setup, Social $299, Search/Seller $599, Geek AI Text $49 · Lofty and BoldTrail: no public prices.
- **487 photographers (except Sprout):** HoneyBook $29/$49/$109 billed yearly, $59/$129 monthly, 30-day trial, 60-day money-back guarantee · Dubsado $335/$525 a year, extra brand $10/month, 21-day Premier trial · Pixieset SM Plus $12 annual / $15 monthly, Pro $18 / $24 · Studio Ninja USD $16/$27/$40 per month, $160/$270/$400 per year, 7-day trial · VSCO One $499.99 billed annually · Bloom Starter $14, Standard $34 (now advertised at half price: $7 / $17 / $33), 1.5% fee on Starter, 7-day trial.
- **492 coaches:** Paperbell $97 / $970 · Simply.Coach annual US$9/29/49/69 · Delenta $29/$49/$79 monthly, $229/$469/$699 a year · HoneyBook (as above) · HighLevel $97/$297/$497 per month, $970/$2,970/$4,970 per year, Starter 3 sub-accounts.
- **586 transaction management:** Dotloop Premium $34.99/month or $344/year, 10 free transactions (read via reader proxy; last week this could not be verified) · SkySlope Suite from $340 · Open to Close Grow $99 / Pro $199 / Scale $399, extra users $69, "Free 30 Day Trial" · Paperless Pipeline $69/$140/$190/$240 … $715, 14-day trial, no card · DocJacket Free, Pro $29 early / $49 standard, $275 a year, Brokerage from $99 · Wise Agent (as above).
- **601 honeybook-pricing:** all HoneyBook plan prices, card fees, ACH 1.5%, instant deposit 1%, 30-day trial · Pixieset SM, Studio Ninja (as above) · Dubsado $35/$55 monthly, $335/$525 a year · Bonsai $9/$19 annual, $15/$25 monthly · 17hats $60/month or $600/year, 7-day trial.
- **603 marketing-agency CRM:** HubSpot Free · Starter $7 annual / $20 monthly · Pro $90/$100 + $1,500 onboarding · Enterprise $150 + $3,500 onboarding. monday CRM Basic $12/$18, Standard $17/$25, Pro $28/$41, from 3 users, 14-day trial. Zoho Standard $14, Professional $23, Enterprise $40 annual, free for 3 users. Copper Basic $23/$29, Professional $59/$69, Business $99/$134. Close Solo $9/$19, Essentials $35/$49, Growth $99/$109, Scale $139/$149, 14-day trial, no card. ActiveCampaign Starter $15, Plus $49, Pro $79, Enterprise $145 annual (1,000 contacts). Productive Essential $10 yearly / $12 monthly, Professional $25 / $29, 14-day trial.
- **618 Pixieset review:** Studio Manager Free / Plus $12 ($15) / Pro $18 ($24) · gallery plans up to Ultimate $40/month annual ($50 monthly) · HoneyBook, Studio Ninja, Dubsado (as above).

## 5. Could not verify (no change claimed)

- **Clio (368, 397):** clio.com/pricing returns 403 / a Cloudflare challenge to curl, WebFetch and the reader proxy. Check in a browser: "Starting at $49/user" last week.
- **Paperbell (492):** curl got 403, but WebFetch read the page fine (matches). Listed for completeness only.
- **Canopy Premium (412):** the "COMING SOON" label still sits right before the Premium card ($149). Check visually before calling Premium available.
- **Monthly prices loaded by JavaScript (annual prices match):** Simply.Coach month-to-month $19/$39/$59/$89 (492), HoneyBook Starter monthly $36 (487/492/601/618), Zoho CRM monthly $20/$35/$50 and Ultimate $52/$65 (603). Zoho's FAQ now describes Ultimate as "tailored for large-scale, bespoke deployments" with no price shown; check in a browser before the next 603 edit.
- **Minor details I couldn't find in today's page text:** Productive.io's 3-seat minimum (603) and 17hats' extra-user price, "$5/mo per extra user" (601). The page shows a $5/month add-on but not clearly for users.
