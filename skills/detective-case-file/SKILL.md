---
name: detective-case-file
description: >-
  Build a single-file interactive HTML "detective case file" learning game for the
  Fantastic Felix / 大侦探 Felix book series — a kid clicks through a paper case folder and
  solves a mystery by dragging clues, ordering a timeline, sorting suspects, assembling
  evidence, and naming the culprit, while practicing the chapter's English vocabulary
  (with tap-to-hear read-aloud). Use this skill whenever the user wants to turn a Fantastic
  Felix chapter/word list into an interactive game, asks for a "case file", "案件文件",
  "侦探游戏", a reading/vocabulary activity for these books, or a drag-and-drop mystery for
  kids — even if they don't say the words "HTML" or "game". Also use it to extend, restyle,
  or fix an existing case file built from this template.
---

# Fantastic Felix — Detective Case File Builder

## What this builds

A `.html` case folder plus a tiny `fonts/` folder and the shared `rewards.js` — it opens
like a detective's paper case file. A child reads a short mystery adapted from a Fantastic
Felix chapter and solves it across five pages of **drag-and-drop puzzles**. Every piece of
text can be **tapped to hear it read aloud**, drops give a soft synthesized "pin" click, and
the case closes with a rubber-stamp thunk. It is built to be **served (e.g. GitHub Pages)**
but also runs by double-clicking the file; it works with mouse or touch and auto-scales to
fit the window. The only assets are the self-hosted display fonts in `fonts/` (which
gracefully fall back to `Courier New` if blocked) and `rewards.js`; everything else is inline
CSS/JS and emoji.

The mechanical engine (page navigation, drag-and-drop, window-fit scaling, read-aloud,
sound, progress stepper, evidence red-string) is **already solved and battle-tested** in
`assets/example-case-01.html`. Your job for a new case is almost entirely **content
authoring** — keep the engine, swap the story.

## How to build a new case file

1. **Read the source chapter / word list.** Identify: the client, the missing/mystery
   object, 3–4 suspects (people, pets), the real culprit, and the key vocabulary words the
   chapter teaches. Fantastic Felix cases always resolve with a small logical deduction
   (e.g. *wet yellow paint + red paint = orange monster*) — find that "aha" for the
   Evidence Board.
2. **Clone the example *and its assets*.** Copy `assets/example-case-01.html` to the user's
   target path (e.g. `detective_case_file_0N.html`). Also make sure the **`fonts/` folder**
   (the three `.woff2` files) and **`rewards.js`** sit next to it — they're shared across all
   cases, so usually they already exist in the project; copy `assets/fonts/` in if not. The
   HTML references them by relative path (`fonts/special-elite.woff2`, `rewards.js`).
