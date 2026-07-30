---
name: gate-adjudication-and-folds
description: Load when a cross-model lens verdict has landed for a doctrine change in this repo and you must decide fold, reject, or stop — including when two lenses propose opposite fixes for one finding, when one lens keeps producing must-fixes after the others hold PROCEED, or when a finding asserts runtime or tool semantics.
---

# Gate Adjudication and Folds

Canonical verdict rules: `skills/cross-model-review/SKILL.md`
(findings are claims, §3; the loop is bounded, §4). This file pins the
adjudication patterns the 2026-07-29/30 campaigns used, each with its
public record. On disagreement, the canon skill wins.

## Fold discipline

- Reproduce a finding against the actual file/repo before folding it.
- Fold commits are named `Fold gate rN: <what>` — single-PR campaigns
  prefix the target, e.g. `Fold #91 gate r1: …` — and state which
  lens produced each item and why the fix is right (see `6fa6154`,
  `5fa241b`, `83a038d`, `1560b97`).
- Your own folds are attack surface for the NEXT round: #90's gate
  caught the staged-diff gate's circular trigger, a defect an earlier
  fold itself introduced (the catch is listed in #90's body; the
  fold-introduced attribution is session-recorded). Do not close on a
  round whose folds no lens has seen, except under the bounded-loop
  close below, where exactly that residual is disclosed by name.

## Rejections carry in-repo counter-evidence

- A reviewer finding you reject gets a recorded counter-fact in the
  fold commit and PR body. #90's body records the aggregate — "7
  findings rejected with in-repo counter-evidence"; the two worked
  examples below are session-recorded, their counter-facts re-derived
  in-repo 2026-07-30:
  - a lens called `→` a banned glyph — rejected by reading checks.py's
    banned class (invisible/bidi/Tag-Block only; U+2192 is not in it)
    and counting occurrences on main (plentiful: 107 hits in
    `skills/*/SKILL.md` at the pre-#90 main);
  - a lens called a line over-wide — rejected with the character
    count (78; the house norm counts characters, not bytes).
- No counter-evidence found = it is not a rejection; it is still an
  open finding.

## Runtime-semantics findings get EXECUTED verification

- When doctrine text asserts what a runtime does, execute it before
  the claim ships. Precedent chain on #96: the draft said the bracket
  form "silently reads empty" — execution shows `os.environ["X"]`
  raises KeyError; `.get()` returns `None`; an unguarded shell `$X`
  expands empty (r1 converged must-fix + r2 refinement, `6fa6154`,
  `5fa241b`). A lens also executed the ❌ example and showed `'\\n'`
  inside single quotes emits a literal backslash-n — the example
  could never produce the incident it described.
- Rule: a doctrine line stating tool/runtime behavior is a claim to
  verify by execution, not prose to wordsmith. This applies to YOUR
  folds too — the r2 refinement corrected an r1 fold's attribution.

## Opposite-fix convergence → adjudicate by the protected property

- Two lenses converged on the SAME gap in #91 (the durable/ephemeral
  overlap for "gitignored but externally archived" paths) with
  OPPOSITE precedence fixes. Adjudication anchored on what the rule
  protects — a later reader's ability to resolve the citation — so
  check-ignore wins: an ignored working path is ephemeral even when
  an external archive preserves it; cite the archive itself. Recorded
  in PR #93's body, the fold commit `1560b97`, and #91's evaluation
  comment — the comment publicly states that the two lenses proposed
  opposite precedences.
- Rule: when converged fixes conflict, derive the answer from the
  rule's protected property, not from either lens's framing — and
  record the adjudication where the next maintainer will read it.

## Terminal conditions

- TRIPLE PROCEED: every lens PROCEED in the same round (#93 r2,
  #97 r3). The normal close.
- Bounded-loop close (non-convergence): canon caps the loop and sends
  a non-converging gate to a human with the trail (cross-model-review
  §4 — on disagreement it wins). The house application, owner-set in
  the 2026-07-23 twelve-round campaign (PR #61 era) and re-applied in
  #90: a campaign may run past canon's 2–3-round cap only under the
  owner's standing campaign mandate; when one lens keeps producing
  must-fixes while the gate otherwise converges (#90's public record:
  grok PROCEED r5–r11, luna PROCEED r7/r9/r11, sol still finding
  last-mile items), declare the close condition before the terminal
  round (session-recorded for #90 at r8; the public record is the
  close itself), execute it, apply the final folds labeled
  `<lens>-unverified`, and put the close AND its named residuals in
  front of the owner — in the PR body's Review gate section and the
  campaign report (`83a038d`; #90 body). A close that leaves
  residuals is surfaced, never silent.
- The two failure shapes this bounds: unbounded re-review (no
  terminal proof ever arrives) and silent early close (residue
  undisclosed). The bound plus named-residual disclosure avoids both.

## Done definition

Every lens finding for the round is folded (commit cites it),
rejected (counter-evidence recorded), or explicitly carried into the
next round's packet; a terminal state was reached by one of the two
closes; the PR body's "Review gate" section states the trajectory,
the rejections, and any unverified residuals by name.

## When NOT to use this skill

Pipeline mechanics (branching, CI, merge, comments) →
`contribution-gate-playbook`. What the doctrine text itself must
satisfy → `doctrine-change-conventions`.

## Provenance

Distilled 2026-07-30 from the session transcript; verified same-day
against PR #90/#93/#97 bodies, the #91/#96/#85 evaluation comments,
and commits `6fa6154`/`5fa241b`/`83a038d`/`1560b97`. Session-recorded
specifics (public anchors in parentheses): the `→`/78-char rejection
details (#90's body carries the aggregate rejections line), the r8
close pre-declaration (the body carries the close itself), and the
fold-introduced attribution of the circular trigger (the body lists
the catch). The `→` occurrence count was re-run in-repo 2026-07-30.

Re-verify: `git log --oneline --grep='Fold' -10` and the newest
combined PR body's "Review gate" section.
