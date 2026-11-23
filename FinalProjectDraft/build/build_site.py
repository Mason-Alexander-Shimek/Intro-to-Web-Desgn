"""Generate the Vallam lore site from the extracted lore tree."""
import json, re, html, pathlib, unicodedata

ROOT = pathlib.Path("/home/claude/work/GitHub/Intro-to-Web-Desgn/Assignment7")
LORE = json.load(open("/home/claude/vallam/lore.json"))
ART  = json.load(open("/home/claude/vallam/art_manifest.json"))
MAPS = json.load(open("/home/claude/vallam/map_manifest.json"))

def esc(s): return html.escape(s, quote=False)

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[\s_]+", "-", s)[:60]

def artfile(name):
    return ART.get(name, {}).get("file")

def kind(name):
    return ART.get(name, {}).get("kind")

def first(node, want):
    for a in node["art"]:
        if kind(a) == want: return artfile(a)
    return None

# ---------- content fragments -------------------------------------------------
def body_html(node, cls="lore-copy"):
    out = []
    buf = []
    for b in node["body"]:
        if "li" in b:
            buf.append(f"<li>{esc(b['li'])}</li>")
        else:
            if buf: out.append("<ul class='lore-list'>" + "".join(buf) + "</ul>"); buf = []
            out.append(f"<p>{esc(b['p'])}</p>")
    if buf: out.append("<ul class='lore-list'>" + "".join(buf) + "</ul>")
    return f"<div class='{cls}'>" + "".join(out) + "</div>" if out else ""

def dossier(node):
    if not node["meta"]: return ""
    rows = []
    for m in node["meta"]:
        if ":" in m[:28]:
            k, v = m.split(":", 1)
            rows.append(f"<div class='dossier-row'><dt>{esc(k.strip())}</dt><dd>{esc(v.strip())}</dd></div>")
        else:
            # family seats are descriptions, not labelled fields
            rows.append(f"<p class='seat-line'>{esc(m)}</p>")
    if all(r.startswith("<p") for r in rows):
        return "".join(rows)
    return "<dl class='dossier'>" + "".join(rows) + "</dl>"

def crest_tile(node):
    """Uniform, short, scannable: the right shape for a Grid."""
    crest = first(node, "emblem")
    fig = (f"<img src='images/{crest}' alt='' loading='lazy'>" if crest
           else "<span class='crest-absent' aria-hidden='true'>&#9670;</span>")
    return (f"<a class='crest-tile' href='#{slug(node['title'])}'>"
            f"<span class='tile-crest'>{fig}</span>"
            f"<span>{esc(node['title'])}</span></a>")

def crest_index(group, label="Jump to"):
    tiles = "".join(crest_tile(e) for e in group["children"])
    return (f"<p class='index-head'>{esc(label)}</p>"
            f"<nav class='crest-index' aria-label='{esc(label)}'>{tiles}</nav>")

def entry_row(node):
    """130-300 words each: variable length, so one full-width row apiece,
       not a uniform card that would stretch to the longest entry."""
    crest = first(node, "emblem")
    fig = (f"<div class='row-crest'><img src='images/{crest}' alt='Emblem of "
           f"{esc(node['title'])}' loading='lazy'></div>") if crest else ""
    return f"""<article class="entry-row" id="{slug(node['title'])}">
{fig}<div class="row-body"><h3>{esc(node['title'])}</h3>
{dossier(node)}{body_html(node, 'entry-copy')}</div></article>"""

PLACE_TILE = {
    "the confluence": "confluence", "the merchant district": "merchant-district",
    "the terrace and the sovereign quarter": "terrace", "greenvale": "greenvale",
    "aldenmere": "aldenmere", "ironside": "ironside", "millfield": "millfield",
    "ashford": "ashford", "fenwick": "fenwick",
}

def place_tile(node):
    t = PLACE_TILE.get(node["title"].lower())
    if not t: return ""
    ref = MAPS[t]["ref"]
    return (f"<a class='place-tile' href='#{slug(node['title'])}'>"
            f"<img src='images/{MAPS[t]['file']}' alt='' loading='lazy'>"
            f"<span class='tile-name'>{esc(node['title'])}</span>"
            f"<span class='tile-ref'>{esc(ref)}</span></a>")

