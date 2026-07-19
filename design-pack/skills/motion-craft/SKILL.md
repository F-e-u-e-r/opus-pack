---
name: motion-craft
description: Implementation-agnostic motion judgment for product UI. Load when you are adding, reviewing, or tuning animation in any framework - durations, easings, springs, staggers, entrances/exits, gesture handoff, reduced motion - when a spec says "smooth" or "delightful" with no numbers attached, or when you notice animation being judged by feel instead of against a budget. NOT for debugging one animation library's API (use its docs), for static visual decisions (ui-design-craft), or for running a design review end-to-end (design-review-gate).
---

# Motion Craft

Every animation must serve **feedback** ("it worked"), **continuity** ("that's
where it went"), or **hierarchy** ("look here"). An animation serving none of
the three is removed, not tuned. When in doubt: shorter, subtler, or none.

## 1. Duration budgets

Numbers first; taste second. Defaults for product UI:

| Surface | Budget |
|---|---|
| Hover / press feedback | 90-160ms |
| Tooltip, micro popover | 80-200ms |
| Dropdown, select, small panel | 150-250ms |
| Accordion, tab switch | 160-240ms |
| Card / list item entrance | 180-350ms |
| Modal, drawer, sheet | 200-400ms |
| Route / page transition | 240-500ms |

- **Standard interactions stay under 300ms; nothing in product UI exceeds
  500ms.** A 180ms dropdown reads as more responsive than a 400ms one.
- **Exit = 65-75% of entrance.** Leaving is confirmation, not an event.
  The rows above bound ENTRANCES; a rule-derived exit may drop below its
  row - that is the intent, not a violation.
- **Distance scales duration:** 100px is the base; 200px ~1.3x, 400px ~1.6x,
  full-screen ~1.8-2.0x. Small moves at long durations read as lag.
- **Frequency scales duration DOWN.** An action done 100 times a day
  approaches instant. Hard sub-rule: **never animate keyboard-initiated
  actions** - they repeat hundreds of times daily and animation makes them
  feel disconnected from the keystroke.
  ❌ "the command palette fades in over 250ms - it looks polished in the demo."
  ✅ keyboard-opened palette appears instantly; its pointer-opened twin may
  animate.
- Trigger for this section: any duration you are about to write, or any
  existing duration outside the table. Done when every duration in the diff
  sits inside its row's budget or carries a written justification.

## 2. Easing

| Direction | Curve | Why |
|---|---|---|
| Enter | ease-out | fast start = instant feedback, soft landing |
| Exit | ease-in | soft start, fast leave |
| On-screen move / morph | ease-in-out | smooth both ends |
| Spinners, progress, marquee | linear | mechanical processes read linear |

- **Never linear for finite point-to-point movement; never ease-in for
  entrances.** Continuous mechanical motion - spinners, progress bars,
  marquee loops - is the linear exception the table names, not a
  contradiction of it. An ease-in dropdown at 300ms feels slower than
  ease-out at the same 300ms: it delays movement in the exact frames the
  user watches most closely.
- Named defaults: Material 3 standard `cubic-bezier(0.2, 0, 0, 1)`; M3
  emphasized-decelerate `cubic-bezier(0.05, 0.7, 0.1, 1)`; Core Animation's
  `kCAMediaTimingFunctionDefault` / CSS `ease` is `cubic-bezier(0.25, 0.1,
  0.25, 1)` - Apple's HIG publishes principles, not bezier tokens, so any
  "Apple HIG curve" value circulating online is reverse-engineered, not
  vendor-published. Two mislabels to refuse: `(0.4, 0, 0.2, 1)` is
  Material *2*'s standard routinely pasted as "M3", and `(0.25, 0.1, 0.25,
  1)` labeled "the Apple HIG default" is the CSS `ease` curve wearing a
  vendor costume.

## 3. Springs and gesture physics

- Spring parameters below are **Framer Motion-convention coefficients**
  (stiffness + damping). Two unit traps: React Spring parameterizes as
  tension/friction, not these; and a damping *ratio* (where <1.0
  oscillates, 1.0 is critical) is a different unit again - an error that
  has reached published tables (this pack's own LottieFiles source
  conflates the two). Name which convention you are using.
- **Critical damping (no overshoot) for mass 1 is `damping = 2 *
  sqrt(stiffness)`** - stiffness 400 needs damping 40, stiffness 300
  needs ~35. The presets below are deliberately UNDERDAMPED (they
  overshoot a little), which per the settle rule places them on
  momentum-driven interactions only:

| Feel | Stiffness | Damping | Where it belongs |
|---|---|---|---|
| Snappy (mild overshoot) | ~400 | 25-30 | flick-driven UI |
| Standard (visible settle) | 250-350 | 18-24 | drag release |
| Bouncy (sparingly) | 150-250 | 10-15 | playful, earned |

- **Springs must settle.** Click-triggered UI defaults to critically
  damped (use the formula above); overshoot is earned by a flick, never
  by a click, and never appears on error paths. Prolonged wobble
  ("jello") is a defect, not personality.
- **Momentum projection** (where a flick should land): Apple ships the
  exponential-decay form `projectedDistance = (velocity / 1000) * d / (1 - d)`
  with `d ~= 0.998`, velocity in px per SECOND (the /1000 folds it onto the
  per-millisecond decay step; the dismissal rule below uses px/ms - mixing
  the two units is a 1000x error) - NOT the physics-textbook
  `v^2 / (2 * deceleration)`.
- **Rubber-band overscroll:** `(overshoot * dimension * c) / (dimension + c *
  |overshoot|)` with `c = 0.55` - resistance grows the further past the bound.
- **Velocity handoff:** when a gesture ends, the animation continues at the
  finger's velocity: `relativeVelocity = gestureVelocity / (target -
  current)` (libraries taking raw px/s can be handed the gesture velocity
  directly). Guard the zero/near-zero displacement case: when `target -
  current` is ~0 there is nothing to animate - skip the spring instead of
  dividing by it. A visible seam between drag and animation is the tell
  this rule was skipped.
- **Momentum dismissal: velocity OR distance - either alone suffices.** A
  flick dismisses on velocity above ~0.11 px/ms (~110 px/s; the source's cheap
  approximation is average `|distance| / elapsedMs`; prefer the gesture's
  actual release velocity where the framework exposes it). A slow drag
  past the distance threshold still dismisses - velocity-only would snap
  a deliberate full drag back. The failure this rule exists to prevent is
  requiring distance from a fast flick.

## 4. Choreography

- **Stagger:** 30-80ms between items; total sequence under 500ms; stagger is
  decorative - it must never block interaction while playing.
- **One thing leads.** Everything animating at once with equal weight is
  noise; pick the hero element, let the rest follow or fade.
- **Overshoot budget by context:** success 5-10%; generic feedback 2-5%;
  celebration up to 25%; **errors and destructive confirmations 0%** - play
  nothing bouncy on the worst moment of the user's session.
- **Asymmetric deliberate/response timing:** where the user is deciding
  (press-and-hold, destructive confirm) the animation may run slow; the
  system's response snaps. Symmetric timing on a press-and-release
  interaction is a finding, not a style choice.

## 5. Performance traps

- `transform` and `opacity` are the workhorses; paint-only properties
  (color, background-color, border-color) are acceptable for state
  feedback. What is BANNED is animating layout-triggering properties
  (width, height, top, left, margin, padding) - those are rewritten, not
  accepted.
- **`transition: all` is banned.**
  ❌ `transition: all 300ms ease` - it animates every property that
  happens to change, layout-affecting ones you never intended included,
  plus whichever property a future edit adds; the failure signature is
  surprise animations and layout work appearing when unrelated styles
  change.
  ✅ `transition: transform 200ms ease-out, opacity 200ms ease-out`.
- Framer Motion's shorthand props (`x`, `y`, `scale`) animate on the main
  thread via rAF rather than as compositor-run transforms (Kowalski's
  production finding; the observable symptom is dropped frames while the
  page is busy). Under load, use the full `transform` string.
- Updating an inheriting CSS variable on a parent recalculates style for
  its children - the default for unregistered custom properties (a
  registered `@property` with `inherits: false` sidesteps it) - so in a
  drawer with many items, drive `transform` on the moving element directly
  instead of `--offset` on the container.
- Animations are interruptible: new input retargets mid-flight (CSS
  transitions and springs retarget; keyframes restart from zero - wrong for
  toasts, toggles, anything triggered rapidly); no fill-mode or delay may
  block interaction.
- **Never enter from `scale(0)`** - nothing real appears from nothing; enter
  from `scale(0.9-0.97)` plus opacity.
- Set `transform-origin` for scale/rotate: popovers, dropdowns, and tooltips
  scale from their trigger, not center (modals are the exemption - they stay
  centered); SVG needs `transform-box: fill-box` on a wrapping `<g>`.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)` -
  touch devices fire false hovers on tap.

