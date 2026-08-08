# Issue-115 STAGE-2 State-Transition Table

Operational states only — never a replacement for the sealed outcome
taxonomy (PASS+SUPPORT / PASS+SATURATED / FAIL-SIGNAL / INCONCLUSIVE
remain §D's, computed at close from receipts). No transition converts
SUSPECT, DRIFT-SHADOWED, invalidity, or cap exhaustion into a
different epistemic outcome. Scope tags: [C]=campaign, [T]=target,
[F]=fixture, [A]=arm, [M]=marker, [S]=slot.

Format: current state | trigger | required checks | next state |
receipt emitted | budget effect.

| # | Current | Trigger | Required checks | Next | Receipt | Budget |
|---|---|---|---|---|---|---|
| 1 | READY [C] | owner authorizes execution (post-STAGE-2 sign-off) | drift check (a) all targets; MANIFEST re-hash; PREREG-v6 hash | RUNNING [C] | campaign-start (roster, hashes, drift results) | none |
| 2 | RUNNING [C] | slot 0 due | executor config matches plan | RUNNING (dry-run in flight) | dry-run receipt (identity from runner report) | −1 |
| 3 | RUNNING [C] | dry-run fails (API/identity) | retry entitlement unused | RUNNING (one retry) | dry-run-retry receipt | −1 |
| 4 | RUNNING [C] | dry-run fails twice | — | HOLD(campaign) | precondition-failure receipt | none |
| 5 | RUNNING [C] | fixture's smoke slot due | fixture hash matches MANIFEST; drift check (b) if first slot of target | RUNNING (smoke in flight) | smoke receipt (execution-kind SMOKE, retry-role) | −1 |
| 6 | smoke result [F] | passes gradability/viability checklist | checklist items all judgeable-pass | fixture CLEARED for scored slots | smoke-pass receipt | none |
| 7 | smoke result [F] | fails checklist (objective fixture defect) | defect class ∈ preregistered set | repair-gate [F] (max 1) | smoke-fail receipt (defect class) | none |
| 8 | smoke result [F] | infra failure (INVALID-RUN conditions on a smoke) | retry entitlement unused | RUNNING (one smoke rerun) | smoke-infra receipt | −1 |
| 9 | smoke result [F] | second infra failure | — | HOLD(campaign) | smoke-infra-hold receipt | none |
| 10 | repair-gate [F] | repaired artifact passes static mini-gate (final-gate lens + owner sign) | new hash versioned into MANIFEST; prior runs of fixture VOID | RUNNING (re-smoke due) | repair-pass receipt (old/new hashes) | re-smoke −1 |
| 11 | repair-gate [F] | mini-gate fails OR owner declines | — | RETIRED [F] (FROZEN-INVALID artifact) | repair-fail receipt | none |
| 12 | re-smoke result [F] | fails again | — | RETIRED [F] | retirement receipt | none |
| 13 | RETIRED [F] | — (consequences) | single-fixture marker? | marker OUT-OF-SCOPE [M]; else marker INCONCLUSIVE(RETIRED-MEMBER) [M]; own+sibling unrun slots RETIRED-CANCELLED [S] | retirement-consequence receipt | cancelled slots uncharged |
| 14 | RUNNING [C] | scored slot due | wrapper/fixture hashes match; arm order per parity table | RUNNING (scored in flight) | run receipt (3 fields: execution-kind/retry-role/validity) | −1 |
| 15 | scored result [S] | INVALID-RUN (protocol/transport) | retry entitlement unused for slot | RUNNING (same-slot rerun immediately) | invalid-run receipt (reason) | −1 |
| 16 | scored result [S] | second INVALID-RUN in slot | — | arm INCOMPLETE [A] (annotated) | arm-incomplete receipt | none |
| 17 | RUNNING [C] | ≥4 consecutive INVALID-RUN anywhere | — | HOLD(campaign) | infra-hold receipt (run list) | none |
| 18 | RUNNING [C] | drift detected (check b/c/d/e or any observation) for a target | §A triple binding evaluated | HOLD(target) + marker(s) DRIFT-SHADOWED [M]; co-occurring generic signal recorded as telemetry only | drift receipt (ref SHA, failed binding, telemetry note) | remaining target slots SKIPPED, uncharged |
| 19 | RUNNING [C] | §0 class-1/2 interruption event | — | STOP [C] | stop receipt (class, evidence) | none |
| 20 | RUNNING [C] | §0 class-3 event (validity-threatening, non-drift) | affected-target set identified | STOP [C] + affected markers SUSPECT [M] | stop receipt + suspect receipts | none |
| 21 | SUSPECT [M] | owner adjudicates: restore | — | marker re-enters outcome domain (in-domain) | adjudication receipt | none |
| 22 | SUSPECT [M] | owner adjudicates: demote | — | marker INCONCLUSIVE (by owner act, never structural) | adjudication receipt | none |
| 23 | SUSPECT [M] | owner adjudicates: rerun | remaining budget ≥ full unit cost | prior set runs VOID; rerun unit appended to schedule | adjudication + void receipts | unit cost on execution |
| 24 | SUSPECT [M] | owner adjudicates: rerun, budget < unit cost | — | marker stays SUSPECT + CAP-EXHAUSTED annotation (owner outlets: restore/demote remain) | cap-blocked-suspect receipt | none |
| 25 | HOLD(target) [T] | owner authorizes resume | drift re-check passes; MANIFEST re-hash; executor config unchanged | RUNNING (slots appended at schedule end, original owner order among resumed targets) | resume receipt | none |
| 26 | HOLD(campaign) [C] | owner authorizes resume (infra remedied) | full §K-4 precondition list | RUNNING (counter reset, pre-HOLD count recorded) | resume receipt | none |
| 27 | STOP [C] | owner authorizes resume | full §K-4 list + class-3 SUSPECT adjudications complete | RUNNING | resume receipt | none |
| 28 | RUNNING [C] | remaining budget < next licensed unit (single-slot rerun) | — | arm INCOMPLETE (CAP-EXHAUSTED annotation) [A] | cap-block receipt | none |
| 29 | RUNNING [C] | invocation 110 consumed OR remaining slots unfundable | safety/drift triggers recorded first | CAP-EXHAUSTED close [C]: remaining slots NOT-RUN in order, arms INCOMPLETE, in-domain markers INCONCLUSIVE | cap-exhaustion receipt | terminal |
| 30 | RUNNING [C] | final schedule slot completed | drift check (d) all targets; ledger↔receipts reconciliation | COMPLETE [C] (outcome computation per sealed §D; then disposition PR path w/ check e) | campaign-close receipt | terminal |
| 31 | any [C] | ledger↔receipts divergence detected | — | HOLD(campaign) (protocol deviation) | divergence receipt | none |

Invariants (mechanically checkable):
- I1: no transition writes an outcome class except 21/22 (owner acts)
  and 29/30 (sealed §D arithmetic at close).
- I2: every budget-consuming transition (−1 / unit cost) emits a
  receipt carrying the three receipt fields where execution-kind =
  SCORED, or the SMOKE/DRY-RUN kind otherwise.
- I3: SUSPECT exits only via owner adjudication (21/22/23/24) — no
  structural exit exists.
- I4: DRIFT-SHADOWED has no exit transition inside the campaign.
- I5: rows 15/23 are the only rerun-licensing rows; both are
  atomicity-guarded (15 by single-slot entitlement, 23 by full-unit
  funding).
- I6: SKIPPED / RETIRED-CANCELLED / NOT-RUN slots are never charged.
