# 🤖 JUNIA RUNBOOK (browser agent · learned on the first live run, 2026-10-05)

Used by the browser agent (`AUTOMATION_PLAN.md` §2) in the user's Chrome, where Junia is logged in. One article per brief. Never publish.

## Before you start
- Chrome is started with `--disable-features=CalculateNativeWinOcclusion --disable-backgrounding-occluded-windows --disable-renderer-backgrounding` on the taskbar shortcut (user, 2026-10-05), so it keeps drawing pages while hidden. Tested: typing into Google works while the user is in the Claude app.
- Don't close tabs mid-run: closing a tab can drop the agent's tab group. Close them at the very end.
- Chrome must stay **visible** (not minimized, not fully covered). Windows Chrome stops drawing hidden windows, and screenshots then time out. If that happens, ask the user to put Chrome side by side with the Claude app (Windows key + Left arrow).
- If a tab freezes ("Script injection timed out" for minutes), open a **new tab** on the same workflow URL. Junia keeps the workflow state in the URL `…/workflows/seo-blog-post/<id>`.
- Source of every value: the brief's "JUNIA FIELD BY FIELD" section (`knowledge/briefs/junia/<slug>.md`).

## Step 1 · Add Details (`https://www.junia.ai/dashboard` → **AI Article Writer**)
1. **Main Keyword:** the focus keyword.
2. **Additional Keywords:** type each secondary keyword, press Enter after each.
3. **Headline:** the H1 exactly.
4. Language English, SERP location United States (defaults).
5. **Auto SEO Competitor Research: OFF** (click the switch; it should read "Manual Mode"). Leave Reference Articles empty.
6. Click **Next**.

## Step 2 · Settings
1. **Article Length → Custom**, then click the slider knob and press the Right arrow until it reads **2700 words** (each press = 10 words; from 1500, press 120 times).
2. Tick **Review & edit outline before generating**.
3. **Advanced Settings** (opens a dialog):
   - **Background/Context:** the brief's Background box (the whole thing, including the facts sheet). `form_input` works for this textarea.
   - **Writing Style:** the brief's Writing style box. `form_input` works.
   - **Include Feature Image: OFF** (Junia's generated images were AI art).
   - **Include In-Article Images: ON** (real stock photos; QA copies them into the Media Library and uses the first as the featured image).
   - **Include Meta Title & Description:** leave ON (QA overwrites it).
   - **Include FAQ: OFF** (the outline has our FAQ; this caused duplicate FAQs).
   - **Auto External Linking & References: ON** (user rule 2026-10-05; QA judges each site).
   - ⚠️ The switches only change with real **clicks**, not `form_input`. Click one switch at a time and zoom in to confirm, because the dialog scrolls between clicks.
   - Click **Close**.
4. Click **Generate Outline** (takes 1–3 minutes).

## Step 3 · Review and edit outline
- Junia builds its outline from the Background box, so it is usually close. Compare it with the brief's outline:
  - **Add a missing heading:** scroll to the end, click the purple **+**, click the heading field ("Enter heading text for this section"), type the heading, then click "Enter a talking point" and type one instruction for that section.
  - **Delete a heading:** expand it (chevron); the **trash** icon appears at its right. Delete generic "Conclusion" sections.
- Then click **Generate** (about 1–5 minutes).

## Step 4 · Send to WordPress as a DRAFT
1. On "Article generated", click **here** (opens the editor in a new tab).
2. Top right: **Publish** → in "Publish to", click **WordPress** (integration https://toolpickguide.com is already connected).
3. In the dialog: leave Post ID empty · category from the brief (e.g. Reviews) · Publish to: Posts.
4. ⚠️ **Mode defaults to "public". Change it to "draft"** and zoom in to confirm before clicking. Leave Publish Date empty and "Enable submit to indexer" OFF.
5. Click the dialog's **Publish** button. Success toast: "Successfully published to WordPress!" and a preview tab `?p=<ID>&preview=true` opens.
6. Verify it is not public: `curl -s -o /dev/null -w "%{http_code}" https://toolpickguide.com/wp-json/wp/v2/posts/<ID>` must return **401**. If it returns 200 (public), raise an ALERT at once and ask the user to switch it back to draft in WordPress.
7. Record the draft ID in `LOOP.md`, close the tabs.
- The cloud robot exports and QAs the draft the next morning (Tier B fixes or a corrected body).

## Known differences from the brief to expect (QA fixes these)
- Junia may add "Opening" and "Affiliate disclosure" as H2 headings.
- Junia's outline may skip the last few brief sections: always check for "vs …", "Who should use it", "Don't mess this up" and "FAQs".
