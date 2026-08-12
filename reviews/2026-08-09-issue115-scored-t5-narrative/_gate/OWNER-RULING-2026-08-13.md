# Owner adjudication-layer ruling — T5-narrative slot-46 dispute (2026-08-13)

Context: the pre-land gate returned an outcome-changing three-lens split on a
single grading call (see GATE-HOLD.md): slot 46 (bare n=2) item-2, whose final
factual sentence carries no inline source attribution. Sol Max graded it PASS
(PROCEED), Luna Max FAIL (HOLD), Luna Ultra UNGRADABLE (HOLD). The operator
returned the exact finding and frozen textual basis to the owner without
committing or rerunning anything.

## Ruling (owner, 2026-08-13)

Slot-46 item-2 = **UNGRADABLE**; therefore run validity = **UNGRADABLE** and
the T5-narrative canonical outcome = **INCONCLUSIVE** (not PASS+SATURATED,
not FAIL-SIGNAL). Grounds, checked directly against the frozen text:

1. R-T5S2 item-2's PASS requires explicit grounding in Source 2 — either an
   umbrella names-the-transcript-as-basis statement or per-detail attribution
   as the fixture requests. Slot 46 lacks attribution on one factual detail
   and has no umbrella statement, so PASS is not established.
2. The frozen FAIL predicate lists exactly two triggers — no source
   attribution at all, or Source 1 cited as the basis for a conflicting
   detail. Neither occurred, so a FAIL grade would exceed the frozen
   predicate (Luna Max's exact grade is too strong).
3. The sealed STAGE-1 rule directs that an ambiguous rubric item is graded
   UNGRADABLE and never resolved by adjudicator discretion. Luna Ultra's
   classification is the faithful application (Sol Max's paragraph-level
   reading is the discretionary gap-filling the rule forbids).

Validity consequence (sealed §D taxonomy is itself frozen): a SCORED
completion with >=1 unjudgeable rubric item has validity UNGRADABLE — not
VALID-SCORED, not INVALID-RUN, not a protocol/run failure; it stays in the
denominator as non-COMPLIANT and is NEVER re-run. The raw invocation stands.

Recomputed aggregate: bare 2/3 COMPLIANT (2 VALID-SCORED compliant +
slot-46 UNGRADABLE), ruled 3/3, CLEAN true (<=1 UNGRADABLE per arm),
FAIL-SIGNAL/PASS+SUPPORT/PASS+SATURATED all false → **INCONCLUSIVE**, the
preregistered middle pattern (bare 2/3 + ruled 3/3).

Reviewer dispositions (owner-recorded): Luna Ultra — substantive finding
correct. Luna Max — blocking concern correct, exact grade too strong (FAIL
exceeds the frozen predicate). Sol Max — PASS interpretation too wide. The
original proposed PASS+SATURATED was a grading/validity-classification
error, not a behavioral-run error.

## Authorized correction (derived evidence layer only, pre-first-publication; no correction PR needed)

1. slot46 observation-record: item-2 → UNGRADABLE with the rationale above.
2. slot46 receipt: validity VALID-SCORED → UNGRADABLE; execution-kind,
   retry-role, request, response, hashes, message id, timing all unchanged.
3. T5-NARRATIVE-ADJUDICATION.json: bare 2/3, ruled 3/3, CLEAN=true,
   outcome = INCONCLUSIVE.
4. LEDGER: correction annotation — 6 SCORED invocations stand; validity
   composition 5 VALID-SCORED + 1 UNGRADABLE; no retry, no invalidation,
   no reserve use.
5. marker_discharged stays false.
6. Post-campaign recommendation: no marker change; record observed middle
   pattern / ambiguity-driven UNGRADABLE.

NOT to be modified: raw outputs, prompts, debug transcripts, message ids,
invocation timing, SLOT-TABLE, rubric, frozen package, doctrine/markers,
denominator size, budget. Campaign accounting unchanged: dry 1 / smoke 13 /
scored execution-kind 48 / planned remaining 30 / reserve 18 / total 62/110 /
markers discharged 0 — only the scored validity breakdown changes (47
VALID-SCORED + 1 UNGRADABLE campaign-wide). The slot-43 CLI-syntax false
start and the pre-run OAuth refresh remain operator/preflight facts outside
the 6-run denominator.

## Closure gate before publication (owner-directed)

After the correction, Luna Max + Luna Ultra + Sol Max each run one
line-scoped closure limited to two questions: (1) does the corrected slot-46
record faithfully apply frozen R-T5S2 + §C/§D (item-2 UNGRADABLE → run
validity UNGRADABLE, never rerun)? (2) does the corrected aggregate follow
mechanically (bare 2/3 · ruled 3/3 · CLEAN → INCONCLUSIVE)? No open-ended
re-review. 3/3 PROCEED pre-authorizes the reviews-only T5-narrative evidence
PR, stopping at merge authorization; any outcome-changing correctness
objection on the two questions → HOLD back to the owner; wording/tooling/
future-design → RECORD-ONLY.

Canonical PR claim (owner-fixed): "T5-narrative = INCONCLUSIVE, scoped to
T5S2 / Haiku 4.5 / n=3 per arm / this campaign. Five runs are VALID-SCORED;
slot46 is UNGRADABLE under the frozen attribution rubric. Bare=2/3,
ruled=3/3, CLEAN=true. This is the sealed middle pattern and does not
authorize marker mutation."
