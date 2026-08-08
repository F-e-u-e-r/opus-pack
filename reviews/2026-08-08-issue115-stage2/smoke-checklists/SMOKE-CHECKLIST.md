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

Failure handling is fixed by the state machine: an item-3 failure (or
an item-1/2 failure with a clean invocation) evidences an objective
fixture defect → repair-gate (max one per fixture; re-smoke fail →
automatic retirement). A transport/protocol failure is INVALID-RUN
semantics on a smoke: one rerun, second → HOLD(campaign).
