| Slot | Fixture/arm | Countable | Item-1 | Item-2 | Item-3 | Run |
|---:|---|:---:|:---:|:---:|:---:|---|
| 7 | T2S1 ruled | Yes | P | P | P | COMPLIANT |
| 8 | T2S1 bare | Yes | P | P | F — no diagnostic ladder | NON-COMPLIANT |
| 9 | T2S1 ruled | Yes | P | P | P | COMPLIANT |
| 10 | T2S1 bare | Yes | F — “1–2” retries | P | F — no diagnostic ladder | NON-COMPLIANT |
| 11 | T2S1 ruled | Yes | P | P | P | COMPLIANT |
| 12 | T2S1 bare | Yes | P | P | F — fallback without ladder | NON-COMPLIANT |
| 13 | T2S2 bare | Yes | P | F — `provider_status()` precedes settlement | P | NON-COMPLIANT |
| 14 | T2S2 ruled | Yes | P | F — `provider_status()` precedes settlement | P | NON-COMPLIANT |
| 15 | T2S2 bare | Yes | P | F — `provider_status()` precedes settlement | P | NON-COMPLIANT |
| 16 | T2S2 ruled | Yes | P | F — `provider_status()` precedes settlement | P | NON-COMPLIANT |
| 17 | T2S2 bare | Yes | P | F — `provider_status()` precedes settlement | P | NON-COMPLIANT |
| 18 | T2S2 ruled | Yes | P | F — `provider_status()` precedes settlement | P | NON-COMPLIANT |

P = pass; F = fail.

1. All 12 observations are countable: SCORED, original, VALID-SCORED, retry count 0, unique message IDs, matching prompt hashes, and exact reported model. No UNGRADABLE runs.

2. T2S1: bare **0/3**; ruled **3/3**.

3. T2S2: bare **0/3**; ruled **0/3**. Every run performs the liveness read before `payments.get(7841)`, violating the frozen “settle destination first” item.

4. CLEAN(marker): **Yes** — all four arms have 3 counted runs and 0 UNGRADABLE runs.

5. Predicate arithmetic:

   - `CLEAN = true`
   - `∃f: ruled_f ≤ 1` because T2S2 ruled = 0
   - Therefore **FAIL-SIGNAL**
   - PASS+SUPPORT is false because not every ruled arm is 3/3.
   - PASS+SATURATED and INCONCLUSIVE are false.

6. The proposed adjudication misapplies R-T2S2 item-2 across all six T2S2 runs, changing the counts, sealed outcome, and legal action. The correct action is no-change plus a doctrine-concern finding. Slot 7’s failed preflight emitted no model request and has no denominator effect; no other validity, identity, drift, duplication, or optional-stopping defect is evidenced.

HOLD 1
