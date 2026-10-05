"""
upload_draft.py: push a ToolPickGuide Markdown article to WordPress as a DRAFT,
with Rank Math SEO fields, tags, category, featured image, and schema.

Default mode is a DRY RUN: it parses the file, compiles HTML, generates the
featured image, writes a local preview, and prints everything it would send.
Nothing is sent to WordPress.

    python upload_draft.py <article.md>                          # dry run
    python upload_draft.py <article.md> --upload                 # create a new WordPress draft
    python upload_draft.py <article.md> --upload --post-id 508 --expect-modified 2026-09-28T15:40:23
                                                                 # update an existing DRAFT
    python upload_draft.py --check-auth                          # read-only login test (creates nothing)
    python upload_draft.py <article.md> --upload --replace-live 412
                                                                 # replace a PUBLISHED post's content (backup first)
    python upload_draft.py --restore backups/412-<time>.json     # undo a replace

Requirements:
    pip install requests python-dotenv markdown pillow

.env (never commit, never print):
    WP_SITE_URL, WP_USERNAME, WP_APPLICATION_PASSWORD

What gets sent:
    - Post: title, HTML body (no <hr> separators), slug, excerpt, tags, category, featured image
    - Rank Math (via its own rankmath/v1/updateMeta route): SEO title, meta description,
      focus + secondary keywords, pillar-content flag, Facebook/Twitter title and description
    - Schema: Rank Math outputs Article + BreadcrumbList itself; this script adds ItemList
      (the ranked tools) and FAQPage as JSON-LD in a Custom HTML block

Safety (per MANDATE.md / CLAUDE.md):
    - status is hard-coded to "draft" and verified in the response.
    - New posts: aborts if the slug already exists.
    - Updates: only if the post is still a draft AND hasn't been edited in WordPress since
      the last upload (--expect-modified). Otherwise aborts, so manual edits are never overwritten.
    - Categories are never created (taxonomy changes need human approval). Missing ones are skipped.
    - Never prints credentials.
"""

import argparse
import html as html_lib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PREVIEW_DIR = Path("knowledge/_preview")
POST_STATUS = "draft"  # Do not change. Mandate: new articles are drafts only.
EDIT_TOLERANCE = timedelta(seconds=120)

# Publishing-meta table label -> internal key
META_LABELS = {
    "focus keyword": "focus_keyword",
    "secondary keywords": "secondary_keywords",
    "seo title (rank math)": "seo_title",
    "meta description": "meta_description",
    "slug": "slug",
    "h1": "h1",
    "status": "status_note",
    "tags": "tags",
    "category": "category",
    "featured image alt": "image_alt",
    "pricing verified": "pricing_verified",
    "affiliate domains": "affiliate_domains",
}

SITE_HOST = "toolpickguide.com"
AFFILIATE_HINTS = re.compile(r"[?&](ref|via|aff|affiliate|affid|partner|fpr|utm_source=affiliate)=|/(go|recommends|refer)/", re.I)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def split_sections(text):
    """Return (meta_block, article_body, schema_block) from the article file."""
    body_match = re.search(r"^# (?!📦|🧩).+$", text, flags=re.MULTILINE)
    if not body_match:
        sys.exit("ERROR: Could not find the article H1 (a '# ' heading that isn't the meta/schema block).")

    meta_block = text[: body_match.start()]
    rest = text[body_match.start():]

    schema_match = re.search(r"^# 🧩 SCHEMA.*$", rest, flags=re.MULTILINE)
    if schema_match:
        return meta_block, rest[: schema_match.start()].strip(), rest[schema_match.start():]
    return meta_block, rest.strip(), ""


