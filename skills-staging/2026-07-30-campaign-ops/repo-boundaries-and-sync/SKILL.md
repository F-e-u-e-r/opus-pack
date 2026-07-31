---
name: repo-boundaries-and-sync
description: Load before staging or committing anything in this working tree, after any merge that touches skills/ (live-copy sync duty), when a sync or diff check reports an unexpected missing directory, or when an untracked file sits at the repo root.
---

# Repo Boundaries and Sync

## Boundary map (verified 2026-07-30)

Published (tracked):

- `skills/`, `design-pack/` — pack source (the marketplace roots).
- `hooks/`, `.github/`, `.claude-plugin/` — enforcement, CI,
  manifests.
- `reviews/` — public review and threat-model records.
- `README.md`, `README.zh-Hant.md`, `LICENSE`,
  `THIRD-PARTY-NOTICES.md` — docs; the two READMEs mirror each other.

Gitignored (private — does not publish by default):

- `evals/`, `internal/`, `pack-eval-artifacts/`, `guideline*.txt` —
  fixtures burn on exposure; owner-private notes and drafts. These
  NEVER publish.
- `.claude/` — live install + settings.
- `skills-staging/` — retiring-architect scratch (`92314a6`);
  publishes only on explicit owner instruction.

## The working tree is permanently dirty-adjacent

- The repo root can carry UNTRACKED private session transcripts. On
  2026-07-30 it holds `chat-history.md` and `security-enhancement.md`
  (both full session transcripts — private content). Neither has ever
  entered a commit.
- Standing defense: stage by explicit pathspec, always
  (`git add -- <path>`); never any stage-everything form. The
  gitignore commit for skills-staging states the exact threat in its
  own message: it "keeps a stray `git add -A` from publishing"
  private content (`92314a6`).
- The transcripts' disposition (ignore pattern vs relocation) is the
  owner's pending decision — tracked in issue #100 (`UNCERTAINTY.md`
  item 1). Do not stage, quote, relocate, or edit them; quoting them
  in any public artifact also breaks the rule below.

## No owner quotes in public artifacts

- Standing owner directive (recorded 2026-07-24, applied throughout
  2026-07-29/30): the owner's message wordings never appear in PR
  bodies, commit messages, PR/issue comments, or any published file.
  Evaluation comments describe facts, findings, and decisions only.
  AUTH quotes live in session reports to the owner, nowhere public.
- Verified against practice: the sampled evaluation comments on
  #85/#94/#96 contain no owner quotes.

## Live-copy model and sync duty (three locations)

- `skills/` — the publish source (tracked).
- `.claude/skills/` — repo-local live install (gitignored).
- `~/.claude/skills/` — global install (outside the repo).
- The README Maintainer Notes' sync contract is canonical (on any
  divergence from this file, the README wins): after editing any
  SKILL.md, sync (`cp -R skills/. .claude/skills/`) and run the
  per-skill diff loop before pushing.
- TEMPORARY overlay on that contract (delete this bullet when
  UNCERTAINTY item 4 is settled): today the blanket `cp -R` would
  ALSO install `skill-vetting`, closing the known gap without the
  owner's decision. Until the owner settles it, copy the changed
  skill directories explicitly (`cp -R skills/<name>
  .claude/skills/`), skipping `skill-vetting`; do the same for the
  global copy (`~/.claude/skills/`), then cmp-verify both at the
  merge SHA (campaign practice, recorded in the close reports).
- Current expected state (2026-07-30) — this file is the SINGLE HOME
  for it; START-HERE/MANIFEST/UNCERTAINTY point here. Update this
  file first when the state changes: `skill-vetting` exists in
  `skills/` but in NEITHER live install, so the README loop errors on
  exactly that one directory. Known pre-existing state (the advisory
  hook ships opt-in; install pending an owner decision) — not drift
  you introduced. Every other skill dir cmp-clean at `79ca49c`.
- Removing or renaming a published skill: delete its old dir from the
  live installs by hand in the same change — `cp -R` never deletes
  (README Maintainer Notes).

## Done definition

Nothing from a gitignored/private zone appears in the staged set
(`git status` read, not assumed); every commit was staged by
pathspec; after a merge, both live installs match `skills/` except
the known `skill-vetting` gap — or that gap was closed deliberately
by the owner, in which case update this file's expected state.

## When NOT to use this skill

Deciding whether content may ship at all (covenant, markers, width)
→ `doctrine-change-conventions`. Campaign mechanics →
`contribution-gate-playbook`.

## Provenance

Distilled 2026-07-30 from the session transcript; verified same-day
against: `.gitignore` + `git check-ignore`; `git ls-files` top-level
enumeration; `92314a6`'s commit message; the two transcripts'
presence and untracked status (`git status --short`); README
Maintainer Notes; live-copy diffs run 2026-07-30 (both installs
differ from `skills/` only in `skill-vetting`); evaluation comments
(three read in full, all nine confirmed present).

Re-verify:

    git status --short
    for d in skills/*/; do
      diff -rq "$d" ".claude/skills/$(basename "$d")"
    done

(expected today: the two `??` transcripts, one error line for
`skill-vetting`, and — until the delivering PR merges — this
library's own tracked entries; anything else is new state —
investigate before acting).
