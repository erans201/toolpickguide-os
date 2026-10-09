# Content test: Junia vs in-house (Claude) articles

User decision 2026-10-09: "generate 4 articles of your own each week that will compete Junia's, track them through Google Search Console and judge the results within a specific time frame." For this test only, the in-house writing ban (CLAUDE.md interpretation note, MANDATE.md Content Writer OFF-DUTY) is lifted for the **In-house** arm. MANDATE.md stays verbatim.

## Design

- **Two arms:** **J** = Junia writes (browser robot, as today). **C** = Claude writes in-house (daily cloud robot).
- **Volume:** 4 J + 4 C new articles per week. Publishing weeks: **Oct 12 – Nov 22, 2026** (6 weeks, 24 articles per arm).
- **Fair pairs:** every Monday the weekly robot picks 8 topics (sitemap check + topic gate as always), sorts them into 4 **pairs** of the same type (BOFU / MOFU / TOFU, price-heavy or not) and similar demand, and gives one article of each pair to each arm by coin flip (`python3 -c "import random; random.seed('<pair id>'); print(random.choice('JC'))"` gives the first topic's arm; the second topic gets the other). Pair IDs: `P<week>-<n>` (e.g. P1-1).
- **Same inputs:** both arms get the same brief format and facts sheet, target ~2,700 words, the same stock-photo rule, the same QA gate (`junia_draft.py`), the same publishing and indexing path. The brief's top table carries `| Test arm | J |` or `| Test arm | C |` and `| Test pair | P1-1 |`.
- **Daily caps for the test:** publish max 4/day, indexing max 5/day.

## How the C arm runs

1. **Tue + Fri, daily cloud robot:** writes the full article for each C brief with no article yet (2 per run) to `knowledge/articles/<slug>.md`: Publishing Meta table (every field CLAUDE.md lists, Status `test C, not for the scheduler`; never READY FOR UPLOAD), then the body following the brief, the QA rules and `brand-voice-sample.md`. Only facts-sheet numbers.
2. **Same evening 20:00, browser robot:** picks a free Unsplash stock photo for each new C article (`knowledge/images/<slug>-photo.jpg`), runs `python upload_draft.py knowledge/articles/<slug>.md` (dry run) then `--upload` (creates a **draft**), and adds the row to `knowledge/junia-runs.md` with arm C.
3. From there both arms follow the same path: morning QA by the daily cloud robot, publishing at 20:00 by `publish_draft.py`, indexing request.

## What is measured (per article)

| Metric | Source | Role |
|---|---|---|
| Impressions in the first 42 days | Search Console (`gsc_pull.py`, pages CSV) | **primary** |
| Clicks, average position at day 42 | Search Console | secondary |
| Days from publish to first impression | Search Console | secondary |
| Repairs before publishing (QA fixes, replaced bodies, failed gate runs) | daily robot log | secondary (effort) |

The weekly robot runs `python3 gsc_pull.py --days 90` and fills the snapshot columns below (cumulative since publish; the 90-day window covers each article's whole life during the test). D42 = the Monday snapshot closest to day 42 (± 3 days).

## Time frame and verdict

- **Interim look:** Monday **Nov 23, 2026** (weekly report): early numbers only, no decision.
- **Final verdict:** Monday **Jan 4, 2027** (all 48 articles have reached day 42). The weekly robot writes the verdict into the weekly report and `LOOP.md`; the owner decides.
- **Winner rule:** an arm wins if it beats the other on primary impressions in **at least 15 of 24 pairs**, or its median D42 impressions are **at least 25% higher**. If both or neither rule applies with mixed direction: **tie**, and the cheaper, simpler arm is recommended (C: no Junia subscription, no browser clicks). Repairs break close calls.
- **Caveat:** the site is young; low numbers on both arms are possible. If fewer than half of the articles have any impressions at D42, the verdict says "not enough data" and proposes a 4-week extension.

## Tracking table

| Pair | Arm | Slug | Post ID | Published | First impr. | Repairs | D14 impr. | D28 impr. | D42 impr. | D42 clicks | D42 pos. |
|---|---|---|---|---|---|---|---|---|---|---|---|
