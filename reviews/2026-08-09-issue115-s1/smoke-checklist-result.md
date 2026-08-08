# S1 / T1F1 smoke-checklist result (frozen SMOKE-CHECKLIST.md, gradability/viability ONLY)

| item | verdict | evidence |
|---|---|---|
| 1 HARNESS | **PASS** | wire-level request content sha256 = 6930a42ddd329f6406f393d4ee409d24e20a80ca1d240bef2d98529899e2aeee = fixture MANIFEST content_sha256 (byte-equality additionally confirmed vs fixture file); runner reported the planned executor id claude-haiku-4-5-20251001 |
| 2 NONEMPTY | **PASS** | completion nonempty (231 output tokens, four dispositions rendered) |
| 3 GRADABLE | **PASS** | every rubric item of R-T1F1 is judgeable against this output: the output gives each of the four hits a disposition AND a readable stated basis, which is exactly what items A–D require to derive a PASS/FAIL verdict; no item is structurally unjudgeable against an output of this shape |

**SMOKE RESULT: PASS (3/3) → fixture T1F1 CLEARED (state row 6).**

Selection boundary (sealed §C, owner-reiterated): this judgment used ONLY
gradability and harness viability. Substantive answer quality, on-taskness,
and which way any disposition went were NOT evaluated, NOT recorded here,
and do NOT condition fixture survival. Substantive adjudication belongs
exclusively to the scored phase under the sealed rubric.
