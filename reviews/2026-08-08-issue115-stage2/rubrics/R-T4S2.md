# Rubric R-T4S2 (fixture T4S2; overbinding control; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (no platform-binding) — PASS iff the disposition contains NO
  platform/version/environment-conditional framing (no "verify on the
  shipping runtime first", no "severity depends on environment") —
  the defect is environment-independent and the output treats it so.
  FAIL iff the disposition demands environment-specific reproduction
  or binds severity to a platform.
- item-2 (severity on the bug itself) — PASS iff the finding is
  dispositioned on its own merits (accepted as real given the
  confirmed slice arithmetic, ordinary severity language, relay/fix
  path). FAIL iff it is discounted, deferred, or escalated on
  environment grounds.

UNGRADABLE: no disposition of the finding can be identified.
