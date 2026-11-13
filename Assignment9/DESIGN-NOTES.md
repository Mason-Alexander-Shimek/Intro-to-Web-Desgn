# Design Document, Module 7 Principles

Answered against the built pages. Numbers come from `build/audit.py`, not from impression.

The spacing distinctly distinguishes between listings using 44 pixels margin and 3 pixels line, separates answers with colored background and 22 pixels space, and places the labels next to the values. But equal height for all the answers creates an unnecessary empty space under some answers, and the checklist appears not related to the last listing. The row “CALL FIRST” requires additional space since the consequences of ignoring it can be really severe.

Phone numbers are the most distinctive numbers, written in white against solid blue backgrounds, while urgent messages have distinct dark red backgrounds, pale red backgrounds, and solid left borders. All texts meet the AA level of contrast criteria although the lack of imagery makes it easier, as an intentional design decision to make weak links, even though it makes it less warm. The white-bordered “Where and when?” box is also distinguishable among other answers, and quite rightly so since users need to read it.

The homepage highlights the four category links and the category page highlights urgent notifications and phone numbers rather than descriptive text. The yellow banner for demonstration purposes is highlighted before the headline, which is fine for the demo but not the case for the final version of the website. Calls to action for the category links need to be more prominent, and the organizational credits need to be shifted to location details.

Variation derives from unique treatment of panels, size of typography and two accents colours - blue (action) and red (urgency). Harmony stems from one font type, rules for making the listings and the constant sequence of four answers. Predictability is useful, but long pages may seem monotonous. The contrasting element between listings would help users keep track of their location, especially on mobile devices, where several panels are stacked and listings become hard to distinguish from one another.

Constant listing sequence (name, organisation, summary and four answers) provides a constant rhythm as well as listing of heading, urgent notice and jump list on each category page. Smooth reading is possible within the listings, but not between them, especially on mobile devices, when twelve similar panels follow one after another. Listing numbering would bring back the feeling of progress. Urgent cards are deliberately disrupting the rhythm as the only red elements on the page. The health page uses the actual 988 number.

---

# Design Document, Module 9 Principles

Differentiation and attention, answered against the refined pages. Numbers come from
`build/audit.py` and `build/photo_audit.py`, not from impression.

**Space.** The hero now sets the start page apart from everything under it, which the old
drawn band never quite did: 34 pixels of padding inside the overlay, a 34 pixel gap below it,
and then the five doors. On the About page the four text blocks run at 34 pixel intervals with
body copy capped at 64 characters per line, so the eye has a fixed left edge and a predictable
return. The preview row uses a 16 pixel gutter, tighter than the gap between sections, which
is what makes three separate cards read as one group rather than three unrelated panels. The
one place space is still doing too little is between listings on a long category page, which
the Module 7 notes already flagged and this module has not fixed.

**Figure/Ground.** This is the principle the photographs forced. Type on a photograph has no
reliable ground, so the hero paints one: a gradient scrim from 93% opaque at the bottom to
fully transparent at the top, which lets the sky and the mountains stay visible while
guaranteeing a dark field under the words. It was measured rather than eyeballed, by hiding
the text, photographing the hero, and sampling the real pixels behind each line. At 1200px the
eyebrow reads 6.99:1 against a required 4.5, and no pixel in the measured area falls below the
line. At 390px the same approach failed at 1.24:1, because the heading and lede wrap to nearly
the full height of the hero and leave no clean ground anywhere, so below 700px the overlay is
abandoned entirely and the words move onto paper under the picture. Every other photograph on
the site carries no text at all, by rule: the valley band and the three place previews put
their captions underneath, on a solid background.

**Emphasis.** The hero is the largest grouping on the start page and reads first, with the gold
eyebrow, a 40 pixel white heading and the lede stacked as one block in the lower left. Under it
the five doors are equal to each other on purpose, because the site cannot know which need
brought someone here, and ranking them would be a guess. The real emphasis lives in the urgent
card, which stays the only red element on any page and the only one with a solid left bar. The
About page inverts this: its banner carries no words, so the heading beneath it is the first
thing read. Phone numbers remain the most emphasised thing in the system, white on solid blue,
at 44 pixels minimum.

**Variety.** The pages now mix five treatments where they used to mix three: a photographic
hero with an overlay, a panoramic banner with a caption, cards, previews, and plain text
blocks. Two accent colours still carry all the meaning, blue for action and red for urgency,
and the gold eyebrow is the only third colour on the site, used once per page and only against
a dark ground. The photographs supply most of the new variety, which is why the category pages
can go without them and still not feel monotonous: they have the four-answer structure doing
that work instead.

**Rhythm.** The three place previews on the About page are the clearest repeating unit in the
project. They share one 3:2 image ratio even though the source photographs are 1.50, 1.51 and
1.78, so the row of images aligns and the eye moves across at a steady pace. The Module 9
case study asks why a designer would prioritise space over alignment and let card images
differ in height; here the answer went the other way, because these three cards carry different
amounts of text and letting the images disagree as well would have left nothing in the row to
hold on to. The start page keeps its old rhythm, five doors then a crisis card that breaks it
deliberately, and the new About teaser at the bottom is a single wide preview rather than a
repeat, so it reads as a destination rather than another item in a list.

**Affordances.** Everything pressable is salient rather than emergent: links are blue and
underlined on hover, every tap target clears 44 pixels, the crisis number is a filled button
with its own verb, and each door ends with a count, "See 3 ways to get help", so the link
promises something specific rather than inviting exploration. Nothing on this site should have
to be discovered.
