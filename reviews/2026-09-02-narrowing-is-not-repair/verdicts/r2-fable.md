# r2 verdict — Fable (fresh context, packet-only)

Read: packet-r2.md only. No commands, no other files. Every adjudication row treated as a claim to refute.

## Findings

**F1** — cross-model-review §3, "Prepending a qualifier … is a retraction only if every counterexample the finding cites now falls outside the qualified boundary" — mechanism gap: the test is vacuous when the over-claim finding cites no counterexamples (the README's own round-1 Medium, "generalizes past the evidence", is exactly that shape). A qualifier then passes "every cited counterexample excluded" trivially while still being wider than what was measured. — fix: anchor the test to the measured claim, with cited counterexamples as the explicit check: "…only if the qualified claim is no wider than what was measured, and every counterexample the finding cites falls outside it" — Medium — [verified: README round-1 table row 2 is an over-claim finding with no counterexamples; the rule's test as written would not constrain its repair]

**F2** — cross-model-review neg, quoted `"the digest confirmation is what exposes a failed removal"` — the README's round-1 High reads "the digest confirmation is what makes an incomplete removal detectable"; the neg presents a paraphrase inside quotation marks. — fix: quote the README wording or drop the quotation marks — Medium — [verified: README §Round 1 row 1 vs diff line 68]

