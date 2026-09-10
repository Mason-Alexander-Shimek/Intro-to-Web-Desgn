# A Setting for a Cyberpunk TTRPG Campaign — Assignment 2

## Styling the site and building a navigation component

Assignment 1 was one long page of unstyled lore. For Assignment 2 I split it
into four pages, built a navigation component that links them together, and
wrote the CSS that gives the site its look.

**Live page:** `https://mason-alexander-shimek.github.io/Intro-to-Web-Desgn/Assignment2/`

## What changed from Assignment 1

| Assignment 1 | Assignment 2 |
| --- | --- |
| One page, six sections | Four pages, one topic each |
| `<nav>` was a table of contents with `#anchor` links | `<nav>` links to other pages and sits above the header |
| `styles.css` was empty | Five stylesheets, one shared and four for colour |
| Browser default styling | An Orihia public access terminal |

## File structure

```
Assignment2
├── index.html          Home — how the world fell apart
├── city.html           Moscow and its eight subsectors
├── orihia.html         The corporation that owns the city
├── factions.html       Everyone else
├── images
│   ├── world-map.png            original, kept for reference
│   ├── world-map-terminal.png   green phosphor version, used on the page
│   ├── orihia-logo.png
│   └── bullet-*.png             16x16 console blocks, one per page
├── styles
│   ├── styles.css         Shared base for all four pages
│   ├── page-home.css      Green phosphor
│   ├── page-city.css      Blue phosphor
│   ├── page-orihia.css    Red, and heavier than the rest
│   └── page-factions.css  Violet phosphor
└── README.md
```

Every page loads `styles.css` first and its own `page-*.css` second. The second
file only sets the handful of properties that change from page to page, and it
wins where the two overlap because it is linked later.

## Where the lesson's properties are used

- **`list-style-type: none`** — `styles.css`, on `nav ul`, to strip the bullets
  off the navigation.
- **`list-style-image`** — each `page-*.css`, on `main ul`. The path is
  `url('../images/bullet-home.png')` and starts with `../` because CSS paths are
  relative to the CSS file, and the stylesheets sit inside `styles/` while the
  images sit beside that folder rather than inside it.
- **`display: inline-block`** — `styles.css`, on `nav li`, so the four links sit
  in a row instead of stacking.
- **`color`** — three levels per page: the phosphor for headings, links and
  names, a softer tint for body text, and a dimmed one for captions and inactive
  navigation.
- **`font-family`** — one monospace stack everywhere:
  `Consolas, Monaco, "Courier New", Courier, monospace`. Courier New is the
  cross-platform fallback the lesson recommends, sitting behind the two better
  console faces most machines already have.
- **`margin`** — `margin: 0 auto` on `body` for centring, plus spacing between
  headings, paragraphs and list items.
- **`max-width`** — `680px` on `body`, which holds a line to about 70 monospaced
  characters. Also `max-width: 100%` on `img` so images shrink to fit a phone
  instead of running off the screen.
- **`background-color`** — the screen itself, and the inverted blocks behind the
  header, the active navigation tab, and Orihia's headings.

## Design decisions

**The site is a terminal you are reading in-world.** Monospace throughout, hard
edges, no rounded corners. The screen background is never pure black, because a
CRT carries a faint cast from its phosphor even where nothing is lit.

**One phosphor per page.** Green for the history, blue for the city, red for
Orihia, violet for the factions. Each page tints its whole screen, and its
heading bars, links, names and bullets all burn in that colour.

**Inverted video does the signposting.** The page you are on is the one
navigation tab drawn as solid phosphor with the label cut out of it, which is how
a terminal marks a selected item. The header block uses the same trick at full
width, so you can tell which part of the setting you are in from across the room.

**Orihia's page is deliberately louder.** Its section headings run as inverted
alert bars instead of underlined text, and every rule on the page is twice as
thick. It is a weapons manufacturer that owns the city.

**The world map was recoloured.** A full-colour map inside a monochrome terminal
breaks the fiction, so `world-map-terminal.png` maps the ocean down to unlit
screen and the land up to green phosphor. The original file is still in `images/`
if I want to switch back.

**The district list stayed an `<ol>`.** Numbered lists usually only make sense
for a sequence, and the eight subsectors are not one. I kept the numbers anyway
because they are useful at the table — you can roll a d8 to pick a district.

## Accessibility

Every text colour was checked against its background. Body text runs between
9.8:1 and 11.2:1, the phosphor accents between 6.0:1 and 10.8:1, and the dimmed
captions and inactive navigation links all clear 4.6:1. WCAG AA asks for 4.5:1.

## Notes for myself

A few rules here go past what the lesson covered:

- `nav li` and `main ul` instead of plain `li` and `ul`. The lesson writes
  `li { display: inline-block; }` because its demo page has only one list. This
  site has lists of districts, directors and factions, and that rule would drag
  every one of them into a single line. Naming the parent first limits the rule
  to the list inside `<nav>`.
- `a:hover` and `a:focus`, so links respond to a mouse and stay visible when
  tabbing through with a keyboard.
- `a[aria-current="page"]`, which styles the link pointing at the page you are
  already on.
- `line-height`, `font-size`, `letter-spacing` and `text-transform`, which are
  single properties rather than new layout techniques.

Once classes are covered, the four `page-*.css` files could collapse into one
stylesheet with a class on each `<body>` tag.