def place_section(node):
    """308-1250 words each: long-form, so the locator sits in its own column
       and the prose runs full height beside it."""
    t = PLACE_TILE.get(node["title"].lower())
    fig = ""
    if t:
        ref = MAPS[t]["ref"]
        fig = (f"<figure class='place-locator'>"
               f"<img src='images/{MAPS[t]['file']}' alt='Map detail showing "
               f"{esc(node['title'])}' loading='lazy'>"
               f"<figcaption>Reference square {esc(ref)}</figcaption></figure>")
    return f"""<section class="place-section" id="{slug(node['title'])}">
<h3>{esc(node['title'])}</h3>
<div class="place-split">{fig}<div class="place-copy">{body_html(node, 'copy-inner')}</div></div>
</section>"""

def lore_section(node, level=2):
    bits = [f"<section class='lore-section' id='{slug(node['title'])}'>",
            f"<h{level}>{esc(node['title'])}</h{level}>"]
    band = first(node, "banner") or first(node, "scene")
    if band:
        bits.append(f"<figure class='figure-band'><img src='images/{band}' alt='' loading='lazy'></figure>")
    crest = first(node, "emblem")
    if crest:
        bits.append(f"<figure class='figure-crest'><img src='images/{crest}' alt='' loading='lazy'></figure>")
    bits.append(body_html(node))
    bits.append(dossier(node))
    for ch in node["children"]:
        bits.append(lore_section(ch, min(level + 1, 4)))
    bits.append("</section>")
    return "".join(bits)

# ---------- page shell --------------------------------------------------------
NAV = [("index.html", "Home"), ("world.html", "The World"), ("dominion.html", "Fairbourne"),
       ("vallam.html", "Vallam"), ("factions.html", "Factions"), ("houses.html", "Houses")]

FONTS = ("https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700"
         "&family=Josefin+Sans:wght@300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap")

def shell(page, title, standfirst, theme, hero, body, rail=None, extra_class=""):
    nav = "".join(
        f"<li><a href='{h}'{' class=\"here\" aria-current=\"page\"' if h == page else ''}>{esc(t)}</a></li>"
        for h, t in NAV)
    railhtml = ""
    if rail:
        items = "".join(f"<li><a href='#{slug(t)}'>{esc(t)}</a></li>" for t in rail)
        railhtml = f"<nav class='toc-rail' aria-label='On this page'><p class='rail-head'>On this page</p><ul>{items}</ul></nav>"
    layout = (f"<div class='layout'>{railhtml}<div class='layout-main'>{body}</div></div>"
              if rail else f"<div class='layout-single'>{body}</div>")
    herohtml = ""
    if hero:
        img, kicker = hero
        herohtml = f"""<header class="hero-plate">
<img class="hero-img" src="images/{img}" alt="" >
<div class="hero-text"><p class="kicker">{esc(kicker)}</p>
<h1>{esc(title)}</h1><p class="standfirst">{esc(standfirst)}</p></div></header>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} &mdash; Vallam</title>
<meta name="description" content="{esc(standfirst[:150])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="styles/styles.css">
</head>
<body class="page-{theme} {extra_class}">
<a class="skip" href="#main">Skip to content</a>
<nav class="site-nav" aria-label="Main">
  <a class="brand" href="index.html"><span class="brand-mark">&#10022;</span> VALLAM</a>
  <ul class="nav-links">{nav}</ul>
</nav>
{herohtml}
<main id="main">
{layout}
</main>
<footer class="site-foot">
  <p class="foot-mark">VALLAM</p>
  <p>A lore reference for an eldritch mystery campaign set on Morphe, Anno 1926.</p>
  <p class="foot-meta">Mason Shimek &middot; Intro to Web Design &middot; Assignment 7</p>
</footer>
</body>
</html>"""

# ---------- find the parts ----------------------------------------------------
def part(title):
    for p in LORE:
        if p["title"].lower().startswith(title.lower()): return p
    raise SystemExit(f"part not found: {title}")

world, religions = part("The World"), part("The Religions")
fairbourne, vallam, orgs = part("FAIRBOURNE"), part("VALLAM"), part("Organizations")

pages = {}

