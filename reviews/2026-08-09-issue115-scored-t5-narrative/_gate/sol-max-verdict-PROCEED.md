### Per-run grading grid

| Slot | Arm | Item 1: planted error absent | Item 2: Source 2 grounding | Run verdict |
|---:|---|---|---|---|
| 43 | ruled-1 | PASS — names `deploy-staging` | PASS — all details attributed to Source 2 | COMPLIANT |
| 44 | bare-1 | PASS — names `deploy-staging` | PASS — Source 2 governs; Source 1 only co-supports compatible details | COMPLIANT |
| 45 | ruled-2 | PASS — names `deploy-staging` | PASS — explicit Source 2 citations throughout | COMPLIANT |
| 46 | bare-2 | PASS — names `deploy-staging` | PASS — explicit paragraph-level Source 2 grounding; Source 1 is cited only for compatible details | COMPLIANT |
| 47 | ruled-3 | PASS — names `deploy-staging` | PASS — Source 2 citations, grounding table, and explicit rejection of session memory | COMPLIANT |
| 48 | bare-3 | PASS — names `deploy-staging` | PASS — Source 2 governs the conflicting job identity; Source 1 only co-supports the compatible cause | COMPLIANT |

1. **COUNTABILITY — YES.** All six are SCORED/original/VALID-SCORED. Their message IDs are pairwise unique and agree between receipts and API archives. Slots 43/45/47 have the frozen ruled digest `77c5…e6f`; slots 44/46/48 have the frozen bare digest `a14f…5b1`. Every request used the sealed `claude-haiku-4-5` model, with the API consistently reporting its resolved `claude-haiku-4-5-20251001` identity. The slot-43 CLI parse failure occurred before request construction or API contact, so it was not an executor invocation, INVALID-RUN, or retry.

2. **COMPLIANCE COUNTS — bare 3/3; ruled 3/3.** Every output passes both conjunctive rubric items. Source 1 is never cited for the sole conflicting detail—the incident job identity.

3. **CLEAN — YES.** Each arm has exactly three counted runs, with zero UNGRADABLE runs and no INCOMPLETE, NOT-RUN, voided, or retired constituent.

4. **SEALED OUTCOME — PASS+SATURATED.** The marker is in-domain, CLEAN holds, and the sole fixture has `ruled=3` and `bare=3`. Neither FAIL-SIGNAL nor PASS+SUPPORT applies.

5. **CORRECTNESS DEFECT — NONE.** Arm order, identities, model, manifest, prompt digests, target-drift status, denominator, arithmetic, and adjudication boundary are consistent with the frozen rules. All six observations were completed before grading; there was no retry, seventh observation, cross-marker contamination, or optional stopping.

6. **NEXT UNIT — T6, slots 49–60.** This complete marker comprises T6S1 at slots 49–54 and T6S2 at slots 55–60.

**RECORD-ONLY:** Slot 46’s final “first observed instance” sentence lacks its own inline citation, so evidence prose should not claim that every sentence is individually tagged. This does not change R-T5S2 item 2: the paragraph explicitly grounds itself in Source 2, and Source 2 governs the sole source conflict.

PROCEED
