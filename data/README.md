# 📥 data/: Raw Data Inbox

Raw exports land here. Agents read these files and turn them into tasks, upgrade plans and Junia briefs. **Never put keys or passwords here.**

---

## Sources

| Source | How it gets here | Who runs it | Output files | Report |
|---|---|---|---|---|
| Google Search Console | `python gsc_pull.py` (API, read-only) | User | `gsc-<date>-{queries,pages,query_page}.csv` | `gsc-insights-<date>.md` |
| Google Analytics 4 | `python ga_pull.py` (API, read-only) | User | `ga-<date>-{landing,channels,sources,outbound}.csv` | `ga-insights-<date>.md` |
| Google Keyword Planner | Manual export, dropped here, then `python kp_ingest.py` | User exports, agent or user runs the ingest | `Keyword Stats *.csv` (raw) → `kp-<date>-keywords.csv` | `kp-insights-<date>.md` |
| Semrush / Ahrefs (if added later) | Manual CSV export dropped here | User | `semrush-*.csv` / `ahrefs-*.csv` | agent analysis |

**Cadence:** monthly (around the 1st): GSC and GA4 pulls. Quarterly: Keyword Planner refresh before the strategy review (`CONTENT_STRATEGY.md`).

**Processing rule:** every new file produces either Sheet tasks or an explicit "no action" note in `LOOP.md`. Keyword ideas only become briefs after the topic gate and a sitemap check.

---

## 🔑 Keyword Planner export: step by step

1. Go to ads.google.com → **Tools → Planning → Keyword Planner → Discover new keywords**.
2. Paste **one seed group** from the list below (up to 10 seeds per run).
3. **Location:** United States. **Language:** English. Leave the date range at the default (last 12 months).
4. Click **Get results**, then the **download icon (⬇) → Plan historical metrics / Keyword ideas → .csv**.
5. Save the file into this `data/` folder. The default name "Keyword Stats ….csv" is fine. Repeat for each seed group.
6. Run `python kp_ingest.py`. It reads every export here and writes the demand map.

---

## 🟦 Bing Webmaster Tools keyword API (active source, 2026-10-01)

The Google Ads account is suspended, so Keyword Planner is unavailable. `bing_kw_pull.py` uses Bing's free keyword research API instead:

1. Go to bing.com/webmasters and sign in. Choose **Import from Google Search Console**, then select toolpickguide.com.
2. **Settings (⚙️) → API Access → API Key → Generate**. Copy the key.
3. Add the line `BING_WMT_API_KEY=<the key>` to `.env` (in Notepad, like GA4_PROPERTY_ID). Don't paste it in the chat.
4. `python bing_kw_pull.py --check`, then `python bing_kw_pull.py`.

Volumes are Bing-only searches per month (US, English, last 3 full months). Google's are larger, but the ranking of topics is what matters for the strategy.

---

## 🟩 DataForSEO (paid, pay-per-request): Google volumes, competitor gaps, AI Overviews

`dfs_pull.py` covers what Bing can't: **Google** search volumes, **keyword gaps vs competitors** (`competitors.txt`), and **Google top 10 + AI Overview citations**.

1. Sign up at dataforseo.com and add a small balance (Billing).
2. Go to **app.dataforseo.com/api-access** and copy the **API login** and **API password**. These are not your website password.
3. Add two lines to `.env`: `DATAFORSEO_LOGIN=...` and `DATAFORSEO_PASSWORD=...`. Don't paste them in the chat.
4. `python dfs_pull.py --check` is free and shows your balance.
5. `python dfs_pull.py --volume --gap --serp`. The script prints the number of paid requests before it starts and the actual cost at the end.
   - Requests: 1 for volume, 1 per competitor, 1 per keyword in the SERP check (default 15).

Report: `dfs-insights-<date>.md`. Edit `competitors.txt` to change who gets compared.

---

## 🔌 Keyword Planner API (on hold: the Ads account is suspended)

`kp_pull.py` pulls the same data through the Google Ads API. It's a one-time setup, plus a wait for Google's approval:

1. **Manager account:** ads.google.com/home/tools/manager-accounts → create a free manager account, then link your existing Ads account to it.
2. **Developer token:** in the manager account → **Admin → API Center** → fill in the form (purpose: "keyword research for my own website") → copy the token. Then **apply for Basic access**. Until Google approves it (usually a few business days), the token only works on test accounts.
3. **Google Cloud** (same project as Search Console):
   - APIs & Services → Library → **Google Ads API** → Enable.
   - **OAuth consent screen:** External, add yourself as a test user. Set the publishing status to **In production**; in Testing mode the sign-in expires every 7 days.
   - **Credentials → Create credentials → OAuth client ID → Desktop app** → download the JSON and save it in `saas\` as **`ads-oauth-client.json`**.
4. `pip install google-ads google-auth-oauthlib`
5. `python kp_pull.py --auth`: paste the developer token and the two account IDs, then sign in through the browser.
   - Google may warn that the app is unverified. It's your own app: click **Advanced → Continue**.
6. `python kp_pull.py --check`, then `python kp_pull.py`. All 6 seed groups below are pulled and the demand map is written.

**Secrets:** `google-ads.yaml` and `ads-oauth-client.json`. Never attach them to a chat. `kp-config.json` only holds your account ID.

Without an active ad campaign, Keyword Planner shows **ranges** ("1K – 10K") instead of exact numbers. That's enough for choosing between clusters.

### Seed groups (Option B scope)

| # | Cluster | Seeds (paste as one run) |
|---|---|---|
| 1 | CRM core: Legal + Accounting | legal case management software, crm for law firms, legal practice management software, accounting practice management software, cpa client portal, tax practice management software |
| 2 | CRM core: Photographers + Coaches | crm for photographers, photography client management software, honeybook alternatives, crm for coaches, coaching client management software, client management software for consultants |
| 3 | CRM core: Real Estate + Agencies | crm for real estate agents, real estate transaction management software, agency client portal, crm for marketing agencies, client portal software |
| 4 | Lifecycle: intake and signing | client intake form, online form builder, e-signature software, document signing, client questionnaire, contract template |
| 5 | Lifecycle: onboarding, scheduling, billing | client onboarding software, client onboarding checklist, appointment scheduling software, online booking system, invoicing software for small business, proposal software |
| 6 | Web presence | website builder for small business, website builder for service business, website for consultants, website for photographers, best website builder for coaches |
