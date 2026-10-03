# ⚙️ SETTINGS LOG: every WordPress plugin-setting change (and its undo)

Rules: `CLAUDE.md` → "Site settings". Local agent only, with the user present and logged in. One setting at a time, user OK in chat before each change, re-test after each change.
Allowed: LiteSpeed Cache and Rank Math settings. Never: themes, layouts, plugin install/delete, users, security/login, payments.

**Undo = set the setting back to the "Before" value, save, then purge the LiteSpeed cache.**

| Date | Screen (exact path) | Setting | Before | After | Re-test result | Status |
|---|---|---|---|---|---|---|
