# Assignment 7 — Missoula Resource Finder

The client site for Community Resource Access, built to the scope the winning proposal set:
one start page that routes by need, plus four category pages.

**Every listing on this site is a sample.** Names, phone numbers and addresses are placeholders.
A page that looks like real assistance information but is not is worse than no page at all —
someone acts on it during a bad week. The client supplies the real content at kickoff, which is
what the proposal says happens; what this delivers is the template that content drops into.

## Pages

| File | Holds |
|---|---|
| `index.html` | Four doors, the crisis line, and how the site works |
| `housing.html` | Rent and deposit help, eviction advice, beds for tonight |
| `food.html` | Grocery pantry, SNAP, free meals for children |
| `utilities.html` | Heating bills, shut-off emergencies, cheaper phone and internet |
| `health.html` | Clinic without insurance, prescription help, dental |
| `wireframes.html` | The wireframes drafted before the build |

## The promise the design is built on

Every listing answers the same four questions in the same order:

> **Do I qualify? · What do I bring? · How do I apply? · Where and when?**

Learn the pattern on the first listing and the twelfth takes ten seconds. The generator exists
for exactly this reason — hand-writing twelve listings is how that consistency quietly breaks.
Content lives in `content.json`; `build.py` renders every listing through one template.

## The four rules, and whether they are kept

| Rule | How it is kept | Measured |
|---|---|---|
| Phone first | Every page opens with the number for the thing that cannot wait; every phone number is a 44px tap target, not a string of text | no tap target under 44px |
| No account, no tracking | No forms, no cookies, no scripts of any kind | 0 scripts |
| Short plain sentences | Limits are given in numbers, not "low income". Steps are numbered in the order you do them | — |
| Loads on a weak signal | No images, no webfonts, one system typeface | **18.4 KB heaviest page**, HTML + CSS together |

## Components

**Flexbox**: `.site-nav`, `.urgent-call`, `.jump-list`, `.where-row`, `.rules-strip`, `.ticks`,
`.need-card`, `.site-foot`

**Grid**: `.need-grid` (the four doors), `.answers` (the four questions, 2×2 then stacked)

**Flow**: `.listing`, `.checklist`, `.demo-banner`, `.page-head`

`.need-grid` uses `repeat(4, 1fr)` rather than `auto-fit`. Counted first: at `minmax(230px, 1fr)`
only three fit the 860px column and the fourth orphans onto its own row. Four cards, four tracks.

## The printable checklist

`@media print` hides the nav, the banner, the urgent card, the jump list and all twelve listings,
and prints the "what to bring" checklist alone — one page, real tick boxes. Verified by printing
it, not by assuming the rule applied.

## Testing

`build/audit.py` measures the rendered pages: transferred weight, horizontal overflow, contrast
against the real painted ancestor, tap target height, heading order.

At 1200px and 390px, all five pages: **no overflow, no heading skips, every tap target at least
44px, and every text/background pair meets WCAG AA** (4.5:1 body, 3.0:1 large).

## Known limitations

- The listings are samples. Real content has not been checked against any agency.
- There is no search, no accounts, no translations and no eligibility screening. All four are
  named as out of scope in the proposal and remain out of scope.
- The site is static, so nothing updates itself. Keeping listings current is staff work, which is
  why the listing template and the style guide matter more than the pages do.
- Contrast is measured against solid backgrounds. There are no images, so there is no case here
  where text sits on something the audit cannot read — but that is a property of this design,
  not a general guarantee.
