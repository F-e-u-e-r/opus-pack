# Opus Pack — research roadmap

> All items below are **PARKED** until explicitly promoted by the owner. "Now"
> means the highest-priority item to consider authorizing next; it is **not**
> execution authorization. PARK is not NEXT, and PARK is not latent authorization.

This roadmap is built on the reconciled evaluation state in
[reviews/2026-09-18-activation-eval-reconciliation.md](reviews/2026-09-18-activation-eval-reconciliation.md)
(raw run artifacts are local-only / gitignored). Current production skill content
is unchanged, and nothing here proposes changing it without a controlled experiment
that supports the change.

Frontier: the canonical routing benchmark is strong, but explicit task-surface
routing is **mixed** and autonomous activation remains **weak**. Localization is
**L3 / MIXED**: some surfaces route cleanly while others miss or select neighboring
skills. On the weak-`ground-truth-gates` T2 surface, task-side framing recovers
routing (Surface-Cue **G2/G5**) while the tested description-side expansion does not
(Description-Boundary **D2**) — so the open question is activation execution and
task-surface discrimination, and **no pack-wide description rewrite** follows.

## Now — Instrument Hardening v1

**Purpose:** produce a reliable routing / activation observation instrument before
running additional activation experiments.

The existing research already exposed **stop-compliance** weakness and
**T1b-style runaway** task execution in the current probing setup (localization:
stop-after-routing 9/21; T1b ×3 timed out at the wall). The goal is **not** to
change skill content — it is to make future activation measurement cheaper and
cleaner.

Acceptance criteria (at least):

- reliable decision → observation → stop lifecycle
- no T1b-style runaway task execution
- known-bad cases demonstrably fail
- routing / activation observability preserved
- INVALID remains INVALID
- no silent rerun / replacement / backfill
- raw provenance retained
- no skill-content change

This documentation task does **not** design or execute the instrument.

## Parallel Now — Stable Evaluation / Governance Playbook

Document only the methodology that is **already stable**:

- manifest / SHA binding
- qualification-before-score
- known-bad / two-sided proof
- INVALID preservation
- no silent backfill
- full inventory audit where load-bearing
- failed-revision provenance
- contemporaneous controls
- owner STOP / authorization gates
- PARK ≠ NEXT
- PARK ≠ latent authorization

Do **not** canonicalize the current routing / activation probe implementation.
Mark that implementation **v-next / pending instrument qualification** — it is
exactly what Instrument Hardening v1 above is meant to replace.

## Next — Activation Execution / Instrument Re-test on Proven-Routeable Surfaces

(Not "activation-runtime localization" — localization has already been performed.)

**Research question:** given surfaces already shown to route correctly under
explicit routing, does a *hardened* ordinary-execution instrument convert that
routing competence into autonomous skill activation?

Prior evidence — already scored; this is **not** a fresh attempt to rediscover
whether a generic cue helps:

- **Activation Bridge v1** (generic cue) scored → appropriate activation **6/41**
  (Pattern D: activation rose but stays low; no behavioral increment where it fires).
- **Activation Bridge v2** (mandatory routing checkpoint) scored → **6/41**. v2 shows
  **no observed activation improvement over v1**, but that comparison is **not** a
  clean contemporaneous causal contrast (v1 and v2 are separate cross-campaign
  experiments).
- Generic routing cues were **insufficient** at this tier.
- **Localization** scored → **L3 / MIXED** (skill-and-surface-specific).

Restrict any future experiment to surfaces already demonstrated routeable under
explicit routing, so that routing ambiguity and activation-execution failure are
not conflated. **PARKED.**

## Later / Conditional — Broader Holdout Effectiveness

Promote **only** if the activation-execution work indicates that skill-content /
routing-generalization remains a load-bearing bottleneck.

Potential future goal: new **preregistered** holdout surfaces, unseen during the
current tuning, to measure generalization rather than fixture optimization. Do not
execute now.

## Optional Science — Higher-n Surface-Cue Replication

Recorded as **optional only**. The existing directional result is already sufficient
for the current production decision (**do not change production skill content**).
Higher-n or stronger-tier replication should be promoted only if a concrete future
product or engineering decision requires stronger stability evidence. Do not execute
now.

## Explicitly closed / not-next

- **GTG Description-Boundary Probe v1 = COMPLETE.**
- Tested candidate description = **rejected for shipment** (description `389884bc` /
  SKILL `ec660a81`; canonical `ground-truth-gates` SKILL.md `29f2d5f9` unchanged).
- **T2 description-repair search = closed.** No post-hoc wording search — do not add
  another clause, broaden the clause, copy more T2 wording into the description, or
  run alternative descriptions until one goes green.

A future description hypothesis is not ordinary roadmap continuation. It would
require **independent motivation, new preregistration, and new owner authorization**.
