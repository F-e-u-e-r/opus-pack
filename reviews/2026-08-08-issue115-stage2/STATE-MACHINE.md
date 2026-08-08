# Issue-115 STAGE-2 State-Transition Table (r3)

Operational states only — never a replacement for the sealed outcome
taxonomy (PASS+SUPPORT / PASS+SATURATED / FAIL-SIGNAL / INCONCLUSIVE
remain §D's, computed from receipts). No transition converts SUSPECT,
DRIFT-SHADOWED, invalidity, or cap exhaustion into a different
epistemic outcome. Scope tags: [C]=campaign, [T]=target, [F]=fixture,
[A]=arm, [M]=marker, [S]=slot.

GLOBAL PRE-CHARGE GATE (every invocation, before it starts): the
charge's OWN pool (planned pool for original planned slots; reserve
pool for every retry/rerun/re-smoke/re-entitled attempt/rerun-unit
slot) must hold ≥ the charge, and total consumption after it must be
≤ 110. A charge failing its gate never executes; the TYPE-CORRECT
branch fires instead: failed planned-slot charge → row 29; failed
single-slot scored retry → row 28; failed reserve-funded
DRY-RUN/SMOKE-kind retry or re-entitlement → row 28b; failed
rerun-unit funding at execution position → row 23a-else / 27b-else.
Reserve funding is consumed at EXECUTION POSITION in the
deterministic schedule order (sealed first-come) — never reserved or
escrowed at authorization time.

DRIFT PREEMPTION (global): the moment drift is detected for a target,
every pending invocation, retry, rerun, and rerun-unit slot for that
target is suppressed (not started, not charged) and row 18 governs;
drift is TERMINAL for the target's markers (I4) — no later transition,
including any rerun-unit abort path, may return a DRIFT-SHADOWED
marker to SUSPECT or to the outcome domain.

VALIDITY-EVIDENCE RULE (anti-laundering): when a completion object
with nonempty output exists, neither an exit status nor an error
banner can classify the run INVALID — such a run is graded
(VALID-SCORED or UNGRADABLE) and the anomaly is recorded as
telemetry. INVALID-RUN requires the ABSENCE of a completion object
(transport/API failure) or a recorded digest mismatch
(prompt/model/manifest). An evidence-free INVALID label is a protocol
deviation (row 31).

