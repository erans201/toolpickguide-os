# ✅ SEO & AI-SEARCH ADMIN CHECKLIST (WordPress Admin Tasks)

These need a logged-in WordPress admin, so the user does them. Tick each box when done.
Menu names below match current Rank Math. If a label differs slightly in your version, use Rank Math's settings search.

---

## 1. Author identity (E-E-A-T) · ~10 min
Today the schema names the author **`cezaris.joe`** (your login) with no profiles. Review sites are judged on *who* reviewed.

- [ ] **Users → Profile:** set First/Last name, then **Display name publicly as** → your real name (not `cezaris.joe`).
- [ ] **Biographical Info:** 2–3 sentences: your role, what software you've actually used/implemented, and for how long. Facts only.
- [ ] **Rank Math fields on the same profile page:** add your LinkedIn URL (and X, if any) under the social/"sameAs" fields.
- [ ] Profile picture (Gravatar or a local avatar plugin).
- [ ] Add a link to **`/about-software-reviews/`** (your methodology page) in the bio, e.g. "How we review software."

## 2. Organization profiles · ~5 min
The site's Organization schema has **no social profiles** today.

- [ ] **Rank Math → Titles & Meta → Local SEO:** confirm Organization name "Tool Pick Guide," logo set, and add social profile URLs (LinkedIn company page, X, etc.) in the additional profiles / sameAs field.
- [ ] **Rank Math → Titles & Meta → Social Meta:** Facebook page URL and Twitter/X username.

## 3. Bing + IndexNow (ChatGPT search / Copilot use Bing's index) · ~15 min
- [ ] Go to **bing.com/webmasters** → sign in → **Import from Google Search Console** (fastest), or add the site and verify.
- [ ] Submit `https://toolpickguide.com/sitemap_index.xml`.
- [ ] **Rank Math → Dashboard → Modules:** enable **Instant Indexing** (IndexNow). New and updated pages then ping Bing/Yandex automatically.

## 4. Duplicate FAQ schema on `/best-crm-for-law-firms/` · ~5 min
The live page declares **FAQPage twice**.

- [ ] Edit the post → look for **both** a Rank Math **FAQ block** in the content **and** an FAQ entry in **Rank Math → Schema** tab.
- [ ] Keep one (the FAQ block is simplest), delete the other, Update.
- [ ] Re-check in Google's Rich Results Test (search.google.com/test/rich-results): exactly one FAQPage.
- [ ] Spot-check the other live "best of" posts for the same issue.

## 5. Curate llms.txt · ~5 min
Today it starts with an empty description and ranks chairs/routers equal to your core reviews.

- [ ] **Rank Math → General Settings → llms.txt** (edit the file directly if it's static): paste the block below into the **additional content** field, and consider limiting auto-listed posts to the Reviews / CRM / Client Onboarding categories.

```text
> Tool Pick Guide publishes independent, commercial-intent software reviews for service businesses: law firms, accounting and CPA practices, agencies, real estate agents, photographers, and coaches. Every review ranks tools by the workflow problem they solve (client intake, document collection, portals, billing), with plan-by-plan pricing verified on vendor sites and dated on each page.

## Core buyer's guides
- [7 Best CRM for Law Firms](https://toolpickguide.com/best-crm-for-law-firms/): Legal CRMs ranked for intake, conflict checks, and retainer conversion.
- [Best Legal Case Management Software](https://toolpickguide.com/best-legal-case-management-software/): Case and matter management for solo to mid-size firms.
- [Best Practice Management for Accountants](https://toolpickguide.com/best-practice-management-accountants/): Practice management and client portals for CPA and tax firms.
- [Best Client Management Software for Coaches](https://toolpickguide.com/client-management-software-for-coaches/): Scheduling, packages, payments, and portals for coaches.
- [Best Client Management Software for Photographers](https://toolpickguide.com/client-management-software-for-photographers/): Booking, contracts, and galleries for photographers.
- [Best Client Tracking Software for Real Estate Agents](https://toolpickguide.com/best-client-management-software-real-estate/): Lead follow-up and transaction tools for agents.
- [Best Customer Onboarding Software](https://toolpickguide.com/best-customer-onboarding-software/): Onboarding platforms ranked by use case.
- [Best Free Client Management Software](https://toolpickguide.com/free-client-management-software/): Free plans compared with their real limits.

## Explainers
- [What Is Client Onboarding Software?](https://toolpickguide.com/client-onboarding-software/)
- [What Is Legal Practice Management Software?](https://toolpickguide.com/legal-practice-management-software/)
- [What Is Client Relationship Management Software?](https://toolpickguide.com/what-is-client-relationship-management-software/)

## About
- [How we review software](https://toolpickguide.com/about-software-reviews/)
- [Affiliate disclosure](https://toolpickguide.com/affiliate-disclosure/)
```

- [ ] Open `https://toolpickguide.com/llms.txt` afterwards and confirm the description line appears under the title.

---

## Already automated in the uploader (no action needed)
- Visible "Last updated · Pricing verified" line under each H1 (from the article's `Pricing verified` meta row).
- `rel="sponsored nofollow noopener"` on affiliate links (domains listed in the `Affiliate domains` meta row, or URLs with `?ref=`, `?via=`, `/go/`, etc.). Other external links get `rel="noopener"` and open in a new tab.
- Exactly one ItemList + one FAQPage per uploaded article; Rank Math supplies Article + BreadcrumbList.
