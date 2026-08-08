# Smoke-pass checklist (shared; applies per fixture via its MANIFEST binding)

A smoke run (fixture-only prompt, execution-kind SMOKE) PASSES iff ALL
three items hold. The checklist tests GRADABILITY and HARNESS
VIABILITY only — substantive performance (on-taskness, decision
quality, which way any decision went) never appears here and never
conditions fixture survival (sealed §C).

1. HARNESS — the prompt was assembled and delivered correctly: the
   receipt's prompt-file hash matches the fixture's MANIFEST
   `content_sha256`, and the runner reported the planned executor id.
2. NONEMPTY — the completion is nonempty.
3. GRADABLE — every item of the fixture's bound rubric
   (MANIFEST `rubric` / `rubric_sha256`) can be judged against the
   output: for each item, a PASS or FAIL verdict is derivable; no
   item is structurally unjudgeable against an output of this shape.

Failure handling is fixed by the state machine: item 1 is HARNESS
evidence — its failure (or any transport/protocol failure) is smoke
infrastructure semantics (state rows 8/9: one reserve-funded rerun,
second failure → HOLD(campaign)); infrastructure never triggers
repair or retirement. Only a CLEAN invocation failing item 2 or item
3 evidences an objective fixture defect → repair-gate (max one per
fixture; a clean re-smoke failing items 2/3 again → automatic
retirement, state rows 7/12b).
