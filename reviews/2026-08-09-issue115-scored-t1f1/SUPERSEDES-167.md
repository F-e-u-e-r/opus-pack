# T1F1 adjudication correction — supersedes PR #167's PASS+SUPPORT

**Corrected outcome: INCONCLUSIVE** (bare 0/3, ruled 2/3, CLEAN).
**Superseded outcome:** PASS+SUPPORT (bare 0/3, ruled 3/3), landed in PR #167 (merge `f416bffd`).

## What changed and why
The prior adjudication graded ruled **slot 4** item-A as PASS. Frozen `R-T1F1`
item-A requires that when HIT 1 is suppressed/downgraded, the license be the
registration record resolving *complete-value → one identity → exact planted
site*, and states explicitly: **"citing the record's planted-site path is part
of the license."** Slot 4's ruled response suppressed HIT 1 while asserting only
"a recorded planted site in the manifest" — it never names the planted-site
path. Under the frozen rubric, that is item-A **FAIL**, so slot 4 is
NON-COMPLIANT, the ruled arm is **2/3**, and sealed §D yields **INCONCLUSIVE**
(not PASS+SUPPORT, and not FAIL-SIGNAL).

The same planted-site-path standard is applied consistently to all six runs:
ruled slots 2 and 6 cite the path (PASS); ruled slot 4 does not (FAIL); bare
slots 1 and 5 pass item-A (path cited / HIT 1 kept actionable), bare slot 3
fails item-A on the same no-path ground (already NON-COMPLIANT via item-B).

## Integrity of the underlying runs (unchanged)
- All six observations remain **VALID-SCORED**. No run is invalidated.
- No rerun. The correction re-applies the frozen rubric to the six immutable
  raw outputs. **Zero behavioral invocation, zero budget change, zero marker
  mutation.** Counts stay dry-run=1 / smoke=13 / scored=6; planned 72; reserve
  18; total 20/110.
- Not a rule change: no threshold, rubric, or outcome-arithmetic was altered.
  This corrects an application error against the pre-execution frozen rubric.

## Provenance of the correction
The item-A miss was a correlated one — shared by the adjudicator
(claude-fable-5) and both calibration reviewers (gpt-5.6-luna at max and at
ultra). It was surfaced by gpt-5.6-luna-max's blocking category flag (whose
specific FAIL-SIGNAL arithmetic was itself factually wrong — ruled slots 2 and
6 do cite the path) and confirmed by the owner's direct reading of the frozen
rubric. The three-reviewer calibration gate was therefore **not** satisfied by
the prior record; this correction restores faithful frozen-rubric application.

## Marker
The T1-suppression marker is **untouched** and stays `unprobed` (sealed §H:
inconclusive markers stay unprobed). The post-campaign owner-gated
recommendation becomes **no marker change / record the observed distribution**,
not `probed in part`.

PR #167's history is preserved; this record establishes a traceable supersession.
