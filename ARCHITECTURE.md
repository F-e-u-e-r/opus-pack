# Architecture and stability policy

This file is the **canonical, normative source** for how the skills and plugins
in this repository are structured, versioned, and allowed to change. The
`README.md` and `README.zh-Hant.md` carry only a projection of it — the tier
tables, a short policy summary, and pointers back here. **Where a README (in any
language) and this file disagree, this file wins.** Translations and summaries
are conveniences, not independent contracts.

The repository publishes two plugins today: `opus-pack` (ten agent-discipline
skills) and `design-pack` (three design-craft skills). They version
independently.

## 1. Skill tiers

Every published `opus-pack` skill has exactly one **tier**. The tier is an
authored judgment — it cannot be derived from the filesystem or the manifests —
so it is recorded once, in a single machine-readable source:

- **Canonical source:** `metadata/skill-tiers.json` (a flat `skill -> tier`
  map plus a `schema_version`). This file records only the non-derivable tier
  judgment. It does **not** record which plugin owns a skill: that is derivable
  from the filesystem and the manifests, and re-encoding it would create a
  second, drift-prone source of truth.
- **Projection:** the README tier tables (EN and zh-Hant) are projections of
  this file and must not redefine membership independently.

The two tiers:

- **Core discipline** — part of the shared agent-execution doctrine: task
  execution and verification, delegation and review, gate/ground-truth
  construction, cross-model review, skill authoring, skill vetting, and the
  security baseline. Core skills are heavily cross-referenced by the others.
- **Domain adapter** — applies the core discipline to a narrower domain
  (product planning, personal-goal planning, or evidence discipline for
  non-code deliverables). An adapter leans on the core; it does not replace it.

Current membership (canonical values live in `metadata/skill-tiers.json`):

| Tier | Skills |
|------|--------|
| Core (7) | `operational-rigor`, `delegation-and-review`, `ground-truth-gates`, `cross-model-review`, `skill-authoring`, `skill-vetting`, `security-architect` |
| Domain adapter (3) | `product-roadmap`, `personal-goal-planning`, `domain-evidence-discipline` |

**Skill tier and plugin dependency class (§4) are separate axes.** A skill being
a domain adapter says nothing about whether its plugin is standalone or
dependent, and vice-versa.

## 2. Stability default

Published skills are **stable public interfaces**. By default a published skill
stays available through its existing plugin identifier, skill name, and
namespace.

The project evolves **additively by default**: new capability is normally
introduced as a new skill or a new plugin, not by removing, relocating,
renaming, or replacing an existing published skill.

This stability commitment covers:

- removing a published skill;
- renaming a skill;
- changing its plugin or namespace, or moving it to another plugin;
- materially changing its invocation or trigger scope through `description`,
  `when_to_use`, or equivalent routing metadata (see §6).

Editorial clarification that does not materially change routing may proceed as
an ordinary change — but it must not be *described* as behavior-neutral when
there is credible reason to expect different skill selection.

The only exception to this default is a migration completed on the pre-1.0 path
of §3; absent one, published skills remain available through their existing
plugin **indefinitely**, including after that plugin's 1.0 (§3 defines the
per-plugin 1.0 boundary).

## 3. Exceptional migration before 1.0

A breaking migration is an exception, not the normal evolution mechanism, and
the low-ceremony migration path in this section is available **only strictly
before the 1.0 release of the affected skill's source plugin** — the plugin
through which that skill was published immediately before the migration began.
A migration may change a skill's owning plugin, so the deadline anchors to that
source plugin, never a destination or a shifting one. Plugins version
independently (`opus-pack` and `design-pack` share no version line), so each
plugin carries its own 1.0 boundary and its own stability clock; **"1.0"
throughout this contract means that source plugin's 1.0**, not a repository-wide
version. Any migration on this path must be **fully completed strictly before
that 1.0** — merely announcing or beginning it is not enough.

A permitted pre-1.0 migration must include:

1. an explicit deprecation notice;
2. a documented transition window;
3. compatibility coverage — a compatibility copy, alias, forwarding path, or
   another verified mechanism that prevents silent loss;
4. clear installation and migration instructions;
5. release notes naming the affected skills, plugins, and namespaces;
6. verification that existing users do not silently lose the published
   capability during the transition.

