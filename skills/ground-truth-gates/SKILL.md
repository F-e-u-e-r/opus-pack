---
name: ground-truth-gates
description: Build executable verification gates (golden set, replay corpus, project checks) so "it works" becomes a checked fact instead of a claim. Load when changing any LLM-judgment step (classify/extract/route/prompt), refactoring logic that processes real logged data, designing tests for a fix, or setting up a commit/ship gate for a project. Also the reference for what "proof gate" means in delegation-and-review packets. Do NOT load for one-off scripts or exploratory spikes — plain operational-rigor covers those.
---

# Ground-Truth Gates

**The core finding:** more prose rules do not improve a capable model on
verifiable work — its gating habits are already native. What is missing is
**something to gate against**. Invest in executable ground truth, not in
longer instructions. Build gates first where judgment work happens
(classification, extraction, routing, prompt output) — that is where habits
are weakest and where a gate converts open-ended quality into a number plus
a diff.

## The one command

Once `template/` has been copied into the project as `checks/` (wire-up below):

```bash
bash checks/run-all.sh
```

Discovers every `checks/*/run.mjs` (plus optional `checks/project.sh`), runs
each, prints `PASS`/`FAIL` per gate, exits non-zero if any fail. That is the
commit/ship gate: "all green" stops being a claim and becomes a checked fact.

## The three gates

| Gate | Question it answers | Where it pays |
|---|---|---|
| **golden** | "Is this prompt/classifier actually better, by how much, and which cases does it miss?" | LLM-judgment steps. |
| **replay** | "Did my change alter output on real logged inputs, and exactly where?" | Refactors and regex/prompt tweaks over production data — catches silent drift reading the code cannot see. |
| **project** | "Do build/tests/types/lint pass?" | Drop a `checks/project.sh` with `npm test`, `tsc --noEmit`, etc. |

A starter implementation lives in this skill's `template/` directory —
copy it into the project as `checks/` and wire it up (~15 min per gate):

**golden:** replace `golden/cases.jsonl` with 30–50 *real, hand-labeled*
examples (`{"input": ..., "label": ...}` per line) — a tiny set is gameable;
a perfect score on a small set is an overfit warning, not a win. Replace
`classify()` in `golden/run.mjs` with a call to the real system (keep it
deterministic per input). Set the team's bar by editing `MIN_DEFAULT` in
`golden/run.mjs` — that is what `run-all.sh` (and any hook/CI on top of it)
enforces; the `--min` flag only overrides ad-hoc runs.

**replay:** replace `replay/corpus.jsonl` with a representative sample of
real logged inputs. Replace `transform()` with the step being changed. Run
`node replay/run.mjs --update` once to freeze current behavior; after each
edit, plain `node replay/run.mjs` — **0 diffs = safe; any diff = the exact
records that moved.** Re-`--update` only after eyeballing an *intended*
change, and only as the orchestrator/reviewer — never the editing worker's
own call (rule 4 below: gate changes are not the worker's to make).

## What makes a gate real (task-relative test discipline)

A generic green test is not proof. A gate is real only if:

1. It exercises the **task trajectory** — input, production path, state
   transition, observable output — not a reimplementation of the logic.
2. It would **fail under the broken behavior**. Where practical, run both
   arms: broken arm fails, fixed arm passes. A test that cannot fail proves
   nothing.
3. The **easy fake pass is named** — the way this gate could go green without
   the claim being true (hardcoded expected value, weakened assertion,
   testing the mock) — and closed.
4. **Nobody weakens a gate to turn it green.** A worker's job is to satisfy
   the gate, not to edit it; gate changes are the orchestrator's call.
5. For important behavior claims, prefer **two independent truth sources**
   (e.g., client output + server state, logs + durable artifact).

Preserve evidence: the command run, the log, the artifact, or the CI URL —
so the next session can re-check the claim instead of trusting it.

## When NOT to build a gate

Do not add ceremony to a one-off script or an exploratory spike. The gate
pays where the same judgment or transform will be edited repeatedly, or
where a regression would be silent. One gate that is actually run beats five
that are aspirational.

## Provenance

Distilled 2026-07 from: a private checks/-harness design note (used with
permission; the prose-vs-ground-truth finding), fable-agent-orchestration `935e4a3`
(task-relative-test-gate, fail-under-broken, two truth sources).
`template/` scripts are self-contained (Node + bash, zero deps) and were run
green on 2026-07-06 with Node v23; re-verify with `bash template/run-all.sh`.
