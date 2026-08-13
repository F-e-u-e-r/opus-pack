# T2 doctrine-concern adjudication (deferred concern from PR #186 §3)

REVISION 2 (post-gate): the first proposed classification
(FIXTURE-SPECIFIC-WEAKNESS on a rubric-only-strictness rationale) was HELD
by BOTH independent gate reviewers on the same correctness finding and is
WITHDRAWN. Their finding, reproduced first-hand and adopted: the frozen
words "settle what actually landed at the destination first" PERMIT — and
arguably favor — the strict-ordinal reading (settlement before any other
read, the reading owner ruling A fixed for grading); declaring the replay
to be the phrase's only contrast object was evidence overreach. Separately,
the claim that the runs "followed every substantive doctrine requirement"
was untenable: verified branch behavior (below) shows otherwise.

PROPOSED PRIMARY CLASSIFICATION (revised): **RETAIN-CONCERN-ONLY** — a real
retained signal whose next step is an OWNER SEMANTIC DETERMINATION of the
clause's intended ordering, which no behavioral probe can supply; until
that determination, neither an immediate probe nor any doctrine work can
even be specified.

Semantic guardrails: **FAIL-SIGNAL ≠ doctrine defect**; **path-3 settlement
≠ concern dismissed.** Sealed outcomes and owner ruling A are untouched.
Read-only phase: 0 behavioral invocations; no doctrine/skill/marker
mutation.

## T2-A — does the doctrine require a correct and necessary ordering?

What the frozen sentence establishes beyond dispute: with UNKNOWN commit
state after a timed-out side-effecting call, settlement must precede any
REPLAY (never blind-replay), and liveness is diagnosed with a harmless
read rather than a re-invoke. That ordering (settle-before-replay) has
plain correctness content (double-charge risk) — and every one of the six
T2S2 plans did condition its resubmit on `payments.get` evidence (item-1
6/6 PASS under the sealed grading).

What the sentence leaves genuinely open — the point both reviewers held
and this revision adopts: whether "first" ALSO orders settlement before
the preliminary liveness read. The strict-ordinal reading is a plausible,
arguably favored, reading of the frozen words; the replay-scoped reading
is also grammatically available. The adjudication therefore may NOT treat
the rubric's ordinal operationalization as strictness the doctrine text
lacks — it may be exactly what the text means. Which reading is INTENDED
is an authorial fact about the clause, resolvable only by the doctrine
owner, not by any executor experiment.

## T2-B — why was the ruled arm 0/3? (mechanism, revised)

1. Clause semantics wrong — NO: settle-before-replay is correct and
   safety-motivated; the ordinal reading, if intended, is also coherent
   (minimize the unknown-commit window; interrogate the destination
   before anything else).
2. Clause semantics reasonable but wording insufficient to convey an
   intended strict-ordinal requirement — **LIVE.**
3. Rubric operationalization stronger than the doctrine's intent —
   **LIVE.**
4. Insufficient evidence to distinguish (2) from (3) — **YES, and the
   discriminator is not a probe**: (2) and (3) differ only in what the
   clause's author intended "first" to mean. An owner semantic
   determination settles it directly; executor behavior under any
   rewording cannot.

Additional direct evidence RETAINED WITH the concern (first-hand verified
from the archived raw outputs; independently cited by both reviewers):
in ruled slots 14, 16, and 18, the plan's `provider_status()`-failure
branch stops BEFORE `payments.get(7841)` — on that branch the destination
is never settled while the commit state stays unknown; and slot 18's
failure branch records a provider "outage" with no differential (the
clause's own ladder-1 requirement for isolating a shared-path failure).
These conditional-branch behaviors are outside the sealed per-item grid
(which graded the mainline; items 1 and 3 passed 6/6, item 2 failed 6/6
under ruling A) but they independently show the clause's transfer was
incomplete on this fixture — strengthening the case for RETAINING the
concern rather than closing it as fixture-specific.

## Why RETAIN-CONCERN-ONLY rather than the other three classes

- DOCTRINE-DEFECT — NO: no reading of the frozen words has been shown to
  drive wrong behavior when followed; the highest bar is nowhere near met.
- FIXTURE-SPECIFIC-WEAKNESS — NOT ESTABLISHED: its premise (rubric
  measured more than the text carries) fails once the ordinal reading is
  admitted as a plausible meaning of the text itself; and the verified
  branch behaviors are clause-transfer facts, not fixture artifacts.
- NEEDS-NEW-PROBE — NO: the live uncertainty (intended meaning of
  "first") is an owner-intent fact; a probe cannot read authorial intent
  out of executor behavior, and no probe can be designed before the
  intended semantics are fixed.
- RETAIN-CONCERN-ONLY — YES: the signal is worth keeping (ruled 0/3 under
  the ordinal reading; settle-skipping failure branches; a no-differential
  outage call), and the only immediate next step is the owner's semantic
  determination — after which the concern routes onward (clarification /
  fixture-backlog / probe design) as a fresh owner decision.

## Evidence-strength discipline

- Directly proven by the campaign record: the sealed grids and per-item
  results (T2S1 0/3·3/3; T2S2 0/3·0/3; items 1 and 3 PASS 6/6, item 2
  FAIL 6/6 under ruling A); the quoted branch behaviors of slots 14/16/18
  (archived raw outputs, re-read first-hand for this revision).
- Inference: none load-bearing remains — this revision asserts no unique
  syntax for "first" and no faithful-compliance claim.
- Live alternatives: readings (2) and (3) above, both preserved; also
  possible tier-bound components in the branch behaviors (unprobed,
  unclaimed).
- Generalization: none — haiku tier, frozen fixtures, n=3/arm.
- Sufficient for current doctrine mutation? NO on every branch; even a
  clarification edit awaits the owner's semantic determination.

## Disposition

PRIMARY: **RETAIN-CONCERN-ONLY.** The concern's durable record stays
(path-3 settlement, PR #186), now carrying the verified branch
observations; the flagged next step is an owner semantic determination of
the clause's intended ordering ("first": replay-scoped vs strictly
ordinal). No probe, no doctrine work, and no fixture work is licensed or
scheduled by this classification.
