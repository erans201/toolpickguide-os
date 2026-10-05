# 🛠️ ONSITE PLANS: Onsite Management Agent Database

Owner: **Onsite Management Agent**. Every entry passes the **QA gate** before it's marked done. Every WordPress change is staged as a dry run and **run by the user**.

- **Audit log:** dated findings from live crawls (read-only)
- **Internal link database:** who links to whom (article body links only)
- **Recommendations queue:** proposed fixes with status: `PROPOSED` → `APPROVED` → `STAGED` (dry run ready) → `APPLIED` (user ran it) → `VERIFIED` (agent checked live)

---

## 🔎 AUDIT LOG

| Date | Finding | Severity | Status | Next step |
|---|---|---|---|---|
| 2026-09-28 | Post **508** (`/best-accounting-practice-management-software/`) published by hand; duplicates 412 | 🔴 High | OPEN | User adds Rank Math 301 → `/best-practice-management-accountants/`, purges LiteSpeed + Hostinger caches; then `retire_post.py --redirect-already-set --apply` |
| 2026-09-28 | 4 live vertical pages outdated (LionDesk, Practice.do, Táve, 17hats/Pixifi picks) | 🔴 High | ✅ VERIFIED | Replaced: 412, 492, 487, 474 |
| 2026-09-28 | 6 category archives: no meta description, empty intro, ALL-CAPS names | 🟠 Medium | ✅ VERIFIED | Content + B1 renames applied 21:33 |
| 2026-09-28 | Category H1s read "Category X" | 🟡 Low | OPEN | User uploads `wordpress/toolpickguide-archive-titles.php` to mu-plugins |
| 2026-09-28 | `/best-crm-for-law-firms/` declares **FAQPage twice** | 🟠 Medium | OPEN | User removes one (see `wordpress/SEO-ADMIN-CHECKLIST.md` §4) |
| 2026-09-28 | Author schema = `cezaris.joe` (login name), no sameAs profiles | 🟠 Medium | OPEN | User completes checklist §1–2 |
| 2026-09-28 | `llms.txt` has an empty description; off-topic posts weighted equally | 🟡 Low | OPEN | User pastes curated block (checklist §5) |
| 2026-09-29 | Post 487 says Studio Ninja trial is **14 days**; official page says **7 days** | 🟠 Medium | ✅ VERIFIED (fixed live) | User runs `--replace-live 487 --force-replace` |
| 2026-09-29 | Breadcrumb home item reads **"No title"** on every post (Blocksy `ct-breadcrumbs`, source=default; front page has an empty title). Also exposed in BreadcrumbList microdata. Pages `/home/` (9) and `/home-page/` (276) both untitled; site tagline empty | 🟠 Medium | ✅ FIXED 2026-10-01 (Blocksy source → Rank Math; 22/25 verified; 3 stale LiteSpeed copies await Purge All) | User: title the front page "Home" (Settings → Reading) and/or switch Blocksy breadcrumbs source to Rank Math (enable RM breadcrumbs, label "Home") |
| 2026-10-01 | Post 558 `/photography-client-questionnaire/` published: QA fixes live, but featured image likely shows "Canon" (Junia), featured alt lacks keyword, 2 images hotlinked from images.unsplash.com | 🟠 Medium | OPEN | User: swap/verify image, set keyword alt, re-host Unsplash images in Media Library |
| 2026-09-29 | **Internal links:** 15 of 24 posts get **0 inbound** article links, incl. upgraded 412 and 474, and `/best-crm-for-law-firms/` | 🔴 High | 🟡 PARTLY FIXED (IL-1…4 live; home-office cluster pending IL-5) | See Recommendations IL-1 → IL-4 |

---

## 🔗 INTERNAL LINK DATABASE (re-crawled 2026-09-29 after IL-1…IL-4 · 24 published posts)

`out` = distinct internal articles linked from the body · `in` = articles linking to it

