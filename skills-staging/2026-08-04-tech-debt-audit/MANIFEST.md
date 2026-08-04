# Manifest — tech-debt-audit library (2026-08-04)

One skill, distilled from a contributor's five-repo audit-and-fix session
(2026-07-14, contributor-reported, not linkable — see the skill's own
Sources section for the incident-to-class mapping), verified against the
repository at HEAD `1e38fa8`.

## Delivery / tracking state

By DEFAULT `skills-staging/` is gitignored local working material. For THIS
PR delivery the skill's files were **force-added** (`git add -f`), so they
are tracked and WILL be published by the delivery commit — that is the
intent. Stage only by explicit pathspec under this directory; never
`git add -A` in this repo (a stage-everything command can sweep in
untracked session transcripts elsewhere in the tree).

## What this is, and is not

`tech-debt-audit` is a single self-contained skill, not a multi-skill
campaign library like the three earlier 2026-07-30 batches in this
directory — it is staged rather than placed directly in `skills/` because
it is new (unprobed, no routing-corpus regression evidence yet) and the
maintainer may want to run it through the pack's own review ladder before
a tier/routing decision (ARCHITECTURE.md §5-§6).

## Runtime and dependencies

- **Execution:** the skill's detector is `scripts/debt-scan.mjs` — plain
  Node.js >= 18, zero npm dependencies (only `node:child_process`,
  `node:fs`, `node:path`, `node:os` from the standard library), invoking
  `git` via `execFileSync` where available and falling back to a bounded
  filesystem walk when it is not. No Python, Bash wrapper, or `gh`
  dependency.
- **Self-test:** `node scripts/debt-scan.mjs --self-test` builds a clean
  git tree and a planted-fixture git tree (plus a no-git tree) in a fresh
  temp directory, asserts the clean tree scans 0-actionable, the planted
  tree fires all six detection classes, the no-git tree fires
  `VCS-MISSING`, and — this is the load-bearing assertion — that a
  sentinel secret planted in the fixture never appears verbatim in the
  scan's own output. Exit 0 = all four assertions held. Ran green
  2026-08-04.
- **Target runtime:** exercised on macOS (the session machine); the code
  path is plain POSIX-portable Node with no OS-specific commands, so it is
  expected to run unchanged on Linux, but that has not been separately
  verified.
- **Sibling skills (cross-references resolve when installed):**
  `security-architect` (behavior rule 1 — never read secret/PII values
  into context, which is the design constraint the detector's masking and
  field-shape-only PII scan both exist to satisfy; the threat-model
  bullet's untagged-example clause, from the SAME source incident, is the
  provenance-judgment half of what this skill's `PII-SHAPE` class
  mechanizes), `ground-truth-gates` (sentinel-tagged fixtures — the
  discharge path a `PII-SHAPE` hit routes to), `delegation-and-review`
  (absence-is-not-resolution, for the re-audit-as-delta step),
  `operational-rigor` §3 (the rollback-order rule, cited for the
  post-audit fix-batch case). Where a sibling is absent the pointer
  degrades to plain context; re-resolve section numbers on install
  (skill-authoring §3).

## Review notes for the installer

- **A pre-fix version of `mask()` leaked real characters of every matched
  secret** (leading/trailing chars plus exact length) and its self-test's
  containment check tested a value the content-scan path could never
  reach, so it passed regardless — found in this delivery's one
  adversarial round, fixed before this commit. `mask()` now returns a
  one-way sha256 fingerprint plus a coarse length bucket; nothing derived
  by a reversible transform of the match ever appears. Do not take this
  on trust: matches are captured via regex/JSON parse and only `m[0]` is
  ever passed through `mask()` (grep the source for that call site — it
  is the only one), but VERIFY `mask()` itself by re-running
  `--self-test` and reading its containment line, which now checks every
  6-character run of the planted secret, not just full-string
  containment.
- **Only one adversarial round ran, not the multi-round ladder the other
  batches in this directory cite.** See UNCERTAINTY.md's first item
  before trusting this without a second independent pass — especially
  re-attempting the exact leak-reproduction technique that found the
  first bug.
- `PII-SHAPE` is a shape scan, not a provenance oracle — per the skill's
  own bounds section, an untagged hit is presumed real and is meant to
  escalate to the repo owner, not to auto-clear or auto-redact.
- The skill was, historically-valid but not independently re-checkable
  by an installer without access to the source repos, run read-only
  against two real repos from the source incident (details in the
  skill's Sources section) in addition to the synthetic self-test.
