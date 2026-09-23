# A Setting for a Cyberpunk TTRPG Campaign — Assignment 4

A lore reference for the cyberpunk tabletop campaign I run, built to look like a
public access terminal in the city it describes. Four content pages, a component
library, and a stylesheet that recolours the whole screen from one class on the
`body` tag.

**Live site:** `https://mason-alexander-shimek.github.io/Intro-to-Web-Desgn/Assignment4/`

---

## Assignment 4 - README Questions

### Visual Appeal

**Which icons did you ultimately use and for what purposes?**

Six, each with one fixed meaning so they can be learned. They sit on section
headings across all four pages.

| Icon | Means | Where it appears |
| --- | --- | --- |
| **terminal** | an archive readout | *A Brief History on The Setting*, *Registry Marks* |
| **rings** | the city and its subsectors | *The Subsectors in Full* |
| **die** | a table you can roll on | *Subsector Quick Reference* |
| **alert** | Orihia | *The Directorate Board*, *The Constants*, *Orihia Subsidiaries* |
| **network** | organisations outside Orihia | *Who They Are* |
| **transmit** | sending something to me | *Want More Lore?* |

They are drawn on the same 96px grid with the same stroke weight and the same
geometric vocabulary, so they read as one set. Each is drawn in the phosphor of
the page it belongs to, which is why the alert icon is red and the rings icon is
blue. On the Orihia page the headings are solid red bars, so the icon there gets
`filter: brightness(0)` to knock it back to the same near-black as the heading
text instead of disappearing into the background.

There are also sixteen registry marks, one per organisation on the factions
page. Those are not icons in the same sense, since they identify rather than
label, so they carry real `alt` text while the heading icons carry `alt=""`.

**Which consistent colors, values, lines, and/or shapes did you utilize and why?**

Six colour roles, with each page using the same six in a different hue:

| Role | Home | City | Orihia | Factions |
| --- | --- | --- | --- | --- |
| Screen | `#080C09` | `#070B12` | `#100608` | `#0B0812` |
| Panel | `#0F1712` | `#0E1520` | `#1B0A0D` | `#14101F` |
| Rule | `#3A5F49` | `#33526E` | `#6E2A2C` | `#4E3E73` |
| Muted text | `#6A8173` | `#6B7E8F` | `#8F7374` | `#807795` |
| Body text | `#A9CBB6` | `#A8C4DC` | `#D9B3B3` | `#BCB0D9` |
| Phosphor | `#46D986` | `#48B4F0` | `#FF4B45` | `#A883F5` |

Value does most of the work. The screen is nearly black, body text sits high
above it, and the full phosphor is reserved for things that need attention:
headings, links, the names that open each entry, and the submit button. The
screen is never pure black, because a CRT carries a faint cast from its phosphor
even where nothing is lit.

Line weight carries meaning rather than decoration. 1px divides content inside a
component, 2px separates major regions like the nav and the footer, and 4px is
reserved for the Orihia page, the one page meant to feel heavier than the rest.

Every shape is a hard-edged rectangle. No rounded corners anywhere, because a
terminal does not draw curves. The hero band, the cards, the form panel, the
table cells and the gallery tiles are all the same shape at different sizes.

Colour is never the only signal. The current nav tab is inverted as well as
coloured, links are underlined as well as lit, and every heading has a rule or a
bar under it.

**Which Google Fonts did you use and for what purposes?**

Two, in clearly separate roles:

- **VT323** for the `h1` in every hero, and nowhere else. It is a screen font
  drawn from a DEC VT320 terminal, which is exactly what this site is pretending
  to be. It is a display face, so it appears once per page at large size.
- **IBM Plex Mono** for everything else: body text, navigation, headings, form
  fields, table cells, captions. Monospace holds the terminal feel, and Plex
  stays readable across four thousand words of lore in a way a pixel font would
  not.

Both fall back to `"Courier New"` and the generic `monospace` if Google's
servers do not answer.

### Structure & Organization

**What information does your table organize, and why was a table appropriate?**

The eight subsectors of Moscow, as a roll number, a name and a one-line summary.

A table was right because it is the same three facts repeated eight times, and
because there are two different ways people need to use it. Mid-session you
either scan the name column for the district you want, or you roll a d8 and read
across to find out what you got. Both of those are column operations, and a
table is the only structure that lets the eye move down one column without
reading everything else. The full paragraph descriptions still follow underneath
for when someone actually wants the detail.

**What specific style choices helped you structure and organize your form?**

- `display: block` on the labels, so each one takes its own line and pushes its
  field underneath it. The eye goes label, field, label, field straight down.
- Labels are small and uppercase; field text is normal size and normal case.
  That contrast means you can tell at a glance which lines are questions and
  which are answers.
