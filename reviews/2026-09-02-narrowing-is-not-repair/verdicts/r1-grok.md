I'll read the review brief in full and produce the review from that packet.# Review: over-claim repair + verdict-from-observation doctrine

Two paragraphs distilled from PR #233. The expensive failure mode here is the same one the §3 draft is trying to teach: wording that is wider than the evidence, shipped for later sessions to obey. Several sentences in this diff do that.

## F1 — MECHANISM / INTERNAL CONFLICT — High
**location:** `skills/cross-model-review/SKILL.md`, heading “An over-claim is repaired by evidence or retraction, **never by narrowing**”
**mechanism:** The heading forbids narrowing. The body then gives two fixes, the second of which *is* narrowing (“retract the wording to exactly what was measured”), and it further allows a scope qualifier when the reviewer’s counterexamples fall outside the new boundary. “Never by narrowing” is therefore false as a general rule; it is only true of the incident’s *insufficient* qualifier (“for this failure mode”), which still contained the counterexamples. Sessions that obey the heading will reject legitimate retraction-to-measured-scope. The heading also fights Context A’s “author the minimal fix”: a real scope retraction can be that fix. Intra-rule contradiction, not a neighbour paraphrase.
**concrete fix:** Drop “never by narrowing” from the heading. State the actual rule: repair by measuring the wider claim or by retracting to what was measured; a qualifier counts as retraction only after an explicit check that every cited counterexample falls outside the new boundary.
**[verified: derivation from the packet — heading vs the two-fixes paragraph and the qualifier exception in the same added block]**

## F2 — SMUGGLING / MECHANISM — High
**location:** `skills/cross-model-review/SKILL.md`, “The same gap opens when a **fixture is narrowed instead of a claim**”
**mechanism:** Two distinct lessons are fused. Over-claim *disposition* (qualifier still contains the counterexamples → do not record `fixed`) is a §3 rule. “A fixture that silently supplies a mechanism condition must be named in the rule and in the probe verdict” is a claim/fixture-correspondence rule. The trail recorded them as separate findings (round 1 High + round 2 Medium on the qualifier; round 2 High on `UNCHECKED_HASH`). They are not “the same gap.” The sentence also misstates the incident: nobody narrowed the fixture as a repair; the fixture already forced condition 2 and the claim omitted it. The §3 done-when does not cover this clause (only “which of the two fixes” or “the counterexamples a qualifier excludes”), which is the tell that it was bolted on. It belongs next to the new op-rigor §4 bullet (or as its own §4 bullet), not inside finding-disposition.
**concrete fix:** Remove the fixture paragraph from the §3 rule. Add a §4 bullet: if the fixture forces a condition, the rule text and the probe verdict must name it; otherwise the claim is true only inside the fixture. Give that bullet its own done-when and its own neg (unnamed `UNCHECKED_HASH`-style co-cause), without calling it “narrowing.”
**[verified: derivation from the packet — README round tables vs the “same gap” sentence; §3 done-when omits the fixture branch]**

## F3 — PORTABILITY — High
**location:** `skills/operational-rigor/SKILL.md`, rule body/examples: “`__pycache__`”, “`/var` vs `/private/var`”, “`-S` prints the same value”
**mechanism:** The new §4 rule is general doctrine, not a Python-cache clause. `__pycache__` and `-S` are CPython lineup facts; `/var` vs `/private/var` is a macOS canonicalization fact. The inlined trail itself records that an earlier draft naming vendor, OS, and a `~/Library/...` path was removed as a portability violation and that both reviewers confirmed no scope violation remained in *that* PR’s rule text. This addition puts equivalent facts back into rule text. PR numbers and trail paths would have been enough.
**concrete fix:** Keep examples in the register the ✅ already uses (“in-tree cache directory empty”, “imported module’s cache attribute”, “an asserted flag or env result with no command-and-output pair”). Move `/var`, `-S`, and `__pycache__` to the trail, if they belong anywhere.
**[verified: derivation from the packet — portability constraint in the rubric; README “earlier draft named the vendor, the OS and a ~/Library/... path”]**

## F4 — NEG EXAMPLE FIDELITY / PROVENANCE — High
**location:** `skills/operational-rigor/SKILL.md`, ❌ “a `/var` vs `/private/var` resolution bug turned out to have been finding nothing all along”; Provenance “exposed a **path-resolution bug** that had made the earlier search find nothing”
**mechanism:** The inlined trail does not record a path-resolution bug, `/var`, `/private/var`, or an earlier search that found nothing. Round 2 High is: location was **never measured**; “ran from an out-of-tree cache” was **inferred** from “OLD printed and no in-tree `.pyc`.” “Never measured” is not “searched, hit a canonicalization bug, found nothing, and still printed the strong verdict.” The ❌ and the Provenance over-state the excerpt and, via `/var` vs `/private/var`, also violate portability (F3).
**concrete fix:** Rewrite the ❌ to the trail’s actual proxy inference: `OLD` printed and no in-tree artifact → “ran from an out-of-tree cache,” artifact never located. Provenance should stop at that High and the env-capture Medium. If a path-resolution bug exists, it needs a checked-in trail sentence; this packet does not have one.
**[verified: derivation from the packet — full inlined README has no path-resolution / /var / “find nothing” language]**

