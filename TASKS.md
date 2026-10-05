# ✅ TASKS: exact instructions for GROWTH_PLAN.md

Every task lists who does it, its autopilot tier (`AUTOPILOT.md`), its due date, its exact steps, and how we know it's done.
Owner: **U** = user · **A** = agent (local session) · **AP** = cloud autopilot. Dates are 2026 unless noted.
The Sheet tab `Tasks` mirrors this list (ID in the Task column). Status changes are made there and in `LOOP.md`.

---

## PHASE 0: Infrastructure (Oct 3–11)

### T0.1 · Create the private GitHub repo · U · due Oct 4
1. Go to https://github.com/new (create a free GitHub account first if you don't have one).
2. Owner: your account. **Repository name:** `toolpickguide-os`. **Visibility: Private.**
3. Leave **all** "Initialize" options unchecked (no README, no .gitignore, no license).
4. Click **Create repository**, then copy the URL shown (`https://github.com/<you>/toolpickguide-os.git`) and send it to the agent.
- **Done when:** the agent has the URL.

### T0.2 · First push · A + U · due Oct 4 · needs T0.1
1. The agent runs `git remote add origin <URL>` and `git push -u origin main` in the vault.
2. A **Git Credential Manager** window opens. Choose **Sign in with your browser**, approve in GitHub, then return. This happens once.
3. The agent verifies on GitHub that the repo shows the vault files and **no** `.env`, `gsc-key.json` or `backups/`.
- **Done when:** the repo page lists the files, and a search for ".env" in the repo finds nothing.

### T0.3 · Connect GitHub to Claude · U · due Oct 5 · needs T0.2
1. Open https://claude.ai/code and choose **Connect GitHub** (or Settings → GitHub).
2. Install the **Claude GitHub app**. On the "Repository access" screen choose **Only select repositories** → `toolpickguide-os` → **Install**.
- **Done when:** `toolpickguide-os` appears in the repo picker at claude.ai/code.

### T0.4 · A separate WordPress password for the cloud · U · due Oct 5
1. WordPress admin → **Users → Profile** → scroll to **Application Passwords**.
2. New Application Password Name: `tpg-cloud-autopilot` → **Add New Application Password**.
3. Copy the password shown (spaces included). You'll paste it in T0.6, and only there.
- **Why separate:** if anything goes wrong you can revoke the cloud's access alone, without breaking your local tools.
- **Done when:** the password is pasted into the cloud environment (T0.6).

