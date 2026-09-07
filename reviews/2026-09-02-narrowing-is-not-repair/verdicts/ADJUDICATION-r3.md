# Round 3 (final, cap) adjudication — codex gpt-5.6-sol + Fable 5.1 fresh-context

Pre-registered: `../EXPECTED-r3.md`. Prediction 3 (measured vs substantiated mismatch) landed
as sol F1 + Fable F3; prediction 2 (elliptical consequence clause) as Fable F5; predictions
1 and 4 did not land. sol: FIX F1–F3 (+F4 Low). Fable: FIX F1 (+6 Low, shippable-with-note).
Both last lines agree with bodies. All re-derived from the packet before editing.

| # | Finding | Reproduced? | Disposition |
|---|---|---|---|
| 1 | heading/body bound the qualifier by "measurement" while the body admits non-empirical substantiation (sol F1 Med, Fable F3 Low) — CONVERGED | yes | **fixed**: "what the evidence establishes (the measurement, where the claim is empirical)" once; "that evidence" thereafter |
| 2 | obligation (3) names only command-and-output + revision evidence (sol F2 Med) | yes | **fixed**: "reproducible invocation or procedure and its captured observation, tied to the artifact and environment the claim is about" |
| 3 | done-when widens (3) from diagnostic results to every asserted result (sol F3 Med) | yes | **fixed**: "every asserted diagnostic result" |
| 4 | "weakened to what was" incomplete (sol F4 Low) | yes | **fixed**: "what was observed" |
| 5 | §3 done-when forecloses the owner-accepted deferral the preceding paragraph permits (Fable F1 Med) | yes — Context A's done-when includes deferral | **fixed**: done-when scoped to findings recorded `fixed`; deferral takes the preceding paragraph's disposition |
| 6 | Provenance "retraction to the measured claim" asserts a measurement of the digest step the trail does not show (Fable F2 Low) | yes — README probes import + cache attribute, not the digest | **fixed**: states what the text now claims instead |
| 7 | test keyed to cited, not reproduced, counterexamples (Fable F4 Low) | yes | **fixed**: "every reproduced counterexample the finding cites" |
| 8 | "or the claim asserts the remaining conditions alone" elliptical/ambiguous (Fable F5 Low) | yes | **fixed**: "— unnamed, the claim is read as asserting that the remaining conditions alone suffice" |
| 9 | done-when covers (2) only for the line, not the cited claim (Fable F6 Low) | yes | **fixed**: done-when names both |
| 10 | residual overlap of "unbacked term … weakened" with the check's-name bullet (Fable F7 Low) | yes, tolerable | **rejected-with-reason**: the distinguishing sentence carries the difference; reviewer itself marks no fix required |

**Round cap reached (cross-model-review §4).** The text after these edits has NOT been
reviewed by any reviewer; the edits are wording-scope, each a single clause, each authored
against the full paragraph. Recorded as the shipped gap rather than opening a round 4.

Round-3 verdicts on round-2 rows: Fable CONFIRMED 12, PARTIAL 2 (rows 9, 11 — both re-fixed
above), NOT CONFIRMED by construction 2; sol: all packet-rederivable rows reflected.