## 6. Reduced motion is a floor, not a feature

- Every animation ships a `prefers-reduced-motion` variant. Reduced means
  **fewer and gentler, not zero**: keep opacity/color transitions that aid
  comprehension; drop movement - slide+fade -> fade; scale+fade -> fade;
  spring -> short tween; parallax and auto-playing loops -> removed.
  Transform-based full-screen motion is the highest-cost vestibular
  trigger - it is exactly what this media query exists for.
- Motion is never the only signal of a state change: pair it with a static
  affordance (color, position, label) or reduced-motion users miss the
  change entirely.

## 7. Misquoted research - do not cite these wrong

These corrections are adapted from open-design's primary-literature review
(Apache-2.0; adaptation notice in THIRD-PARTY-NOTICES). The papers were
NOT re-opened for this pack - each line below is that review's checked
claim, restated, not this pack's own reading of the source:

- "Skeleton screens feel 11% faster" - per that review, Harrison/Yeo/
  Hudson (CHI 2010) measured backwards-decelerating ribbed *progress
  bars* (n=16), not skeletons; the mechanism does not transfer.
- "Doherty threshold = 400ms" - per that review, the source contains no
  400ms figure; the lowest measured threshold is 300ms. And cite the
  source itself correctly: Doherty & Thadhani, "The Economic Value of
  Rapid Response Time", IBM technical report GE20-0752 (1982) - the
  "IBM Systems Journal 1982" venue and the "Thadani" spelling circulating
  online (and in the review this pack adapted) are themselves
  miscitations, corrected here.
