"""
make_featured_image.py: generate a text-free, illustrated 1200x630 featured image per article.

No words on the image (per user direction, 2026-09-29). Each article gets:
  - a subject illustration picked from its topic (camera, house, documents, chat, scales, versus, switch)
  - a palette, layout, and decorative pattern chosen from the article's slug, so no two images match

    python make_featured_image.py knowledge/<article>.md      # regenerate one image
    python make_featured_image.py --all                        # regenerate every article image

Used automatically by upload_draft.py. Requires: pip install pillow
"""

import hashlib
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 630
SS = 2  # supersampling for smooth edges

PALETTES = [  # (background top, background bottom, accent 1, accent 2, line/ink)
    ((14, 30, 54), (32, 76, 120), (255, 196, 87), (94, 234, 212), (248, 250, 252)),
    ((40, 18, 56), (106, 44, 112), (255, 138, 128), (255, 214, 102), (255, 247, 237)),
    ((8, 47, 45), (22, 101, 88), (253, 224, 71), (167, 243, 208), (240, 253, 250)),
    ((49, 23, 14), (146, 64, 14), (254, 215, 170), (125, 211, 252), (255, 251, 235)),
    ((17, 24, 39), (55, 48, 163), (244, 114, 182), (129, 230, 217), (238, 242, 255)),
    ((236, 244, 255), (191, 219, 254), (37, 99, 235), (249, 115, 22), (30, 41, 59)),
    ((254, 243, 199), (253, 186, 116), (190, 24, 93), (21, 94, 117), (41, 37, 36)),
    ((220, 252, 231), (134, 239, 172), (21, 128, 61), (219, 39, 119), (20, 83, 45)),
]


def theme_for(stem, title):
    s = f"{stem} {title}".lower()
    if " vs " in s or "-vs-" in s:
        return "versus"
    if "alternative" in s:
        return "switch"
    for key, theme in (("photograph", "camera"), ("real-estate", "house"), ("real estate", "house"),
                       ("account", "documents"), ("cpa", "documents"), ("tax", "documents"),
                       ("coach", "chat"), ("law", "scales"), ("legal", "scales")):
        if key in s:
            return theme
    return "documents"


def S(v):
    return int(v * SS)


def rr(draw, box, r, **kw):
    draw.rounded_rectangle([S(b) for b in box], radius=S(r), **kw)


def gradient(top, bottom, angle_flip):
    img = Image.new("RGB", (S(W), S(H)))
    d = ImageDraw.Draw(img)
    for y in range(S(H)):
        t = y / S(H)
        t = 1 - t if angle_flip else t
        d.line([(0, y), (S(W), y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def blobs(img, rng, colors):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(rng.randint(3, 5)):
        c = rng.choice(colors)
        x, y, r = rng.randint(-100, W + 100), rng.randint(-100, H + 100), rng.randint(140, 320)
        d.ellipse([S(x - r), S(y - r), S(x + r), S(y + r)], fill=c + (rng.randint(50, 90),))
    return Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(S(70))))


def pattern(img, rng, ink, kind):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = 28
    if kind == "dots":
        step = rng.choice([28, 34, 40])
        for x in range(0, W, step):
            for y in range(0, H, step):
                d.ellipse([S(x), S(y), S(x + 3), S(y + 3)], fill=ink + (a,))
    elif kind == "grid":
        step = rng.choice([48, 60])
        for x in range(0, W, step):
            d.line([S(x), 0, S(x), S(H)], fill=ink + (a - 10,), width=S(1))
        for y in range(0, H, step):
            d.line([0, S(y), S(W), S(y)], fill=ink + (a - 10,), width=S(1))
    elif kind == "rings":
        cx, cy = rng.randint(200, 1000), rng.randint(100, 530)
        for r in range(60, 900, 55):
            d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], outline=ink + (a - 8,), width=S(2))
    elif kind == "diagonal":
        for x in range(-H, W, 36):
            d.line([S(x), S(H), S(x + H), 0], fill=ink + (a - 12,), width=S(2))
    return Image.alpha_composite(img, layer)


