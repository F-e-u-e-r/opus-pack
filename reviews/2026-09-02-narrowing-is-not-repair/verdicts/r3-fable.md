# r3 verdict — Fable 5.1, fresh-context, packet-only

Read: packet-r3.md only. No commands, no other files. Every disposition row was
treated as a claim and re-derived from the diff, the three contexts and the README.
Out-of-scope items (house convention, #115 queue, trail paths, PR number, marker
counts) are not re-reported.

## Findings

### axis 1 — MECHANISM true in general

F4 — cross-model-review §3, "every counterexample the finding cites falls outside
the qualified boundary" — mechanism: the test is keyed to what the finding CITES,
not to what was reproduced. Context A reproduces the finding, not each
counterexample; a cited counterexample that does not actually break the claim but
sits inside the qualified boundary would fail test 2 and block a retraction that is
in fact sound. Conservative failure, but the rule as written makes an unreproduced
reviewer assertion controlling. Fix: "every reproduced counterexample the finding
cites". Severity Low. [verified: derivation from the diff text against Context A's
"reproduce first" clause; no README case exercises it]

Otherwise axis 1: no finding. The op-rigor heading (sufficient observations vs
merely-consistent proxies), the "broken search and an empty location look the same
from a proxy" mechanism, and obligations (1)–(3) hold in general; obligation (1)'s
"observation sufficient for it" admits sound indirect inference as row 3 required.

### axis 2 — INTERNAL CONFLICT / PARAPHRASE

F1 — cross-model-review §3, "Done when each over-claim finding's disposition names
which repair was applied" — mechanism: Context A (the paragraph immediately before)
is done when "every reproduced finding carries a disposition this section's triage
permits (owner-accepted deferral included)". A reproduced over-claim finding that is
deferred under Context A has no repair applied, so it satisfies Context A's done-when
and fails the new one; the new done-when silently forecloses a disposition the
neighbouring rule permits. The body's own trigger is narrower ("check both
explicitly before recording `fixed`"), so the done-when is wider than the rule it
closes. Concrete fix: "Done when each over-claim finding recorded `fixed` names
which repair was applied — …" (or "…each over-claim finding's disposition names
which repair was applied or the deferral the paragraph above permits"). Severity
Medium — an over-broad done-when in doctrine that contradicts the adjacent
paragraph; one-clause fix. [verified: derivation from Context A's done-when text
vs diff lines 56–58 and 54]

F3 — cross-model-review §3, "retract the wording to what was measured" / "no wider
than the measurement" — mechanism: the same paragraph admits non-empirical claims
("by a probe where the claim is empirical"), but both tests and the done-when are
bounded only by "the measurement"; for a claim substantiated by derivation there is
no measurement to bound against and the tests have no referent. Fix: "no wider than
what the evidence supports (the measurement, where the claim is empirical)" once,
and let "measurement" stand elsewhere. Severity Low. [verified: internal
derivation from diff lines 49–58]

F5 — operational-rigor §4 obligation (2), "or the claim asserts the remaining
conditions alone" — mechanism: elliptical; reads either as the consequence of not
naming the forced condition (the intended sense) or as a permitted alternative
("either name it, or make the claim assert the remaining conditions"), and the verb
is missing ("…alone suffice"). Row 12's "remaining conditions" landed but left the
clause ambiguous. Fix: "— unnamed, the claim is read as asserting that the remaining
conditions alone suffice". Severity Low. [verified: internal derivation from diff
lines 110–114]

### axis 3 — REDUNDANCY

F7 — operational-rigor §4 obligation (1), "an unbacked term is measured or the line
is weakened to what was" — mechanism: restates Context B's "assert only the
properties that trace established … stays unverified — say so" for the object of a
self-authored verdict line. The distinguishing sentence (coverage-of-a-property vs
sufficiency-for-the-printed-line) carries the difference and row 5 landed; residual
overlap is tolerable. Fix: none required; optionally append "(the check's-name
bullet's 'say so', applied to your own line)". Severity Low, shippable-with-note.
[verified: side-by-side of Context B and diff lines 106–109]

Otherwise axis 3: no finding. neg vs Provenance in cross-model-review still share
the two-leftovers fact, but neg is now the failure shape and Provenance the
narrative (row 14 landed as described). Obligation (3) is not Context C: Context C
bans fabrication; (3) assigns evidentiary status to un-captured but possibly real
results.

### axis 4 — SCOPE of the op-rigor rule's three obligations and done-when

F6 — operational-rigor §4 done-when, "every material forced condition is named in
the line" — mechanism: obligation (2) requires the forced condition to be named "in
the verdict line and in any claim the probe is cited to support"; the done-when
covers only the line, so a probe whose line is correct but whose cited claim drops
the condition (exactly the README's round-1 → round-2 shape) is "done" under the
done-when while violating (2). Row 11 claimed the done-when covers all three;
it covers (2) only halfway. Fix: "…named in the line and in any claim it is cited
to support…". Severity Low. [verified: derivation from diff lines 110–120]

Otherwise axis 4: no finding. "any claim the probe is cited to support" keeps (2) a
duty on the citing session, not a rule about authoring elsewhere; (3)'s "at the
revision the claim is about" is the right scope.

### axis 5 — PORTABILITY

axis 5: no finding. Rule text and examples in both files name no vendor, OS,
interpreter, path or tool; "compiler", "clean", "cache attribute", "validation mode",
"digest confirmation" are generic. Machine specifics stay in the README.

### axis 6 — NEG/✅/❌ FIDELITY vs README

axis 6: no finding. Checked:
- neg quote "the digest confirmation is what makes an incomplete removal
  detectable" — verbatim to README round-1 High (row 8 landed).
- neg "prepends 'for this failure mode' and records `fixed`" — README round-1
  disposition "fixed by scoping to 'for this failure mode'".
- neg "two leftovers inside that failure mode that keep the digest matching while
  the removal failed" — README round-2 Medium names exactly two (regeneration
  overwrites; byte-identical) and states scoping "did NOT repair", which places
  them inside the failure mode.
