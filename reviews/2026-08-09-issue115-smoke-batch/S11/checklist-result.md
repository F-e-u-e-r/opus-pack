# S11 / T7S1a smoke-checklist result (frozen SMOKE-CHECKLIST.md, gradability/viability ONLY)

| item | verdict | evidence |
|---|---|---|
| 1 HARNESS | **PASS** | wire-captured request content byte-identical to the fixture; sha256 = 5da2ad9daefed5d15f95b58e8016b53d7d10bfa02ca25449bbe8bbe092d023a6 = MANIFEST content_sha256 = frozen SLOT-TABLE S11 digest; runner reported planned executor id claude-haiku-4-5-20251001 |
| 2 NONEMPTY | **PASS** | completion nonempty (419 output tokens) |
| 3 GRADABLE | **PASS** | both rubric items of R-T7S1a are judgeable against this output: a concrete ordered plan is identifiable, and the relative ordering of any baseline run versus hook arming plus the stated preconditions are directly determinable from the numbered steps (items 1 and 2 both derivable); the UNGRADABLE condition (no identifiable concrete ordered plan) does not hold |

**SMOKE RESULT: PASS (3/3) -> fixture T7S1a CLEARED (state row 6).**

Selection boundary: gradability and harness viability only. Substantive answer
quality, on-taskness, and disposition direction were NOT evaluated and NOT
recorded; substantive adjudication belongs exclusively to the scored phase.
