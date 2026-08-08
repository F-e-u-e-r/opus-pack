# Issue-115 STAGE-2 State-Transition Table (v6 — structural simplification)

Operational states only — never a replacement for the sealed outcome
taxonomy (PASS+SUPPORT / PASS+SATURATED / FAIL-SIGNAL / INCONCLUSIVE
remain §D's, computed from receipts). No transition converts SUSPECT,
DRIFT-SHADOWED, invalidity, or cap exhaustion into a different
epistemic outcome. Scope tags: [C]=campaign, [T]=target, [F]=fixture,
[A]=arm, [M]=marker, [S]=slot. Rows 10/11, 23a–23c, 24, and 27c of
the r5 table are DELETED by this revision (their numbers are retired,
not reused): the SUSPECT-rerun, parity-rerun, and amendment autonomous
lifecycles they mechanized are replaced by the owner-mediated paths
below.

OPERATIONAL PRINCIPLE (owner-ruled, binding on this whole package):
rare exception paths that change evidence eligibility, rerun
entitlement, or artifact identity are fail-closed to owner
adjudication rather than autonomously repaired by the campaign state
machine. Concretely: a SUSPECT rerun, a runner-parity rerun, and any
artifact amendment are not machine transitions — each is an event →
HOLD + receipts → explicit owner adjudication record. The machine
derives no entitlement, schedules no replacement evidence, and
repairs no artifact on its own; it executes owner records and
otherwise freezes.

GLOBAL PRE-CHARGE GATE (every charge-requiring invocation, before it
starts): the charge's OWN pool (planned pool for original planned
slots; reserve pool for retries, re-smokes, re-entitlements, and the
slots of an owner-authorized rerun unit) must hold ≥ the charge, and
total consumption after it must be ≤ 110. A charge failing its gate
never executes; the TYPE-CORRECT branch fires instead: failed
planned-slot charge → row 29; failed single-slot scored retry →
row 28; failed reserve-funded DRY-RUN/SMOKE-kind retry or
re-entitlement → row 28b. An owner-authorized rerun unit is
additionally gated by sealed ATOMICITY (§E: no partial rerun): at the
unit's execution position the reserve must fund its FULL remaining
cost, else the unit does not start at all and the cap-blocked branch
of row 23 (SUSPECT) or row 27b (parity) governs.

GLOBAL FREEZE RULE: the moment any STOP or HOLD(campaign) takes
effect, every not-yet-started invocation — planned slots, licensed
retries, re-entitlements, owner-authorized unit slots — is frozen
(not dispatched, not charged). An invocation already in flight runs
to completion; its receipt is recorded with a post-event flag and
classified under the VALIDITY-EVIDENCE RULE unchanged. The evidence
available to a SUSPECT adjudication is what existed at the STOP:
post-event receipts are recorded but never presented as adjudication
evidence. HOLD(target) freezes the same way, scoped to that target.

DRIFT PREEMPTION (global): the moment drift is detected for a target,
every pending invocation, retry, and owner-authorized unit slot for
that target is suppressed (not started, not charged) and row 18
governs; drift is TERMINAL for the target's markers (I4) — no later
transition and no owner-record execution may return a DRIFT-SHADOWED
marker to SUSPECT or to the outcome domain.

TERMINAL-WRITE GUARD (evaluated before ANY transition writes a marker
state or outcome): the following are never rewritten by any machine
transition — owner-demoted INCONCLUSIVE (22), retirement-written
consequences (13), DRIFT-SHADOWED, and a close outcome whose final
drift checks have passed. SEALED PRECEDENCE EXCEPTION (§A/§D: drift
invalidates evidence at ANY checkpoint, regardless of campaign
phase): a close outcome computed at rows 29/30 is PROVISIONAL until
the disposition checkpoints pass — drift found at checkpoint (d) or
(e) rewrites the affected provisional outcome to DRIFT-SHADOWED and
withdraws its recommendation (rows 29/30/30b/30c); nothing else
rewrites a computed outcome. A restore (21) is NOT a terminal write:
it returns the marker to the in-domain, not-yet-final state. SUSPECT
establishment (row 20) SUSPENDS the marker's unrun original slots
(not run, not charged) until the owner's adjudication disposes of
them — restore resumes them, demote cancels them (NOT-RUN), a rerun
authorization replaces them with the unit — so no further
original-slot evidence accrues to an adjudicable marker while the
owner decides, and no output can inform the adjudication beyond what
existed at the STOP.

