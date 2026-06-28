# Design Notes — internals, dimensions, and fixes already made

Read this when you need to touch the engine, match the visual system exactly, or debug a
case file. The canonical, working implementation is `assets/example-case-01.html` — when in
doubt, diff against it. Everything below documents *why* it is the way it is, including bugs
we already fixed (don't reintroduce them).

## Table of contents
1. Layout & dimensions
2. Color & type system
3. Window-fit scaling (`#scaler`) + drag interaction
4. Read-aloud (TTS)
5. Page navigation
6. Per-page logic hooks to edit
7. Gotchas we already fixed
8. Presentation layer (fonts, paper, cover reveal, stepper, sound, magnifier, red string)

---

## 1. Layout & dimensions

- Stage: `#app` is **1400 × 1300 px** (widened and raised from 960×640 to use a modern
  widescreen and give room for larger fonts), 12px dark border, inside `#scaler` (which
  scales it to the window). `body` is `overflow: auto` so a too-small window can still
  scroll as a fallback — but the goal is that `fitToWindow()` shrinks it to fit.
- Pages: each `.page` is absolutely positioned, full-stage, `padding: 40px 40px`, a flex
  column. Only `.page.active` is visible (opacity + translate transition).
- Vertical budget per page ≈ 1300 − 24 (border) − 80 (padding) ≈ **1196px of content**. The
  bottom button uses `margin-top: auto`, so if inner content exceeds the budget the button
  is pushed out of view — the #1 thing to watch when authoring.
- Per-page italic instruction line under the `.page-title` is sized at **32px**.
- Timeline slots: **240 × 190px**, 5 across via `justify-content: space-between`. Cards
  are 300px wide / 30px font in the tray; when placed (`.card.placed`) they become 28px
  bold and fill the slot. The track is 200px tall. The tray (`.timeline-cards`) wraps to
  two rows if needed and has a min-height of 340px.
- Evidence tiles: 150×150 in the tray; when placed (`.evidence-placed`) they are **enlarged**
  to ~**220px tall** (icon ~124–130px) and drop into a centered `.placed-row` inside the dashed
  `.monster-zone`. The zone is **1180×560** and is a vertically-centered flex column with two
  children — **placed-row → `.reasoning`** — kept compact (one ~26px `gap`) so the enlarged
  card row + reasoning read as one vertically-centered block within the box. Size the placed
  card *width* to the count so the single row fills most of the box (~255px each for 4 cards,
  ~340px for 3) without wrapping. The `.reasoning` box is **in-flow** (`position: static;
  margin: 0 auto`). There is **no** `.monster-drawing` reveal emoji in the box (removed — it
  forced a big mid-gap); the culprit is revealed via the reasoning text and on the Solve page.
  Cork board is **1300×760** (extra is just cork margin). No `getEvidencePosition()` — placed
  tiles are appended, not coordinate-positioned.
- Cover: TOP SECRET stamp is 220×220 / 34px; `Felix's Case File` title is 80px; subtitle
  `#01 — …` is 40px; `.cover-info` box uses 36px monospace text with 60px/120px padding
  and a 320px min-height.
- Solve page: suspect cards are 250px wide with 110px avatars / 30px names; accusation zone
  is 680×320; CASE CLOSED stamp stays 280×280 / 40px font. The overlay uses
  `justify-content: space-evenly` so the stamp, verdict text, and Next/Reward Wall buttons
  are evenly spaced, with equal gaps between them.

## 2. Color & type system

CSS variables on `:root` (keep these identical across the series so all cases match):

```
--paper: #f5f0e1;      --paper-dark: #e8e0c8;   --ink: #2c2416;
--brown: #6b4e3d;      --brown-dark: #4a3528;
--red: #b83a2a;        --red-dark: #8f2a1d;
--yellow: #e6b84a;     --orange: #e07b39;
--shadow: rgba(44, 36, 22, 0.25);
```

Type: body `Georgia, 'Times New Roman', serif`; headings/labels/badges/stamps
`'Courier New', monospace`, uppercase, letter-spaced. The serif-vs-monospace split is what
makes it read as a "file" rather than a webpage — keep it.

Signature components: `.cover-stamp` / `.stamp` (rotated circular rubber stamp),
`.case-badge`, `.btn` (stamped, with a hard drop-shadow that compresses on hover),
`.timeline-line` (dashed → solid `--orange` when complete), `.folder` (manila tab via
`::before`), `shake` keyframe for wrong drops, `fall` keyframe confetti, `popIn` for placed
evidence.

## 3. Window-fit scaling + drag interaction

**Why `#scaler` exists:** the folder is a fixed 1400×1300 canvas. On smaller windows it would
be clipped, so `fitToWindow()` computes `currentScale = min(scaleX, scaleY)` and applies
`transform: scale(...)` to `#scaler`. Runs on load + resize. It scales **both down and up**:
on a big screen the file grows to fill the window (minus a small margin) so the text isn't
left tiny and cramped. (Earlier versions capped at `1` / 100% — that's what made the file
look small on large monitors; don't re-add the cap unless a case genuinely needs it.)

**Drag system** (`makeDraggable` → `startDrag` / `onDragMove` / `onDragEnd`): a single
pointer abstraction for **mouse and touch**. On grab, the element is moved to `document.body`
(escaping the scaled/transformed ancestor) and positioned `fixed`. Key detail: because the
source is measured *inside* the scaled `#scaler`, `getBoundingClientRect()` returns scaled
sizes — so `startDrag` divides width/height and the grab offset by `currentScale` to render
the clone at natural size and keep the cursor on the grab point. Drop targets are detected
with `document.elementFromPoint(x, y)` (viewport coords, scale-independent).

Drop zones are matched by class + `data-*`:
`.timeline-slot` ← `data-order`, `.folder-zone` ← `data-suspect`,
`.monster-zone` ← `data-type`, `.culprit-zone` ← `data-suspect`.
To add a new draggable: give it the right `data-*`, ensure its container is a recognized
drop zone, and call `makeDraggable()` on it in the init block. **Do not** use the native
HTML5 `draggable`/`dragstart` API — it's broken on touch and conflicts with the scaling.

## 4. Read-aloud (TTS)

- `speak(text, btn)` uses `window.speechSynthesis` with `SpeechSynthesisUtterance`,
  `lang='en-US'`, `rate=0.85`. Re-tapping the active button stops it; only one plays at a
  time. The button pulses (`.speaking`) while talking.
- Two button styles:
  - `.speak-btn` — a small round 🔊 added programmatically by `addSpeakButton()` to each
    `.card, .clue, .evidence, .suspect-card`. Positioned at the **outside top-right corner**
    (`top:-9; right:-9`) so it never covers the text. Reads `visibleText(el)`, which skips
    badges and emoji icons (`SKIP_SPEAK`).
  - `.speak-inline` — declared in HTML for text blocks (cover info, reasoning) with a
    `data-speak="..."` attribute carrying a clean spoken version.
- **Win congratulation:** the Solve page's `#finalSpeakBtn` is a `.speak-inline` by the
  verdict title. `showFinalMessage()` fires `speak(btn.dataset.speak, btn)` ~900ms after the
  stamp lands (after the confetti) so the case closes with a spoken "Congratulations,
  detective!…". The button also lets the child replay it. Per case, rewrite its `data-speak`
  to a warm, case-specific line.
- Guards that must stay: `startDrag` early-returns if the pointer is on a `.speak-btn`
  (so tapping the speaker never drags); `placeEvidenceOnBoard` strips `.speak-btn` from the
  cloned tile so placed evidence has no dead button.
- Requires a browser with voices (Chrome/Edge/Safari fine). It degrades gracefully with an
  alert if `speechSynthesis` is missing.

## 5. Page navigation

`goToPage(n)` toggles `.active`/`.prev` on `.page` sections with a small timeout for the
transition. The current page index is `currentPage`. `Next` buttons start `.hidden` and are
revealed by each page's completion check (`checkTimelineComplete`, `checkSuspectsComplete`,
`checkEvidenceComplete`). The cover's "Open File" calls `goToPage(1)` directly.

## 6. Per-page logic hooks to edit

When changing content, these are the only JS spots that need to match the HTML:

- **Timeline:** card/slot count is read from the DOM, so usually no JS change. Keep
  `data-order` correct, and **shuffle the cards' DOM order** so none start in their answer
  slot (the example uses 3, 5, 1, 4, 2).
- **Suspects:** `folderCounts` (init 0 per suspect), `folderTargets` (clues per suspect),
  and the magic total in `checkSuspectsComplete()` (`total === 8` in the example = total
  clue count). The culprit-flag branch in `handleSuspectDrop` names the culprit. **Shuffle
  the clues' DOM order too** — never list them grouped by suspect, or adjacency solves the
  puzzle; interleave so no two same-suspect clues touch (example order: Fang, Harry, Annie,
  Rosamond, Fang, Annie, Harry, Rosamond).
- **Evidence:** `evidenceState` keys must match the tiles' `data-type`; the reveal condition
  checks the real clues (e.g. `yellow && brush && monster`) — rename consistently if you change
  evidence. Real clues are appended into `#placedRow` by `placeEvidenceOnBoard(source, 'clue')`
  (no coordinates). The **distractor is always rejected** — its `handleEvidenceDrop` branch does
  `return false` after `monsterZone.classList.add('shake')` + `showBoardHint()`, so it never
  reaches `#placedRow` or `evidenceState` (and so gets no red string). Only the `.board-hint`
  wording differs per case (silly "Pancakes aren't a clue!" vs. ruled-out "Not the skunk!").
- **Solve:** `handleCulpritDrop` hard-codes the culprit's `data-suspect`. Set it. On a correct
  drop it hides the dragged card and renders the **caught suspect** in the zone — the suspect's
  own avatar emoji (read live from `dragEl.querySelector('.suspect-avatar')`) + name + a rotated
  `CULPRIT` tag, animated in with `culpritLand` — so the face visibly lands instead of the zone
  blanking to a text line. `showFinalMessage()` auto-speaks the `#finalSpeakBtn` congratulation
  ~900ms after the stamp — update its `data-speak` to a case-specific congratulation.

## 7. Gotchas we already fixed (don't reintroduce)

- **Can't scroll / only one page visible:** caused by `body { overflow: hidden }` + a fixed
  stage bigger than the window. Fixed via `#scaler` + `fitToWindow()` and `overflow: auto`.
- **Stage zooms out too far on large screens and looks tiny:** fixed by dropping the
  `min(..., 1)` cap in `fitToWindow()` so the file also scales **up** to fill the window
  (see section 3). Now the layout stays roomy on big monitors.
- **Fonts and boxes felt cramped on the 640px-tall canvas:** fixed by widening/raising the
  stage to **1400×1300px** and bumping key text sizes: `.page-title` 28→42px, buttons
  16→26px, cover-info 16→36px, `.card`/`.clue`/timeline slots 13→18px,
  `.card.placed` 12→16px, folder headings 16→32px, evidence labels 11→22px, reasoning box
  14→26px, final text 20→28px. Always update `fitToWindow()`'s
  divisors from 960×640 → 1400×1300 to match, or the file will render at the wrong scale.
- **Dragged/placed text overflowing its box:** the drag code sets an explicit pixel height;
  if content rewraps in a narrower drop zone it clips. Fixed with `height: auto !important`
  on `.clue.dragging/.placed`, `overflow-wrap/word-break`, and by sizing the drag clone in
  *natural* (un-scaled) pixels.
- **Timeline card text spilling past the slot border:** slots were 70px tall — too short for
  4 wrapped lines. Fixed by enlarging slots to 110px and shrinking placed-card font; the
  page spacing was re-tightened so the Next button still shows.
- **Evidence Board button cut off:** cork board was 320px, pushing the button below 640.
  Trimmed to 240px + tighter gaps.
- **Three evidence tiles overlapping:** 90px tiles dropped at colliding coordinates inside a
  280px zone. First fixed by shrinking placed tiles and laying them in a top row; **now fully
  replaced** by a centered `.placed-row` flex container — tiles are appended (not positioned),
  so any count (3 or 4) stays centered with no overlap math.
- **Placed cards left-aligned / reasoning covering a tile / cards too small:** the old layout
  used absolute per-card `top/left` (`getEvidencePosition()`) + a `bottom:50px` reasoning box,
  so cards hugged the left and the reasoning overlapped a corner tile. An interim fix added a
  centered `.placed-row` but also kept a big `.monster-drawing` between the cards and reasoning,
  which forced a large mid-gap and squeezed the cards small. **Final layout:** drop the
  `.monster-drawing`/`.monster-label` from the box, keep only `.placed-row` + in-flow
  `.reasoning` in a vertically-centered flex column, and **enlarge** the placed tiles (~220px
  tall) into one centered row sized to the card count. Don't reintroduce absolute coordinates
  or the mid-board reveal emoji here.
- **Speaker button covering card text:** moved from inside the card (`top:4; right:4`) to the
  outside corner (`top:-9; right:-9`), mirroring the number badge.
- **File looks small & cramped on big screens:** `fitToWindow()` used to cap the scale at
  `1` (`min(scaleX, scaleY, 1)`), so the fixed 960×640 stage never grew past 100% and sat
  in a sea of empty space with tiny text. Fixed by dropping the cap (`min(scaleX, scaleY)`)
  so the file also scales **up** to fill the window. The drag math already reads
  `currentScale`, so up-scaling stays correct. To make it even bigger, lower the
  `margin` in `fitToWindow()` (currently 24px) or widen the `#app` canvas.

If you hit a new layout problem, prefer **tightening spacing or shrinking placed elements**
over making a page scroll — the fixed-canvas paper look is the whole point.

## 8. Presentation layer (fonts, paper, cover reveal, stepper, sound, magnifier, red string)

This layer was added on top of the base engine. A cloned case inherits all of it for free;
keep these intact unless you mean to change the whole series.

- **Self-hosted fonts.** `@font-face` blocks load `fonts/special-elite.woff2` (titles/headings,
  `Special Elite`) and `fonts/stardos-stencil-400/700.woff2` (stamps/badges, `Stardos
  Stencil`), `font-display: swap`, fallback `Courier New`. The `fonts/` folder must ship next
  to the HTML. Served over http(s) it always loads; on `file://` Chromium usually loads it,
  some browsers fall back — that's fine. Body text stays `Georgia`.
- **Paper texture.** Two parts. (1) The **sheet** itself: `#app` carries a kraft-paper
  background — a warm radial tonal wash + a **sepia-tinted** `feTurbulence` mottle, both
  rendered as a *single full-sheet image* (`background-size: 100% 100%`, `no-repeat`) and
  `background-blend-mode: multiply` over a yellow kraft base (`#efe1bd`). Rendering the noise
  full-size (not a tiled 200px swatch) is deliberate — tiling showed visible seam "grid lines."
  The noise is tinted warm via `feComponentTransfer` (R>G>B funcs) so the specks read brown,
  not the cool grey a plain `saturate 0` grain gives. It sits *behind* the transparent pages,
  so it shows on bare paper and barely touches cards/text. (2) `#app::before` is a faint
  (`opacity:.10`, `mix-blend-mode:multiply`) warm fine-grain over *everything* (also a single
  full-sheet image, no tiling); `#app::after` is just an inset vignette. Both
  `pointer-events:none`, `z-index:3` (above pages, below the `.final-message` win overlay at
  100). Keep both layers seamless (full-cover, not tiled) and warm-tinted; we tried a neutral
  tiled grain and it looked cool and gridded. We also tried coffee-ring stains and removed
  them — looked random. To dial intensity: `#app::before` `opacity` for the speckle, the
  mottle `feFunc*` `slope`/`intercept` for the blotch contrast, the radial alpha for the
  vignette, and the base `#efe1bd` for overall warmth/lightness.
- **Cover reveal (sealed → opened).** The cover ships sealed: only `.cover-open-btn` shows;
  `.cover-reveal` (title/stamp/info/start button) is `display:none`. Clicking adds `.opened`,
  which both reveals `.cover-reveal` and fires the staggered entrance keyframes
  (`stampDrop`, `riseIn`, `popBtn`). The `TOP SECRET` stamp is absolutely positioned over the
  end of "Case File" (`left:100%; margin-left:-50px; top:72%`) so it only kisses the last "e".
  **Why gated:** the click unlocks the Web-Audio context so the stamp thunk always plays.
- **Progress stepper.** One shared `#progressStepper` (5 `.step-dot`s) lives in the top band,
  `position:absolute; top:20px; left:50%`, `z-index:4`, `pointer-events:none`. `updateStepper(n)`
  (called from `goToPage`) toggles `.done`/`.active`; hidden on the cover (`n>=1` shows it).
- **Per-page prop.** Each page's first child is a `.page-prop` emoji watermark
  (`position:absolute; bottom-right; opacity:.24; z-index:-1`) — purely decorative.
- **Sound (Web Audio, no assets).** `getCtx()` lazily creates/resumes one `AudioContext`.
  `playPinSound()` = short triangle blip on every correct drop; `playStampSound()` = sine
  thud + noise burst for the cover/CASE-CLOSED stamp. Calls are safe before unlock (they just
  no-op while suspended). No mute button by design.
- **Magnifier cursor.** A data-URI SVG magnifier is set as `cursor` on inspect surfaces
  (`.card, .clue, .evidence, .suspect-card, .cork-board, .clues-pool, .timeline-cards,
  .suspect-lineup`), fallback `grab`. Buttons keep the normal pointer.
- **Evidence polaroids + pushpins + red string.** Placed tiles are white cards
  (`.evidence-placed`, `position:relative`) with a red pushpin `::before` and an alternating
  tilt baked into `popPinL/R` keyframes (`both` fill so the tilt persists). The
  `.string-layer` SVG (`viewBox="0 0 1180 560"`, `preserveAspectRatio="none"`, `z-index:0`) sits
  behind the cards (`.placed-row`/`.reasoning` are `z-index:1`). `drawStrings()` (fired ~380ms
  into `revealMonster`) measures each `[data-role="clue"]` card and the reasoning box with
  `getBoundingClientRect()`, **divides by `currentScale`**, and draws a quadratic path per clue
  with a `stroke-dasharray` draw-on. It is generic over clue count — never hard-code 3 or the
  distractor's `data-type`; drive it off `data-role` (`placeEvidenceOnBoard(source, role)`).
