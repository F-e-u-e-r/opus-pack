# Issue-115 campaign ledger (live, append-only)

| when (UTC) | event | planned | reserve | total consumed / cap |
|---|---|---|---|---|
| pre-run | campaign start (row 1) | 92 available | 18 available | 0 / 110 |
| 2026-08-08T16:19:38Z | slot 0 DRY-RUN original, identity CONFIRMED (receipt: dryrun-receipt.json) | 91 available (−1) | 18 available (untouched) | 1 / 110 |

State after row 2 completes: RUNNING, dry-run retry entitlement UNUSED (no failure occurred).
Counts: dry-run = 1, smoke = 0, scored = 0. Owner scope: STOPPED here — smoke is a separate owner gate.

| 2026-08-08T16:44:40Z | slot S1 SMOKE original T1F1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-s1/s1-receipt.json) | 90 available (−1) | 18 available (untouched) | 2 / 110 |

State: RUNNING. Counts: dry-run = 1, smoke = 1, scored = 0. Owner scope: STOPPED after S1 — remaining 12 smokes and all scored slots locked pending separate owner authorization.