def card(d, box, fill, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        rr(d, (x0 + 10, y0 + 14, x1 + 10, y1 + 14), 28, fill=(0, 0, 0, 60))
    rr(d, box, 28, fill=fill)


# ---------- subject illustrations (all drawn as shapes: no text) ----------

def draw_camera(d, cx, cy, s, ink, a1, a2):
    rr(d, (cx - 150 * s, cy - 80 * s, cx + 150 * s, cy + 110 * s), 30 * s, fill=ink)
    rr(d, (cx - 60 * s, cy - 118 * s, cx + 40 * s, cy - 70 * s), 12 * s, fill=ink)
    for r, c in ((78, a1), (58, (30, 30, 40)), (36, a2), (14, ink)):
        d.ellipse([S(cx - r * s), S(cy + 15 * s - r * s), S(cx + r * s), S(cy + 15 * s + r * s)], fill=c)
    d.ellipse([S(cx + 95 * s), S(cy - 55 * s), S(cx + 125 * s), S(cy - 25 * s)], fill=a1)


def draw_house(d, cx, cy, s, ink, a1, a2):
    d.polygon([(S(cx - 170 * s), S(cy - 10 * s)), (S(cx), S(cy - 150 * s)), (S(cx + 170 * s), S(cy - 10 * s))], fill=a1)
    rr(d, (cx - 130 * s, cy - 20 * s, cx + 130 * s, cy + 140 * s), 10 * s, fill=ink)
    rr(d, (cx - 30 * s, cy + 40 * s, cx + 30 * s, cy + 140 * s), 8 * s, fill=a2)
    for dx in (-95, 55):
        rr(d, (cx + dx * s, cy + 15 * s, cx + (dx + 40) * s, cy + 55 * s), 6 * s, fill=a2)
    rr(d, (cx + 70 * s, cy - 120 * s, cx + 105 * s, cy - 55 * s), 4 * s, fill=ink)


def draw_documents(d, cx, cy, s, ink, a1, a2):
    for i, c in enumerate((a2, a1, ink)):
        off = (2 - i) * 26 * s
        rr(d, (cx - 110 * s + off, cy - 140 * s + off, cx + 70 * s + off, cy + 110 * s + off), 18 * s, fill=c)
    for j in range(5):
        y = cy - 95 * s + j * 36 * s
        w = 120 if j % 2 == 0 else 90
        rr(d, (cx - 75 * s, y, cx + (w - 75) * s, y + 12 * s), 6 * s, fill=(150, 160, 180))
    rr(d, (cx + 60 * s, cy + 10 * s, cx + 170 * s, cy + 150 * s), 16 * s, fill=a1)
    for r in range(3):
        for c in range(3):
            x, y = cx + 76 * s + c * 30 * s, cy + 58 * s + r * 28 * s
            rr(d, (x, y, x + 20 * s, y + 18 * s), 4 * s, fill=ink)
    rr(d, (cx + 76 * s, cy + 24 * s, cx + 154 * s, cy + 44 * s), 4 * s, fill=ink)


def draw_chat(d, cx, cy, s, ink, a1, a2):
    rr(d, (cx - 170 * s, cy - 130 * s, cx + 60 * s, cy + 10 * s), 40 * s, fill=ink)
    d.polygon([(S(cx - 120 * s), S(cy + 5 * s)), (S(cx - 150 * s), S(cy + 55 * s)), (S(cx - 70 * s), S(cy + 5 * s))], fill=ink)
    rr(d, (cx - 40 * s, cy - 10 * s, cx + 170 * s, cy + 120 * s), 40 * s, fill=a1)
    d.polygon([(S(cx + 110 * s), S(cy + 115 * s)), (S(cx + 150 * s), S(cy + 160 * s)), (S(cx + 60 * s), S(cy + 115 * s))], fill=a1)
    for i in range(3):
        x = cx - 110 * s + i * 50 * s
        d.ellipse([S(x), S(cy - 75 * s), S(x + 26 * s), S(cy - 49 * s)], fill=a2)
    for j in range(2):
        rr(d, (cx, cy + 25 * s + j * 38 * s, cx + (130 - j * 40) * s, cy + 43 * s + j * 38 * s), 8 * s, fill=ink)


def draw_scales(d, cx, cy, s, ink, a1, a2):
    rr(d, (cx - 10 * s, cy - 130 * s, cx + 10 * s, cy + 120 * s), 8 * s, fill=ink)
    rr(d, (cx - 90 * s, cy + 110 * s, cx + 90 * s, cy + 135 * s), 10 * s, fill=ink)
    d.line([S(cx - 150 * s), S(cy - 90 * s), S(cx + 150 * s), S(cy - 110 * s)], fill=ink, width=S(14 * s))
    for px, py, c in ((cx - 150 * s, cy - 90 * s, a1), (cx + 150 * s, cy - 110 * s, a2)):
        d.line([S(px), S(py), S(px - 50 * s), S(py + 110 * s)], fill=ink, width=S(5 * s))
        d.line([S(px), S(py), S(px + 50 * s), S(py + 110 * s)], fill=ink, width=S(5 * s))
        d.chord([S(px - 70 * s), S(py + 70 * s), S(px + 70 * s), S(py + 150 * s)], 0, 180, fill=c)
    d.ellipse([S(cx - 22 * s), S(cy - 152 * s), S(cx + 22 * s), S(cy - 108 * s)], fill=a1)


def draw_versus(d, cx, cy, s, ink, a1, a2):
    card(d, (cx - 300 * s, cy - 140 * s, cx - 30 * s, cy + 140 * s), a1)
    card(d, (cx + 30 * s, cy - 140 * s, cx + 300 * s, cy + 140 * s), a2)
    for x0, c in ((cx - 300 * s, a2), (cx + 30 * s, a1)):
        d.ellipse([S(x0 + 95 * s), S(cy - 95 * s), S(x0 + 175 * s), S(cy - 15 * s)], fill=ink)
        for j in range(3):
            rr(d, (x0 + 50 * s, cy + 20 * s + j * 32 * s, x0 + (220 - j * 40) * s, cy + 36 * s + j * 32 * s), 8 * s, fill=ink)
    d.ellipse([S(cx - 48 * s), S(cy - 48 * s), S(cx + 48 * s), S(cy + 48 * s)], fill=ink)
    d.line([S(cx - 20 * s), S(cy - 22 * s), S(cx + 20 * s), S(cy + 22 * s)], fill=a1, width=S(10 * s))
    d.line([S(cx + 20 * s), S(cy - 22 * s), S(cx - 20 * s), S(cy + 22 * s)], fill=a2, width=S(10 * s))


def draw_switch(d, cx, cy, s, ink, a1, a2):
    for i, c in enumerate((a2, ink, a1)):
        x = cx - 230 * s + i * 170 * s
        card(d, (x, cy - 100 * s + (i % 2) * 40 * s, x + 130 * s, cy + 90 * s + (i % 2) * 40 * s), c)
    for dy, c in ((-150, a1), (150, a2)):
        y = cy + dy * s
        d.line([S(cx - 220 * s), S(y), S(cx + 200 * s), S(y)], fill=c, width=S(14 * s))
        tip = cx + 230 * s if dy < 0 else cx - 250 * s
        base = tip - 40 * s if dy < 0 else tip + 40 * s
        d.polygon([(S(tip), S(y)), (S(base), S(y - 28 * s)), (S(base), S(y + 28 * s))], fill=c)


SUBJECTS = {"camera": draw_camera, "house": draw_house, "documents": draw_documents, "chat": draw_chat,
            "scales": draw_scales, "versus": draw_versus, "switch": draw_switch}


def render(stem, title, out_path, theme=None):
    seed = int(hashlib.sha256(stem.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    top, bottom, a1, a2, ink = PALETTES[seed % len(PALETTES)]
    if rng.random() < 0.5:
        a1, a2 = a2, a1
    img = gradient(top, bottom, rng.random() < 0.5)
    img = blobs(img, rng, [a1, a2])
    img = pattern(img, rng, ink, rng.choice(["dots", "grid", "rings", "diagonal"])).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")  # RGB canvas + RGBA draw = real alpha blending

    layout = rng.choice(["right", "left", "center"])
    theme = theme or theme_for(stem, title)
    cx = {"right": 800, "left": 400, "center": 600}[layout] if theme not in ("versus", "switch") else 600
    cy = 330

    if theme not in ("versus", "switch"):  # floating backdrop card + side accents for depth
        card(d, (cx - 230, cy - 200, cx + 230, cy + 200), ink + (38,), shadow=False)
        for _ in range(rng.randint(2, 4)):
            w, h = rng.randint(90, 160), rng.randint(60, 105)
            left_ok, right_ok = cx - 250 - w > 40, cx + 250 + w < W - 40
            side = rng.choice([sd for sd, ok in (("L", left_ok), ("R", right_ok)) if ok] or ["R"])
            x = rng.randint(40, cx - 250 - w) if side == "L" else rng.randint(cx + 250, W - 40 - w)
            y = rng.randint(50, H - 50 - h)
            card(d, (x, y, x + w, y + h), rng.choice([a1, a2, ink]) + (rng.randint(150, 230),))
    SUBJECTS[theme](d, cx, cy, 1.0 if theme in ("versus", "switch") else 1.15, ink, a1, a2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").resize((W, H), Image.LANCZOS).save(out_path, "PNG", optimize=True)
    return out_path


def build_for_article(article_path, title, tools):
    """Called by upload_draft.py. Returns the photo path, or None.

    Only a realistic photo counts: knowledge/images/<stem>-photo.(webp|jpg|jpeg|png) (Junia-style AI photo or
    stock photo). Generated illustrations are never used any more (user rule 2026-10-06: "do not create those
    kind of pictures, use Junia's style"). With no photo, the uploader keeps the post's current image."""
    article_path = Path(article_path)
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        photo = article_path.parent / "images" / f"{article_path.stem}-photo{ext}"
        if photo.is_file():
            return photo
    return None


if __name__ == "__main__":
    import upload_draft

    targets = sorted(Path("knowledge").glob("*.md")) if sys.argv[1:] == ["--all"] else [Path(a) for a in sys.argv[1:]]
    if not targets:
        sys.exit("Usage: python make_featured_image.py <article.md> | --all")
    for path in targets:
        article = upload_draft.load_article(path)
        out = path.parent / "images" / f"{path.stem}.png"
        out.unlink(missing_ok=True)
        print(build_for_article(path, article["title"], article["tools"]), "·", theme_for(path.stem, article["title"]))
