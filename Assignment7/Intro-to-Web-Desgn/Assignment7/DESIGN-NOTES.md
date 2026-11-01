# Design Document — Module 7 Principles

Answered against the built pages. Numbers come from `build/audit.py`, not from impression.

---

## Space

**Where am I already using space to separate or group content?**
Three scales, and they do all the grouping. Between listings: 44px of margin and a 3px rule, so a
listing is unmistakably a separate thing. Inside a listing: the four answers sit in tinted panels
with 22px between them, so the panel edge does the grouping and no heading has to say "this is a
different question". Between a label and its value in `.where-row`: 14px, tight enough that
"ADDRESS" and the street clearly belong together.

**Where does the layout feel crowded or disconnected?**
Crowded: the `.answers` grid stretches all four panels to the tallest, so "What do I bring?" with
five short items gets the same height as "How do I apply?" with five long steps, and the short one
ends in a block of empty tint. Disconnected: the printable checklist sits 56px below the last
listing with no visual tie back to it, so on a long page it reads as a new page rather than a
summary of the one above.

**Which content could use more space to stand out?**
The `CALL FIRST` row inside "Where and when?". It is the single most expensive thing to get wrong —
a wasted bus fare and half a day — and it currently gets the same 9px row padding as the bus route.

**Where could padding, margins and gaps be more consistent?**
`.answer` uses 18/20/20, `.urgent-card` uses 24/22/26, `.jump-nav` uses 16/18/18, `.checklist` uses
26/24/28. Four panels, four spacing recipes. They look like a family because they share a tint and
a rule weight, not because they share a scale.

---

## Figure/Ground

**What are the main figures, and what grounds do they sit on?**
The phone numbers. Each one is white on `--accent` (#10477c), a solid filled block on either white
paper or a pale tint — the highest-contrast object on the page, and deliberately the one that looks
most like something you press. Second: the urgent card, dark red on `--urgent-tint`, with a 10px
left bar so it reads as a block even in peripheral vision.

**Where does text or an important element blend into its background?**
Nowhere, measured. Every text and background pair on all five pages passes AA at both widths. That
is a cheap win here and I should say why: this design has no images, so there is no case where type
sits on something unpredictable. It is the absence of a hard problem, not the solving of one.

**Where could contrast, size or space make a figure stand out more?**
`.answer-where` is already set apart — white with a 2px border while the other three answers are
tinted and borderless. That is the strongest figure/ground move in the listing and it was made for a
reason: "where and when" is what you act on after you have decided you qualify.

**Do I have text over images? How is it kept readable?**
No. There are zero images on the site. That is a decision taken from the brief — "loads on a weak
signal" — and it removes the whole class of problem. It also costs the site warmth, which is a real
trade: this design is legible before it is friendly.

---

## Emphasis

**What is the most important thing on each page?**
Start page: the four doors. Category pages: the urgent card, then the phone number inside whichever
listing applies. Not the prose.

**What draws the eye first, and is it what I want?**
On a category page, yes — the urgent card is the only red object above the fold and it is sized to
win. On the start page, not quite. The yellow demo banner sits above the headline and currently
takes the eye first. That is correct for an honest demonstration and wrong for a real site, and the
banner comes out when real content goes in.

**Where could I adjust contrast, size or space to emphasise key content?**
The `See 3 ways to get help ›` line on each door is the actual call to action and is the smallest
text in the card at 16px. It should be the second-largest thing in it, not the smallest.

**Is anything competing that should recede?**
`.run-by` — "Run by [Organisation name]" — sits between the listing name and its summary, in the
reading path, and almost nobody needs it before they know whether they qualify. It belongs down in
"Where and when?" with the address.

---

## Variety

**Where do elements already differ?**
Shape: tinted borderless panels for three answers, a bordered white one for the fourth, a filled
block for every phone number, a 10px-barred card for anything urgent. Weight: 38px bold headline,
30px listing name, 19px answer heading, 17px list item. Colour: exactly two hues carry meaning —
blue for *do this*, red for *this cannot wait*.

**What keeps it cohesive?**
One typeface for everything. Two accent colours and no more. The same 3px rule above every listing
on every page. And the four answers in the same order, twelve times, which is the strongest
unifying device on the site.

**Where is it too uniform, or too chaotic?**
Too uniform: by the third listing on a page, the four-panel block has no variation at all. That is
the intended trade — predictability is the product here — but it does mean a long page reads flat.
Too chaotic: nowhere. If anything the site is under-varied.

**Where could one contrasting element help?**
Between listings. A single rule, or the listing's name repeated as a running marker, would tell you
how far down a page you are. Right now the only way to know is the jump list at the top.

---

## Rhythm

**Where do I repeat or alternate arrangements?**
The listing template is the rhythm: name, who runs it, one-line summary, then four answers in a
fixed order. It repeats three times per page across four pages. Every page also opens on the same
three beats — heading, urgent card, jump list — so the shape of a category page is learned once.

**Does the eye move smoothly, or does it stall?**
It moves smoothly within a listing and stalls between them. The 3px top rule is the only marker
that one has ended and the next begun, and at phone width, where the four answers stack into a
single column, three listings become twelve near-identical panels in a row.

**Where could repeating or alternating help?**
At phone width specifically. Numbering the listings (1 of 3, 2 of 3) would restore the sense of
progress the stacked layout removes.

**Where would I break the rhythm on purpose?**
Once per page, and it is already built: the urgent card. It is the only red element, the only one
with a thick left bar, and it sits above the rhythm rather than inside it — so it reads as an
interruption, which is exactly what it is. On the health page it breaks further still: the number
is 988 rather than a placeholder, because that one is real and someone might need it today.
