# Design notes, Assignment 6

## Alignment

Everything on every page sits in one 680px column, centred with `max-width: 680px; margin: 0 auto;` on the `body`. That gives every component the same left and right edge: the nav rule, the hero band, the card group, the form, the table, the gallery and the footer rule all start and stop at the same two vertical lines down the whole page.

Inside that column the components stack as horizontal blocks, which is the pattern the lesson describes. On the homepage: nav, hero, paragraph, card row, history, form, footer. The card group is a Grid now, it wasnt quite a grid before. Its three bottom edges were 41px apart under `inline-block` and are 0px apart under Grid. Every horizontal block on the homepage now has nav rule, hero band, card row, form panel, footer rule, and starts and stops on the same two vertical lines, and the rows inside those blocks line up too.

## Line & Shape

Lines already in the design:

- 2px rule under the nav and above the footer (4px on the Orihia page)
- 1px rule under each section heading
- 1px borders around the cards, the form, the table cells and every gallery tile

Shapes: the hero band, the card rectangles, the form panel, the table grid and the gallery tiles are all hard-edged rectangles. Nothing on the site has a rounded corner, which is deliberate — a CRT terminal does not draw curves. 1px is a divider inside a component, 2px separates major regions, and 4px is reserved for Orihia, which is supposed to feel heavier than the others.

## Color & Value

We've got six swatches, named by role, with the four featured hues deliberately spaced apart in value. Each page fills the same six roles from this one palette. The in-between values are blends of Void,
the page's swatch, and Bone, so nothing on the site is a colour that isn't in the table above or on a line between two entries in it. The screen is nearly black, body text sits high above it, and the full-strength hue is reserved for things that need attention: headings, links, the names that open each entry, and the submit button. The thing I got wrong before this week was that the four featured hues were within 19 L* of each other, so in greyscale the four pages were indistinguishable. They are 29 L* apart now. Red could not go darker without failing contrast on a dark background, so the extra range came from lifting green instead.

## Continuity

The eye runs straight down the centre of the column. The repeated left edge pulls it downward, and each full-width rule acts as a stop before the next block. The card group continues off the page, and each card carries the colour of the page it leads to, so the blue card and the blue city page are visibly the same thread. The registry marks do the same on the factions page, where a mark seen in the gallery reappears in the entry below.


## Form Component Plan

A lore request form. The homepage already ended with an invitation to ask for more lore, which put the work on the reader to figure out how. Its purpose is to collect who is asking and how to reach them, let them say which part of the setting they mean, take a free-text question, and record how far along they are in character creation so the answer can be pitched correctly. Since its a request form, it has to collect a contact, a category, free text and a status, with the goal of getting the question asked in one sitting, without the reader deciding it is easier to just send a message instead. Supporting that, text and email inputs, a select, a text area, three radio buttons, one checkbox, a submit button, all grouped in a fieldset help. The form sits in a panel one step lighter than the screen so it reads as one object. Labels are uppercase and small, fields are dark with a phosphor border, so the eye moves label, field, label, field down the column. The submit button is the only solid phosphor block in the whole of `main`, which makes it the most prominent thing on the page once you are looking at the form.


## Pattern

The registry on the factions page is now a uniform grid: sixteen cards, each one a mark, a name and a paragraph, in that order, every column the same width and every row the same height. It replaced two components that were each doing half the job, so now the page is only saying what it needs to once. The pattern still breaks in exactly one place, on the Orihia page, where headings become inverted bars and every rule doubles in weight. That break reads harder now that the rest of the site is more regular than it was.
