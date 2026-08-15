# Gate closure — T5-placement concern disposition

**STATUS: CLOSED by owner adjudication. There was NO round 3 and NO
final 2/2 PROCEED.** This record states that plainly rather than
presenting a clean dual approval that did not occur.

Reviewers: `gpt-5.6-luna` and `gpt-5.6-sol`, both at reasoning effort
`max`, each isolated with its packet as the only file in its working
directory, neither shown the other's verdict. All four verdicts are
retained verbatim in this directory, including every HOLD.

## Round 1 — exact-record review

Eight questions on the disposition record's fidelity. Luna: PROCEED.
Sol: HOLD on two defects, both reproduced first-hand by the author
before any repair:

1. **A closeness claim the counts do not support.** The record said the
   probe failed on identifiability "not by narrowly missing a threshold
   at n=6". Recomputed from the frozen grid, one arm on each fixture
   sat exactly one observation from a band edge, so the claim was
   unsupported — and worse, it reasoned FROM the per-arm counts, which
   the same record declares carry no weight in the disposition.
2. **"completed as preregistered" reading as as-written compliance.**
   Because grading used the operator applying the frozen predicate
   rather than the separate model adjudicator the prereg *proposed*,
   the phrase could be read as asserting protocol-compliance
   as-written, contradicting the `AUTHORIZED-ADJUDICATION-METHOD-DEVIATION`
   recorded in the same document.

Both repaired. The owner-fixed ruling sentence was left byte-untouched;
the scoping was added beside it rather than inside it.

## Round 2 — repair review, and what it actually found

Four questions on the repair. **Both reviewers returned HOLD, and both
simultaneously confirmed the disposition record itself carried no
defect in any of the four authorized blocking categories** — no
outcome misstatement, no marker mutation, no doctrine overclaim, no
provenance error.

Their common finding was narrower and correct: the author's claim that
the two defect classes were "machine-barred" was overstated. The
guards were keyword blocklists, which cannot bar a paraphrase class.
Sol reproduced two concrete bypasses against the printed predicates;
Luna independently noted that the as-preregistered guard tested global
co-presence rather than per-occurrence scoping.

## Owner adjudication

**Finding: VALID, but outside the authorized blocking taxonomy.**

The gate's HOLD licence was fixed in advance at four categories:
outcome misstatement, marker mutation, doctrine overclaim, provenance
error. Both reviewers confirmed none of the four was present, so
check-completeness cannot be retroactively promoted into blocking
semantics.

**The process deviation was the author's, not the reviewers'.** The
round-2 dispatch packet granted HOLD authority over its own four
questions — one of which asked whether the checks were merely
cosmetic — and so was BROADER than the owner contract it was serving.
Both reviewers exercised the licence they were actually handed,
correctly. Recorded here so the trail does not later read as reviewers
exceeding their remit.

Stated in the owner's own framing: *round-2 reviewers correctly
identified two check-coverage weaknesses under the broader review
packet they received. Both simultaneously confirmed the disposition
record had no authorized semantic blocker. Owner adjudication restored
the original narrower HOLD taxonomy, accepted the check findings as
factual non-blocking findings, and authorized bounded mechanical repair
without another model-review round.*

## Why no round 3

- `DISPOSITION.md` has not changed by a single byte since round 2, and
  both reviewers cleared its semantics at exactly those bytes.
- Only `disposition_checks.py` changed afterwards.
- The replacement guards are structural assertions that can be
  adjudicated mechanically, and each already carries a mutant control
  proving it fails on its bypass.

Re-running two models to confirm that a content hash changes when
content changes would add negligible information and would convert a
mechanical correctness question into a reviewer vote.

## The repaired guards, described precisely

Three structural invariants replaced the keyword blocklists, each with
a mutant control that trips it and is then restored:

- **Content pin** — the two repaired paragraphs are pinned by sha256.
  Any edit to them, including a semantically equivalent rewrite, fails
  the gate and forces re-review.
- **Structural prohibition** — the reasoning body may contain no
  per-arm count (`n/6`) and no band label. This removes the expressive
  surface through which a descriptive count could re-enter the
  reasoning, rather than banning particular sentences.
- **Per-occurrence adjacency** — the phrase "as preregistered" may
  occur only in the owner's ruling and in its own scope note, in that
  order, with nothing else carrying it between or after.

**Precision that matters, and is not to be overstated:** these checks
mechanically enforce the currently sealed record shape and the
observed failure classes. They do **not** prove that no semantically
equivalent overclaim can ever be expressed. The content pin in
particular is not a semantic classifier — it is a tripwire that
re-opens the gate whenever the pinned text changes at all.

Suite: `disposition_checks.py` **50/50 PASS**, including the three
mutant controls.

## Closure state

- Disposition semantics: cleared by both reviewers at the current bytes.
- Round-2 HOLDs: retained verbatim, adjudicated non-blocking under the
  original taxonomy, and mechanically repaired anyway.
- Rounds run: **two.** No round 3. No final 2/2 PROCEED.
- Behavioural invocations for this disposition: **0.** No executor run,
  no use of the remaining hard-cap capacity, no use of the T2 headroom
  or the stage-2 reserve.
