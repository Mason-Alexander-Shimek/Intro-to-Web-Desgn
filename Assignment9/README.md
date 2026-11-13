# Assignment 9 — Within Reach

The client site for Community Resource Access, Missoula. Assignment 7 scoped and built it,
Assignment 8 added icons and a drawn hero, and Assignment 9 is the refinement pass: real
photographs of Missoula, responsive image delivery, an About page, and a component library
pulled out into its own folder.

**Every listing on this site is a sample.** Names, phone numbers and addresses are placeholders,
and the phone numbers use the reserved 555 range. The one real number is 988, on the health
page and the About page.

---

## Goals and requirements

What the site has to accomplish, and where each item stands. Taken from the client brief and
the signed proposal.

| # | Requirement | State | Note |
|---|---|---|---|
| 1 | Five needs, each with its own page | **done** | Housing, food, utilities, health care, transportation |
| 2 | Same four questions on every listing, same order | **done** | Do I qualify / What do I bring / How do I apply / Where and when |
| 3 | Works on a phone on a weak signal | **done** | Category pages 30 KB; see the weight budget below |
| 4 | Crisis route that needs no reading | **done** | Urgent card above the listings on every page; 988 on the start page |
| 5 | No accounts, no tracking, no forms | **done** | Nothing on the site collects anything |
| 6 | Printable "what to bring" | **done** | `@media print` drops everything else |
| 7 | Dignified imagery of real Missoula places | **done** | Five photographs; see credits, which are **not yet cleared** |
| 8 | Warm neutrals, high contrast | **done** | Every text/background pair measured at AA, photographs included |
| 9 | About page: who runs this, who it serves | **done** | `about.html`, added this module |
| 10 | Contact details | **placeholder** | Marked as placeholder on the page; waiting on the client |
| 11 | Searchable resources | **out of scope** | Excluded by the signed proposal; open question 3 |
| 12 | "Last updated" date on every listing | **not started** | Needs a person and a routine, not a field. Open question 4 |
| 13 | Volunteer and donate sign-up | **not started** | New scope, and the first thing that would collect data. Open question 5 |
| 14 | Real, verified listings | **blocked** | Nothing has been checked against any agency. Open question 7 |

---

## What's new in Assignment 9

**Photographs, delivered responsibly.** Five pictures of Missoula replace the drawn hero.
Each one ships as AVIF, WebP and JPEG at three or four widths, and the browser takes the first
format it understands. AVIF comes in at roughly 40% of the JPEG, which is what makes the
photographs affordable at all.

**The hero stops overlaying on phones.** Above 700px the heading sits on the photograph behind
a dark scrim. Below it, the picture becomes a band and the words move onto paper underneath.
This was not a style preference: at 390px the heading, lede and eyebrow wrap to about nine
lines, which is nearly the full height of the hero, so no scrim could both protect type that
tall and leave the photograph visible. Measured first, then changed. Before the fix the eyebrow
ran **1.24:1** against a required 4.5.

**Photographs stay off the category pages.** Housing, food, utilities, health care and
transportation carry no pictures at all and still weigh about 30 KB. Those are the pages
someone opens in trouble, and a decorative photograph above the phone number costs bytes and
pushes the number down the screen. The pictures live where someone is reading rather than
acting: the start page and the About page.

**An About page.** Who runs the site, who it is for, how it is built, and how it is meant to
stay current, plus clearly-marked placeholder contact details.

**A component library in its own folder.** `../ComponentLibrary/` holds every reusable piece,
grouped by the Module 9 categories. Building it immediately found a bug: the hero bound its
text colour to `h1` rather than to a class, so the component worked on exactly one page. Colour
now lives on `.hero-overlay` and any heading level inherits it.

---

## Weight budget

Hard numbers, not good intentions. Measured over HTTP with the browser choosing from `srcset`,
by `build/photo_audit.py`.

| Page | Phone, first screen | Phone, whole page | Desktop, first screen |
|---|---|---|---|
| `index.html` | 38.7 KB | 46.5 KB | 57.1 KB |
| `about.html` | 43.4 KB | 66.2 KB | 54.0 KB |
| the five category pages | 29–30 KB | 29–30 KB | 29–30 KB |

**Budget: 80 KB before the first scroll, 190 KB for the whole page.** The audit fails the build
if either is exceeded. Worst case, for a browser that understands neither AVIF nor WebP, is
217 KB on the About page, because it falls back to JPEG.

---

## Testing

Three scripts. All of them measure the rendered page rather than reading the source.

```
python3 build/build.py          # regenerate the seven pages from content.json
python3 build/images.py         # re-encode the photographs (needs the source PNGs)
python3 build/audit.py          # structure, contrast, tap targets, headings, overflow
python3 build/photo_audit.py    # real transferred weight, contrast over photographs, layout shift
```

`photo_audit.py` exists because `audit.py` could not see the one thing this module added. Its
contrast check walks up the DOM looking for a painted background colour and gives up when it
meets a background image, so text on a photograph was being silently skipped. The new script
hides the type, photographs the hero, and samples the actual pixels behind each line.

Current state, all seven pages, at 1200px and 390px: **every page exists and links to every
other, every anchor resolves, no horizontal overflow, no heading-level skips, every tap target
at least 44px, every text/background pair meets AA including the three lines painted on the
hero, and every image reserves its space before it loads.**

---

## How I work, and the tests that account for it

From the Project 1 post-mortem, the three things I actually do, and the specific checks that
catch each one. Broken into named tests rather than left as good advice.

### Tendency 1 — I choose a layout before measuring the content

This is the mistake the post-mortem was about, and I repeated it once since. Flexbox and Grid
are picked by content length, and content length is a thing you can count.

