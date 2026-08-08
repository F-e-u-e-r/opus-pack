# Issue-115 STAGE-2 — SEAL RECORD

STAGE-2 SEALED 2026-08-08 under the owner's structural-simplification
ruling (option b): the three autonomous exception lifecycles were
demoted to owner-mediated fail-closed paths, the four residual
mechanical items were closed, and a scope-limited three-lens closure
review reached all-PROCEED on the frozen tree. No r7 was run, per the
same ruling.

## Sealed identity

- Package: `issue115-stage2-v1`
- Sealed content commit: `db09c2d` (branch `issue115-stage2-package`;
  baseline main `fac48c20…`)
- MANIFEST.sha256:
  `25700fd5bce2b07bbf5e89e9080bb0777acafea7a8282b081e7ac3c24972e860`
- STAGE-1 contract: `PREREG-v6-SEALED.md` sha256 `2c7e3f21…` (sealed
  earlier the same day; unchanged throughout STAGE-2)
- This seal record and `OWNER-APPROVAL.json` live OUTSIDE the
  manifest's hash set by design (self-reference avoidance; RUNBOOK 3).

## What sealed means here — and what it does not

SEALED = the package design is frozen and review-complete. It does
NOT authorize execution. Still owed, in order, both owner acts:
1. `OWNER-APPROVAL.json` signature binding this exact package id +
   MANIFEST.sha256 (status is deliberately left
   `PENDING-OWNER-APPROVAL`; no one signs it for the owner);
2. the owner's explicit run authorization (state row 1).
Behavioral runs executed to date: 0 — no dry-run, no smoke, no
scored run.

## Closure-gate trail (all verdicts in this session's scratchpad,
`stage2-closure/`, retained as audit evidence)

- v6 revision (commits `a900a14` + `d0b138f`): lifecycles deleted
  (former rows 10/11, 23a–23c, 24, 27c), owner-mediated rows
  7b/23/23b/27b added, package version model replaced the amendment
  chain, TERMINAL-WRITE GUARD gained the sealed drift-precedence
  exception, GLOBAL FREEZE RULE added, four residuals closed
  (cancellation extinction; completion-status receipt field; DRY-RUN
  N/A binding; I1–I8 checker).
- Closure round on `d0b138f` (scope-limited per the owner's ruling):
  luna-ultra PROCEED (0 findings — fidelity + semantics preserved);
  luna-max FIX 1,2,3 (retry liveness fence; post-event receipts vs
  outcome arithmetic; missing ADJUDICATION-INTERRUPTED row);
  sol-max FIX 1,2,3,4 (gates outside the freeze set; DRY-RUN clean
  identity-failure routing; sentinel sweep false claim; unicode
  sweep gap U+2061–2064).
- Fix commit `43f9f77` (all seven, fail-closed remedies only; sweeps
  proven able to fail two-sidedly).
- Confirmation on `43f9f77`: sol 4/4 CLOSED, PROCEED; ultra 0
  findings, PROCEED (explicitly: default-excluded + owner-adopted
  post-event receipts are semantics-preserving); max 1–2 CLOSED,
  FIX 3 v2 (ABANDON left completed R-slots poolable).
- Fix commit `db09c2d` (ABANDON voids completed R-slots,
  ABANDONED-UNIT annotation — original set or complete replacement
  unit, never a mixture).
- Re-confirmation on `db09c2d`: max finding 3 CLOSED, pooling replay
  found no path, PROCEED.
- Seal-rule check: owner-mediated demotion held by all lenses; four
  residuals closed; static checks (34) + repo gates green at
  `db09c2d`; three lenses all-PROCEED in scope. No finding asked to
  re-mechanize an autonomous lifecycle; none impeached the 92-slot
  main path.

## Standing constraints carried forward

The operational principle (owner-ruled) binds every future edit:
rare exception paths that change evidence eligibility, rerun
entitlement, or artifact identity are fail-closed to owner
adjudication rather than autonomously repaired by the campaign state
machine. Any artifact change from here is a NEW package version
(new id + regenerated manifest + fresh owner approval receipt +
re-gate of the affected scope); this sealed version stays immutable
on the record.
