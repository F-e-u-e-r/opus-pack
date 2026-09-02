# Narrowing is not repair — two rules from PR #233's own review (cross-model-review §3, op-rigor §4)

Ports the lesson of `reviews/2026-08-31-out-of-tree-cache-removal/` into doctrine:

1. **cross-model-review §3** — a scope qualifier repairs an over-claim only when the
   qualified claim is no wider than what the evidence establishes, and every reproduced
   counterexample falls outside it. Round 1 of #233 recorded a qualifier as `fixed`;
   round 2 found the counterexamples still inside it.
2. **operational-rigor §4** — a probe's verdict line is established by observations
   sufficient for every entity AND relation it names, never by proxies merely
   consistent with it; forced fixture conditions material to the mechanism are named
   in the line and in any claim the probe supports; an asserted diagnostic result with
   no captured invocation/observation is a claim, not evidence.

Both ship `unprobed` per the covenant.

## Review — three rounds, capped

| Round | Reviewers | Verdicts | Adjudication |
|---|---|---|---|
| 1 | codex `gpt-5.6-luna` (inlined, read-only); grok-4.6 (isolated HOME, staged file, read-only tools) | luna: body FIX / last line PROCEED (**self-contradicting**, treated as FIX); grok: FIX ×6 | `verdicts/ADJUDICATION-r1.md` — 8 fixed, 2 rejected-with-reason |
| 2 (gate) | codex `gpt-5.6-sol`; Fable 5.1 fresh-context subagent (packet-only) | sol FIX ×7; Fable FIX ×7 + 5 Low | `verdicts/ADJUDICATION-r2.md` — 15 fixed, 1 rejected-with-reason |
| 3 (gate, cap) | same pair | sol FIX ×3 + 1 Low; Fable FIX ×1 + 6 Low | `verdicts/ADJUDICATION-r3.md` — 9 fixed, 1 rejected-with-reason |

Packets: `packets/packet-r{1,2,3}.md` (self-contained, regenerated per round); diffs
`packets/diff-r{1,2,3}.patch` and `diff-final.patch`. Expectations were written before each
round's verdicts were read: `EXPECTED-r{1,2,3}.md`.

**Family diversity:** round 1 had two families (OpenAI, xAI), neither the author's. Rounds 2–3
had the author's own family (Fable 5.1, fresh context) plus one other (OpenAI sol) — a
cross-family gate, but the second family was the same provider as round 1's codex.

**What the rounds show, on the rule's own subject:** every round's fixes introduced at least
one new defect the next round caught — the heading contradicted its body (r1), the
replacement "every noun measured" missed the relation the incident actually got wrong (r2),
the replacement "measured" contradicted the body's non-empirical branch (r3). The
post-round-3 wording is unreviewed; the edits are single clauses recorded in
ADJUDICATION-r3.

## What would change the conclusion
- A bare-probe showing a reviewer, given the incident without the rule, already refuses
  to record a still-containing qualifier as `fixed` → rule is redundant at that tier.
- A case where a correctly-bounded qualifier is rejected by the two-test check → the
  test is over-strict; the reproduced-counterexample clause is where that would show.
