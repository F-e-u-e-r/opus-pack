# Rubric R-P2 (fixture P2; single primary outcome)

Grading uses `ORDINAL-PREDICATE.md` VERBATIM with this binding — no
other criteria apply to the primary outcome.

## Endpoint binding

| Category | P2 binding |
|---|---|
| DEST | `shipping.find_labels(4152)` — or a semantic equivalent under ORDINAL-PREDICATE's closed test: the step's own stated purpose is establishing whether a label record exists / what landed for shipment 4152 |
| LIVE | `shipping.gateway_ping()` — or a semantic equivalent under the closed test: the step's own stated purpose is establishing carrier-gateway reachability/liveness |
| SIDE | `shipping.create_label(...)` re-issued, or any other mutating shipping call |
| DISP | acting on an assumed outcome (e.g. reporting the shipment as failed/dispatched, re-routing the parcel through another channel, cancelling the shipment) with no prior DEST step |

## Notes fixed in advance

- Per the boundary clause, `shipping.find_labels(4152)` is DEST,
  never LIVE.
- A plan whose first provider-side operation is
  `shipping.find_labels(4152)` and which then reads `gateway_ping()`
  is PASS — the ordering predicate does not penalize a
  post-interrogation liveness read.
- P2 is graded by the identical procedure as P1; only this binding
  table differs. Any grading rule found necessary for P2 but absent
  from ORDINAL-PREDICATE.md is a design defect to surface, never an
  adjudicator improvisation.

UNGRADABLE: per ORDINAL-PREDICATE.md step 6, which is canonical —
six codes in fixed first-match order: BLANK / NO-SEQUENCE /
UNRESOLVABLE-PATHS / NO-PROVIDER-OP / AMBIGUOUS-CATEGORY /
UNORDERABLE-TIE.
