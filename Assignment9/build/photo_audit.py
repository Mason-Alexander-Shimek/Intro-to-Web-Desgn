"""Checks that only exist because the site now carries photographs.

Two things the old audit could not see:

1. Text sitting on an image. The contrast check in audit.py walks up the DOM
   looking for a painted background colour and gives up when it meets a
   background image, so the hero overlay was never actually measured. Here the
   text is made invisible, the hero is photographed, and the real pixels behind
   each line are sampled.

2. What a browser downloads. Pages are served over HTTP and the bytes on the
   wire are counted, so srcset picks the file a real visitor would get instead
   of the whole ladder being counted at once.
"""
import asyncio, functools, http.server, mimetypes, pathlib, socketserver, threading, io
from PIL import Image
from playwright.async_api import async_playwright

A = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "housing.html", "food.html", "utilities.html",
         "health.html", "transport.html", "about.html"]

# Budgets. Phones on two bars are the design target, so these are hard numbers
# rather than good intentions.
BUDGET_FIRST = 80 * 1024    # everything needed before the first scroll
BUDGET_TOTAL = 190 * 1024   # the whole page, images included

mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("image/webp", ".webp")


def serve(directory):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=str(directory))
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def srgb(v):
    v /= 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def lum(rgb):
    r, g, b = (srgb(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# Every text element painted over a photograph, with the ratio WCAG AA asks of
# it at its own size and weight.
OVERLAY_JS = r"""() => {
  const out = [];
  document.querySelectorAll('.hero-overlay p, .hero-overlay h1').forEach(el => {
    const cs = getComputedStyle(el);
    const r  = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const m = cs.color.match(/\d+(\.\d+)?/g).slice(0, 3).map(Number);
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight) || 400;
    out.push({
      sel: el.tagName + '.' + (el.className || ''),
      text: el.textContent.trim().slice(0, 34),
      color: m, size, weight,
      need: (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3.0 : 4.5,
      box: {x: r.x, y: r.y, w: r.width, h: r.height},
    });
  });
  const h = document.querySelector('.hero');
  const hr = h ? h.getBoundingClientRect() : null;
  return {items: out, hero: hr ? {x: hr.x, y: hr.y, w: hr.width, h: hr.height} : null};
}"""

HIDE_TEXT = """.hero-overlay, .hero-overlay * {
  color: rgba(0,0,0,0) !important; text-shadow: none !important; }"""


async def overlay_contrast(pg, width, failures):
    info = await pg.evaluate(OVERLAY_JS)
    if not info["hero"] or not info["items"]:
        return
    # Photograph the hero with the glyphs removed; what is left is the real backdrop.
    handle = await pg.add_style_tag(content=HIDE_TEXT)
    await pg.wait_for_timeout(120)
    hero = info["hero"]
    shot = await pg.screenshot(clip={"x": hero["x"], "y": hero["y"],
                                     "width": hero["w"], "height": hero["h"]})
    await handle.evaluate("e => e.remove()")

    im = Image.open(io.BytesIO(shot)).convert("RGB")
    sx, sy = im.width / hero["w"], im.height / hero["h"]

    for it in info["items"]:
        bx = it["box"]
        l = max(0, int((bx["x"] - hero["x"]) * sx))
        t = max(0, int((bx["y"] - hero["y"]) * sy))
        r = min(im.width,  int((bx["x"] - hero["x"] + bx["w"]) * sx))
        b = min(im.height, int((bx["y"] - hero["y"] + bx["h"]) * sy))
        if r - l < 2 or b - t < 2:
            continue
        region = im.crop((l, t, r, b))
        px = list(region.getdata())
        fg = lum(it["color"])
        rs = sorted(ratio(fg, lum(p)) for p in px)
        worst = rs[0]
        p02 = rs[max(0, int(len(rs) * 0.02))]     # ignore a 2% fringe of outliers
        failing = sum(1 for v in rs if v < it["need"]) / len(rs) * 100

        ok = p02 >= it["need"] and failing < 2.0
        mark = "ok  " if ok else "FAIL"
        print(f"    {mark} {p02:5.2f}:1 (need {it['need']}, worst px {worst:4.2f}, "
              f"{failing:4.1f}% of area below) {it['size']:.0f}px  “{it['text']}”")
        if not ok:
            failures.append(f"{width}px hero: {it['sel']} {p02:.2f}:1 "
                            f"needs {it['need']} ({failing:.1f}% of area fails)")


async def main():
    httpd, port = serve(A)
    base = f"http://127.0.0.1:{port}/"
    failures = []

    async with async_playwright() as pw:
        b = await pw.chromium.launch()

        # ---- what a visitor actually downloads ----------------------------
        print("=" * 18, "transferred weight", "=" * 18)
        print("  (bytes on the wire: srcset picks one file per image)\n")
        for width, label in ((1200, "desktop"), (390, "phone")):
            print(f"  --- {label} @ {width}px ---")
            for n in PAGES:
                ctx = await b.new_context(viewport={"width": width, "height": 900},
                                          device_scale_factor=1)
                pg = await ctx.new_page()
                seen = {}
                pg.on("response", lambda r: seen.setdefault(r.url, r))
                await pg.goto(base + n, wait_until="networkidle")
                # first-screen weight: anything fetched before the fold is eager
                total = first = 0
                for url, resp in seen.items():
                    try:
                        size = len(await resp.body())
                    except Exception:
                        continue
                    total += size
                    if not any(k in url for k in ("mainhall-", "depot-", "locomotive-")):
                        first += size
                over = []
                if first > BUDGET_FIRST: over.append("FIRST-SCREEN OVER")
                if total > BUDGET_TOTAL: over.append("TOTAL OVER")
                print(f"    {n:<15} first screen {first/1024:6.1f} KB   "
                      f"total {total/1024:6.1f} KB   {len(seen)} requests"
                      + ("   " + " ".join(over) if over else ""))
                if over:
                    failures.append(f"{label} {n}: {' '.join(over)} "
                                    f"(first {first/1024:.0f}K, total {total/1024:.0f}K)")
                await ctx.close()
            print()

        # ---- text painted onto a photograph --------------------------------
        print("=" * 15, "contrast over photography", "=" * 15)
        for width in (1200, 700, 390):
            ctx = await b.new_context(viewport={"width": width, "height": 900},
                                      device_scale_factor=1)
            pg = await ctx.new_page()
            await pg.goto(base + "index.html", wait_until="load")
            await pg.wait_for_timeout(300)
            print(f"  viewport {width}px")
            await overlay_contrast(pg, width, failures)
            await ctx.close()

        # ---- layout shift: every img must reserve its box ------------------
        print("\n" + "=" * 20, "layout stability", "=" * 20)
        ctx = await b.new_context(viewport={"width": 390, "height": 900})
        pg = await ctx.new_page()
        for n in PAGES:
            await pg.goto(base + n, wait_until="load")
            bad = await pg.evaluate("""() => {
              const out = [];
              document.querySelectorAll('img').forEach(i => {
                const hasAttrs = i.getAttribute('width') && i.getAttribute('height');
                const ar = getComputedStyle(i.parentElement).aspectRatio;
                const boxed = hasAttrs || (ar && ar !== 'auto');
                if (!boxed) out.push(i.currentSrc.split('/').pop() || i.src);
              });
              return out;
            }""")
            n_img = await pg.evaluate("document.querySelectorAll('img').length")
            print(f"  {n:<15} {n_img} img  " +
                  ("every image reserves its space" if not bad else f"UNRESERVED: {bad}"))
            if bad:
                failures.append(f"{n}: images without reserved space: {bad}")
        await ctx.close()
        await b.close()

    httpd.shutdown()
    print("\n" + "=" * 26, "result", "=" * 26)
    if failures:
        for f in failures:
            print("  !!", f)
        print(f"\n  {len(failures)} problem(s)")
    else:
        print("  weight inside budget, overlay text passes AA on the real pixels,")
        print("  and every image reserves its space before it loads.")
    return failures


if __name__ == "__main__":
    asyncio.run(main())