- ✅ path-returned / survived-the-clean / cache-attribute read-back / resolve-to-one
  file / forced mode named — README round-2 High #1 and #2 fixes. "REPRODUCED" as
  the printed token is not quoted in the README (it says "prints its own verdict"
  and "not reproduced"); illustrative, not a quote — acceptable.
- ❌ "old output printed and the in-tree cache directory is empty → 'ran from an
  out-of-tree cache'" — README: INFERRED from "OLD printed and no in-tree .pyc";
  "forced validation mode absent from the line" derivable from "unreported
  co-cause … fixed in … its verdict line".

### axis 7 — PROVENANCE vs README

F2 — cross-model-review Provenance, "the repair recorded in round 2 was retraction
to the measured claim" — mechanism: the README records round 2's repair as "the text
now says the confirmation detects a REMAINING mismatch and does not prove the
removal worked". That is a retraction, but nothing in the README shows the digest
confirmation's behaviour was MEASURED (the probe measures import result and
`__cached__`, not the digest step), so "to the measured claim" asserts a match to
a measurement the trail does not show — the rule's own defect class, in its own
provenance. Row 9's swap ("the repair recorded in round 2") landed; the appended
predicate is NOT CONFIRMED. Fix: "the repair recorded in round 2 was a retraction —
the text now claims only that the confirmation detects a remaining mismatch and
does not prove the removal worked". Severity Low (narrative, not mechanism), but
fix it if F1 is being touched anyway. [verified: README round-2 Medium row vs diff
lines 79–80; absence of any digest measurement in README "What was probed"]

Otherwise axis 7: no finding. Op-rigor Provenance re-derives line by line: first
revision printed "ran from an out-of-tree cache" from OLD-printed + no in-tree
artifact (README r2 High #1); same-family second variant, not cross-family (README
"two variants of one model family"); location inferred, forced mode an unreported
co-cause, environment results lacking checked-in evidence (r2 High #1, High #2,
Medium #2); rewrite captured path + `__cached__`, env probes captured (r2 fixes).
"a leftover that regeneration overwrites; one byte-identical to the regenerated
artifact" — verbatim in substance to README r2 Medium #1.

### axis 8 — DENSITY

axis 8: no finding beyond F5. The op-rigor bullet (34 lines) is within the section's
norm set by Context B; the cross-model-review rule states test 1 in the heading and
again in the body, which is the pack's heading-then-body form, not padding.

### axis 9 — ROUND-2 DISPOSITIONS actually landed?

| row | status from packet |
|---|---|
| 1 | CONFIRMED — heading, test 1 + test 2 with AND, done-when names bounding measurement and excluded counterexamples. Sub-claim "README round-1 row 2 has no counterexample" CONFIRMED (Medium row cites none). |
| 2 | CONFIRMED landed — but the new done-when it feeds introduces F1. |
| 3 | CONFIRMED — sufficiency-vs-consistency heading; ✅ "resolve to the same file", ❌ "the relation never established". |
| 4 | CONFIRMED — "establishes the claim only under that condition"; "material to the mechanism". README quote "in the wild an unchanged source or a forged header does the same" is verbatim. |
| 5 | CONFIRMED — distinction sentence present; "read the code that emits it" absent from the diff. |
| 6 | NOT CONFIRMED by construction — the deleted sentence is not in the packet; I can only confirm no drill sentence appears in the diff. |
| 7 | out of scope per packet; the one packet-checkable sub-claim (Context A cites "PR #30" in rule text) CONFIRMED. The grep/SHA evidence is NOT CONFIRMED by construction. |
| 8 | CONFIRMED — verbatim match to README round-1 High. |
| 9 | PARTIALLY CONFIRMED — "the repair recorded in round 2" landed; the appended "was retraction to the measured claim" is not derivable (F2). |
| 10 | CONFIRMED — operational form present; the new "broken search / empty location" sentence names a mechanism, not rhetoric. |
| 11 | PARTIALLY CONFIRMED — three numbered obligations; done-when covers (1), (3) and the line-half of (2) only (F6). |
| 12 | CONFIRMED — "remaining conditions" (but see F5 on the surrounding clause). |
| 13 | CONFIRMED — "the first revision of the probe"; quoted line matches README. |
| 14 | CONFIRMED — neg is the failure shape; narrative lives in Provenance. |
| 15 | CONFIRMED — "changed the sentence without closing the finding". |
| 16 | CONFIRMED in Provenance ("as lacking checked-in evidence"). Rule text (3) still says "a reviewer marks it unconfirmed" — prescriptive rule wording, not a README paraphrase; no finding. |
| round-1 rows 4,5,6,8,11 "CONFIRMED by both" | NOT CONFIRMED by construction — no round-1 table is in the packet. |

## Verdict

One Medium (F1: the new done-when contradicts Context A's permitted deferral —
over-broad, one-clause fix). Six Low (F2–F7) are shippable-with-note; F2 and F6
are cheap to fold in while F1 is edited. Body and last line agree.

FIX F1
