# Issue-115 STAGE-2 Slot Ledger (pre-execution)

Budget envelope (sealed, immutable): planned 92 / hard cap 110 /
reserve 18. STAGE-2 redistributes nothing here — this ledger only
enumerates the sealed numbers; raising the cap requires owner
authorization and is not a runbook power.

## Fixed planned slots (92)

| Slot | Kind | Unit |
|---|---|---|
| 0 | DRY-RUN | 1 |
| S1–S13 | SMOKE (one per fixture, immediately before its scored block) | 13 |
| 1–78 | SCORED (13 fixtures × 2 arms × n=3, counterbalanced order per RUNBOOK §1) | 78 |
| **Total planned** | | **92** |

Per-target scored allocation (sealed §E): T1 6, T2 12, T3 6, T4 12,
T5 12, T6 12, T7 18 = 78.

## Reserve (18) — what may consume it

| Event | Atomic cost | Licensing |
|---|---|---|
| Dry-run retry | 1 | once (state row 3) |
| Smoke infra rerun | 1 per smoke | once per smoke (row 8); second failure → HOLD, not reserve |
| Scored INVALID-RUN same-slot rerun | 1 per slot | once per slot (row 15); second → arm INCOMPLETE, not reserve |
| Re-smoke infra rerun | 1 per re-smoke | once (row 12c); second → HOLD(campaign): SMOKE-INFRA |
| Post-amendment re-smoke | 1 per amended fixture | max one repair per fixture (row 7b; owner-approved amendment packet) |
| Owner re-entitlement at resume | 1 per HOLD event | single bound invocation, no nested retries (row 26) |
| Owner-authorized rerun unit (SUSPECT row 23 / parity row 27b) | SUSPECT units: T1 6 · T2 12 · T3 6 · T4 12 · T5-placement 6 · T5-narrative 6 · T6 12 · T7 18; parity: 6 per affected fixture | licensed ONLY by an explicit owner authorization record; reserve −1 per R-slot at execution; sealed atomic start (the reserve must fund the full unit at its position or it does not start); an un-smoked unit fixture first clears its unconsumed planned smoke slot; any interruption → ADJUDICATION-INTERRUPTED hold, back to the owner |

## Exhaustion and failure outcomes (typed per the state rows — the
ledger never substitutes a different branch)

- Second dry-run failure → HOLD(campaign): PRECONDITION-FAILED (row 4).
- Second harness/transport failure of the same smoke or re-smoke →
  HOLD(campaign): SMOKE-INFRA (rows 9/12c).
- Second INVALID-RUN in the same scored slot → that arm INCOMPLETE
  (row 16 — an arm consequence, not a campaign HOLD).
- Pre-charge failure of a single-slot scored retry → arm INCOMPLETE
  with CAP-EXHAUSTED annotation (row 28).
- Pre-charge failure of a reserve-funded DRY-RUN/SMOKE-kind retry or
  re-entitlement → HOLD(campaign): RESERVE-EXHAUSTED (row 28b).
- Owner-authorized unit unfundable in full at its execution position
  (sealed atomicity): the unit does not start — a SUSPECT unit's
  marker stays SUSPECT + CAP-EXHAUSTED annotation with the owner's
  restore/demote outlets intact (row 23); a parity unit's affected
  in-domain marker(s) → INCONCLUSIVE(PARITY-VOID) (row 27b).
- Objective fixture defect at smoke → HOLD(campaign): FIXTURE-DEFECT;
  owner outlets retire / amend (new package version) / close
  (rows 7/7b).
- No partial rerun exists on any path; an interrupted owner-authorized
  unit freezes at ADJUDICATION-INTERRUPTED with prior evidence
  preserved (row 23) — never a silent cancellation or auto-recovery.
- Replacement fixtures: no such mechanism exists; wanting one is a
  STAGE-1-level change → HOLD to owner (RUNBOOK §4).
- Ledger↔receipts divergence, evidence-free INVALID labels, or any
  hash differing from the approved package version's MANIFEST →
  HOLD(campaign): PROTOCOL (row 31).

## Two pools, strictly separated

- PLANNED POOL (92): funds ONLY the original planned slots (dry-run
  0, smokes S1–S13, scored 1–78), each exactly once. A cancelled or
  skipped planned slot's budget is FROZEN — it reduces total
  consumption and is NEVER reallocated to fund anything else.
- RESERVE POOL (18): funds ONLY retries/reruns — the dry-run retry,
  smoke/re-smoke reruns, post-amendment re-smokes, single-slot
  INVALID reruns, owner re-entitlements at resume, and the R-slots
  of owner-authorized rerun units (reserve −1 per slot at execution
  position; no authorization-time reservation, so the sealed
  first-come consumption order over the executed schedule is
  preserved; a unit unfundable in full at its position never
  starts).
- Consequently the sealed bound holds mechanically: rerun-class
  consumption can never exceed 18, whatever planned slots were
  cancelled; planned consumption can never exceed 92; total ≤ 110
  (invariant I7). The global pre-charge gate checks the OWN pool of
  every charge before invocation.

## Accounting rules

- SKIPPED, NOT-RUN(RETIRED-SELF/SIBLING), and NOT-RUN slots are never
  charged and their planned budget stays frozen (invariant I6).
- Every charge emits a receipt with execution-kind / retry-role /
  validity-for-SCORED plus the rendered-prompt and raw-output digests
  where applicable and the runner-native completion-status evidence;
  the ledger is append-only during execution and re-derived from
  receipts at every HOLD, resume, and close — divergence →
  HOLD(campaign) (state row 31).
- The absolute 92-slot expansion with per-slot expected
  rendered-prompt digests lives in `SLOT-TABLE.md` (generated,
  frozen with the package).
