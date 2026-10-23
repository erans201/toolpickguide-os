"""
stock_photo.py: find and download free stock photos for our pages, from Pixabay (PIXABAY_API_KEY, preferred since
2026-10-23: Pexels paused new API keys) or Pexels (PEXELS_API_KEY). User decisions 2026-10-17/23: the cloud robot picks
photos itself; Unsplash is not used here because its API terms forbid self-hosted copies. Pixabay's license needs no
attribution and its API terms ask us to download images rather than hotlink them, which is what we do.

    python stock_photo.py --search "lawyer reviewing documents with client"   # 8 candidates + thumbnails to look at
    python stock_photo.py --get 3184465 --out knowledge/images/<stem>-photo.jpg          # Pexels ID
    python stock_photo.py --get pixabay-1838584 --out knowledge/images/<stem>-photo.jpg  # Pixabay ID (as --search prints it)

--search prints each candidate (ID, photographer, Pexels description) and saves small previews to
knowledge/_preview/pexels/<id>.jpg so the robot can LOOK at them before choosing (realistic photo, no logos,
slogans or overlaid text, fits the article). --get saves a 1200 px wide JPG plus <file>.credit.json; upload_draft.py
and media_fix.py read that file and put "Photo by <name> on Pexels" into the Media Library caption, and the
mu-plugin wordpress/toolpickguide-photo-credits.php shows the credits under the post and a site-wide
"Photos provided by Pexels" link (Pexels API guidelines). Key: PEXELS_API_KEY in .env / the cloud environment,
never printed. Read-only on our site; 200 requests/hour, 20,000/month (free).
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path

import requests

API = "https://api.pexels.com/v1"
PREVIEW = Path("knowledge/_preview/pexels")


PIXABAY = "https://pixabay.com/api/"


def env(name):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    return os.environ.get(name, "").strip()


def pixabay_search(query, n):
    k = env("PIXABAY_API_KEY")
    r = requests.get(PIXABAY, params={"key": k, "q": query, "image_type": "photo", "orientation": "horizontal",
                                      "safesearch": "true", "per_page": max(n, 3), "min_width": 1200}, timeout=60)
    if r.status_code != 200:
        sys.exit(f"ERROR: Pixabay HTTP {r.status_code}: {r.text[:200].replace(k, '[REDACTED]')}")
    return r.json().get("hits", [])


def key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    k = os.environ.get("PEXELS_API_KEY", "").strip()
    if not k:
        sys.exit("ERROR: PEXELS_API_KEY is not set (.env or the cloud environment).")
    return k


def call(path, params):
    k = key()
    r = requests.get(f"{API}/{path}", params=params, headers={"Authorization": k}, timeout=60)
    if r.status_code != 200:
        sys.exit(f"ERROR: Pexels HTTP {r.status_code}: {r.text[:200].replace(k, '[REDACTED]')}")
    return r.json()


def search(query, n):
    PREVIEW.mkdir(parents=True, exist_ok=True)
    if env("PIXABAY_API_KEY"):
        hits = pixabay_search(query, n)
        if not hits:
            print("No results. Try a broader query.")
        for h in hits[:n]:
            thumb = PREVIEW / f"pixabay-{h['id']}.jpg"
            thumb.write_bytes(requests.get(h["webformatURL"], timeout=60).content)
            print(f"pixabay-{h['id']} | {h['imageWidth']}x{h['imageHeight']} | by {h['user']} | {h.get('tags', '')} | preview: {thumb}")
        return
    photos = call("search", {"query": query, "orientation": "landscape", "per_page": n}).get("photos", [])
    if not photos:
        print("No results. Try a broader query.")
    for p in photos:
        thumb = PREVIEW / f"{p['id']}.jpg"
        thumb.write_bytes(requests.get(p["src"]["medium"], timeout=60).content)
        print(f"{p['id']} | {p['width']}x{p['height']} | by {p['photographer']} | {p.get('alt') or ''} | preview: {thumb}")


def get(photo_id, out):
    if str(photo_id).startswith("pixabay-"):
        return get_pixabay(str(photo_id).split("-", 1)[1], out)
    p = call(f"photos/{photo_id}", {})
    raw = requests.get(p["src"]["original"], timeout=120).content
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)))
        im.save(out, "JPEG", quality=82)
    except ImportError:  # no Pillow: keep the large rendition Pexels already sizes
        out.write_bytes(requests.get(p["src"]["large2x"], timeout=120).content)
    credit = {"source": "Pexels", "photographer": p["photographer"], "photographer_url": p["photographer_url"],
              "photo_url": p["url"], "pexels_id": p["id"], "alt_hint": p.get("alt") or ""}
    out.with_suffix(".credit.json").write_text(json.dumps(credit, indent=1), encoding="utf-8")
    print(f"✅ Saved {out} (by {p['photographer']} on Pexels) + {out.with_suffix('.credit.json').name}")


def get_pixabay(pid, out):
    k = env("PIXABAY_API_KEY")
    r = requests.get(PIXABAY, params={"key": k, "id": pid}, timeout=60)
    hits = r.json().get("hits", []) if r.status_code == 200 else []
    if not hits:
        sys.exit(f"ERROR: Pixabay photo {pid} not found (HTTP {r.status_code}).")
    h = hits[0]
    raw = requests.get(h["largeImageURL"], timeout=120).content
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)))
        im.save(out, "JPEG", quality=82)
    except ImportError:
        out.write_bytes(raw)
    credit = {"source": "Pixabay", "photographer": h["user"], "photo_url": h["pageURL"], "pixabay_id": h["id"],
              "alt_hint": h.get("tags", "")}
    out.with_suffix(".credit.json").write_text(json.dumps(credit, indent=1), encoding="utf-8")
    print(f"✅ Saved {out} (Pixabay {h['id']} by {h['user']}; no attribution required) + {out.with_suffix('.credit.json').name}")


def main():
    ap = argparse.ArgumentParser(description="Free stock photos from Pexels.")
    ap.add_argument("--search", metavar="QUERY")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--get", metavar="PHOTO_ID")
    ap.add_argument("--out", metavar="FILE")
    a = ap.parse_args()
    if a.search:
        search(a.search, a.n)
    elif a.get and a.out:
        get(a.get, a.out)
    else:
        sys.exit("Use --search QUERY, or --get PHOTO_ID --out knowledge/images/<stem>-photo.jpg")


if __name__ == "__main__":
    main()
