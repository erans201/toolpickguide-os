# 📊 INDEX: CONTENT PIPELINE DASHBOARD

## 🗂️ Article Tracker
| Article file | Vertical | Funnel | Target slug | Vault status | WP Post ID | Last updated |
|---|---|---|---|---|---|---|
| `knowledge/best-accounting-software-2026.md` | 🧾 Accounting | BOFU pillar | `/best-accounting-practice-management-software/` | ✅ RETIRED 2026-09-29: 301 → `/best-practice-management-accountants/`, post in Trash | 508 (trashed) | 2026-09-29 |
| `knowledge/best-coaching-software-2026.md` | 🎯 Coaches | BOFU pillar | (retired) | SUPERSEDED source for post 509 (retired) | 509 (trashed) | 2026-09-29 |
| `knowledge/upgrade-412-best-practice-management-accountants.md` | 🧾 Accounting | BOFU pillar | `/best-practice-management-accountants/` (LIVE) | ✅ LIVE UPGRADED 2026-09-28 19:49 + 19:52 (same content twice). ORIGINAL backup: backups/412-20260928-194902.json. Delete orphan media 515 | 412 (live) | 2026-09-28 |
| `knowledge/upgrade-492-client-management-software-for-coaches.md` | 🎯 Coaches | BOFU pillar | `/client-management-software-for-coaches/` (LIVE) | ✅ LIVE UPGRADED 2026-09-28 19:49 (backup: backups/492-20260928-194918.json). Add category CRM & Pipelines by hand | 492 (live) | 2026-09-28 |
| `knowledge/upgrade-487-client-management-software-for-photographers.md` | 📸 Photographers | BOFU pillar | `/client-management-software-for-photographers/` (LIVE) | ✅ LIVE UPGRADED 2026-09-28 20:57 (backup: backups/487-20260928-205721.json). Categories Reviews + CRM & Pipelines | 487 (live) | 2026-09-28 |
| `knowledge/upgrade-474-best-client-management-software-real-estate.md` | 🏠 Real Estate | BOFU pillar | `/best-client-management-software-real-estate/` (LIVE) | ✅ LIVE UPGRADED 2026-09-28 21:07 (backup: backups/474-20260928-210707.json). Re-run 21:4x blocked by double-run guard (no change) | 474 (live) | 2026-09-28 |
| `knowledge/upgrade-487-client-management-software-for-photographers.md` (v2) | 📸 Photographers | BOFU pillar | `/client-management-software-for-photographers/` (LIVE) | UPGRADE v2 READY: 6 tools (+Pixieset), matrix, free + wedding/RE sections, HoneyBook price fix | 487 (live) | 2026-09-29 |
| `knowledge/honeybook-alternatives-2026.md` | 📸 Photographers cluster | MOFU | `/honeybook-alternatives/` | WP DRAFT uploaded 2026-09-29 20:47 by scheduler (2,533 words, QA ✅). Awaiting user go-ahead for READY FOR UPLOAD | 554 (WP draft) | 2026-09-29 |
| `knowledge/honeybook-vs-dubsado-2026.md` | 📸 Photographers cluster | MOFU | `/honeybook-vs-dubsado/` | WP DRAFT uploaded 2026-09-29 20:47 by scheduler (2,514 words, QA ✅). Awaiting user go-ahead for READY FOR UPLOAD | 556 (WP draft) | 2026-09-29 |
| `knowledge/briefs/junia/photography-contract-template.md` | 📸 Photographers | TOFU | `/photography-contract-template/` | JUNIA WEEK 1: brief + facts sheet ready; image `junia-photography-contract-template.png` | n/a | 2026-09-29 |
| `knowledge/briefs/junia/photography-client-questionnaire.md` | 📸 Photographers | TOFU | `/photography-client-questionnaire/` | JUNIA WEEK 1: brief + facts sheet ready; image `junia-photography-client-questionnaire.png` | n/a | 2026-09-29 |
| `knowledge/briefs/junia/pixieset-studio-manager-review.md` | 📸 Photographers | MOFU | `/pixieset-studio-manager-review/` | JUNIA WEEK 1: brief + facts sheet ready; image `junia-pixieset-studio-manager-review.png` | n/a | 2026-09-29 |
| (WP post 509) `/best-crm-for-coaches/` | 🎯 Coaches | duplicate | `/best-crm-for-coaches/` | ✅ RETIRED 2026-09-29 22:00: 301 → `/client-management-software-for-coaches/` (via `toolpickguide-redirects.php`), post in Trash | 509 (trashed) | 2026-09-29 |

---

