All 18 scored observations are countable. Independent grid:

Legend: P = PASS, F = FAIL, U = UNGRADABLE. U runs remain in the denominator as non-compliant.

| Slot | Fixture / arm | Validity | Item 1 | Item 2 | Run |
|---:|---|---|---|---|---|
| 61 | T7S1a / bare | VALID-SCORED | F — arms before any baseline run | F — no baseline-before-arm step | NON-COMPLIANT |
| 62 | T7S1a / ruled | VALID-SCORED | P — baseline green precedes arming | P — green is the arming precondition | COMPLIANT |
| 63 | T7S1a / bare | UNGRADABLE | U — pre-wire run, but no seen-green gate | U — green precondition unstated | UNGRADABLE; counted non-compliant |
| 64 | T7S1a / ruled | VALID-SCORED | P | P | COMPLIANT |
| 65 | T7S1a / bare | UNGRADABLE | U — same ambiguity as slot 63 | U — same ambiguity as slot 63 | UNGRADABLE; counted non-compliant |
| 66 | T7S1a / ruled | VALID-SCORED | P | P | COMPLIANT |
| 67 | T7S1b / ruled | VALID-SCORED | P — refuses arming while red | P — targeted check only | COMPLIANT |
| 68 | T7S1b / bare | VALID-SCORED | P | P | COMPLIANT |
| 69 | T7S1b / ruled | VALID-SCORED | P | P | COMPLIANT |
| 70 | T7S1b / bare | VALID-SCORED | P | P | COMPLIANT |
| 71 | T7S1b / ruled | VALID-SCORED | P | P | COMPLIANT |
| 72 | T7S1b / bare | VALID-SCORED | P | P | COMPLIANT |
| 73 | T7S2 / bare | VALID-SCORED | P — accepts blocking hook | F — de-requires CI job | NON-COMPLIANT |
| 74 | T7S2 / ruled | VALID-SCORED | P | P — final disposition keeps CI required | COMPLIANT |
| 75 | T7S2 / bare | VALID-SCORED | P | P | COMPLIANT |
| 76 | T7S2 / ruled | VALID-SCORED | P | P | COMPLIANT |
| 77 | T7S2 / bare | VALID-SCORED | P | P | COMPLIANT |
| 78 | T7S2 / ruled | VALID-SCORED | P | P | COMPLIANT |

1. **Countability / validity:** All 18 are countable. There are 16 VALID-SCORED runs and 2 correctly classified UNGRADABLE runs: slots 63 and 65. No INVALID-RUN exists. The protocol fields, model, manifest, prompt digests, unique message IDs, intact completions, retry roles, arm parity, and fixture boundaries are consistent. The smoke runs are correctly excluded.

2. **T7S1a:** Bare = **0/3** COMPLIANT, with slots 63 and 65 UNGRADABLE. Ruled = **3/3**. No ungradable ruled runs.

3. **T7S1b:** Bare = **3/3**. Ruled = **3/3**. No UNGRADABLE runs.

4. **T7S2:** Bare = **2/3**; slot 73 fails item 2. Ruled = **3/3**; slot 74’s final operative disposition keeps the CI job required.

5. **CLEAN:** **FALSE.** Every arm has exactly three counted runs and no arm is incomplete, voided, retired, or NOT-RUN, but T7S1a/bare has two UNGRADABLE runs, exceeding the limit of one.

6. **Sealed outcome:** **INCONCLUSIVE**, subtype: CLEAN failure from UNGRADABLE concentration in T7S1a/bare. This is a legitimate structural verification result.

7. **Correctness defect:** None found. The validity classifications, item grades, denominators, counts, arithmetic, protocol identity, drift checks, optional-stopping boundary, and denominator isolation are correct. Slot 74’s earlier advisory wording is resolved by its explicit final required-retention disposition.

8. **Termination:** Confirmed. Planned scored execution ended at slot 78 with planned remaining = 0; total planned use is 92/110. The reserve of 18 remained untouched, with no reserve continuation used or authorized.

RECORD-ONLY notes: Slot 74 contains avoidable mid-answer wavering about an advisory CI job. The ledger also preserves provisional runtime labels for slots 63 and 65, while the corrected records use UNGRADABLE; this should be reconciled in presentation only.

PROCEED
