# A Setting for a Cyberpunk TTRPG Campaign — Assignment 3

## Building components with `<div>` and classes

Assignment 2 styled four pages using only tag selectors, which meant each page
needed its own stylesheet just to change colour. Assignment 3 introduces `<div>`
containers and the `class` attribute, so this time there is one stylesheet, a
reusable hero, and a card component written once and used three times.

**Live page:** `https://mason-alexander-shimek.github.io/Intro-to-Web-Desgn/Assignment3/`

## What changed from Assignment 2

| Assignment 2 | Assignment 3 |
| --- | --- |
| Five stylesheets, one per page plus a base | One `styles.css`, with a class on each `<body>` |
| `<header>` alone at the top of each page | A `.hero` component wrapping it |
| No grouped content | A `.file-card` component, used three times |
| Tag selectors only | Class selectors and nested selectors |
| Styling was the only thing tying the pages together | The homepage now routes to the other three |

## File structure

```
Assignment3
├── index.html          Home — the hero, the card group, and the history
├── city.html           Moscow and its eight subsectors
├── orihia.html         The corporation that owns the city
├── factions.html       Everyone else
├── images
│   ├── world-map.png            original, kept for reference
│   ├── world-map-terminal.png   phosphor version, used in the hero
│   ├── orihia-logo.png
│   ├── card-*.png               one image per card
│   └── bullet-*.png             16x16 console blocks, one per page theme
├── styles
│   └── styles.css
└── README.md
```

## The components

**`.hero`** opens every page. On the three inner pages it holds only the header
block. On the homepage it also carries the world map, a quotation pulled from the
end of the history, and the citation underneath it.

```html
<div class="hero">
  <header>
    <h1>A Setting for a Cyberpunk TTRPG Campaign</h1>
    <h2>A player's guide to Moscow...</h2>
  </header>
  <figure>...</figure>
  <blockquote>This is life, and it's normal...</blockquote>
  <cite>Player's Guide — A Brief History</cite>
</div>
```

**`.file-card`** is written once and used three times, one per page a reader can
go to next. Each card holds a title, the file it opens, an image and a blurb.
Each also carries a second class — `card-city`, `card-orihia`, `card-factions` —
that lends it the colour of the page it leads to, so the group previews the
colour coding before you arrive.

**`.file-card-group`** wraps the three cards. Because the cards are
`display: inline-block`, setting `text-align: center` on the group is enough to
centre them as a row.

## Where the lesson's ideas are used

- **`class` attribute** — on the two components, on each card variant, and on
  every `<body>` tag to pick the page theme.
- **Class selectors** — `.hero`, `.file-card`, `.file-card-group`, `.page-city`.
- **Nested selectors** — `.hero img`, `.hero blockquote`, `.hero cite`,
  `.file-card h3`, `.file-card p`. These are what let the hero subtitle and the
  section headings both be `<h2>` while looking nothing alike, and what lets the
  card images be sized without touching the map or the Orihia emblem.
- **`display: inline-block`** — the navigation links and the cards.
- **`display: block`** — on `<cite>`, which is inline by default, so the
  citations sit on their own line.
- **`width: fit-content`** — on the card paragraphs, with `margin: 0 auto`.
- **`<blockquote>` and `<cite>`** — in the hero, sharing one background colour so
  they read as a single panel rather than two stray pieces of text.

## Design decisions

**The site is a terminal you are reading in-world.** Monospace throughout, hard
edges, and a screen background that is never pure black, because a CRT carries a
faint cast from its phosphor even where nothing is lit.

**One phosphor per page**, switched by the `<body>` class: green for the history,
blue for the city, red for Orihia, violet for the factions.

**Inverted video does the signposting.** The navigation tab for the page you are
on is drawn as solid phosphor with the label cut out of it, which is how a
terminal marks a selected item. The hero header uses the same trick full width.

**Orihia's page runs heavier.** Its section headings are inverted alert bars
rather than underlined text, and every rule on the page is twice as thick.

**The card images are schematics, not photographs.** A ring plan for the city, the
emblem for Orihia, and a node graph for the factions, each drawn in that page's
phosphor. They are placeholders in the sense that any better art can drop
straight into `images/` under the same filenames.

## Accessibility

Every text colour was checked against its background. Body text runs between
9.8:1 and 11.2:1, the phosphor accents between 6.0:1 and 10.8:1, and the dimmed
captions and inactive navigation links all clear 4.6:1. WCAG AA asks for 4.5:1.

## Notes for myself

Things here that go past what the lesson covered:

- **`nav li` and `main ul` rather than plain `li` and `ul`.** The lesson writes
  `li { display: inline-block; }` because its demo page has one list. This site
  has lists of districts, directors and factions that would all collapse into a
  single line.
- **Two classes on one element**, as in `class="file-card card-city"`. The first
  builds the card, the second colours it.
- **Section 8 of the stylesheet depends on rule order.** `.page-home main a` and
  `.card-city h3 a` are equally specific, so the only thing deciding the winner is
  which one the browser reads last. That is why the card variants sit at the very
  bottom of the file.
- **`max-width: 24%` on the cards, not a third.** Padding and borders are added
  on top of a percentage width rather than included in it, so three cards at 31%
  each did not fit. `min-width` is what drops them onto separate rows on a phone.
- **`vertical-align: top`** on the cards, so uneven cards line up along their
  tops instead of their last line of text.
- **`font-style: normal` on `<cite>`**, which browsers italicise by default.
  Italic monospace is hard to read.
- **`a:hover`, `a:focus` and `a[aria-current="page"]`**, for the mouse, the
  keyboard, and marking the current page.