# ---------- 2. world ----------------------------------------------------------
rail = [c["title"] for c in world["children"]] + [c["title"] for c in religions["children"]]
body = (f"<section class='part-intro'><h2 class='sr-only'>Morphe</h2>{body_html(world)}</section>"
        + "".join(lore_section(c) for c in world["children"])
        + "<h2 class='cat-head' id='the-religions'>The Religions</h2>"
        + "".join(lore_section(c) for c in religions["children"]))
pages["world.html"] = shell("world.html", "The World",
    "Morphe: a older, larger world at Earth's distance from its sun, where the oceans decide everything.",
    "world", (ART["p01_x9.png"]["file"], "Part One"), body, rail)

# ---------- 3. dominion -------------------------------------------------------
rail = [c["title"] for c in fairbourne["children"]]
body = (f"<section class='part-intro'>{body_html(fairbourne)}</section>"
        + "".join(lore_section(c) for c in fairbourne["children"]))
pages["dominion.html"] = shell("dominion.html", "Fairbourne",
    "The Dominion, its Crown and Parliament, and the war that has not stopped since 1903.",
    "dominion", (ART["p12_x41.png"]["file"], "Part Two"), body, rail)

# ---------- 4. vallam ---------------------------------------------------------
culture = next(c for c in vallam["children"] if c["title"].lower() == "culture")
hoods   = next(c for c in vallam["children"] if "neighborhood" in c["title"].lower())
places  = [c for c in hoods["children"] if c["title"].lower() not in ("a gazetteer.",)]
rail = [c["title"] for c in culture["children"]] + ["The Neighbourhoods"] + [p["title"] for p in places]

located = [p for p in places if p["title"].lower() in PLACE_TILE]
index_tiles = "".join(place_tile(p) for p in located)
cards = "".join(place_section(p) for p in located)
longform = "".join(lore_section(p) for p in places if p["title"].lower() not in PLACE_TILE)
extra = "".join(
    f"<li><a href='#'><img src='images/{MAPS[k]['file']}' alt='' loading='lazy'>"
    f"<span>{k.replace('-', ' ').title()}</span><em>{MAPS[k]['ref']}</em></a></li>"
    for k in ("aldenshore", "coppergate", "narrows", "old-strand", "galmier-archipelago"))

body = (f"<section class='part-intro'>{body_html(vallam)}</section>"
        + "".join(lore_section(c) for c in culture["children"])
        + "<h2 class='cat-head' id='the-neighbourhoods'>The Neighbourhoods</h2>"
        + f"<figure class='figure-band figure-map'><img src='images/{MAPS['_full']['file']}'"
          " alt='A new plan of the city of Vallam, 1926' loading='lazy'>"
          "<figcaption>Hale &amp; Corrigan, Map-Makers, Millfield &middot; New Edition, revised to Anno 1926."
          " Each reference square is three-quarters of a mile.</figcaption></figure>"
        + "<p class='index-head'>Jump to a neighbourhood</p>"
        + f"<nav class='place-index' aria-label='Neighbourhoods'>{index_tiles}</nav>"
        + cards
        + f"<h3 class='sub-head'>Also on the plan</h3><ul class='tile-strip'>{extra}</ul>"
        + longform)
pages["vallam.html"] = shell("vallam.html", "Vallam",
    "Capital of the Dominion of Fairbourne. Six and a half million people on a drowned river mouth.",
    "vallam", (ART["p18_x56.png"]["file"], "Part Three"), body, rail)

# ---------- 5. factions -------------------------------------------------------
cats = orgs["children"][:6]
rail = [c["title"].title() for c in cats]
chunks = []
for c in cats:
    band = first(c, "banner") or first(c, "scene")
    chunks.append(f"<h2 class='cat-head' id='{slug(c['title'])}'>{esc(c['title'].title())}</h2>")
    if band:
        chunks.append(f"<figure class='figure-band'><img src='images/{band}' alt='' loading='lazy'></figure>")
    chunks.append(body_html(c))
    chunks.append(crest_index(c))
    chunks.append("<div class='entry-list'>" + "".join(entry_row(e) for e in c["children"]) + "</div>")