- `width: 100%` with `box-sizing: border-box` on every text field, select and
  textarea, so they all start and stop on the same two vertical lines rather
  than each being as wide as its own padding makes it.
- A panel background one step lighter than the screen, so the whole form reads
  as a single object rather than loose fields on a page.
- The fieldset's default border removed, because the panel already draws that
  boundary and two nested boxes looked like a mistake.
- The submit button is the only solid block of full phosphor anywhere in `main`.
  Nothing else competes with it, so the end of the form is obvious.
- Placeholders carry real examples rather than repeating the label.

### Design Goals

**What is the goal of your form, and how did it support your site's goals?**

The goal is to get a question asked in one sitting, before the reader decides it
is easier to just message me and then forgets.

The site exists so players can look things up themselves instead of asking me
during play. That works right up until the page does not cover what they need,
and at that point the site was previously a dead end: the homepage said "feel
free to ask" and gave no way to do it. The form catches the question at exactly
the moment it comes up, and asks which part of the setting it concerns and how
far along the player is in character creation, so the answer can be pitched at
the right level rather than dumping everything.

**How does the gallery support your website's goals?**

Players hear organisation names in play long before they meet anyone from them,
and they see the marks stencilled on things. The gallery is a visual index: all
sixteen registry marks in one block with their names, so you can match a mark
you saw to a name, then read the full entry below. Without it, the factions page
was sixteen paragraphs with no way in.

**What pattern did you use: uniform, alternating, or something else, and why?**

Uniform. Every tile is the same size and holds the same two things in the same
order, mark then name. The whole point is comparing marks against each other, so
anything that varied between tiles would read as a difference in status or type
between the organisations, which is not true. They are all equally unfamiliar
until you meet one.

The uniform grid also sets up the break. The Orihia page is the only place the
site's pattern changes, and that lands harder because everything else is so
regular.

### Checking In

- **Learning about and applying design principles:** Good. Alignment and pattern
  were the easy ones, since the whole site is one centred column of repeating
  blocks. Continuity took the longest to see, and the fix was making each card
  carry the colour of the page it leads to so the thread continues across pages.
- **Using typography in your designs:** Good, once I stopped trying to make one
  font do everything. Giving VT323 exactly one job and letting IBM Plex Mono
  carry the rest solved it.
- **Creating components:** This is the part that clicked. Building the form once
  in `components.html` and then dropping it into the page was much faster than
  how I was working before.
- **Exploring `display: flex;`** Still new. The gallery works, but I mostly
  understand `flex-wrap` and `gap` and I would want more practice before using
  flex for a whole page layout rather than one component.

---

## New CSS properties used this module

`position: sticky`, `z-index`, `display: flex`, `flex-wrap`, `justify-content`,
`gap`, `text-shadow`, `box-shadow`, `background-image` with `linear-gradient()`,
`border-collapse`, `box-sizing`, `accent-color`, `cursor`, `resize`, `filter`.

## File structure

```
Assignment4
├── index.html          Hero, card group, history, lore request form
├── city.html           Subsector quick-reference table, then the full list
├── orihia.html         The corporation
├── factions.html       Registry mark gallery, then the full list
├── components.html     The component library. Not linked from the nav.
├── images
│   ├── icon-*.png              6 icons
│   ├── icons-contact-sheet.png all six together, for the Discussion post
│   ├── mark-*.png              16 registry marks, one per organisation
│   ├── card-*.png              card schematics
│   ├── bullet-*.png            list bullets
│   └── world-map*.png, orihia-logo.png
├── styles
│   └── styles.css
├── DESIGN-NOTES.md     design process document notes
└── README.md
```

`components.html` holds every reusable piece with no page theme applied, so
these are the base versions each page's `body` class then recolours. There is a
commented test area directly under the opening body tag for building new
components before they touch a real page, and each component is separated by the
comment block from the lesson plus an `<hr>`.

## Accessibility

Every form field has a `<label for="...">` pointing at that field's `id`, rather
than a bare label that looks connected but is not. Radio and checkbox labels
wrap their own input so the whole phrase is clickable. Every text colour was
checked against its background: field text runs 9.8:1 to 11.2:1, table text
9.2:1 to 10.3:1, and button labels 6.0:1 to 10.8:1, against the 4.5:1 that WCAG
AA asks for.

## Known limitations

- **The form does not send anything.** GitHub Pages serves static files, so
  there is no server to receive a submission, and it has no `action` attribute
  on purpose. A service like Formspree would make it live.
- **`main img` sets `display: block`**, which is right for the world map and
  wrong for an icon in a heading. `main h2 img` has to set `display: inline` and
  its own margins to escape it.
- **The card row does not bottom-align.** Three cards of uneven height sit on
  their tops. Flexbox would fix it and I have not rebuilt that component yet.
