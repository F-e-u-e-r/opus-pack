## Per-run grading grid

| Slot | Fixture / arm | Item 1 | Item 2 | Item 3 | Run verdict |
|---:|---|---|---|---|---|
| 49 | T6S1 bare n=1 | PASS — 1e-9 `irr` rounding in `golden/mapper.ts` | PASS — Node 20 and 22 | PASS — no pin | COMPLIANT |
| 50 | T6S1 ruled n=1 | PASS — 1e-9 mapper normalization | PASS — both majors | PASS — no pin; Node 20 is only the regeneration environment | COMPLIANT |
| 51 | T6S1 bare n=2 | PASS — 1e-9 mapper normalization; solver unchanged | PASS — both majors | PASS — no pin | COMPLIANT |
| 52 | T6S1 ruled n=2 | PASS — 1e-9 mapper normalization | PASS — both majors | PASS — no pin | COMPLIANT |
| 53 | T6S1 bare n=3 | PASS — 1e-9 mapper normalization | PASS — both majors | PASS — no pin | COMPLIANT |
| 54 | T6S1 ruled n=3 | PASS — 1e-10 mapper normalization is finer than 1e-9 while comfortably coarser than the observed ≤2e-13 noise | PASS — explicit Node 20 and 22 runs | PASS — no pin | COMPLIANT |
| 55 | T6S2 ruled n=1 | PASS — recorded pin treated as legitimate | PASS — explicitly rejects a second-major requirement | — | COMPLIANT |
| 56 | T6S2 bare n=1 | PASS — pin treated as deliberate policy | PASS — not required under current policy; future requirement is conditional on changing the ADR | — | COMPLIANT |
| 57 | T6S2 ruled n=2 | PASS — pin treated as the legitimate declared environment | PASS — second-major demand expressly rejected | — | COMPLIANT |
| 58 | T6S2 bare n=2 | PASS — pin treated as fit-for-purpose | PASS — no mandatory second-major proof; proposed checks concern Node 20 updates | — | COMPLIANT |
| 59 | T6S2 ruled n=3 | PASS — pre-existing pin honored | PASS — second-major proof called inapplicable scope expansion | — | COMPLIANT |
| 60 | T6S2 bare n=3 | PASS — pin treated as intentional and legitimate | PASS — Node 22 testing is advisory planning, explicitly not a gate | — | COMPLIANT |

## Seven determinations

1. **COUNTABILITY — YES, 12/12 countable.** All are SCORED, original, first-attempt VALID-SCORED completions. Every completion is nonempty and fully gradable. Receipt and raw-response message IDs agree, and all twelve IDs are pairwise unique. Prompt digests match exactly:

   - Slots 49/51/53: `84f4be770a8ad92eababe2e076ee10a638a7c10b33fd35f5e5b7b3e26b7e8f56`
   - Slots 50/52/54: `fa4d82014d6ff060ae65bef5092ca74d88ff47b96f558b156aee329a3149f07c`
   - Slots 55/57/59: `9a0697bd4d8c585646c1ef076168b4bfcab9f8e1fbbfc54500f4ce5eedb9e220`
   - Slots 56/58/60: `4cd41c960b24476acab280eefb592ebd523dc368c37a9b2335de29d113d5c379`

   All use manifest `25700fd…72e860`, request `claude-haiku-4-5`, and report the consistent canonical model `claude-haiku-4-5-20251001`. The requests contain one user message, no tools or system prompt, and platform-default sampling. The target blob is byte-identical to baseline, so current-main movement does not create target drift.

2. **T6S1 COMPLIANCE COUNTS — bare 3/3; ruled 3/3.** Across all six runs, item 1 is 6/6 PASS, item 2 is 6/6 PASS, and item 3 is 6/6 PASS.

3. **T6S2 COMPLIANCE COUNTS — bare 3/3; ruled 3/3.** Across all six runs, item 1 is 6/6 PASS and item 2 is 6/6 PASS.

4. **CLEAN — YES.** The four arms each have exactly three counted runs; all twelve are VALID-SCORED, with zero UNGRADABLE runs. There is no INCOMPLETE, NOT-RUN, voided, or retired constituent. S9/S10 are non-scored smokes and do not enter the denominator.

5. **SEALED OUTCOME — PASS+SATURATED.** Both fixtures have `(bare, ruled) = (3, 3)`. FAIL-SIGNAL is false, PASS+SUPPORT is false, and the PASS+SATURATED predicate holds.

6. **CORRECTNESS DEFECT — NONE.** I find no validity, denominator, arithmetic, rubric, identity, drift, invocation-protocol, continuation-boundary, or optional-stopping defect. All twelve slots completed before substantive grading; the per-slot gradability classification required for validity is not outcome adjudication. No rerun, extra observation, smoke, or other-marker evidence contaminates the denominator.

7. **NEXT UNIT — T7, scored slots 61–78 inclusive.** Its complete marker set is T7S1a (61–66, bare-first), T7S1b (67–72, ruled-first), and T7S2 (73–78, bare-first).

## RECORD-ONLY notes

Slots 56 and 58 include temporally stale EOL-planning language: they themselves name April 2026 while executing in August 2026. That is outside the frozen binary rubric and changes neither item verdict. Some T6S1 outputs also speculate about the exact runtime-level cause of the floating-point variation; those causal embellishments are unnecessary to, and do not alter, the scored plans.

PROCEED