| # | Current | Trigger | Required checks | Next | Receipt | Budget |
|---|---|---|---|---|---|---|
| 1 | READY [C] | owner authorizes execution (post-STAGE-2 sign-off) | drift check (a) all targets; artifact digests match the campaign-start anchor (the merged-PR tree) with zero amendment receipts; PREREG-v6 hash 2c7e3f21… | RUNNING [C] | campaign-start (roster, PR merge SHA, MANIFEST digest, drift results) | none |
| 2 | RUNNING [C] | slot 0 due | pre-charge gate (planned) | dry-run in flight | dry-run receipt (kind DRY-RUN, retry-role original, runner-reported identity) | planned −1 |
| 3 | dry-run result | fails (API/identity) | retry entitlement unused; pre-charge gate (reserve) | one dry-run retry | dry-run receipt (retry-role rerun) | reserve −1 |
| 4 | dry-run result | fails twice | — | HOLD(campaign): PRECONDITION-FAILED | precondition-failure receipt | none |
| 5 | RUNNING [C] | fixture's smoke slot due | fixture content hash valid under the current digest set; pre-charge gate (planned) | smoke in flight | smoke receipt (kind SMOKE, retry-role, prompt sha256) | planned −1 |
| 6 | smoke result [F] | passes checklist | — | fixture CLEARED | smoke-pass receipt | none |
| 7 | smoke result [F] | clean invocation, checklist items 2 or 3 fail (objective fixture defect) | defect class ∈ preregistered set | repair-gate [F] (max 1) | smoke-fail receipt (defect class) | none |
| 8 | smoke result [F] | checklist item 1 fails, or INVALID-RUN conditions (harness/transport — never a fixture defect) | retry entitlement unused; pre-charge gate (reserve) | one smoke rerun | smoke receipt (retry-role rerun) | reserve −1 |
| 9 | smoke result [F] | second harness/transport failure | — | HOLD(campaign): SMOKE-INFRA | smoke-infra-hold receipt | none |
| 10 | repair-gate [F] | repaired artifact passes static mini-gate (final-gate lens + owner sign) | AMENDMENT RECEIPT issued (old hash → new hash, owner-signed); the campaign's valid digest set = start anchor ⊕ all amendment receipts — a hash outside that set is a protocol deviation (row 31); prior runs of the fixture VOID; pre-charge gate (reserve) for the re-smoke | re-smoke in flight | repair-pass + amendment receipts | reserve −1 |
| 11 | repair-gate [F] | mini-gate fails OR owner declines | — | RETIRED [F] (artifact FROZEN-INVALID) | repair-fail receipt | none |
| 12a | re-smoke result [F] | passes checklist | — | fixture CLEARED | re-smoke-pass receipt | none |
| 12b | re-smoke result [F] | clean invocation, items 2/3 fail | — | RETIRED [F] | retirement receipt | none |
| 12c | re-smoke result [F] | item-1/harness/transport failure | retry entitlement unused; pre-charge gate (reserve); second such failure → HOLD(campaign): SMOKE-INFRA | one re-smoke rerun | smoke receipt / smoke-infra-hold | reserve −1 |
| 13 | RETIRED [F] | — (consequences per sealed §D) | single-fixture marker? | marker OUT-OF-SCOPE [M] per sealed §D; else marker INCONCLUSIVE(RETIRED-MEMBER) [M] per sealed §D (domain guard applies: a SUSPECT / SUSPECT-RERUN-PENDING / DRIFT-SHADOWED marker keeps its state, the retirement recorded as an annotation for the owner); the retired fixture's own unrun slots NOT-RUN(RETIRED-SELF); same-marker-set siblings' unrun slots NOT-RUN(RETIRED-SIBLING) (a sibling serving a different marker — T5 — untouched) | retirement-consequence receipt | cancelled slots uncharged; their planned budget FROZEN |
| 14 | RUNNING [C] | target's FIRST scored slot due | drift check (b) NOW; artifact hashes valid under current digest set; assembled prompt digest = the slot's SLOT-TABLE expected value; arm order per parity table; pre-charge gate (planned) | scored in flight | run receipt (kind SCORED, retry-role, validity, rendered-prompt sha256, raw-output sha256) | planned −1 |
| 14b | RUNNING [C] | subsequent scored slot due | as 14 minus drift check (b) | scored in flight | run receipt (same fields) | planned −1 |
| 15 | scored result [S] | INVALID-RUN per the VALIDITY-EVIDENCE RULE (no completion object, or digest mismatch — evidence attached) | retry entitlement unused; no drift pending; pre-charge gate (reserve) | same-slot rerun immediately | invalid-run receipt (evidence, retry-role rerun) | reserve −1 |
| 16 | scored result [S] | second INVALID-RUN in slot | — | arm INCOMPLETE [A] — recorded even when row 17 co-fires; survives any resume | arm-incomplete receipt | none |
| 17 | RUNNING [C] | ≥4 consecutive INVALID-RUN anywhere | row 16's consequence recorded first if co-triggered | HOLD(campaign): RUN-INFRA | infra-hold receipt (run list) | none |
| 18 | RUNNING [C] | drift detected for a target (any checkpoint or observation) | §A triple binding evaluated | HOLD(target) + marker(s) DRIFT-SHADOWED [M] (terminal; overrides and freezes any SUSPECT/PENDING state's outlets); all pending target work suppressed; co-occurring generic signal = telemetry | drift receipt (ref SHA, failed binding, telemetry) | remaining target slots SKIPPED, uncharged, planned budget FROZEN |
| 19 | RUNNING [C] | §0 class-1/2 interruption event | — | STOP [C] | stop receipt (class, evidence) | none |
| 20 | RUNNING [C] | §0 class-3 event (validity-threatening, non-drift) | CONSERVATIVE SCOPE RULE: default = every target with executed, non-terminal evidence in the event window (runner/config events: since the last verified-parity receipt); narrower only with receipt-backed derivation AND owner confirmation | STOP [C] + affected markers SUSPECT [M] | stop + suspect receipts (scope derivation) | none |
| 21 | SUSPECT [M] | owner adjudicates: restore | — | marker re-enters outcome domain; §D computed over the PRESERVED prior evidence | adjudication receipt | none |
| 22 | SUSPECT [M] | owner adjudicates: demote | — | marker INCONCLUSIVE (owner act, never structural) | adjudication receipt | none |
| 23 | SUSPECT [M] | owner adjudicates: rerun — ONE-SHOT per marker (rerun-used consumed NOW, at authorization) | — | SUSPECT-RERUN-PENDING [M]; the unit (fixtures × 2 arms × 3) is appended at the current schedule end as R-slots; prior evidence is PRESERVED until unit completion (delayed VOID — operational definition of the sealed "rerun VOIDS every prior run": the void takes effect when the replacement exists, keeping never-pooled arithmetic while preventing an evidence vacuum on abort) | adjudication receipt (rerun-used) | none — no escrow |
| 23a | SUSPECT-RERUN-PENDING [M] | the unit reaches its execution position | any unit fixture without a smoke-pass receipt runs its (unconsumed) planned smoke slot first and must CLEAR; then ATOMIC funding gate: reserve ≥ full unit cost → charge the whole unit now; else → marker returns to SUSPECT + CAP-EXHAUSTED annotation (restore/demote remain, prior evidence intact) | unit slots execute under rows 14/14b semantics as R-slots | unit-start receipt (or cap-blocked-suspect receipt) | reserve −(unit cost) or none |
| 23b | SUSPECT-RERUN-PENDING [M] | every unit slot completes with a counted run (VALID-SCORED or UNGRADABLE) | — | prior fixture-set runs VOID NOW; marker re-enters outcome domain; sealed §D computed over the REPLACEMENT unit's runs only | unit-completion + void receipts | none further |
| 23c | SUSPECT-RERUN-PENDING [M] | the unit cannot complete | branch by cause: (i) DRIFT → marker DRIFT-SHADOWED (terminal, I4 — never back to SUSPECT); (ii) infra (an arm INCOMPLETE inside the unit, or campaign HOLD) → unit ABORTED: unexecuted slots uncharged, charged-but-unexecuted funding released to reserve, marker returns to SUSPECT (restore/demote only — rerun consumed; prior evidence intact) | unit-abort receipt (cause, funds released) | per branch |
| 23d | SUSPECT-RERUN-PENDING [M] | owner cancels BEFORE the unit's first slot starts (a post-start cancellation does not exist — outputs can never inform a cancellation) | — | marker returns to SUSPECT (restore/demote only — rerun consumed) | cancellation receipt | none (nothing charged) |
| 24 | SUSPECT [M] | owner adjudicates rerun while reserve < unit cost (advisory check at authorization) | — | marker stays SUSPECT + CAP-EXHAUSTED annotation (restore/demote remain); rerun-used NOT consumed (the unit was never created) | cap-blocked-suspect receipt | none |
| 25 | HOLD(target) [T] (non-drift causes only — a drift HOLD has no in-campaign resume) | owner authorizes resume | drift re-check passes; digests valid under current set; executor config unchanged | RUNNING; resumed targets form one owner-order-sorted queue appended after the remaining planned schedule (deterministic insertion; in-flight never interrupted) | resume receipt | none |
| 26 | HOLD(campaign) [C] | owner authorizes resume (infra remedied) | full §K-4 preconditions; for PRECONDITION-FAILED / SMOKE-INFRA / RESERVE-EXHAUSTED: the owner may attach ONE re-entitlement per HOLD event (reserve-funded; the attempt must PASS/reach a verdict before dependent slots); a SECOND HOLD of the same subtype requires the resume receipt to carry infra-remediation evidence, else the owner's only path is campaign close | RUNNING (consecutive counter reset; pre-HOLD count recorded; INCOMPLETE arms stay INCOMPLETE) | resume + re-entitlement receipts | reserve per re-entitlement |
| 27 | STOP [C] | owner authorizes resume | full §K-4 list + class-3 SUSPECT adjudications complete | RUNNING | resume receipt | none |
| 27b | RUNNING [C] | runner-level parity difference discovered (sealed §C) | comparisons VOID; ONE-USE per fixture per parity event (receipt-guarded); the six-slot rerun is appended as R-slots; at ITS execution position the atomic funding gate applies: reserve ≥ 6 → charge and run; else → the fixture's IN-DOMAIN marker(s) INCONCLUSIVE(PARITY-VOID) — a SUSPECT/PENDING/DRIFT-SHADOWED marker instead keeps its state with a PARITY-VOID annotation for the owner | parity-void receipt (+ unit-start / inconclusive / annotation receipts) | reserve −6 at execution position, or none |
| 28 | RUNNING [C] | pre-charge gate fails for a licensed single-slot scored retry | — | arm INCOMPLETE (CAP-EXHAUSTED annotation) [A] | cap-block receipt | none |
| 28b | RUNNING [C] | pre-charge gate fails for a reserve-funded DRY-RUN/SMOKE-kind retry or re-entitlement | — | HOLD(campaign): RESERVE-EXHAUSTED (owner decides: close, or resume under row 26's constraints) | reserve-exhausted receipt | none |
| 29 | RUNNING [C] | pre-charge gate fails for the next PLANNED slot, or total consumption reaches 110 | safety/drift triggers recorded first; drift check (d) over ALL targets (completed included) BEFORE any outcome derivation | CAP-EXHAUSTED close [C]: remaining slots NOT-RUN in order; their arms INCOMPLETE; markers with damaged sets → INCONCLUSIVE (domain guard applies — SUSPECT/PENDING keep their states with CAP-EXHAUSTED annotations; a PENDING unit that never started leaves its marker SUSPECT per 23a-else); markers with COMPLETE clean sets → ordinary sealed §D results; drift at (d) → DRIFT-SHADOWED | cap-exhaustion receipt | terminal |
| 30 | RUNNING [C] | final schedule slot (R-slots included) completed | drift check (d) over ALL targets; ledger↔receipts reconciliation | COMPLETE [C]: sealed §D outcomes computed | campaign-close receipt | terminal |
| 30b | COMPLETE or CAP-EXHAUSTED close [C] | marker-disposition PR opened | drift check (e-open) | DISPOSITION-PENDING | e-open receipt | none |
| 30c | DISPOSITION-PENDING | immediately before PR merge | drift check (e-merge) | merge proceeds for undrifted targets; a drifted target's recommendation WITHDRAWN before merge, recorded DRIFT-SHADOWED | e-merge receipt (withdrawals) | none |
| 31 | any [C] | ledger↔receipts divergence; an evidence-free INVALID label; any artifact hash outside the valid digest set (start anchor ⊕ amendment receipts) | — | HOLD(campaign): PROTOCOL | divergence receipt | none |

R-SLOT BINDING: appended rerun slots are numbered `R<u>.<k>` (u = the
unit's append order, k = position inside the unit, which follows §1's
interleave for its fixtures). Each R-slot's expected rendered-prompt
digest EQUALS its fixture×arm digest from SLOT-TABLE.md (the prompt
bytes are unchanged); the receipt records the R-slot id plus the
parent fixture/arm/n-index. No VOID original slot is ever reused.

Invariants (mechanically checkable):
- I1: outcome classes are written ONLY by owner acts (21/22), sealed
  §D retirement consequences (13), the parity-void else-branch for
  in-domain markers (27b), and close-time sealed §D arithmetic
  (23b/29/30) — nowhere else.
- I2: every budget-consuming transition emits a receipt carrying
  execution-kind, retry-role, and (for SCORED) validity, plus
  rendered-prompt and raw-output digests where row 14's fields apply.
- I3: SUSPECT exits only via owner adjudication (21/22/23/24);
  SUSPECT-RERUN-PENDING exits only via 23a-else/23b/23c/23d; the
  rerun outlet is one-shot per marker, consumed at authorization
  (23) — except 24, where no unit was created.
- I4: DRIFT-SHADOWED has no exit inside the campaign; no abort,
  resume, retirement, parity, or cap path returns it to SUSPECT or
  the outcome domain.
- I5: scored-slot executions beyond the planned 78 are licensed ONLY
  by rows 15 (single slot), 23a/23b (SUSPECT unit), and 27b (parity
  unit) — each pool- and position-gated; rows 3/8/10/12c/26 license
  only DRY-RUN/SMOKE-kind retries, each entitlement-bounded with
  type-correct exhaustion branches (4/9/28b).
- I6: SKIPPED / NOT-RUN(-SELF/-SIBLING) / NOT-RUN slots are never
  charged; frozen planned budget is never reallocated.
- I7: reserve consumption never exceeds 18, planned consumption never
  exceeds 92, total never exceeds 110; reserve is charged only at
  execution position (no standing reservations), so first-come order
  over the actually-executed deterministic schedule is preserved.