- [x] Count words in the longest and shortest item of every repeating set **before** choosing
- [x] Start page: five cards on a six-column track, counted, so the last card is never orphaned
- [x] Phone: five cards become two columns with the fifth spanning, so there is no hole
- [x] About page: three previews share one 3:2 image ratio so the row cannot go ragged
- [x] Re-check every grid at 390, 700, 760 and 1200

### Tendency 2 — I report a thing as done without checking it ran

Patch scripts that print "patched" whether or not anything matched. Every edit script in this
project now asserts its match count and raises if it is wrong.

- [x] `build/images.py` exits if a source file is missing instead of writing nothing
- [x] Every in-place edit asserts the number of matches before writing
- [x] `photo_audit.py` returns a list of failures and prints a count, not a cheerful summary
- [x] Claims in this README are pasted from a run, not remembered

### Tendency 3 — I trust a measurement that looks plausible

The contrast check returned exactly 1.00 for everything once, because it was sampling the
glyphs rather than the background. A number that looks wrong usually is.

- [x] Contrast sampled from a screenshot with the text hidden, not from computed styles
- [x] Report the worst pixel, the 2nd-percentile pixel, **and** the share of the area that fails
- [x] Verify any surprising result before writing it down

### Per-page checks

Run at 390px and 1200px. Automated unless marked.

| Page | Nav | Contrast | Hierarchy | Responsive | Weight | Images |
|---|---|---|---|---|---|---|
| `index.html` | ✓ | ✓ incl. hero overlay | ✓ one h1 | ✓ overlay drops at 700 | ✓ 38.7 KB | ✓ srcset, reserved, alt |
| `housing.html` | ✓ | ✓ | ✓ | ✓ | ✓ 30.2 KB | none by design |
| `food.html` | ✓ | ✓ | ✓ | ✓ | ✓ 29.1 KB | none by design |
| `utilities.html` | ✓ | ✓ | ✓ | ✓ | ✓ 29.9 KB | none by design |
| `health.html` | ✓ | ✓ | ✓ | ✓ | ✓ 29.8 KB | none by design |
| `transport.html` | ✓ | ✓ | ✓ | ✓ | ✓ 30.0 KB | none by design |
| `about.html` | ✓ | ✓ | ✓ | ✓ preview row stacks | ✓ 43.4 KB | ✓ srcset, reserved, alt |

Still manual, and worth keeping manual:

- [ ] Read every page aloud once. Sentences that are hard to say are hard to read under stress.
- [ ] Print `housing.html` and check the checklist is the only thing on the paper.
- [ ] Tab through the start page with no mouse and confirm the skip link appears first.
- [ ] Open the published URL on an actual phone, not an emulated one.

---

## Image credits — not yet cleared

The five photographs were supplied for this assignment. **I have not verified their licence or
authorship, and that has to happen before this site is published anywhere public.** Listing them
honestly rather than inventing attributions:

| File | Subject | Licence |
|---|---|---|
| `hero-wide-*`, `hero-narrow-*` | Clark Fork riverfront and downtown Missoula | **unconfirmed** |
| `valley-band-*` | Aerial view of the Missoula valley | **unconfirmed** |
| `mainhall-*` | Main Hall, University of Montana | **unconfirmed** |
| `depot-*` | The Missoula depot and the bear statue | **unconfirmed** |
| `locomotive-*` | Logging locomotive, Fort Missoula | **unconfirmed** |

The icons are a different matter and are cleared: fifteen are
[Feather](https://feathericons.com) (MIT, Cole Bemis) and the door mark is original.

**Brand assets**, in both formats the module asks for:

| File | Use |
|---|---|
| `images/logo-door.svg` | Source. Uses `currentColor`, so it takes the colour of whatever it sits beside |
| `images/logo-door-256.png`, `-512.png` | Raster, brand blue on transparency, for anywhere SVG will not go |

The mark is an open door, which is the metaphor that goes with the name *Within Reach*. If the
client picks **Steady Ground** it should become stepping stones, and if they pick **Waypoint**,
a signpost. That is open question 1 and it has to close before the logo is finished.

The client brief also asks for photographs of real Missoula community members with consent.
None of these show identifiable people at close range, and the client would need to supply any
that do, with releases.

---

## Open questions for the client

In the order they block work.

1. **The name.** Within Reach, Steady Ground or Waypoint. Mocked up as *Within Reach* with an
   open-door mark. The logo metaphor changes with the name.
2. **"Other living expenses."** The brief names five needs and then adds "and other living
   expenses." Sixth door, or a catch-all inside the five? A peer working the same brief made it
   a sixth door, which is a defensible answer: a catch-all inside the five is one nobody finds.
3. **Search.** The brief asks for searchable resources; the signed proposal excludes search
   across a live database. A scope and cost conversation, not a quick answer.
4. **"Last updated" dates.** Who confirms a listing, and how often? A date that is six months
   old does more damage than no date, because it proves nobody is watching.
5. **Volunteer and donate sign-up.** New scope, and the first thing that would collect anything
   about a visitor.
6. **Photography.** Licences for the five pictures above, and any photographs of community
   members with releases.
7. **The real listings.** Still the blocker on everything.

---

## Known limitations

- The listings are samples. Nothing has been verified against any agency.
- The photograph licences are unconfirmed. See above.
- No search, no accounts, no translations, no eligibility screening.
- The site is static, so nothing updates itself. Staleness is the biggest long-run risk: a
  wrong phone number is worse than no site at all.
- Content changes belong in `build/content.json`. A rebuild overwrites hand-edited HTML.
- `wireframes.html` is a planning document and is deliberately not linked from the navigation.
