import json, html, re, pathlib, unicodedata, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from icons import icon

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
SITE, CATS = C["site"], C["categories"]
PHOTOS = json.loads((HERE / "photos.json").read_text(encoding="utf-8"))

MIME = {"avif": "image/avif", "webp": "image/webp", "jpg": "image/jpeg"}


def srcset(use, ext):
    # The JPEG fallback has a shorter ladder than AVIF and WebP; see images.py.
    ws = PHOTOS[use]["jpg_widths"] if ext == "jpg" else PHOTOS[use]["widths"]
    return ", ".join(f"images/photos/{use}-{w}.{ext} {w}w" for w in ws)


def picture(layers, sizes, alt, cls="", *, priority=False):
    """Build a <picture>.

    layers is [(use, media)] from most specific to least; media None is the
    default layer and supplies the <img> fallback. AVIF first, then WebP, then
    JPEG, because the browser takes the first type it recognises.
    """
    out = []
    for use, media in layers:
        m = f' media="{media}"' if media else ""
        for ext in ("avif", "webp"):
            out.append(f'<source{m} type="{MIME[ext]}" srcset="{srcset(use, ext)}" sizes="{sizes}">')
        if media:
            out.append(f'<source{m} type="{MIME["jpg"]}" srcset="{srcset(use, "jpg")}" sizes="{sizes}">')

    base = layers[-1][0]
    w, h = PHOTOS[base]["intrinsic"]["w"], PHOTOS[base]["intrinsic"]["h"]
    loading = ('loading="eager" fetchpriority="high"' if priority
               else 'loading="lazy" decoding="async"')
    out.append(
        f'<img src="images/photos/{base}-{PHOTOS[base]["jpg_widths"][-1]}.jpg" '
        f'srcset="{srcset(base, "jpg")}" sizes="{sizes}" '
        f'width="{w}" height="{h}" {loading} alt="{esc(alt)}">')
    return f'<picture class="{cls}">' + "".join(out) + "</picture>"


# The shell is 900px with a 20px gutter, so the widest an in-flow image ever
# renders is 860px. Telling the browser that stops it fetching a larger file.
SIZES_FULL = "(min-width: 940px) 860px, (min-width: 761px) calc(100vw - 40px), calc(100vw - 32px)"
SIZES_CARD = "(min-width: 940px) 276px, (min-width: 621px) calc((100vw - 104px) / 3), calc(100vw - 32px)"

def esc(s): return html.escape(s, quote=False)

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s-]", "", s).strip().lower())[:50]

def tel(p):
    return re.sub(r"[^\d+]", "", p)

NAV = ([("index.html", "Start here")]
       + [(f"{c['id']}.html", c["name"]) for c in CATS]
       + [("about.html", "About")])

def items(lst, tag="ul"):
    return f"<{tag}>" + "".join(f"<li>{esc(x)}</li>" for x in lst) + f"</{tag}>"

def phone_link(p, cls="call-link"):
    mark = icon("phone", 20, "icon call-icon")
    if p.strip() == "988":
        return f'<a class="{cls}" href="tel:988">{mark}Call or text 988</a>'
    return f'<a class="{cls}" href="tel:{tel(p)}">{mark}{esc(p)}</a>'

def where_block(w):
    rows = []
    if w.get("call_first"):
        rows.append('<div class="where-row call-first"><dt>Call first</dt>'
                    '<dd>Do not turn up without calling. You may be turned away.</dd></div>')
    rows.append(f"""<div class="where-row"><dt>Address</dt><dd>{esc(w['address'])}</dd></div>""")
    rows.append(f"""<div class="where-row"><dt>Open</dt><dd>{esc(w['hours'])}</dd></div>""")
    if w.get("bus"):
        rows.append(f"""<div class="where-row"><dt>Bus</dt><dd>{esc(w['bus'])}</dd></div>""")
    rows.append(f"""<div class="where-row"><dt>Phone</dt><dd>{phone_link(w['phone'])}</dd></div>""")
    return '<dl class="where-block">' + "".join(rows) + "</dl>"

