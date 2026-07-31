# Manifest — skill-vetting hardening library (2026-07-30)

Extracted from the `security-enhancement.md` session transcript by a five-screener
+ three-reviewer + final-gate orchestration, and verified against the repository
at HEAD `79ca49c`. The session is the Workstream-B skill-vetting hardening
campaign, shipped as **PR #83** (`7cd2af6`, merged 2026-07-26 — an ancestor of the
default branch; no local drift in `hooks/` or `.github/`).

## Delivery / tracking state

By DEFAULT `skills-staging/` is gitignored local working material (repo
`.gitignore`; policy tracked by a GitHub issue — filed as #98 per this session,
confirm with `gh issue view 98`). For THIS PR delivery the seven files
were **force-added** (`git add -f`), so they are now tracked and WILL be published
by the delivery commit — that is the intent. Because they are tracked, `.gitignore`
no longer excludes them; stage only by explicit pathspec under this directory and
never `git add -A` (a GitHub issue — filed as #100 per this session; confirm with
`gh issue view 100` — tracks the untracked session transcripts a stage-everything
command could sweep in). Before install, review through the pack's three-lens +
cross-family ladder, then copy the four skill directories into `.claude/skills/`
by the repo's documented convention (NOT the START-HERE/MANIFEST/UNCERTAINTY files).

**The trio (START-HERE / MANIFEST / UNCERTAINTY) is REVIEW-ONLY and is NOT
installed; no installed skill hard-depends on it.** Each skill carries its own
load-bearing open-items locally (e.g. security-invariants' "Known open items"
section) and cites the durable `reviews/2026-07-25-skill-vetting-*.md` threat
model + design records as the authoritative `NOT MET`/OPEN source. A skill's
"see UNCERTAINTY.md" pointer is a review-time convenience for the fuller
safe-defaults, not an install-time dependency — after install, the authoritative
open-items list is the threat model's own markers.

## Runtime and dependencies

- **Execution:** the skills are instruction text; their re-verify blocks assume
  **Bash** (the three re-verification wrappers this library cites —
  `test-skill_snapshot.sh`, `test-skill-vetting-advisory.sh`,
  `test-mutation_matrix.sh` — are `#!/usr/bin/env bash`, not plain POSIX sh; the
  repo carries more `test-*.sh` wrappers, all Bash), Python 3 (stdlib only — the
  hooks and checks import nothing
  external), and Git. `gh` (authenticated) is optional and only for the PR/issue
  re-verify lines; without it those are `user-must-provide`.
- **Sibling skills (cross-references resolve when installed):** `operational-rigor`
  (§2 authorization, §5 twin-sweep/three-defects), `delegation-and-review` (§1
  session-time lineup, §3 miss-costly-audit stop rule, §7 external-content),
  `cross-model-review` (family-diversity + no-shallow-tier gate), `ground-truth-gates`
  (proof-gate doctrine). Where a sibling is absent the pointer degrades to plain
  context; re-resolve section numbers on install (skill-authoring §3).
