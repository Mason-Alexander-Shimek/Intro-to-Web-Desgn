# Design Document — Module 7 Principles

Answered against the built pages, with numbers taken from `audit.py` rather than from impression.

---

## Space

**Where am I already using space to separate or group content?**
Three scales, used consistently. Between parts: `.cat-head` carries 76px above it and 104px when
it starts a new group, so "Criminal Organisations" is visibly a different thing from the families
above it. Between entries: `.entry-row` has 30px of padding and a hairline rule, so the gap does
the grouping and the rule only confirms it. Inside entries: a 28px gap between the crest column
and the text column, which is what makes them read as one object rather than two.

**Where does the layout feel crowded or disconnected?**
Crowded: the `.dossier` field sits 8px under the entry heading and 16px above the body, so on
short entries the heading, the label and the first line stack up tightly. Disconnected: on the
neighbourhood sections the locator is sticky and the prose can run 1250 words, so by the bottom of
Fenwick the map is still there but the heading that named it is long gone.

**Which content could use more space to stand out?**
The `.pull` epigraph on the home page. It has 30px of left padding against a 3px rule and nothing
else, and it is competing with a full city map directly above it.

**Where could padding, margins and gaps be more consistent?**
The card-like surfaces disagree: `.crest-tile` uses 20px/12px/16px, `.gateway-card` uses
34px/22px/30px, `.entry-row` uses 30px vertical and no horizontal. They read as a family because
they share a border and a background, not because they share a spacing scale. A 4px scale applied
across all three would fix it.

---

## Figure/Ground

**What are the main figures, and what grounds do they sit on?**
The emblems are the primary figures — 24 pieces of white line art, knocked out to transparency and
sitting on `--panel` (#101217) inside a card on `--void` (#08090b). That is deliberate: the source
art was white on black, so the ground it was drawn for is the ground it still has. The secondary
figures are the map locator tiles, which invert the relationship — a bright parchment square on a
near-black page, which is why they pull the eye on `vallam.html`.

**Where does text or an important element blend into its background?**
One measured case: `.crest-absent`, the diamond standing in where an organisation has no emblem,
measures **2.46:1**. It is `aria-hidden` and carries no information, so it is decorative — but it
is below AA and I am recording it as an exception rather than calling the page clean.

**Where could contrast, size or space make a figure stand out more?**
The emblems are set at 86% opacity in the index tiles and 94% in the entry rows. The index is the
thing people scan, so the fainter version is on the wrong element — those two values should swap.

**Do I have text over images? How is it kept readable?**
Yes, on every hero. The image is held at 40% opacity and a `::after` gradient runs from 55% black
at the top through 20% to 97% at the bottom, so the headline and standfirst sit on the darkest end
of the ramp rather than on the photograph. The audit cannot measure a gradient ground, so that
pair is checked by eye, not by number — which is a weaker guarantee and worth saying.

---

## Emphasis

**What is the most important thing on each page?**
Home: the five gateways. World, Fairbourne: the first paragraph, because those pages are read, not
searched. Vallam: the map. Factions, Houses: the crest index, because that is how someone finds the
one entry they came for.

**What draws the eye first, and is it what I want?**
On Vallam, yes — the map is 1500px wide and the only full-colour object on a black page. On Houses,
no. The sepia banner above the crest index is wide and warm and takes the eye before the crests do,
even though the crests are the functional content and the banner is atmosphere.

**Where could I adjust contrast, size or space to emphasise key content?**
Drop the group banners to a smaller inset, or move them below the index. Currently the decoration
is larger than the navigation it sits above.

**Is anything competing that should recede?**
The `.toc-rail`. It repeats every heading on the page at `--muted` in a 212px column, which is right
for scanning but means that on `houses.html` sixteen link texts are visible before any content is.
Collapsing it to the six category names on long pages would let the content lead.

---

## Variety

**Where do elements already differ?**
Size: crests run 64px in an index tile, 106px in an entry row, 86px on a gateway card. Shape: the
emblems are round or shield-shaped, the map tiles are hard squares, the banners are 3:1 letterboxes.
Colour: each part carries its own `--hue` — teal for the world, red for the war, gold for the city,
blue for the factions, violet for the houses.

**What keeps it cohesive?**
One palette of roles rather than one palette of colours: every page uses the same `--void`,
`--panel`, `--rule`, `--bone` and `--muted`, and changes only `--hue`. Three typefaces throughout.
Every bordered surface uses the same 1px `--rule`.

**Where is it too uniform, or too chaotic?**
Too uniform: `world.html` and `dominion.html` are long-form only — heading, paragraphs, heading,
paragraphs, with three images between them. They are the two pages with nothing to scan.
Too chaotic: nowhere measured, but `vallam.html` carries 26 images and four different block types
on one page, which is the most any page is asked to hold.

**Where could one contrasting element help?**
On the two long-form pages. A pull quote or a single inset emblem every few sections would give the
eye somewhere to land, and both pages have unused art available.

---

## Rhythm

**Where do I repeat or alternate arrangements?**
The same two-step repeats on three of the six pages: a Grid index of uniform tiles, then a flowing
list of full-width entries. Factions runs it six times, once per category. Houses runs it twice.
Vallam runs it once. Someone who learns it on one page already knows the next.

**Does the eye move smoothly, or does it stall?**
It stalls in one place: `factions.html` repeats index-then-entries six times with identical spacing,
so the fourth category looks exactly like the first and there is no sense of progress through the
page. The rail is the only way to tell where you are.

**Where could repeating or alternating help?**
Alternating the locator column on `vallam.html` — map left, then map right — would mark each
neighbourhood as a new section without adding a rule or a heading.

**Where would I break the rhythm on purpose?**
Once, and it is already there: `.cat-head.break` gives Criminal Organisations 104px of space instead
of 76px, so the page draws a breath before the underworld. That is the only intentional break, and
keeping it to one is what makes it read as a decision instead of an inconsistency.
