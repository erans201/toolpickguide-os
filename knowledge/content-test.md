# Content test: Junia vs in-house (Claude) articles

User decision 2026-10-09: "generate 4 articles of your own each week that will compete Junia's, track them through Google Search Console and judge the results within a specific time frame." For this test only, the in-house writing ban (CLAUDE.md interpretation note, MANDATE.md Content Writer OFF-DUTY) is lifted for the **In-house** arm. MANDATE.md stays verbatim.

## Design

- **Two arms:** **J** = Junia writes (browser robot, as today). **C** = Claude writes in-house (daily cloud robot).
- **Volume:** 4 J + 4 C new articles per week. Publishing weeks: **Oct 12 – Nov 22, 2026** (6 weeks, 24 articles per arm).
- **Fair pairs:** every Monday the weekly robot picks 8 topics (sitemap check + topic gate as always), sorts them into 4 **pairs** of the same type (BOFU / MOFU / TOFU, price-heavy or not) and similar demand, and gives one article of each pair to each arm by coin flip (`python3 -c "import random; random.seed('<pair id>'); print(random.choice('JC'))"` gives the first topic's arm; the second topic gets the other). Pair IDs: `P<week>-<n>` (e.g. P1-1).
- **No competing articles (user rule 2026-10-09):** the two topics of a pair are different search intents, never two versions of one keyword. Every new brief must pass `python3 cannibal_check.py` (no STRONG match with a live page or any open brief, the other 7 of the week included); `publish_draft.py` blocks a STRONG match with a live page.
- **Same inputs:** both arms get the same brief format and facts sheet, target ~2,700 words, the same stock-photo rule, the same QA gate (`junia_draft.py`), the same publishing and indexing path. The brief's top table carries `| Test arm | J |` or `| Test arm | C |` and `| Test pair | P1-1 |`.
- **Daily caps for the test:** publish max 4/day, indexing max 5/day.

## How the C arm runs

1. **Tue + Fri, daily cloud robot:** writes the full article for each C brief with no article yet (2 per run) to `knowledge/articles/<slug>.md`: Publishing Meta table (every field CLAUDE.md lists, Status `test C, not for the scheduler`; never READY FOR UPLOAD), then the body following the brief, the QA rules and `brand-voice-sample.md`. Only facts-sheet numbers.
2. **Same evening 20:00, browser robot:** picks a free Unsplash stock photo for each new C article (`knowledge/images/<slug>-photo.jpg`), runs `python upload_draft.py knowledge/articles/<slug>.md` (dry run) then `--upload` (creates a **draft**), and adds the row to `knowledge/junia-runs.md` with arm C.
3. From there both arms follow the same path: morning QA by the daily cloud robot, publishing at 20:00 by `publish_draft.py`, indexing request.

## What is measured (per article)

**Reach (Search Console, `gsc_pull.py`):**

| Metric | Role |
|---|---|
| Impressions in the first 42 days | **primary reach score** |
| Clicks, average position at day 42 | secondary |
| Days from publish to first impression | secondary |

**User behavior (added by the user 2026-10-09: "judge articles also by user behavior, measured by heat map"):**

| Metric | Source | Role |
|---|---|---|
| Engagement rate (engaged sessions / sessions) | GA4, `ga_pull.py` landing report | **primary behavior score** |
| Average session duration | GA4 landing report | secondary |
| Outbound clicks per 100 sessions (vendor and affiliate links) | GA4 outbound report | secondary (closest signal to earnings) |
| Scroll depth, rage clicks, dead clicks, quick backs | Microsoft Clarity (`clarity_pull.py`, daily) | secondary |
| Heatmap review (where readers stop, what they click) | Clarity heatmaps, visual check | qualitative, at the interim and final look |

Behavior numbers only count with enough visits: a page needs **at least 30 sessions** by day 42 to enter the behavior comparison.

**Effort:** repairs before publishing (QA fixes, replaced bodies, failed gate runs), from the daily robot.

The weekly robot runs `python3 gsc_pull.py --days 90` and `python3 ga_pull.py --property 551985779 --days 90` and fills the snapshot columns below (cumulative since publish). D42 = the Monday snapshot closest to day 42 (within 3 days). Clarity numbers come from `data/clarity-daily.csv`, pulled daily by the local robot once the owner has installed Clarity.

## Time frame and verdict

- **Interim look:** Monday **Nov 23, 2026** (weekly report): early numbers plus a heatmap check of the busiest test pages, no decision.
- **Final verdict:** Monday **Jan 4, 2027** (all 48 articles have reached day 42). The weekly robot writes the verdict into the weekly report and `LOOP.md`; the owner decides.
- **Two scores per pair:** **reach** (D42 impressions) and **behavior** (D42 engagement rate; only pairs where both pages have 30+ sessions).
- **Winner rule:** an arm wins if it wins **reach** (beats the other in at least 15 of 24 pairs, or its median D42 impressions are at least 25% higher) **and does not lose behavior** (wins or ties the behavior pairs, or behavior has too little data). If one arm wins reach and the other wins behavior, the verdict is **split**: the report shows both, and outbound clicks per 100 sessions (closest to money) decide the recommendation. If neither wins reach: **tie**, broken by behavior, then by the cheaper, simpler arm (C: no Junia subscription, no browser clicks), then by repairs.
- **Caveat:** the site is young; low numbers on both arms are possible. If fewer than half of the articles have any impressions at D42, the verdict says "not enough data" and proposes a 4-week extension.

## Tracking table

| Pair | Arm | Slug | Post ID | Published | First impr. | Repairs | D14 impr. | D28 impr. | D42 impr. | D42 clicks | D42 pos. | D42 sessions | D42 engagement rate | D42 avg duration (s) | D42 outbound per 100 | D42 scroll depth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
