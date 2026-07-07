# Fresh-Context Review Record - 2026-07-07

Purpose: preserve the independent review findings for `opus-pack` so future
sessions do not depend on chat context. This record captures the maintainer
handoff summary from the fresh-context review and the follow-up local review.

Scope reviewed:

- Six skills under `skills/`
- The mirrored live install under `.claude/skills/`
- `ground-truth-gates/template/`
- `hooks/gate-before-commit.sh`
- English and Traditional Chinese READMEs

Review lenses from `skill-authoring` section 6:

1. Factual: paths, commands, claims, and drift-prone facts.
2. Doctrine: contradictions between skills or with the pack's own rules.
3. Usability: whether a zero-context reader can trigger and follow the rules.

## Blocking Findings Fixed

1. `delegation-and-review` originally said to spawn an agent only when the
   orchestrator can immediately do other work. That contradicted the pack's
   own mandatory fresh-context review and critic rules. Resolution: section 1
   now names three sufficient reasons to spawn: throughput, independence, and
   context protection.
2. The golden gate's threshold was not clearly enforced through `run-all.sh`.
   Resolution: the team threshold is now `MIN_DEFAULT` in `golden/run.mjs`,
   and `run-all.sh` runs the golden gate with that default.

## Important Findings Fixed

- `gate-before-commit.sh` depended on `jq`; the hook now blocks likely commits
  when `jq` is missing instead of silently allowing an ungated commit, while
  non-commit commands still pass.
- `project.sh` is documented to run from the repo root so commands such as
  `eslint .` inspect the project rather than only `checks/`.
- `replay/run.mjs --update` is documented as an orchestrator/reviewer action,
  not the editing worker's own call.
- `replay/run.mjs` refuses an empty corpus.
- Dispatch packet fields were consolidated to `delegation-and-review` section 2
  as the single source of truth.
- Web refresh-token guidance now uses a path-scoped `HttpOnly; Secure;
  SameSite` cookie or server-side sessions.
- `skill-authoring` section 1 now requires positive/negative examples where
  misreading is costly, rather than requiring heavy examples for every rule.

## Follow-Up Local Review Fixes

- `golden/run.mjs` now refuses an empty `cases.jsonl` unconditionally, including
  ad-hoc `--min 0` runs.
- `gate-before-commit.sh` now checks whether gates exist before requiring `jq`,
  and missing `jq` no longer blocks unrelated non-commit Bash calls.
- The review record itself was added here to satisfy the pack's files-as-state
  discipline.
- Stray `.DS_Store` was removed.

## Verification Commands

Run these after edits:

```bash
diff -rq skills .claude/skills
bash skills/ground-truth-gates/template/run-all.sh
node --check skills/ground-truth-gates/template/golden/run.mjs
node --check skills/ground-truth-gates/template/replay/run.mjs
bash -n skills/ground-truth-gates/template/run-all.sh
bash -n hooks/gate-before-commit.sh
```

Hook behavior to re-check with a disposable fixture:

- Non-commit Bash command passes.
- Green `git commit` command passes.
- Red `git commit` command exits 2 and reports gate output.
- Missing `jq` plus non-commit command passes.
- Missing `jq` plus likely `git commit` exits 2.