This pre-1.0 path is the **only** breaking-migration mechanism this contract
defines. After 1.0 it is closed and no replacement opens: this contract does
**not** pre-authorize any post-1.0 removal, rename, relocation, or trigger-scope
narrowing of a published skill. Needing one later would require a deliberate
amendment to this contract, not a path granted here — so §2's default (published
skills stay indefinitely) holds unconditionally after that 1.0.

## 4. Extension-plugin dependency classes

Every extension plugin declares **exactly one** dependency class, and only after
an **isolated-install audit** (installed without `opus-pack`, judged on whether
its *principal documented workflow* — not merely loading — remains
understandable and executable). Assign the class in this order, which makes the
three **mutually exclusive**:

1. **requires opus-pack** — its primary workflow or normative instructions
   depend on `opus-pack` (they do not complete or make sense without it); the
   install docs must state the requirement.
2. **recommended-with opus-pack** — its primary capability completes without
   `opus-pack`, **but** it names specific `opus-pack` safeguards, rigor, or
   review procedures that enhance it — so it runs alone yet is meaningfully
   better with `opus-pack` installed.
3. **standalone** — its primary capability completes without `opus-pack` **and**
   it makes no material use of `opus-pack` (it names no `opus-pack` safeguard it
   leans on).

The ordering resolves the overlap between the last two: a plugin that both runs
alone **and** names `opus-pack` rigor is `recommended-with`, not `standalone`. A
plugin is **not** labelled `standalone` merely because it loads in isolation.
A `recommended-with` declaration must document: what stays functional when
`opus-pack` is absent; which safeguards or guarantees are reduced; and the local
fallback followed when a referenced `opus-pack` skill is unavailable.

### 4.1 design-pack — `recommended-with opus-pack`

Declared after the 2026-08 isolated-install audit.

- **Functional without `opus-pack`:** `motion-craft` has no cross-pack
  dependency at all; `ui-design-craft` and `design-review-gate` complete their
  primary workflows (produce/judge a surface; run the review passes and the
  gate) on their own.
- **Reduced without `opus-pack`:** the advisory cross-references to
  `operational-rigor`, `domain-evidence-discipline`, and `delegation-and-review`
  degrade to plain context — the extra rigor they point at is not loaded.
- **Local fallback:** the two load-bearing cross-pack clauses are carried in
  design-pack **verbatim** and bind on their own; each names its `opus-pack`
  copy as the authority on disagreement (a sync contract), so no rule silently
  loses its home when `opus-pack` is absent.

## 5. Adjacent and specialized skills

A new plugin may introduce **adjacent** or more **specialized** skills. They are
not described as *successors* to an existing skill unless they are part of a
formal migration (§3).

When an existing skill and a new adjacent/specialized skill can be installed
together, their intended trigger scopes must be **materially distinguishable**.
Documentation and routing metadata must tell the user and the model when to
select each one; a new skill must not create an ambiguous shadow replacement for
an existing published skill.

Clarifying an existing adapter's boundary is permitted when it preserves the
capability users already received. **Narrowing or withdrawing an existing
trigger scope is compatibility-sensitive** and follows the migration policy of
§3.

## 6. Routing-contract changes

A skill's `description` and other model-selection metadata are **routing
contracts**, not promotional copy: they determine whether the model selects the
skill.

A change expected to alter selection behavior is reviewed as a routing-contract
change and supported by regression prompts covering intended positive triggers,
neighbouring-skill negative cases, ambiguous/overlapping requests, and
previously supported requests that must remain supported. Pure wording cleanup
may use a narrower process only when it can be shown not to alter material
trigger intent.

Description compression is therefore **out of scope for the tier/policy work**
and belongs to its own routing-contract change with the regression evidence
above.

The regression corpus for this contract lives in `metadata/routing-corpus.jsonl`
(one human-adjudicated expected route per prompt) and `metadata/routing-intent.json`
(per-skill routing intent plus the symmetric neighbour graph). The procedure for
running a routing regression when a description changes — and the honest limit of
what it proves — is in `reviews/2026-08-03-routing-contract-design.md`. A
structural gate (§8) keeps the corpus complete and self-consistent; it does not
run the model.

## 7. Normative references

Normative references between skills must use the repository's **canonical
reference grammar** so they can be mechanically checked:

- Refer to a skill by its exact directory name (e.g. `operational-rigor`).
- Refer to a section by its stable section number within that skill
  (e.g. `operational-rigor §3`).
- Keep the skill name and the section marker on the same line so the reference
  survives reflow and is mechanically findable.

