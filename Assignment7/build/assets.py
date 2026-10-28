"""Prepare Vallam art for a black-background site.

Emblems are white line art on black: the black is knocked out to transparency so
they sit on any dark surface. Scenes and banners are sepia photographs and keep
their ground, resized and saved as JPEG.
"""
from PIL import Image, ImageOps
import pathlib, json, shutil

SRC  = pathlib.Path("/home/claude/vallam/art")
DEST = pathlib.Path("/home/claude/work/GitHub/Intro-to-Web-Desgn/Assignment7/images")
DEST.mkdir(parents=True, exist_ok=True)

def classify(im):
    sm = im.convert("RGB").resize((80, 80))
    px = list(sm.get_flattened_data()) if hasattr(sm, "get_flattened_data") else list(sm.getdata())
    sat = sum(max(p) - min(p) for p in px) / len(px)
    ratio = im.width / im.height
    if sat < 5:                 return "emblem"
    if ratio >= 2.0:            return "banner"
    return "scene"

def knockout(im):
    """White-on-black line art -> white-on-transparent."""
    rgb = im.convert("RGB")
    lum = ImageOps.grayscale(rgb)
    # push near-black fully clear, keep the strokes solid
    alpha = lum.point(lambda v: 0 if v < 14 else min(255, int((v - 14) * 255 / 200)))
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out.crop(out.getbbox() or (0, 0, im.width, im.height))

manifest = {}
for f in sorted(SRC.glob("*.png")):
    im = Image.open(f)
    kind = classify(im)
    stem = f.stem
    if kind == "emblem":
        out = knockout(im)
        cap = 1500 if out.width / max(out.height, 1) > 2.5 else 520
        if out.width > cap:
            out = out.resize((cap, round(out.height * cap / out.width)), Image.LANCZOS)
        # line art needs few colours; quantising keeps the alpha and cuts size ~5x
        out = out.quantize(colors=64, method=Image.FASTOCTREE)
        name = f"{stem}.png"
        out.save(DEST / name, optimize=True)
    else:
        out = im.convert("RGB")
        cap = 1500
        if out.width > cap:
            out = out.resize((cap, round(out.height * cap / out.width)), Image.LANCZOS)
        name = f"{stem}.jpg"
        out.save(DEST / name, quality=82, optimize=True, progressive=True)
    manifest[f.name] = {"kind": kind, "file": name,
                        "w": out.width, "h": out.height,
                        "kb": round((DEST / name).stat().st_size / 1024, 1)}

json.dump(manifest, open("/home/claude/vallam/art_manifest.json", "w"), indent=1)

tot = sum(v["kb"] for v in manifest.values())
from collections import Counter
print(Counter(v["kind"] for v in manifest.values()))
print(f"{len(manifest)} assets, {tot:.0f} KB total")
for k, v in sorted(manifest.items(), key=lambda x: -x[1]["kb"])[:6]:
    print(f"  heaviest: {v['file']:<20} {v['w']}x{v['h']:<6} {v['kb']} KB  ({v['kind']})")
