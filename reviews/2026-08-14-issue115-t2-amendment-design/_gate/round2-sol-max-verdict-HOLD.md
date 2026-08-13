### (a) Round-1 discharge

1. **R1 — Partially discharged:** M1-r2 removes the first-among-all-reads overreach, but the M1 heading and disposition still describe superseded M1 as preferred and as adding no policy beyond #188.
2. **R2 — Partially discharged:** M1-r2 correctly conditions the obligation on both prerequisites, but the disposition table still claims unconditional M1 preserves the no-query branch.
3. **R3 — Discharged:** “that read-back” identifies the branch-(2) operation, while “separate” excludes it from the ordered-after liveness/status reads.
4. **R4 — Discharged:** The provenance now attributes the semantics to #188, treats E only as the control, and appropriately limits the #191 evidence.
5. **R5 — Not fully discharged:** Re-wrap, n-gram scope, T2, and branch-reading mechanics are addressed, but §5(d) still requires “all nine” carriers to remain byte-identical despite §7 correctly identifying only seven pre-existing carriers, and §5(f) inaccurately calls a paraphrased condition “verbatim-scoped.”

### (b) Equivalence

Yes—[M1-r2](/Users/ccso/Developer/fable/reviews/2026-08-14-issue115-t2-amendment-design/T2-AMENDMENT-DESIGN.md:104) is semantically equivalent to #188 in context: it orders only destination read-back relative to separate liveness/status reads, leaves unrelated provider reads unconstrained, and merely restates existing invariant 5 rather than adding policy.

### (c) New defects

No new semantic defect appears in M1-r2 itself, but adding it created a new record inconsistency: §3 says “[all three](/Users/ccso/Developer/fable/reviews/2026-08-14-issue115-t2-amendment-design/T2-AMENDMENT-DESIGN.md:65)” although four candidates are now listed; the stale [disposition table](/Users/ccso/Developer/fable/reviews/2026-08-14-issue115-t2-amendment-design/T2-AMENDMENT-DESIGN.md:142) and contradictory [nine-carrier acceptance condition](/Users/ccso/Developer/fable/reviews/2026-08-14-issue115-t2-amendment-design/T2-AMENDMENT-DESIGN.md:206) are blocking overclaims.

VERDICT: HOLD — stale M1/M2/M3 dispositions; nine-carrier byte-identity contradiction; false “verbatim-scoped” claim; candidate-count inconsistency