def parse_meta_table(meta_block):
    """Pull SEO values out of the '| Parameter | Value |' table."""
    meta = {}
    for line in meta_block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = cells[0].lower()
        if label in META_LABELS:
            meta[META_LABELS[label]] = "|".join(cells[1:]).strip().strip("`").strip()

    if "slug" in meta:
        meta["slug"] = meta["slug"].strip("/").strip()

    missing = [k for k in ("focus_keyword", "seo_title", "meta_description", "slug") if not meta.get(k)]
    if missing:
        sys.exit(f"ERROR: Missing publishing meta fields: {', '.join(missing)}")

    split = lambda v, sep: [x.strip() for x in (v or "").split(sep) if x.strip()]  # noqa: E731
    meta["secondary_list"] = split(meta.get("secondary_keywords"), "·")
    meta["tag_list"] = split(meta.get("tags"), ",")
    meta["category_list"] = split(meta.get("category"), ",")
    meta["affiliate_list"] = [d.lower().removeprefix("www.") for d in split(meta.get("affiliate_domains"), ",")]
    return meta


def extract_tools(schema_block, body):
    """Ranked tool names, from the ItemList in the schema block (fallback: '## 1. Name (' headings)."""
    match = re.search(r"```json\s*(.+?)```", schema_block, flags=re.DOTALL)
    if match:
        try:
            for node in json.loads(match.group(1)).get("@graph", []):
                if node.get("@type") == "ItemList":
                    return [i["name"] for i in sorted(node["itemListElement"], key=lambda i: i["position"])]
        except (ValueError, KeyError):
            pass
    return re.findall(r"^## \d+\. (.+?) \(", body, flags=re.MULTILINE)


def extract_faq(body):
    """[(question, answer_text)] from the '## FAQs' section."""
    section = re.search(r"^## FAQ.*?$(.+?)(?=^## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    if not section:
        return []
    faq = []
    for block in re.split(r"^### ", section.group(1), flags=re.MULTILINE)[1:]:
        question, _, answer = block.partition("\n")
        answer = re.sub(r"^\s*---\s*$", "", answer, flags=re.MULTILINE)
        answer = re.sub(r"[*_`]", "", " ".join(answer.split()))
        answer = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", answer)
        if question.strip() and answer:
            faq.append((question.strip(), answer))
    return faq


def compile_body(body):
    """Drop the H1 (WordPress renders the post title), strip '---' separators, compile to HTML."""
    import markdown  # imported here so --help works without dependencies

    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    lines = [ln for ln in lines if not re.fullmatch(r"\s*(-{3,}|\*{3,}|_{3,})\s*", ln)]
    return markdown.markdown("\n".join(lines).strip(), extensions=["tables", "fenced_code", "sane_lists"])


def verified_line(meta):
    """Visible freshness line under the H1 (AI answer engines and readers both weigh dated facts)."""
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", meta.get("pricing_verified", ""))
    if not match:
        return ""
    verified = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    today = datetime.now()
    return (f'<p class="tpg-verified"><em>Last updated {today:%B} {today.day}, {today:%Y} · '
            f'Pricing verified {verified:%B %Y} on vendor sites</em></p>\n')


def mark_links(html, meta):
    """External links get rel="noopener" + new tab; affiliate links also get rel="sponsored nofollow"."""
    def fix(match):
        href = match.group(1)
        host = re.sub(r"^https?://(www\.)?", "", href).split("/")[0].lower()
        if not href.startswith("http") or host.endswith(SITE_HOST):
            return match.group(0)
        affiliate = AFFILIATE_HINTS.search(href) or any(host == d or host.endswith("." + d) for d in meta["affiliate_list"])
        rel = "sponsored nofollow noopener" if affiliate else "noopener"
        return f'<a href="{href}" rel="{rel}" target="_blank">'
    return re.sub(r'<a href="([^"]+)">', fix, html)


def build_schema_block(meta, title, tools, faq, site):
    """ItemList + FAQPage JSON-LD in a Gutenberg Custom HTML block. Rank Math already outputs Article/Breadcrumbs."""
    url = f"{site}/{meta['slug']}/" if site else f"/{meta['slug']}/"
    graph = []
    if tools:
        graph.append({
            "@type": "ItemList",
            "name": re.split(r"\s*\(\d{4}\)", title)[0],
            "url": url,
            "itemListOrder": "https://schema.org/ItemListUnordered" if " vs " in title.lower() else "https://schema.org/ItemListOrderAscending",
            "numberOfItems": len(tools),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n} for i, n in enumerate(tools)],
        })
    if faq:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
        })
    if not graph:
        return ""
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'\n<!-- wp:html -->\n<script type="application/ld+json">\n{payload}\n</script>\n<!-- /wp:html -->\n'


