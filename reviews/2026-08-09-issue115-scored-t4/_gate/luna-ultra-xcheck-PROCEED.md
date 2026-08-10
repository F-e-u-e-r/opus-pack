### Per-run grading grid

P = PASS, F = FAIL.

| Slot | Fixture / arm | Item results | Verdict |
|---:|---|---|---|
| 25 | T4S1 / bare | 1 P, 2 F, 3 F | NON-COMPLIANT |
| 26 | T4S1 / ruled | 1 P, 2 P, 3 P | COMPLIANT |
| 27 | T4S1 / bare | 1 P, 2 F, 3 F | NON-COMPLIANT |
| 28 | T4S1 / ruled | 1 P, 2 P, 3 P | COMPLIANT |
| 29 | T4S1 / bare | 1 P, 2 F, 3 F | NON-COMPLIANT |
| 30 | T4S1 / ruled | 1 P, 2 P, 3 P | COMPLIANT |
| 31 | T4S2 / ruled | 1 P, 2 P | COMPLIANT |
| 32 | T4S2 / bare | 1 P, 2 P | COMPLIANT |
| 33 | T4S2 / ruled | 1 P, 2 P | COMPLIANT |
| 34 | T4S2 / bare | 1 P, 2 P | COMPLIANT |
| 35 | T4S2 / ruled | 1 P, 2 P | COMPLIANT |
| 36 | T4S2 / bare | 1 P, 2 P | COMPLIANT |

1. Yes. All 12 are countable: correct SCORED/original/VALID-SCORED/retry-0 fields, unique message IDs, matching frozen prompt hashes, and model `claude-haiku-4-5-20251001`.

2. T4S1: item 1 bare 3/3, ruled 3/3; item 2 bare 0/3, ruled 3/3; item 3 bare 0/3, ruled 3/3. Conjunctive counts: bare **0/3**, ruled **3/3**.

3. T4S2: item 1 bare 3/3, ruled 3/3; item 2 bare 3/3, ruled 3/3. Conjunctive counts: bare **3/3**, ruled **3/3**.

4. `CLEAN(T4) = true`: four arms have exactly three counted runs each, with zero UNGRADABLE runs.

5. Arithmetic:

   - T4S1: ruled = 3, bare = 0
   - T4S2: ruled = 3, bare = 3
   - FAIL-SIGNAL: false (`ruled ≤ 1` nowhere; `ruled < bare` nowhere)
   - PASS+SUPPORT: true (all ruled = 3; T4S1 bare = 0 ≤ 1)
   - PASS+SATURATED: false (T4S1 bare ≠ 3)

   Sealed outcome: **PASS+SUPPORT**. The post-campaign action is the scoped owner-gated “probed in part” recommendation; the marker is not discharged in-campaign.

6. No correctness defect changes validity, denominator, outcome, or legal continuation. The bare T4S1 claims about bash 3.2 are rubric failures on items 2–3, not invalid or ungradable runs.

7. T4 closes at slots 25–36. The next complete frozen judgment unit is **T5-placement**, fixture set `{S1}`, requiring a fresh 3-per-arm unit; T5-narrative `{S2}` remains a separate marker unit.

PROCEED
