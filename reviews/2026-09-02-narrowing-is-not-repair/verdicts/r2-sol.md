BLUF: FIX. The revision introduces two fresh mechanism over-claims, and three round-1 dispositions remain not confirmed. [verified: comparison of the diff, contexts, adjudication, and README in this packet]

F1. `cross-model-review/SKILL.md`, “only if every counterexample the finding cites now falls outside the qualified boundary” — Excluding the cited counterexamples rebuts those examples but does not establish the qualified claim throughout its remaining scope. The done-when compounds this by requiring only that excluded examples be named. — Require both exclusion of the cited counterexamples and evidence warranting the claim over the retained scope; word the disposition accordingly. — severity High — [verified: a qualifier can exclude every cited example while retaining an unsupported domain]

F2. `cross-model-review/SKILL.md`, “two repairs exist: measure … or retract” — This is a false exhaustive claim. A wider claim may be substantiated by already-existing but previously omitted evidence, a valid derivation, or an authoritative source; a new probe is only one way to substantiate it. — Replace with “two broad repairs exist: substantiate the wider claim with adequate evidence, using a probe where empirical measurement is required; or retract/narrow it.” — severity Medium — [verified: the rule purports to enumerate all repairs but names only new measurement and retraction]

F3. `operational-rigor/SKILL.md`, “never from proxies consistent with it” and “every noun in the line corresponds to a measured value” — Sound verdicts may be derived from indirect observations when those observations jointly entail the verdict; the defect is using observations merely consistent with it. Conversely, measuring every noun does not establish the verbs or relations between them—the incident’s unsupported claim was precisely the relation “ran from.” The done-when can therefore pass while the original defect remains. — Require observations sufficient to establish every material entity, condition, and relationship asserted by the verdict; prohibit proxies that are merely consistent rather than sufficient. — severity High — [verified: locating X and Y separately does not establish “X ran from Y,” while sufficient indirect evidence can validly establish a verdict]

F4. `operational-rigor/SKILL.md`, “makes the claim true only inside the fixture” and “name every forced condition” — A fixture does not determine where a claim is true; it limits what the probe establishes. Also, “every forced condition” broadens from the preceding “one of the mechanism’s conditions” to irrelevant setup details. — Say the probe supports the claim only under each forced condition material to the asserted mechanism, and require those material conditions—not every fixture setting—to appear in the verdict and supported rule text. — severity Medium — [verified: evidence scope and truth scope are distinct, and fixtures necessarily force immaterial setup conditions]

F5. `operational-rigor/SKILL.md`, “read the code that emits it” and “capture each asserted probe’s invocation and output at the revision” — The asserted “one level deeper” distinction does not remove the overlap with Context B, which already requires inspecting the oracle, invocation path, attributable revision, executed path, and logged pass/fail result. Only the sufficiency of the verdict’s observations and disclosure of forced mechanism conditions are new. — Delete the duplicated tracing/capture requirements or explicitly defer them to the preceding bullet, leaving this rule to govern whether the captured observations entail the printed verdict. — severity Medium — [verified: direct clause-by-clause comparison with Context B]

F6. `cross-model-review/SKILL.md`, “A contributor-reported doctrine drill (not linkable) showed the same shape earlier” — Marking this “shape only” prevents it from serving as evidence, but does not make the historical assertion supported by the inlined README. It adds no operative criterion and conflicts with the packet’s provenance constraint. — Remove the sentence, or supply reviewable provenance in the evidence trail. — severity Low — [verified: the only supplied README contains no contributor-drill claim]

F7. both provenance additions, “standing #115 queue” and `reviews/2026-09-02-narrowing-is-not-repair/` — The claimed house convention, queue, and exact trail location cannot be re-derived from this packet. The adjudication merely asserts them. — Verify these against the full tree before commit and include that evidence in the gate packet, or remove the unverifiable references. — severity Low — [unverified]

Axis 1: findings F1–F4. [verified: mechanism analysis above]

Axis 2: findings F3 and F5. [verified: comparison within the new bullet and against Context B]

Axis 3: finding F5. [verified: clause-level overlap with Context B]

Axis 4: findings F3 and F4. Obligation (2) conceptually belongs under verdict fidelity and is now inside one bullet with one done-when, but that done-when is insufficient and its evidence-scope wording is inaccurate. [verified: structure and wording of the added bullet]

Axis 5: no finding. [verified: no machine, OS, vendor, concrete path, or volatile tool-lineup fact remains in operative rule text]

Axis 6: no finding. The ✅ and ❌ examples match the README’s measured-path correction and the earlier proxy inference. [verified: direct comparison with the README]

Axis 7: findings F6 and F7. [verified/unverified as individually tagged]

Axis 8: finding F6. [verified: the unsupported shape-only sentence supplies no criterion]

Axis 9, round-1 dispositions:

- #1 NOT CONFIRMED: the heading contradiction is gone, but F1 shows the replacement still over-claims what excluding cited counterexamples establishes. [verified: diff]
- #2 NOT CONFIRMED: the clause was moved into one §4 rule, but F4 shows its mechanism wording remains defective. [verified: diff]
- #3 NOT CONFIRMED: the distinction was added, but substantive duplication remains as F5. [verified: Context B comparison]
- #4 CONFIRMED: the author-belief rhetoric was removed and replaced by the broken-search ambiguity. [verified: diff]
- #5 CONFIRMED: the identified machine- and runtime-specific tokens are absent from operative rule text. [verified: diff]
- #6 CONFIRMED: the unsupported path-resolution bug is absent; the ❌ now states the proxy inference recorded by the README. [verified: diff and README]
- #7 NOT CONFIRMED: “shape only” limits evidentiary use but leaves an unsupported and unnecessary historical assertion; see F6. [verified: packet provenance]
- #8 CONFIRMED: the provenance now says asserted results lacked captured output, matching the README. [verified: README]
- #9 NOT CONFIRMED: the claimed house convention and queue cannot be checked from this packet; see F7. [unverified]
- #10 NOT CONFIRMED: the exact trail path and “this file is in it” cannot be checked from this packet; see F7. [unverified]
- #11 CONFIRMED: “shows a leftover” was changed to “names a leftover.” [verified: diff]

FIX F1,F2,F3,F4,F5,F6,F7