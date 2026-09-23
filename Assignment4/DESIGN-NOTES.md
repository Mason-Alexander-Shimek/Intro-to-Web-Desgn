# Design notes — Assignment 4

Raw material for the design process document. These are factual descriptions of
what is actually in the site, so the "where" questions are answered. The
reflective parts, what I would change and why, are mine to write.

## Alignment

Everything on every page sits in one 680px column, centred with
`max-width: 680px; margin: 0 auto;` on the `body`. That gives every component
the same left and right edge: the nav rule, the hero band, the card group, the
form, the table, the gallery and the footer rule all start and stop at the same
two vertical lines down the whole page.

Inside that column the components stack as horizontal blocks, which is the
pattern the lesson describes. On the homepage: nav, hero, paragraph, card row,
history, form, footer.

*Still to decide:* the card row is centred as a group, so with three cards of
uneven height their bottom edges do not line up. Whether that matters.

## Line & Shape

Lines already in the design:

- 2px rule under the nav and above the footer (4px on the Orihia page)
- 1px rule under each section heading
- 1px borders around the cards, the form, the table cells and every gallery tile

Shapes: the hero band, the card rectangles, the form panel, the table grid and
the gallery tiles are all hard-edged rectangles. Nothing on the site has a
rounded corner, which is deliberate — a CRT terminal does not draw curves.

Weight carries meaning rather than decoration: 1px is a divider inside a
component, 2px separates major regions, and 4px is reserved for Orihia, the one
page that is supposed to feel heavier than the others.

## Color & Value

Six values per page, and each page uses the same six roles in a different hue:

| Role | Home | City | Orihia | Factions |
| --- | --- | --- | --- | --- |
| Screen | `#080C09` | `#070B12` | `#100608` | `#0B0812` |
| Panel | `#0F1712` | `#0E1520` | `#1B0A0D` | `#14101F` |
| Rule | `#3A5F49` | `#33526E` | `#6E2A2C` | `#4E3E73` |
| Muted text | `#6A8173` | `#6B7E8F` | `#8F7374` | `#807795` |
| Body text | `#A9CBB6` | `#A8C4DC` | `#D9B3B3` | `#BCB0D9` |
| Phosphor | `#46D986` | `#48B4F0` | `#FF4B45` | `#A883F5` |

Value does most of the work. The screen is nearly black, body text sits high
above it, and the phosphor is reserved for things that need attention: headings,
links, the names that open each entry, and the submit button.

Colour is never the only signal. The current nav tab is also inverted, the
current page also has a different heading treatment, and every link is also
underlined.

## Continuity

The eye runs straight down the centre of the column. The repeated left edge
pulls it downward, and each full-width rule acts as a stop before the next
block.

The card group continues off the page: each card carries the colour of the page
it leads to, so the blue card and the blue city page are visibly the same
thread. The registry marks do the same on the factions page, where a mark seen
in the gallery reappears in the entry below.

## Pattern

The page structure repeats across all four pages: nav, hero band, content,
footer. Once you have seen one page you can predict the next.

Within components the pattern is uniform. Every card is title, file name, image,
blurb, in that order. Every gallery tile is mark then name. Every table row is
number, name, one line.

The pattern breaks exactly once, on the Orihia page, where headings become
inverted bars and the rules double in weight. That break is the point: the
corporation that owns the city should not look like everyone else.

## Form Component Plan

**1. What type of form and for what purpose?**
A lore request form. The homepage already ended with an invitation to ask for
more lore, which put the work on the reader to figure out how. The form gives
that a shape.

**2. What does it need to do at minimum?**
Collect who is asking and how to reach them, let them say which part of the
setting they mean, take a free-text question, and record how far along they are
in character creation so the answer can be pitched correctly.

**3. Form type plus needs equals goal.**
A request form that has to collect a contact, a category, free text and a status
= a goal of getting the question asked in one sitting, without the reader
deciding it is easier to just send a message instead.

**4. What elements and design decisions support that goal?**
Elements: text and email inputs, a select, a textarea, three radio buttons, one
checkbox, a submit button, all grouped in a fieldset under a legend.

Design decisions: the form sits in a panel one step lighter than the screen so
it reads as one object. Labels are uppercase and small, fields are dark with a
phosphor border, so the eye moves label, field, label, field down the column.
The submit button is the only solid phosphor block in the whole of `main`, which
makes it the most prominent thing on the page once you are looking at the form.
Placeholders carry real examples rather than repeating the label.

*Still to answer:* whether the radio question is worth the extra step, or
whether it is one field too many for a form that only needs a question.
