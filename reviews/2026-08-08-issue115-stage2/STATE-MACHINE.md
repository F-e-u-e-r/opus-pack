# Issue-115 STAGE-2 State-Transition Table (r5)

Operational states only — never a replacement for the sealed outcome
taxonomy (PASS+SUPPORT / PASS+SATURATED / FAIL-SIGNAL / INCONCLUSIVE
remain §D's, computed from receipts). No transition converts SUSPECT,
DRIFT-SHADOWED, invalidity, or cap exhaustion into a different
epistemic outcome. Scope tags: [C]=campaign, [T]=target, [F]=fixture,
[A]=arm, [M]=marker, [S]=slot.

GLOBAL PRE-CHARGE GATE (every CHARGE-REQUIRING invocation, before it
starts): the charge's OWN pool (planned pool for original planned
slots; reserve pool for retries/re-smokes/re-entitled attempts and
for rerun-unit ENCUMBRANCES) must hold ≥ the charge, and total
consumption after it must be ≤ 110. A charge failing its gate never
executes; the TYPE-CORRECT branch fires instead: failed planned-slot
charge → row 29; failed single-slot scored retry → row 28; failed
reserve-funded DRY-RUN/SMOKE-kind retry or re-entitlement → row 28b;
failed rerun-unit encumbrance at execution position → row 23a-else /
27b-else.

ENCUMBRANCE MODEL (rerun units only): when a SUSPECT or parity unit
reaches its execution position, its FULL cost is encumbered from the
reserve pool in one atomic act (sealed first-come order — nothing is
reserved at authorization). The unit's R-slots are PRE-FUNDED: they
draw down the encumbrance one slot at a time and are EXEMPT from the
per-invocation gate and from row 14's planned −1 (an R-slot receipt
records "encumbrance-drawdown" as its budget effect). Encumbered
slots are not charge-requiring, so they can never trigger row 29;
every abort/preemption path — drift, infra, retirement, STOP, any
HOLD — releases the unit's undrawn encumbrance back to the reserve
pool. Live encumbrance counts inside the reserve bound (I7).

DRIFT PREEMPTION (global): the moment drift is detected for a target,
every pending invocation, retry, rerun, and rerun-unit slot for that
target is suppressed (not started, not charged) and row 18 governs;
drift is TERMINAL for the target's markers (I4) — no later transition,
including any rerun-unit abort path, may return a DRIFT-SHADOWED
marker to SUSPECT or to the outcome domain.

GLOBAL STATE-WRITE GUARD (evaluated before ANY transition writes a
marker state or outcome): a marker whose state is already TERMINAL —
owner-written (21/22), retirement-written (13), DRIFT-SHADOWED, or a
previously computed close outcome — is NEVER rewritten by any later
transition (13/20/27b/29/30/30b included); the later event is recorded
as an annotation on the terminal state. A SUSPECT-RERUN-PENDING marker
is never directly rewritten either: an event that would affect it
(class-3 STOP, class-1/2 STOP, HOLD, retirement, drift) first routes
through row 23c's abort semantics — the unit aborts, undrawn
encumbrance is released — and only then does the marker take its
post-abort state (SUSPECT via 23c(ii), or DRIFT-SHADOWED via 23c(i));
row 20 therefore marks a PENDING marker SUSPECT only through that
abort path, never by direct overwrite. SUSPECT establishment (row 20)
also SUSPENDS the marker's unrun ORIGINAL slots (not run, not
charged): restore resumes them, demote cancels them (NOT-RUN), a
rerun authorization replaces them with the unit — so no further
evidence for an adjudicable marker is collected while the owner
decides, and no output can inform the adjudication beyond what
existed at the STOP.

