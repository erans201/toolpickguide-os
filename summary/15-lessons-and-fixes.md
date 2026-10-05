# 🧰 15 · Lessons learned and fixes

| Problem | Fix |
|---|---|
| Hostinger's edge strips the login header, so uploads failed | mu-plugin `toolpickguide-auth-bridge.php` (must stay installed) |
| Rank Math redirects blocked by Hostinger's firewall | add the path to `wordpress/toolpickguide-redirects.php` and re-upload |
| Changes don't show on the live site | purge LiteSpeed **and** Hostinger's CDN (hPanel → Websites → Advanced → Cache Manager → Purge All), then LiteSpeed once more |
| The cloud robot can't send email directly (blocked) | it emails through the website plugin `toolpickguide-owner-mail.php` |
| Junia ignored a brief pasted into one box (601/603) | briefs are now filled field by field |
| Junia's publish mode defaults to **public** | always switch Mode to **draft**; then confirm the post's REST URL returns 401 (not public) |
| Junia duplicated the FAQ | Junia's own FAQ switch stays OFF |
| Junia hotlinked Unsplash photos | `junia_draft.py --apply` copies them into the Media Library |
| Chrome froze when hidden behind other windows | taskbar shortcut flags (`--disable-features=CalculateNativeWinOcclusion` and two others); keep Chrome visible |
| Typing long text froze Quora and Junia | insert the whole text at once |
| Closing a tab mid-run dropped the agent's tab group | close tabs only at the end |
| Connection resets while uploading | reads retry 3 times; writes never retry (no double changes) |
| Two pages competed for the same search (508/412, 509/492) | retired with 301 redirects; sitemap check before every new slug |
| Speed: jQuery + theme CSS blocked rendering | LiteSpeed Load JS Deferred, CSS Combine + Minify, jQuery deferred (score 85 → 93) |
| Featured AI images with garbled text on 601/603 | swapped for real photos with `media_fix.py --featured-media` |
| PartnerStack: some programs need the Network approval first; Zendesk isn't on PartnerStack anymore | Network applied; Zendesk emailed |
| Impact marketplace showed "Access is Denied" | the account is limited until the 8am application is approved |
| The agent's safety checks block some actions (auto-publishing, editing the Weekly routine, `--replace-live`, Quora Post clicks at times) | those stay your clicks; the agent never retries a blocked action |