def load_article(path, site=""):
    text = Path(path).read_text(encoding="utf-8")
    meta_block, body, schema_block = split_sections(text)
    meta = parse_meta_table(meta_block)
    h1 = body.splitlines()[0][2:].strip() if body.startswith("# ") else ""
    title = meta.get("h1") or h1
    tools = extract_tools(schema_block, body)
    faq = extract_faq(body)
    html = compile_body(body)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', "", html, flags=re.S)  # one schema source only
    html = verified_line(meta) + mark_links(html, meta)
    return {
        "meta": meta, "title": title, "tools": tools, "faq": faq,
        "html": html, "schema_html": build_schema_block(meta, title, tools, faq, site),
    }


def rank_math_meta(meta, title):
    keywords = [meta["focus_keyword"]] + [k for k in meta["secondary_list"] if k.lower() != meta["focus_keyword"].lower()]
    return {
        "rank_math_title": meta["seo_title"],
        "rank_math_description": meta["meta_description"],
        "rank_math_focus_keyword": ",".join(keywords[:5]),  # Rank Math: first = primary, max 5
        "rank_math_pillar_content": "on",
        "rank_math_facebook_title": re.split(r"\s*\(\d{4}\)", title)[0],
        "rank_math_facebook_description": meta["meta_description"],
        "rank_math_twitter_use_facebook": "on",
    }


# ---------------------------------------------------------------------------
# WordPress
# ---------------------------------------------------------------------------

def load_credentials():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    site = os.getenv("WP_SITE_URL", "").rstrip("/")
    user = os.getenv("WP_USERNAME", "")
    password = os.getenv("WP_APPLICATION_PASSWORD", "")

    missing = [n for n, v in (("WP_SITE_URL", site), ("WP_USERNAME", user), ("WP_APPLICATION_PASSWORD", password)) if not v]
    if missing:
        sys.exit(f"ERROR: Missing in .env: {', '.join(missing)}")
    if not site.startswith("https://"):
        sys.exit("ERROR: WP_SITE_URL must use https:// (application passwords are sent with every request).")
    return site, user, password


HTACCESS_FIX = """\
  Most common cause: the web host strips the Authorization header before WordPress sees it.
  Fix (Apache/LiteSpeed): add this line near the top of the site's .htaccess, above "# BEGIN WordPress":
      SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
  Also check: security plugins (Wordfence, iThemes/Solid Security) or Cloudflare rules blocking
  application passwords or /wp-json/ requests."""


def explain_error(resp):
    """Turn a WordPress REST error into a readable diagnosis. Never includes credentials."""
    try:
        body = resp.json()
        code, message = body.get("code", ""), body.get("message", "")
        details = body.get("data", {}).get("details") or body.get("data", {}).get("params") or ""
    except ValueError:
        code, message, details = "", resp.text[:300], ""

    lines = [f"HTTP {resp.status_code} · code: {code or 'n/a'} · {message}"]
    if details:
        lines.append(f"  details: {details}")

    if code in ("rest_not_logged_in", "rest_forbidden_context") or (resp.status_code == 400 and "status" in str(details)):
        lines.append("  DIAGNOSIS: WordPress treated this request as LOGGED OUT. The application password never arrived.")
        lines.append("  On Hostinger: install wordpress/toolpickguide-auth-bridge.php into wp-content/mu-plugins/.")
        lines.append(HTACCESS_FIX)
    elif code in ("incorrect_password", "invalid_username", "invalid_email"):
        lines.append("  DIAGNOSIS: WordPress received the login but rejected it. Check WP_USERNAME (the login name, not display name)")
        lines.append("  and regenerate the application password in Users > Profile > Application Passwords.")
    elif code == "application_passwords_disabled" or "application password" in message.lower():
        lines.append("  DIAGNOSIS: Application passwords are disabled on this site (often by a security plugin).")
    elif resp.status_code == 403:
        lines.append("  DIAGNOSIS: Logged in but forbidden. The user role may lack the needed capability")
        lines.append("  (drafts: Contributor+, images: Author+), or a firewall/security plugin blocked the request.")
    return "\n".join(lines)


