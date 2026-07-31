# START HERE — campaign-ops library (2026-07-30)

What this library is: the distillation of the 2026-07-29/30 maintainer
session that integrated contributor PRs #85–#89, #91, and #94–#96 into
main through three combined gates — PR #90 (merge `a148180`), PR #93
(`92077a7`), PR #97 (`79ca49c`) — and opened the probe-debt tracker,
issue #92. The engineering core is not the doctrine content those PRs
carried; it is operating the contributor-PR pipeline (combined branch →
tri-lens cross-model gate → owner-authorized merge → post-merge duties)
without breaking the house covenant, the privacy boundaries, or the
published-record conventions.

Authored 2026-07-30 by the retiring architect from the session
transcript (`chat-history.md`, a local untracked file at the repo root)
with every repo-facing claim re-verified against the repository on
2026-07-30. Companion files: `MANIFEST.md` (per-skill evidence),
`UNCERTAINTY.md` (everything NOT settled — read it before trusting a
claim near its topics).

## Canonical-source map (who wins on disagreement)

| Topic                     | Canonical source                        |
|---------------------------|-----------------------------------------|
| Cross-model gate doctrine | `skills/cross-model-review/SKILL.md`    |
| Authoring/covenant method | `skills/skill-authoring` + README       |
|                           | ("House covenant" paragraph)            |
| Execution discipline      | `skills/operational-rigor`              |
| Practice records          | PR #90/#93/#97 bodies, per-PR           |
|                           | evaluation comments, issue #92          |
| This library              | repo-specific operating layer, dated    |
|                           | 2026-07-30 — canon and records win      |

## Current-state triage (as observed 2026-07-30)

Facts a fresh session must not misread as its own breakage:

- At authoring time: 0 open PRs; 1 open issue (#92) — #92 is DESIGNED
  to stay open while any `unprobed` marker exists; it is a queue, not
  a stale ticket. This delivery itself adds issue #100 (transcript
  disposition; UNCERTAINTY item 1) and, while open, the delivering PR.
- The repo root carries UNTRACKED private session transcripts
  (`chat-history.md`, `security-enhancement.md`). Never stage them;
  see `repo-boundaries-and-sync`. Owner disposition pending (#100).
- `skills-staging/` is gitignored by owner decision (`92314a6`);
  this library was force-added on an explicit owner instruction —
  that delivery is not license to publish other ignored zones.
- The README per-skill sync loop currently errors on `skill-vetting`
  (present in `skills/`, absent from both live installs) — a known
  pre-existing state, not drift you introduced.
- Many local branches are residue of merged or abandoned campaigns —
  do not adopt-and-finish them (see `failure-archaeology`).

## Reading order

1. `contribution-gate-playbook` — the pipeline end to end.
2. `gate-adjudication-and-folds` — judging lens verdicts.
3. `doctrine-change-conventions` — what any doctrine diff satisfies.
4. `repo-boundaries-and-sync` — what may be staged, synced, published.
5. `failure-archaeology` — dead ends and residue from this session.

## Relationship to the older local library (2026-07-12)

`skills-staging/` also holds a 12-skill library authored 2026-07-12
(local-only, unpublished, gitignored — its existence is public via
`92314a6`'s commit message). Overlap map, verified 2026-07-30:

- Partially superseded by this library: cross-model-gate-ops,
  release-and-publish, repo-state-and-sync (verified stale examples
  in `UNCERTAINTY.md` item 5: the 2026-07 reviewer lineup, the
  bump-every-PR rule, the `README.zh-TW.md` filename).
- Old editing-skills-and-docs overlaps the new
  doctrine-change-conventions — and is itself stale (its description
  counts "the eight SKILL.md files"; `skills/` now has ten).
- NAME COLLISION: the old library and this one BOTH carry a skill
  named `failure-archaeology` (different content). Never install both
  libraries into one skills directory without renaming one.
- Everything unlisted (architecture-contract, build-and-env,
  config-and-flags, debugging-playbook, diagnostics-and-tooling,
  eval-operations, validation-and-qa) has the old library as sole
  source — verify each claim against the repo before relying on it.

Precedence for overlapping topics: canon skills first, then the newer
dated statement, then the older library.
