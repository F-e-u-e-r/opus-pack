---
name: failure-archaeology
description: Load when about to wait on CI in a hand-rolled loop, ship a doctrine line that states runtime behavior, adopt or delete a leftover local branch, add a contributor clause without a probe marker, or re-open something this session settled (version bumps, mid-campaign PRs, the sol r11 residue, the untracked transcripts).
---

# Failure Archaeology — 2026-07-29/30 session

Dead ends, traps, and residue from the contributor-PR campaign
session, so no future agent re-walks them. Entry fields per the
project-skill template: disposition / what happened / mechanism /
standing rule / residue location.

## 1. dead — hand-rolled CI wait loop

- What: an until-loop ("wait until no check is pending") was launched
  to wait for PR #90's CI, then stopped; the session's own live note
  hedged that an inverted loop condition would return early. A
  transient API error landed in the same window. (Transcript-recorded
  only — the stopped loop left no repo artifact.)
- Mechanism: a hand-written wait predicate is unverifiable from the
  outside — when it exits you cannot distinguish "done" from
  "predicate wrong", and a mid-wait interruption leaves no state.
- Standing rule: read CI state directly and re-derive on every
  resume — `gh pr checks <n>` — instead of encoding the wait
  condition in a loop you cannot test. The session's later CI waits
  (#93, #97) completed as plain background status checks.
- Residue: none (the loop was stopped; nothing landed).

## 2. dead — untested runtime-semantics text in #96 (fixed in gate)

- What: contributor text asserted `os.environ["KEY"]` "silently reads
  empty" in non-interactive shells, and its ❌ example used `'\\n'`
  inside single quotes.
- Mechanism: prose about runtime behavior that nobody had executed.
  Both lenses converged on the KeyError correction (r1); sol+luna
  refined `.get()` → `None` (r2); a lens executed the printf example
  and showed `'\\n'` emits a literal backslash-n, so the example
  could never produce the incident it described.
- Standing rule: runtime claims in doctrine get executed verification
  before shipping (`gate-adjudication-and-folds`).
- Record: `6fa6154`, `5fa241b`, PR #97 body, #96's evaluation
  comment.

## 3. recurring-trap — covenant markers missing on contributor clauses

- What: #95's clause carried only the Provenance-level label
  (`f529014`); the #85–#89 batch needed six in-body markers added
  (`814d116`); a sweep found five Provenance entries missing the
  contributor-reported label (#90 body).
- Mechanism: contributors satisfy the covenant at the Provenance
  level and miss the in-body standing form; every batch re-imports
  the same gap.
- Standing rule: sweep new clauses for marker + label pairing as an
  integration fix BEFORE gate round 1 (`doctrine-change-conventions`).
- Tripwire: a new clause whose opening sentence lacks the marker
  while its Provenance entry says unprobed.

## 4. recurring-trap — your own folds introduce defects

- What: #90's gate caught the staged-diff gate's circular trigger
  (the catch is named in #90's body; that an earlier fold introduced
  it is session-recorded).
- Standing rule: folds are attack surface for the next round; no
  terminal close on unreviewed folds outside the disclosed
  bounded-loop residual (`gate-adjudication-and-folds`).

## 5. residue, not in-progress work — local branch graveyard

- What (observed 2026-07-30): local branches with deleted upstreams
  (`[origin/…: gone]`: integrate-pr62-65, integrate-pr68-69,
  phase-a…d, hook-*, delegation-*) plus never-pushed mine-* and
  pr3x-review branches from earlier mining campaigns.
- Standing rule: residue — do not adopt-and-finish, do not delete
  without the owner's ask (cleanup mutates the owner's workspace;
  operational-rigor §2). Observed mechanics: this repo merges with
  TRUE merge commits, so `git branch --merged main` DOES list all of
  these branches as merged (verified 2026-07-30: 37 of 37) —
  reachability is the authoritative signal here. The canonical
  squash-merge caveat ("squash defeats `--merged`") applies to
  squash-based repos, not to this one's observed history. The
  never-pushed mine-*/pr3x-review branches are also listed as merged
  — their content landed via other branches; still residue, not live
  work.
- Residue location: `git branch -vv` on the owner's machine.

## Deliberately-not-done (do not "helpfully" complete)

- No version bump for #84–#97 — doctrine-only merges do not bump
  (`doctrine-change-conventions`). Do not "fix" the badge forward.
- #91 was NOT merged into #90 although it was open before #90 merged
  — mid-campaign arrivals stay out of the pinned set
  (`contribution-gate-playbook` step 0). It got its own campaign
  (#93) instead.
- No r12 for #90 — sol's r11 residue closed under the bounded-loop
  precedent and ships labeled `sol-unverified` in the PR body. Do not
  re-open the campaign to "finish" sol's convergence; a future
  finding against those two folds is a NEW finding, handled fresh.
- `security-enhancement.md` and `chat-history.md` stay untouched at
  the repo root — owner disposition pending (issue #100;
  `UNCERTAINTY.md` item 1). Do not move, stage, or edit them.

## Re-verify

`git branch -vv | grep -c ': gone'` (nonzero = residue still
present) and `gh pr view 90 --json body --jq .body | grep -n
'sol-unverified\|bounded'` (the disclosed residual is still the
record). Entry 5's branch list is machine-local — re-observe it
rather than trusting this file's snapshot.

## Provenance

Distilled 2026-07-30 from the session transcript; commits, PR bodies,
and comments cited inline were re-read in-repo the same day; the
branch list was observed directly (`git branch -vv`, 2026-07-30).