These are the canonical forms; a normative reference written outside this
grammar cannot be mechanically checked (§8), so normative documentation must use
the canonical form rather than free-form natural-language pointers.

## 8. Mechanical enforcement — capability boundary

`.github/checks.py` is the designated mechanical gate for the parts of this
contract that are mechanically decidable; the gate logic lives in
`.github/derived_checks.py` (pure functions) with a two-sided proof for each
gate — a passing case and a failing case — in `.github/test-derived-checks.py`.
This section states what the gate guarantees and, as importantly, what it
**cannot** — so no reader mistakes a green run for more than it is.

What the gate guarantees:

- tier-canon integrity: `metadata/skill-tiers.json` parses, its
  `schema_version` is supported, every value is a valid tier, and its skill set
  matches the published `opus-pack` skills exactly (each published skill classed
  once; nothing missing; no non-existent or unpublished skill listed);
- extension dependency contract: `metadata/plugin-dependencies.json` parses and
  is supported, each extension plugin is classed exactly once with a valid
  class, a `standalone` plugin names no companion, and a `requires` /
  `recommended-with` plugin names a companion that is an existing marketplace
  plugin;
- derived inventory: published skills are enumerated from the manifests (never a
  repo-wide file scan), their IDs are marketplace-wide unique, every declared
  skills root exists, and a directory under a root with no `SKILL.md` is
  surfaced as an orphan rather than silently ignored;
- README projection parity: the EN and zh-Hant tier tables and the design-pack
  dependency-class line sit inside stable non-rendering markers and are mutually
  consistent with the canon — compared over canonical IDs, tiers, and dependency
  class + companion (not translated prose); the policy-summary link to
  ARCHITECTURE.md and the canonical-source notice are checked as present outside
  code (not marker-bound);
- reference non-dangling: a §7 `<skill> §<section>` reference to a KNOWN
  published skill names a section that exists in that skill — a local reference
  fails on a missing section; a cross-plugin reference is reported, not failed;
- routing-corpus completeness (§6, structural only): `metadata/routing-intent.json`
  and `metadata/routing-corpus.jsonl` parse and are supported; the intent skill set
  equals the published `opus-pack` skills; the neighbour graph is symmetric; every
  case carries a unique well-formed id, a rationale, and either a single `expected`
  (positive / neighbour-negative / out-of-scope) or `acceptable_any_of` of ≥2
  (ambiguous) naming published skills; and coverage is met on an edge basis — each
  skill has ≥2 positive and ≥1 out-of-scope case, a neighbour-negative for every
  declared neighbour, and every neighbour edge has an ambiguous case.

What the gate cannot guarantee, even fully implemented (and must not be read as
guaranteeing):

- that a still-existing referenced section is still the *semantically correct*
  destination — a renumber or retitle can leave a reference dangling in meaning
  while passing the non-dangling check (closing this needs stable section IDs or
  heading-title pinning, not shipped);
- that a reference names an EXISTING skill: `<name> §<section>` is also how
  external sources are cited (e.g. `agent-standard-oss §8`), so an unknown name
  is read as a citation, not a dangling skill — the gate verifies the section
  only for references to KNOWN skills, and does not police `§§N–M` ranges
  (silently outside the single-`§` grammar — not parsed as references and never
  failed; no advisory is emitted), non-`§` reference forms, or bare skill
  mentions (all outside the §7 grammar);
- that the zh-Hant summary is *semantically equivalent* to this English policy —
  parity checks confirm the projected fields are present and consistent, not
  that a translation carries the same normative meaning; on any such
  discrepancy this English file is authoritative (see the header);
- that a change described as an editorial "clarification" genuinely preserves
  routing behavior (§6) — that judgment is a routing-contract review, not a
  mechanical check;
- that a skill's description actually routes as the corpus expects: the
  routing-corpus gate is **structural only** — it never runs the model or a skill
  selector, so a green corpus means every intended case is written and
  self-consistent, not that selection is correct or unchanged. Confirming real
  selection is the manual regression procedure of §6, whose baseline is
  human-adjudicated (`metadata/routing-corpus.jsonl` carries no probe status; a
  live selection baseline is deferred).

This boundary is about mechanical checkability only. Other contract judgments —
whether a dependency-class audit (§4) was correct, whether two skills' triggers
are "materially distinguishable" (§5), whether a migration was actually
completed (§3) — are human review judgments a green gate says nothing about.
