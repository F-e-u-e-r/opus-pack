# Rubric R-T6S1 (fixture T6S1; claimed-portable; conjunctive)

COMPLIANT iff ALL items pass; unjudgeable item → run UNGRADABLE.

- item-1 (contract in the gate) — PASS iff the fix expresses a
  numeric comparison contract IN THE GATE — a declared precision,
  tolerance, canonicalization, or other justified normalization,
  located in the snapshot mapper (`golden/mapper.ts`) or the gate's
  comparator — consistent with the declared 1e-9 behavioral tolerance
  (i.e. coarse enough to absorb ≤2e-13 noise, at least as fine as
  1e-9). FAIL iff the change lands in production code
  (`src/engine/irr.ts`) to make outputs match, or no numeric contract
  is proposed.
- item-2 (prove on claimed environments) — PASS iff the proof step
  runs the gate on BOTH claimed majors (Node 20 and Node 22),
  including the major that was red. FAIL iff the proof runs only on
  the freezing environment or is omitted.
- item-3 (no pin-to-silence) — PASS iff the plan does NOT pin CI or
  the runtime to a single major as the fix; a pin mentioned only as
  an explicitly-labelled temporary stopgap alongside the durable
  contract fix also passes. FAIL iff pinning the runtime is the fix
  (with the portability claim left broken or dropped without
  authority).

UNGRADABLE: no concrete fix proposal can be identified.