| ID | Slug | Type | out | in |
|---|---|---|---|---|
| 372 | client-onboarding-software | Explainer (hub) | 6 | 4 |
| 338 | crm-operations-best-client-management-software | BOFU (general CRM) | 5 | 3 |
| 358 | free-client-management-software | BOFU (budget) | 5 | 3 |
| 78 | best-doc-signing-tools | BOFU (e-sign) | 0 | 2 |
| 368 | best-legal-case-management-software | BOFU (legal pillar) | 3 | 5 |
| 397 | legal-practice-management-software | Explainer (legal) | 2 | 4 |
| 52 | best-form-builders-for-lead-capture | BOFU (forms) | 0 | 1 |
| 487 | client-management-software-for-photographers | BOFU (vertical, upgraded) | 4 | 6 |
| 492 | client-management-software-for-coaches | BOFU (vertical, upgraded) | 3 | 5 |
| 412 | best-practice-management-accountants | BOFU (vertical, upgraded) | 3 | 4 |
| 474 | best-client-management-software-real-estate | BOFU (vertical, upgraded) | 4 | 4 |
| 404 | best-crm-for-law-firms | BOFU (legal) | 3 | 6 |
| 384 | best-customer-onboarding-software | BOFU (onboarding) | 0 | **0** |
| 354 | what-is-client-relationship-management-software | Explainer (CRM) | 7 | **0** |
| 65 | help-desk-tools-for-tiny-teams-under-5 | BOFU (support) | 0 | **0** |
| 32 | website-builders-for-service-businesses | BOFU (web) | 0 | **0** |
| 85 | best-note-apps-for-research-consulting | Home office | 0 | **0** |
| 82 | cloud-storage-with-best-version-history | Home office | 0 | **0** |
| 87 | best-vpn-for-remote-work | Home office | 0 | **0** |
| 103 | best-wifi-router-for-home-office-dead-zones | Home office | 0 | **0** |
| 105 | best-budget-standing-desk-that-doesnt-wobble | Home office | 0 | **0** |
| 110 | best-office-chair-under-300 | Home office | 0 | **0** |
| 112 | best-monitor-for-spreadsheets | Home office | 0 | **0** |
| 508 | best-accounting-practice-management-software | 🔴 Duplicate (retire) | 2 | **0** |

**Re-crawl** after every link change and update this table.

---

## 📋 RECOMMENDATIONS QUEUE

| ID | Recommendation | Pages touched | Status |
|---|---|---|---|
| IL-1 | **Hub → vertical links.** Add a short "By industry" list linking the 4 vertical pages (412, 492, 487, 474) + `/best-crm-for-law-firms/` from the 3 strongest hubs: `/client-onboarding-software/`, `/crm-operations-best-client-management-software/`, `/free-client-management-software/` | 372, 338, 358 | ✅ VERIFIED live 2026-09-29 |
| IL-2 | **Legal cluster.** Cross-link `/best-crm-for-law-firms/` ↔ `/best-legal-case-management-software/` ↔ `/legal-practice-management-software/` (each links the other two) | 404, 368, 397 | ✅ VERIFIED live 2026-09-29 |
| IL-3 | **Vertical ↔ vertical.** Coaches (492) → Photographers (487) (shared HoneyBook/Dubsado); Accountants (412) → `/best-legal-case-management-software/` (professional-services intake) | 492, 412 | ✅ VERIFIED live 2026-09-29 |
| IL-4 | **Explainer → BOFU.** `/what-is-client-relationship-management-software/` links to all 4 vertical pages + law-firm CRM ("Pick by industry") | 354 | ✅ VERIFIED live 2026-09-29 |
| IL-6 | **Zero-inbound fix:** 78→372/384/487 · 52→354/32/372 · 384→65/78 · 65→354/384 · 32→52/354 | 78, 52, 384, 65, 32 | ✅ VERIFIED live (re-crawl 2026-10-02) |
| IL-5 | Home-office posts: decide keep/move/noindex before investing in links (tied to category proposal B3) | 7 posts | ✅ RESOLVED 2026-10-02: all 7 noindexed (CONTENT_STRATEGY Option B). No links needed |
| SP-1 | **Mobile speed (LCP).** 17/20 pages show the featured image at 3.5–4.3 s (target ≤ 2.5 s) because jQuery + theme CSS block rendering for ~1.6 s. LiteSpeed settings, one at a time: Load JS Deferred → CSS Minify + Combine → JS Minify → WebP. Keep Lazy Load OFF for the first image. Full steps: `TASKS.md` T1.16 | all | PROPOSED 2026-10-03: user changes settings, agent re-tests |
| IMG-1 | **Featured image with overlaid title text**: `/help-desk-tools-for-tiny-teams-under-5/`. Replace with a realistic photo (prompts: `knowledge/briefs/image-prompts.md`). `/best-form-builders-for-lead-capture/` (text on the monitor) is **OK since 2026-10-05**: text on items in the scene is allowed | 1 post | FOUND 2026-10-04: needs new images, then `media_fix.py` (user `--apply`) |
| IL-7 | **Contextual in-text links** (new tool `inject_links.py`): see the CONTEXTUAL LINK ROADMAP below | 354, 372, 358 (+ 487, 474 via upgrade files) | PROPOSED 2026-10-02: dry run, then the user runs `--upload` |

