# Round 1 adjudication — codex gpt-5.6-luna (inlined packet, read-only) + grok-4.6 (isolated HOME, staged file, read-only tools)

Pre-registered expectations: `../EXPECTED-r1.md` (written before either verdict was read).
Both verdicts were reproduced by my own re-derivation from the packet before any edit.

**luna's verdict is self-contradicting** — body opens "Verdict: FIX. Findings: F1–F7" and the
required last line is `PROCEED`. Per cross-model-review §5 that is not a confirmed PROCEED;
it is treated as FIX and its findings are adjudicated on merit. grok: `FIX F1,F2,F3,F4,F5,F8`.

| # | Finding (luna / grok) | Reproduced? | Disposition |
|---|---|---|---|
| 1 | heading "never by narrowing" contradicts the body's qualifier exception (luna F1+F3 High, grok F1 High) — CONVERGED | yes — same paragraph | **fixed**: heading now states the condition itself: "a scope qualifier repairs an over-claim only when the counterexamples fall outside it"; the two repairs (measure / retract) stated without "never" |
| 2 | fixture-forces-a-condition clause is a distinct rule smuggled into §3; grok adds it misstates the incident (nobody narrowed a fixture) (luna F2 Med + F6 High, grok F2 High) — CONVERGED; predicted #1 | yes | **fixed**: removed from §3; re-authored as obligation (2) of the op-rigor §4 rule with its own done-when and ✅/❌ mention |
| 3 | op-rigor rule paraphrases the check's-name bullet (luna F4 Med; grok axis 2 explicitly disagrees) | in part — the "read the code that emits it" sentence overlaps trace-to-oracle | **fixed in part**: added the explicit distinction ("one level deeper — the oracle's own printed line"); kept the every-noun test, which the neighbour does not own. Remainder **rejected-with-reason**: the neighbour governs a cited check's coverage, this governs a harness's own verdict computation — grok's derivation matches mine |
| 4 | "wrong in the direction of its author's belief" is rhetoric / not generally true (luna F5 Low + F12 Low, grok F8 Med) — CONVERGED; predicted #5 | yes | **fixed**: deleted; replaced by the operational statement (a broken search and an empty location look the same) |
| 5 | portability: `-S`, `__pycache__`, `/var` vs `/private/var` in rule text (luna F7 Med, grok F3 High) — CONVERGED | yes | **fixed**: all removed; examples now in the ✅'s own register (in-tree cache directory, module's cache attribute, diagnostic result) |
| 6 | ❌ and Provenance cite a path-resolution bug the trail does not record (luna F8 Med + F11 Med, grok F4 High) — CONVERGED; self-found before verdicts (EXPECTED-r1 §self-found) | yes — `grep realpath` on the 08-31 README: 0 hits; the harness has a comment only | **fixed**: ❌ rewritten to the trail's actual proxy inference; bug claim removed from Provenance |
| 7 | private doctrine drill sentence in Provenance is uncheckable (luna F9 High, grok F5 Med) — CONVERGED | yes | **fixed**: reduced to a shape-only tag ("recorded as shape only, not as evidence"), the pack's existing form for contributor incidents (cf. the bash-3.2 entry) |
| 8 | "four environment claims NOT CONFIRMED" not established by the excerpt (luna F10 Med, grok F7 Low) — CONVERGED | yes | **fixed**: restated as the README does (asserted results, no captured output) |
| 9 | "Ships `unprobed`… #115 queue" adds no criterion (luna F13 Low) | n/a | **rejected-with-reason**: house convention on every Provenance entry in both files (11 + 4 marker instances in op-rigor alone); removing it here would break the covenant's marker/queue pairing |
| 10 | trail path `reviews/2026-09-02-narrowing-is-not-repair/` unverifiable from packet (grok F6 Low, [unverified]) | n/a | **rejected-with-reason**: the trail is created in the same commit as the rule; this file is in it |
| 11 | "the next round shows a leftover" reads as observation (grok axis 6, no id) | yes | **fixed**: "names a leftover" |

Not raised by either reviewer, self-found: marker form on the op-rigor rule was "contributor
incident as shape"; the incident is an in-repo PR trail, so the plain form is used.

Remedies were authored here: neither reviewer's proposed wording was pasted. luna's F1 remedy
("evidence, valid narrowing, or retraction") would have kept narrowing as a peer of the other
two, which is the framing the incident refutes; grok's F2 remedy called for a separate §4
bullet, which would have duplicated the every-noun test — folded as an obligation instead.
