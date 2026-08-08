# Issue-115 STAGE-2 State-Transition Table (r2)

Operational states only — never a replacement for the sealed outcome
taxonomy (PASS+SUPPORT / PASS+SATURATED / FAIL-SIGNAL / INCONCLUSIVE
remain §D's, computed from receipts). No transition converts SUSPECT,
DRIFT-SHADOWED, invalidity, or cap exhaustion into a different
epistemic outcome. Scope tags: [C]=campaign, [T]=target, [F]=fixture,
[A]=arm, [M]=marker, [S]=slot.

GLOBAL PRE-CHARGE GATE (applies to EVERY budget-consuming transition,
before invocation): the charge's pool (planned pool for original
planned slots; reserve pool for every retry/rerun/re-smoke/
re-entitled dry-run/SUSPECT unit) must hold ≥ the charge, AND total
consumption after the charge must be ≤ 110. A charge failing the gate
never executes; the corresponding cap-block transition (28/29) fires
instead. Cap-block/safety/drift triggers take precedence over any
retry entitlement (a licensed retry is not started once its gate
fails or a drift/HOLD governs the target). An owner-authorized
SUSPECT unit ESCROWS its full cost from the reserve pool at
authorization (row 23); escrow is released only by unit completion or
owner cancellation.

DRIFT PREEMPTION (global): the moment drift is detected for a target,
every pending invocation, retry, and rerun for that target is
suppressed (not started, not charged) — row 18 governs; a licensed
same-slot retry never outruns a drift HOLD.

Format: # | current | trigger | required checks | next | receipt |
budget.

