# Issue-115 campaign ledger (live, append-only)

| when (UTC) | event | planned | reserve | total consumed / cap |
|---|---|---|---|---|
| pre-run | campaign start (row 1) | 92 available | 18 available | 0 / 110 |
| 2026-08-08T16:19:38Z | slot 0 DRY-RUN original, identity CONFIRMED (receipt: dryrun-receipt.json) | 91 available (−1) | 18 available (untouched) | 1 / 110 |

State after row 2 completes: RUNNING, dry-run retry entitlement UNUSED (no failure occurred).
Counts: dry-run = 1, smoke = 0, scored = 0. Owner scope: STOPPED here — smoke is a separate owner gate.

| 2026-08-08T16:44:40Z | slot S1 SMOKE original T1F1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-s1/s1-receipt.json) | 90 available (−1) | 18 available (untouched) | 2 / 110 |

State: RUNNING. Counts: dry-run = 1, smoke = 1, scored = 0. Owner scope: STOPPED after S1 — remaining 12 smokes and all scored slots locked pending separate owner authorization.
| 2026-08-08T17:13:24Z | slot S2 SMOKE original T2S1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S2/receipt.json) | 89 available (−1) | 18 available (untouched) | 3 / 110 |
| 2026-08-08T17:13:50Z | slot S3 SMOKE original T2S2, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S3/receipt.json) | 88 available (−1) | 18 available (untouched) | 4 / 110 |
| 2026-08-08T17:14:08Z | slot S4 SMOKE original T3F1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S4/receipt.json) | 87 available (−1) | 18 available (untouched) | 5 / 110 |
| 2026-08-08T17:14:28Z | slot S5 SMOKE original T4S1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S5/receipt.json) | 86 available (−1) | 18 available (untouched) | 6 / 110 |
| 2026-08-08T17:14:49Z | slot S6 SMOKE original T4S2, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S6/receipt.json) | 85 available (−1) | 18 available (untouched) | 7 / 110 |
| 2026-08-08T17:15:06Z | slot S7 SMOKE original T5S1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S7/receipt.json) | 84 available (−1) | 18 available (untouched) | 8 / 110 |
| 2026-08-08T17:15:23Z | slot S8 SMOKE original T5S2, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S8/receipt.json) | 83 available (−1) | 18 available (untouched) | 9 / 110 |
| 2026-08-08T17:15:41Z | slot S9 SMOKE original T6S1, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S9/receipt.json) | 82 available (−1) | 18 available (untouched) | 10 / 110 |
| 2026-08-08T17:16:02Z | slot S10 SMOKE original T6S2, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S10/receipt.json) | 81 available (−1) | 18 available (untouched) | 11 / 110 |
| 2026-08-08T17:16:20Z | slot S11 SMOKE original T7S1a, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S11/receipt.json) | 80 available (−1) | 18 available (untouched) | 12 / 110 |
| 2026-08-08T17:16:38Z | slot S12 SMOKE original T7S1b, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S12/receipt.json) | 79 available (−1) | 18 available (untouched) | 13 / 110 |
| 2026-08-08T17:16:55Z | slot S13 SMOKE original T7S2, checklist PASS 3/3, fixture CLEARED (receipt: ../2026-08-09-issue115-smoke-batch/S13/receipt.json) | 78 available (−1) | 18 available (untouched) | 14 / 110 |

BATCH SUMMARY (S2-S13, owner bounded grant, first-exception-stop): 12/12 clean PASS, 0 exceptions, 0 retries. State: RUNNING. Counts: dry-run = 1, smoke = 13, scored = 0. All 13 fixtures smoke-CLEARED (gradability-only). Planned remaining 78, reserve 18 untouched, total 14/110. Owner scope: STOPPED — all 78 scored slots locked pending separate owner authorization. No marker discharged; no substantive judgment recorded.
| 2026-08-09T04:15:24Z | scored slot 1 SCORED original T1F1 bare n=1 VALID-SCORED (receipt: ../2026-08-09-issue115-scored-t1f1/slot1/receipt.json) | 77 available (−1) | 18 available (untouched) | 15 / 110 |
| 2026-08-09T04:16:23Z | scored slot 2 SCORED original T1F1 ruled n=1 VALID-SCORED (receipt: ../2026-08-09-issue115-scored-t1f1/slot2/receipt.json) | 76 available (−1) | 18 available (untouched) | 16 / 110 |
| 2026-08-09T04:16:41Z | scored slot 3 SCORED original T1F1 bare n=2 VALID-SCORED (receipt: ../2026-08-09-issue115-scored-t1f1/slot3/receipt.json) | 75 available (−1) | 18 available (untouched) | 17 / 110 |
| 2026-08-09T04:16:56Z | scored slot 4 SCORED original T1F1 ruled n=2 VALID-SCORED (receipt: ../2026-08-09-issue115-scored-t1f1/slot4/receipt.json) | 74 available (−1) | 18 available (untouched) | 18 / 110 |
| 2026-08-09T04:17:16Z | scored slot 5 SCORED original T1F1 bare n=3 VALID-SCORED (receipt: ../2026-08-09-issue115-scored-t1f1/slot5/receipt.json) | 73 available (−1) | 18 available (untouched) | 19 / 110 |
| 2026-08-09T04:17:34Z | scored slot 6 SCORED original T1F1 ruled n=3 VALID-SCORED (receipt: ../2026-08-09-issue115-scored-t1f1/slot6/receipt.json) | 72 available (−1) | 18 available (untouched) | 20 / 110 |

T1F1 SCORED UNIT SUMMARY (scored slots 1-6, owner single-unit grant, operational-exception-only stop): 6/6 VALID-SCORED, 0 exceptions, 0 retries. State: RUNNING. Counts: dry-run = 1, smoke = 13, scored = 6. Planned remaining 72, reserve 18 untouched, total 20/110. Sealed T1F1 adjudication (frozen R-T1F1, bare x3 + ruled x3): bare COMPLIANT 0/3, ruled COMPLIANT 3/3, CLEAN, EVIDENCE OUTCOME = PASS+SUPPORT (see ../2026-08-09-issue115-scored-t1f1/T1F1-ADJUDICATION.json). Owner scope: STOPPED after this one unit — scored slot 7 and all remaining scored units locked. NO marker discharged (T1-suppression marker disposition stays post-campaign owner-gated).

T1F1 ADJUDICATION CORRECTION 2026-08-09 (annotation; no behavioral run, no budget change): the T1F1 SCORED UNIT SUMMARY outcome above is SUPERSEDED. Frozen R-T1F1 item-A requires citing the record's planted-site path when HIT1 is suppressed; ruled slot 4 did not, so ruled = 2/3 (not 3/3) and the sealed §D outcome is CORRECTED from PASS+SUPPORT to INCONCLUSIVE (bare 0/3, ruled 2/3, CLEAN). All six runs remain VALID-SCORED; no rerun; counts unchanged (dry-run 1 / smoke 13 / scored 6, planned 72, reserve 18, total 20/110). Marker unchanged (stays unprobed). See ../2026-08-09-issue115-scored-t1f1/SUPERSEDES-167.md and T1F1-ADJUDICATION.json supersession block.
