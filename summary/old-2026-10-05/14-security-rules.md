# 🔒 14 · Security rules

## Secret files: never share, attach, copy or upload
| File / place | Holds |
|---|---|
| `.env` (project folder) | WordPress app password, mailbox password, Bing, DataForSEO and PageSpeed keys |
| `gsc-key.json` | Google service-account key (Search Console + GA4) |
| `google-ads.yaml`, `ads-oauth-client.json` | Google Ads tokens (account suspended) |
| Cloud environment "robot" (claude.ai/code) | the robot's copies of the above |

- **Never attach them to a chat** (the + or @ button sends the whole file). If it happens, rotate (replace) that password or key right away.
- Never paste a password, key or token into chat, a Doc, an email or GitHub.
- GitHub ignores the secret files (`.gitignore`), and `git status` is checked before every commit.

## If a secret leaks
- **WordPress app password:** WP admin → Users → Profile → Application Passwords → **Revoke** → create a new one → update `.env` (and the robot environment if it was the cloud one).
- **Google key:** Google Cloud → IAM & Admin → Service Accounts → `gsc-reader` → Keys → delete the old one → create a new JSON key.
- **Mailbox password:** change it in Hostinger → Emails; update `.env` and the robot environment.

## The agent never
- Types passwords, creates accounts, solves captchas, or enters payment/tax details.
- Reads your mailbox beyond the affiliate senders listed in `knowledge/affiliate-senders.txt`.
- Sends an email for you without your "send" for that exact email (the robot's update to you is the one exception, and its recipient is fixed).
- Changes the theme, plugins, users, security or payment settings.
- Permanently deletes anything.

## Account-safety notes
- The robot's WordPress password is separate from yours (`tpg-cloud-autopilot`), so you can cut off the robot alone.
- The website email plugin only emails you, only for logged-in editors, at most 10 a day.
