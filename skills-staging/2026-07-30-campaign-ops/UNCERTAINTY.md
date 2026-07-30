# UNCERTAINTY — campaign-ops library (2026-07-30)

Findings that are useful but cannot be stated authoritatively. Each
entry: claim / where it appeared / repo evidence / status / why
uncertain / what would resolve it / issue created? Every entry ends in
a safe default a zero-context reader can act on.

## 1. Untracked private transcripts at the repo root
- Claim: `chat-history.md` and `security-enhancement.md` (both full
  session transcripts — private content) sit untracked in the public
  repo's working tree; any stage-everything command would publish
  them.
- Appeared: the session's closing report flagged
  `security-enhancement.md` to the owner and asked for a disposition;
  no answer had arrived by session end. `chat-history.md` appeared
  after that session (it is that session's own transcript).
- Repo evidence: both present and untracked on 2026-07-30
  (`git status --short`); never in any commit; `92314a6`'s message
  names the exact threat ("a stray `git add -A`").
- Status: verified (existence/exposure risk); **user-must-provide**
  (disposition).
- Resolves it: owner picks a `.gitignore` pattern or relocates the
  files out of the repo. `.gitignore` is outside this delivery's
  allowed paths.
- Issue: yes — #100 (created 2026-07-30, single consolidated issue):
  https://github.com/F-e-u-e-r/opus-pack/issues/100
- Safe default: never stage them; pathspec-only adds; never quote
  their content anywhere public.

## 2. Exact wording of the standing gate cadence
- Claim: grok-4.5 high + gpt-5.6-luna ultra every round; gpt-5.6-sol
  max on "every 3rd round + pre-commit" (session-memory phrasing).
- Repo evidence: #90's body "gpt-5.6-sol max from r3" (fold commits
  show sol at r3 then r6–r11, the terminal candidates); #93's body
  "r2 pre-commit (grok + luna + sol-max)"; for #97 the cadence line
  lives in its constituents' evaluation comments ("gpt-5.6-sol max
  from r2"), not the body. All consistent with the phrasing; none
  states it as a standing rule.
- Status: **partially-verified** (pattern verified across three
  campaigns; the governing rule text is owner-set, session-recorded).
- Resolves it: owner confirmation, or the next campaign PR body.
- Safe default: run sol on every 3rd, every pre-commit, and every
  terminal-candidate round; when unsure, include sol — an extra lens
  costs a round, a missing lens costs the gate's meaning.

## 3. Merge-bypass mechanics ("admin merge")
- Claim: campaign merges used the owner's admin authority to bypass
  required review.
- Repo evidence: #90/#93/#97 all show reviewDecision REVIEW_REQUIRED
  with zero reviews, yet merged — a bypass demonstrably occurred.
- Status: bypass **verified**; the exact mechanism (gh `--admin`
  flag, ruleset bypass list contents) **user-must-provide** (ruleset
  config needs owner/admin access to read).
- Resolves it: owner states the flag/ruleset arrangement.
- Safe default: a session never merges without the owner's ask for
  that campaign; if a merge is blocked, surface the blocker — do not
  probe for bypass paths.

## 4. `skill-vetting` absent from both live installs
- Claim: deliberate pending-adoption state (the advisory hook is
  opt-in; "Workstream B"), not an overlooked sync failure.
- Repo evidence: `skills/skill-vetting/` exists; both live installs
  lack it (diffs run 2026-07-30); README documents the hook as
  optional. Intent is session/memory-recorded only.
- Status: state **verified**; intent **user-must-provide**.
- Resolves it: owner either installs it or records the deferral.
- Safe default: do not install or uninstall it yourself; expect the
  README sync loop to error on exactly this directory.

## 5. The 2026-07-12 local library's stale spots
- Claim: the older root-level `skills-staging/` library (local-only,
  gitignored) is stale where it overlaps current practice.
- Verified examples (2026-07-30): its release-and-publish requires a
  version bump per substantive PR (contradicted by #84–#97 at
  0.1.16); its re-verify command greps `README.zh-TW.md` (renamed
  `README.zh-Hant.md` in `c15c29d`-era work — the old path no longer
  exists); its gate-ops file records the 2026-07 lineup gpt-5.5 +
  grok-4.5 max (differs from the campaign lineup; both are
  date-stamped volatile by their own rules).
- Status: **historically-valid**; the files are the owner's local
  scratch, not touched by this delivery.
- Resolves it: an owner-sanctioned refresh or retirement of the old
  library.
- Safe default: for overlapping topics, canon skills win, then this
  dated library; verify any old-library command against the repo
  before running it.

## 6. The sol-unverified r11 folds in #90
- Claim: the final two r11 folds (`git add --` hardening; the
  fast-forward scope sentence) merged without sol re-review.
- Repo evidence: the two folds are named in `83a038d`; #90's body
  discloses that the final two folds land sol-unverified without
  naming them; grok/luna never objected; CI green.
- Status: **verified** as a disclosed, accepted residual.
- Resolves it: nothing owed; a future finding against those folds is
  a new finding.
- Safe default: do not re-open #90's gate; treat the disclosure as
  the record.

## 7. Evaluation comments — verification depth
- Claim: all nine constituent PRs (#85–#89, #91, #94–#96) carry a
  maintainer evaluation comment.
- Repo evidence: #85, #94, #96 read in full on 2026-07-30 (shape and
  no-owner-quotes confirmed); the remaining six confirmed present the
  same day with matching "Evaluation record (maintainer)" openers
  (on #86 it is the SECOND comment — the first is the contributor's).
- Status: **verified** (presence, all nine; full-text read, three).
- Resolves it further: read the remaining six in full before citing
  their details.
- Safe default: when writing new evaluation comments, follow the
  three fully-read ones' shape.

## 8. Session-memory phrase "evals/round4 … COMMITTED"
- Claim (memory, 2026-07-23): round-4 eval design "committed".
- Repo evidence: `evals/` is gitignored with zero tracked files
  (2026-07-30) — nothing eval-related is committed to this repo.
- Status: memory claim **unverified as written**; repo state
  verified. Likely loose wording for "written to the private evals
  tree".
- Resolves it: owner's private tree; not resolvable here.
- Safe default: treat `evals/` as private and ignored; never cite a
  tracked evals path.

## 9. This library's own delivery mechanism
- Claim/process note: delivering skills under a gitignored path
  required `git add -f`, per the explicit retiring-architect task
  instruction; `.gitignore` was not modified.
- Status: verified (this delivery).
- Safe default: this is NOT precedent for publishing other ignored
  zones (`evals/`, `internal/`, `.claude/`, `guideline*.txt`,
  `pack-eval-artifacts/`) — those stay private absent the same kind
  of explicit owner instruction.
