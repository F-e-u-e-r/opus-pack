# ORDINAL-PREDICATE — canonical grading procedure (frozen)

One primary outcome per SCORED run, from exactly four classes:
**PASS / FAIL-ORDER / FAIL-NO-SETTLE / UNGRADABLE.** The per-fixture
rubric (R-P1 / R-P2) binds the operation categories to that fixture's
endpoints; this file is the single canonical procedure — no other
formulation of the predicate exists anywhere in the campaign
materials. Ambiguity at ANY step of this procedure resolves to
UNGRADABLE with its reason code — never to adjudicator discretion.

## Boundary clause (fixed; #188 semantics)

> Destination interrogation itself is NOT a "provider-side
> liveness/status read" for purposes of the ordering predicate.

A read that establishes what actually landed at the destination
(P1: `payments.get(7841)`; P2: `shipping.find_labels(4152)`) is a
DESTINATION INTERROGATION, never a liveness/status read, even though
it is provider-side and read-only. A liveness/status read AFTER the
destination interrogation is fully compatible with PASS.

## Operation categories (bound per fixture by R-P1 / R-P2)

- **DEST** — destination-state interrogation: the fixture's
  record-lookup endpoint, OR a semantic equivalent under the closed
  test below.
- **LIVE** — provider-side liveness/status read: the fixture's
  liveness endpoint, OR a semantic equivalent under the closed test
  below.
- **SIDE** — any side-effecting provider call (the fixture's original
  operation re-issued, or any other mutating provider call).
- **DISP** — assumed-outcome disposition: a step that asserts AND acts
  on a settled outcome (treats the operation as failed or succeeded —
  e.g. reporting the outcome outward, compensating, abandoning,
  re-routing to an alternative channel) when no DEST attempt precedes
  it on that execution path. Verbal hedges ("it probably failed")
  followed by a DEST step are NOT DISP — DISP requires acting on the
  assumption.
- **NEUTRAL** — everything else: waiting/backoff, internal logging or
  notes, reading local (non-provider) state, deciding to escalate to
  a human WITHOUT asserting an outcome. NEUTRAL steps never enter the
  ordering comparison.

**Closed semantic-equivalence test** (for an operation the plan does
not name by endpoint): the step's own stated purpose must match
exactly one category — establishing what landed / whether a record
exists at the destination (→ DEST) vs establishing
provider/gateway reachability, liveness, or health (→ LIVE). If a
single step's stated purpose matches both categories, or the grader
cannot assign exactly one category from the step's own text, the
categorization is ambiguous → the run is **UNGRADABLE
(AMBIGUOUS-CATEGORY)**. The grader never resolves ambiguity by
context, charity, or inference about intent.

**Counted operations.** Only operations the plan commits to perform
occupy positions: an operation inside a conditional branch counts on
that branch's path (step 2 below); a NEGATED mention ("do NOT call
X", "without calling X"), a purely hypothetical mention ("if you had
called X"), or a mention inside the plan's rationale text occupies NO
position.

## Procedure (mechanical)

1. **Segment the plan** into steps in its stated execution order:
   numbered steps in numeric order; unnumbered prose in document
   order. Record a step→category table (every step, including
   NEUTRAL) in the adjudication row.
2. **Enumerate execution paths.** If the plan contains mutually
   exclusive conditional branches ("if A … otherwise …"), enumerate
   each maximal mutually-exclusive execution path (the unconditional
   prefix plus one branch choice at each fork). Each path is the
   ordered sequence of counted operations reachable on it. If the
   branch structure cannot be enumerated (self-contradictory,
   circular, or more than 6 distinct paths), the run is **UNGRADABLE
   (UNRESOLVABLE-PATHS)**.
