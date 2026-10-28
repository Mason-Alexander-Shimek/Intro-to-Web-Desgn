import asyncio, pathlib, json
from playwright.async_api import async_playwright

A = pathlib.Path("/home/claude/work/GitHub/Intro-to-Web-Desgn/Assignment7")
PAGES = ["index.html", "world.html", "dominion.html", "vallam.html", "factions.html", "houses.html"]

JS = r"""() => {
  const out = {overflow: [], contrast: [], headings: [], alt: [], tiny: []};

  // ---- horizontal overflow
  const de = document.documentElement;
  out.scrollW = de.scrollWidth; out.clientW = de.clientWidth;
  if (de.scrollWidth > de.clientWidth + 1) {
    document.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right > de.clientWidth + 1 && r.width > 0)
        out.overflow.push(el.tagName + '.' + (el.className||'').toString().slice(0,32)
                          + ' right=' + Math.round(r.right));
    });
    out.overflow = out.overflow.slice(0, 6);
  }

  // ---- contrast, measured against the real painted ancestor
  const lum = c => { const [r,g,b] = c.map(v => { v/=255;
      return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*r + 0.7152*g + 0.0722*b; };
  const parse = s => { const m = s.match(/\d+(\.\d+)?/g); return m ? m.slice(0,3).map(Number) : null; };
  const bgOf = el => {
    for (let p = el; p; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return {grad: true};
      const c = cs.backgroundColor;
      if (c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) {
        const v = parse(c);
        const a = c.startsWith('rgba') ? parseFloat(c.split(',')[3]) : 1;
        if (v && a > 0.85) return {c: v};
      }
    }
    return {c: [0,0,0]};
  };
  const ratio = (f, b) => { const L1 = lum(f), L2 = lum(b);
    return (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05); };

  document.querySelectorAll('p,h1,h2,h3,h4,li,a,span,dt,dd,cite,figcaption').forEach(el => {
    if (!el.textContent.trim()) return;
    if (el.children.length && !Array.from(el.childNodes).some(n => n.nodeType===3 && n.textContent.trim())) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const fg = parse(cs.color); if (!fg) return;
    const bg = bgOf(el);
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3.0 : 4.5;
    if (size < 12) out.tiny.push(el.tagName + '.' + (el.className||'').toString().slice(0,28) + ' ' + size + 'px');
    if (bg.grad) return;                       // gradient ground: not measurable this way
    const cr = ratio(fg, bg.c);
    if (cr < need)
      out.contrast.push({sel: el.tagName + '.' + (el.className||'').toString().slice(0,30),
                         ratio: +cr.toFixed(2), need, size,
                         text: el.textContent.trim().slice(0,34)});
  });
  // dedupe by selector, keep worst
  const seen = {};
  out.contrast.forEach(c => { if (!seen[c.sel] || c.ratio < seen[c.sel].ratio) seen[c.sel] = c; });
  out.contrast = Object.values(seen).sort((a,b) => a.ratio - b.ratio).slice(0, 8);
  out.tiny = [...new Set(out.tiny)].slice(0, 5);

  // ---- heading order
  let prev = 0;
  document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
    const n = +h.tagName[1];
    if (prev && n > prev + 1) out.headings.push(`h${prev} -> h${n}: ${h.textContent.trim().slice(0,38)}`);
    prev = n;
  });

  // ---- images without alt
  document.querySelectorAll('img').forEach(i => {
    if (i.getAttribute('alt') === null) out.alt.push(i.getAttribute('src'));
  });
  out.alt = out.alt.slice(0, 5);
  out.imgCount = document.querySelectorAll('img').length;
  return out;
}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1400, 390):
            print(f"\n{'='*18} viewport {w}px {'='*18}")
            pg = await b.new_page(viewport={"width": w, "height": 900})
            await pg.route("**://fonts.g**/**", lambda r: asyncio.ensure_future(r.abort()))
            for name in PAGES:
                await pg.goto((A / name).as_uri(), wait_until="load")
                await pg.wait_for_timeout(450)
                r = await pg.evaluate(JS)
                flags = []
                if r["overflow"]: flags.append(f"OVERFLOW {r['scrollW']}>{r['clientW']}")
                if r["contrast"]: flags.append(f"contrast x{len(r['contrast'])}")
                if r["headings"]: flags.append(f"heading-skip x{len(r['headings'])}")
                if r["alt"]:      flags.append(f"missing-alt x{len(r['alt'])}")
                if r["tiny"]:     flags.append(f"tiny-type x{len(r['tiny'])}")
                print(f"  {name:<15} imgs={r['imgCount']:<3} " + ("OK" if not flags else " | ".join(flags)))
                for c in r["contrast"]:
                    print(f"       {c['ratio']:>5}:1 (need {c['need']}) {c['size']}px  {c['sel']:<34} “{c['text']}”")
                for h in r["headings"][:3]: print(f"       heading: {h}")
                for o in r["overflow"][:3]: print(f"       overflow: {o}")
                for t in r["tiny"]:        print(f"       tiny: {t}")
            await pg.close()
        await b.close()

asyncio.run(main())
