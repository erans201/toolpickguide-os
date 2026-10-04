# ⚙️ SETTINGS LOG: every WordPress plugin-setting change (and its undo)

Rules: `CLAUDE.md` → "Site settings". Local agent only, with the user present and logged in. One setting at a time, user OK in chat before each change, re-test after each change.
Allowed: LiteSpeed Cache and Rank Math settings. Never: themes, layouts, plugin install/delete, users, security/login, payments.

**Undo = set the setting back to the "Before" value, save, then purge the LiteSpeed cache.**

| Date | Screen (exact path) | Setting | Before | After | Re-test result | Status |
|---|---|---|---|---|---|---|
| 2026-10-03 | LiteSpeed Cache → Page Optimization (all tabs) | **Baseline snapshot, nothing changed** | CSS Minify OFF · CSS Combine OFF · UCSS OFF · Load CSS Async OFF · Font display OFF · JS Minify OFF · JS Combine OFF · **Load JS Deferred OFF** · HTML Minify OFF · DNS prefetch ctrl OFF · Remove query strings OFF · Google Fonts async OFF / remove OFF · Emoji remove OFF · Lazy Load Images OFF · iframe lazy OFF · LQIP OFF · Add missing sizes OFF · VPI OFF · Localize OFF · Guest optimization only ON | — | mobile lab 3/20 pass (data/psi-2026-10-03.csv) | reference |
| 2026-10-03 | LiteSpeed Cache → Page Optimization → JS Settings | Load JS Deferred | OFF | **Deferred** (default excludes kept: jquery.js, jquery.min.js, gtm.js, analytics.js) | Purged all. jquery-migrate now deferred. Mobile lab: client-onboarding 76→92 (LCP 4.18→3.30 s), law-firm CRM 80→93 (3.93→3.16 s), help-desk 76→79 (TBT 209→47 ms). 0 console errors (2 pages), health check 32/32 OK, page looks normal. `data/psi-2026-10-03-after-js-defer.csv` | ✅ kept |
| 2026-10-03/04 | LiteSpeed Cache → Page Optimization → CSS Settings | CSS Combine | OFF | **ON** (8 stylesheets → 2; merged file /wp-content/litespeed/css/…css loads 200) | Needed LSCache purge + Hostinger Cache Manager Purge All + a second LSCache page purge (LiteSpeed builds the merged file in the background; the first copies after a purge can still be unmerged). Mobile lab: client-onboarding 92→98 (LCP 3.30→2.25 s ✅ pass), help-desk 79→93 (4.1→3.14 s), law-firm CRM 93→93 (likely an unmerged copy). 0 console errors, phone screenshots OK (2 pages). `data/psi-2026-10-04-check-1617.csv` | ✅ kept |
