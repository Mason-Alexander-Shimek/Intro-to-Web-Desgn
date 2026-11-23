"""Walk the Vallam PDF in reading order and emit a structured content tree."""
import pymupdf, json, re, pathlib, html

SRC = "/mnt/user-data/attachments/ff01b069-a533-5842-b85e-98d30395b651/307c87fb-Vallam_Setting.pdf"
OUT = pathlib.Path("/home/claude/vallam")

doc = pymupdf.open(SRC)

def level(size, bold):
    if size >= 70: return "h1"     # part title: THE WORLD, VALLAM, ORGANIZATIONS
    if size >= 34: return "h2"     # major section: The Great War, The Neighborhoods
    if size >= 19: return "h3"     # section: The Continents, Astralism
    if size >= 13: return "h4"     # entry: a single org, family or neighbourhood
    if size <= 10.5: return "meta" # stat line: "Location: ...", "Precinct: ..."
    return "body"

# ---- 1. flatten the document into typed blocks, in order -------------------
flat = []
for pno in range(len(doc)):
    page = doc[pno]
    for b in sorted(page.get_text("dict")["blocks"], key=lambda b: (b["bbox"][1], b["bbox"][0])):
        if b.get("type") != 0:
            continue
        for ln in b.get("lines", []):
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if not txt:
                continue
            sp = max(ln["spans"], key=lambda s: len(s["text"]))
            lvl = level(round(sp["size"], 1), "bold" in sp["font"].lower())
            flat.append({"p": pno + 1, "lvl": lvl, "t": txt, "y": ln["bbox"][1]})

# ---- 2. join wrapped body lines into paragraphs ---------------------------
BULLET = re.compile(r"^\s*[●○•▪]\s*")
merged = []
for blk in flat:
    t = blk["t"]
    is_b = bool(BULLET.match(t))
    t = BULLET.sub("", t).strip()
    kind = "li" if is_b else blk["lvl"]
    prev = merged[-1] if merged else None
    joinable = (
        prev and kind in ("body", "li") and prev["lvl"] == kind
        and not prev["t"].endswith(("।", "."))  # keep sentence-final breaks soft
    )
    # a wrapped line continues the previous one when the previous did not end a sentence
    if prev and kind == prev["lvl"] and kind in ("body", "li", "meta") \
       and not re.search(r"[.!?:;]['\"’”)]?$", prev["t"]):
        prev["t"] = (prev["t"] + " " + t).strip()
        continue
    # display titles are set across several spans ("FAIRBOURN" + "E"); rejoin them
    if prev and kind in ("h1", "h2", "h3") and prev["lvl"] == kind and prev["p"] == blk["p"] \
       and not re.search(r"[.!?]$", prev["t"]):
        sep = "" if (t[:1].islower() or len(t) == 1) else " "
        prev["t"] = (prev["t"] + sep + t).strip()
        continue
    merged.append({"p": blk["p"], "lvl": kind, "t": t, "y": blk["y"]})

# ---- 3. images, keyed by the page they appear on --------------------------
art_at, seen = [], set()        # (page, y, filename) for every image, in page order
for pno in range(len(doc)):
    page = doc[pno]
    for im in page.get_images(full=True):
        if im[0] in seen:
            continue
        seen.add(im[0])
        rects = page.get_image_rects(im[0])
        y = rects[0].y0 if rects else 0.0
        art_at.append((pno + 1, y, f"p{pno+1:02d}_x{im[0]}.png"))

# ---- 4. build the tree ----------------------------------------------------
tree, h1, h2, h3, h4 = [], None, None, None, None

def node(t, p, y=0.0):
    return {"title": t, "page": p, "y": y, "body": [], "meta": [], "art": [], "children": []}

for blk in merged:
    lvl, t, p = blk["lvl"], blk["t"], blk["p"]
    if lvl == "h1":
        h1 = node(t, p, blk["y"]); tree.append(h1); h2 = h3 = h4 = None
    elif lvl == "h2":
        if h1 is None:
            h1 = node("Introduction", p); tree.append(h1)
        h2 = node(t, p, blk["y"]); h1["children"].append(h2); h3 = h4 = None
    elif lvl == "h3":
        parent = h2 or h1
        if parent is None:
            h1 = node("Introduction", p); tree.append(h1); parent = h1
        h3 = node(t, p, blk["y"]); parent["children"].append(h3); h4 = None
    elif lvl == "h4":
        parent = h3 or h2 or h1
        if parent is None:
            h1 = node("Introduction", p); tree.append(h1); parent = h1
        h4 = node(t, p, blk["y"]); parent["children"].append(h4)
    else:
        cur = h4 or h3 or h2 or h1
        if cur is None:
            h1 = node("Introduction", p); tree.append(h1); cur = h1
        if lvl == "meta":
            cur["meta"].append(t)
        elif lvl == "li":
            cur["body"].append({"li": t})
        else:
            cur["body"].append({"p": t})

# attach each image to the LAST heading that opens at or above it in the document
def flatten(nodes, acc):
    for n in nodes:
        acc.append(n)
        flatten(n["children"], acc)
    return acc

ordered = sorted(flatten(tree, []), key=lambda n: (n["page"], n["y"]))
placed = 0
for pg, y, name in art_at:
    owner = None
    for n in ordered:
        if (n["page"], n["y"]) <= (pg, y):
            owner = n
        else:
            break
    (owner or tree[0])["art"].append(name)
    placed += 1
json.dump(tree, open(OUT / "lore.json", "w"), indent=1, ensure_ascii=False)

def count(nodes, d=0):
    n = 0
    for x in nodes:
        n += 1 + count(x["children"], d + 1)
    return n

print(f"top-level parts : {len(tree)}")
print(f"total nodes     : {count(tree)}")
print(f"images on pages : {placed}")
print()
for t in tree:
    kids = ", ".join(c["title"][:28] for c in t["children"][:7])
    print(f"  {t['title'][:34]:<34} ({len(t['children'])} sections)  {kids}")