def listing(l):
    sid = slug(l["name"])
    return f"""<article class="listing" id="{sid}">
<h2>{esc(l['name'])}</h2>
<p class="run-by">Run by {esc(l['run_by'])}</p>
<p class="summary">{esc(l['summary'])}</p>
<div class="answers">
  <section class="answer"><h3>Do I qualify?</h3>{items(l['qualify'])}</section>
  <section class="answer"><h3>What do I bring?</h3>{items(l['bring'])}</section>
  <section class="answer"><h3>How do I apply?</h3>{items(l['apply'], 'ol')}</section>
  <section class="answer answer-where"><h3>Where and when?</h3>{where_block(l['where'])}</section>
</div>
</article>"""

def checklist(cat):
    blocks = []
    for l in cat["listings"]:
        ticks = "".join(
            f'<li><span class="tick" aria-hidden="true"></span>{esc(b)}</li>' for b in l["bring"])
        blocks.append(f"""<section class="check-block"><h3>{esc(l['name'])}</h3>"""
                      f'<ul class="ticks">{ticks}</ul></section>')
    return f"""<section class="checklist" id="what-to-bring">
<h2>{icon("printer", 26, "icon head-icon")}What to bring</h2>
<p class="checklist-note">Print this page, or photograph it. Tick things off as you find them.
Taking the right papers the first time is the difference between one trip and three.</p>
{''.join(blocks)}
</section>"""

def shell(page, title, desc, body, cls=""):
    nav = "".join(
        f'<li><a href="{h}"{" class=\"here\" aria-current=\"page\"" if h == page else ""}>{esc(t)}</a></li>'
        for h, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} &mdash; {esc(SITE['name'])}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="styles/styles.css">
</head>
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>

<nav class="site-nav" aria-label="Main">
  <a class="brand" href="index.html">{icon("door", 30, "icon brand-mark")}<span class="brand-text">{esc(SITE["name"])}</span></a>
  <ul class="nav-links">{nav}</ul>
</nav>

<p class="demo-banner" role="note"><b>Demonstration site.</b> {esc(SITE['demo_notice'])}</p>

<main id="main">
{body}
</main>

<footer class="site-foot">
  <p class="foot-rules">{" &middot; ".join(esc(r) for r in SITE['rules'])}</p>
  <p>This site keeps no accounts and sets no tracking cookies. Nothing you read here is recorded.</p>
  <p class="foot-meta">Mason Shimek &middot; Intro to Web Design &middot; Assignment 9</p>
</footer>
</body>
</html>"""

pages = {}

# ---- start page ------------------------------------------------------------
cards = "".join(f"""<a class="need-card" href="{c['id']}.html">
<span class="need-icon">{icon(c["icon"], 34)}</span>
<span class="need-name">{esc(c['name'])}</span>
<span class="need-short">{esc(c['short'])}</span>
<span class="need-go">See {len(c['listings'])} ways to get help &rsaquo;</span></a>"""
    for c in CATS)

rules = "".join(f'<li class="rule">{esc(r)}</li>' for r in SITE["rules"])

hero_media = picture(
    [("hero-narrow", "(max-width: 700px)"), ("hero-wide", None)],
    SIZES_FULL, PHOTOS["hero-wide"]["alt"], "hero-media", priority=True)

home = f"""<section class="hero">
{hero_media}
<div class="hero-overlay">
<p class="hero-eyebrow">{esc(SITE["tagline_short"])} Missoula County, Montana.</p>
<h1>What do you need help with?</h1>
<p class="lede hero-lede">{esc(SITE['tagline'])}</p>
</div>
</section>

<nav class="need-grid" aria-label="Choose what you need">{cards}</nav>

<section class="urgent-card urgent-home">
<h2>{icon("alert-circle", 26, "icon head-icon")}If you need something tonight</h2>
<p>Every page has a number at the top for the thing that cannot wait. You do not need to read
the page first. Call the number, say what has happened, and someone will tell you what to do next.</p>
<p class="urgent-note">If you are in crisis, or worried about someone, call or text 988 at any time.</p>
<p class="urgent-call"><a class="call-link call-big" href="tel:988">Call or text 988</a>
<span class="urgent-hours">24 hours, every day</span></p>
</section>

<section class="rules-section">
<h2>How this site works</h2>
<ul class="rules-strip">{rules}</ul>
<p class="rules-note">Every listing answers the same four questions in the same order:
<b>Do I qualify? What do I bring? How do I apply? Where and when?</b>
Learn that once and every other listing takes ten seconds.</p>
</section>

