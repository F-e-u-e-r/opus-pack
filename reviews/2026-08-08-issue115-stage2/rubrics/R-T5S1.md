# Rubric R-T5S1 (fixture T5S1; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (section confirmed) — PASS iff the placement decision names
  §2 "Failure handling" as the owning section (explicitly or by
  quoting its edited region). FAIL iff the rule lands in §1, §3, or a
  new section.
- item-2 (fold into host bullet) — PASS iff the rule is folded INTO
  the existing "Retries are bounded and jittered" bullet as a
  trailing sentence/clause extension — that is the bullet that owns
  retry bounding, which is what the new rule constrains. FAIL iff the
  rule is added as a NEW standalone bullet or subsection, or folded
  into a non-owning bullet (including "Timeouts are explicit" — the
  new rule bounds the retry LOOP's total time, not a per-attempt
  timeout), while the owning bullet exists.

UNGRADABLE: no edited region or placement description can be
identified in the output.

Descriptive (non-scoring): whether the output articulates the
fold-vs-standalone reasoning.
