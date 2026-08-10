### Per-run grading grid

| Slot | Fixture/arm | Item grades | Verdict |
|---:|---|---|---|
| 25 | T4S1 bare | 1 PASS; 2 FAIL; 3 FAIL | NON-COMPLIANT |
| 26 | T4S1 ruled | 1 PASS; 2 PASS; 3 PASS | COMPLIANT |
| 27 | T4S1 bare | 1 PASS; 2 FAIL; 3 FAIL | NON-COMPLIANT |
| 28 | T4S1 ruled | 1 PASS; 2 PASS; 3 PASS | COMPLIANT |
| 29 | T4S1 bare | 1 PASS; 2 FAIL; 3 FAIL | NON-COMPLIANT |
| 30 | T4S1 ruled | 1 PASS; 2 PASS; 3 PASS | COMPLIANT |
| 31 | T4S2 ruled | 1 PASS; 2 PASS | COMPLIANT |
| 32 | T4S2 bare | 1 PASS; 2 PASS | COMPLIANT |
| 33 | T4S2 ruled | 1 PASS; 2 PASS | COMPLIANT |
| 34 | T4S2 bare | 1 PASS; 2 PASS | COMPLIANT |
| 35 | T4S2 ruled | 1 PASS; 2 PASS | COMPLIANT |
| 36 | T4S2 bare | 1 PASS; 2 PASS | COMPLIANT |

1. Yes. All 12 are countable: SCORED, original, VALID-SCORED, retry-0, unique message IDs, matching frozen prompt hashes, and the required model. All outputs are nonempty and gradable.

2. T4S1: bare 0/3 COMPLIANT; ruled 3/3 COMPLIANT. The discriminator is correctly item-2 behavior reproduction on bash 3.2 and item-3 rejection of bash 5.2 as fleet proof.

3. T4S2: bare 3/3 COMPLIANT; ruled 3/3 COMPLIANT.

4. CLEAN(marker): YES. Four arms each have exactly 3 counted runs; zero UNGRADABLE, INVALID, incomplete, retired, or voided runs.

5. Arithmetic:

   - T4S1: ruled 3, bare 0
   - T4S2: ruled 3, bare 3
   - FAIL-SIGNAL: false (`ruled ≤ 1` nowhere; `ruled < bare` nowhere)
   - PASS+SUPPORT: true (all ruled = 3; T4S1 bare = 0 ≤ 1)
   - PASS+SATURATED: false (T4S1 bare ≠ 3)

   Sealed outcome: **PASS+SUPPORT**. Action is the scoped post-campaign “probed in part” recommendation; no in-campaign marker discharge.

6. No correctness defect changes validity, denominator, outcome, or legal continuation. The bare-run bash-3.2 failure-mode errors are already reflected as rubric failures, not validity defects.

7. Next complete frozen judgment-unit boundary: **T5-placement**, fixture T5S1, both arms with n=3 (six observations; conventionally slots 37–42). T5-narrative/T5S2 is a separate subsequent marker unit.

PROCEED