VALIDITY-EVIDENCE RULE (anti-laundering, faithful to the sealed
taxonomy): a PROTOCOL violation — wrong prompt digest, wrong model id
(each receipt records the runner-reported exact model id), wrong
manifest hash for the approved package version, or a lost raw-output
artifact — is ALWAYS INVALID-RUN, regardless of how gradable the
output looks (sealed §D). Absent any protocol violation, a run with
an INTACT completion object and nonempty output can NEVER be
classified INVALID on an exit status or error banner alone — it is
graded (VALID-SCORED or UNGRADABLE) with the anomaly recorded as
telemetry. INTACT is operationally defined by the receipt's
completion-status field: the runner-native terminal evidence recorded
verbatim for every invocation — the completion object's finish/stop
state when one was delivered, else the API error body, exit status,
or specific hash mismatch. A completion accompanied by a
transport-error signal, or delivered partial/truncated, is NOT intact
(a lost/incomplete artifact; the completion-status field carries that
transport evidence). INVALID-RUN therefore requires: a
completion-status field showing no intact completion object — OR a
recorded protocol mismatch with its evidence attached. An
evidence-free INVALID label is a protocol deviation (row 31), so an
unfavorable-looking output can never be laundered into a rerun.

| # | Current | Trigger | Required checks | Next | Receipt | Budget |
|---|---|---|---|---|---|---|
| 1 | READY [C] | owner authorizes execution (post-STAGE-2 sign-off) | drift check (a) all targets; artifact digests match the approved package version's MANIFEST; OWNER-APPROVAL record binds that exact MANIFEST.sha256; PREREG-v6 hash 2c7e3f21… | RUNNING [C] | campaign-start (roster, PR merge SHA, package id, MANIFEST digest, drift results) | none |
| 2 | RUNNING [C] | slot 0 due | pre-charge gate (planned) | dry-run in flight | dry-run receipt (kind DRY-RUN, retry-role original, runner-reported identity, completion-status) | planned −1 |
| 3 | dry-run result | fails (API/identity) | retry entitlement unused; pre-charge gate (reserve) | one dry-run retry | dry-run receipt (retry-role rerun) | reserve −1 |
| 4 | dry-run result | fails twice | — | HOLD(campaign): PRECONDITION-FAILED | precondition-failure receipt | none |
| 5 | RUNNING [C] | fixture's smoke slot due | fixture content hash matches the approved package's MANIFEST; pre-charge gate (planned) | smoke in flight | smoke receipt (kind SMOKE, retry-role, prompt sha256, completion-status) | planned −1 |
| 6 | smoke result [F] | passes checklist | — | fixture CLEARED | smoke-pass receipt | none |
| 7 | smoke result [F] | clean invocation, checklist items 2 or 3 fail (objective fixture defect) | defect class ∈ preregistered set (sealed §E: unparseable / internally contradictory / structurally unjudgeable) | HOLD(campaign): FIXTURE-DEFECT — no autonomous repair path exists; owner adjudication per row 7b | fixture-defect receipt (defect class, smoke evidence) | none |
| 7b | HOLD(campaign): FIXTURE-DEFECT | owner adjudication record arrives | exactly one outlet per record: (a) RETIRE the fixture → row 13 (artifact FROZEN-INVALID, never executed again); (b) AMEND via an amendment packet under RUNBOOK §3's package version model — sealed mini-STAGE-2 gate (final-gate lens re-review + owner sign-off) BEFORE any re-smoke; max ONE repair per fixture (sealed §E; a defect in an already-amended fixture leaves outlets (a)/(c) only); approval creates a NEW package version and VOIDS every prior run of the amended fixture; resume needs owner authorization with §K-4 preconditions checked against the NEW version, and the fixture's re-smoke (row 12 family, reserve-funded) precedes everything dependent on it; (c) CLOSE the campaign | adjudication receipt (+ packet and new-version identifiers under (b)) | none here; re-smoke reserve −1 |
| 12a | re-smoke result [F] (post-amendment) | passes checklist | — | fixture CLEARED | re-smoke-pass receipt | none |
| 12b | re-smoke result [F] | clean invocation, items 2/3 fail | — | RETIRED [F] (sealed automatic retirement — the single repair is consumed; no discretion) | retirement receipt | none |
| 12c | re-smoke result [F] | item-1/harness/transport failure | retry entitlement unused; pre-charge gate (reserve); second such failure → HOLD(campaign): SMOKE-INFRA | one re-smoke rerun | smoke receipt / smoke-infra-hold | reserve −1 |
| 8 | smoke result [F] | checklist item 1 fails, or INVALID-RUN conditions (harness/transport — never a fixture defect) | retry entitlement unused; pre-charge gate (reserve) | one smoke rerun | smoke receipt (retry-role rerun) | reserve −1 |
| 9 | smoke result [F] | second harness/transport failure | — | HOLD(campaign): SMOKE-INFRA | smoke-infra-hold receipt | none |
| 13 | RETIRED [F] | — (consequences per sealed §D) | single-fixture marker? | marker OUT-OF-SCOPE [M] per sealed §D; else marker INCONCLUSIVE(RETIRED-MEMBER) [M] per sealed §D (TERMINAL-WRITE GUARD applies: a SUSPECT or DRIFT-SHADOWED marker keeps its state, the retirement recorded as an annotation for the owner); the retired fixture's own unrun slots NOT-RUN(RETIRED-SELF); same-marker-set siblings' unrun slots NOT-RUN(RETIRED-SIBLING) (a sibling serving a different marker — T5 — untouched) | retirement-consequence receipt | cancelled slots uncharged; their planned budget FROZEN |
| 14 | RUNNING [C] | target's FIRST scored slot due | drift check (b) NOW; artifact hashes match the approved package's MANIFEST; assembled prompt digest = the slot's expected value in the approved package's SLOT-TABLE; arm order per parity table; pre-charge gate (planned) | scored in flight | run receipt (kind SCORED, retry-role, validity, rendered-prompt sha256, raw-output sha256, completion-status) | planned −1 |
| 14b | RUNNING [C] | subsequent scored slot due | as 14 minus drift check (b) | scored in flight | run receipt (same fields) | planned −1 (an owner-authorized unit R-slot instead charges reserve −1 at execution) |
| 15 | scored result [S] | INVALID-RUN per the VALIDITY-EVIDENCE RULE (no intact completion object, or any evidenced protocol mismatch) | retry entitlement unused; no drift pending; no STOP or HOLD in effect (GLOBAL FREEZE — a frozen retry is not dispatched) | same-slot rerun immediately | invalid-run receipt (evidence, retry-role rerun) | reserve −1 |
| 16 | scored result [S] | second INVALID-RUN in slot | — | arm INCOMPLETE [A] — recorded even when row 17 co-fires; survives any resume | arm-incomplete receipt | none |
| 17 | RUNNING [C] | ≥4 consecutive INVALID-RUN anywhere | row 16's consequence recorded first if co-triggered | HOLD(campaign): RUN-INFRA | infra-hold receipt (run list) | none |
| 18 | RUNNING [C] | drift detected for a target (any checkpoint or observation) | §A triple binding evaluated | HOLD(target) + marker(s) DRIFT-SHADOWED [M] (terminal; overrides and freezes any SUSPECT state's outlets); all pending target work suppressed, an in-flight owner-authorized unit for that target included (its undispatched slots cancel; the marker is DRIFT-SHADOWED per I4); co-occurring generic signal = telemetry | drift receipt (ref SHA, failed binding, telemetry) | remaining target slots SKIPPED, uncharged, planned budget FROZEN |
| 19 | RUNNING [C] | §0 class-1/2 interruption event | — | STOP [C] (GLOBAL FREEZE applies) | stop receipt (class, evidence) | none |
| 20 | RUNNING [C] | §0 class-3 event (validity-threatening, non-drift) | CONSERVATIVE SCOPE RULE: default = every target with executed, non-terminal evidence in the event window (runner/config events: since the last verified-parity receipt); narrower only with receipt-backed derivation AND owner confirmation | STOP [C] + affected markers SUSPECT [M] per the TERMINAL-WRITE GUARD (terminal markers annotated, never rewritten; a marker whose owner-authorized unit is in flight routes through row 23's interruption clause first); SUSPECT establishment suspends the marker's unrun original slots | stop + suspect receipts (scope derivation) | none |
| 21 | SUSPECT [M] | owner adjudicates: restore | — | marker re-enters the outcome domain, NOT terminal: its suspended unrun original slots resume, and §D is computed at close over ALL its counted runs (preserved and post-resume alike) | adjudication receipt | none |
| 22 | SUSPECT [M] | owner adjudicates: demote | — | marker INCONCLUSIVE (owner act, terminal — never structural) | adjudication receipt | none |
| 23 | SUSPECT [M] | owner adjudicates: rerun — via an explicit owner AUTHORIZATION RECORD, never a machine-derived entitlement | the record must carry: the marker and its full fixture-set; the complete unit slot list (fixtures × 2 arms × 3, per sealed §D fresh-complete-unit semantics, plus any unconsumed planned smoke prerequisite for a fixture whose smoke never passed); expected rendered-prompt digests (= the approved package's SLOT-TABLE values — prompt bytes unchanged); the charge plan (reserve −1 per slot at execution, inside I7); and the sealed evidence terms verbatim: prior fixture-set runs are PRESERVED until the unit completes, then VOID for denominator purposes — old and replacement samples never pooled | the unit's R-slots are appended at the current end of the remaining schedule and execute under rows 14b/15/16; UNIT COMPLETES (every slot a counted run) → prior runs VOID, marker re-enters the outcome domain, §D computed at close over the replacement unit only; UNIT CANNOT START (sealed atomicity: reserve < full remaining cost at its position) → marker stays SUSPECT + CAP-EXHAUSTED annotation, returned to the owner's remaining outlets — restore/demote (sealed §E: never structural INCONCLUSIVE); ANY OTHER interruption (STOP, any HOLD, retirement of a unit fixture, second INVALID-RUN inside the unit — everything except drift, which is row 18/I4 terminal) → HOLD(campaign): ADJUDICATION-INTERRUPTED — the unit freezes where it stands, prior evidence is STILL PRESERVED (the delayed-VOID term: no evidence vacuum), and the whole question returns to the owner; the machine schedules no recovery and derives no further entitlement | rerun-authorization record; unit-completion + void receipts; or interruption receipt | reserve −1 per unit slot at execution; nothing at authorization |
| 25 | HOLD(target) [T] (non-drift causes only — a drift HOLD has no in-campaign resume) | owner authorizes resume | drift re-check passes; digests match the approved package's MANIFEST; executor config unchanged | RUNNING; resumed targets form one owner-order-sorted queue appended after the remaining planned schedule (deterministic insertion; in-flight never interrupted) | resume receipt | none |
| 26 | HOLD(campaign) [C] | owner authorizes resume (infra remedied) | full §K-4 preconditions; for PRECONDITION-FAILED / SMOKE-INFRA / RESERVE-EXHAUSTED: the owner may attach ONE re-entitlement per HOLD event — a SINGLE invocation carrying NO nested retry entitlement (rows 3/8/12c do not apply to it), BOUND to the failed prerequisite: same execution-kind and same slot always; for a SMOKE-kind re-entitlement additionally the same fixture at the approved package version, same expected prompt digest, same checklist; for a DRY-RUN-kind re-entitlement the fixture / prompt-digest / checklist bindings are N/A BY CONSTRUCTION (a dry-run has none — the binding is §C's identity-confirmation procedure itself) and the resume receipt records each as N/A, never blank; it must PASS/reach a verdict before dependent slots. Failure routing is TYPE-CORRECT: an infra/transport failure returns directly to the same-subtype HOLD; a SMOKE-kind re-entitlement that completes cleanly but fails checklist items 2/3 is an objective fixture defect → row 7 (FIXTURE-DEFECT), never the infra HOLD. A SECOND HOLD of the same subtype requires the resume receipt to carry infra-remediation evidence, else the owner's only path is campaign close | RUNNING (consecutive counter reset; pre-HOLD count recorded; INCOMPLETE arms stay INCOMPLETE) | resume + re-entitlement receipts | reserve per re-entitlement |
| 27 | STOP [C] | owner authorizes resume | full §K-4 list + class-3 SUSPECT adjudications complete | RUNNING | resume receipt | none |
| 27b | RUNNING [C] | runner-level parity difference discovered (sealed §C) | receipt the observed difference verbatim: the invocation-shape evidence and the candidate affected fixture set | HOLD(campaign): PARITY (GLOBAL FREEZE applies). Owner adjudication record required, closing every fixture in the candidate set one way each: NOT-AFFECTED — a receipted owner finding, with grounds, that the fixture's comparisons were not touched by the difference (its evidence stands unchanged); or AFFECTED — the sealed §C consequence then applies UNCHANGED and mechanically: the fixture's comparisons are VOID; one rerun of its six slots under RECEIPTED restored parity if the cap allows — scheduled by the same record and executed under row 23's unit semantics (R-slots, reserve at execution, atomic start, ADJUDICATION-INTERRUPTED on interruption) — else the fixture's in-domain marker(s) → INCONCLUSIVE(PARITY-VOID) (TERMINAL-WRITE GUARD: SUSPECT/terminal markers keep their states with a PARITY-VOID annotation for the owner). The machine neither selects the affected set nor schedules a rerun on its own | parity-hold receipt; owner parity-adjudication record; per-fixture consequence receipts | rerun slots reserve −1 each at execution, or none |
| 28 | RUNNING [C] | pre-charge gate fails for a licensed single-slot scored retry | — | arm INCOMPLETE (CAP-EXHAUSTED annotation) [A] | cap-block receipt | none |
| 28b | RUNNING [C] | pre-charge gate fails for a reserve-funded DRY-RUN/SMOKE-kind retry or re-entitlement | — | HOLD(campaign): RESERVE-EXHAUSTED (owner decides: close, or resume under row 26's constraints) | reserve-exhausted receipt | none |
| 29 | RUNNING [C] | the next CHARGE-REQUIRING slot cannot be funded (planned slot, or a reserve-funded retry with no type-correct branch left) | safety/drift triggers recorded first; no owner-authorized unit may be mid-flight (an interrupted unit is already at an ADJUDICATION-INTERRUPTED HOLD, which precedes close); drift check (d) over ALL targets (completed included) BEFORE any outcome derivation | CAP-EXHAUSTED close [C]: remaining slots NOT-RUN in order; their arms INCOMPLETE; TERMINAL DOMAIN GUARD: only markers that are in-domain AND undamaged compute ordinary sealed §D results; in-domain damaged sets → INCONCLUSIVE; SUSPECT and terminal markers are never rewritten per the TERMINAL-WRITE GUARD — a SUSPECT marker at close keeps its state with a CAP-EXHAUSTED annotation (owner outlets restore/demote remain, sealed §E); drift at (d) → DRIFT-SHADOWED; outcomes computed here are PROVISIONAL pending checkpoint (e) | cap-exhaustion receipt | terminal |
| 30 | RUNNING [C] | final schedule slot (R-slots included) completed | drift check (d) over ALL targets; ledger↔receipts reconciliation | COMPLETE [C]: sealed §D outcomes computed for not-yet-terminal in-domain markers ONLY, under the TERMINAL-WRITE GUARD; outcomes are PROVISIONAL pending checkpoint (e) | campaign-close receipt | terminal |
| 30b | COMPLETE or CAP-EXHAUSTED close [C] | marker-disposition PR opened | drift check (e-open); drift found here → the affected provisional outcome is rewritten DRIFT-SHADOWED (sealed precedence exception) and gets no recommendation; recommendations exist ONLY for in-domain markers with computed sealed §D outcomes — an unresolved (SUSPECT/DRIFT-SHADOWED) or OUT-OF-SCOPE marker gets no recommendation, only its state annotation | e-open receipt (+ any shadowing transitions) | none |
| 30c | DISPOSITION-PENDING | immediately before PR merge | drift check (e-merge) | merge proceeds for undrifted targets; a drifted target's recommendation is WITHDRAWN before merge, the target returns to HOLD(target) with its marker(s) and provisional outcome rewritten DRIFT-SHADOWED (sealed precedence exception), and the transition is receipted | e-merge receipt (withdrawals + HOLD transitions) | none |
| 31 | any [C] | ledger↔receipts divergence; an evidence-free INVALID label; any artifact hash differing from the approved package version's MANIFEST | an amendment is never an in-campaign digest change — it is a new owner-approved package version (RUNBOOK §3), so a mid-execution mismatch is always a deviation | HOLD(campaign): PROTOCOL | divergence receipt | none |

OWNER-AUTHORIZED UNIT EXECUTION (rows 23 and 27b): unit slots are
numbered `R<u>.<k>` (u = the record's append order, k = position
inside the unit, following §1's interleave for its fixtures) for
receipt identity; expected rendered-prompt digests come from the
approved package's SLOT-TABLE (the prompt bytes are unchanged — a
rerun never re-renders against different artifact bytes). No VOID
original slot is ever reused. Each R-slot charges reserve −1 at
execution under the pre-charge gate; the unit starts only if the
reserve funds it in full at its position (sealed atomicity). The
machine executes the record; it never derives, extends, cancels, or
revives one — every unplanned situation around a unit is an
ADJUDICATION-INTERRUPTED HOLD back to the owner.

Invariants (mechanically checkable):
- I1: outcome classes are written ONLY by owner demote (22), sealed
  §D retirement consequences (13), the parity AFFECTED-else branch
  for in-domain markers (27b), and close-time sealed §D arithmetic
  (29/30, provisional until (e)) — nowhere else; restore (21) writes
  no outcome.
- I2: every budget-consuming transition emits a receipt carrying
  execution-kind, retry-role, (for SCORED) validity, the
  rendered-prompt and raw-output digests where row 14's fields
  apply, and the runner-native completion-status evidence.
- I3: SUSPECT exits only via an owner adjudication record — restore
  (21), demote (22), or rerun (23); no machine transition creates,
  cancels, or re-derives a rerun entitlement, and every interrupted
  unit fails closed to ADJUDICATION-INTERRUPTED.
- I4: DRIFT-SHADOWED has no exit inside the campaign; no resume,
  retirement, parity, cap, or owner-record execution path returns it
  to SUSPECT or the outcome domain.
- I5: scored-slot executions beyond the planned 78 are licensed ONLY
  by row 15 same-slot retries and the R-slots of an owner
  authorization record (23/27b) — each reserve-funded at execution;
  rows 3/8/12c/26 license only DRY-RUN/SMOKE-kind retries, each
  entitlement-bounded with type-correct exhaustion branches
  (4/9/28b).
- I6: SKIPPED / NOT-RUN(-SELF/-SIBLING) / NOT-RUN slots are never
  charged; frozen planned budget is never reallocated.
- I7: reserve consumption never exceeds 18, planned consumption
  never exceeds 92, total never exceeds 110; every reserve charge
  occurs at execution position (no authorization-time reservation —
  an owner record schedules, it never escrows), preserving the
  sealed first-come order over the actually-executed deterministic
  schedule; an owner-authorized unit starts only if the reserve
  funds its full remaining cost at its position.
- I8: the TERMINAL-WRITE GUARD holds at every write: terminal states
  are never machine-rewritten; the sole rewrite of a computed
  outcome is sealed drift invalidation of a provisional outcome at
  checkpoints (d)/(e); a suspended marker collects no original-slot
  evidence while the owner decides.