### T0.5 · A separate Google key for the cloud (+ rotate the leaked one) · U · due Oct 5 · ✅ DONE 2026-10-04 (leaked key deleted, user-confirmed; cloud Google key still postponed)
1. https://console.cloud.google.com → project **saas-website-project-510316** → **IAM & Admin → Service Accounts** → `gsc-reader`.
2. **Keys** tab: if key `6fe0ca43…` still exists (it was attached in chat on Oct 1), click its trash icon → **Delete**.
3. **Add key → Create new key → JSON → Create.** A file downloads. Open it in Notepad (don't attach it anywhere), select all, and copy. You'll paste it in T0.6.
4. Keep using your local `gsc-key.json` as before. If you deleted the key it came from in step 2, also save this new file as `saas\gsc-key.json`.
- **Done when:** the JSON is pasted into the cloud environment and `python gsc_pull.py --check` still works locally.

### T0.6 · Configure the cloud environment · U · due Oct 6 · needs T0.4, T0.5
1. https://claude.ai/code → **Environments** → **Default** → **Edit** (the screen may be labeled "Environment settings").
2. **Environment variables:** add one per line, exactly these names:
   - `WP_SITE_URL=https://toolpickguide.com`
   - `WP_USERNAME=<your WordPress login name>`
   - `WP_APPLICATION_PASSWORD=<password from T0.4>`
   - `GSC_KEY_JSON=<the whole JSON from T0.5, on one line>`
   - `GA4_PROPERTY_ID=551985779`
   - `BING_WMT_API_KEY=<your Bing key from .env>`
   - `DATAFORSEO_LOGIN=<from .env>` and `DATAFORSEO_PASSWORD=<from .env>`
   - `PAGESPEED_API_KEY=<from T0.11, add when ready>`
3. **Network access:** choose **Full**, or a custom allowlist with `toolpickguide.com`, `*.googleapis.com`, `oauth2.googleapis.com`, `ssl.bing.com`, `api.dataforseo.com`, `github.com`, plus vendor pricing domains (the weekly price watch needs them).
4. **Save.**
- **Done when:** the agent's test run (T0.8 step 3) reports "env OK" without printing any value.

### T0.7 · Make the tools cloud-ready · A · due Oct 6 · ✅ DONE 2026-10-03 (12 offline tests pass: `python -m unittest discover -s tests`)
1. `gsc_pull.py` and `ga_pull.py`: read the key from the `GSC_KEY_JSON` environment variable when the file is absent.
2. New `autopilot/guard.py`:
   - kill switch (`AUTOPILOT_PAUSED`)
   - daily caps and the monthly DataForSEO budget, both tracked in `autopilot/ledger.json`
   - used by `inject_links.py`, `junia_draft.py` and `dfs_pull.py` whenever `TPG_AUTOPILOT=1`
3. New `autopilot/healthcheck.py`: sitemap URLs return 200, robots tags unchanged (baseline file), and the sitemap count is recorded.
4. New `pagespeed_pull.py`: mobile Core Web Vitals for the top 20 URLs → `data/psi-<date>.csv`.
5. `set_robots.py`: support WordPress **pages** as well as posts (needed for T1.10).
6. Offline tests; commit; push.
- **Done when:** the tests pass and the commit is on GitHub.

### T0.8 · Create the cloud routines · A · due Oct 7 · needs T0.3, T0.6, T0.7 · ✅ created 2026-10-03 in SHADOW MODE (environment robot): Daily `trig_019Gyymnstw37fncEMdeLMkR` · Weekly `trig_01BSJ83tE327KXC11s7CssNR` · Monthly `trig_01VEzonPQmfYbkHM4AQMBbey` (claude.ai/code/routines). Shadow mode lives in each routine's prompt; the local agent removes it only after the user approves the practice-week digests.
1. Create **TPG Daily Ops** (`0 5 * * *`), **TPG Weekly Review** (`0 6 * * 1`) and **TPG Monthly Report** (`0 7 1 * *`) with the prompts in `AUTOPILOT.md` §5, the repo `toolpickguide-os`, and the Google Drive + Sheets connectors.
2. **Shadow week (Oct 7–13):** Tier B runs as **dry-run only**; the digest lists what *would* have been done.
3. **Run now** once and read the run log: env OK, health check OK, digest Doc created in Drive.
- **Done when:** 3 consecutive daily runs succeed (Oct 7–9) and the user has read the digests.

### T0.9 · Stop counting your own visits in GA4 · U · due Oct 6 · ✅ DONE 2026-10-04 (user-confirmed; check in the Nov 1 GA4 data)
1. Google search "what is my IP" → copy it.
2. GA4 → **Admin** → **Data streams** → your web stream → **Configure tag settings** → **Show more** → **Define internal traffic** → **Create** → Rule name `Me` → traffic_type value `internal` → **IP address · equals** → paste → **Create**.
3. GA4 → **Admin** → **Data settings → Data filters** → **Internal Traffic** → filter state **Active** → **Save**.
- **Done when:** the next monthly GA4 report no longer shows ~100 direct homepage sessions.

### T0.10 · Remove plain-text password files · U · due Oct 5 · ✅ DONE 2026-10-04 (files verified gone)
1. In `C:\Users\User\Documents\saas`, delete **`New Application Password.txt`** and **`.env.txt`**. Your `.env` already holds what the tools need.
2. If either file held a password you still use, revoke that WordPress application password (Users → Profile → Application Passwords → Revoke) and create a fresh one in `.env`.
- **Done when:** both files are gone. (Git already ignores them, so they never reached GitHub.)

### T0.11 · PageSpeed key + speed baseline · U then A · due Oct 8 · ✅ DONE 2026-10-03 (key in .env + robot env; baseline in GROWTH_PLAN §1; fix list in T1.16)
1. U: Google Cloud (same project) → **APIs & Services → Library** → "PageSpeed Insights API" → **Enable** → **Credentials → Create credentials → API key** → **Restrict key** → API restrictions: PageSpeed Insights API → **Save**. Add `PAGESPEED_API_KEY=<key>` to `.env` and to the cloud environment.
2. A: run `python pagespeed_pull.py` → write the CWV baseline into `GROWTH_PLAN.md` §1 and a fix list into `ONSITE_PLANS.md`.
- **Done when:** LCP/INP/CLS are recorded for the top 20 pages.

### T0.12 · Move the Drive folder · U · due Oct 5 · ✅ DONE 2026-10-03 (agent access verified)
1. Drive → **My Drive** → right-click **ToolPickGuide OS** → **Organize → Move** → choose your folder → **Move**.
- **Done when:** ToolPickGuide OS sits inside your folder. The agent keeps access.

---

## PHASE 1: Foundation (Oct 12 – Nov 30)

### T1.1 · Apply the two QA-corrected drafts · U · due Oct 12 · ✅ DONE (576 + 572 live with corrected text, verified 2026-10-04)
Run in PowerShell in `saas`:
```
python junia_draft.py --brief knowledge/briefs/junia/client-intake-form-template.md --post-id 576 --replace-content knowledge/junia-576-client-intake-form-template.md
python junia_draft.py --brief knowledge/briefs/junia/photography-contract-template.md --post-id 572 --replace-content knowledge/junia-572-photography-contract-template.md
```
- **Done when:** both print "✅ Draft … updated (still a draft)".

### T1.2 · Publish the 3 ready articles · U (Tier C) · due Oct 14 · needs T1.1 · ✅ DONE 2026-10-04 (586, 576, 572 live, index/follow)
1. WordPress → **Posts → Drafts** → open **586**, **576** and **572** one at a time.
2. In each: read it through, check the featured image has no readable text or logos, click **Save Draft** (Rank Math rescores), then **Publish**.
3. Search Console → **URL Inspection** → paste each new URL → **Request indexing**.
- **Done when:** all 3 load publicly and indexing is requested. Autopilot adds the IL-7e link (474 → transaction management) in the next upgrade (T1.6).

### T1.3 · Contextual links IL-7a–c · AP (Tier B) · due Oct 14
1. AP runs `python inject_links.py --upload` within the caps, verifies the 3 links live, and marks the roadmap rows **DONE**.
- **Done when:** the 3 links are live, and posts 65 and 32 each have ≥ 2 inbound links in the next crawl.

### T1.4 · Join affiliate programs · U · due Oct 20 · started 2026-10-04
**Status 2026-10-04: all 7 fitting programs applied.** Lawmatics, HoneyBook, Clio, Pixieset submitted; 8am/MyCase (Impact) In Review; Paperbell + Simply.Coach Pending. Skipped: Dubsado Ambassador (needs a Dubsado account and content). Not usable: TaxDome, PracticePanther, Canopy. **Next:** the agent checks `python mail_tool.py --inbox` each session, logs approvals and link formats in MEMORY.md, then adds links to pages (T1.11). User: Impact payment + tax (W-8BEN, individual) when prompted.
**Everything you need is in `knowledge/affiliate-applications.md`:** the verified list in order, paste-ready answers, and the Clio/MyCase email. Apply in this order:
1. Lawmatics: https://www.lawmatics.com/partners/affiliate
2. TaxDome: https://marketing.taxdome.com/ (pre-approved)
3. HoneyBook: https://forms.gle/L5XMJGtSKuQuns7FA
4. Paperbell: https://paperbell.com/affiliate-information/
5. Simply.Coach: https://simply.coach/affiliate-program/
6. Pixieset: https://affiliates.mypixieset.com/
7. Dubsado **Ambassador** (cash; the basic program only pays credit): https://www.dubsado.com/ambassador-program
8. Send the Clio and MyCase email (§4 of the kit).
- Dropped after verification 2026-10-04: PracticePanther (lead form only, no web link until Preferred Partner) and Canopy (customer-only link).
- Then paste each approved link (or its format) to the agent.
- **Done when:** 5+ programs are approved and their link formats are logged in MEMORY.md.

### T1.5 · Affiliate research sprint 3 · A · due Oct 16 · ✅ DONE 2026-10-04 (MEMORY.md Sprint 3: 8 joinable: Lofty, Sprout Studio, Studio Ninja, Jotform, HubSpot, Wix, Squarespace, PandaDoc; DocuSign via CJ 3P)
1. Research the programs (official pages first, third-party sources labeled 3P) for:
   - Dotloop, SkySlope, Open to Close, Paperless Pipeline, DocJacket, Wise Agent, Follow Up Boss, Lofty
   - Dubsado, Pixieset, Studio Ninja, Sprout Studio
   - Jotform, Wix, Squarespace
   - DocuSign, PandaDoc
2. Log them in MEMORY.md as Sprint 3 (same table format), and add the joinable ones to T1.4.
- **Done when:** the table is complete with verification levels.

### T1.6 · Upgrade 474 for "real estate CRM" (4,400/mo) · A → U · due Oct 23
1. A: re-verify the 5 tools' prices on their official pages.
2. A: rewrite `knowledge/upgrade-474-…md`:
   - Title/H1: "Best Real Estate CRM & Client Management Software (2026)"
   - "real estate crm" in the H1, first paragraph, one H2 and the meta description
   - IL-7e link to `/best-real-estate-transaction-management-software/`
   - an FAQ "CRM vs transaction management"
3. A: dry run; QA; commit.
4. U: `python upload_draft.py knowledge/upgrade-474-best-client-management-software-real-estate.md --upload --replace-live 474 --force-replace`
5. U: Search Console → URL Inspection → Request indexing.
- **Done when:** live, verified by the agent, and IL-7e marked DONE.

### T1.7 · 487: link the orphan + re-verify prices · A → U · due Oct 23
1. A: in `knowledge/upgrade-487-…md`, add a natural link to `/photography-client-questionnaire/` in the booking/questionnaire section.
2. A: re-verify the 6 tools' prices; update "Pricing verified"; dry run.
3. U: `python upload_draft.py knowledge/upgrade-487-client-management-software-for-photographers.md --upload --replace-live 487 --force-replace`
- **Done when:** 558 has ≥ 1 inbound link (IL-7d DONE) and the prices are dated this month.

### T1.8 · Upgrade 404 law-firm CRM (fixes the duplicate FAQ schema) · A → U · due Oct 30
1. A: export the live 404, then write `knowledge/upgrade-404-best-crm-for-law-firms.md`:
   - verified prices (Lawmatics, Clio Grow, MyCase, PracticePanther, etc.)
   - Source lines; one FAQ block
   - links to 397 and 368
   - "law firm crm" in the H1
2. A: dry run (the dry run must show exactly 1 FAQPage).
3. U: `python upload_draft.py knowledge/upgrade-404-best-crm-for-law-firms.md --upload --replace-live 404`
- **Done when:** the live page shows 1 FAQPage block and the agent has verified it.

### T1.9 · Upgrade 558 questionnaire for its variants (~600/mo) · A → U · due Nov 6
1. A: create `knowledge/upgrade-558-photography-client-questionnaire.md` from the live text. Add the variants ("photography questionnaire", "questionnaire for photography clients", "senior/wedding questionnaire" sections) and keep the 60 questions accurate.
2. U: `python upload_draft.py knowledge/upgrade-558-photography-client-questionnaire.md --upload --replace-live 558`
- **Done when:** live and verified.

### T1.10 · Fix the duplicate homepage `/home/` · A → U · due Oct 23 · needs T0.7 step 5
1. A: confirm page 9 `/home/` duplicates the front page and has no inbound links that matter.
2. U: `python set_robots.py --noindex-pages 9 --apply`
- **Done when:** `/home/` shows `noindex` and has left the sitemap.

### T1.11 · Add affiliate links + FTC disclosure to BOFU pages · A → U (Tier C) · rolling from Oct 21 · needs T1.4
1. A, for each approved program: add the link to every page that ranks the tool (rankings unchanged), add the domain to the page's `Affiliate domains` row, and add the FTC disclosure under the H1. Dry run.
2. U: run the printed `--replace-live … --force-replace` command per page.
- **Done when:** every BOFU page with an approved program has working, `sponsored nofollow`-tagged links.

### T1.12 · Track affiliate clicks as a GA4 key event · U · due Oct 22
1. GA4 → **Admin → Events**. Wait until the event `click` appears (it comes from enhanced measurement's outbound clicks).
2. Toggle **Mark as key event** on `click`.
- **Done when:** the monthly GA4 report shows key events from outbound clicks.

### T1.13 · Bing sitemap + IndexNow · U · due Oct 16
1. Bing Webmaster Tools → **Sitemaps → Submit sitemap** → `https://toolpickguide.com/sitemap_index.xml`.
2. WordPress → **Rank Math → Dashboard → Modules** → turn on **Instant Indexing**. Then **Rank Math → General Settings → Instant Indexing** → enable for **Posts** and **Pages** → **Save**.
- **Done when:** Bing shows the sitemap as Success, and new posts appear in the Instant Indexing history.

### T1.14 · Author identity + "How we evaluate" page · U + A (Tier C) · due Nov 6
1. U: send the agent your public author name (or an editorial team name), a 3–4 sentence bio of real relevant experience, and optionally a photo.
2. A: draft:
   - an Author/About section
   - a "How we evaluate software" page: pricing verified on vendor pages with dates, no hands-on claims unless real, how rankings are decided, the affiliate policy
3. U: approve. A: upload as **draft pages**. U: publish.
- **Done when:** both pages are live and linked from the footer/about page. (This is a site page, not an article; the user approved this exception on the task.)

### T1.15 · llms.txt · A → U · due Oct 30
1. A: write `wordpress/llms.txt` (site summary, key pages by vertical, editorial policy).
2. U: hPanel → **File Manager** → `public_html` → **Upload** → `llms.txt`.
3. A: verify https://toolpickguide.com/llms.txt returns 200.
- **Done when:** the file is live.

### T1.16 · Speed fixes from the CWV baseline · A with the user present (new settings rule 2026-10-03) · due Nov 13 · needs T0.11
**Progress 2026-10-04:** done: Load JS Deferred, CSS Combine, CSS Minify, jQuery removed from the defer-exclude list (all logged in `wordpress/SETTINGS-LOG.md`). Top-20 average 85→93 before the jQuery change; form-builders back to 98. Not done: JS Minify (tiny gain), WebP (needs a QUIC.cloud account: user), Lazy Load (keep OFF). Next measurement: Monthly Report Nov 1.
*User: log in to WP admin in the in-app browser once; the agent does the clicks, asks before each change and logs it in `wordpress/SETTINGS-LOG.md`.*
**Measured cause (2026-10-03, `data/psi-2026-10-03.csv`):** 17 of 20 pages miss mobile LCP (3.5–4.3 s lab; target ≤ 2.5 s). The LCP element is the in-article featured image (1024×1024). It is not lazy-loaded and downloads in ~0.5 s, but it waits ~1.6 s for render-blocking files: `jquery.min.js` + `jquery-migrate.min.js` (~750 ms) and Blocksy's `main.min.css` plus small CSS files (`related-posts`, `posts-nav`). Server response is fast (90–145 ms) and CLS is 0 everywhere. No real-user (CrUX) data exists yet, so for now this is about visitor experience more than ranking. Lab scores vary ±15 between runs, so re-test any page twice.
1. LiteSpeed Cache: change **one setting at a time**, purging the cache and re-testing in between. The agent re-runs `pagespeed_pull.py` and reports anything that breaks layout so the user can switch it back.
   - JS Settings → **Load JS Deferred: Deferred** (biggest expected win: removes jQuery from the render path). Then check that menus, the table of contents and FAQ toggles still work.
   - CSS Settings → **CSS Minify ON** and **CSS Combine ON** (merges the small Blocksy CSS files).
   - JS Settings → **JS Minify ON**
   - Image Optimization → **WebP Replacement ON** (after "Gather image data" + "Send optimization request").
   - **Leave Media → Lazy Load Images OFF** unless the first image is excluded: lazy-loading the featured image would make LCP worse.
   - Optional, later: Google's tag (`gtag.js`, ~180 KB) is the biggest file on every page. Delaying it would speed things up but loses visits from people who leave without interacting. Not recommended while traffic is this low.
- **Done when:** the top 20 pages pass mobile CWV, or the remaining failures are listed with a cause.

### T1.17 · Junia settings · U · due Oct 12
1. Junia article settings: turn **off** automatic external links, automatic internal links and images/stock photos.
2. Keep "Save as draft" on.
- **Done when:** the next Junia draft has no Unsplash images and no unlisted links (the QA gate confirms).

---

## CONTENT QUEUE (Phase 1–2, two briefs per week, written by the Weekly Review)

Every item: sitemap check + topic gate (`CONTENT_STRATEGY.md`) + facts verified the same week. Price-heavy items get a full facts sheet inside the paste box.

| # | Article | Google demand/mo | Type | Week |
|---|---|---|---|---|
| C1 | HoneyBook pricing (plans, fees, alternatives) | 1,600 | price-heavy BOFU (**brief ready 2026-10-05**: `knowledge/briefs/junia/honeybook-pricing.md`) | Oct 19 |
| C2 | Best CRM for marketing agencies | 1,390 | price-heavy BOFU (**brief ready 2026-10-05**: `knowledge/briefs/junia/best-crm-for-marketing-agencies.md`; Pipedrive left out, prices unverifiable) | Oct 19 |
| C3 | Service contract template (service businesses) | 2,400 | TOFU template | Oct 26 |
| C4 | Clio vs MyCase | 260 (CPC $107) | price-heavy MOFU | Oct 26 |
| C5 | Pixieset Studio Manager review | 320 | MOFU (brief ready) | Nov 2 |
| C6 | Law firm website design (spoke; must not target post 32's terms) | 2,400 | MOFU | Nov 2 |
| C7 | Client portal software for service businesses | 720 | BOFU | Nov 9 |
| C8 | Real estate CRM free options (links up to 474) | 90+ | BOFU | Nov 9 |
| C9 | Proposal template for service businesses | 4,400 (HIGH ads competition) | TOFU template | Nov 16 |
| C10 | Client onboarding checklist (must link up to 372; not target "client onboarding software") | 170 | TOFU | Nov 16 |

**Weekly cycle (exact):**
- **Mon 08:00:** AP writes 2 briefs and puts them in the Weekly Report.
- **Tue:** U pastes each brief box into Junia (drafts only).
- **Wed 07:00:** AP's Daily Ops exports the drafts, applies passing fixes (Tier B), and prepares corrected versions for failures (Tier C).
- **Thu:** U reviews and publishes (Tier C), then requests indexing.

---

## PHASE 2: Content velocity (Dec 2026 – Feb 2027)

### T2.1 · Keep the weekly cycle running · AP + U · weekly
- **Done when:** 2 articles are published per week (8/month) and none fails QA twice.

### T2.2 · Monthly price watch · AP · 1st of each month
- AP re-checks every price on live BOFU pages against official pages. Each change becomes a Tier C item with the exact edit and command.

### T2.3 · Community: 20 replies a month · U (dedicated chat) · weekly
- Use the separate Reddit/Quora chat session. AP fills the weekly thread queue in `COMMUNITY_MARKETING.md` §8.
- **Done when:** 20 replies a month, at most 4 with a link, each logged.

### T2.4 · Monthly link roadmap · AP · 1st of each month
- Re-crawl; add `IL-…` rows for any page with < 3 inbound links (natural anchors only); apply within the caps.

### T2.5 · Quarterly strategy review · AP + U · Jan 1, 2027
- Run the `CONTENT_STRATEGY.md` §1 process with fresh data. U approves the new cluster roles and queue.

---

## PHASE 3: Authority (Mar – May 2027)

### T3.1 · Linkable templates · A → U · Mar 2027
- Turn the intake form and contract templates into a downloadable PDF and a "make a copy" Google Doc, linked from their articles.

### T3.2 · Outreach list + email · A · Mar 2027
- 30 resource pages (state-bar practice-management pages, real-estate associations, photography associations) with a contact for each, plus a short, honest email template.

### T3.3 · Send outreach · U · 5 emails a week, Mar–May
- Send from your own email. Log replies in the Sheet. (The agent never sends.)

### T3.4 · Backlink tracking (free) · U → AP · monthly
- Search Console → **Links** → **Top linking sites** → **Export → CSV** → save to `data/gsc-links-<date>.csv` → AP adds it to the monthly report.

### T3.5 · Optional: YouTube walkthroughs · U · 1 a month
- AP writes a 3-minute script per BOFU page; U records the screen and uploads; AP embeds the video in the page (Tier C). Reason: YouTube is the most-cited source in AI Overviews (11 of 15).

### T3.6 · AI-answer formatting pass · A → U · Apr 2027
- Every BOFU page gets a 2–3 sentence answer box under the H1, a "best for" table and question-shaped H2s. Applied via upgrade files.

---

## PHASE 4: Scale and conversion (Jun – Sep 2027)

### T4.1 · Conversion pass on the top 10 earning pages · A → U
- Comparison table with a CTA button per tool, a "Top pick" box near the top, and the FTC disclosure kept.

### T4.2 · Earnings per page review · AP · monthly
- From the affiliate dashboards (U exports CSVs to `data/`) plus GA4 key events. Pages with traffic but low clicks get a conversion fix.

### T4.3 · Agencies cluster expansion · per the quarterly review
- If agencies demand holds: client portal for agencies, SuiteDash vs Assembly, etc.

### T4.4 · Annual refresh · Sep 2027
- Update the year in every title, re-verify all prices, re-rank tools.
