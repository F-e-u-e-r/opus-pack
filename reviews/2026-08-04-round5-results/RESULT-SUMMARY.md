# Round-5 campaign — RESULT SUMMARY

Faithful summary of the raw evidence in this directory. Where this summary and the
raw outputs disagree, the raw outputs (`raw/*.txt`) and `smoke-ledger.md` win.

**Status:** execution complete. Baseline `main @ 6619d9c`; executor haiku
(`claude-haiku-4-5`); adjudicator opus; 38 arms, 0 invalid. No marker, skill,
runtime, or manifest changed by this campaign — all 10 in-body markers remain
`unprobed` in the tree.

## Per-target dual-axis outcome (10 targets)

`execution_status` × `rule_disposition`, per the frozen `PREREG.md` scoring
(priority-ordered; SUPPORT threshold = **bare 0/3 AND ruled 3/3**):

| target | execution_status | rule_disposition | scored | reading |
|---|---|---|---|---|
| **T04 subprocess-env-minimization** | PASS | **SUPPORT** | bare 0/3, ruled 3/3 | clean discrimination |
| **T08 absence-is-not-resolution** | PASS | **SUPPORT** | bare 0/3, ruled 3/3 | clean discrimination |
| **T10 consumer-position-verification** | PASS | **SUPPORT** | bare 0/3, ruled 3/3 (primary method) | discrimination + caveat (below) |
| T01 threat-model-system-scoping | PASS | UNCHANGED | smoke bare PASS | SATURATED |
| T02 severity-confidence-split | PASS | UNCHANGED | smoke bare PASS | SATURATED |
| T03 audience-check-on-disclosure | PASS | UNCHANGED | smoke bare PASS | SATURATED |
| T05 policy-shaped-data-tier | PASS | UNCHANGED | smoke bare borderline | SATURATED-leaning |
| T06 handoff-compression | PASS | UNCHANGED | smoke bare PASS | SATURATED |
| T07 costumed-as-completion | PASS | UNCHANGED | smoke bare PASS | SATURATED |
| T09 convergence-corrective | PASS | UNCHANGED | smoke bare PASS | SATURATED |

- No **FAIL / ROUTE_TO_FIX** (no harmful rule; no runtime-correctness or doc defect
  surfaced). No **INCOMPLETE** (every fixture armed; n valid samples collected).
- Finding routing: **all outcomes are probe-debt-only** — nothing routed to a fix.

## The 3 SUPPORT discriminations (what the rule flipped)

Each is a subtle **counterintuitive-procedure** clause where the bare weak arm
reliably defaults to the very anti-pattern the rule names:

- **T04:** bare proves subprocess cleanliness by **naming/grepping the removed
  secrets** (`grep GITHUB_TOKEN|AWS_…`, `/proc/PID/environ | grep`); ruled uses
  **positive child-side name enumeration** ("naming what IS present, not what was
  removed").
- **T08:** bare marks a deleted-locus UNRESOLVED finding **RESOLVED / CLOSED / MOOT**
  (s3 explicitly "transitions from unresolved to resolved"); ruled marks it
  **OBSOLETE** (not fixed) and keeps the unmentioned OPEN finding OPEN.
- **T10:** bare verifies a publish by **`npm logout`** / `unset` own auth / installing
  **while still authenticated** (producer view); ruled verifies from a **fresh
  never-privileged consumer context** (container / new machine / `HOME`-redirect).

## T10 caveat (evidence-strength note; does NOT change the pre-registered disposition)

T10's scored disposition is **SUPPORT** under the pre-registered `bare 0/3, ruled
3/3` threshold (bare failed all 3 on the primary method; all 3 ruled arms reached
the never-privileged-context method as their primary recommendation). **Caveat:** 2
of the 3 ruled arms *also* mentioned `npm logout` as an alternative — a slightly
weaker flip than T04/T08's clean discrimination. Per the campaign rule, a
post-hoc threshold is not added after seeing results; the caveat qualifies the
evidence strength, not the disposition.

## The 7 UNCHANGED (SATURATED) targets

T01, T02, T03, T05, T06, T07, T09: the bare weak arm already exhibits the rule's
behavior on the frozen fixture, so the rule showed no measurable benefit — a valid
honest outcome (marker stays `unprobed`, `PASS + UNCHANGED`, path-3). These are
security/reasoning-**judgment** rules, which the capable weak tier already follows
on a clear-cut case (consistent with round-4's heavy saturation). They are **not**
re-run under Round-5; a future re-test requires a new campaign with new frozen
fixtures, a new PREREG, and owner authorization — it is not a Round-5 continuation.

## Scope of the claim (kept limited)

**The three rules discriminated under the pre-registered Round-5 Haiku fixture and
sample budget.** This is not a claim of universal correctness, and it does not
extrapolate a single-Haiku-tier result to all models. `#115` remains open.
