## Assignment 4, README Questions

**Which icons did you ultimately use and for what purposes?**
Six, each with one fixed meaning so they can be learned, being terminal. They are drawn on the same 96px grid with the same stroke weight and geometrics, so they read as one set. Each is drawn in the phosphor of the page it belongs to, which is why the alert icon is red and the rings icon is blue. On the Orihia page the headings are solid red bars, so the icon there gets `filter: brightness(0)` to knock it back to the same near-black as the heading text instead of disappearing into the background. There are also sixteen registry marks, one per organisation on the factions.

**Which consistent colors, values, lines, and/or shapes did you utilize and why?**
Six colour roles, with each page using the same six in a different hue. Value does most of the work. The screen is nearly black, body text sits high above it, and the full phosphor is reserved for things that need attention. The screen is never pure black, because a CRT carries a faint cast from its phosphor even where nothing is lit.

**Which Google Fonts did you use and for what purposes?**
Two. VT323 for the `h1` in every hero and nowhere else, then IBM Plex Mono for everything else.

**What information does your table organize, and why was a table appropriate?**
The eight subsectors of Moscow, as a roll number, a name and a one-line summary. A table was right because it is the same three facts repeated eight times, and because mid-session you either scan the name column for the district you want, or you roll a d8 and read across to find out what you got.

**What specific style choices helped you structure and organize your form?**
First was `display: block` on the labels, so each one takes its own line and pushes its field underneath it. The contrast means you can tell at a glance which lines are questions and which are answers. Box sizing start and stopping all start and stop on the same two vertical lines rather than each being as wide as its own thing makes it. As previously mentioned, the panel background is also one step lighter than the screen, so the whole form reads as a single object rather than loose fields on a page. The fieldset's default border is also removed, because the panel already draws that boundary and two nested boxes looked like a mistake.

**What is the goal of your form, and how did it support your site's goals?**
The goal is to get a question asked in one sitting, before the reader decides it is easier to just message me and then forgets. The site exists so players can look things up themselves instead of asking me
during play. The homepage said "feel free to ask" and gave no way to do it, so we made a form to answer the question.

**How does the gallery support your website's goals?**
Players hear organization names in play long before they meet anyone from them, and they see the marks stenciled on things. The gallery just gives marks in one block with their names, so you can match a mark
you saw to a name, then read the full entry below. Without it, the factions page was sixteen paragraphs with no way in.

**What pattern did you use: uniform, alternating, or something else, and why?**
Uniform. Every tile is the same size and holds the same two things in the same order, mark then name. The whole point is comparing marks against each other, so anything that varied between tiles would read as a difference in status or type between the organisations. They are all equally unfamiliar until you meet one.
  its own margins to escape it.
- **The card row does not bottom-align.** Three cards of uneven height sit on
  their tops. Flexbox would fix it and I have not rebuilt that component yet.
