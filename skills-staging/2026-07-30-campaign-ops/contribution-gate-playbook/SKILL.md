---
name: contribution-gate-playbook
description: Load when contributor PRs are open on F-e-u-e-r/opus-pack and the owner asks to review, integrate, or merge them (any "follow our previous practice" form), or when a combined-*/integrate-* branch exists with its constituent PRs still open. Not for authoring doctrine (doctrine-change-conventions) or judging individual lens verdicts (gate-adjudication-and-folds).
---

# Contribution Gate Playbook

The observed, repo-verified pipeline that took #85–#89 → PR #90
(`a148180`), #91 → PR #93 (`92077a7`), and #94–#96 → PR #97 (`79ca49c`)
on 2026-07-29/30. Canonical gate doctrine is
`skills/cross-model-review/SKILL.md` — this file only pins how THIS
repo runs it. On any disagreement, the canon skill wins.

## Step 0 — pin the campaign set

Trigger: the owner's ask arrives.

- The set = the PRs open at instruction time (`gh pr list --state
  open`). Record the numbers before touching anything.
- A PR that opens mid-campaign is NOT swept in. Precedent: #91 opened
  2026-07-29T22:18Z, before #90 merged (23:34Z); it was excluded from
  #90, flagged to the owner, and handled as its own campaign (#93).
- The owner's ask authorizes THIS set; a later set needs a fresh ask
  (operational-rigor §2, per-invocation grant).

## Step 1 — verify each PR's verifiable claims

- Every repo-facing claim in a PR's text (a commit id, a section
  number, a "main already says X") is checked against the repo BEFORE
  the gate. Precedent: #85's `8f8413f` incident claim was verified
  in-repo, and the check is recorded in #85's evaluation comment.
- A claim that fails verification is a finding to surface and
  adjudicate, not something to silently fix or silently accept.

## Step 2 — build the combined branch

- One integration branch from current main, named by joining the PR
  numbers — `combined-85-86-87-88-89`, `combined-94-95-96` (multi-PR)
  or `integrate-91` (single PR) are the observed forms.
- Bring each PR's head branch local first (`gh pr checkout <number>`
  handles fork PRs too; the campaign merge commits show `pr-<number>`
  local branch names). Merging every head into the combined branch is
  what closes each constituent by reachability once the combined PR
  merges (observed on #85–#89 and #94–#96; GitHub marks them MERGED).
  Merge ASCENDING (lowest number first) — the house convention that
  keeps Provenance-entry stacking orderly.
- Provenance-tail conflicts are the expected conflict shape: stack
  both entries in PR order and reconcile with zero content loss (read
  both sides in full; nothing dropped silently).

## Step 3 — integration fixes, before round 1

Integrator additions are separate commits, named as integration
fixes, and are gate-reviewed like all other content. The recurring
three (commits `f529014`, `814d116`):

- in-body `unprobed` markers on clauses carrying only a
  Provenance-level label (the covenant's standing form);
- rewrap added lines over 80 characters without changing words;
- Provenance blank-line normalization (house continuous-prose style).

## Step 4 — checks green at every commit

- `python3 .github/checks.py` green before every push. The campaign
  PR bodies record checks green at every (fold) commit as the norm.

## Step 5 — run the gate rounds

- Lens lineup as run 2026-07-29/30 — a dated OPERATING RECORD, not a
  lineup to trust (the canonical rule is cross-model-review §1:
  discover reviewers at session time; the concrete run recipes are
  owner-personal and are NOT in this repo — ask the owner): grok-4.5
  high + gpt-5.6-luna ultra EVERY round; gpt-5.6-sol max joining
  every 3rd round, pre-commit rounds, and terminal-candidate rounds.
  Each campaign's records state its own cadence (PR #90/#93 bodies;
  for #97, its constituents' evaluation comments) — the newest
  campaign's record is the freshest statement; the standing wording
  is owner-set (UNCERTAINTY item 2).
- Lenses run as background CLI jobs writing verdict files. An empty
  or still-writing file is NOT a verdict; wait for the completion
  signal, then read the file.
- Each round's packet carries the current diff and the cumulative
  disposition ledger of prior rounds' folds and rejections.
- Judge what comes back per `gate-adjudication-and-folds`.

## Step 6 — reach a terminal state

- Normal close: TRIPLE PROCEED — every lens PROCEED in the SAME round
  (#93 r2; #97 r3).
- Non-convergence close: the bounded-loop close (cross-model-review
  §4 is the canonical loop bound; `gate-adjudication-and-folds` has
  this repo's precedents). Residuals are disclosed in the PR body.

## Step 7 — combined PR, CI, merge

- Push the branch; open ONE combined PR. Body shape: "What lands" per
  constituent / "Review gate" (rounds, lenses, fold trajectory,
  rejections) / "Integration notes" — the #90 shape; #93/#97 carry
  the same three blocks with lighter headings.
- Wait for the three CI checks (consistency, hook-suites,
  gate-template) by reading state directly — `gh pr checks 97`,
  substituting the campaign PR number; do not hand-roll wait loops
  (`failure-archaeology` entry 1).
- Merge as a merge commit, and ONLY on an owner ask whose words cover
  MERGING this campaign — write the AUTH line first (operational-rigor
  §2); this playbook is never that authorization. An owner ask to
  merge does not skip the CI wait: report pending checks and merge on
  green, or on the owner's explicit go given the pending state.
  Observed record, not a norm to reuse: the three campaign merges
  landed with reviewDecision REVIEW_REQUIRED and zero reviews — an
  owner-side bypass whose exact mechanism is not readable from here
  (UNCERTAINTY item 3). If a merge is blocked, surface the blocker;
  never probe for bypass paths.

## Step 8 — post-merge duties (all of them, in order)

1. Evaluation comment on EVERY constituent PR — maintainer-record
   shape: what was verified for that PR / gate folds applied to its
   text / final decision + merge SHA. Never quote the owner's
   messages (`repo-boundaries-and-sync`).
2. Sync the live skill copies and cmp-verify at the merge SHA
   (`repo-boundaries-and-sync` has the current expected state).
3. Probe debt: new `unprobed` markers are ALREADY the live queue —
   issue #92's canonical view is a grep, so there is no hand-kept
   list to update.
4. Update session memory with the campaign record.

## Done definition

Every constituent PR shows MERGED; the combined merge commit is on
main with CI green; an evaluation comment sits on every constituent;
live installs cmp-clean per the current expected state; no
private-zone path appears in any pushed commit (`git show --stat` on
each).

## When NOT to use this skill

- The owner asked a question about a PR (assess, don't integrate).
- The change is yours, not a contributor's — the gate doctrine still
  applies via cross-model-review, but the combined-branch and per-PR
  comment mechanics here assume third-party PRs.

## Provenance

Distilled 2026-07-30 from the 2026-07-29/30 session transcript
(`chat-history.md`, local) and verified same-day against: PR
#90/#93/#97 bodies and merge commits `a148180`/`92077a7`/`79ca49c`;
evaluation comments on all nine constituent PRs (three read in full,
six confirmed present with matching openers — UNCERTAINTY item 7);
issue #92; commits `f529014`/`814d116`/`6fa6154`/`5fa241b`/`83a038d`/
`1560b97`; `.github/checks.py`; `.github/workflows/checks.yml`;
`gh pr view <n> --json reviewDecision,reviews`; `gh pr view 91 --json
createdAt`.

Re-verify: `gh pr view 97 --json body --jq .body | head -45` — and if
a newer combined/integrate PR exists, read the newest body instead;
practice evolves campaign by campaign and the PR bodies are its
freshest public record.