body = f"<section class='part-intro'>{body_html(orgs)}</section>" + "".join(chunks)
pages["factions.html"] = shell("factions.html", "Factions",
    "Who holds power in Vallam, who prints the news, who prays, and who is watching.",
    "factions", (ART["p43_x115.png"]["file"], "Part Four"), body, rail)

# ---------- 6. houses ---------------------------------------------------------
fam  = orgs["children"][6]
crim = orgs["children"][7]
rail = [e["title"] for e in fam["children"]] + [e["title"] for e in crim["children"]]
band = first(fam, "banner") or first(fam, "scene")
cband = first(crim, "banner") or first(crim, "scene")
body = (f"<h2 class='cat-head' id='{slug(fam['title'])}'>{esc(fam['title'].title())}</h2>"
        + (f"<figure class='figure-band'><img src='images/{band}' alt='' loading='lazy'></figure>" if band else "")
        + body_html(fam)
        + crest_index(fam, "The nine houses")
        + "<div class='entry-list'>" + "".join(entry_row(e) for e in fam["children"]) + "</div>"
        + f"<h2 class='cat-head break' id='{slug(crim['title'])}'>{esc(crim['title'].title())}</h2>"
        + (f"<figure class='figure-band'><img src='images/{cband}' alt='' loading='lazy'></figure>" if cband else "")
        + body_html(crim)
        + crest_index(crim, "The outfits")
        + "<div class='entry-list'>" + "".join(entry_row(e) for e in crim["children"]) + "</div>")
pages["houses.html"] = shell("houses.html", "Houses & the Underworld",
    "Nine families hold Aldenmere. Seven organisations hold everything the families will not touch.",
    "houses", (ART["p55_x149.png"]["file"] if "p55_x149.png" in ART else ART["p48_x128.png"]["file"], "Part Five"),
    body, rail)

# ---------- 1. home -----------------------------------------------------------
GATE = [
    ("world.html", "The World", "p07_x27.png",
     "Morphe, its moon and its oceans. Why nobody crosses the Nihil, and what lives under it."),
    ("dominion.html", "Fairbourne", "p38_x102.png",
     "The Crown, Parliament, and a war that began in 1903 and has not formally ended."),
    ("vallam.html", "Vallam", "p39_x105.png",
     "Six and a half million people, twelve neighbourhoods, and a prohibition nobody keeps."),
    ("factions.html", "Factions", "p40_x108.png",
     "Police, press, clubs and the Suppression Bureau, which removes books that notice too much."),
    ("houses.html", "Houses", "p57_x156.png",
     "Nine families on the hill. Seven outfits below it. Every one of them has a crest."),
]
gates = "".join(
    f"""<a class="gateway-card" href="{h}">
<span class="gate-crest"><img src="images/{ART[c]['file']}" alt="" loading="lazy"></span>
<span class="gate-name">{esc(n)}</span><span class="gate-copy">{esc(d)}</span></a>"""
    for h, n, c, d in GATE)

home_body = f"""<section class="part-intro">
<p>This is a reference for players, not a novel. It opens on the broad shape of the world and
narrows, section by section, until it reaches a single street in Vallam.</p>
<p>Nothing here needs reading in order. Every part has its own index, every organisation its own
entry, and every neighbourhood its place on the plan. Start wherever your question is.</p>
</section>
<div class="gateway-grid">{gates}</div>
<figure class="figure-band figure-map">
<img src="images/{MAPS['_full']['file']}" alt="A new plan of the city of Vallam, 1926" loading="lazy">
<figcaption>A New Plan of the City of Vallam &middot; Anno 1926 &middot; Population 6,500,000.
<a href="vallam.html#the-neighbourhoods">Go to the neighbourhood index &rsaquo;</a></figcaption>
</figure>
<blockquote class="pull"><p>What is permitted for others is not permitted for you.</p>
<cite>&mdash; motto on the badge of the Suppression Bureau</cite></blockquote>"""

pages["index.html"] = shell("index.html", "Vallam",
    "A lore reference for an eldritch mystery campaign set on Morphe, Anno 1926.",
    "home", (ART["p35_x94.png"]["file"], "Anno 1926"), home_body, None, "is-home")

for name, src in pages.items():
    (ROOT / name).write_text(src, encoding="utf-8")
    print(f"{name:<16} {len(src)/1024:6.1f} KB")
