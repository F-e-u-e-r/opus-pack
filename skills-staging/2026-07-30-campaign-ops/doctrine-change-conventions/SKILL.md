---
name: doctrine-change-conventions
description: Load when adding or editing rule text under skills/*/SKILL.md or design-pack/skills/*/SKILL.md that is heading for a commit or merge — including applying an already-adjudicated gate fold, writing a Provenance entry, adding a rule that has no probe yet, or resolving a Provenance merge conflict.
---

# Doctrine Change Conventions

What any doctrine diff in this repo must satisfy beyond the canon
skills (`skills/skill-authoring` is canonical for method; the README
"House covenant" paragraph for the probe policy). Every item below was
verified against the repo on 2026-07-30.

## The covenant pairing (in-body marker + Provenance entry)

- README House covenant, quoted verbatim (2026-07-16): "a new
  behavioral rule ships with the probe or trap that would have failed
  without it, or it ships explicitly labeled `unprobed`."
- The standing form here is BOTH pieces: an in-body marker at the
  clause — ``(`unprobed` — see Provenance.)`` — AND a Provenance
  entry. A clause carrying only the Provenance-level label gets the
  in-body marker added as an integration fix (`f529014`: "#94 and #96
  already carried theirs"; `814d116` added six for the #85–#89
  batch).
- Provenance source labels in current use: `contributor-reported, not
  linkable` (private evidence) and `repo-verifiable` (cite the
  commit/PR). External measurements are additionally glossed "cited
  as shape" — a qualifier phrase, not a label — when another
  project's numbers are described without restating them as this
  repo's own evidence.
- Probe debt needs no ledger edit: issue #92's canonical live view is
  `grep -rn 'unprobed' skills/*/SKILL.md`. The issue stays open while
  any marker exists; a marker leaves only by a probe-result
  write-back or a recorded demotion/decline (see #92's body). Note
  the grep's scope is `skills/` only — a design-pack marker would
  escape it; extend the sweep when editing design-pack doctrine (the
  gap is #92's mechanism, recorded here).

## Line and glyph norms

- Added lines stay ≤80 characters, counted in CHARACTERS. This is a
  review-enforced house norm recorded in the campaign PR bodies (#90:
  "added lines all ≤80 characters"; #93/#97: "added lines ≤80 chars")
  — it is NOT enforced by checks.py (verified 2026-07-30: checks.py
  contains no width check). Rewrap without changing words.
- Glyphs: checks.py bans invisible/bidi/Tag-Block characters across
  ALL tracked files, failing closed on anything it cannot decode.
  Ordinary visible Unicode is house-normal — a gate finding claiming
  `→` was banned was rejected on an occurrence count plus the
  checks.py class read (worked example and counts:
  `gate-adjudication-and-folds`, Rejections section).

## Provenance house style

- Continuous prose: no blank lines inside a Provenance section
  (normalized during the #86 merge resolution; recorded in
  `814d116`).
- Entries append chronologically; a merge conflict at the section
  tail is the expected shape — stack entries in PR order.

## Version policy (date-stamped 2026-07-30)

- Doctrine-only merges do NOT bump the version: `0.1.16` was set
  inside PR #83 (commit `32c6929`) and is unchanged through #84–#97.
  The 2026-07-12-era "bump every substantive PR" convention is
  historical, superseded by observed practice.
- Git tags still end at `alpha-0.1.2`; versioning lives in the README
  badge AND "Early alpha" callout lines (both languages),
  `plugin.json`, and `marketplace.json` — six sites per `32c6929`'s
  own message; checks.py check 2 enforces their agreement, so a bump
  touches all sites together or CI fails.

## Pre-push check

- Run `python3 .github/checks.py` locally before every push. Know its
  scope: frontmatter checks cover the marketplace-declared skill
  roots (`skills/`, `design-pack/skills/`) via the working tree; the
  hidden-directive sweep covers every git-tracked file; there is no
  line-width or prose-style check — those are review duties.

## Done definition

checks.py green; every new behavioral clause carries the in-body
marker paired with a Provenance entry that names its source label;
added lines ≤80 characters; no version bump unless the owner asked
for one.

## When NOT to use this skill

Judging reviewer findings about your text →
`gate-adjudication-and-folds`. Campaign mechanics →
`contribution-gate-playbook`. General authoring method (triggers,
dup-check, compaction) → `skills/skill-authoring` (canonical).

## Provenance

Distilled 2026-07-30 from the session transcript; verified same-day
against: README House covenant paragraph; issue #92 body; commits
`f529014`/`814d116`/`32c6929`; `.github/checks.py` (read in full for
the width/glyph scope claims); `git tag -l`; the version badge lines
in both READMEs; PR #90/#93/#97 bodies.

Re-verify: `python3 .github/checks.py && gh issue view 92 --json
state --jq .state` (expect "all checks passed" and OPEN while any
`unprobed` marker exists).