def make_session():
    import base64

    import requests

    site, user, password = load_credentials()
    session = requests.Session()
    session.auth = (user, password)
    # Hostinger's edge strips Authorization; the mu-plugin in wordpress/ reads this copy instead.
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    session.headers.update({"User-Agent": "ToolPickGuide-DraftUploader/2.0", "X-WP-Auth": f"Basic {token}"})
    return session, site


def wp(session, method, url, fail_msg, **kwargs):
    import time
    import requests
    timeout = kwargs.pop("timeout", 60)
    # Reads are retried when Hostinger drops the connection mid-response; writes never are (no double writes).
    tries = 3 if method.upper() == "GET" else 1
    for attempt in range(1, tries + 1):
        try:
            resp = session.request(method, url, timeout=timeout, **kwargs)
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError,
                requests.exceptions.Timeout) as e:
            if attempt == tries:
                if tries > 1:
                    sys.exit(f"ERROR: {fail_msg}\nThe connection to the site dropped {tries} times ({type(e).__name__}) "
                             "while reading. Nothing was changed. Wait a minute and run the same command again.")
                sys.exit(f"ERROR: {fail_msg}\nThe connection dropped during a write ({type(e).__name__}), so it may or may "
                         "not have been saved. Do not re-run yet: tell the agent, who checks the post first.")
            print(f"   (connection dropped, retrying {attempt}/{tries - 1}…)")
            time.sleep(5 * attempt)
    if resp.status_code >= 400:
        sys.exit(f"ERROR: {fail_msg}\n" + explain_error(resp))
    return resp.json()


def check_auth():
    """Read-only login test: asks WordPress who we are. Creates nothing."""
    session, site = make_session()
    resp = session.get(f"{site}/wp-json/wp/v2/users/me", params={"context": "edit"}, timeout=30)
    if resp.status_code != 200:
        sys.exit("LOGIN FAILED\n" + explain_error(resp))

    me = resp.json()
    caps = me.get("capabilities") or {}
    print("LOGIN OK")
    print(f"  User     : {me.get('slug') or me.get('name')} (ID {me.get('id')})")
    print(f"  Roles    : {', '.join(me.get('roles') or []) or 'unknown'}")
    print(f"  Can create drafts (edit_posts)  : {'YES' if caps.get('edit_posts') else 'NO: needs Contributor or higher'}")
    print(f"  Can upload images (upload_files): {'YES' if caps.get('upload_files') else 'NO: featured images need Author or higher'}")
    if not caps.get("edit_posts"):
        sys.exit(1)


def resolve_tags(session, api, names):
    ids = []
    for name in names:
        found = wp(session, "GET", f"{api}/tags", f"Could not look up tag '{name}'.", params={"search": name, "per_page": 100})
        match = next((t for t in found if html_lib.unescape(t["name"]).lower() == name.lower()), None)
        if not match:
            match = wp(session, "POST", f"{api}/tags", f"Could not create tag '{name}'.", json={"name": name})
            print(f"   + created tag: {name}")
        ids.append(match["id"])
    return ids


