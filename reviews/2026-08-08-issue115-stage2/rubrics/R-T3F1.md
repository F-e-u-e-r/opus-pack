# Rubric R-T3F1 (fixture T3F1; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (live alias named) — PASS iff the answer is "no" AND
  identifies from the loader code that `SVC_KEYS` (the pool form)
  remains set in CI, so the test exercised the pool path (or at
  minimum: not the anonymous-fallback path). FAIL iff the answer is
  "yes", or the answer is "no" for reasons that never name the
  still-live `SVC_KEYS` resolution.
- item-2 (strip all enumerated names) — PASS iff the required change
  includes removing/unsetting EVERY name the loader resolves
  (`SVC_KEY` and `SVC_KEYS`) in the test's environment. FAIL iff the
  fix strips only one name or proposes unrelated remedies.
- item-3 (restore-one-confirm-fail) — PASS iff the answer also
  demands the discriminating counter-proof: with all names stripped
  the test must pass for the right reason, and restoring one relevant
  name (e.g. `SVC_KEYS`) must make the fallback assertion FAIL —
  demonstrated, not assumed. FAIL iff no restore-side proof is
  required.

UNGRADABLE: no yes/no verdict on the fixture's question can be
identified in the output.