**F3** — cross-model-review neg "the repair that held was the retraction" and Provenance "the repair that held was retraction to the measured claim" — the README records two rounds; the retraction was applied in round 2 and no round reviewed it afterwards. "Held" asserts survival under scrutiny the trail does not contain. — fix: "the repair recorded in round 2 was the retraction" — Medium — [verified: README §Review lists rounds 1 and 2 only; round 2 row 3 is the retraction's own disposition, nothing follows it]

**F4** — operational-rigor §4, "an inference prints the right answer for the wrong reason" — not true in general: an inference from measured premises can be sound (a checked return code → failure), and an inference can also print the wrong answer. This is the successor to the deleted "direction of its author's belief" sentence (adjudication row 4) and is rhetoric of the same kind. — fix: "and an inference from proxies can print the line while the observation it names never occurred" — Medium — [verified: sentence text in diff; row 4 disposition claims rhetoric was replaced by an operational statement, but this clause is neither operational nor generally true]

**F5** — operational-rigor §4 obligation (2), "a fixture that forces one of the mechanism's conditions … makes the claim true only inside the fixture" — false in general and contradicted by the cited README: "in the wild an unchanged source or a forged header does the same". Forcing a condition establishes the claim under that condition, wherever it holds, not "only inside the fixture". — fix: "establishes the claim only under that condition" — Medium — [verified: README §What was probed, paragraph beginning "Out-of-tree placement alone is NOT sufficient"]

**F6** — operational-rigor §4, "Two obligations: (1) … (2) …" followed by "And the trail carrying the verdict … capture each asserted probe's invocation and output" — three imperatives labelled as two; and the done-when ("every noun in the verdict line and every forced condition is backed by a captured measurement") does not test obligation (2)'s actual requirement (the forced condition is NAMED in the line and in supported rule text — a forced condition is a fixture setting, not a measurement) nor the trail-capture imperative. Adjudication row 2's "re-authored as obligation (2) … with its own done-when" is therefore NOT CONFIRMED: there is one shared done-when and it does not cover (2). The "in any rule text the probe supports" clause also reaches past a verification rule into doctrine authoring. — fix: count three (or fold trail-capture into (1)); done-when: "every noun in the verdict line is backed by a captured measurement, every forced condition is named in the line, and every asserted result has its invocation and output captured" — Medium — [verified: diff lines 117–131]

**F7** — operational-rigor §4, "The check's-name bullet above traces a CITED check to its oracle; this is one level deeper — the oracle's own printed line" — mis-positioned against Context B, which already reaches "the assertions … inspected at the revision the cited run actually used". A printed line is downstream of the assertions, not deeper. The real distinction — the neighbour asks whether the assertions cover the property; this rule asks whether the assertions measure what the line names rather than proxies — is not what the sentence says. Row 3's "fixed in part" is only partly re-derivable: the distinction exists, its wording is wrong. — fix: "the check's-name bullet asks whether a cited check's assertions cover a property; this asks whether those assertions measure what the printed line names, or proxies for it" — Medium — [verified: Context B text vs diff lines 109–110]

**F8** — operational-rigor §4, "or the rule asserts the other condition alone" — presumes exactly two conditions; a mechanism with three has "other conditions". — fix: "the remaining conditions alone" — Low — [verified: diff line 125]

**F9** — operational-rigor Provenance, "the probe checked into reviews/2026-08-31-… printed 'stale bytes ran from an out-of-tree cache'" — the checked-in probe is the rewritten one (README: "the probe now captures…"); the bad line belonged to its first revision. Also the quoted string is not verbatim in the README (which quotes "ran from an out-of-tree cache"). — fix: "the probe's first revision printed…" and align or unquote — Low — [verified: README round-2 row 1 and §What was probed]

**F10** — Provenance claims outside the README: (a) "PR #233" — the README never states its own PR number (only "#230" as the landed limb); (b) "A contributor-reported doctrine drill (not linkable) showed the same shape earlier" — still asserts an event as fact, and row 7's claim that this is "the pack's existing form (cf. the bash-3.2 entry)" cannot be checked from the packet; (c) row 9's "11 + 4 marker instances" and row 10's same-commit trail are likewise outside the packet. All NOT CONFIRMED; none refuted. — fix for (b): "a contributor-reported incident of the same shape is noted, uncited" or delete — Low — [unverified]

**F11** — density/redundancy: the cross-model-review neg (lines 68–75) and its Provenance paragraph (lines 84–94) narrate the same PR #233 sequence twice at near-equal length; the op-rigor trail-capture sentence overlaps Context C ("report skipped verification as skipped") without naming the delta (capture vs. non-fabrication). — fix: neg keeps the failure shape only, Provenance keeps the narrative — Low — [verified: diff text]

**F12** — cross-model-review §3, "A qualifier that still contains them … repaired nothing" — over-states when a qualifier excludes some cited counterexamples but not all; the finding stays open, but "nothing" is false. — fix: "still contains any of them has not closed the finding" — Low — [verified: diff lines 64–65]

## Axis lines

- axis 1 (mechanism): F1, F4, F5, F12
- axis 2 (internal conflict / paraphrase): F7; heading-vs-body of the §3 paragraph is now consistent (both state the counterexample condition) — no further finding
- axis 3 (redundancy): F11
- axis 4 (scope): F6 (obligation (2) fits a verdict-line rule only for the "name it in the line" half; the "rule text the probe supports" half is authoring doctrine; not one done-when)
- axis 5 (portability): no finding — no `-S`, `__pycache__`, `/var`, vendor or OS token in rule text; PR/issue numbers confined to neg/Provenance, matching Context A's house form
- axis 6 (neg/✅ fidelity): F2, F9; the two counterexamples, "names a leftover", and the ✅'s capture steps match the README
- axis 7 (provenance): F3, F10; "second variant of the same family, not a cross-family gate", "location inferred", "unreported co-cause", "environment probes were captured" are supported
- axis 8 (density): F11
- axis 9 (round-1 dispositions): rows 1, 5, 6, 11 and the self-found marker-form change CONFIRMED from the diff (row 6's "grep realpath: 0 hits" re-derived — the README contains no "realpath"); row 2 NOT CONFIRMED as stated (F6); row 3 partly confirmed (F7); row 4 deletion confirmed but replacement reintroduces the defect class (F4); row 7 shape-only reduction present, house-form claim NOT CONFIRMED (F10); row 8 confirmed in substance, "marked … unconfirmed" is not the README's framing ("no evidence checked in") — Low, folded into F10; rows 9 and 10 reasons plausible, NOT CONFIRMED from the packet

## Honest limits
Everything outside the diff, the three contexts, the adjudication table and the README (house conventions, marker counts, the bash-3.2 entry, the commit contents, prior-round text) is unverifiable here and reported as such.

FIX F1 F2 F3 F4 F5 F6 F7
