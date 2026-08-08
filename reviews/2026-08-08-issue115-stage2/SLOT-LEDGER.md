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
| Repair re-smoke | 1 per repaired fixture | max one repair per fixture (row 10) |
| Owner-authorized SUSPECT fixture-set rerun unit | T1 6 · T2 12 · T3 6 · T4 12 · T5-placement 6 · T5-narrative 6 · T6 12 · T7 18 | only if remaining budget ≥ full unit (rows 23/24); no smoke re-run inside the unit |

## What must HOLD instead of spending reserve

- A second infra failure of the same smoke or slot (rows 9/16).
- A second dry-run failure (row 4).
- Any unit the remaining budget cannot fund IN FULL (rows 24/28 — no
  partial rerun, ever).
- Replacement fixtures: no such mechanism exists; wanting one is a
  STAGE-1-level change → HOLD to owner (RUNBOOK §4).
- Ledger↔receipts divergence (row 31).

## Accounting rules

- SKIPPED (target HOLD), RETIRED-CANCELLED, and NOT-RUN slots are
  never charged (invariant I6).
- Every charge emits a receipt with the three receipt fields
  (execution-kind / retry-role / validity-for-SCORED); the ledger is
  append-only during execution and re-derived from receipts at every
  HOLD, resume, and close — divergence → HOLD(campaign).
- Arithmetic check: 92 planned + 18 reserve = 110 = hard cap. The
  worst-case licensed consumption cannot exceed 110 by construction
  (each licensed event is entitlement-bounded and atomicity-guarded).
