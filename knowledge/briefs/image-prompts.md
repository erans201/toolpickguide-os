# 🖼️ FEATURED IMAGE PROMPTS (for Junia or any AI image tool)

**User direction (2026-09-29):** photo-style AI images replace the generated illustrations. The no-text rule still applies.

## Rules for every image
- **Format:** landscape 16:9 (ideally 1200×630). Square images get cropped in social previews.
- **Paste this at the end of every prompt:**
  > no text, no letters, no numbers, no words on screens, no logos, no brand names, no watermarks, unbranded camera and devices
- **Reject and regenerate** if any readable text, logo, or misspelled brand name appears (e.g., "Canon", "Cangle"). AI tools often invent fake brand names on cameras and laptops.
- **Save as:** `knowledge/images/<article-file-stem>-photo.webp` (or `.jpg` / `.png`). The uploader automatically prefers a `-photo` file over the generated illustration.

---

## Live pages (swap with `--force-replace --refresh-image`)

| Post | Save as | Prompt |
|---|---|---|
| 412 Accountants | `upgrade-412-best-practice-management-accountants-photo.webp` | Editorial photo of a small accounting office during tax season: a tidy desk with a laptop showing abstract colorful charts, neat stacks of paper folders, a calculator, a coffee mug, and warm window light. Shallow depth of field, calm and organized mood, modern and professional. |
| 474 Real Estate | `upgrade-474-best-client-management-software-real-estate-photo.webp` | Editorial photo of a real estate agent's workspace: a laptop and a smartphone on a light wood desk beside a small model house and a set of house keys, a bright modern home interior softly blurred in the background, golden-hour light. Optimistic, professional mood. |
| 487 Photographers | `upgrade-487-client-management-software-for-photographers-photo.webp` | Editorial photo of a photographer's studio desk: an unbranded mirrorless camera, a laptop showing a grid of blurred photo thumbnails, printed proofs, and a notebook, warm natural window light. Creative, organized mood. |
| 492 Coaches | `upgrade-492-client-management-software-for-coaches-photo.webp` | Editorial photo of a coaching session in a bright modern office: two people seated across a small table, one taking notes in a notebook, a laptop open to a blurred calendar view, plants and soft daylight. Warm, trusting, professional mood. |

## WordPress drafts (set the featured image by hand in WP admin: they're drafts)

| Draft | Save as | Prompt |
|---|---|---|
| 554 HoneyBook alternatives | `honeybook-alternatives-2026-photo.webp` | Editorial photo of a creative freelancer at a sunlit desk comparing options: a laptop with blurred app windows side by side, a notebook with a hand-drawn comparison sketch (no readable words), a coffee cup, and plants. Thoughtful, decision-making mood. |
| 556 HoneyBook vs Dubsado | `honeybook-vs-dubsado-2026-photo.webp` | Editorial photo of two laptops side by side on a clean white desk, each showing a different blurred colorful dashboard, with a small plant between them and soft studio light. Balanced, symmetrical, head-to-head composition. |

## Junia draft 558 (Photography Client Questionnaire)
Junia's camera images show **"Canon"** and **"Cangle"**. Regenerate them, or replace them with:

| Use | Prompt |
|---|---|
| Featured image | Editorial photo of a photographer and a couple reviewing a printed questionnaire together at a bright café table, an unbranded camera resting beside them, candid and friendly mood, shallow depth of field. |
| In-content image | Overhead photo of a clipboard with a blank checklist form, a pen, an unbranded camera, and printed photo proofs on a warm wooden desk. |

## Junia brief: Client Intake Form Template (`/client-intake-form-template/`)
`junia_draft.py --apply` looks for `knowledge/images/junia-client-intake-form-template.png`. Save the photo there, or let it generate the text-free fallback.

| Use | Prompt |
|---|---|
| Featured image | Editorial photo of a small-business owner welcoming a new client at a bright, modern office desk: a tablet showing a blurred, empty form layout, a pen and a blank clipboard, two coffee cups, soft daylight. Friendly, organized, first-meeting mood. |

## Junia brief: Best Real Estate Transaction Management Software (`/best-real-estate-transaction-management-software/`)
Save as `knowledge/images/junia-best-real-estate-transaction-management-software.png`.

| Use | Prompt |
|---|---|
| Featured image | Editorial photo of a real estate transaction coordinator at a bright desk: a laptop showing a blurred checklist-style dashboard, a tablet with a blank signature field, a set of house keys and a small model house beside a neat folder, soft morning light. Organized, calm, closing-day mood. |
