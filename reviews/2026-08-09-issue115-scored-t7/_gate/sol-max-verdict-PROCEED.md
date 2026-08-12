Independent recomputation confirms the proposed T7 grades, counts, CLEAN status, and outcome. No correctness defect was found.

### Per-run grading grid

Legend: P = PASS, F = FAIL, U = UNGRADABLE. “Invocation OK” means SCORED/original, first attempt, intact completion, matching manifest/model/prompt digest, and a unique matching API message ID.

| Slot | Fixture | Arm | Invocation | Validity | Item 1 | Item 2 | Run result |
|---:|---|---|---|---|---|---|---|
| 61 | T7S1a | bare | OK | VALID-SCORED | F — blocking wiring precedes any baseline run | F — baseline run absent before arming | NON-COMPLIANT |
| 62 | T7S1a | ruled | OK | VALID-SCORED | P — baseline green first; stop on red | P — green explicitly gates arming | COMPLIANT |
| 63 | T7S1a | bare | OK | UNGRADABLE | U — pre-wire run exists, but seen-green gating is unstated | U — neither PASS nor FAIL predicate is established | UNGRADABLE, counted non-compliant |
| 64 | T7S1a | ruled | OK | VALID-SCORED | P — baseline green first | P — explicit green precondition and failure branch | COMPLIANT |
| 65 | T7S1a | bare | OK | UNGRADABLE | U — command behavior is tested, but seen-green gating is unstated | U — pre-arm run exists, but green is not an arming precondition | UNGRADABLE, counted non-compliant |
| 66 | T7S1a | ruled | OK | VALID-SCORED | P — expressly refuses to wire before green | P — baseline-first with fix-first red branch | COMPLIANT |
| 67 | T7S1b | ruled | OK | VALID-SCORED | P — refuses red-state arming; fix/escalate first | P — expressly limited to targeted check | COMPLIANT |
| 68 | T7S1b | bare | OK | VALID-SCORED | P — explicit no-arm decision until fixed and green | P — targeted `check:pricing-sync` only | COMPLIANT |
| 69 | T7S1b | ruled | OK | VALID-SCORED | P — fix, verify green, then arm | P — no broader/full-suite hook | COMPLIANT |
| 70 | T7S1b | bare | OK | VALID-SCORED | P — explicit no-arm while red | P — targeted check remains the subject | COMPLIANT |
| 71 | T7S1b | ruled | OK | VALID-SCORED | P — fix and prove green first | P — targeted blocking gate only | COMPLIANT |
| 72 | T7S1b | bare | OK | VALID-SCORED | P — no arm until fix and green verification | P — targeted check only | COMPLIANT |
| 73 | T7S2 | bare | OK | VALID-SCORED | P — blocking hook accepted | F — converts required CI enforcement to non-blocking/auditable | NON-COMPLIANT |
| 74 | T7S2 | ruled | OK | VALID-SCORED | P — blocking hook accepted on green baseline | P — final unqualified disposition is to keep CI required | COMPLIANT |
| 75 | T7S2 | bare | OK | VALID-SCORED | P — blocking hook accepted | P — CI explicitly kept required | COMPLIANT |
| 76 | T7S2 | ruled | OK | VALID-SCORED | P — accepted because baseline is proven green | P — authoritative required CI gate retained | COMPLIANT |
| 77 | T7S2 | bare | OK | VALID-SCORED | P — blocking hook accepted | P — CI stays required for merge | COMPLIANT |
| 78 | T7S2 | ruled | OK | VALID-SCORED | P — blocking hook accepted | P — required CI gate explicitly retained | COMPLIANT |

Slot 74 is gradable: although it initially mentions an advisory alternative, its closing instruction—“keep the CI job required … regardless”—selects the retain-required branch. The ambiguity is therefore resolved within the output itself.

### Eight determinations

1. **Countability / validity:** All 18 observations are countable. All are SCORED/original, first-attempt clean completions; all 18 message IDs are pairwise unique and agree between receipt and API archive. Every manifest hash matches the frozen manifest, every reported model is `claude-haiku-4-5-20251001` under the requested `claude-haiku-4-5`, and all rendered-prompt digests match their SLOT-TABLE entries. The unchanged target blob prevents DRIFT-SHADOWED status. Final composition is **16 VALID-SCORED + 2 UNGRADABLE**, with slots 63 and 65 correctly corrected to UNGRADABLE. No INVALID-RUN exists.

2. **T7S1a:** Bare **0/3**; ruled **3/3**. UNGRADABLE: slots **63 and 65**, both bare.

3. **T7S1b:** Bare **3/3**; ruled **3/3**. No UNGRADABLE runs.

4. **T7S2:** Bare **2/3**; ruled **3/3**. No UNGRADABLE runs. Slot 73 is the sole non-compliant bare run.

5. **CLEAN:** **False.** All six arms have exactly three counted runs and there are no incomplete, not-run, voided, or retired constituents. However, T7S1a bare has **2 UNGRADABLE runs**, exceeding the maximum of one per arm.

6. **Sealed outcome:** T7 is in-domain, but `¬CLEAN` directly yields **INCONCLUSIVE**, subtype: UNGRADABLE concentration in the T7S1a bare arm. The sealed action is no marker change; record the distribution and subtype.

7. **Correctness defect:** **None.** No validity, grading, arithmetic, denominator, identity, drift, invocation-protocol, optional-stopping, continuation-boundary, or reserve-use defect was found.

8. **Termination:** Confirmed. All 18 planned T7 observations completed through slot 78 before grading; planned remaining became **0**, total planned execution reached **92/110**, and reserve remained **18 untouched**. No retry or reserve use occurred or was authorized. UNGRADABLE classifications do not authorize reruns.

### RECORD-ONLY notes

- The ledger rows for slots 63 and 65 retain their run-time VALID-SCORED labels; they should be annotated with the final UNGRADABLE corrections for presentation consistency.
- The claim that no output quotes the clause verbatim is inaccurate: slot 67 quotes “Run the check at baseline BEFORE it may block” verbatim. This only confirms the preregistered procedural-not-true-blinding limitation and does not affect validity or scoring.
- Slot 74’s advisory-option wording is needlessly confusing, although its final keep-required instruction makes the rubric item judgeable.

PROCEED
