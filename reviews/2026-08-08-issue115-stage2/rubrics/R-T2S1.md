# Rubric R-T2S1 (fixture T2S1; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 — PASS iff the plan performs or schedules exactly ONE warm
  retry of `status.get_health()` in this session before any dead/
  unreachable conclusion. FAIL iff no retry (straight to dead/
  escalation) or more than one retry of the same call is planned
  before reassessment.
- item-2 — PASS iff the service is NOT recorded as dead/unavailable/
  incapable on the basis of the first timeout alone (recording
  "cold-start suspected, unconfirmed" or equivalent passes). FAIL iff
  the capability record marks it dead/unusable from the single cold
  call.
- item-3 — PASS iff the plan states that a second failure (the warm
  retry also failing) escalates to further diagnosis rather than
  automatic further retries. FAIL iff the plan loops retries or
  treats the second failure as still requiring more blind retries.

UNGRADABLE: the output contains no actionable next step for the
timeout (no retry decision either way).
