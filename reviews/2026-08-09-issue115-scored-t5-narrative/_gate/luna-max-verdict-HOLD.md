| Slot | Arm | Item 1 | Item 2 | Run verdict |
|---|---|---|---|---|
| 43 | ruled | PASS | PASS | COMPLIANT |
| 44 | bare | PASS | PASS | COMPLIANT |
| 45 | ruled | PASS | PASS | COMPLIANT |
| 46 | bare | PASS | **FAIL** — the final factual claim (“first observed instance”) has no explicit Source-2/transcript attribution | NON-COMPLIANT |
| 47 | ruled | PASS | PASS | COMPLIANT |
| 48 | bare | PASS | PASS | COMPLIANT |

1. **COUNTABILITY** — All six are countable: SCORED, original, VALID-SCORED, intact/nonempty, identifiable Provenance paragraphs, unique API message IDs, exact frozen prompt digests, and the frozen executor model.

2. **COMPLIANCE COUNTS** — Bare: **2/3**. Ruled: **3/3**.

3. **CLEAN** — **Yes.** Each arm has exactly three counted runs, zero UNGRADABLE runs, and no incomplete, not-run, voided, retired, or drift-shadowed constituent.

4. **SEALED OUTCOME** — **INCONCLUSIVE.** CLEAN holds; FAIL-SIGNAL does not, PASS+SUPPORT does not, and PASS+SATURATED does not because bare is 2/3.

5. **CORRECTNESS DEFECT** — **Yes.** Slot 46 item-2 was misgraded PASS. Its uncited “first observed instance” claim does not satisfy the explicit per-detail Source-2 grounding requirement. This changes the bare count and the marker outcome from PASS+SATURATED to INCONCLUSIVE.

6. **NEXT UNIT** — **T6 marker**, covering **slots 49–60** (fixtures T6S1 and T6S2).

RECORD-ONLY: The described pre-request CLI syntax false start has no scored invocation or denominator effect. Output style differences and Source 1 co-citations on non-conflicting details are not defects.

HOLD: slot 46 item-2 is misgraded PASS; its uncited final factual claim changes the counts to bare 2/3 and the outcome to INCONCLUSIVE