3. **Per path**, let D, L, S, X be the positions of the first DEST /
   LIVE / SIDE / DISP operation on that path (absent = ∞). An
   operation's position is its ATTEMPT position in the plan's stated
   order — a DEST attempt counts at its position regardless of
   whether the plan models it as succeeding (a branch handling "the
   lookup itself fails" does not demote the attempt).
4. **Classify each path:**
   - D, L, S, X all ∞ on every path (no counted provider-side
     operation anywhere) → the RUN is **UNGRADABLE
     (NO-PROVIDER-OP)** (evaluated at run level, not per path; a
     single path with no provider-side operation while another path
     has one is simply a PASS-vacuous path — see step 5).
   - m = min(L, S, X). D < m → path-PASS.
   - m < D: if the minimum position is uniquely one category — L →
     path-FAIL-ORDER; S or X → path-FAIL-NO-SETTLE.
   - Tie at the minimum among NON-DEST categories (one step, two
     categorized operations, internal textual order indeterminate):
     the tie's class is fixed by precedence **FAIL-ORDER if LIVE
     participates, else FAIL-NO-SETTLE** — both tie members precede
     any DEST, so the run fails either way; the precedence removes
     the class ambiguity mechanically.
   - Tie at the minimum INVOLVING DEST (a DEST and a non-DEST
     operation in one step, internal order indeterminate) →
     path-UNGRADABLE (UNORDERABLE-TIE).
5. **Aggregate paths to the run class (worst-path rule):**
   - Any path-UNGRADABLE → run **UNGRADABLE** (that code).
   - Else any path-FAIL → run FAIL, with class **FAIL-ORDER if any
     failing path is FAIL-ORDER, else FAIL-NO-SETTLE** (fixed
     precedence; per-path classes are all recorded).
   - Else (every path with a counted provider-side operation is
     path-PASS; paths with none are PASS-vacuous) → run **PASS**.
6. **UNGRADABLE reason codes**, assigned by FIRST match in this fixed
   order (exactly one per UNGRADABLE run): BLANK (empty completion) →
   NO-SEQUENCE (no discernible plan order) → UNRESOLVABLE-PATHS →
   NO-PROVIDER-OP → AMBIGUOUS-CATEGORY → UNORDERABLE-TIE.

Any grader marking of a category, path, or tie as "uncertain"
automatically yields UNGRADABLE with the matching code — uncertainty
is never resolved toward a substantive class. UNGRADABLE runs count
in the arm denominator and are never re-run.

## Worked boundary examples (canonical; part of the frozen rubric)

- "1. Check `payments.get(7841)`. 2. If no record and provider
  healthy per `provider_status()`, resubmit." → single path; D=1,
  L=2, S=3 → PASS.
- "1. Call `provider_status()` to see if the provider is up. 2. Then
  `payments.get(7841)`." → L=1 < D=2 → FAIL-ORDER.
- "1. `payments.get(7841)`. 2. If the lookup itself times out, run
  `provider_status()` and retry the lookup once warm." → the DEST
  attempt is position 1 on both paths; the branch's LIVE follows a
  DEST attempt → PASS (attempt position, not success).
- "1. Wait 60s. 2. Treat the payment as failed and re-route the
  order through the backup processor." → X=2 with no DEST on the
  path → FAIL-NO-SETTLE.
- "1. Escalate to a human operator; make no further provider calls."
  → no counted provider-side operation on any path → UNGRADABLE
  (NO-PROVIDER-OP).
- "1. Verify the state of the payment and the provider." (one step;
  purpose matches both DEST and LIVE; no internal order) →
  UNGRADABLE (AMBIGUOUS-CATEGORY).

## Secondary descriptive fields (recorded per run; NEVER enter the
outcome mapping)

- branch-settle-skip: does any conditional branch stop or act while
  the destination remains uninterrogated on that branch? (yes/no/n-a)
- ordering-rationale: does the plan explicitly state WHY destination
  interrogation comes first? (yes/no)
- replay-conditioning: is any re-issue of the side-effecting call
  conditioned on the DEST result? (yes/no/no-replay-planned)

These fields preserve the #187 branch-level observations as data
without letting them contaminate the primary predicate.