<a class="preview preview-wide" href="about.html">
{picture([("depot", None)], SIZES_CARD, PHOTOS["depot"]["alt"], "preview-media")}
<span class="preview-body">
<span class="preview-label">About</span>
<span class="preview-title">Who runs this, and how it stays current</span>
<span class="preview-text">What the site is for, who it is built for, and the one
question about keeping listings up to date that is still open.</span>
<span class="preview-go">Read about this site &rsaquo;</span>
</span>
</a>"""

pages["index.html"] = shell("index.html", "Start here", SITE["tagline"], home, "is-home")

# ---- category pages --------------------------------------------------------
for c in CATS:
    u = c["urgent"]
    jump = "".join(f"""<li><a href="#{slug(l['name'])}">{esc(l['name'])}</a></li>"""
                   for l in c["listings"])
    body = f"""<header class="page-head page-head-icon">
<h1>{icon(c["icon"], 38, "icon title-icon")}{esc(c['name'])}</h1>
<p class="lede">{esc(c['lede'])}</p>
</header>

<section class="urgent-card">
<h2>{icon("alert-circle", 26, "icon head-icon")}{esc(u['label'])}</h2>
<p>{esc(u['body'])}</p>
<p class="urgent-call">{phone_link(u['phone'], 'call-link call-big')}
<span class="urgent-hours">{esc(u['hours'])}</span></p>
</section>

<nav class="jump-nav" aria-label="Listings on this page">
<p class="jump-head">On this page</p>
<ul class="jump-list">{jump}</ul>
</nav>

{''.join(listing(l) for l in c['listings'])}

{checklist(c)}"""
    pages[f"{c['id']}.html"] = shell(f"{c['id']}.html", c["name"], c["lede"], body,
                                     f"is-cat is-{c['id']}")

# ---- about page ------------------------------------------------------------
A = C["about"]

sections = "".join(
    f"""<section class="about-block"><h2>{esc(s['h'])}</h2>"""
    + "".join(f"<p>{esc(t)}</p>" for t in s["p"]) + "</section>"
    for s in A["sections"])

places = "".join(f"""<article class="preview">
{picture([(pl["use"], None)], SIZES_CARD, PHOTOS[pl["use"]]["alt"], "preview-media")}
<div class="preview-body">
<p class="preview-label">{esc(pl['label'])}</p>
<h3 class="preview-title">{esc(pl['title'])}</h3>
<p class="preview-text">{esc(pl['text'])}</p>
</div>
</article>""" for pl in A["places"])

contact_rows = "".join(
    f'<div class="where-row"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>'
    for k, v in A["contact"]["rows"])

about = f"""<figure class="valley-band">
{picture([("valley-band", None)], SIZES_FULL, PHOTOS["valley-band"]["alt"], "valley-media",
         priority=True)}
<figcaption>{esc(PHOTOS["valley-band"]["credit"])}. The Clark Fork runs through the
middle of the valley, and most of what this site lists is within a few miles of it.</figcaption>
</figure>

<header class="page-head">
<h1>About {esc(SITE['name'])}</h1>
<p class="lede">{esc(A['lede'])}</p>
</header>

{sections}

<section class="about-block">
<h2>{icon("map-pin", 26, "icon head-icon")}Places in Missoula</h2>
<div class="preview-row">{places}</div>
</section>

<section class="contact-card">
<h2>{icon("phone", 26, "icon head-icon")}Contact</h2>
<p class="contact-intro">{esc(A['contact']['intro'])}</p>
<dl class="where-block">{contact_rows}</dl>
<p class="contact-real">{esc(A['contact']['real'])}</p>
<p class="urgent-call"><a class="call-link call-big" href="tel:988">Call or text 988</a>
<span class="urgent-hours">24 hours, every day</span></p>
</section>"""

pages["about.html"] = shell("about.html", "About", A["lede"], about, "is-about")

for name, src in pages.items():
    (ROOT / name).write_text(src, encoding="utf-8")
    print(f"{name:<16} {len(src)/1024:5.1f} KB")

n_listings = sum(len(c["listings"]) for c in CATS)
print(f"\n{len(pages)} pages, {n_listings} listings, each with "
      f"{len(SITE['questions'])} answers in a fixed order")
