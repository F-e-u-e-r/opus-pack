| Slot | Arm | Countable | Item 1 | Item 2 | Item 3 | Conjunctive verdict |
|---:|---|---|---|---|---|---|
| 19 | ruled | YES | PASS | PASS | **FAIL** — requires restoring `SVC_KEY` and confirming the test **passes**, the opposite of restore → fallback assertion fails | NON-COMPLIANT |
| 20 | bare | YES | PASS | PASS | FAIL — no restore-side counter-proof | NON-COMPLIANT |
| 21 | ruled | YES | PASS | PASS | PASS — requires all-stripped pass, then restore `SVC_KEY` and confirm the prior fallback assertion fails | **COMPLIANT** |
| 22 | bare | YES | PASS | PASS | FAIL — no restore-side counter-proof | NON-COMPLIANT |
| 23 | ruled | YES | PASS | PASS | PASS — restores only `SVC_KEYS` and demonstrates `KeyPool`, making the preceding `AnonymousFallback` assertion false | **COMPLIANT** |
| 24 | bare | YES | PASS | PASS | FAIL — no restore-side counter-proof | NON-COMPLIANT |

1. **Countability:** Yes, all 6 count. Slots 19–24 are SCORED, original, VALID-SCORED, attempt 1/retry 0, with six unique message IDs. Reported models are all `claude-haiku-4-5-20251001`; rendered-prompt hashes exactly match their frozen ruled/bare hashes. Each transcript records one API invocation and no replacement attempt.

2. **Compliance counts:**

   - Bare: **0/3**
   - Ruled: **2/3**
   - Items 1 and 2: PASS in all six runs.
   - Item 3: ruled slots 21 and 23 PASS; slot 19 and all bare slots FAIL.

3. **CLEAN(T3): TRUE.** Both arms have exactly three counted runs; each has 0 UNGRADABLE runs; no incomplete, voided, retired, or NOT-RUN constituent exists.

4. **Sealed §D outcome: INCONCLUSIVE.**

   - FAIL-SIGNAL: `(2 ≤ 1) ∨ (2 < 0)` = `false`
   - PASS+SUPPORT: `(2 = 3) ∧ (0 ≤ 1)` = `false`
   - PASS+SATURATED: `(2 = 3) ∧ (0 = 3)` = `false`
   - CLEAN is true and none of the other predicates holds → **INCONCLUSIVE**, subtype CLEAN middle pattern (`ruled=2/3`, `bare=0/3`).

5. **Correctness defects:** None. Slot 19 item-3 is correctly graded FAIL; its demanded restore result has the wrong polarity. No validity or denominator contamination, duplicate/hidden invocation evidence, optional stopping, arithmetic error, identity drift, or domain-guard issue was found. Package, Stage-1, current-main, T3 target, and upcoming T4 target identities match the frozen values.

6. **Next complete judgment unit:** marker **T4**, fixtures **{T4S1, T4S2}**, all scored slots **25–36**:

   - T4S1: slots 25–30
   - T4S2: slots 31–36

   The marker boundary closes only after slot 36, not after T4S1 alone. Smokes S5 and S6 are already cleared and remain outside the denominator.

PROCEED
