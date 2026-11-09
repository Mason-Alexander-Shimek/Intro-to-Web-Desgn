# Assignment 8 — Within Reach (working name)

The client site for Community Resource Access, Missoula. Assignment 7 scoped and built it;
Assignment 8 adds the visual layer — a brand mark, category icons, and a hero illustration —
and adds Transportation as a fifth category because the client brief names it.

**Every listing on this site is a sample.** Names, phone numbers and addresses are placeholders,
and the phone numbers use the reserved 555 range. The one real number is 988, on the health page.

## Pages

| File | Holds |
|---|---|
| `index.html` | Five doors, the crisis line, and how the site works |
| `housing.html` | Rent and deposit help, eviction advice, beds for tonight |
| `food.html` | Grocery pantry, SNAP, free meals for children |
| `utilities.html` | Heating bills, shut-off emergencies, cheaper phone and internet |
| `health.html` | Clinic without insurance, prescription help, dental |
| `transport.html` | Bus passes, rides to appointments, car repairs |
| `wireframes.html` | One wireframe per page, plus the component inventory |

## What's new in Assignment 8

**Icons.** Sixteen marks, all inlined as SVG rather than loaded as files: no extra HTTP request,
no layout shift, and `stroke="currentColor"` means each one takes the colour of the text beside
it. Fifteen are [Feather](https://feathericons.com) (MIT, Cole Bemis); the door mark is original.
The whole set is 2.8 KB — lighter than one small JPEG.

**The hero is drawn, not photographed.** Two reasons. The brief asks for dignified imagery of real
Missoula places and warns against stock photography that presents hardship as pity — an
illustrated Mount Sentinel and the Clark Fork sidesteps that problem entirely. And a 1.4 KB SVG
keeps the "loads on a weak signal" promise that a 200 KB photograph would break.

**Warmer neutrals.** The brief asks for calm, warm neutrals with high contrast. The panel tint
moved from a blue-grey `#f1f4f7` to a warm `#f4f1ec`, with the rules and secondary text warmed to
match. The deep blue accent stayed: it holds AA comfortably and pairs with the warm red by
lightness as well as hue, so the two never rely on colour alone.

**A fifth door.** Transportation, with three sample listings, because the brief lists it among the
needs and the Assignment 7 build had no door for it.

## Testing

`python3 build/audit.py` measures the rendered pages. At 1200px and 390px, all six pages:
**every page exists and links to every other, every anchor resolves, no horizontal overflow, no
heading-level skips, every tap target at least 44px, and every text/background pair meets WCAG AA.**

Heaviest page **22.9 KB**, counting HTML, CSS and the hero SVG together. No photographs, no
webfonts, no scripts.

## Open questions for the client

These are the decisions I cannot make for them, in the order they block work.

1. **The name.** Three options were offered — Within Reach, Steady Ground, Waypoint. The site is
   mocked up as *Within Reach* with an open-door mark, because that tagline ("Local help, made
   clear") matches what the site actually does. The logo metaphor changes with the name: stepping
   stones for Steady Ground, a signpost for Waypoint.
2. **"Other living expenses."** The brief names housing, utilities, food, transportation and
   healthcare, then adds "and other living expenses." Is that a sixth door, or a catch-all that
   lives inside the five?
3. **Search.** The brief asks for searchable resources. The signed proposal explicitly excludes
   "search across a live database." This is a scope and cost conversation, not a quick answer.
4. **"Last updated" dates.** The brief wants them on every listing for trust. That needs a person
   and a routine, not just a field — who updates, and how often?
5. **Volunteer and donate sign-up.** New scope. The site currently has no forms, no accounts and
   no tracking, which is a deliberate promise; a sign-up form is the first thing that would
   collect anything about a visitor.
6. **Photography.** The brief asks for real Missoula places and community members with consent.
   I cannot source those — the client would need to supply them, with releases.
7. **The real listings.** Still the blocker on everything. Nothing on the site has been checked
   against any agency.

## Known limitations

- The listings are samples. Nothing has been verified against any agency.
- No search, no accounts, no translations, no eligibility screening. All four are out of scope in
  the signed proposal; items 3 and 5 above would change that.
- The site is static, so nothing updates itself. Staleness is the biggest long-run risk here — a
  wrong phone number is worse than no site at all.
- Contrast is measured against solid backgrounds. The hero illustration carries no text over it,
  deliberately, so there is no case where type sits on something the audit cannot read.
- Content changes belong in `build/content.json`; a rebuild overwrites hand-edited HTML.
