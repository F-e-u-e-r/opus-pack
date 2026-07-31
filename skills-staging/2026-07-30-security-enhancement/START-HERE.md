# START HERE — skill-vetting hardening library (2026-07-30)

A focused, project-specific skill library extracted from the
`security-enhancement.md` session transcript and **verified against the current
repository**. It captures the durable engineering lessons of the **skill-vetting
hardening campaign** that shipped as PR #83 (`7cd2af6`, merged 2026-07-26, an
ancestor of the current default branch).

## The engineering core (what the hard part actually is)

The skill-vetting subsystem is a SessionStart tripwire whose whole value is
**honest observation of attacker-controlled content**. Its GOALS are to never
silently miss a changed skill, never let a hostile name reach a shell or the model
as instructions, and never present its own broken measurement as a clean result —
and several of those goals are only PARTLY met (the shell and prose-injection
boundaries are documented OPEN; see UNCERTAINTY.md), which is exactly why this
library separates shipped invariants from open risk.
The campaign's real lesson is not any single fix — it is that **the fixes
themselves, and the tools that verify them, are the most dangerous surface**: a
quoting "fix" that didn't fix, a mutation harness that scored 55/55 with zero
discriminating power, a test whose name asserted a property its fixture never
reached. This library exists so the next session does not re-walk those.

## Canonical source map (verify against these, do not trust prose alone)

| What | Source of truth | Caveat |
|---|---|---|
| Observation/persistence + CLI | `hooks/skill_snapshot.py` | 1201 lines; the primitive decides no verdicts |
| SessionStart hook | `hooks/skill-vetting-advisory.py` | thin; in-code comments ARE the round-by-round archaeology |
| Vetting procedure | `skills/skill-vetting/SKILL.md` | §3 binds a verdict to an exit-0 digest |
| Evidence harness | `hooks/mutation_matrix.py` + `hooks/mutations.json` | authoritative-mode gate is code-enforced |
| Threat model + invariants I1–I11 | `reviews/2026-07-25-skill-vetting-snapshot-threat-model.md` | the `NOT MET`/OPEN list is the risk map; I12–I17 are the round-8 DESIGN's, unimplemented; a couple of doc claims overstate the code — the I6 `:296` "guaranteed logging" line and the advisory.py docstring's "never re-advises" — see UNCERTAINTY "Known live-doc defects" |
| Round-8 design D1–D5 | `reviews/2026-07-25-skill-vetting-round8-design.md` | **DESIGN, explicitly unimplemented** — do not read as shipped |
| Consistency gate | `.github/checks.py` | enforces duplicate-test + mutation_matrix env-read invariants |

## Current state (so you don't misread it)

At the pinned HEAD the live `hooks/` and `.github/` surfaces have **no drift from
HEAD**, `python3 .github/checks.py` is green, and both skill-vetting suites pass;
the worktree intentionally contains this library's staged additions (that is the
deliverable, not breakage). Several threat-model items are **documented OPEN at
merge and still open** — G3-SHELL, G3 prose-injection, the §1 procedure boundary,
I11 full serialization, the I2/I10 halves — and D1–D5 are unimplemented. These are
in `UNCERTAINTY.md`; do not read the skills as claiming them closed.

## The four skills and when each fires

1. **`skill-vetting-security-invariants`** — editing the hooks or the digest/
   baseline/anomaly/CLI logic, or about to cite an invariant as met.
2. **`mutation-matrix-evidence-discipline`** — editing/citing the mutation
   harness, or building any tool whose own output is the evidence.
3. **`skill-vetting-hardening-archaeology`** — before re-attempting a fix or
   design, or when reaching for a buried idea ("just add quotes", "mark it
   equivalent", "finish D1–D5").
4. **`security-hardening-review-ops`** — running/reviewing a cross-model
   hardening campaign, or pushing/merging a security-sensitive branch.

**Overlap:** a runtime-hook change that also adds/edits a test **co-loads 1 and
2** — the security invariants govern the behavior, the mutation/evidence skill
governs the test's honesty. The security↔mutation "alone" split never suppresses
**4**: if that change is part of a hardening campaign or a security-sensitive
push/PR/merge, load 4 as well.

## Reading order

New here → this file, then `MANIFEST.md` (what each skill claims + its evidence),
then the skill whose trigger you are about to hit. Assessing risk → `UNCERTAINTY.md`
and the threat model's OPEN list first. These skills are STAGED, not installed;
see the repo's install conventions before copying any into `.claude/skills/`.
