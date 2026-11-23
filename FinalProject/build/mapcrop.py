"""Cut a locator tile per neighbourhood from the Vallam map using its grid reference."""
from PIL import Image
import pathlib, json

MAP  = "/mnt/user-data/attachments/ff01b069-a533-5842-b85e-98d30395b651/c8fcdc7c-image.png"
DEST = pathlib.Path("/home/claude/work/GitHub/Intro-to-Web-Desgn/Assignment7/images")
DEST.mkdir(parents=True, exist_ok=True)

# inner neat-line of the mapped area, measured from the frame rules
X0, Y0, X1, Y1 = 166, 166, 5166, 6833
COLS, ROWS = 18, 24
CW, CH = (X1 - X0) / COLS, (Y1 - Y0) / ROWS

# grid references as printed in the map's own neighbourhood index
PLACES = {
    "aldenmere": "P10", "aldenshore": "N9",  "ashford": "D11",
    "confluence": "J14", "coppergate": "G11", "fenwick": "E7",
    "greenvale": "N14", "ironside": "G15",  "merchant-district": "J11",
    "millfield": "D16", "narrows": "M11",   "old-strand": "P7",
    "sovereign-quarter": "I22", "terrace": "I19", "galmier-archipelago": "M4",
}

SPAN = 5          # tile covers 5x5 reference squares
OUT  = 560        # delivered pixel size

def cell(ref):
    letter, num = ref[0].upper(), int(ref[1:])
    return ord(letter) - 65, num - 1

im = Image.open(MAP).convert("RGB")
man = {}
for name, ref in PLACES.items():
    c, r = cell(ref)
    cx, cy = X0 + (c + 0.5) * CW, Y0 + (r + 0.5) * CH
    half = SPAN * CW / 2
    box = (cx - half, cy - half, cx + half, cy + half)
    # keep the tile inside the mapped area
    dx = min(0, box[0] - X0) + max(0, box[2] - X1)
    dy = min(0, box[1] - Y0) + max(0, box[3] - Y1)
    box = (box[0] - dx, box[1] - dy, box[2] - dx, box[3] - dy)
    tile = im.crop(tuple(round(v) for v in box)).resize((OUT, OUT), Image.LANCZOS)
    f = f"map-{name}.jpg"
    tile.save(DEST / f, quality=80, optimize=True, progressive=True)
    man[name] = {"ref": ref, "file": f, "kb": round((DEST / f).stat().st_size / 1024, 1)}

full = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
full.save(DEST / "map-vallam-full.jpg", quality=78, optimize=True, progressive=True)
man["_full"] = {"file": "map-vallam-full.jpg",
                "kb": round((DEST / "map-vallam-full.jpg").stat().st_size / 1024, 1)}

json.dump(man, open("/home/claude/vallam/map_manifest.json", "w"), indent=1)
print(f"{len(PLACES)} locator tiles + full map")
print(f"tiles total: {sum(v['kb'] for k, v in man.items() if k != '_full'):.0f} KB"
      f" | full map: {man['_full']['kb']} KB")
