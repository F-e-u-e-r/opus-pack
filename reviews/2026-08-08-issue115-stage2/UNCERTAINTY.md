# Issue-115 STAGE-2 uncertainty ledger

Inherited from the sealed STAGE-1 §I (all still binding): 0-tool
single-turn fixtures measure stated decisions, not enacted multi-step
behavior; results bind to the executor tier and these fixtures; the
fixture author maintained/folded T6 and T7's clauses (mitigated by the
gates, not eliminated); label-stripping is procedural, not true
blinding — the pre-frozen binary rubric is the load-bearing control;
single adjudicator, hypothesis-aware, UNGRADABLE-not-discretion;
T5-S2's two-part criterion is conservative evidence of re-reading;
saturation at the executor tier says nothing about stronger tiers;
the per-arm UNGRADABLE distribution is published because
UNGRADABLE-as-data can depress a treatment arm's score.

STAGE-2-specific additions:

1. Rubric operationalization is itself an interpretive artifact: the
   per-item PASS/FAIL definitions in rubrics/ compress the sealed
   checklists into binary tests; a residual judgment margin survives
   inside individual items (e.g. what counts as "citing the
   registration record"). The margin is bounded by
   UNGRADABLE-not-discretion but not zero.
2. R-T4S1 relies on the executor demanding on-environment
   reproduction without requiring bash-internals knowledge; the
   grader note in that rubric records the known behavioral divergence
   (bash 3.2 aborts rather than silently passing) so graders do not
   penalize either reading of the mechanism.
3. The T1 fixture's REGISTRY excerpt models the #152 registration
   contract in miniature; fidelity to the full production semantics
   (e.g. revocation-on-live-use) is out of fixture scope and remains
   unprobed by this campaign.
4. The state machine is reviewed statically (invariant checks, three
   lenses) but has never executed; a latent transition gap would
   surface as a HOLD at run time, fail-closed by construction, but
   the absence of such gaps is asserted by review, not by execution.
5. The dry-run's identity confirmation is the only behavioral
   invocation that precedes evidence collection; between STAGE-2
   sign-off and campaign start the executor's platform may drift in
   ways config inspection cannot see. The dry-run receipt at campaign
   start is the detection point (a mismatch → HOLD before any smoke).
6. Counterbalancing removes the fixed arm↔position correlation but
   n=3 per arm cannot estimate, only bound, residual order effects;
   no order-effect statistic will be computed (preregistered
   omission, budget-bound).