- **Target runtime:** the re-verify commands were exercised on macOS (the session
  machine); they are portable to **macOS/Linux with Bash** (matching the live
  primitive's stated platform scope), not to a bare POSIX shell.
  `user-must-provide`: confirm the deployment runtime before relying on OPS-11's
  macOS-specific tooling notes.

## The four skills — what each is ← the repo evidence that would falsify it

Open the cited source to re-verify. The security skill's evidence is fully
repo-resolvable (file:line, commit, threat-model section, in-code comment). The
mutation and archaeology skills are MOSTLY repo-resolvable, with a few
**history-only anecdotes** that have no repo source (they come from the session):
the `tee`-piped exit-code incident (archaeology + R4), the "~14×" doc-drift count,
and R8's `seq -w`/`field()` probe examples. The review-ops skill has the most
history-only content — several incidents are sourced from the session transcript
and the gitignored `internal/gate-b-2026-07-25/` ledger, NOT independently
repo-verifiable; its canonical-rule citations DO resolve. None of the skills cite
the orchestration's internal screener IDs. The normalized evidence inventory
(which of the five screeners surfaced each lesson) is an orchestration artifact,
not shipped here.

- **skill-vetting-security-invariants** — 7 shipped security invariants of the
  observation/persistence primitive and its trust boundary ← `hooks/skill_snapshot.py`
  (`_anomaly_snap`:526, `_resolve_dot_base`:847, `_cli_status`:1152-1189, budget:326),
  `hooks/skill-vetting-advisory.py` (`skip_baseline`:489), `hooks/test-skill-vetting-advisory.py:132`,
  `skills/skill-vetting/SKILL.md` §3, threat-model goals G1–G6+G3-SHELL and
  **invariants I1–I11** (I12–I17 are the round-8 design's, unimplemented). Each
  re-checked against current source 2026-07-30. These are repository-verified
  facts about shipped behavior.

- **mutation-matrix-evidence-discipline** — 8 rules for trusting/extending the
  evidence harness and the test-honesty it enforces ← `hooks/mutation_matrix.py`
  (`check_mutation`:86, `MEASUREMENT_PATHS`:245, `identity_snapshot`:253,
  `_blob_matches_head`:448, `run_id`:455, pristine-control:583/608),
  `.github/checks.py` (duplicate-def check 5 :435-457 before the final decision
  :484-486, over the two named hook suites only; mutation_matrix env-read gate
  :466-481), `hooks/mutations.json`. The authoritative run is
  `mutation_matrix.py --authoritative` (not `test-mutation_matrix.sh`, the harness
  unit suite). Applies `ground-truth-gates`' proof-gate doctrine to this tool.

- **skill-vetting-hardening-archaeology** — the campaign's dead ends with
  disposition tags + the "fold-time-invented-mechanism is the defect" meta-signal,
  the deliberately-NOT-done D1–D5 designs, and the rejected options ← round-5/6/7
  defect table and answered-vs-open questions in
  `reviews/2026-07-25-skill-vetting-round8-design.md`, commits `550689d`
  (false-claim) + `b427bf8` (correction) both in history, round-6/8 in-code
  comments in the two hooks, `.github/workflows/checks.yml` (CI reorder). Failure
  archaeology of a named campaign.

- **security-hardening-review-ops** — 12 reviewer-orchestration and delivery-
  governance rules ← the session transcript, gate ledger `internal/gate-b-2026-07-25/`
  (gitignored — a local record), PR #83 merge, and the installed `operational-rigor`
  / `delegation-and-review` / `cross-model-review` doctrine it defers to. These are
  **project observations and governance decisions from the campaign**, not
  pack-wide behavioral doctrine — each defers to the canonical skill it cites for
  stop conditions and model selection (OPS-1's overlap figure is an n=1 observation,
  not a law).

## On probe markers and the house covenant

The pack covenant (`README.md`) requires a NEW behavioral rule to ship with a
discriminating probe/trap OR an in-body `unprobed` label. This library adds no
new PACK-WIDE behavioral doctrine: the invariant and harness skills are
repository-verified facts (their falsification path is the cited source), the
archaeology is failure history, and the review-ops rules are project observations
that DEFER to already-covenanted canonical skills rather than asserting new
behavior. Where a rule restates an existing pack behavioral rule it points at that
rule (e.g. the mutation core principle → `ground-truth-gates`; OPS stop conditions
→ `delegation-and-review`/`cross-model-review`) rather than re-asserting it — noting
that OPS-1/OPS-5 TIGHTEN those canonical rules for this campaign (a hard cap, a
human-authorization gate) rather than purely restating them; a tightening that
composes with the canonical rule owes no new probe. Of the twelve OPS rules,
OPS-2/6/8/9/10/11 have no canonical counterpart and each already carries an
in-body `(unprobed — project observation, no probe)` marker (probe debt tracked
in issue #105); OPS-1/3/4/5/7/12 cite and defer to a canonical rule. If a
future edit turns any of the deferring rules into a standalone behavioral
claim, that edit owes the covenant's probe-or-`unprobed` marker in the same
way.

## Re-verification

Each skill ends with its own re-verify block. The whole library's ground pin:
`git merge-base --is-ancestor 7cd2af6 HEAD` must succeed (PR #83 shipped state is
present) and `python3 .github/checks.py` must be green. If PR #83 has been
superseded by later skill-vetting work, re-verify each invariant against the new
source before trusting these files.