3. **Replace only the content slots** (see the page-by-page guide below). Leave the
   `<style>` block and the `<script>` block alone except for the small per-page data they
   reference (card counts, suspect names, the culprit's name).
4. **Re-check the invariants** (see "The engine — don't break these").
5. **Verify it fits.** Each page must fit inside the 1400×1300 frame with the bottom button
   visible. Open it and walk all five pages. If content is too tall, tighten spacing —
   don't let the file scroll internally.

For deeper internals (color palette, exact dimensions, how drag/scaling/TTS work, and the
bugs we already fixed so you don't reintroduce them), read
`references/design-notes.md`.

## The five-page flow

The case is a fixed sequence. Each page is a `<section class="page" data-page="N">`. The
player unlocks the **Next** button by completing that page's puzzle; navigation is the
`goToPage(n)` function. Keep this arc — it mirrors how Felix actually solves cases (gather
→ narrow → reason → accuse) and gives a satisfying build-up.

| # | Page | Puzzle | Teaches |
|---|------|--------|---------|
| 0 | **Cover** | "Open the Case File" → animated reveal | The case setup: client, missing item, location |
| 1 | **The Case Timeline** | Drag shuffled event cards into 1→5 order | Sequencing, past-tense narration |
| 2 | **Suspect Files** | Drag each clue into the right suspect's folder | Matching facts to characters |
| 3 | **Evidence Board** | Drag the key evidence onto the board to reveal the deduction | The logical "aha", cause/effect |
| 4 | **Solve the Case** | Drag the culprit into the accusation zone → Case Closed | Conclusion, payoff |

### Content slots per page

**Page 0 — Cover.** Fill the `.cover-info` rows: `Client`, `Missing`, `Location`,
`Status: OPEN`. Update the two-line `<h1>` (`Felix's` / `Case File`) and `.subtitle`
(`#0N — The <Case Name>`). Keep the `TOP SECRET` stamp.

The cover is **sealed → opened**: on load it shows only a `.cover-open-btn`
("📂 Open the Case File"); the title/stamp/info live inside `.cover-reveal` (hidden until
opened). Clicking the button adds `.opened` to `.cover`, which fires the staggered entrance
(title rises → `TOP SECRET` stamp slams onto the end of "Case File" → info cascades →
"Start Investigation →" pops in). **This gating is deliberate** — the click is the user
gesture that unlocks the Web-Audio context, so the stamp-thunk sound is *guaranteed* to play
(browsers block audio before any gesture). Don't move the reveal back to auto-play-on-load or
the cover sound goes silent on first load.

**Page 1 — Timeline.** Write 5 short past-tense event sentences in `#timelineCards`, each a
`<div class="card" data-order="K">`. **Keep `data-order` = the correct chronological
position** but **shuffle the DOM order** so the puzzle isn't pre-solved. There are exactly 5
slots; if you want more/fewer events, add/remove both a `.timeline-slot` and a `.card` and
keep the counts equal. Keep sentences to ~1 short line — long sentences feel like work, not
play.

**Page 2 — Suspect Files.** One `.folder[data-suspect="Name"]` per suspect (4 in the
example). Each clue is a `.clue[data-suspect="Name"]` in `#cluesPool`. A clue is accepted
only by its matching folder. **Shuffle the clues in the DOM** — never list them grouped by
suspect (Annie, Annie, Fang, Fang…), because adjacency hands the child the answer. Order
them so no two clues for the same suspect touch and the sequence doesn't mirror the folder
layout (e.g. Fang, Harry, Annie, Rosamond, Fang, Annie, Harry, Rosamond). A fixed order is
fine — it just has to be genuinely mixed, the same way the timeline cards are shuffled. In
the JS, update `folderCounts`, `folderTargets` (clues per suspect), and the total in
`checkSuspectsComplete()` (it equals the total number of clues). The culprit's folder is
flagged specially (the example flags `Harry` as `SUSPICIOUS...` instead of `CLEARED`) —
point that flag at your real culprit.

**Page 3 — Evidence Board.** Put the **real** evidence tiles (2–4, however many the chapter's
deduction needs) + 1 distractor in `#evidenceTray` (`data-type`). The real ones, when all
dropped, trigger the reveal — the dashed box highlights (`.monster-zone.revealed`) and
`#reasoning` (the deduction, often a color-mix or simple logic) fades in. Update the reasoning
text and the `evidenceState` keys if you rename types. **Vary the distractor per case** —
don't make every case's red herring 🥞 Pancakes.

**Always reject the distractor** (shake + hint + bounce back), whatever flavor it is — a
silly prop *or* a real ruled-out lead. Dropping it on the board shakes the box
(`monsterZone.classList.add('shake')`), flashes a one-line `.board-hint`, and bounces it back
to the tray (`handleEvidenceDrop` returns `false` for that type; it never enters
`evidenceState` or `#placedRow`, so it gets no red string). Only the hint *wording* changes
with flavor:

- **A silly, unrelated prop** (🥞 pancakes, 🦴 bone, 🧦 sock, 🍪 cookies, 🪁 kite — vary it
  per case) → a playful "not evidence" line, e.g. *"Pancakes aren't a clue!"*
- **A wrong lead the detective actually ruled out** (e.g. the skunk Felix blames before
  realizing it was his own dog) → e.g. *"Not the skunk! Felix ruled it out."*

Rejecting it teaches the elimination step; *accepting* a distractor reads as "this was part
of the answer," which muddies the deduction — so never place it on the board. The case is
solved by the **real clues only** (however many the chapter has — 2, 3 or 4); the distractor
never gates Next. Case 01 (silly pancake) and Case 02 (ruled-out skunk) are both reference
implementations of the reject behavior.

**Board layout — big centered cards, compact column, no absolute coordinates.** Placed clues
drop into a centered `.placed-row` (`#placedRow`) that lives *inside* the dashed
`.monster-zone`, which is a vertically-centered flex column. Its children are the
`.string-layer` SVG (behind), the **placed-row**, and the **`.reasoning`** box. Placed tiles
are **enlarged** white **polaroids pinned to the cork** (`.evidence-placed` ≈ 220px tall,
~124px icon, a red pushpin via `::before`, alternating ±2.5° tilt) and sit in **one centered
row** — size their width to the card count so the row fills most of the box width without
wrapping (≈255px each for 4 cards, ≈340px for 3). Keep the row + reasoning **compact** (one
`gap` of ~40px) so the pair reads as one vertically-centered block that fits the box height.
There is **no separate big "monster" reveal emoji** — it ate the vertical space; the culprit
is revealed by the reasoning text (its logic chain ends on the culprit's emoji) and again on
the Solve page. Do **not** reintroduce absolute per-card `top/left` coordinates, a
`bottom:50px` reasoning box, or a full-size `.monster-drawing` between cards and reasoning.

**Red "case string" — keep it generic over the clue count.** On reveal, `drawStrings()` draws
a red string from each real clue down to the conclusion box (SVG path, `stroke-dasharray`
draw-on, positions measured live and divided by `currentScale`). It connects **every
`#placedRow .evidence-placed[data-role="clue"]` card**, so it works for **2, 3 or 4** clues
with no change. The mechanism is `placeEvidenceOnBoard(source, role)`: pass `'clue'` for real
evidence (gets a string) and `'distractor'` for the accepted fun prop (no string). **Never
hard-code the clue count or the distractor's `data-type`** in the string code — drive it off
`data-role` so any case's clue count and any distractor name just work.

**Page 4 — Solve the Case.** One `.suspect-card[data-suspect="Name"]` per suspect in the
lineup. `handleCulpritDrop` accepts only the culprit — **set that name to your culprit.**
When the culprit lands, the zone shows the **caught suspect** (its avatar emoji + name + a
rotated `CULPRIT` tag, dropped in via the `culpritLand` animation) rather than blanking to a
plain text line — so the dragged face visibly "lands" in the accusation zone instead of just
vanishing. `handleCulpritDrop` reads the avatar from the dragged card
(`dragEl.querySelector('.suspect-avatar').textContent`) so it works for any suspect emoji.
Update the `#finalMessage` verdict text and keep a Felix-style closing quote (he signs off
as the great detective with a light, playful aside). The win screen also **reads a
congratulation aloud automatically** — `showFinalMessage()` calls `speak()` on the
`#finalSpeakBtn` button (~900ms after the stamp lands), and a 🔊 button sits by the verdict
title to replay it. Update that button's `data-speak` to a warm, case-specific congratulation
(e.g. "Congratulations, detective! You solved the case! …") so finishing feels rewarding and
gives one last bit of listening practice. Size the main final text around 42px and the Felix quote around 32px.

## The engine — don't break these

These are the invariants that make the file work everywhere. Changing them is how case
files silently break:

- **Self-contained folder, three relative deps.** Everything is inline (one `<style>`, one
  `<script>`, emoji for art) **except** the self-hosted `fonts/*.woff2` and `rewards.js`,
  referenced by relative path. Keep those next to the HTML. No CDNs, no build step. It's
  meant to be served (GitHub Pages) but also opens by double-click; the fonts fall back to
  `Courier New` if a browser blocks `file://` font loads.
- **Fixed 1400×1300 stage inside `#scaler`.** The `fitToWindow()` function scales the whole
  folder to the window; drag math reads `currentScale` to stay correct when scaled. Keep
  the `#scaler` wrapper around `#app`. Don't switch the layout to fluid/responsive units —
  the paper-folder look depends on the fixed canvas. **Anything measured for geometry (the
  evidence red string) must divide `getBoundingClientRect()` values by `currentScale`.**
- **Unified pointer drag system.** `makeDraggable()` + `startDrag/onDragMove/onDragEnd`
  handle **both mouse and touch**. New draggable items just need the right `data-*`
  attribute and a `makeDraggable()` call in the init block. Don't reach for the native
  HTML5 drag API — it doesn't work on touch and fights the scaling.
- **Each page fits in 1300px tall with its Next button visible.** This is the most common
  regression. After adding content, confirm nothing is clipped at the bottom. The top band
  holds the shared `#progressStepper` (5 dots, updated in `goToPage()`) and each page a faint
  corner `.page-prop` watermark — both are decoration, don't let them push content down.
- **Read-aloud on every text item.** Per-item 🔊 buttons are added in `initReadAloud()` via
  `addSpeakButton()`; inline blocks (cover info, reasoning) use `.speak-inline` with a
  `data-speak` attribute. Speech uses the browser `speechSynthesis` API (`en-US`, slow
  rate). Speaker buttons must never start a drag (guarded in `startDrag`) and must be
  stripped from cloned/placed copies.
- **Synthesized sound, gesture-gated.** `playPinSound()` (soft tick on a correct drop) and
  `playStampSound()` (CASE CLOSED / cover thunk) are generated with the Web Audio API — no
  audio files. The audio context only unlocks after a user gesture, which is why the cover is
  sealed behind the "Open the Case File" click. There is intentionally **no mute button**.

## Aesthetic

Detective / aged-paper / rubber-stamp. **Display type is self-hosted: `Special Elite`
(distressed typewriter) for titles/headings, `Stardos Stencil` for stamps and badges**; body
story text stays `Georgia` serif. The typewriter-vs-stencil contrast over a serif body sells
the "case file" feel. Warm paper-and-ink palette (creams, browns, a detective red, accent
yellow/orange), with a faint **paper grain + vignette** on `#app` (via `::before`/`::after`).
Signature touches: dashed drop zones, double-rule dividers, drop-shadow "stamped" buttons,
shake on a wrong drop, a **magnifier cursor** across the whole case file (every page), evidence shown as
**cork-board polaroids with pushpins and a red connecting string**, soft synth "pin" clicks,
and the payoff — confetti + a rotated `CASE CLOSED` stamp that **presses down with a thunk**.
The exact CSS variables and values are in `references/design-notes.md` — reuse them so every
case in the series looks like one consistent set.

Keep the tone light and kid-friendly: short sentences, a little humor, a playful
red-herring gag (varied per case), and a clear win state. The reward for finishing is the
stamp + confetti + Felix's sign-off quote.

## Build checklist

- [ ] Cloned `example-case-01.html` to the right path **and** `fonts/` + `rewards.js` sit next to it
- [ ] Cover: client / missing / location / title / subtitle updated; left the sealed→`.opened` reveal flow intact (so the stamp sound stays gesture-unlocked)
- [ ] Timeline: 5 short events, `data-order` correct but DOM shuffled, slot count = card count
- [ ] Suspects: folders + clues match; clues DOM order shuffled (not grouped by suspect); `folderTargets` and the complete-total updated; culprit folder flagged
- [ ] Evidence: real clues (2–4) + 1 distractor (varied per case, not always pancakes); the distractor — silly prop *or* ruled-out lead — is **always rejected** (shake + `.board-hint`, bounces back, never placed); reasoning text + `evidenceState` consistent; only the real clues gate Next
- [ ] Evidence red string: clues placed with `role 'clue'`, distractor with `'distractor'`; no hard-coded clue count or distractor `data-type` in `drawStrings()` (works for 2/3/4 clues)
- [ ] Solve: lineup matches suspects; `handleCulpritDrop` points at the real culprit; verdict + Felix quote written; `#finalSpeakBtn` congratulation auto-plays on win
- [ ] Read-aloud works on every page (tap 🔊, hear English); progress stepper + per-page prop show correctly
- [ ] Sound: a soft click on correct drops, the stamp thunk on cover open and on CASE CLOSED
- [ ] All five pages fit 1400×1300; every Next/Open button is fully visible
- [ ] Opened in a browser and played start → finish with both mouse and a touch/trackpad
