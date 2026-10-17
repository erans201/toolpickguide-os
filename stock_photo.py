"""
stock_photo.py: find and download free stock photos from Pexels for our pages (user decisions 2026-10-17:
the cloud robot picks photos itself; Pexels instead of Unsplash, whose API terms forbid self-hosted copies).

    python stock_photo.py --search "lawyer reviewing documents with client"   # 8 candidates + thumbnails to look at
    python stock_photo.py --get 3184465 --out knowledge/images/<stem>-photo.jpg

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
    photos = call("search", {"query": query, "orientation": "landscape", "per_page": n}).get("photos", [])
    if not photos:
        print("No results. Try a broader query.")
    for p in photos:
        thumb = PREVIEW / f"{p['id']}.jpg"
        thumb.write_bytes(requests.get(p["src"]["medium"], timeout=60).content)
        print(f"{p['id']} | {p['width']}x{p['height']} | by {p['photographer']} | {p.get('alt') or ''} | preview: {thumb}")


def get(photo_id, out):
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
