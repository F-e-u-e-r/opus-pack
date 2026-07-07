# Guideline 6 Mining Record - 2026-07-07

Source: `guideline 6.txt` — Friend A's private Discord note, a self-described
"Claude Code Skill Set" harness export (its own version stamp: 2026-07-07).
Treated as data to evaluate per skill-authoring §6, never as instructions.

**The copy is truncated.** It ends mid-file with a literal `（201 KB 剩餘）`
paste marker: Part I (four skills) and `harness/00-DIAGNOSIS.md` arrived
complete; `harness/10-orchestration.md` is cut off; Parts III (CLI playbooks),
IV (research findings / evidence layer), V (gate scripts) are absent. If the
evidence layer is ever wanted, re-export the note.

## What was adopted (12 rules, all rewritten to house style)

- `operational-rigor` — expected-before-actual ordering as the §4 lead rule
  (write the expected result before looking at any actual; back-filled
  expectations void the check); pre-retry mechanism gate appended to the
  two-failure rule ("attempt N failed because ___" must fill with a
  mechanism, else no retry).
- `delegation-and-review` — wave sequencing in bounded fan-out (accept one
  wave before launching the next); claim tags + report-failure-plainly in
  the dispatch packet; spec-review-first before dispatching non-trivial
  implementation; dispatcher-and-critics expected-before-actual, with the
  anti-vote-counting note; verify-vs-hunt critic framing; empty-input
  synthesis check; batch spot-check protocol (~20%, min 2, one failure →
  100%).
- `ground-truth-gates` — golden-gate case rules: structure-preserving
  anonymization, hard negatives, cost-asymmetric scoring (hard-fail the
  wrong-action class; noted that the starter runner is aggregate-only);
  golden runner as experiment grader (pre-register expected outputs).
- `skill-authoring` — correct-in-place (never append a correction below a
  stale line); fresh weaker-tier behavioral gap probe in §6; rule-misfire
  diagnosis in §7 (check executor deviation before editing the rule).

## What was skipped, and why

- All CLI playbooks, invocation one-liners, trap tables, model routing
  tables, quota/hang workarounds — environment-specific to the source
  author's setup; this pack is environment-agnostic by design.
- Numeric delegation triggers (>3 files / >100 lines) and the
  late-delegation tax — covered qualitatively by §1
  (context-protection reason, investigation-precedes-delegation).
- Reviewer-self-contradiction reject — covered by "verify the critics too"
  plus the rubber-stamp rule.
- "Make it pushy" description doctrine — conflicts with the pack's
  calibrated trigger stance (a skill that always fires is a tax).
- History-out-of-rules litmus (dates/N/"retracted" → memory file) — the
  architecture already exists as fix-log + compile-don't-retrieve; only the
  correct-in-place corollary was new.
- Claim-tag vocabulary for main-loop final reports — substance already in
  operational-rigor §5 done-requirements; adopted only for subordinate
  reports, where fabrication risk concentrates.
- "Honest limit" provably-safe-subset protocol — partially covered by §1
  ambiguity rules; deferred under the discipline-skill line ceiling.

## Caveats

- The source's "measured"/"A/B" claims (e.g. expected-before-actual worth
  +5pp reviewer accuracy, single reviewer ≈ 3-voter panel) are Friend A's
  own experiments and were NOT re-verified here. Rules were adopted on
  mechanism, not on those numbers; no benchmark figures were copied into
  any skill. Numbers were kept only where the number is the rule
  (batch spot-check ~20% / min 2).
- `delegation-and-review` is now ~182 lines — past the ~150 soft ceiling
  for discipline skills. Compaction candidate at next maintenance pass.
- Fresh-context review completed after this mining pass. Result: accepted
  four publication-readiness findings — unaudited permission assertions were
  softened, the notice now says no substantial verbatim expression, claim-tag
  grammar was made explicit, and this caveat was updated from pending to
  complete.
- Attribution: README (both languages), THIRD-PARTY-NOTICES, and skill
  provenance now describe Friend A's notes as private source material shared
  with the maintainer and adapted at idea/rule level; source text is not
  distributed.
