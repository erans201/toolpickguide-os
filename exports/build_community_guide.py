from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from reportlab.pdfbase.pdfmetrics import registerFontFamily


INK = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#6B7280")
ACCENT = colors.HexColor("#2563EB")
SOFT = colors.HexColor("#EFF6FF")
WARN = colors.HexColor("#FEF3C7")
LINE = colors.HexColor("#D1D5DB")

S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=INK, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=11, leading=15, textColor=MUTED, spaceAfter=14),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=ACCENT, spaceBefore=14, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK, spaceAfter=5, alignment=TA_LEFT),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.8, leading=12, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8.8, leading=12, textColor=INK),
    "quote": ParagraphStyle("quote", fontName="Helvetica", fontSize=9.6, leading=14, textColor=INK, leftIndent=8, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=14, textColor=INK, leftIndent=14,
                             bulletIndent=3, spaceAfter=2),
}

S["h1"].keepWithNext = 1
S["h2"].keepWithNext = 1
story = []
P = lambda t, s="p": story.append(Paragraph(t, S[s]))  # noqa: E731


def bullets(items, mark="•"):
    for it in items:
        if mark == "☐":
            story.append(Paragraph(it, ParagraphStyle("chk", parent=S["bullet"], bulletFontName="Courier-Bold", bulletFontSize=9, leftIndent=24), bulletText="[ ]"))
        else:
            story.append(Paragraph(it, S["bullet"], bulletText=mark))
    story.append(Spacer(1, 4))


