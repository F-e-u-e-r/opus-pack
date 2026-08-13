# T2 doctrine-amendment DESIGN gate — CLOSURE RECORD

Scope: design/compare/seal a proposed minimal semantic delta for the
uncertain-outcome rule; NO canonical file modified; behavioral
invocations 0; headroom 11 + old reserve 18 untouched; #115 OPEN;
T2 marker untouched.

Trail:

1. Target fresh-read from main `327b264` (blob `28216fd8…`,
   uncertain-outcome entry frozen byte-exact); amendment contract
   locked to "smallest wording change making the settled
   STRICTLY-ORDINAL requirement explicit"; nine untouchable
   invariants declared; three candidates authored (M1 minimal
   two-sentence per the grant's preferred semantics; M2 short form;
   M3 E-derived subset) with per-axis dispositions; machine checks
   (byte pin, scratch patch simulation, invariant carriers,
   E-similarity n-gram guard) built and green.
2. Round 1 (Luna Max + Sol Max, independent, verdicts not shared):
   **HOLD × 2, convergent on the same root cause** — "the first
   provider-side read" in M1 (and its analogues in M2/M3)
   OVEREXPRESSES the #188 ruling, which orders destination
   interrogation before liveness/status reads only, not before all
   provider-side reads; the unconditional first sentence collided
   with the no-query branch (one reviewer adding: the condition must
   also carry the request-identity prerequisite); the keyed-read vs
   liveness-read boundary was ambiguous where sentence two dropped
   its qualifier. Each reviewer proposed a corrected wording;
   semantically aligned → synthesized as **M1-r2** (no Ultra needed:
   convergence, not disagreement):
   "Where the destination can be queried under the request identity,
   that read-back precedes any separate provider-side liveness/status
   read — and a liveness/status read never substitutes for
   destination-state evidence."
   Also adopted: provenance rewording ("implements #188's settled
   semantics; the E-arm served only as the experimental control"),
   a byte-exact one-line-for-six-lines patch with NO re-wrap
   latitude, carrier-count correction (seven pre-existing + two
   carried by the insertion), n-gram-guard scope honesty, and two
   future-mutation-gate obligations (T2-marker byte-check;
   no-query/no-identity reading line-check).
3. Round 2: **both reviewers confirmed M1-r2 semantically EQUIVALENT
   to #188 (no weaker, no stronger)**; HOLDs narrowed to record
   consistency (stale M1/M2/M3 disposition rows, the nine-vs-seven
   carrier contradiction, a false "verbatim-scoped" label, a
   candidate-count slip). All four reproduced and fixed; M1-r2
   wording unchanged.
4. Round 3 (focused, final bounded round): **PROCEED × 2** — all
   fixes discharged, no new defects, machine checks 22/22.

STATUS: GATE CLOSED (2/2 PROCEED at round 3 of the ≤3-round bound).
The recommended amendment is **M1-r2** with the §5 byte-exact patch
and the §5 mechanical acceptance list (a)–(f) binding the future
mutation gate. This closure changes no canonical file: applying the
patch to `external-systems.md` is the NEXT owner gate.
