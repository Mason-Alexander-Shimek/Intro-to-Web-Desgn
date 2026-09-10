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
| Browser default styling | Type, colour, spacing and a centred column |

## File structure

```
Assignment2
├── index.html          Home — how the world fell apart
├── city.html           Moscow and its eight subsectors
├── orihia.html         The corporation that owns the city
├── factions.html       Everyone else
├── images
│   ├── world-map.png
│   ├── orihia-logo.png
│   └── bullet-*.png    16x16 custom list bullets, one per page
├── styles
│   ├── styles.css      Shared base for all four pages
│   ├── page-home.css   Green
│   ├── page-city.css   Blue
│   ├── page-orihia.css Red, and heavier than the rest
│   └── page-factions.css  Violet
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
- **`color`** — the page accent in each `page-*.css`, plus muted grey for
  captions and footer text.
- **`font-family`** — Georgia for body text with `"Times New Roman", Times,
  serif` behind it as fallbacks, Verdana for headings and interface text, and
  Impact on the Orihia page.
- **`margin`** — `margin: 0 auto` on `body` for centring, plus spacing between
  headings, paragraphs and list items.
- **`max-width`** — `700px` on `body`, which keeps a line of text under about 80
  characters. Also `max-width: 100%` on `img` so images shrink to fit a phone
  instead of running off the screen.

## Design decisions

**One colour per page.** Green for the history, blue for the city, red for
Orihia, violet for the factions. Each page opens with a solid band of its colour
carrying the title, the matching link in the navigation is underlined in it, and
the list bullets are drawn in it. If you land mid-scroll you can tell which part
of the setting you are in without reading a word.

**Orihia's page is deliberately heavier.** Impact instead of Verdana, headings
as solid black bars, six-pixel black borders, names set in the corporate red. It
is a weapons manufacturer that owns the city, so its page should feel louder than
the others.

**Georgia for the lore, Verdana for everything else.** The lore runs long, and a
serif is easier to read at that length. Verdana handles the navigation, headings
and the bold names that open each list entry, because those are things you scan
rather than read.

**The district list stayed an `<ol>`.** Numbered lists usually only make sense
for a sequence, and the eight subsectors are not one. I kept the numbers anyway
because they are useful at the table — you can roll a d8 to pick a district.

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