| # | Current | Trigger | Required checks | Next | Receipt | Budget |
|---|---|---|---|---|---|---|
| 1 | READY [C] | owner authorizes execution (post-STAGE-2 sign-off) | drift check (a) all targets; MANIFEST re-hash vs the merged-PR tree digest; PREREG-v6 hash 2c7e3f21… | RUNNING [C] | campaign-start (roster, PR merge SHA, MANIFEST digest, drift results) | none |
| 2 | RUNNING [C] | slot 0 due | pre-charge gate (planned) | dry-run in flight | dry-run receipt (kind DRY-RUN, retry-role original, runner-reported identity) | planned −1 |
| 3 | dry-run result | fails (API/identity) | retry entitlement unused; pre-charge gate (reserve) | one dry-run retry | dry-run receipt (retry-role rerun) | reserve −1 |
| 4 | dry-run result | fails twice | — | HOLD(campaign): PRECONDITION-FAILED | precondition-failure receipt | none |
| 5 | RUNNING [C] | fixture's smoke slot due | fixture content hash matches MANIFEST; pre-charge gate (planned) | smoke in flight | smoke receipt (kind SMOKE, retry-role, prompt sha256 = fixture content sha256) | planned −1 |
| 6 | smoke result [F] | passes gradability/viability checklist | — | fixture CLEARED | smoke-pass receipt | none |
| 7 | smoke result [F] | fails checklist (objective fixture defect) | defect class ∈ preregistered set | repair-gate [F] (max 1) | smoke-fail receipt (defect class) | none |
| 8 | smoke result [F] | transport/protocol failure (INVALID-RUN conditions on a smoke, runner-native evidence attached) | retry entitlement unused; pre-charge gate (reserve) | one smoke rerun | smoke receipt (retry-role rerun) | reserve −1 |
| 9 | smoke result [F] | second transport/protocol failure | — | HOLD(campaign): SMOKE-INFRA | smoke-infra-hold receipt | none |
| 10 | repair-gate [F] | repaired artifact passes static mini-gate (final-gate lens + owner sign) | new hash versioned into MANIFEST (a MANIFEST regeneration is itself part of this gated event and nothing else may regenerate it); prior runs of fixture VOID; pre-charge gate (reserve) for the re-smoke | re-smoke in flight | repair-pass receipt (old/new hashes) | reserve −1 |
| 11 | repair-gate [F] | mini-gate fails OR owner declines | — | RETIRED [F] (artifact FROZEN-INVALID) | repair-fail receipt | none |
| 12a | re-smoke result [F] | passes checklist | — | fixture CLEARED | re-smoke-pass receipt | none |
| 12b | re-smoke result [F] | fails checklist | — | RETIRED [F] | retirement receipt | none |
| 12c | re-smoke result [F] | transport/protocol failure | retry entitlement unused; pre-charge gate (reserve) | one re-smoke rerun; a second such failure → HOLD(campaign): SMOKE-INFRA | smoke receipt / smoke-infra-hold | reserve −1 |
| 13 | RETIRED [F] | — (consequences per sealed §D) | single-fixture marker? | marker OUT-OF-SCOPE [M] per sealed §D; else marker INCONCLUSIVE(RETIRED-MEMBER) [M] per sealed §D; the retired fixture's own unrun slots NOT-RUN(RETIRED-SELF) [S]; unrun slots of the SAME MARKER SET's sibling fixtures NOT-RUN(RETIRED-SIBLING) [S] (a sibling serving a different marker — T5 — is untouched) | retirement-consequence receipt | cancelled slots uncharged; their planned budget is FROZEN, never reallocated |
| 14 | RUNNING [C] | target's FIRST scored slot due | drift check (b) NOW (after smoke, immediately before scored); wrapper/fixture/clause hashes match MANIFEST; expected rendered-prompt sha256 from SLOT-TABLE matches the assembled prompt; arm order per parity table; pre-charge gate (planned) | scored in flight | run receipt (kind SCORED, retry-role, validity, rendered-prompt sha256, raw-output sha256) | planned −1 |
| 14b | RUNNING [C] | subsequent scored slot due | same as 14 minus drift check (b) | scored in flight | run receipt (same fields) | planned −1 |
| 15 | scored result [S] | INVALID-RUN (runner-native evidence attached: API error body, exit status, or a hash mismatch record — a classification without such evidence is itself a protocol deviation → row 31) | retry entitlement unused; no drift pending for target; pre-charge gate (reserve) | same-slot rerun immediately | invalid-run receipt (evidence, retry-role rerun) | reserve −1 |
| 16 | scored result [S] | second INVALID-RUN in slot | — | arm INCOMPLETE [A] (annotated) — recorded even when row 17 also fires on the same invocation | arm-incomplete receipt | none |
| 17 | RUNNING [C] | ≥4 consecutive INVALID-RUN anywhere | row 16's consequence, if co-triggered, is recorded FIRST and survives any later resume (counter reset never resurrects an entitlement or clears an INCOMPLETE) | HOLD(campaign): RUN-INFRA | infra-hold receipt (run list) | none |
| 18 | RUNNING [C] | drift detected for a target (any checkpoint or observation) | §A triple binding evaluated | HOLD(target) + marker(s) DRIFT-SHADOWED [M]; all pending invocations/retries for the target suppressed; co-occurring generic signal recorded as telemetry only | drift receipt (ref SHA, failed binding, telemetry note) | remaining target slots SKIPPED, uncharged, planned budget FROZEN |
| 19 | RUNNING [C] | §0 class-1/2 interruption event | — | STOP [C] | stop receipt (class, evidence) | none |
| 20 | RUNNING [C] | §0 class-3 event (validity-threatening, non-drift) | CONSERVATIVE SCOPE RULE: the affected set defaults to every target with any executed, non-terminal evidence inside the event's time window (for a runner/config/parity event: every such target since the last verified-parity receipt); a narrower set is legitimate only with receipt-backed derivation AND owner confirmation | STOP [C] + affected markers SUSPECT [M] | stop receipt + suspect receipts (scope derivation) | none |
| 21 | SUSPECT [M] | owner adjudicates: restore | — | marker re-enters outcome domain | adjudication receipt | none |
| 22 | SUSPECT [M] | owner adjudicates: demote | — | marker INCONCLUSIVE (owner act, never structural) | adjudication receipt | none |
| 23 | SUSPECT [M] | owner adjudicates: rerun — available ONCE per marker (rerun-used guard; after use, only restore/demote remain) | reserve pool ≥ full unit cost → ESCROW it now | SUSPECT-RERUN-PENDING [M]: prior fixture-set runs VOID; unit appended at current schedule end | adjudication + void + escrow receipts | reserve escrow (unit cost) |
| 23b | SUSPECT-RERUN-PENDING [M] | unit's slots execute (rows 14/14b semantics, reserve-funded from escrow) and ALL complete | per-slot checks as 14 | marker re-enters outcome domain; sealed §D arithmetic computed over the REPLACEMENT unit's runs only | unit-completion receipt | escrow consumed |
| 23c | SUSPECT-RERUN-PENDING [M] | unit cannot complete (drift/HOLD/infra per their own rows) | — | marker returns to SUSPECT (rerun consumed; owner outlets: restore/demote) | unit-abort receipt | unconsumed escrow released |
| 24 | SUSPECT [M] | owner adjudicates rerun, reserve pool < unit cost | — | marker stays SUSPECT + CAP-EXHAUSTED annotation (restore/demote remain) | cap-blocked-suspect receipt | none |
| 25 | HOLD(target) [T] | owner authorizes resume | drift re-check passes; MANIFEST re-hash vs campaign-start digest; executor config unchanged | RUNNING; the target joins the resume queue — ALL resumed targets execute in ORIGINAL owner order as one queue appended after the currently remaining planned schedule; a later-authorized target that precedes an already-queued (not yet started) resumed target in owner order is inserted before it; in-flight slots are never interrupted | resume receipt | none |
| 26 | HOLD(campaign) [C] | owner authorizes resume (infra remedied) | full §K-4 precondition list; for PRECONDITION-FAILED: the owner explicitly RE-ENTITLES one further dry-run (reserve −1) and it must PASS before any other slot runs; for SMOKE-INFRA: the owner re-entitles one further smoke attempt for the blocked fixture (reserve −1) and it must reach a checklist verdict before that fixture's scored slots | RUNNING (consecutive counter reset; pre-HOLD count recorded; INCOMPLETE arms stay INCOMPLETE) | resume receipt (+ re-entitlement receipts) | reserve per re-entitlement |
| 27 | STOP [C] | owner authorizes resume | full §K-4 list + class-3 SUSPECT adjudications complete | RUNNING | resume receipt | none |
| 27b | RUNNING [C] | runner-level parity difference discovered mid-campaign (sealed §C) | affected fixture identified; comparisons VOID | if reserve pool ≥ 6: the fixture's six scored slots re-run ONCE under restored parity (appended at schedule end, reserve-funded); else its marker(s) INCONCLUSIVE(PARITY-VOID) | parity-void receipt (+ rerun or inconclusive receipts) | reserve −6 or none |
| 28 | RUNNING [C] | pre-charge gate fails for a licensed single-slot retry | — | arm INCOMPLETE (CAP-EXHAUSTED annotation) [A] | cap-block receipt | none |
| 29 | RUNNING [C] | pre-charge gate fails for the next PLANNED slot, or total consumption reaches 110 | safety/drift triggers recorded first; drift check (d) runs NOW over all non-terminal targets BEFORE any outcome derivation | CAP-EXHAUSTED close [C]: remaining slots NOT-RUN in order; their arms INCOMPLETE; markers whose sets are thereby damaged → INCONCLUSIVE; markers with COMPLETE clean sets receive their ordinary sealed §D result; drift found at (d) → those markers DRIFT-SHADOWED instead | cap-exhaustion receipt | terminal |
| 30 | RUNNING [C] | final schedule slot completed | drift check (d) all targets; ledger↔receipts reconciliation | COMPLETE [C]: sealed §D outcomes computed | campaign-close receipt | terminal |
| 30b | COMPLETE [C] | marker-disposition PR opened | drift check (e-open) | DISPOSITION-PENDING | e-open receipt | none |
| 30c | DISPOSITION-PENDING | immediately before PR merge | drift check (e-merge) | merge proceeds for undrifted targets; a drifted target's recommendation is WITHDRAWN before merge and the target recorded HOLD/DRIFT-SHADOWED | e-merge receipt (withdrawals listed) | none |
| 31 | any [C] | ledger↔receipts divergence, or an evidence-free INVALID classification, or any unauthorized MANIFEST regeneration detected | — | HOLD(campaign): PROTOCOL | divergence receipt | none |

