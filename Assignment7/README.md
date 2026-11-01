# Assignment 7 — Missoula Resource Finder

The client site for Community Resource Access, built to the scope the winning proposal set:
one start page that routes by need, plus four category pages.

**Every listing on this site is a sample.** Names, phone numbers and addresses are placeholders,
and the phone numbers use the reserved 555 range. A page that looks like real assistance
information but is not is worse than no page at all — someone acts on it during a bad week. The
client supplies the real content at kickoff, which is what the proposal says happens; what this
delivers is the template that content drops into.

The one real number on the site is 988, on the health page, because someone might need it today.

## Files

| File | Holds |
|---|---|
| `index.html` | Four doors, the crisis line, and how the site works |
| `housing.html` | Rent and deposit help, eviction advice, beds for tonight |
| `food.html` | Grocery pantry, SNAP, free meals for children |
| `utilities.html` | Heating bills, shut-off emergencies, cheaper phone and internet |
| `health.html` | Clinic without insurance, prescription help, dental |
| `wireframes.html` | One wireframe per proposed page, plus the component inventory |
| `styles/styles.css` | The site |
| `styles/wireframes.css` | The wireframe sheet |
| `build/content.json` | All listing content |
| `build/build.py` | Renders the five pages from the content |
| `build/audit.py` | Measures navigation, weight, contrast, tap targets, overflow |

## The promise the design is built on

Every listing answers the same four questions in the same order:

> **Do I qualify? · What do I bring? · How do I apply? · Where and when?**

Learn the pattern on the first listing and the twelfth takes ten seconds. The generator exists for
exactly this reason — hand-writing twelve listings is how that consistency quietly breaks.

## Components

**New, built from scratch for this project**

| Component | System | What it is |
|---|---|---|
| `.answers` | **Grid** | The four questions, 2×2 on a laptop and stacked on a phone, order never changing |
| `.where-block` → `.where-row` | **Flexbox** | Label-and-value rows, with the call-first flag given the urgent colour |
| `.checklist` → `.ticks` | Flow + Flexbox | Tick boxes, plus the print stylesheet that makes the page printable |

**Reused from the component library** — `.site-nav` (Module 2 nav), `.site-foot`, `.page-head`,
`.need-card` (card row), `.jump-nav` (nav variant), `.urgent-card` (feature section variant),
`.rules-strip` (chip row variant).

Seven of ten components already existed, which is why only three are billed as new work and why
the estimate came down from 116 hours to 92. The inventory is on the wireframe sheet.

`.need-grid` uses `repeat(4, 1fr)` rather than `auto-fit`. Counted first: at `minmax(230px, 1fr)`
only three fit the 860px column and the fourth orphans onto a row of its own.

## The four rules, and whether they are kept

| Rule | How | Measured |
|---|---|---|
| Phone first | Every page opens with the number for the thing that cannot wait; every phone number is a tap target, not a string of text | no tap target under 44px |
| No account, no tracking | No forms, no cookies, no scripts of any kind | 0 scripts |
| Short plain sentences | Limits in numbers, not "low income". Steps numbered in the order you do them | — |
| Loads on a weak signal | No images, no webfonts, one system typeface | **17.6 KB heaviest page**, HTML + CSS together |

## The printable checklist

`@media print` hides the nav, banner, urgent card, jump list and all twelve listings, and prints
the "what to bring" checklist alone — one page, real tick boxes. Verified by printing it, not by
assuming the rule applied.

## Testing

`python3 build/audit.py` measures the rendered pages rather than reasoning about them.

At 1200px and 390px, all five pages: **every page exists, links to every other page and resolves
every in-page anchor; no horizontal overflow; no heading-level skips; every tap target at least
44px; and every text/background pair meets WCAG AA** (4.5:1 body, 3.0:1 large).

The navigation check caught a real inconsistency during the build: the nav was emitting
single-quoted attributes while the cards used double. The pages now emit double quotes throughout.

## Known limitations

- The listings are samples. Nothing here has been checked against any agency.
- No search, no accounts, no translations, no eligibility screening. All four are named as out of
  scope in the proposal and remain out of scope.
- The site is static, so nothing updates itself. Keeping listings current is staff work, which is
  why the listing template and the style guide matter more than the pages do.
- Contrast is measured against solid backgrounds. There are no images, so no text sits on anything
  the audit cannot read — that is a property of this design, not a general guarantee.
- Editing the HTML by hand works, but a rebuild from `build/build.py` overwrites it. Content
  changes belong in `build/content.json`.
