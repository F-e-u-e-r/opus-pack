# Design-review packet — proposed doctrine rule "coverage before clearance" (⑬)

You are one of two independent reviewers (mutually blind; you see only this packet). This is a WORDING-LEVEL design review of ONE proposed rule for `skills/delegation-and-review/SKILL.md` §3 of an agent-discipline skill pack. No bytes have landed; implementation is separately gated. Review the PROPOSED WORDING on the ten axes below.

## Settled context — do NOT re-vote it
The maintainer's read-only orientation established (and the owner ratified) a PARTIAL-GAP: current doctrine has a dispatch-side scope declaration, a completion-claim audit (dishonesty-bound, execution-deliverable-bound, claim-side), a packet-errors rule (finding-side only), and a settled-tree protocol (motion-bound) — and a constructed counterexample passes ALL of them: an honest reviewer PROCEEDs over a silently-truncated packet (a pagination cap dropped one requested file's diff), and the orchestrator reads the verdict as full-requested-scope clean. False clearance, zero rule violations. The owner-locked invariant: **a clearance may bind only the scope actually made available to and covered by that review — credited scope ⊆ actually covered scope — explanation-based, deliberately NOT `declared_paths == diff_paths`.**

## Existing neighbor (current main, for the pairing check)
The packet-errors rule reads: "A reviewer's verdict inherits the dispatch packet's own errors — a wrong premise in the spec manufactures a finding that is correct given the packet and false given the system … Before crediting a CRITICAL or must-fix, check the packet's own claim, not only the diff against it …" The proposed rule is designed as its declared all-clear counterpart (claims-before-finding / coverage-before-clearance).

## THE PROPOSED WORDING (rule bullet, D&R §3, placed immediately after the packet-errors rule)
```
- **A clean verdict is never evidence about material the reviewer did not
  receive or otherwise verify — reconcile coverage before crediting a
  clearance** (`unprobed` — see Provenance). The packet-errors rule above
  checks the packet's CLAIMS before crediting a finding; this is its
  all-clear counterpart: it checks the review's COVERAGE before crediting
  a clearance. A bounded-scope review's PROCEED gets consumed as "the
  requested scope is clean", but the verdict can bind only the scope the
  reviewer actually covered — and an assembly gap (a truncated diff, a
  pagination cap, a glob that missed a path) produces an honest PROCEED
  that silently clears material nobody saw: no fraud exists anywhere, so
  the completion-claim audit above never fires — the gap is a COVERAGE
  defect in the dispatch, never the reviewer's failure. Before expanding
  an all-clear to the full requested scope, reconcile three things: the
  REQUIRED scope (what this clearance is about to be credited against),
  the AVAILABLE material (what the reviewer could actually see — an
  embedded diff, an independent copy, or trusted access to the frozen
  tree all qualify; availability is not prompt-embedding), and the
  COVERED scope (what the verdict's own evidence shows was examined).
  The clearance binds the covered scope only — downward, never inflated
  upward. Every gap between required and covered is EXPLAINED or it
  stays open: a required path never made available and never examined is
  UNREVIEWED, never clean — a reviewer's silence about it is not
  clearance (it could not mention what it never saw), and the only way
  to close it without re-review is the orchestrator's own independent
  ground truth that the path is unchanged against the review baseline
  (verified, not assumed — unchanged material legitimately produces no
  diff to review); an extra path beyond the brief is an authorized
  producer's output, or a discovered dependency to escalate and
  re-scope, or it stays outside the clearance — never silently absorbed,
  and never auto-filed as misconduct; a reviewer assigned a subset
  judges that subset — its PROCEED never expands to paths it was never
  given. No machine-readable path manifest is required — the
  reconciliation is the orchestrator's read of what the brief asked
  against what the packet carried and the verdict shows, at whatever
  granularity the dispatch actually declared.
  ❌ "the reviewer PROCEEDed and never mentioned B, so B is clean" — B's
  diff was dropped by a pagination cap; the PROCEED covers what the
  packet carried, and B was never in it.
  ✅ "brief asked A+B; packet carried only A; before crediting A+B
  clean, diffed B against the review baseline myself — unchanged, so
  the A-clearance plus the verified-unchanged B closes the scope."
```

