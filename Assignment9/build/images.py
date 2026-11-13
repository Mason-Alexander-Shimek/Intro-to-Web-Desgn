"""Turn the source photographs into responsive, weight-budgeted image sets.

Every photograph ships as AVIF, WebP and JPEG at several widths. The browser
picks the smallest format it understands, so modern phones pull the AVIF and
nothing breaks on older ones.

Run: python3 build/images.py
Sources live outside the repo; SRC_DIR points at them. The generated files in
images/photos/ are committed, so the site builds without the originals.
"""
import pathlib, sys, json
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "images" / "photos"
SRC_DIR = pathlib.Path("/mnt/user-data/attachments/ff01b069-a533-5842-b85e-98d30395b651")

# Quality settings. AVIF and WebP are perceptual scales, not percentages;
# these were chosen by encoding and looking, not by guessing.
Q = {"avif": 46, "webp": 74, "jpeg": 78}

# How many widths of the JPEG fallback to generate, counting up from smallest.
JPEG_LADDER = 2

# crop is (left, top, right, bottom) as fractions of the source. None keeps all.
PHOTOS = {
    "valley": {
        "src": "0ee5b61d-image.png",
        "alt": "The Missoula valley seen from above, with the Clark Fork river "
               "winding through the middle of town and the Sapphire Mountains beyond.",
        "credit": "Aerial view of Missoula, Montana",
    },
    "riverfront": {
        "src": "ac0e7ccf-image.png",
        "alt": "The Clark Fork river running past downtown Missoula, with the "
               "riverside path, Caras Park and the hills above the city.",
        "credit": "Clark Fork river and downtown Missoula",
    },
    "mainhall": {
        "src": "eff81067-image.png",
        "alt": "Main Hall at the University of Montana, a red brick building with "
               "a clock tower, below the grassy slope of Mount Sentinel.",
        "credit": "Main Hall, University of Montana",
    },
    "depot": {
        "src": "822a3547-image.png",
        "alt": "The Missoula depot, a yellow brick building with two towers, with "
               "the bronze bear statue in front and the M on Mount Sentinel behind.",
        "credit": "Missoula depot and the bear statue",
    },
    "locomotive": {
        "src": "aa803c18-image.png",
        "alt": "A preserved logging locomotive and flatcar loaded with timber at "
               "Fort Missoula, with the hills west of town behind it.",
        "credit": "Historical logging locomotive, Fort Missoula",
    },
}

# Each use gets its own crop and width ladder, because a hero and a thumbnail
# want different shapes and different amounts of detail.
USES = {
    # homepage hero, wide screens: a letterbox band
    "hero-wide":   {"photo": "riverfront", "crop": (0.0, 0.26, 1.0, 0.78), "widths": [640, 860, 1100, 1280]},
    # homepage hero, phones: a taller crop so the overlay has somewhere to sit
    "hero-narrow": {"photo": "riverfront", "crop": (0.10, 0.12, 0.92, 0.88), "widths": [420, 640, 860, 1050]},
    # about page banner
    "valley-band": {"photo": "valley",     "crop": None,                    "widths": [640, 860, 1100, 1400]},
    # about page gallery cards
    "mainhall":    {"photo": "mainhall",   "crop": (0.0, 0.04, 1.0, 0.92),  "widths": [380, 560, 760]},
    "depot":       {"photo": "depot",      "crop": None,                    "widths": [380, 560, 760]},
    "locomotive":  {"photo": "locomotive", "crop": (0.0, 0.10, 1.0, 0.94),  "widths": [380, 560, 760]},
}


def crop_box(im, frac):
    if not frac:
        return im
    w, h = im.size
    l, t, r, b = frac
    return im.crop((round(l * w), round(t * h), round(r * w), round(b * h)))


def build(preview_only=False):
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, total = {}, 0

    for use, spec in USES.items():
        meta = PHOTOS[spec["photo"]]
        src = SRC_DIR / meta["src"]
        if not src.exists():
            sys.exit(f"missing source: {src}")

        im = Image.open(src).convert("RGB")
        im = crop_box(im, spec["crop"])
        cw, ch = im.size

        if preview_only:
            p = OUT / f"_preview-{use}.png"
            im.resize((700, round(700 * ch / cw)), Image.LANCZOS).save(p)
            print(f"{use:<14} crop {cw}x{ch} ratio {cw/ch:.2f} -> {p.name}")
            continue

        widths = [w for w in spec["widths"] if w <= cw] or [cw]
        # JPEG only exists for browsers that understand neither AVIF nor WebP,
        # which is a sliver of traffic running old software on old screens. They
        # get the two smaller widths; shipping them a 1280px fallback put the two
        # largest files in the repo behind a door almost nobody opens.
        jpg_widths = widths[:JPEG_LADDER]
        entry = {"alt": meta["alt"], "credit": meta["credit"],
                 "ratio": round(cw / ch, 4), "widths": widths,
                 "jpg_widths": jpg_widths, "sizes": {}}

        for w in widths:
            h = round(w * ch / cw)
            rs = im.resize((w, h), Image.LANCZOS)
            formats = [("avif", "avif"), ("webp", "webp")]
            if w in jpg_widths:
                formats.append(("jpeg", "jpg"))
            for fmt, ext in formats:
                f = OUT / f"{use}-{w}.{ext}"
                if fmt == "jpeg":
                    rs.save(f, "JPEG", quality=Q["jpeg"], optimize=True, progressive=True)
                else:
                    rs.save(f, fmt.upper(), quality=Q[fmt])
                kb = f.stat().st_size / 1024
                entry["sizes"][f.name] = round(kb, 1)
                total += kb
            # report the AVIF, which is what almost every visitor will actually get
            jpg = entry["sizes"].get(f"{use}-{w}.jpg")
            print(f"  {use:<14} {w:>5}px  avif {entry['sizes'][f'{use}-{w}.avif']:>6.1f} KB"
                  f"   webp {entry['sizes'][f'{use}-{w}.webp']:>6.1f} KB"
                  + (f"   jpg {jpg:>6.1f} KB" if jpg else "   jpg      —"))
        entry["intrinsic"] = {"w": widths[-1], "h": round(widths[-1] * ch / cw)}
        manifest[use] = entry

    if not preview_only:
        (HERE / "photos.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"\n{len(manifest)} image sets, {total/1024:.2f} MB on disk across all "
              f"formats and widths (a visitor downloads one file per image)")


if __name__ == "__main__":
    build(preview_only="--preview" in sys.argv)