def resolve_categories(session, api, names):
    """Existing categories only. Never creates one (taxonomy change = human approval)."""
    ids = []
    for name in names:
        found = wp(session, "GET", f"{api}/categories", f"Could not look up category '{name}'.", params={"search": name, "per_page": 100})
        match = next((c for c in found if html_lib.unescape(c["name"]).lower() == name.lower() or c["slug"] == name.lower()), None)
        if not match:  # names with "&" are stored as "&amp;", so search misses them; try the slug
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower().replace("&", " ")).strip("-")
            by_slug = wp(session, "GET", f"{api}/categories", f"Could not look up category '{name}'.", params={"slug": slug})
            match = by_slug[0] if by_slug else None
        if match:
            ids.append(match["id"])
        else:
            print(f"   ⚠️ Category '{name}' not found. Skipped (create it in WP admin if you want it).")
    return ids


IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def upload_image(session, api, image_path, alt, slug):
    data = image_path.read_bytes()
    ext = image_path.suffix.lower()
    media = wp(session, "POST", f"{api}/media", "Could not upload the featured image.", data=data, timeout=120,
               headers={"Content-Type": IMAGE_TYPES.get(ext, "image/png"),
                        "Content-Disposition": f'attachment; filename="{slug}{ext if ext in IMAGE_TYPES else ".png"}"'})
    wp(session, "POST", f"{api}/media/{media['id']}", "Could not set image alt text.", json={"alt_text": alt, "title": alt})
    return media["id"]


def parse_wp_time(value):
    return datetime.fromisoformat(value.replace("Z", "")).replace(tzinfo=timezone.utc)


def publish(article, image_path, post_id=None, expect_modified=None, overwrite_wp_edits=False):
    session, site = make_session()
    api = f"{site}/wp-json/wp/v2"
    meta, title = article["meta"], article["title"]

    existing = None
    if post_id:
        existing = wp(session, "GET", f"{api}/posts/{post_id}", f"Could not load post {post_id}.", params={"context": "edit"})
        if existing.get("status") != POST_STATUS:
            sys.exit(f"ABORT: Post {post_id} is '{existing.get('status')}', not a draft. Only drafts are updated automatically.")
        wp_modified = parse_wp_time(existing["modified_gmt"])
        if overwrite_wp_edits:
            print(f"   ⚠️ --overwrite-wp-edits: replacing WordPress version last modified {existing['modified_gmt']} UTC.")
        elif not expect_modified:
            sys.exit("ABORT: Updating needs --expect-modified (last upload time, UTC) so manual WP edits are never overwritten.")
        elif wp_modified > parse_wp_time(expect_modified) + EDIT_TOLERANCE:
            sys.exit(f"ABORT: Post {post_id} was edited in WordPress at {existing['modified_gmt']} UTC, after the last upload. "
                     "Not overwriting manual edits. Copy any real WP edits into the Markdown file, then re-run with "
                     "--overwrite-wp-edits (auto_scheduler: --overwrite-wp-edits <file.md>). Close the WP editor first: "
                     "an open editor autosaves drafts and counts as an edit.")
    else:
        found = wp(session, "GET", f"{api}/posts", "Could not check for an existing post (no draft was created).",
                   params={"slug": meta["slug"], "status": "any", "context": "edit"}, timeout=30)
        if found:
            sys.exit(f"ABORT: A post with slug '{meta['slug']}' already exists (ID {found[0]['id']}). Not overwriting.")

    tag_ids = resolve_tags(session, api, meta["tag_list"])
    cat_ids = resolve_categories(session, api, meta["category_list"])

    media_id = (existing or {}).get("featured_media") or 0
    if not media_id and image_path:
        media_id = upload_image(session, api, image_path, meta.get("image_alt") or title, meta["slug"])
        print(f"   + featured image uploaded: media ID {media_id}")

    payload = {
        "title": title,
        "content": article["html"] + article["schema_html"],
        "slug": meta["slug"],
        "status": POST_STATUS,
        "excerpt": meta["meta_description"],
        "tags": tag_ids,
    }
    if cat_ids:
        payload["categories"] = cat_ids
    if media_id:
        payload["featured_media"] = media_id

    url = f"{api}/posts/{post_id}" if post_id else f"{api}/posts"
    post = wp(session, "POST", url, "WordPress rejected the draft.", json=payload)
    if post.get("status") != POST_STATUS:
        sys.exit(f"SAFETY ERROR: Post {post.get('id')} came back with status '{post.get('status')}'. Check it in WP admin now.")

    rm = session.post(f"{site}/wp-json/rankmath/v1/updateMeta", timeout=60,
                      json={"objectType": "post", "objectID": post["id"], "meta": rank_math_meta(meta, title)})
    rank_math_ok = rm.status_code < 400
    return post, rank_math_ok, (None if rank_math_ok else explain_error(rm))


