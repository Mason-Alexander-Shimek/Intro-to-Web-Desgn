import asyncio, pathlib, re
from playwright.async_api import async_playwright

A = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "housing.html", "food.html", "utilities.html",
         "health.html", "transport.html"]

JS = r"""() => {
  const out = {overflow: [], contrast: [], small_taps: [], headings: [], tiny: []};
  const de = document.documentElement;
  out.scrollW = de.scrollWidth; out.clientW = de.clientWidth;
  if (de.scrollWidth > de.clientWidth + 1) {
    document.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right > de.clientWidth + 1 && r.width > 0)
        out.overflow.push(el.tagName + '.' + (el.className||'').toString().slice(0,30));
    });
    out.overflow = [...new Set(out.overflow)].slice(0, 5);
  }

  const lum = c => { const [r,g,b] = c.map(v => { v/=255;
      return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*r + 0.7152*g + 0.0722*b; };
  const parse = s => { const m = s.match(/\d+(\.\d+)?/g); return m ? m.slice(0,3).map(Number) : null; };
  const bgOf = el => {
    for (let p = el; p; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const c = cs.backgroundColor;
      if (c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) {
        const v = parse(c);
        const a = c.startsWith('rgba') ? parseFloat(c.split(',')[3]) : 1;
        if (v && a > 0.85) return v;
      }
    }
    return [255,255,255];
  };
  const ratio = (f,b) => { const L1=lum(f), L2=lum(b);
    return (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05); };

  document.querySelectorAll('p,h1,h2,h3,li,a,span,dt,dd,b').forEach(el => {
    if (!el.textContent.trim()) return;
    if (el.children.length && !Array.from(el.childNodes).some(n=>n.nodeType===3&&n.textContent.trim())) return;
    const cs = getComputedStyle(el);
    if (cs.visibility==='hidden'||cs.display==='none') return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const fg = parse(cs.color); if (!fg) return;
    const bg = bgOf(el); if (!bg) return;
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight)||400;
    const need = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3.0 : 4.5;
    if (size < 14) out.tiny.push(el.tagName+'.'+(el.className||'').toString().slice(0,24)+' '+size+'px');
    const cr = ratio(fg, bg);
    if (cr < need) out.contrast.push({sel: el.tagName+'.'+(el.className||'').toString().slice(0,28),
                                      ratio:+cr.toFixed(2), need, size,
                                      text: el.textContent.trim().slice(0,30)});
  });
  const seen = {};
  out.contrast.forEach(c => { if (!seen[c.sel] || c.ratio < seen[c.sel].ratio) seen[c.sel] = c; });
  out.contrast = Object.values(seen).sort((a,b)=>a.ratio-b.ratio).slice(0,8);
  out.tiny = [...new Set(out.tiny)].slice(0,5);

  // tap targets: anything you are meant to press
  document.querySelectorAll('a, button').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    if (r.height < 44) out.small_taps.push(
      `${el.textContent.trim().slice(0,26)} — ${Math.round(r.width)}x${Math.round(r.height)}`);
  });
  out.small_taps = [...new Set(out.small_taps)].slice(0, 6);

  let prev = 0;
  document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
    const n = +h.tagName[1];
    if (prev && n > prev + 1) out.headings.push(`h${prev}->h${n}: ${h.textContent.trim().slice(0,30)}`);
    prev = n;
  });
  out.imgs = document.querySelectorAll('img').length;
  return out;
}"""

def check_navigation():
    """Every proposed page exists, every page links to every other, and every
    in-page anchor resolves."""
    import re
    problems, navs = [], {}
    for n in PAGES:
        html = (A / n).read_text(encoding="utf-8")
        ids = set(re.findall(r'id="([^"]+)"', html))
        hrefs = re.findall(r'href="([^"]+)"', html)
        nav = set()
        for h in hrefs:
            if h.startswith(("tel:", "mailto:", "http")):
                continue
            if h.startswith("#"):
                if h[1:] not in ids:
                    problems.append(f"{n}: dead anchor {h}")
            else:
                target = h.split("#")[0]
                if target.endswith(".html"):
                    nav.add(target)
                if target and not (A / target).exists():
                    problems.append(f"{n}: dead link {h}")
        navs[n] = nav
    for n in PAGES:
        missing = set(PAGES) - navs[n] - {n}
        if missing:
            problems.append(f"{n}: nav does not reach {', '.join(sorted(missing))}")
    print("=" * 20, "navigation", "=" * 20)
    if problems:
        for x in problems:
            print("  !!", x)
    else:
        print(f"  all {len(PAGES)} pages exist, link to each other, and every anchor resolves")
    return not problems


async def main():
    check_navigation()

    # ---- transferred weight, which is what "weak signal" actually means
    print("=" * 22, "page weight", "=" * 22)
    css = (A / "styles" / "styles.css").stat().st_size
    worst = 0
    for n in PAGES:
        html = (A / n).read_text(encoding="utf-8")
        hb = len(html.encode("utf-8"))
        # every local asset the page actually requests
        assets = 0
        for src in re.findall(r'(?:src|href)="(?!http|#|tel:|mailto:)([^"]+)"', html):
            f = A / src.split("?")[0]
            if f.suffix in (".svg", ".png", ".jpg", ".jpeg", ".webp", ".woff2") and f.exists():
                assets += f.stat().st_size
        total = hb + css + assets
        worst = max(worst, total)
        extra = f" + art {assets/1024:4.1f} KB" if assets else ""
        print(f"  {n:<15} html {hb/1024:5.1f} KB + css {css/1024:5.1f} KB{extra}"
              f" = {total/1024:5.1f} KB   ~{total*8/56000:4.1f}s on a 56k line")
    svg = len(list((A / "images").glob("*.svg"))) if (A / "images").exists() else 0
    print(f"  heaviest page: {worst/1024:.1f} KB, {svg} vector file(s), 0 photographs, 0 webfonts")

    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1200, 390):
            print(f"\n{'='*20} viewport {w}px {'='*20}")
            pg = await b.new_page(viewport={"width": w, "height": 900})
            for n in PAGES:
                await pg.goto((A / n).as_uri(), wait_until="load")
                await pg.wait_for_timeout(300)
                r = await pg.evaluate(JS)
                flags = []
                if r["overflow"]:   flags.append(f"OVERFLOW {r['scrollW']}>{r['clientW']}")
                if r["contrast"]:   flags.append(f"contrast x{len(r['contrast'])}")
                if r["small_taps"]: flags.append(f"small-tap x{len(r['small_taps'])}")
                if r["headings"]:   flags.append(f"heading-skip x{len(r['headings'])}")
                if r["tiny"]:       flags.append(f"tiny-type x{len(r['tiny'])}")
                print(f"  {n:<15} imgs={r['imgs']}  " + ("OK" if not flags else " | ".join(flags)))
                for c in r["contrast"]:
                    print(f"       {c['ratio']:>5}:1 (need {c['need']}) {c['size']}px {c['sel']:<30} “{c['text']}”")
                for t in r["small_taps"]: print(f"       tap: {t}")
                for h in r["headings"]:   print(f"       {h}")
                for t in r["tiny"]:       print(f"       tiny: {t}")
            await pg.close()
        await b.close()

asyncio.run(main())