## Draft Provenance paragraph (lands with the rule at implementation)
```
The coverage-before-clearance rule (2026-08-29) comes from a first-hand
orientation over this file's own review-lane semantics, after an intake
question asked whether brief-vs-diff reconciliation was already covered:
the dispatch-side scope declaration (§2), the completion-claim audit
(dishonesty-bound, bound to an execution deliverable, and claim-side),
the packet-errors rule (finding-side), and the settled-tree protocol
(motion-bound) each pass a constructed counterexample in which an honest
reviewer PROCEEDs over a silently-truncated packet (a pagination cap
dropping one requested file's diff) and the orchestrator reads the
verdict as full-scope clean — a false clearance with zero rule
violations. The rule closes the consumption-side gap; the locked
invariant is credited-scope ⊆ actually-covered-scope,
explanation-based, deliberately not path-set equality. Ships `unprobed`
per the covenant; its probe — a bare vs ruled orchestrator handed a
truncated packet's PROCEED and a broader requested scope, scored on
whether the absent path gets credited clean — joins the standing #115
queue.
```

## Static discrimination controls (7/7; expected verdict written before determination)
| # | Control | Setup | Expected | Wording clause that carries it |
|---|---|---|---|---|
| C1 | EXTRA | brief allows A/B; diff carries unexplained C | no full clearance; C not auto-fraud | "an extra path … never silently absorbed, and never auto-filed as misconduct" |
| C2 | MISSING-CLAIM | brief requests A/B; packet carries only A; consumed as all-reviewed | B = UNREVIEWED; A-only clearance | "a required path never made available and never examined is UNREVIEWED, never clean" |
| C3 | UNCHANGED | brief allows A/B; only A changed | no failure for B's absence from the diff | "orchestrator's own independent ground truth that the path is unchanged … unchanged material legitimately produces no diff to review" |
| C4 | AUTHORIZED-DERIVED | brief authorizes generated artifact C | C not misjudged as unexplained extra | "an authorized producer's output" |
| C5 | DISCOVERED-DEPENDENCY | unauthorized C found necessary mid-work | escalate/re-scope; not silent accept, not auto-reject | "a discovered dependency to escalate and re-scope" |
| C6 | SUBSET | reviewer assigned A only | judges A only; PROCEED never inflates to A+B | "a reviewer assigned a subset judges that subset — its PROCEED never expands" |
| C7 | DIRECT-ACCESS | packet embeds no B diff, but reviewer holds trusted frozen-copy access and its verdict evidence shows B examined | NOT misjudged as coverage-missing | "AVAILABLE material (… trusted access to the frozen tree all qualify; availability is not prompt-embedding)" + "COVERED scope (what the verdict's own evidence shows was examined)" |

## Review scope — answer ALL ten explicitly
1. Does the rule close the CLEARANCE-CONSUMPTION gap (orchestrator-side), rather than restating the dispatch-side owned-scope declaration?
2. Is strict path-set equality kept OUT of the doctrine (explanation-based reconciliation only)?
3. Does missing requested material stay UNREVIEWED — and is it impossible to clear it via the reviewer's silence / "no findings mentioned"?
4. Is the verified-unchanged carve-out safe (independent ground truth, verified not assumed — no hole where "probably unchanged" clears a dropped path)?
5. Are extra paths and discovered dependencies handled by explanation/escalation, never auto-fraud and never silent absorption?
6. Does a subset reviewer's PROCEED stay bound to its subset?
7. Can trusted repo/frozen-copy access legitimately satisfy availability (no prompt-embedding-equality regression)?
8. Is the rule properly deduplicated against the completion-claim fraud audit and the settled-tree protocol (complement, not overlap or contradiction)?
9. Does it avoid disproportionate bookkeeping for an ordinary single-file review (no machine-readable manifest requirement; granularity follows the dispatch's own declaration)?
10. Zero content from any other queued workstream — in particular nothing about "review evidence must be RE-READ never REGENERATED"?

If you believe correctness REQUIRES new runtime path-set tooling, file that as a DESIGN FINDING (it is not an authorization for tooling).

## Verdict format (mandatory)
Number findings, anchor each to the wording, classify on an axis. Final line exactly one of:
`PROCEED` or `FIX <numbered list of blocking findings>`