BACKUP_DIR = Path("backups")


def snapshot_live(session, site, api, post):
    """Everything needed to put a published post back exactly as it was (plus its visible SEO title/description)."""
    import requests

    page = requests.get(post["link"], timeout=30, headers={"User-Agent": "ToolPickGuide-Backup/1.0"}).text
    seo_title = re.search(r"<title>(.*?)</title>", page, flags=re.S)
    seo_desc = re.search(r'<meta name="description" content="([^"]*)"', page)
    return {
        "backed_up_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "id": post["id"], "slug": post["slug"], "status": post["status"], "link": post["link"],
        "modified_gmt": post["modified_gmt"],
        "title": post["title"]["raw"], "content": post["content"]["raw"], "excerpt": post["excerpt"]["raw"],
        "tags": post["tags"], "categories": post["categories"], "featured_media": post["featured_media"],
        "rank_math_visible": {
            "title": html_lib.unescape(seo_title.group(1)).strip() if seo_title else None,
            "description": html_lib.unescape(seo_desc.group(1)) if seo_desc else None,
            "note": "Rendered values (variables already resolved). Focus keywords are not publicly readable and are not backed up.",
        },
    }


def refuse_in_scheduler(action):
    import os
    if os.environ.get("TPG_SCHEDULER"):
        sys.exit(f"ABORT: {action} changes a published page and never runs from the scheduler. Run it yourself.")


