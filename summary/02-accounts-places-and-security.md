# 02 · Accounts, places and security

No passwords here, ever. They live only in `.env` on your PC and in the cloud environment "robot".

## Accounts (all business ones use eran@toolpickguide.com)
| Service | Used for |
|---|---|
| WordPress + Hostinger (hPanel) | the website, File Manager, cache |
| Mailbox eran@toolpickguide.com | robot updates go out; affiliate replies come in |
| cezaris.joe@gmail.com | where robot updates arrive |
| GitHub `erans201/toolpickguide-os` | the whole project, private |
| claude.ai/code (environment "robot") | the cloud robots |
| Search Console (`sc-domain:toolpickguide.com`), GA4 (`551985779`) | Google data |
| Bing Webmaster, DataForSEO (≤ $5/mo), PageSpeed | keyword and speed data |
| Junia.ai, Quora | articles; community answers |
| Impact, PartnerStack, FirstPromoter | affiliate programs |
| Google Ads | **suspended**: never open a new account |

## Where things live
- **Your PC:** `C:\Users\User\Documents\saas`. Rules `CLAUDE.md`, robot rules `AUTOPILOT.md`, tasks `TASKS.md`, diary `LOOP.md`, articles and briefs `knowledge\`, data `data\`, site plugins `wordpress\`, backups `backups\`.
- **Drive:** ToolPickGuide OS › Reports (robot reports) · Plans & Briefs · Strategy · Guides · Summary (these pages).
- **Sheet:** "ToolPickGuide PM Tracker", tab Tasks.
- **Site plugins (must stay installed):** auth-bridge (logins), redirects, owner-mail (robot email), archive-titles.

## Secret files: never share, attach or upload
`.env`, `gsc-key.json`, `google-ads.yaml`, `ads-oauth-client.json`. Never attach them to a chat (the + or @ button sends the whole file).

## If a secret leaks
- **WordPress password:** WP admin → Users → Profile → Application Passwords → Revoke → make a new one → update `.env`.
- **Google key:** Google Cloud → IAM & Admin → Service Accounts → gsc-reader → Keys → delete → create new.
- **Mailbox:** change the password in Hostinger → Emails; update `.env` and the robot environment.

## Nobody ever
Types passwords for you, creates accounts, solves captchas, enters payment or tax details, permanently deletes anything, or changes the theme, plugins, users or security settings.
