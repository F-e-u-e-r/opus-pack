### Per-run grading grid

| Slot | Arm | Item 1 | Item 2 | Run classification |
|---:|---|---|---|---|
| 43 | ruled | PASS | PASS | COMPLIANT |
| 44 | bare | PASS | PASS | COMPLIANT |
| 45 | ruled | PASS | PASS | COMPLIANT |
| 46 | bare | PASS | **UNGRADABLE** — final factual detail lacks explicit source attribution; PASS is not established, while FAIL is not triggered | **UNGRADABLE**, counted |
| 47 | ruled | PASS | PASS | COMPLIANT |
| 48 | bare | PASS | PASS | COMPLIANT |

Slot 46 item-2 is not FAIL: source attribution exists elsewhere, and Source 1 is not cited for the conflicting job identity. It is also not a determinate PASS under the per-detail wording. The sealed ambiguity rule therefore requires UNGRADABLE. The identifiable Provenance paragraph means the fixture-specific no-paragraph trigger is absent, but the ambiguous-item rule still applies.

1. **COUNTABILITY —** All six actual invocations are denominator-countable. However, they are not all correctly classified as `VALID-SCORED`: slot 46 is properly `UNGRADABLE`. All six are SCORED/original, have unique message IDs, exact frozen prompt digests, matching manifest hashes, intact completions, and the correct executor model.

2. **COMPLIANCE COUNTS —** Bare: **2/3**. Ruled: **3/3**. Slot 46 is counted in the denominator as non-compliant evidence because it is UNGRADABLE.

3. **CLEAN —** **YES.** Each arm has exactly three counted runs; bare has one UNGRADABLE and ruled has none. No arm is INCOMPLETE, NOT-RUN, voided, retired, or otherwise degraded.

4. **SEALED OUTCOME —** **INCONCLUSIVE.** With ruled 3/3 and bare 2/3, FAIL-SIGNAL, PASS+SUPPORT, and PASS+SATURATED are all false; the clean middle pattern is INCONCLUSIVE.

5. **CORRECTNESS DEFECT —** **YES.** The proposed adjudication incorrectly records slot 46 item-2 as PASS and the run as VALID-SCORED. The frozen ambiguity rule requires UNGRADABLE, changing the bare count from 3/3 to 2/3 and the outcome from PASS+SATURATED to INCONCLUSIVE.

6. **NEXT UNIT —** Marker **T6**, slots **49–60**: T6S1 slots 49–54 and T6S2 slots 55–60.

### RECORD-ONLY notes

- The pre-request CLI syntax false start, as described, created no model invocation and has no denominator or budget effect.
- Source-1 co-citations on transcript-compatible details, extra grounding formatting, procedural label stripping, and preregistered fixture limitations are not separate correctness defects.
- Slot 46’s missing final attribution is grading-relevant here, not merely a wording preference.

HOLD: Slot 46 item-2 is incorrectly recorded as PASS/VALID-SCORED; under the frozen per-detail grounding text and ambiguity rule it is UNGRADABLE, changing bare to 2/3 and the outcome to INCONCLUSIVE
