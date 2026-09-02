# Round 2 (gate) adjudication — codex gpt-5.6-sol (inlined, read-only) + Fable 5.1 (fresh-context subagent, packet-only)

Pre-registered: `../EXPECTED-r2.md`. Predictions 1, 2 and 5 landed (obligation (2) wording,
the "measured or weakened" clause, and the agreement-as-corroboration lean in row 3); 3, 4, 6
did not. Both verdicts re-derived from the packet before any edit. Both FIX; last lines agree
with bodies.

| # | Finding | Reproduced? | Disposition |
|---|---|---|---|
| 1 | excluding cited counterexamples does not establish the qualified claim over its retained scope; vacuous when the finding cites none (sol F1 High, Fable F1 Med) — CONVERGED | yes — README round-1 row 2 is an over-claim with no counterexample | **fixed**: heading and test now bound the qualified claim by the measurement AND require counterexample exclusion; done-when names the bounding measurement |
| 2 | "two repairs exist" is a false exhaustive (sol F2 Med) | yes | **fixed**: "substantiate the wider claim — by a probe where the claim is empirical — or retract" |
| 3 | measuring every noun does not establish the relation ("ran from") — the incident's actual defect; sound inference from sufficient indirect observations is allowed (sol F3 High) | yes | **fixed**: rule re-based on observations SUFFICIENT for each entity and relation vs proxies merely consistent; ✅/❌ name the relation |
| 4 | "true only inside the fixture" false; "every forced condition" over-broad (sol F4 Med, Fable F5 Med) — CONVERGED | yes — README: "in the wild an unchanged source or a forged header does the same" | **fixed**: "establishes the claim only under that condition"; "every forced condition material to the mechanism" |
| 5 | overlap with the check's-name bullet; "one level deeper" mis-states the distinction (sol F5 Med, Fable F7 Med) — CONVERGED | yes | **fixed**: distinction restated as coverage-of-a-property vs sufficiency-for-the-printed-line; "read the code that emits it" dropped |
| 6 | drill sentence still an unsupported historical assertion (sol F6 Low, Fable F10b Low) | yes | **fixed**: deleted (third round raising it) |
| 7 | house convention / #115 queue / trail path / marker counts / PR number not derivable from the packet (sol F7 Low, Fable F10a,c) | n/a — [unverified] by construction | **rejected-with-reason**, with evidence recorded here: `grep -c "standing #115 queue" skills/operational-rigor/SKILL.md skills/cross-model-review/SKILL.md` on the tree; PR #233 = upstream merge `a51396d`; the trail directory is in this commit. Context A itself cites "PR #30" in rule text, the house form |
| 8 | neg quotes a paraphrase inside quotation marks (Fable F2 Med) | yes — README row 1 wording differs | **fixed**: verbatim |
| 9 | "the repair that held" asserts scrutiny the trail lacks (Fable F3 Med) | yes | **fixed**: "the repair recorded in round 2" |
| 10 | "an inference prints the right answer for the wrong reason" is the same rhetoric class as the deleted sentence (Fable F4 Med) | yes | **fixed**: replaced with the operational form (can print the line while the relation never held) |
| 11 | three imperatives labelled two; done-when does not cover (2) or the capture requirement; "rule text the probe supports" reaches into authoring (Fable F6 Med) | yes | **fixed**: three obligations, done-when covers all three; "any claim the probe is cited to support" keeps it a verification duty |
| 12 | "the other condition alone" presumes two conditions (Fable F8 Low) | yes | **fixed**: "remaining conditions" |
| 13 | Provenance attributes the bad line to the checked-in probe, which is the rewrite; quote not verbatim (Fable F9 Low) | yes | **fixed**: "the first revision of the probe"; quote aligned to README |
| 14 | neg and Provenance narrate the same sequence twice (Fable F11 Low) | yes | **fixed**: neg cut to the failure shape; narrative kept in Provenance |
| 15 | "repaired nothing" over-states partial exclusion (Fable F12 Low) | yes | **fixed**: "changed the sentence without closing the finding" |
| 16 | row 8's "marked … unconfirmed" is not the README's framing (Fable, folded into F10) | yes | **fixed**: "as lacking checked-in evidence" |

Round-1 dispositions re-checked by the reviewers: rows 1, 2, 3, 7 NOT CONFIRMED by sol — each
is the subject of a row above and re-fixed; rows 4, 5, 6, 8, 11 CONFIRMED by both.

Remedies authored here. sol's F1 remedy ("evidence warranting the claim over the retained
scope") was re-based on the pack's measured-claim vocabulary; sol's F3 remedy was adopted in
substance (sufficiency vs consistency) with the pack's own examples; Fable's F1 and F6 fixes
were close to what landed and were judged against the full paragraph before landing. Two
reviewers agreeing on rows 1, 4, 5 raised their priority in my queue, not their status —
each was re-derived.