def box(rows, bg=SOFT):
    t = Table([[Paragraph(r, S["cell"])] for r in rows], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story.append(t)
    story.append(Spacer(1, 8))


def table(header, rows, widths):
    data = [[Paragraph(h, S["cellb"]) for h in header]] + [[Paragraph(c, S["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), SOFT), ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story.append(t)
    story.append(Spacer(1, 8))


def step(n, title):
    story.append(Paragraph(f"Step {n}: {title}", S["h1"]))


# ---------------- Cover ----------------
P("Reddit &amp; Quora Community Marketing", "title")
P("Step-by-step guide · ToolPickGuide.com · October 2026 · the “Authority Bridge” method", "sub")

box(["<b>What this is:</b> a practical guide for posting genuinely helpful answers on Reddit and Quora, so the "
     "people choosing software (lawyers, real estate agents, photographers and other service businesses) "
     "start to trust ToolPickGuide, and so Google's AI answers, which often quote Reddit, start to notice us.",
     "<b>Who does what:</b> the agent finds threads and drafts replies every week. <b>You review and post them from "
     "your own accounts.</b> The agent never posts, votes, or creates accounts."])

P("Why now", "h2")
bullets(["Google showed an AI answer on 13 of our 15 biggest target searches, and ToolPickGuide was quoted in 0 of them.",
         "Reddit ranks #2–3 on most of the commercial searches we checked. Buyers add “reddit” to their searches because they trust real people more than listicles.",
         "Today 0 visits come from Reddit or Quora, so every visit from here on is measurable progress."])

P("The three rules that never bend", "h2")
table(["Rule", "What it means in practice"],
      [["1. You post", "Only from your own, real accounts. No second accounts, no asking friends to upvote."],
       ["2. Always disclose", "Any time you mention or link ToolPickGuide, say so plainly: “I run ToolPickGuide.” Never pose as a customer or a neutral bystander."],
       ["3. Help first (80/20)", "At least 4 of every 5 replies carry <b>no link at all</b>. The answer must be complete without clicking anything."]],
      [40, 130])

# ---------------- Steps ----------------
step(1, "Set up your profiles (week 1, about 20 minutes)")
bullets(["<b>Reddit:</b> pick a plain, real-sounding username (not “ToolPickGuide_Official”). In your profile bio write: "
         "<i>“I write software comparisons for service businesses at ToolPickGuide.”</i>",
         "<b>Quora:</b> add a profile credential such as <i>“Writes software comparisons at ToolPickGuide”</i>, and add the topics "
         "Legal Practice Management, Real Estate Agents, CRM Software and Wedding Photography.",
         "Turn on notifications for replies to your answers, so you can respond to follow-up questions within a day."])

step(2, "Read each community's rules before your first post")
P("Every subreddit has its own rules, and many limit or ban self-promotion. Breaking them gets you removed, sometimes for good.")
bullets(["Where to look: the subreddit's <b>About</b> tab (rules) and its <b>wiki</b> or pinned posts.",
         "Write down for each community: (a) are links allowed? (b) is self-promotion allowed, and how often? (c) is it open to everyone, or professionals only? (d) any required post flair?",
         "If links aren't allowed, you can still help there. Just never add a link."])
table(["Priority", "Vertical", "Where to start (check rules first)"],
      [["1", "Legal", "r/LawFirm · legal-ops threads in r/smallbusiness · Quora: “law firm software”, “Clio vs MyCase”"],
       ["2", "Real estate", "r/realtors · r/RealEstateTechnology · Quora: “best CRM for real estate agents”"],
       ["3", "Photographers", "r/WeddingPhotography · r/photobusiness · Quora: “HoneyBook vs Dubsado”, photography contracts"],
       ["—", "Cross-vertical", "r/smallbusiness · r/Entrepreneur · Quora: client intake, onboarding"]],
      [18, 32, 120])
P("Some professional subreddits are for members of that profession only. If you don't qualify, read and learn there, but don't post.", "small")

step(3, "Build a helpful history (week 1)")
P("Before any link, post <b>3–5 genuinely helpful replies with no link</b>. New accounts that start by dropping links get filtered or banned. "
  "A short history of good answers makes everything after it more credible.")

step(4, "Find good threads (the agent does this weekly; here's how)")
P("Google searches that surface real questions:")
table(["Search", "Finds"],
      [["site:reddit.com \"clio vs mycase\"", "Legal software decisions"],
       ["site:reddit.com best crm for realtors", "Real estate CRM questions"],
       ["site:reddit.com \"transaction coordinator\" software", "Contract-to-close workflow pain"],
       ["site:quora.com legal practice management software", "Legal questions on Quora"],
       ["site:reddit.com honeybook vs dubsado", "Photographer CRM decisions"]],
      [85, 85])
P("<b>A good thread is:</b> under about 30 days old · asked by someone in our audience · has real back-and-forth · not already fully answered. "
  "Skip threads where the best answer is already there. Adding a weaker one helps nobody.")

step(5, "Write the reply: answer first, then reasoning, then a next step")
table(["Part", "What to write", "Length"],
      [["1. The answer", "Answer the exact question in the first 1–2 sentences.", "1–2 sentences"],
       ["2. The reasoning", "Why: what to choose based on their situation. Use a simple analogy if it helps.", "2–4 short paragraphs"],
       ["3. A next step", "Something they can do today, in any tool (a demo test, a checklist).", "1 short paragraph"],
       ["4. Disclosure", "Only if you mention or link ToolPickGuide: “(Disclosure: I run ToolPickGuide…)”", "1 line"]],
      [30, 110, 30])
bullets(["Short paragraphs (2–3 sentences). Write like a knowledgeable peer, not a brochure.",
         "Never use: delve, testament, furthermore, in conclusion, unlock, game-changer, seamless.",
         "Prices only from our verified facts sheets, always with “as of [month]”. Never say you “tested” a tool.",
         "No legal, tax or financial advice. Talk about software and workflow; send them to their bar, CPA or broker for rules."])

step(6, "Decide whether to add a link (the bridge)")
table(["Question", "If yes", "If no"],
      [["Does the community allow links?", "Continue", "No link"],
       ["Is the reply already complete without the link?", "Continue", "Fix the reply first"],
       ["Does one of our pages go deeper on <i>this exact question</i>?", "Continue", "No link"],
       ["Have 4 no-link replies come before this one?", "Add ONE link + disclosure", "No link this time"]],
      [90, 45, 35])
P("Which page to link:", "h2")
table(["Question is about…", "Link"],
      [["Choosing legal case / practice management software", "toolpickguide.com/best-legal-case-management-software/"],
       ["What legal practice management software is", "toolpickguide.com/legal-practice-management-software/"],
       ["Law firm intake / CRM", "toolpickguide.com/best-crm-for-law-firms/"],
       ["Real estate CRM", "toolpickguide.com/best-client-management-software-real-estate/"],
       ["Photographer CRM", "toolpickguide.com/client-management-software-for-photographers/"],
       ["Transaction management · intake form · photo contract", "Wait until those articles are published"]],
      [62, 108])

step(7, "Check before you post (QA checklist)")
bullets(["Answers the question completely without a click",
         "Disclosure present if ToolPickGuide is mentioned or linked",
         "At most one link, matched to the question, and allowed by the community",
         "Every price is verified and dated (“as of October 2026”)",
         "No “tested” claims, no legal or tax advice, no banned words",
         "Not a copy of an earlier reply. Always adapt the template"], mark="☐")

step(8, "Post, then stay in the conversation")
bullets(["Reply to follow-up questions within about a day. That's where most of the trust is built.",
         "If someone disagrees, thank them and add what's useful. Never argue or defend the site.",
         "If you got a fact wrong, edit the reply and say what you corrected.",
         "Don't delete replies that got downvoted. Learn from them instead."])

step(9, "Log every reply")
P("Add a row to the weekly queue in <b>COMMUNITY_MARKETING.md</b> (section 8): date, community, thread link, angle, link yes/no, and what happened (replies, upvotes). "
  "Or just tell the agent and it will log it.")

step(10, "Measure once a month")
bullets(["On the 1st of the month, run <b>python ga_pull.py --property 551985779</b>. The report shows visits from reddit.com and quora.com and which pages they landed on.",
         "Also note: which replies got responses or upvotes, and whether anyone mentioned ToolPickGuide without you.",
         "Keep the angles that worked, drop the rest, and set next month's targets with the agent."])

# ---------------- Calendar ----------------
P("Your October calendar", "h1")
table(["Week", "The agent prepares", "You do", "Goal"],
      [["1 · Oct 5–11", "Rules summary per community · 5 threads + draft replies (no links)", "Set up profiles · read rules · post 3–5 replies", "A helpful history"],
       ["2 · Oct 12–18", "6 threads + drafts, mostly legal · at most 1 with a link", "Post 4–6 replies", "1 disclosed link"],
       ["3 · Oct 19–25", "6 threads + drafts: real estate + photographers", "Post 4–6 replies", "1–2 disclosed links"],
       ["4 · Oct 26–Nov 1", "6 threads + drafts · monthly results", "Post 4–6 · run ga_pull.py on Nov 1", "Review and adjust"]],
      [27, 63, 50, 30])
P("<b>Monthly cap:</b> about 20 replies, at most 4 with a link. Quality beats volume every time.", "p")

# ---------------- Templates ----------------
P("Reply templates (always adapt, never paste as-is)", "h1")
P("Template 1: Legal software debate", "h2")
P("<i>Thread: “3-attorney firm choosing between Clio and MyCase. Which one and why?”</i>", "small")
for para in [
    "Honestly, both will run a small firm fine. The better question is what breaks first in <i>your</i> week.",
    "If it's intake and integrations, meaning you already use a bunch of tools and want them talking to each other, Clio tends to win. Its app ecosystem is the big draw.",
    "If it's adoption, meaning you need your paralegal and your least techy partner using it by Friday, MyCase usually gets there faster. The client portal is simple, and clients actually use it.",
    "Two things to do in either demo: make them walk through your real trust workflow (deposit › invoice › transfer › reconcile), and ask how you'd export everything if you ever leave. Those two answers tell you more than the feature list.",
    "Pricing changes a lot. As of October 2026, Clio's entry plan starts at $49/user/month and MyCase Basic at $50 billed yearly, but check their pricing pages. And run the trust-accounting side past your bar's rules, not just the vendor.",
    "(Disclosure: I write legal software comparisons at ToolPickGuide. I can link the side-by-side if it helps, but the demo test above matters more than which logo you pick.)"]:
    story.append(Paragraph(para, S["quote"]))
P("<b>Link, if allowed:</b> toolpickguide.com/best-legal-case-management-software/", "small")
story.append(Spacer(1, 8))

P("Template 2: Real estate workflow / CRM bottleneck", "h2")
P("<i>Thread: “My CRM is great for leads, but deals still fall apart between contract and close. What am I missing?”</i>", "small")
for para in [
    "You're probably asking your CRM to do a job it wasn't built for.",
    "A CRM is great at the <i>before</i> (leads, follow-up, nurture) and the <i>after</i> (past-client touches). The messy middle, from contract to keys, is transaction management: deadlines tied to the contract date, documents, signatures, and the broker's compliance file.",
    "The fix that works for most agents: keep the CRM for people, and run each deal from one checklist that keys every task off the contract date. Inspection, appraisal, financing, closing. When the date moves, the whole checklist moves.",
    "On tools: a lot of agents pair their CRM with something like Dotloop, which is free for your first 10 transactions. Others want it all in one place and use a CRM that includes transaction management. Wise Agent does both from $49/month as of October 2026. If you have a TC, ask what they already use. Don't make them switch for your sake.",
    "(Disclosure: I run ToolPickGuide and compared these tools in more depth. No link needed, though. The contract-date checklist is 80% of the fix.)"]:
    story.append(Paragraph(para, S["quote"]))
P("<b>Link, if allowed:</b> toolpickguide.com/best-client-management-software-real-estate/", "small")

# ---------------- Do / Don't ----------------
P("Quick do / don't", "h1")
table(["Do", "Don't"],
      [["Answer the question fully in the reply itself", "Post just a link, or “check out my article”"],
       ["Disclose every time ToolPickGuide comes up", "Pretend to be a customer or a neutral user"],
       ["Adapt each reply to the thread", "Paste the same reply in several threads"],
       ["Use dated, verified prices", "Guess prices or say you “tested” a tool"],
       ["Stay for follow-up questions", "Argue with critics or ask for upvotes"],
       ["Follow each community's rules", "Use a second account or post where links are banned"]],
      [85, 85])
box(["<b>Questions or stuck?</b> Tell the agent the thread link and what you want to say. It drafts the reply, checks it against "
     "this guide, and logs it. Source of truth for this plan: <b>COMMUNITY_MARKETING.md</b> in the vault."], WARN)


def footer(c, d):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(20 * mm, 12 * mm, "ToolPickGuide · Community marketing guide · October 2026")
    c.drawRightString(190 * mm, 12 * mm, f"Page {d.page}")
    c.restoreState()


out = r"C:\Users\User\Documents\saas\exports\community-marketing-guide-2026-10.pdf"
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                        title="Reddit & Quora Community Marketing: Step-by-Step Guide", author="ToolPickGuide", pageCompression=1)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