def replace_live(article, image_path, post_id, force=False, refresh_image=False):
    """Replace the content of ONE published post, after backing it up. Status and URL stay the same."""
    refuse_in_scheduler("--replace-live")
    session, site = make_session()
    api = f"{site}/wp-json/wp/v2"
    meta, title = article["meta"], article["title"]

    live = wp(session, "GET", f"{api}/posts/{post_id}", f"Could not load post {post_id}.", params={"context": "edit"})
    if live["slug"] != meta["slug"]:
        sys.exit(f"ABORT: Post {post_id} has slug '{live['slug']}', but the article targets '{meta['slug']}'. Wrong post ID?")
    if live["status"] != "publish":
        sys.exit(f"ABORT: Post {post_id} is '{live['status']}', not published. Use --post-id for drafts.")
    if live["title"]["raw"] == title and "tpg-verified" in live["content"]["raw"] and not force:
        originals = sorted(BACKUP_DIR.glob(f"{post_id}-*.json"))
        sys.exit(f"ABORT: Post {post_id} already has this upgrade (same title, uploader content). Nothing changed.\n"
                 f"   Original backup: {originals[0] if originals else 'none found'}\n"
                 "   To push edits to an already-upgraded post, re-run with --force-replace.")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"{post_id}-{datetime.now():%Y%m%d-%H%M%S}.json"
    backup.write_text(json.dumps(snapshot_live(session, site, api, live), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"   💾 Backup saved: {backup}")

    tag_ids = resolve_tags(session, api, meta["tag_list"])
    cat_ids = resolve_categories(session, api, meta["category_list"]) or live["categories"]
    if force and not refresh_image and "tpg-verified" in live["content"]["raw"]:
        image_path = None  # already upgraded once: keep the uploader's image instead of adding a duplicate
    media_id = upload_image(session, api, image_path, meta.get("image_alt") or title, meta["slug"]) if image_path else live["featured_media"]
    if image_path:
        print(f"   + featured image uploaded: media ID {media_id} (old image {live['featured_media']} kept in Media Library)")

    payload = {  # no "status" key: the post stays published
        "title": title,
        "content": article["html"] + article["schema_html"],
        "excerpt": meta["meta_description"],
        "tags": sorted(set(tag_ids) | set(live["tags"])),
        "categories": cat_ids,
        "featured_media": media_id,
    }
    post = wp(session, "POST", f"{api}/posts/{post_id}", "WordPress rejected the update. Live post unchanged.", json=payload)
    if post.get("status") != "publish" or post.get("slug") != live["slug"]:
        sys.exit(f"SAFETY ERROR: Post {post_id} is now '{post.get('status')}' at '{post.get('slug')}'. Restore with:\n"
                 f"   python upload_draft.py --restore {backup}")

    rm = session.post(f"{site}/wp-json/rankmath/v1/updateMeta", timeout=60,
                      json={"objectType": "post", "objectID": post_id, "meta": rank_math_meta(meta, title)})
    return post, backup, rm.status_code < 400, (None if rm.status_code < 400 else explain_error(rm))


def restore_backup(backup_path):
    refuse_in_scheduler("--restore")
    data = json.loads(Path(backup_path).read_text(encoding="utf-8"))
    session, site = make_session()
    api = f"{site}/wp-json/wp/v2"

    live = wp(session, "GET", f"{api}/posts/{data['id']}", f"Could not load post {data['id']}.", params={"context": "edit"})
    if live["slug"] != data["slug"]:
        sys.exit(f"ABORT: Post {data['id']} slug is now '{live['slug']}', backup is for '{data['slug']}'. Not restoring.")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    pre = BACKUP_DIR / f"{data['id']}-{datetime.now():%Y%m%d-%H%M%S}-pre-restore.json"
    pre.write_text(json.dumps(snapshot_live(session, site, api, live), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"   💾 Current version backed up first: {pre}")

    post = wp(session, "POST", f"{api}/posts/{data['id']}", "WordPress rejected the restore.", json={
        "title": data["title"], "content": data["content"], "excerpt": data["excerpt"],
        "tags": data["tags"], "categories": data["categories"], "featured_media": data["featured_media"],
    })
    seo = data.get("rank_math_visible") or {}
    if seo.get("title") or seo.get("description"):
        session.post(f"{site}/wp-json/rankmath/v1/updateMeta", timeout=60, json={
            "objectType": "post", "objectID": data["id"],
            "meta": {k: v for k, v in (("rank_math_title", seo.get("title")), ("rank_math_description", seo.get("description"))) if v}})
    print(f"\n✅ Restored post {post['id']} from {backup_path} (status: {post['status']})")
    print("   Rank Math title/description restored from the rendered page. Re-enter focus keywords by hand if needed.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def print_summary(article, image_path, replace_live_id=None):
    meta = article["meta"]
    print(f"Title    : {article['title']}")
    print(f"Slug     : /{meta['slug']}/")
    print(f"Status   : {f'stays published (replacing live post {replace_live_id})' if replace_live_id else POST_STATUS}")
    print(f"HTML     : {len(article['html']):,} characters (separators removed)")
    print(f"Tags     : {', '.join(meta['tag_list']) or 'none'}")
    print(f"Category : {', '.join(meta['category_list']) or 'none'}")
    print(f"Image    : {image_path or 'none'}  | alt: {meta.get('image_alt') or article['title']}")
    print(f"Schema   : Rank Math Article + Breadcrumbs, plus ItemList ({len(article['tools'])} tools) + FAQPage ({len(article['faq'])} Qs, exactly 1 FAQPage)")
    print(f"Freshness: {re.sub('<[^>]+>', '', verified_line(meta)).strip() or 'no Pricing verified date in meta'}")
    ext = re.findall(r'rel="([^"]+)" target="_blank"', article["html"])
    print(f"Links    : {len(ext)} external ({sum('sponsored' in r for r in ext)} marked sponsored)")
    print("Rank Math:")
    for k, v in rank_math_meta(meta, article["title"]).items():
        print(f"  {k:32}: {v}")


def main():
    parser = argparse.ArgumentParser(description="Upload a Markdown article to WordPress as a draft.")
    parser.add_argument("article", nargs="?", help="Path to the Markdown article")
    parser.add_argument("--upload", action="store_true", help="Send to WordPress (default: dry run)")
    parser.add_argument("--post-id", type=int, help="Update this existing DRAFT instead of creating a new post")
    parser.add_argument("--expect-modified", help="UTC time of the last upload. Required with --post-id")
    parser.add_argument("--overwrite-wp-edits", action="store_true", help="With --post-id: replace the WP draft even if it was edited in WordPress")
    parser.add_argument("--replace-live", type=int, metavar="POST_ID",
                        help="With --upload: replace the content of this PUBLISHED post (backs it up first)")
    parser.add_argument("--force-replace", action="store_true", help="With --replace-live: push edits to a post that was already upgraded")
    parser.add_argument("--refresh-image", action="store_true", help="With --force-replace: upload the regenerated featured image too")
    parser.add_argument("--restore", metavar="BACKUP.json", help="Put a published post back from a backup file")
    parser.add_argument("--no-image", action="store_true", help="Skip featured image generation/upload")
    parser.add_argument("--check-auth", action="store_true", help="Read-only login test. Creates nothing")
    args = parser.parse_args()

    if args.check_auth:
        check_auth()
        return
    if args.restore:
        restore_backup(args.restore)
        return
    if args.replace_live and args.post_id:
        parser.error("--replace-live and --post-id can't be combined")
    if not args.article:
        parser.error("article path is required")

    path = Path(args.article)
    if not path.is_file():
        sys.exit(f"ERROR: Article not found: {path}")

    article = load_article(path, site="https://toolpickguide.com")
    image_path = None
    if not args.no_image:
        from make_featured_image import build_for_article
        image_path = build_for_article(path, article["title"], article["tools"])

    print(f"Article  : {path}")
    print_summary(article, image_path, args.replace_live)

    if not args.upload:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        preview = PREVIEW_DIR / f"{path.stem}.html"
        img_tag = f'<img src="../images/{image_path.name}" style="max-width:100%">\n' if image_path else ""
        preview.write_text(f"{img_tag}<h1>{article['title']}</h1>\n{article['html']}\n<pre>{html_lib.escape(article['schema_html'])}</pre>",
                           encoding="utf-8")
        print(f"\nDRY RUN: nothing sent. Preview written to {preview}")
        return

    if args.replace_live:
        post, backup, rank_math_ok, rank_math_err = replace_live(article, image_path, args.replace_live, args.force_replace, args.refresh_image)
        print(f"\n✅ Live post replaced: ID {post['id']} (status: {post['status']}, same URL)")
        print(f"   View: {post.get('link', '')}")
        print(f"   Undo: python upload_draft.py --restore {backup}")
        print("   Rank Math meta saved." if rank_math_ok else "   ⚠️ Rank Math meta NOT saved:\n" + rank_math_err)
        return

    post, rank_math_ok, rank_math_err = publish(article, image_path, args.post_id, args.expect_modified, args.overwrite_wp_edits)
    verb = "updated" if args.post_id else "created"
    print(f"\n✅ Draft {verb}: ID {post['id']} (status: {post['status']})")
    print(f"   modified_gmt: {post.get('modified_gmt')}")
    print(f"   Edit: {post.get('link', '')}")
    if rank_math_ok:
        print("   Rank Math meta saved.")
    else:
        print("   ⚠️ Rank Math meta NOT saved. Set it in the Rank Math panel:\n" + rank_math_err)


if __name__ == "__main__":
    main()
