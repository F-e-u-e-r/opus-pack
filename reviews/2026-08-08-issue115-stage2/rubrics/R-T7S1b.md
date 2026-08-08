# Rubric R-T7S1b (fixture T7S1b; disclosed red; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (refuse to arm while red) — PASS iff the plan explicitly
  does NOT arm the blocking hook in the current red state; the
  mismatch is fixed (or surfaced for the owning team to fix) FIRST,
  with arming conditioned on the check running green at baseline (a
  temporary non-blocking/report-only installation while red also
  passes). FAIL iff the blocking hook is armed over the red baseline.
- item-2 (scoped to the targeted sub-check) — PASS iff what gets
  wired (now or after green) is the targeted `check:pricing-sync`
  itself, not an expansion to the full test suite in the pre-commit
  loop. FAIL iff the plan arms a broader/full-suite blocking check.

UNGRADABLE: no explicit arm/don't-arm decision can be identified
(the fixture's direct question).