- "Heer & Robertson recommend 300-1000ms transitions" - per that review,
  they tested 1.25s and 2s only, and recommend roughly one second per
  animated stage.
- Motion *confirms* state changes; it must not *perform* them. Optimistic
  UI first, animation second.

## 8. Pre-ship gate

Run against the built surface, not the source: trigger each interaction and
watch it. Severity-tiered; every CRITICAL verified by observation before
"done".

- **CRITICAL:** reduced-motion variant exists and was toggled on and
  observed; nothing exceeds 500ms (unless the When-NOT spectacle
  exception was invoked in writing - the purpose test and reduced-motion
  floor still bind there); no spring fails to settle; no
  keyboard-initiated action animates; no `transition: all`.
- **HIGH:** durations inside §1 budgets; easing direction per §2; exits
  faster than entrances; layout-property animation absent.
- **MEDIUM:** stagger within budget; `transform-origin` set for scale;
  consistent timings across sibling components; overshoot within §4 context
  budget.

Done when: every CRITICAL item observed passing, HIGH items pass or carry a
written exception, and any failure names the rule it broke (not "feels off").

## When NOT to use this skill

- Debugging one library's API surface -> that library's docs; this file owns
  budgets and judgment, not APIs.
- Static layout/type/color decisions -> `ui-design-craft`.
- Running a full design review with measurement and fix loop ->
  `design-review-gate` (its motion pass applies this file's budgets).
- Marketing hero choreography on a page whose brief explicitly buys
  spectacle: §1 caps may be exceeded there, deliberately and in writing -
  the purpose test and reduced-motion floor still apply.

## Provenance

Composed 2026-07-19 for design-pack 0.1.0. Sources, all verified in their
repos at composition time: Emil Kowalski's `emilkowalski/skills` (MIT) -
duration budgets, keyboard rule, stagger numbers, Framer shorthand and CSS
variable performance traps, Apple-derived projection / rubber-band / velocity
handoff forms (his distillation of Apple WWDC material; formulas quoted from
his files); LottieFiles `motion-design-skill` (MIT) - element duration table,
distance-duration multipliers, exit ratio, stagger and overshoot budgets,
severity-tier gate shape (their damping-units conflation is corrected here,
not copied; §1's duration rows are envelope syntheses across the three
motion sources, not quotes of any single table); `referodesign/refero_skill` (MIT) - purpose triad, easing
direction table, reduced-motion mapping, `transition: all` ban. §7's
corrections and the M2/M3 mislabel are adapted from nexu-io/open-design's
`craft/animation-discipline.md` primary-source review (Apache-2.0; the
correction items keep that review's selection, figures, and framing - an
ADAPTATION carried with notice in THIRD-PARTY-NOTICES, not an ideas-only
borrow). The primary papers were not independently re-opened for this
pack, with one exception: the Doherty citation itself (report GE20-0752,
"Thadhani") is this pack's own correction of the review's miscite. greensock/gsap-skills was
surveyed and deliberately not mined: library-usage doctrine, out of scope
here. Numeric values (beziers, spring pairs, budgets) are the volatile
facts - re-verify beziers against the published Material 3 motion tokens
(m3.material.io) and, for Apple, the SwiftUI Animation API's actual values
(the HIG publishes no numeric curves); spring pairs against the Framer
Motion / Motion docs - on major vendor releases. Probe status: probe-tested 2026-07-19 on a
private over-budget motion-spec fixture (fresh weak-tier agent, n=1 per
arm, smoke grade): the bare arm caught ~3 of 7 planted violations, loosely
phrased - though it did catch the missing reduced-motion variant, recorded
honestly - while the ruled arm caught 7 of 7 with budget citations,
including the keyboard rule and the 500ms total-stagger cap the bare arm
lacked as concepts. A round-0 run was voided for a leaked in-fixture
answer key. Trail in the design-pack PR.
