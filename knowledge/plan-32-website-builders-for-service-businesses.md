# 🛠️ Upgrade Plan · Post 32 · /website-builders-for-service-businesses/

- **Status:** ✅ Scope approved 2026-10-01 (`CONTENT_STRATEGY.md` → Web presence = **Maintain**, reframed as a CRM spoke). Still open: questions A and B below. Word-count trimming removed (the length rule applies only to new in-house articles).
- **Reframe (strategy):** "website builders for service businesses that **capture leads and feed your CRM**". For each builder, cover native forms/booking and the CRM connection (native, Zapier, or none). Add a section on connecting your website to your CRM, linking to the vertical CRM pages (hub).
- **Why this page:** Search Console (90 days to 2026-09-28) shows 241 impressions = 37% of all site impressions, avg position 73, 0 clicks. Source: `data/gsc-insights-2026-10-01.md`
- **Cannibalization check (2026-10-01):** sitemap (39 URLs) has no other website-builder page. Safe to upgrade in place. **URL/slug stays the same.**

---

## 📊 What Google already matches this page to (top queries)

| Query | Impr. | Avg pos |
|---|---|---|
| service business website | 28 | 79 |
| what is the best website builder for local service businesses? | 25 | 76 |
| best website builder for service business | 20 | **51** |
| professionals page builder services | 18 | 83 |
| custom page builder services | 17 | 79 |
| website builder for service business | 11 | 75 |
| best website builder for service based business | 10 | 62 |
| best website builder for professional services | 8 | **52** |

The best positions are on "best website builder for…" phrasing, and the H1 doesn't contain "best".

---

## 🔍 Audit findings (live page, read-only fetch 2026-10-01)

1. **Orphan page:** 0 internal links point to it (ONSITE_PLANS.md crawl table). This is likely the biggest reason it sits at position 73.
2. **H1 is missing the main keyword:** "Website Builders for Service Businesses (No Fluff)". The SEO title is fine ("Best Website Builders for Service Businesses (2026 Picks)").
3. **No verified pricing:** only generic ranges ("$10 to $40 per month"). There are no per-tool prices and no `**Source:**` lines, which breaks the Outbound links rule.
4. **8 off-topic outbound links:** Washington and Minnesota tax pages, an FTC surveillance-pricing press release, a Reddit thread, a random designer's portfolio, an asset-manager agency page, a Jotform help page and a local-SEO course. None of them support the claims they sit next to.
5. **Broken heading structure:** orphan H2s (Home page / Service pages / About page / Contact page) and H3s (Lead capture / Trust and proof / SEO basics / Operations) sit under the wrong parent sections. Two tables of contents render (in-content plus plugin).
6. **Generic FAQs:** questions like "What makes this website builder guide different from typical roundups?" don't match what people search. The real query "what is the best website builder for local service businesses?" (25 impressions) isn't answered directly anywhere.
7. **Content QA Standards violations:**
   - 3,971 words, over the 3,000 BOFU maximum. The "Best overall / Best for premium…" recap repeats the Quick decision guide.
   - Banned word: "seamless" ×1.
   - No affiliate disclosure and no FTC link.
8. **Featured image:** `image0-1.png` (old). Needs a text-free photo-style image under the image rule.

---

## ✅ Proposed changes

| # | Change | Detail |
|---|---|---|
| 1 | **H1 and keywords** | H1 → "Best Website Builders for Service Businesses (2026)". Focus keyword: *best website builder for service business*. Secondary: service business website · website builder for professional services · local service business website. |
| 2 | **Answer box at the top** | A 2–3 sentence direct answer to "best website builder for local service businesses", then a comparison table (tool · best for · starting price · booking · lead forms). |
| 3 | **Verified pricing** | A starting price for each tool, taken from the vendor's official pricing page, plus a `**Source:**` line and a "Pricing verified 2026-10-xx" date. Anything I can't verify gets left out, never guessed. |
| 4 | **Replace the 8 off-topic outbound links** | Use official docs (vendor help centers, Google Business Profile help, FTC endorsement guidance). Every URL is checked before it's added. |
| 5 | **Fix heading structure** | Add parent H2s: "Pages every service business site needs" and "Launch checklist". Remove the duplicate in-content TOC. |
| 6 | **New FAQs (5–6), shaped like real queries** | What's the best website builder for a local service business? · Wix or Squarespace for a service business? · Do I need WordPress for SEO? · How much does a service business website cost per month? · Can I take bookings and payments on my site? |
| 7 | **Remove repetition only** | Merge the duplicate recap into the Quick decision guide. Remove "seamless". No word-count target. |
| 8 | **Affiliate disclosure and FTC link** | Only if affiliate links exist. See question B. |
| 9 | **Internal links in (fixes the orphan)** | Add 4–5 links pointing to this page from: `/best-form-builders-for-lead-capture/`, `/client-onboarding-software/`, `/client-management-software-for-photographers/`, `/client-management-software-for-coaches/` and `/best-doc-signing-tools/`. These go through `link_injector.py` (IL-7), which the user runs. |
| 10 | **Internal links out** | Keep the form-builders link. Add links to doc-signing, the photographer and coach CRM pages, and client onboarding. |
| 11 | **Featured image** | A photo-style, text-free image (prompt added to `knowledge/briefs/image-prompts.md`), saved as `website-builders-for-service-businesses-photo.*`. |

---

## ❓ Decisions needed from the user

- **A. Tool lineup:**
  - Keep the current 7 (Wix, Squarespace, WordPress, Webflow, GoDaddy, Shopify, Google Sites)?
  - Or replace the weak-fit ones (Shopify, Google Sites) with builders aimed at service businesses?
- **B. Affiliate links:** do you have (or plan to join) affiliate programs for any of these builders? If yes, which ones?
  - Rankings never change because of payouts.

---

## ▶️ Workflow after approval
1. The agent verifies prices on the official pages, then writes `knowledge/upgrade-32-website-builders-for-service-businesses.md`.
2. The agent runs `python upload_draft.py knowledge/upgrade-32-website-builders-for-service-businesses.md --replace-live 32` as a **dry run** only.
3. **The user runs** the same command with the real flag. It creates a backup first, and `--restore` undoes it.
4. **The user runs** the IL-7 link injection (`link_injector.py`).
5. Re-pull GSC around 2026-11-01 and compare position and impressions for the queries above.
