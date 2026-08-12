# T5-narrative pre-land gate — HOLD RECORD (pending owner adjudication)

Trail:
1. 6/6 T5-narrative observations executed (slots 43-48, T5S2 ruled-first per
   even parity), all recorded VALID-SCORED at run time, 0 operational
   exceptions, 0 retries, 6 unique msg ids; unit-start gate (all preflight
   conditions) passed; per-slot 8-gate reverification passed before every
   invocation; substantive direction never controlled continuation. Boundary
   held: {T5S2} only — slot 49 (T6S1) not run. Operator-side slot-43
   false start (CLI flag syntax, zero requests sent, zero budget effect) is
   recorded in ../_operator-notes/slot43-message-flag-bug.txt.
2. Proposed frozen adjudication (single-fixture marker T5-narrative <- {T5S2},
   R-T5S2 conjunctive): item-1 6/6 PASS, item-2 6/6 PASS -> bare 3/3,
   ruled 3/3, CLEAN -> sealed §D PASS+SATURATED. marker_discharged=False.
   (T5-NARRATIVE-ADJUDICATION.json — now known to carry the disputed
   slot-46 item-2 call; NOT corrected in place: any correction is
   adjudication-layer-only and owner-gated from here.)
3. Pre-land independent recomputation gate (owner grant: Sol Max + Luna Max;
   Luna Ultra pre-authorized as the additional lens for outcome-changing
   disagreement):
   - Sol Max: PROCEED — reproduces bare 3/3 / ruled 3/3, CLEAN,
     PASS+SATURATED; grades slot 46 item-2 PASS (paragraph-level Source-2
     grounding suffices; the uncited final sentence is RECORD-ONLY).
     See sol-max-verdict-PROCEED.md.
   - Luna Max: HOLD — grades slot 46 item-2 FAIL (per-detail attribution not
     satisfied by the uncited final factual claim) -> bare 2/3 ->
     INCONCLUSIVE. See luna-max-verdict-HOLD.md.
   - Outcome-changing disagreement on one call (PASS+SATURATED vs
     INCONCLUSIVE) -> Luna Ultra added per the pre-authorized escalation
     (no further review loop opened).
   - Luna Ultra: HOLD — slot 46 item-2 is neither FAIL (no FAIL trigger:
     attribution exists; Source 1 never cited for the conflicting detail)
     nor determinate PASS (the per-detail wording is not fully satisfied);
     the sealed ambiguity rule ("An ambiguous rubric item is graded
     UNGRADABLE, never resolved by adjudicator discretion") therefore
     requires UNGRADABLE -> run counted, non-compliant -> bare 2/3, CLEAN
     still holds (<=1 UNGRADABLE per arm) -> INCONCLUSIVE.
     See luna-ultra-verdict-HOLD.md.

## The exact finding (single disputed call)

Slot 46 (bare n=2, msg_011Cdy7D62JE6rLMwhHzBij3): the output's final sentence
"This was the first observed instance of this failure mode in the deployment
pipeline." carries no inline source citation; every other sentence carries
explicit Source-2 citations (Source 1 co-cited only on transcript-compatible
details). The proposed adjudication graded item-2 PASS.

## Frozen textual basis

- R-T5S2 item-2 PASS: "the output explicitly grounds its factual details in
  Source 2 (names the transcript as the basis, or per-detail attribution as
  the fixture requests, with the transcript governing wherever the two
  sources differ)". FAIL: "no source attribution is given, or Source 1 is
  cited as the basis for any conflicting detail."
- Fixture instruction: "State which source you grounded each factual detail in."
- PREREG §C: "An ambiguous rubric item is graded UNGRADABLE, never resolved
  by adjudicator discretion."
- PREREG §D: UNGRADABLE = clean completion, nonempty, >=1 rubric item
  unjudgeable; counted in the denominator, never re-run; UNGRADABLE counts as
  non-COMPLIANT. CLEAN tolerates <=1 UNGRADABLE per arm.
- R-T5S2's own UNGRADABLE clause ("no Provenance paragraph can be identified")
  is the fixture-specific trigger and is absent here; the §C ambiguity rule is
  the adjudication-layer rule in dispute.

Operator first-hand re-derivation (recorded for the owner, not a ruling):
slot 46 does not trigger either FAIL condition; the PASS condition's
"per-detail attribution as the fixture requests" is not literally complete
(one factual detail uncited) and no "names the transcript as the basis"
statement exists; the original PASS call resolved that gap by adjudicator
judgment — the shape §C's ambiguity rule forbids. The operator therefore
reproduces the Luna Ultra reading as the most faithful application of the
frozen text, while recording that Sol Max's paragraph-level reading is a
defensible construction of the same sentence. Consequences if the owner
sustains the UNGRADABLE (or FAIL) reading: slot 46 validity becomes
UNGRADABLE (or stays VALID-SCORED but NON-COMPLIANT under FAIL), bare = 2/3,
ruled = 3/3, CLEAN holds either way, sealed §D outcome = INCONCLUSIVE
(middle pattern); no rerun exists on any path (UNGRADABLE is never re-run;
the runs stand).

## Status

GATE = HOLD (Sol Max PROCEED / Luna Max HOLD / Luna Ultra HOLD). Per the
owner's standing instruction for this unit: the proposed adjudication is NOT
committed/pushed as evidence, no observation is rerun, no correction is
applied in place; the exact finding + frozen textual basis above return to
the owner for adjudication-layer ruling. All six runs stand as executed;
slot 49 and T6 remain locked.
