# 🗝️ 02 · Accounts, services and where things live

No passwords or keys are written here, ever. They live only in `.env` on your PC and in the cloud environment "robot".

## Accounts and services

| Service | What it's for | Account / ID | Notes |
|---|---|---|---|
| **WordPress** (toolpickguide.com/wp-admin) | the website | login name in `.env` | two application passwords: one for your PC tools, one (`tpg-cloud-autopilot`) for the robot |
| **Hostinger hPanel** (hpanel.hostinger.com) | hosting, File Manager, CDN cache | your Hostinger login | mu-plugins live in `public_html/wp-content/mu-plugins/` |
| **Business mailbox** | sends robot updates; affiliate replies arrive here | eran@toolpickguide.com (Hostinger mail) | the agent reads only allowlisted affiliate senders |
| **Your personal email** | receives the robot's updates | cezaris.joe@gmail.com | the only address the robot can email |
| **GitHub** | stores the whole project (private) | repo `erans201/toolpickguide-os` | the robot reads and writes it every run |
| **Claude (claude.ai/code)** | the robots | environment **robot** (`env_015sxhK8YZgCWnzJkTi8ghe1`) | routines at claude.ai/code/routines |
| **Google Search Console** | Google rankings and indexing | property `sc-domain:toolpickguide.com` (UI in Hebrew) | read by `gsc_pull.py` |
| **Google Analytics 4** | visitors | property `551985779` | your own visits are filtered out (since 2026-10-04) |
| **Google Cloud** | the API key for Search Console/GA4 | project `saas-website-project-510316`, service account `gsc-reader` | the old leaked key was deleted 2026-10-04 |
| **Google Ads** | keyword volumes | **suspended** (2026-10-01) | never open a new account to get around it |
| **Bing Webmaster Tools** | free keyword volumes | API key in `.env` | `bing_kw_pull.py` |
| **DataForSEO** | paid Google data | login in `.env` | robot may spend up to $5/month |
| **PageSpeed API** | speed tests | key in `.env` + robot | `pagespeed_pull.py` |
| **Junia.ai** | writes the articles | your Junia login (in Chrome) | saves to WordPress as **drafts** |
| **Quora** | community answers | your Quora account | credential "Founder at Tool Pick Guide (2026–present)" |
| **LinkedIn** | identity for affiliate forms | linkedin.com/in/eran-shalev | |
| **Affiliate networks** | Impact (8am/MyCase), PartnerStack (Close, Pipedrive, etc.), FirstPromoter (Paperbell, Simply.Coach) | all on eran@toolpickguide.com | payout/tax details: you only |

---

## Google Drive and Sheets
- **Drive folder "ToolPickGuide OS"** (`1fDbp-iy0hXXSEyeWX0FJYjpt83oI_hoU`), inside your own folder. Subfolders:
  - **Reports** (`1f7EORJ8raqezd7vl5yGBq9iAOv4JxWHX`): daily, weekly and monthly robot reports
  - **Plans & Briefs** (`1uBQANu4CHTtmQfDL9ttHZdSbTMF5zGuw`): Junia field sheets, Quora queues
  - **Strategy** (`1JWh7OtwlsbD8kCuCWzUTcFf-AyAH0Ezs`) · **Guides** (`1E7V4-GcFGoNuwHVLM816Y1nsjgrGX9wA`) · **Summary** (these files)
- **PM Tracker sheet:** "ToolPickGuide PM Tracker", tab `Tasks` (ID `1RQkHyvvl_yjJA7V4y9NiLKsAJJzhFrIrA5jMxbuaz6E`).
- The Drive connector only sees files it created itself, so keep robot files inside "ToolPickGuide OS".

---

## The project folder on your PC: `C:\Users\User\Documents\saas`

| Where | What |
|---|---|
| `CLAUDE.md` | the master rulebook every agent reads |
| `AUTOPILOT.md` | what the cloud robot may do alone |
| `AUTOMATION_PLAN.md` | the A-to-Z automation plan |
| `GROWTH_PLAN.md` · `TASKS.md` | goals and the exact task list |
| `LOOP.md` | the diary: one line per action, newest at the bottom |
| `MEMORY.md` | research: competitors, affiliate program details |
| `VERTICAL_MATRIX.md` | which page owns which keyword (no two pages compete) |
| `CONTENT_STRATEGY.md` | site scope and the "topic gate" every new idea passes |
| `ONSITE_PLANS.md` | audits and the internal-link roadmap |
| `COMMUNITY_MARKETING.md` | Quora/Reddit method and weekly queue |
| `knowledge/` | article files, Junia briefs (`briefs/junia/`), affiliate kit, runbooks, emails |
| `data/` | data pulls (Search Console, GA4, Bing, DataForSEO, PageSpeed) |
| `wordpress/` | site plugins (mu-plugins), settings log, category pages |
| `autopilot/` | robot safety code, health check, ledger, email sender |
| `backups/` | automatic backups before every live change (not in GitHub) |
| `summary/` | this folder |

## Site plugins we wrote (in `wordpress/`, uploaded to mu-plugins)
- `toolpickguide-auth-bridge.php`: makes logins work through Hostinger's edge. **Must stay installed.**
- `toolpickguide-redirects.php`: simple 301 redirects when Rank Math's can't be created.
- `toolpickguide-owner-mail.php`: lets the cloud robot email you (2026-10-05).
- `toolpickguide-archive-titles.php`: cleaner category titles.