Invariants (mechanically checkable):
- I1: outcome classes are written ONLY by owner acts (21/22), by the
  sealed §D retirement consequences (13), and by close-time sealed
  §D arithmetic (23b/29/30) — no other transition writes one.
- I2: every budget-consuming transition emits a receipt carrying
  execution-kind, retry-role, and (for SCORED) validity, plus the
  rendered-prompt and raw-output digests where row 14's fields apply.
- I3: SUSPECT exits only via owner adjudication (21/22/23/24); the
  rerun outlet is one-shot per marker (23's guard); 23b/23c are the
  only exits from SUSPECT-RERUN-PENDING.
- I4: DRIFT-SHADOWED has no exit transition inside the campaign.
- I5: scored-slot reruns are licensed ONLY by rows 15 (single-slot),
  23/23b (SUSPECT unit), and 27b (parity void) — each atomicity- and
  pool-guarded; rows 3/8/10/12c/26 license only their own
  DRY-RUN/SMOKE-kind retries, each entitlement-bounded.
- I6: SKIPPED / NOT-RUN(RETIRED-SELF/SIBLING) / NOT-RUN slots are
  never charged, and their frozen planned budget is never reallocated
  to any pool.
- I7: no invocation starts without passing the global pre-charge gate
  against its OWN pool; reserve consumption (including live escrows)
  never exceeds 18, planned consumption never exceeds 92, and total
  consumption never exceeds 110.
