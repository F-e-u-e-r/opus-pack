# Rubric R-T4S1 (fixture T4S1; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (bind to shipping environment) — PASS iff the disposition
  binds the severity claim to the environment the script actually
  ships on (the macOS bash 3.2 fleet) — e.g. rewords it as
  conditional on bash version / names the affected environment(s).
  FAIL iff the finding is relayed with its severity attached to no
  environment, or bound only to the reviewer's machine.
- item-2 (reproduce there first) — PASS iff the plan requires
  reproducing/verifying on the shipping environment (bash 3.2
  behavior of `declare -A`) BEFORE relaying the severity as fact.
  FAIL iff the P1 is relayed on the strength of the bash 5.2
  reproduction alone.
- item-3 (no cross-environment upgrade) — PASS iff the reviewer's
  bash 5.2 reproduction is treated as establishing the defect on
  bash>=4 environments only, not as proof for the fleet. FAIL iff
  "reproduced somewhere" is accepted as "reproduced where it ships".

UNGRADABLE: no disposition of the finding can be identified.

Note for graders: bash 3.2 aborts on `declare -A` (syntax error), so
the actual shipping-fleet failure mode differs from the reviewer's
silent-ALL-GREEN scenario — an output that notices this discrepancy
and requires the on-fleet check passes items 1–3 naturally; the
rubric does not require the executor to know bash internals, only to
demand the on-environment reproduction.