**How IL-1 → IL-4 will be applied:** upgrades use `--replace-live`, which needs a Markdown source file per post. Only the 4 vertical pages have one today. For 372/338/358/404/368/397/354, the Onsite Agent will stage a small, link-only edit tool (backup-first, dry run, user-run) before any change. **Built 2026-09-29:** `link_injector.py` + `wordpress/internal-link-plan.json` (backup-first, content-only writes, idempotent markers, refuses upgrade-file posts, `--restore`). Offline tests 6/6 passed.

---

## 🔗 CONTEXTUAL LINK ROADMAP (machine-readable · read by `inject_links.py`)

**Re-crawl 2026-10-02 (17 indexable posts; the 7 noindexed home-office posts are excluded).** The "15 orphan pages" figure from 2026-09-29 is outdated: IL-1→IL-6 fixed most of them. Today:
- **0 inbound:** 558 `/photography-client-questionnaire/`
- **1 inbound:** 65 `/help-desk-tools-for-tiny-teams-under-5/` (from 384) · 32 `/website-builders-for-service-businesses/` (from 52)

Rows were chosen only where the anchor phrase already appears naturally in the source text. Rejected false matches: "security questionnaires" (372, 384) → 558, "a website widget" (65) → 32, "free plan" (52, about a form builder) → 358.

`inject_links.py` processes rows with Status **TODO**. Statuses: TODO · DONE (verified live) · MANUAL (upgrade-file post: edit its Markdown, then `--replace-live`) · WAITING (target not published yet).

| ID | Source post | Anchor phrase | Target | Status |
|---|---|---|---|---|
| IL-7a | 354 | support tickets | /help-desk-tools-for-tiny-teams-under-5/ | DONE |
| IL-7b | 372 | customer onboarding | /best-customer-onboarding-software/ | DONE |
| IL-7c | 358 | your website | /website-builders-for-service-businesses/ | DONE |
| IL-7d | 487 | questionnaire | /photography-client-questionnaire/ | DONE |
| IL-8a | 487 | HoneyBook pricing | /honeybook-pricing/ | DONE |
| IL-8b | 492 | HoneyBook pricing | /honeybook-pricing/ | DONE |
| IL-8c | 338 | agencies | /best-crm-for-marketing-agencies/ | DONE |
| IL-8d | 372 | marketing agencies | /best-crm-for-marketing-agencies/ | DONE |
| IL-9a | 603 | Close | https://refer.close.com/f1y5ubxmzeo4 | TODO |
| IL-7e | 474 | transaction management | /best-real-estate-transaction-management-software/ | WAITING |

- **IL-7d (fixes the only orphan):** add the link in `knowledge/upgrade-487-…md`, then the user runs `python upload_draft.py knowledge/upgrade-487-client-management-software-for-photographers.md --upload --replace-live 487 --force-replace`. The intake-form article (draft 576) also links to 558 once published.
- **IL-7e:** after draft 586 is published, same route through `knowledge/upgrade-474-…md`.