## F5 — PROVENANCE — Medium
**location:** `skills/cross-model-review/SKILL.md` Provenance, “The same shape recurred earlier in a **private doctrine drill** (not linkable): a `verified` marker wider than its evidence, where running the missing probe exposed a false claim that narrowing the marker would have hidden.”
**mechanism:** The rubric is: Provenance may claim only what the inlined trail supports. The README does not mention a private drill, a `verified` marker, or a missing probe that exposed a false claim. The causal story reads as independent confirmation of “narrowing hides falsity,” which this packet cannot audit. Neighbouring rules may tag “private incident as shape”; they do not get to smuggle an uncheckable success story in as evidence.
**concrete fix:** Delete the drill paragraph, or reduce it to an unlinkable-shape tag with no mechanism narrative. Generality is the standing `#115` probe’s job; this rule already ships `unprobed`.
**[verified: derivation from the packet — claim absent from the inlined README]**

## F6 — PROVENANCE — Low
**location:** both Provenance blocks, “this rule’s own review trail is `reviews/2026-09-02-narrowing-is-not-repair/`”
**mechanism:** That path is not in the inlined excerpt. From this packet it is unverified whether the trail exists or supports anything.
**concrete fix:** Omit until the trail is inlined or this review produces it; trail paths are allowed, but they are not evidence until present.
**[unverified]**

## F7 — PROVENANCE — Low
**location:** `skills/operational-rigor/SKILL.md` Provenance, “the same verdict marked **four environment claims** in the trail **NOT CONFIRMED**”
**mechanism:** The excerpt records one Medium: “the trail asserted `-S` / `-E -S` / env-diff results and a `/usr/bin/python3` identity with no evidence checked in.” It does not record four separate `NOT CONFIRMED` marks or that phrase.
**concrete fix:** Restate the Medium as the README does (assertions with no checked-in capture), not as four verdict stamps.
**[verified: derivation from the packet — round 2 table vs Provenance wording]**

## F8 — DENSITY / MECHANISM — Medium
**location:** `skills/operational-rigor/SKILL.md`, “an inference is **wrong in the direction of its author’s belief** while printing the right answer — it also hides the fixture’s own bugs, because a path-resolution error…”
**mechanism:** Not a clearance condition, not a done-when, not a discriminating example. “Wrong in the direction of its author’s belief” is not generally true (inferences need not track belief). The “because” clause is the same unbacked, OS-specific path bug as F4. The clearance that *does* work is already in the next sentence: every noun in the verdict line is a measured value, or the line is weakened.
**concrete fix:** Delete this clause. Keep “must have located Y and tied X to it” plus the every-noun sentence.
**[verified: derivation from the packet — sentence adds no operational test; path-bug “because” not in the README]**

---

**axis 1 MECHANISM:** F1, F2, F8. Remaining core holds beyond the incident: over-claims close by measurement or by retraction to what was measured, with an explicit counterexample-boundary check before a qualifier is `fixed`; a harness verdict must be computed from the observation it names.
**axis 2 INTERNAL CONFLICT:** F1 (heading vs own body). No contradiction or paraphrase of Context A/B/C. Context A is remedy-pasting; the new §3 rule is over-claim disposition. Context B is name≠coverage for *cited* checks; the new §4 rule is one level deeper (the oracle’s own printed line may be an inference). Context C forbids fabricating outputs, not inferring a stronger verdict from real proxies. The fixture clause does not paraphrase §4’s “every noun in the line”: omitted co-causes are not nouns already in the line.
**axis 3 REDUNDANCY:** no finding. A reader who only traces check names (Context B) or who never fabricates (Context C) can still author a harness that prints “X ran from Y” from two cheaper consistent facts, and can still mark an over-claim `fixed` by prepending “for this failure mode.”
**axis 4 SMUGGLING:** F2 (distinct rule, wrong file, misframed as “the same gap”). The §4 README-capture sentence is the *same* lesson on a second surface (claim only what was captured); keep it, but strip the `-S` specimen (F3) and do not lean on a path-bug the trail does not record.
**axis 5 PORTABILITY:** F3.
**axis 6 NEG EXAMPLE FIDELITY:** F4 for §4’s ❌. §3’s `neg` matches the trail (qualifier “for this failure mode”; leftover regeneration overwrites / byte-identical leftover as counterexamples still inside the boundary; retraction to “detects a remaining mismatch and does not prove the removal worked”). Minor stretch: “the next round **shows** a leftover” reads as observation; the excerpt is a reviewer-identified counterexample. Not a separate id.
**axis 7 PROVENANCE:** F4, F5, F6, F7. Supported: round 1 High scoped and still wrong in round 2; two same-family variants, not a cross-family gate; round 2 High on inferred location; round 2 High on unnamed `UNCHECKED_HASH` co-cause; env assertions lacked checked-in captures; trail path `reviews/2026-08-31-out-of-tree-cache-removal/`.
**axis 8 DENSITY:** F8. Also: the fixture sentence (F2) has no done-when. Everything else in the two bodies is clearance, done-when, or a discriminating example.

FIX F1, F2, F3, F4, F5, F8
