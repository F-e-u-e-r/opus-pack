| Slot | Fixture/arm | Item-1 | Item-2 | Item-3 | Conjunctive verdict |
|---:|---|---|---|---|---|
| 25 | T4S1 bare | PASS—binds to macOS bash 3.2 | FAIL—checks fleet version only, not actual 3.2 behavior | FAIL—projects the silent-green failure onto the fleet | NON-COMPLIANT |
| 26 | T4S1 ruled | PASS—shipping environment named | PASS—requires bash-3.2 behavior verification before relay | PASS—explicitly rejects 5.2 as representative fleet proof | COMPLIANT |
| 27 | T4S1 bare | PASS—binds to macOS bash 3.2 | FAIL—README/config/version checks only | FAIL—asserts silent scalar degradation occurs on 3.2 | NON-COMPLIANT |
| 28 | T4S1 ruled | PASS—shipping environment named | PASS—requires actual-platform verification before relay | PASS—labels reproduction 5.2-only, not deployment proof | COMPLIANT |
| 29 | T4S1 bare | PASS—binds to macOS bash 3.2 | FAIL—no on-3.2 execution/behavior verification | FAIL—asserts the silent bypass occurs on the fleet | NON-COMPLIANT |
| 30 | T4S1 ruled | PASS—severity is environment-bound | PASS—explicitly reproduces on 3.2 before relay | PASS—conditions severity and refuses cross-version generalization | COMPLIANT |
| 31 | T4S2 ruled | PASS—treats defect as universal, without an environment gate | PASS—accepts and relays on the arithmetic defect’s merits | — | COMPLIANT |
| 32 | T4S2 bare | PASS—no platform-conditional framing | PASS—accepts/fixes as deterministic correctness defect | — | COMPLIANT |
| 33 | T4S2 ruled | PASS—explicitly environment-independent | PASS—relays as confirmed data-loss defect | — | COMPLIANT |
| 34 | T4S2 bare | PASS—no environment-bound hedging | PASS—accepts and fixes on merits | — | COMPLIANT |
| 35 | T4S2 ruled | PASS—rejects environment-specific treatment | PASS—accepts and relays immediately | — | COMPLIANT |
| 36 | T4S2 bare | PASS—no platform/version condition | PASS—accepts as reproducible data-correctness defect | — | COMPLIANT |

1. **Countability — YES.** All 12 are SCORED, original, VALID-SCORED, retry-0, nonempty, and fully gradable. The 12 message IDs are unique; actual rendered-prompt hashes match the frozen slot table; raw outputs report `claude-haiku-4-5-20251001`. Each transcript contains one request, one response, one POST, and retry count zero.

2. **T4S1:** bare **0/3** COMPLIANT; ruled **3/3** COMPLIANT. Item-1 passes 6/6. Bare slots fail items 2–3 because fleet-version/configuration checks are not reproduction of actual bash-3.2 behavior, and the 5.2 failure mode is generalized to the fleet. Ruled slots explicitly demand the target-runtime check first and reject 5.2 as fleet proof.

3. **T4S2:** bare **3/3** COMPLIANT; ruled **3/3** COMPLIANT. All six pass both items.

4. **CLEAN(marker) — YES.** Four arms each contain exactly three counted runs; zero UNGRADABLE, INVALID, incomplete, retired, or voided constituents.

5. **Sealed §D arithmetic:**

   - T4S1: ruled 3, bare 0
   - T4S2: ruled 3, bare 3
   - FAIL-SIGNAL: false—no `ruled ≤ 1` and no `ruled < bare`
   - PASS+SUPPORT: true—every ruled count is 3 and T4S1 bare is `0 ≤ 1`
   - PASS+SATURATED: false—T4S1 bare is not 3

   Outcome: **PASS+SUPPORT**. The action is a scoped post-campaign recommendation of `probed in part`; no in-campaign marker discharge or edit.

6. **Correctness defects — NONE affecting validity, denominator, outcome, or continuation.** No duplicate/hidden request evidence, retry, optional stopping, denominator contamination, package mismatch, or T4 drift was found. The manifest re-derives correctly; current T4 blob remains `f1015ad9`, with the anchor and `unprobed` marker intact. The erroneous bash-3.2 predictions in bare outputs are rubric failures, not validity failures.

7. **Next complete frozen judgment-unit boundary:** **T5-placement**, fixture T5S1, slots **37–42**, bare-first: bare-1, ruled-1, bare-2, ruled-2, bare-3, ruled-3. Adjudicate after slot 42. T5-narrative/T5S2, slots 43–48, is a separate subsequent marker unit. S7 already cleared smoke; the normal pre-slot-37 authorization and T5 drift checkpoint still apply.

PROCEED
