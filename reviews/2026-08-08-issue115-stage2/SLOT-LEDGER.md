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
| Owner-authorized SUSPECT fixture-set rerun unit | T1 6 · T2 12 · T3 6 · T4 12 · T5-placement 6 · T5-narrative 6 · T6 12 · T7 18 | one-shot per marker; charged atomically at execution position (rows 23a/24); an un-smoked unit fixture first clears its unconsumed planned smoke slot |

## What must HOLD instead of spending reserve

- A second infra failure of the same smoke or slot (rows 9/16).
- A second dry-run failure (row 4).
- Any unit the remaining budget cannot fund IN FULL (rows 24/28 — no
  partial rerun, ever).
- Replacement fixtures: no such mechanism exists; wanting one is a
  STAGE-1-level change → HOLD to owner (RUNBOOK §4).
- Ledger↔receipts divergence (row 31).

## Two pools, strictly separated

- PLANNED POOL (92): funds ONLY the original planned slots (dry-run
  0, smokes S1–S13, scored 1–78), each exactly once. A cancelled or
  skipped planned slot's budget is FROZEN — it reduces total
  consumption and is NEVER reallocated to fund anything else.
- RESERVE POOL (18): funds ONLY retries/reruns — the dry-run retry,
  smoke/re-smoke reruns, repair re-smokes, single-slot INVALID
  reruns, parity-void fixture reruns (6 per event, charged atomically
  at execution position), owner re-entitlements at resume, and
  owner-authorized SUSPECT units (charged atomically IN FULL at the
  unit's execution position — no authorization-time reservation, so
  the sealed first-come consumption order over the executed schedule
  is preserved; a unit unfundable at its position never starts).
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
  where applicable; the ledger is append-only during execution and
  re-derived from receipts at every HOLD, resume, and close —
  divergence → HOLD(campaign) (state row 31).
- The absolute 92-slot expansion with per-slot expected
  rendered-prompt digests lives in `SLOT-TABLE.md` (generated,
  frozen with the package).
