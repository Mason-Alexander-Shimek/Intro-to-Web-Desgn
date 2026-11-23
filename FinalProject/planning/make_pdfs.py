"""Render the three planning documents to Letter PDFs.

Run: python3 planning/make_pdfs.py   (from the FinalProject folder)

Google Fonts is unreachable from this environment, so the sheets are designed
around local serif faces and the PDF renders identically anywhere.
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out"

DOCS = [("sitemap.html",    "Vallam-Sitemap.pdf"),
        ("wireframes.html", "Vallam-Wireframes.pdf"),
        ("proposal.html",   "Vallam-Proposal.pdf")]


async def main():
    OUT.mkdir(exist_ok=True)
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for src, pdf in DOCS:
            f = HERE / src
            if not f.exists():
                problems.append(f"missing source: {src}")
                continue
            ctx = await b.new_context(viewport={"width": 1100, "height": 1400})
            pg = await ctx.new_page()
            await pg.goto(f.as_uri(), wait_until="load")
            await pg.wait_for_timeout(400)

            # Horizontal overflow in print means content is being cut off the page.
            await pg.emulate_media(media="print")
            await pg.wait_for_timeout(200)
            over = await pg.evaluate("""() => {
              const bad = [];
              document.querySelectorAll('.doc *').forEach(el => {
                if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0)
                  bad.push((el.className || el.tagName) + ' +' +
                           (el.scrollWidth - el.clientWidth) + 'px');
              });
              return bad.slice(0, 6);
            }""")
            if over:
                problems.append(f"{src}: content wider than its box -> {over}")

            await pg.pdf(path=str(OUT / pdf), format="Letter",
                         print_background=True,
                         margin={"top": "14mm", "bottom": "14mm",
                                 "left": "13mm", "right": "13mm"})
            await ctx.close()

            size = (OUT / pdf).stat().st_size / 1024
            try:
                import pypdf
                pages = len(pypdf.PdfReader(str(OUT / pdf)).pages)
            except Exception:
                pages = "?"
            print(f"  {pdf:<26} {pages} pages  {size:6.1f} KB")
        await b.close()

    if problems:
        print("\n  PROBLEMS:")
        for x in problems:
            print("   !!", x)
        return 1
    print("\n  three documents rendered, nothing overflowing its box")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
