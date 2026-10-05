# Price watch 2026-10-05 (autopilot Weekly Review, shadow mode)

- **Scope:** every live BOFU page with a facts file in `knowledge/` (posts 368, 397, 412, 474, 487, 492, 586). Each vendor's official pricing page was fetched on 2026-10-05 and compared with the upgrade file **and** the live page (the two matched everywhere, so every difference below is live right now).
- **Nothing was changed on the site.** Price changes on live pages are Tier C: the local agent edits the upgrade file, dry-runs it, and the user runs the `--replace-live` command.

---

## 1. MUST FIX: Paperbell price rose (post 492, `/client-management-software-for-coaches/`)

**Official (https://paperbell.com/pricing/, 2026-10-05):** "$97/ month" · "$1164 $970 / year (2 Mo Free!)". 30-day money-back guarantee and "no transaction fees" unchanged. Confirmed twice (WebFetch + reader).

Edits in `knowledge/upgrade-492-client-management-software-for-coaches.md`:
- L42: `$57/month or $570/year.` → `$97/month or $970/year.`
- L106: `**Standard (monthly):** $57/month` → `**Standard (monthly):** $97/month`
- L107: `**Standard (annual):** $570/year (2 months free)` → `**Standard (annual):** $970/year (2 months free)`
- L113: `And at $57/month, it's not the cheapest option` → `And at $97/month, it's not the cheapest option`
- L269: `| Paperbell Standard (annual) | $570 |` → `| Paperbell Standard (annual) | $970 |` (move the row below HoneyBook so the cost table stays sorted; it now ties with GoHighLevel Starter at $970)
- L330: `in one plan at $57/month or $570/year.` → `in one plan at $97/month or $970/year.`
- Review any "best value / budget" wording around Paperbell.
- Update the `Pricing verified` row to `2026-10-05 …`.

## 2. MUST FIX: Simply.Coach prices are annual-billing prices (post 492)

**Official (https://simply.coach/pricing/, 2026-10-05):** annual billing Starter $9 / Essentials $29 / Growth $49 / Leap $69 per month "paid annually"; month-to-month $19 / $39 / $59 / $89. "Save upto 52% on our Annual plans!" 14-day trial, no card. Client caps 3 / 7 / 30 / unlimited (unchanged).

- L43: `From $9/month.` → `From $9/month billed annually ($19 month to month).`
- L137: `**Starter:** $9/month.` → `**Starter:** $9/month billed annually ($19 monthly).`
- L138: `**Essentials:** $29/month.` → `**Essentials:** $29/month billed annually ($39 monthly).`
- L139: `**Growth:** $49/month.` → `**Growth:** $49/month billed annually ($59 monthly).`
- L140: `**Leap:** $69/month.` → `**Leap:** $69/month billed annually ($89 monthly).`
- L141: `Annual billing advertises savings of "up to 52%" (exact annual prices not listed publicly)` → `Prices above are billed annually (Simply.Coach advertises savings of "up to 52%"); month-to-month is $19 / $39 / $59 / $89`
- L270: `| Simply.Coach Growth (monthly) | $588 |` → `| Simply.Coach Growth (annual) | $588 |`
- L333: `Simply.Coach starts at $9/month for 3 clients` → `Simply.Coach starts at $9/month (billed annually) for 3 clients`

**User command after the local agent edits + dry-runs (PowerShell, in the `saas` folder):**
```
python upload_draft.py knowledge/upgrade-492-client-management-software-for-coaches.md --upload --replace-live 492 --force-replace
```
Undo: `python upload_draft.py --restore backups/<the file it prints>.json`

---

## 3. SHOULD FIX: Follow Up Boss trial + extra users (post 474, `/best-client-management-software-real-estate/`)

**Official (https://www.followupboss.com/pricing, 2026-10-05):** "14-day free trial, easy migration, no contracts". Pro extra users $49/month ($41 annual); Platform extra users $20/month ($17 annual); Grow is "$69 month/per user".

- L93: `7-day free trial, no contract, cancel anytime` → `14-day free trial, no contract, cancel anytime`
- L102: `**Extra users:** $49/month on Grow and Pro ($41 annual on Pro)` → `**Extra users:** Grow is priced per user · Pro $49/month ($41 annual) · Platform $20/month ($17 annual)`

Fold into the T1.6 rewrite of 474 (due Oct 23), so there's one replace instead of two.

## 4. WORDING: Clio "billed yearly" (post 397, `/legal-practice-management-software/`)

**Official (https://www.clio.com/pricing/):** "Starting at $49/user"; no billing period stated.
- L292: `Clio from $49, PracticePanther from $49 and MyCase from $50, each billed yearly` → `Clio from $49, plus PracticePanther from $49 and MyCase from $50 billed yearly`
- L298: `such as PracticePanther's Solo plan and Clio's Starter plan, both from $49 per user per month billed yearly.` → `such as PracticePanther's Solo plan ($49 per user per month billed yearly) and Clio's Starter plan (from $49 per user per month).`

Low risk; batch it with the next 397 edit.

## 5. Optional polish
- **487 HoneyBook card fees:** HoneyBook's own page says both "2.7% + 10¢" (FAQ) and "2.9% + 25¢" (plan table). Safe wording: `cards from 2.7% + 10¢ (HoneyBook's plan table lists 2.9% + 25¢), ACH 1.5%`.
- **487 Dubsado team users:** `team users from $25/month` → `3 extra users free, then from $25/month (4–10 users)` (dubsado.com/pricing).
- **487 VSCO source link:** `vsco.co/workspace/pricing-plans` now 301-redirects to `https://www.vsco.co/subscribe/plans` (prices unchanged).
- **586 DocJacket:** short mentions say "Pro $49/month"; today's early-customer rate is $29 ($49 standard). The pricing section already says both.
- **412 TaxDome:** prices all match `taxdome.com/pricing` (now readable). The `Pricing verified` line can cite the official page (2026-10-05) instead of the third-party Portico breakdown.

## 6. Matches (no action)
Clio, MyCase, PracticePanther, Smokeball, Lawmatics, Filevine (368/397) · TaxDome, Karbon, Canopy, Financial Cents, Pascal (412) · Delenta, HoneyBook, GoHighLevel (492) · Wise Agent, Real Geeks, Lofty, BoldTrail (474) · SkySlope, Open to Close, Paperless Pipeline, DocJacket pricing section (586) · Sprout Studio, Dubsado, Pixieset, Studio Ninja, VSCO, Bloom (487).

## 7. Could not verify
- **Dotloop (586):** dotloop.com returns 403 to automated requests. Check https://www.dotloop.com/products/plans-pricing/ in a browser (page says Free 10 transactions; Premium $34.99/month or $344/year).
- **Canopy Premium (412):** a "COMING SOON" label sits near the Premium card; check visually before saying Premium is available.
- **HoneyBook Starter monthly (487):** loads via JavaScript; the coaches check read $36 from the page's price data.
