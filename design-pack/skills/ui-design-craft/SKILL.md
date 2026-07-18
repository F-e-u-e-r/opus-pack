---
name: ui-design-craft
description: Static visual judgment for generated or restyled UI. Load when you are about to produce or modify any user-facing surface - a landing/marketing page, product screen, mockup, or component styling - when a brief says "make it look good/premium/modern" with no design system attached, or when you notice generated UI converging on default AI aesthetics. NOT for motion decisions (motion-craft), for running a measured design review (design-review-gate), for charts (the environment's dataviz tooling), or for native mobile idiom questions (Apple HIG / Material directly).
---

# UI Design Craft

AI-generated UI fails in a recognizable direction: it optimizes for the safe
average. The counter is not taste words - it is bans with exact signatures,
budgets with numbers, and a mechanical gate. One meta-rule governs the whole
file, learned from production tests upstream: **"use sparingly" does not
transfer to a generating model; binary phrasing and countable caps do.**

## 0. Classify the surface before generating anything

First action, before any code or mockup:

- **MARKETING** (landing, portfolio, about, pricing): all sections below
  apply, §2 layout budgets included.
- **APP UI** (dashboard, admin, dense product screens, editors, tables):
  route the visual system to an established design system (Material, Fluent,
  Carbon, Polaris, or the project's own); from this file apply only §1 bans,
  §3 discipline, §4 states, §5 floors. The §2 marketing budgets do NOT
  apply - a dashboard is allowed to be dense and repetitive.
- **HYBRID** (product site with embedded app screens): classify each section.
- Out of scope entirely - say so and route: data tables (TanStack/AG Grid),
  code editors (Monaco/CodeMirror), native mobile (HIG/Material), realtime
  collaboration surfaces.
- If the project has a governing design contract (DESIGN.md, tokens file,
  brand guide), it outranks every default in this file - verify and consume
  it per `design-review-gate` ("the design contract"); the bans below still
  apply to whatever the contract leaves open.

## 1. The ban list (AI tells, with signatures)

Hard bans by default; a ban yields only to an explicit brand fact or brief
requirement, stated in writing ("the brand IS purple" unlocks purple - the
override is the recorded reason, never silent).

**Color tells**
- Default indigo/violet accent: `#6366f1 #4f46e5 #8b5cf6 #7c3aed` and their
  Tailwind neighbors. The single most reliable AI fingerprint.
- The "premium consumer" beige+brass+espresso family applied to every
  luxury/artisan/wellness brief; same for olive/clay/terracotta earth tones
  as an unresearched default.
- Evenly distributed color with no accent hierarchy; semantic colors
  (error/success) reused decoratively.

**Typography tells**
- Fraunces or Instrument Serif as unjustified display defaults (the two
  LLM-favorite serifs); any serif repeated from your previous project.
- The decorative one-word swap: one headline word italicized, serif-ed, or
  color-shifted purely to feel "designed". Distinction comes from layout,
  scale, weight, or media - not a costume on one word.
- Em-dash in generated page copy: **zero**, everywhere on the page -
  headlines, body, captions, buttons, alt text. Upstream production tests
  found models ignore "limit em-dashes"; only the binary form holds. Use a
  hyphen or restructure. (Scope: copy on generated surfaces - not code, not
  prose documents.)
- ALL-CAPS or small labels without letter-spacing; italic descenders clipped
  by tight line-height (leading below ~1.1 with no padding).

**Container tells**
- Cards as the default grouping: if removing border+shadow+background+radius
  hurts nothing, it was never a card - use sections, columns, dividers.
- Decorative left accent stripe (`border-left: 4px solid <accent>`): stripes
  carry meaning (status, priority, selection) or they go.
- The 3-column icon-in-colored-circle feature grid, repeated symmetrically -
  the single most recognizable signature of generated marketing pages.
- "Split header" (huge left headline + small floating right paragraph) as a
  section-header default; stack vertically instead, max-width ~65ch.
- Hairline borders above AND below every row of a list or spec table.
- Standard emoji standing in for icons: use an icon set or a plain
  Unicode glyph (an arrow, a bullet, a diamond) - emoji as UI iconography
  reads as unfinished work.

**Label and meta tells**
- Eyebrow labels (small caps tracking-wide strings above headlines) above
  every section. Cap: **at most 1 eyebrow per 3 sections, hero included** -
  the check is a count, see §7.
- Section numbering (`001 · Capabilities`), version stamps in heroes or
  footers (`v0.6`, `BETA`, `Build 0048`), pagination on tiles (`01 / 4`).
- Locale/weather/time strips ("LIS 14:23 · 18°C"), scroll cues ("Scroll to
  explore"), decorative status dots, poetic section labels ("From the
  field", "Quietly trusted by"), generic step labels ("Step 1 / Step 2" -
  the verb is the label: "Install", "Configure", "Ship").
- Middle-dot separator chains ("foo · bar · baz · qux") - max one `·` per
  metadata line.

**Fake-content tells**
- Div-built fake product UI in the hero (fake terminal, fake dashboard of
  styled divs) - use a real screenshot, a real component, or nothing.
- Placeholder people ("Jane Doe", "John Smith"), invented testimonials,
  fake logos, fake metrics. Absent real content, design the empty state.
- Image-led direction collapsed to text-only because no image was handy:
  preserve the media slot with honest dimensions and an art-direction note
  instead of faking imagery with CSS blobs.

**Mode tells**
- Dark mode as an unrequested default: light is the baseline unless the
  brief says otherwise (dark is a brand decision, not a vibe).
- "Calm editorial" autopilot (cream canvas + oversized serif + airy spacing)
  on products that need utility or proof. Before using it, write down why
  THIS product earns an editorial voice; no written reason, no serif system.

## 2. Layout budgets (MARKETING surfaces)

- **Hero:** headline max 2 lines desktop; subtext max 20 words; at most 4
  text elements total (one eyebrow-or-brand-strip, headline, subtext, CTA
  row of 1 primary + max 1 secondary); CTAs visible without scrolling; top
  padding capped ~6rem. Trust logos, pricing teasers, and feature bullets
  live in sections BELOW the hero, never inside it. If the value
  proposition does not fit in 20 words, the proposition is unclear - fix
  that, not the rule.
- **Headline scale is planned with the asset:** 3-5 word headlines may take
  the largest scale; 6+ words step down one or two sizes. A hero headline
  wrapping to 4 lines is a font-size error, not a copy problem.
- **Navigation:** single line at desktop, height max 80px (default 64-72px).
  A two-line desktop nav is broken, not cozy.
- **Section rhythm:** a layout family (3-col cards, full-width quote,
  text+image split...) appears at most once per page; a page of 8 sections
  uses at least 4 distinct families; max 2 consecutive alternating
  image/text "zigzag" sections - the third consecutive is a gate failure.
- **Bento grids:** exactly as many cells as there is content (3 items = a
  1+2 or 2+1 composition, never a blank filler tile), and at least 2-3
  cells carry real visual variation (image, tinted background, pattern) -
  not six white-on-white text tiles.
- **Mobile collapse is declared per section** in the same component; "the
  framework will handle it" is not a declaration.

## 3. Type and color discipline

- Hierarchy has 3-4 distinct levels, differentiated by weight and spacing,
  not size alone.
- **Accent budget: at most 2 visible accent uses per screen.** Spend them
  deliberately - a highlighted label plus the primary action is the usual
  allocation. Links draw from the same budget; once it is spent, style
  them as underlined foreground text instead.
- One lock each per page: ONE theme (no section flipping to inverted
  mid-page), ONE accent applied identically, ONE corner-radius system.
- Contrast floors (WCAG AA): text needs 4.5:1 at normal size and 3:1 only
  at large size - placeholder text and text over images or scrims
  included, with no exemption for either; non-text UI (focus rings,
  component boundaries, state indicators) needs 3:1; secondary BODY-size
  text needs 4.5:1 in both color modes - dark-mode secondary text is
  where this fails silently.
- Micro text is whitelisted, not vibes-based: the smallest size (11px and
  below) appears only in an enumerated role list you can state (timestamps,
  badge pills, axis labels...) - any other use upgrades a size.

## 4. State coverage - the most reliable generated-UI failure

Shipping only the populated state IS the failure mode. Every surface that
fetches, accepts, or transforms data renders five states before it is done:

| State | Must contain |
|---|---|
| Loading | skeleton/spinner plus a "taking longer than expected" fallback |
| Empty | headline, plain explanation, primary CTA - designed, not blank |
| Error | plain-language cause, recovery action, user input preserved |
| Populated | the case you actually designed |
| Edge | extreme volume, long unbroken strings, missing optional fields |

Edge matrix to actually try: 10,000-row table with sort+filter; 200-char
title with no spaces; missing avatar/optional field; 0 results after a
filter; offline mid-submit. Render each and look - reading the code is not
rendering.

## 5. Platform floors (APP and touch surfaces)

- Touch targets: 44x44pt (iOS) / 48x48dp (Android) minimum - vendor floors,
  not suggestions.
- Modal scrims visibly isolate the foreground: content behind reads as
  inert, and any text sitting over the scrim still meets the §3 floors.
  Material's published scrim token (black at 32% opacity) is the vendor
  anchor to start from; heavier is a legitimate brand choice, while a
  missing or near-invisible scrim is a defect.
- Press/hover states never shift layout (no border-width or size jumps -
  swap colors/elevation instead).
- Both color modes rendered and looked at before done, with every state of
  §4 checked in each - dark mode regressions hide in secondary text and
  disabled states.

## 6. Restyling an existing surface: preservation rules

A redesign is a visual change, not a silent content or interface change.
Never modify without explicit approval: URL slugs and anchor IDs, primary
nav labels, form field names and order (autofill + analytics depend on
them), the logo/wordmark, legal and consent copy. Extract existing brand
colors FIRST - a purple brand stays purple, overriding §1's indigo ban.
Never regress accessibility already present (focus states, alt text,
keyboard paths, contrast). These names are interfaces with hidden consumers
- operational-rigor's call-site sweep applies to them, verbatim: "Interfaces
include observable output text and names." (canonical copy in
operational-rigor §3; on disagreement that file wins).

## 7. The pre-flight gate (mechanical)

Run before delivering the surface. Every box, honestly; **if a single box
cannot be honestly ticked, the surface is not done.** Counts are counted,
not estimated.

- [ ] Surface classified (§0) and, for APP UI, a design system named?
- [ ] Zero em-dashes in page copy (search the output for the character)?
- [ ] Accent count per screen <= 2, and accent is none of the §1 hexes
      (grep the stylesheet for them)?
- [ ] Eyebrow count <= ceil(sections / 3) (count uppercase-tracking labels)?
- [ ] Layout-family repetition within budget; zigzag run <= 2?
- [ ] Hero: <= 2-line headline, <= 20-word subtext, <= 4 text elements,
      CTA above the fold?
- [ ] One theme lock, one accent lock, one radius system?
- [ ] WCAG AA floors pass for text, CTAs, forms, placeholders, focus rings?
- [ ] All five §4 states rendered and looked at?
- [ ] Touch targets and scrim floors met (§5, app surfaces)?
- [ ] Restyle only: §6 preservation list untouched or approval quoted?
- [ ] No banned tell present without a written brand/brief override?

Litmus checks when a box feels arguable:
- **Card test:** remove border/shadow/background - if nothing breaks, it
  was not a card.
- **Identity test:** hide the logo - if the first viewport could belong to
  any company, the design is not done.
- **Editorial test:** swap the logo for a boutique hotel's - if the hero
  still reads plausible, you built generic calm-editorial, not this brand.

## When NOT to use this skill

- Motion decisions (durations, easing, springs) -> `motion-craft`.
- Running a measured review with a fix loop -> `design-review-gate`; its
  static pass applies this file's gate.
- Charts and data visualization -> the environment's dataviz tooling.
- Native mobile idiom -> Apple HIG / Material directly.
- Brand identity creation (naming, logo) - out of scope for this pack.

## Provenance

Composed 2026-07-19 for design-pack 0.1.0. The ban corpus and layout budgets
are curated - deliberately not imported wholesale - from three MIT sources
verified in their repos at composition time: Leonxlnx/taste-skill (layout
hard rules incl. hero/nav/zigzag/bento/eyebrow caps and their mechanical
counts, the production-test tell corpus, the em-dash binary and its
"use sparingly fails" lesson, preservation rules, the pre-flight
if-one-box-fails framing; its full §9-10 corpus remains the deeper upstream
reference), referodesign/refero_skill (indigo/cards/dark-default/calm-
editorial/emoji/stripe tells, litmus tests, media-slot preservation), and
Emil Kowalski's skills (context; his marketing directives stripped).
Ideas adopted without text from Apache-2.0 nexu-io/open-design (accent
budget number, five-state table shape and edge matrix, tiered-ban
severity), from MIT garrytan/gstack (surface classifier, icon-circle-grid
tell - independently listed by taste-skill), and from MIT
creativetimofficial/ui (micro-text whitelist technique). WCAG/HIG/Material
floors are vendor facts - re-verify on major vendor releases; hex lists and
font-fashion bans are the fastest-decaying facts here (they track model
training data - revisit each model generation). Probe status: probe-tested
2026-07-19 on a private planted-slop fixture (fresh weak-tier agent, n=1
per arm, smoke grade): the bare arm found 0 of 7 planted tells - returning
CSS-engineering nits instead - while the ruled arm found 6 of 7 with rule
citations plus budget catches beyond the plants; it missed the em-dash
tell, recorded as the arm's one gap (rule retained - one miss is not yet a
wrong rule, skill-authoring §7). A round-0 run was voided for a leaked
in-fixture answer key, caught by the expected-before-actual discrepancy
rather than the score. Trail in the design-pack PR.
