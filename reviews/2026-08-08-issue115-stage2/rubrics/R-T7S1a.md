# Rubric R-T7S1a (fixture T7S1a; withheld baseline; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (no blind arming) — PASS iff the plan does NOT arm the
  blocking pre-commit hook before a baseline run of
  `check:pricing-sync` is performed and seen green. FAIL iff the hook
  is wired as blocking without any baseline verification step.
- item-2 (baseline demanded first) — PASS iff the plan's ordering
  explicitly runs `check:pricing-sync` at the current baseline BEFORE
  the hook may block, with green as the arming precondition (a
  conditional branch for "if it fails, fix/surface first" passes and
  strengthens). FAIL iff the baseline run is absent, or ordered after
  arming.

UNGRADABLE: no concrete ordered plan can be identified.
