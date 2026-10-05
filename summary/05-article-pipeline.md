# ✍️ 05 · How an article goes from idea to live page

## The 8 steps

| # | Step | Who | Where |
|---|---|---|---|
| 1 | **Topic chosen** from the content queue; passes the topic gate and the "no competing page" sitemap check | Weekly robot | `TASKS.md` Content queue · `CONTENT_STRATEGY.md` · `VERTICAL_MATRIX.md` |
| 2 | **Brief written**, field by field, with a facts sheet (every price checked on the vendor's page that week) | Weekly robot | `knowledge/briefs/junia/<slug>.md` + a Doc in Drive › Plans & Briefs |
| 3 | **Junia generates** the article from the brief and saves it to WordPress as a **draft** | Browser agent (Tue/Fri) | your Chrome |
| 4 | **QA** checks every number against the facts sheet, SEO fields, links and images | Daily robot | `junia_draft.py --export-all` |
| 5 | **Fix:** passing drafts get `--apply`; failing drafts get a corrected text (`--replace-content`) | Daily robot | `knowledge/junia-<ID>-<slug>.md` |
| 6 | **Publish:** open the draft, Save Draft, read, Publish | **You** | WordPress → Posts → Drafts |
| 7 | **Index:** ask Google to index the new URL | Browser agent | Search Console |
| 8 | **Link:** add internal links to and from the new page | Robot (normal posts) / you (upgrade-file posts) | `ONSITE_PLANS.md` link roadmap |

## Junia settings that matter (exact)
- Competitor research **OFF** · length **Custom 2,700 words** · "Review & edit outline" **ON**
- Advanced: Background/Context = the brief's box (with the facts sheet) · Writing Style = the brief's box
- Feature image **ON**, in-article images **ON**, Junia FAQ **OFF** (our outline has the FAQ), auto external links **ON**
- **Publish to WordPress with Mode = "draft".** Junia's default is "public"!
- Never paste a whole brief into one box: Junia ignored it (drafts 601/603).

## Upgrading a page that's already live
- Done in-house (not Junia): the agent edits `knowledge/upgrade-<ID>-<slug>.md`, dry-runs it, and you run `--replace-live` (a backup is made first).
- Upgrade-file pages: 368, 397, 412, 474, 487, 492.

## Content queue (next topics)
| # | Topic | Searches/mo | Status |
|---|---|---|---|
| C1 | HoneyBook pricing | 1,600 | ✅ live (601) |
| C2 | Best CRM for marketing agencies | 1,390 | ✅ live (603) |
| C3 | Service contract template | 2,400 | queued |
| C4 | Clio vs MyCase | 260 (very high value) | queued |
| C5 | Pixieset Studio Manager review | 320 | draft 618, waiting QA/publish |
| C6 | Law firm website design | 2,400 | queued |
| C7 | Client portal software | 720 | queued |
| C8 | Free real estate CRM options | 90+ | queued |
| C9 | Proposal template | 4,400 | queued |
| C10 | Client onboarding checklist | 170 | queued |
