# A Setting for a Cyberpunk TTRPG Campaign — Assignment 4

## A component library, a Google Font, and three new components

Assignment 3 built a hero and a card. Assignment 4 adds a form, a table and a
flexbox gallery, collects every component into a library page, and swaps the
system monospace stack for a pair of Google Fonts.

**Live page:** `https://mason-alexander-shimek.github.io/Intro-to-Web-Desgn/Assignment4/`

## What changed from Assignment 3

| Assignment 3 | Assignment 4 |
| --- | --- |
| System monospace only | VT323 for display, IBM Plex Mono for reading |
| Two components | Five, plus an icon set |
| No component library | `components.html` collects all of them |
| Nav scrolled away | Nav sticks to the top of the window |
| Classes only | An ID (`#gallery`) where the element is unique |
| No images of my own | Six icons and sixteen registry marks |

## File structure

```
Assignment4
├── index.html          Home — hero, card group, history, lore request form
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
├── DESIGN-NOTES.md     raw material for the design process document
└── README.md
```

## The component library

`components.html` holds every reusable piece with no page theme applied, so
these are the base versions that each page's `body` class then recolours. There
is a commented test area directly under the opening body tag for building new
components before they go anywhere near a real page.

Components are separated with the comment blocks from the lesson and an `<hr>`
between each:

```html
<!-- ------------------------------------------------ -->
<!-- --------------------- FORM --------------------- -->
<!-- ------------------------------------------------ -->
```

## Typography

Two families, both from Google Fonts:

- **VT323** for the `h1` in every hero. It is a screen font drawn from a DEC
  VT320 terminal, which is exactly what this site is pretending to be. It is
  used in one place only, at large sizes, because it is a display face.
- **IBM Plex Mono** for everything else. Monospace keeps the terminal feel, and
  Plex stays readable across four thousand words of lore in a way a pixel font
  never would.

The `<link>` sits in the head of all five pages. Both fall back to
`"Courier New"` and the generic `monospace` if Google's servers do not answer.

## The new components

**Form** (`.lore-form`, on the homepage under Want More Lore). A lore request:
name, email, a dropdown for which part of the setting, a textarea for the
question, radio buttons for how far along the reader is in character creation,
and a checkbox for update notifications.

**Table** (on `city.html`). A quick reference for the eight subsectors with a
roll column, so a d8 picks one at the table. The full descriptions still follow
underneath.

**Gallery** (`#gallery`, on `factions.html`). Sixteen registry marks, one per
organisation, in a flex container that wraps them into rows.

## Where the lesson's ideas are used

- **Google Fonts** — `<link>` in every head, applied with `font-family`.
- **`text-shadow`** — a phosphor bloom on lit headings and the hero quotation.
- **`linear-gradient` and `box-shadow`** — the hero band has a top-to-bottom
  brightness falloff and throws a glow onto the screen around it.
- **Form elements** — `<form>`, `<fieldset>`, `<legend>`, `<label>`, `<input>`,
  `<select>`, `<option>`, `<textarea>`, radio, checkbox, `<button>`.
- **`input[type="..."]` selectors** — so the text and email fields can be styled
  without catching the radios and checkboxes.
- **`:hover`** — navigation links, card titles and the submit button.
- **Table elements** — `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`.
- **Positioning** — `position: sticky` on the nav, so the way out never scrolls
  away on pages this long.
- **Flexbox** — `display: flex`, `flex-wrap`, `justify-content` and `gap` on the
  gallery and the icon set.
- **ID vs class** — `#gallery` and `#icon-set` are IDs because there is exactly
  one of each. The cards and the form are classes because they repeat.

## Accessibility

- Every form field has a `<label for="...">` pointing at the field's `id`. The
  lesson's example uses bare labels, which look the same but are not actually
  connected to anything a screen reader can follow.
- Radio and checkbox labels wrap their own input, so the whole phrase is a click
  target rather than just the little circle.
- Every text colour was checked against its background. Field text runs between
  9.8:1 and 11.2:1, table text between 9.2:1 and 10.3:1, and button labels
  between 6.0:1 and 10.8:1. WCAG AA asks for 4.5:1.
- Decorative icons carry `alt=""` so screen readers skip them. The registry
  marks carry real alt text, because they identify something.

## Notes for myself

- **The form does not send anything.** GitHub Pages serves static files, so
  there is no server to receive a submission. It has no `action` attribute on
  purpose. A service like Formspree or Google Forms would make it live.
- **`main img` sets `display: block`**, which is right for the map and the
  emblem and wrong for a small icon sitting in a heading. `main h2 img` has to
  set `display: inline` and its own margins to get out of it. This cost me three
  wrong attempts, with the icon landing centred on its own line each time.
- **`border-collapse: collapse`** on the table, or every cell draws its own
  border next to the table's and everything looks doubled.
- **`box-sizing: border-box`** on the form fields, so `width: 100%` means the
  whole field rather than the field plus its padding.
- **`accent-color`** recolours the native radio and checkbox to the page
  phosphor. Newer than the rest of this, and it degrades to the browser default.
- **Icons live in wide headings only.** Inside a `<th>` or a `<legend>` or a
  narrow card title there is not enough room, and they wrap.
- **`icon-alert` is not placed on a page yet.** Every heading on `orihia.html`
  is an inverted red bar, and a red icon would vanish into it. It is in the
  library, ready for a dark heading.