VALIDITY-EVIDENCE RULE (anti-laundering, faithful to the sealed
taxonomy): a PROTOCOL violation — wrong prompt digest, wrong model id
(each receipt records the runner-reported exact model id), wrong
manifest/version hash, or a lost raw-output artifact — is ALWAYS
INVALID-RUN, regardless of how gradable the output looks (sealed §D).
Absent any protocol violation, a run with a completion object and
nonempty output can NEVER be classified INVALID on an exit status or
error banner alone — it is graded (VALID-SCORED or UNGRADABLE) with
the anomaly recorded as telemetry. INVALID-RUN therefore requires:
no INTACT completion object — a transport/API-layer failure, where a
partial or truncated completion delivered alongside a transport error
signal counts as a lost/incomplete artifact (protocol evidence
attached) — OR a recorded protocol mismatch with its evidence
attached; only an intact completion object with nonempty output
invokes the never-INVALID-on-banner rule. An evidence-free INVALID label
is a protocol deviation (row 31).

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
| 10 | repair-gate [F] | repaired artifact passes static mini-gate (final-gate lens + owner sign) | AMENDMENT RECEIPT issued (artifact PATH + version tag fixture-vN + old hash → new hash + new bare/ruled rendered-prompt digests + owner signature + timestamp); the campaign's valid digest set is PER-PATH: an amended path's old hash is SUPERSEDED and no longer valid, each path has exactly one current hash (start anchor for unamended paths, latest amendment for amended ones) — any other hash is a protocol deviation (row 31); R-slot receipts record the fixture version they ran against, and their expected rendered-prompt digests come from the CURRENT valid version; prior runs of the fixture VOID; pre-charge gate (reserve) for the re-smoke | re-smoke in flight | repair-pass + amendment receipts | reserve −1 |
| 11 | repair-gate [F] | mini-gate fails OR owner declines | — | RETIRED [F] (artifact FROZEN-INVALID) | repair-fail receipt | none |
| 12a | re-smoke result [F] | passes checklist | — | fixture CLEARED | re-smoke-pass receipt | none |
| 12b | re-smoke result [F] | clean invocation, items 2/3 fail | — | RETIRED [F] | retirement receipt | none |
| 12c | re-smoke result [F] | item-1/harness/transport failure | retry entitlement unused; pre-charge gate (reserve); second such failure → HOLD(campaign): SMOKE-INFRA | one re-smoke rerun | smoke receipt / smoke-infra-hold | reserve −1 |
| 13 | RETIRED [F] | — (consequences per sealed §D) | single-fixture marker? | marker OUT-OF-SCOPE [M] per sealed §D; else marker INCONCLUSIVE(RETIRED-MEMBER) [M] per sealed §D (domain guard applies: a SUSPECT / SUSPECT-RERUN-PENDING / DRIFT-SHADOWED marker keeps its state, the retirement recorded as an annotation for the owner); the retired fixture's own unrun slots NOT-RUN(RETIRED-SELF); same-marker-set siblings' unrun slots NOT-RUN(RETIRED-SIBLING) (a sibling serving a different marker — T5 — untouched) | retirement-consequence receipt | cancelled slots uncharged; their planned budget FROZEN |
| 14 | RUNNING [C] | target's FIRST scored slot due | drift check (b) NOW; artifact hashes valid under current digest set; assembled prompt digest = the slot's SLOT-TABLE expected value; arm order per parity table; pre-charge gate (planned) | scored in flight | run receipt (kind SCORED, retry-role, validity, rendered-prompt sha256, raw-output sha256) | planned −1 |
| 14b | RUNNING [C] | subsequent scored slot due | as 14 minus drift check (b) | scored in flight | run receipt (same fields) | planned −1 (an R-slot instead records encumbrance-drawdown; no planned or per-invocation charge) |
| 15 | scored result [S] | INVALID-RUN per the VALIDITY-EVIDENCE RULE (no intact completion object, or any evidenced protocol mismatch) | retry entitlement unused; no drift pending; pre-charge gate (reserve) | same-slot rerun immediately | invalid-run receipt (evidence, retry-role rerun) | reserve −1 |
| 16 | scored result [S] | second INVALID-RUN in slot | — | arm INCOMPLETE [A] — recorded even when row 17 co-fires; survives any resume | arm-incomplete receipt | none |
| 17 | RUNNING [C] | ≥4 consecutive INVALID-RUN anywhere | row 16's consequence recorded first if co-triggered | HOLD(campaign): RUN-INFRA | infra-hold receipt (run list) | none |
| 18 | RUNNING [C] | drift detected for a target (any checkpoint or observation) | §A triple binding evaluated | HOLD(target) + marker(s) DRIFT-SHADOWED [M] (terminal; overrides and freezes any SUSPECT/PENDING state's outlets); all pending target work suppressed; co-occurring generic signal = telemetry | drift receipt (ref SHA, failed binding, telemetry) | remaining target slots SKIPPED, uncharged, planned budget FROZEN |
| 19 | RUNNING [C] | §0 class-1/2 interruption event | — | STOP [C] | stop receipt (class, evidence) | none |
| 20 | RUNNING [C] | §0 class-3 event (validity-threatening, non-drift) | CONSERVATIVE SCOPE RULE: default = every target with executed, non-terminal evidence in the event window (runner/config events: since the last verified-parity receipt); narrower only with receipt-backed derivation AND owner confirmation | STOP [C] + affected markers SUSPECT [M] per the GLOBAL STATE-WRITE GUARD (terminal markers annotated, never rewritten; PENDING markers via 23c abort first; SUSPECT establishment suspends the marker's unrun original slots) | stop + suspect receipts (scope derivation) | none |
| 21 | SUSPECT [M] | owner adjudicates: restore | — | marker re-enters outcome domain; §D computed over the PRESERVED prior evidence | adjudication receipt | none |
| 22 | SUSPECT [M] | owner adjudicates: demote | — | marker INCONCLUSIVE (owner act, never structural) | adjudication receipt | none |
| 23 | SUSPECT [M] | owner adjudicates: rerun — ONE-SHOT per marker: rerun-used is set NOW, at authorization, is PERMANENT regardless of the unit's later fate (abort or cap-block at position — none resets it), and the authorization itself is FINAL (no cancellation exists) | receipt check: no prior rerun authorization exists for this marker | SUSPECT-RERUN-PENDING [M]; the unit (fixtures × 2 arms × 3) is appended at the current schedule end as R-slots; prior evidence is PRESERVED until unit completion (delayed VOID — operational definition of the sealed "rerun VOIDS every prior run": the void takes effect when the replacement exists, keeping never-pooled arithmetic while preventing an evidence vacuum on abort) | adjudication receipt (rerun-used) | none — no escrow |
| 23a | SUSPECT-RERUN-PENDING [M] | the unit reaches its execution position | A rerun authorization is FINAL (sealed one-outlet adjudication) — no cancellation transition exists at any point, so no output can ever inform a reversal. Any unit fixture without a smoke-pass receipt runs its (unconsumed) planned smoke slot first and must CLEAR — a prerequisite smoke that leads to repair-retirement (rows 7→11/12b) aborts the unit via 23c(ii). Then ATOMIC ENCUMBRANCE: reserve ≥ full unit cost → encumber it now; else → marker returns to SUSPECT + CAP-EXHAUSTED annotation (restore/demote remain — rerun-used stays consumed; prior evidence intact) | unit R-slots execute under rows 14/14b semantics, pre-funded by the encumbrance | unit-start receipt (or cap-blocked-suspect receipt) | reserve encumbrance −(unit cost) or none |
| 23b | SUSPECT-RERUN-PENDING [M] | every unit slot completes with a counted run (VALID-SCORED or UNGRADABLE) | — | prior fixture-set runs VOID NOW; marker re-enters outcome domain; sealed §D computed over the REPLACEMENT unit's runs only | unit-completion + void receipts | none further |
| 23c | SUSPECT-RERUN-PENDING [M] | the unit cannot complete — causes: drift; infra (an arm INCOMPLETE inside the unit); its fixture RETIRING (incl. via the prerequisite smoke's repair path); STOP; HOLD(campaign); non-drift HOLD(target) | branch: (i) DRIFT → marker DRIFT-SHADOWED (terminal, I4 — never back to SUSPECT); (ii) ALL OTHER causes → unit ABORTED — R-slots cancelled, marker returns to SUSPECT (restore/demote only — rerun-used stays consumed; prior evidence intact). BOTH branches release the unit's undrawn encumbrance to the reserve pool | unit-abort receipt (cause, encumbrance released) | undrawn encumbrance released |
| 24 | SUSPECT [M] | owner adjudicates rerun while reserve < unit cost (advisory check at authorization) | applies ONLY when no prior rerun authorization exists for this marker (receipt-checked) — after any row-23 authorization the flag is permanent and this row is unreachable | marker stays SUSPECT + CAP-EXHAUSTED annotation (restore/demote remain); rerun-used NOT consumed (no unit was ever created) | cap-blocked-suspect receipt | none |
| 25 | HOLD(target) [T] (non-drift causes only — a drift HOLD has no in-campaign resume) | owner authorizes resume | drift re-check passes; digests valid under current set; executor config unchanged | RUNNING; resumed targets form one owner-order-sorted queue appended after the remaining planned schedule (deterministic insertion; in-flight never interrupted) | resume receipt | none |
| 26 | HOLD(campaign) [C] | owner authorizes resume (infra remedied) | full §K-4 preconditions; for PRECONDITION-FAILED / SMOKE-INFRA / RESERVE-EXHAUSTED: the owner may attach ONE re-entitlement per HOLD event — a SINGLE invocation carrying NO nested retry entitlement (rows 3/8/12c do not apply to it), BOUND to the failed prerequisite: same execution-kind, same slot, same fixture at its CURRENT valid version, same expected prompt digest, same checklist (the resume receipt records the binding; an unrelated invocation never unblocks anything); it must PASS/reach a verdict before dependent slots, and its failure returns directly to the same-subtype HOLD; a SECOND HOLD of the same subtype requires the resume receipt to carry infra-remediation evidence, else the owner's only path is campaign close | RUNNING (consecutive counter reset; pre-HOLD count recorded; INCOMPLETE arms stay INCOMPLETE) | resume + re-entitlement receipts | reserve per re-entitlement |
| 27 | STOP [C] | owner authorizes resume | full §K-4 list + class-3 SUSPECT adjudications complete | RUNNING | resume receipt | none |
| 27b | RUNNING [C] | runner-level parity difference discovered (sealed §C) | comparisons VOID; ONE-USE per fixture per parity event (receipt-guarded); the six-slot rerun is appended as R-slots; at ITS execution position the atomic ENCUMBRANCE applies: reserve ≥ 6 → encumber and run (R-slots pre-funded; any mid-unit interruption → row 27c); else → the fixture's IN-DOMAIN marker(s) INCONCLUSIVE(PARITY-VOID) per the state-write guard — a SUSPECT/PENDING/DRIFT-SHADOWED marker instead keeps its state with a PARITY-VOID annotation for the owner | parity-void receipt (+ unit-start / inconclusive / annotation receipts) | reserve −6 at execution position, or none |
| 27c | parity unit in flight | the unit cannot complete — a second INVALID-RUN in one of its R-slots, STOP, any HOLD, retirement, or drift | — | unit ABORTED: remaining R-slots cancelled, undrawn encumbrance released, the parity one-use stays consumed; the fixture's comparisons remain VOID, so its IN-DOMAIN markers → INCONCLUSIVE(PARITY-VOID) (state-write guard: terminal/SUSPECT/PENDING markers keep their states with a PARITY-VOID annotation); a drift cause additionally applies row 18 to the target | parity-abort receipt (cause, encumbrance released) | undrawn encumbrance released |
| 28 | RUNNING [C] | pre-charge gate fails for a licensed single-slot scored retry | — | arm INCOMPLETE (CAP-EXHAUSTED annotation) [A] | cap-block receipt | none |
| 28b | RUNNING [C] | pre-charge gate fails for a reserve-funded DRY-RUN/SMOKE-kind retry or re-entitlement | — | HOLD(campaign): RESERVE-EXHAUSTED (owner decides: close, or resume under row 26's constraints) | reserve-exhausted receipt | none |
| 29 | RUNNING [C] | the next CHARGE-REQUIRING slot cannot be funded (planned slot, or a reserve-funded retry with no type-correct branch left) — encumbered R-slots are NOT charge-requiring and always complete or abort via their own rows first | safety/drift triggers recorded first; no live encumbrance may remain (units finish or abort before close); drift check (d) over ALL targets (completed included) BEFORE any outcome derivation | CAP-EXHAUSTED close [C]: remaining slots NOT-RUN in order; their arms INCOMPLETE; TERMINAL DOMAIN GUARD: only markers that are in-domain AND undamaged compute ordinary sealed §D results; in-domain damaged sets → INCONCLUSIVE; terminal and adjudicable markers are never rewritten per the GLOBAL STATE-WRITE GUARD (CAP-EXHAUSTED annotations added where relevant); explicit unstarted-unit transitions, receipted: an unstarted SUSPECT unit aborts (nothing encumbered) and its marker STAYS SUSPECT with a CAP-EXHAUSTED annotation; an unstarted parity unit aborts and the fixture's in-domain markers → INCONCLUSIVE(PARITY-VOID) with a CAP annotation; drift at (d) → DRIFT-SHADOWED | cap-exhaustion receipt | terminal |
| 30 | RUNNING [C] | final schedule slot (R-slots included) completed | drift check (d) over ALL targets; ledger↔receipts reconciliation | COMPLETE [C]: sealed §D outcomes computed for not-yet-terminal in-domain markers ONLY, under the GLOBAL STATE-WRITE GUARD (owner-written, retirement-written, SUSPECT, PENDING, DRIFT-SHADOWED, and previously computed outcomes are never rewritten) | campaign-close receipt | terminal |
| 30b | COMPLETE or CAP-EXHAUSTED close [C] | marker-disposition PR opened | drift check (e-open); recommendations exist ONLY for in-domain markers with computed sealed §D outcomes — an unresolved (SUSPECT/PENDING/DRIFT-SHADOWED) or OUT-OF-SCOPE marker gets no recommendation, only its state annotation | DISPOSITION-PENDING | e-open receipt | none |
| 30c | DISPOSITION-PENDING | immediately before PR merge | drift check (e-merge) | merge proceeds for undrifted targets; a drifted target's recommendation is WITHDRAWN before merge, the target returns to HOLD(target) with its marker(s) DRIFT-SHADOWED, and the transition is receipted | e-merge receipt (withdrawals + HOLD transitions) | none |
| 31 | any [C] | ledger↔receipts divergence; an evidence-free INVALID label; any artifact hash outside the valid digest set (start anchor ⊕ amendment receipts) | — | HOLD(campaign): PROTOCOL | divergence receipt | none |

R-SLOT BINDING: appended rerun slots are numbered `R<u>.<k>` (u = the
unit's append order, k = position inside the unit, which follows §1's
interleave for its fixtures). DIGEST AUTHORITY (single, versioned):
every slot's expected rendered-prompt digest — original or R-slot —
comes from the fixture's CURRENT VALID VERSION: the start-anchor
digests (as materialized in SLOT-TABLE.md) while no amendment exists,
else the latest amendment receipt's rendered digests. SLOT-TABLE.md
and MANIFEST.json are DERIVED views of the start-anchor version;
inside a repair's amendment transaction they are regenerated once and
their new hashes are recorded IN the amendment receipt, binding the
derived metadata to the same gated transaction. The receipt records
the R-slot id, parent fixture/arm/n-index, and the fixture version it
ran against. No VOID original slot is ever reused.

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
  rerun outlet is one-shot per marker, set permanently at
  authorization (23) — 24 is reachable only with no prior
  authorization on record, so the flag can never be reset by
  cancellation, abort, or cap-block.
- I4: DRIFT-SHADOWED has no exit inside the campaign; no abort,
  resume, retirement, parity, or cap path returns it to SUSPECT or
  the outcome domain.
- I8: the GLOBAL STATE-WRITE GUARD holds at every write: terminal
  states (owner-written, retirement-written, DRIFT-SHADOWED, computed
  outcomes) are never rewritten; PENDING markers change state only
  through 23a-else/23b/23c; adjudicable markers collect no new
  original-slot evidence while suspended.
- I5: scored-slot executions beyond the planned 78 are licensed ONLY
  by rows 15 (single slot), 23a/23b (SUSPECT unit), and 27b (parity
  unit) — each pool- and position-gated; rows 3/8/10/12c/26 license
  only DRY-RUN/SMOKE-kind retries, each entitlement-bounded with
  type-correct exhaustion branches (4/9/28b).
- I6: SKIPPED / NOT-RUN(-SELF/-SIBLING) / NOT-RUN slots are never
  charged; frozen planned budget is never reallocated.
- I7: reserve consumption (live encumbrances included) never exceeds
  18, planned consumption never exceeds 92, total never exceeds 110;
  reserve charges and encumbrances occur only at execution position
  (no authorization-time reservations), preserving first-come order
  over the actually-executed deterministic schedule; undrawn
  encumbrance is released on every abort/preemption path, so no live
  encumbrance can exist at campaign close.