## 🔁 Lifecycles
Every change passes the **QA gate** before it's logged as done. Every WordPress write is **run by the user**.

| Workflow | Owner | Flow |
|---|---|---|
| **New article** (Content Writer, currently OFF-DUTY) | Onsite / PM | `DRAFT` → QA → `READY FOR UPLOAD` (user's go-ahead only) → WP draft (Post ID logged) → published by a human in WP admin |
| **Junia.ai article** | SEO (brief) → QA | Sitemap check → `knowledge/briefs/junia/<slug>.md` (prompt + facts sheet) → user pastes into Junia → Junia saves a WP **draft** → QA checks the draft against the facts sheet → user publishes → agent verifies live + adds internal links |
| **Live-page upgrade** | Onsite | `knowledge/upgrade-<ID>-<slug>.md` → QA + dry run → user runs `--replace-live <ID>` (auto backup) → agent verifies live → logged. Undo: `--restore backups/<ID>-<time>.json` |
| **Retire a duplicate** | Onsite | Dry run → user adds the 301 in Rank Math + purges caches → user runs `retire_post.py --redirect-already-set --apply` (verifies 301, backup, Trash) → agent verifies → logged |
| **Category content / renames** | Onsite | `wordpress/CATEGORY-PAGES.md` → QA + dry run → user runs `update_categories.py --apply` (auto backup) → agent verifies → logged. Undo: `--restore` |

---

## ⚙️ Upload Paths
- **Manual:** agent runs the dry run and hands over the command. User runs `python upload_draft.py <file> --upload` and pastes the output back.
- **Automated (user-owned):** Windows Task Scheduler runs `run_scheduler.bat` → `auto_scheduler.py` uploads any `READY FOR UPLOAD` article once. State: `upload_state.json`. Log: `logs/auto_scheduler.log`. Never used for published posts.

---

## 📤 Upload Log
*(Appended automatically by `auto_scheduler.py`, or by the agent after a manual run. Never edit rows by hand.)*

| Uploaded | Article | WP Post ID | WP status | Via |
|---|---|---|---|---|
| 2026-09-28 18:40 | `knowledge/best-accounting-software-2026.md` | 508 | draft | auto_scheduler |
| 2026-09-28 18:40 | `knowledge/best-coaching-software-2026.md` | 509 | draft | auto_scheduler |
| 2026-09-28 19:49 | `knowledge/upgrade-492-client-management-software-for-coaches.md` | 492 | publish (content replaced) | replace-live (user) |
| 2026-09-28 19:49 | `knowledge/upgrade-412-best-practice-management-accountants.md` | 412 | publish (content replaced; original backup 412-20260928-194902.json) | replace-live (user) |
| 2026-09-28 19:52 | `knowledge/upgrade-412-best-practice-management-accountants.md` | 412 | publish (same content re-applied; duplicate image 515 orphaned) | replace-live (user) |
| 2026-09-28 20:57 | `knowledge/upgrade-487-client-management-software-for-photographers.md` | 487 | publish (content replaced) | replace-live (user) |
| 2026-09-28 21:07 | `knowledge/upgrade-474-best-client-management-software-real-estate.md` | 474 | publish (content replaced) | replace-live (user) |
| 2026-09-29 (correction) | `knowledge/best-accounting-software-2026.md` | 508 | **publish**: published by hand in WP admin ~19:18 on 2026-09-28 (the 18:40 row above recorded the upload as draft); retire pending | manual (WP admin) |
| 2026-09-29 19:43 | `knowledge/upgrade-412-best-practice-management-accountants.md` | 412 | publish (force-replace: IL-3 links) | replace-live (user) |
| 2026-09-29 19:43 | `knowledge/upgrade-492-client-management-software-for-coaches.md` | 492 | publish (force-replace: IL-3 links) | replace-live (user) |
| 2026-09-29 19:43 | `knowledge/upgrade-487-client-management-software-for-photographers.md` | 487 | publish (force-replace: Studio Ninja 7-day trial + annual prices) | replace-live (user) |
| 2026-09-29 20:47 | `knowledge/honeybook-alternatives-2026.md` | 554 | draft | auto_scheduler |
| 2026-09-29 20:47 | `knowledge/honeybook-vs-dubsado-2026.md` | 556 | draft | auto_scheduler |
| (WP draft 217, pre-existing) | 📸 Photographers cluster | MOFU | unknown slug | ⚠️ OLD draft "Dubsado vs HoneyBook: The Honest Comparison for Creative Studios": same intent as draft 556. **Never publish both.** User decides: keep 556, trash 217 | 217 (WP draft) | 2026-09-29 |
