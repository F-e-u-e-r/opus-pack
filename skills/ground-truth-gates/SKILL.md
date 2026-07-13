---
name: ground-truth-gates
description: Build executable verification gates (golden set, replay corpus, project checks) so "it works" becomes a checked fact instead of a claim. Load when changing any LLM-judgment step (classify/extract/route/prompt), refactoring logic that processes real logged data, designing tests for a fix, setting up a commit/ship gate for a project, designing a runtime guard (a hook, validator, or auth check) and its fail direction, or when you are about to trust a passing test that has never been shown able to fail. Also the reference for what "proof gate" means in delegation-and-review packets. Do NOT load for one-off scripts or exploratory spikes — plain operational-rigor covers those.
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
| **project** | "Do build/tests/types/lint pass?" | Drop a `checks/project.sh` with `npm test`, `tsc --noEmit`, an SCA scan failing on critical/known-exploited (`npm audit` / `pip-audit`), etc. |

A starter implementation lives in this skill's `template/` directory —
copy it into the project as `checks/` and wire it up (~15 min per gate):

**golden:** replace `golden/cases.jsonl` with 30–50 *real, hand-labeled*
examples (`{"input": ..., "label": ...}` per line) — a tiny set is gameable;
a perfect score on a small set is an overfit warning, not a win. Replace
`classify()` in `golden/run.mjs` with a call to the real system (keep it
deterministic per input). Set the team's bar by editing `MIN_DEFAULT` in
`golden/run.mjs` — that is what `run-all.sh` (and any hook/CI on top of it)
enforces; the `--min` flag only overrides ad-hoc runs.

Three rules make the golden gate earn its keep:

- **Anonymize structure-preserving** — replace PII values with same-shape
  stand-ins (digits for digits, `client@example.com` for an email, a
  placeholder name like `Jordan Lee` for a name). `REDACTED` destroys the
  very shapes the logic keys on.
- **Include hard negatives** — real inputs that look like a match but must
  fall through. That is where regressions hide and where synthetic cases
  never go.
- **Score cost-asymmetrically** — name the class of wrong output that
  triggers a real, unconfirmed action (wrong route, wrong send) and treat
  any instance of it as a hard failure, not something aggregate accuracy can
  average away. The starter `run.mjs` implements this: set `DEFER_LABEL` to
  your safe-fallback label and the gate hard-fails on any false route
  regardless of accuracy.

The golden runner doubles as an experiment grader: pre-register expected
outputs as cases before any runs, then grade with code, not impressions —
no harness, no experiment.

**replay:** replace `replay/corpus.jsonl` with a representative sample of
real logged inputs. Replace `transform()` with the step being changed. Run
`node replay/run.mjs --update` once to freeze current behavior; after each
edit, plain `node replay/run.mjs` — **0 diffs = safe; any diff = the exact
records that moved.** Re-`--update` only after eyeballing an *intended*
change, and only as the orchestrator/reviewer — never the editing worker's
own call (rule 4 below: gate changes are not the worker's to make).

**replay variant — parity (no corpus):** a refactor of pure-ish logic (config parsing, path
handling, formatting) often has no logged corpus to replay. Keep the pre-change
implementation *callable* — a pinned import, a second checkout, or
`git show <base>:<path>` copied into a `_old` module — and run old vs new over a
declared input set, asserting identical output/exit (allow-list any intended
diffs). It is the replay gate for code you are refactoring when you have nothing
logged. (Freezing the old source *text* as a string is not a parity test — it
never runs the old code.)

## What makes a gate real (task-relative test discipline)

A generic green test is not proof. A gate is real only if:

1. It exercises the **task trajectory** — input, production path, state
   transition, observable output — not a reimplementation of the logic.
2. It would **fail under the broken behavior**. Run both arms where practical —
   broken arm fails, fixed arm passes — and prove a *negative* test can fail by
   running it against a known-bad arm. Instrument the failure's **own** signal,
   not a proxy: an unchanged field or intact-looking output can pass while the
   failure still occurred.
3. The **easy fake pass is named** and closed — hardcoded expected value,
   weakened assertion, testing the mock, a test that compiled but was never
   registered/run, a permanently `#[ignore]`/`.skip`ped backlog test that reads
   as coverage. Confirm a new test actually *runs* — the runner lists it, or it
   fails when you deliberately break the code — not merely that it compiles. For
   a guard/error path, assert three things, not just the exit code: the
   returncode, a message string unique to THIS check (many errors share exit 2),
   and that the dangerous side-effect did NOT occur (`assertNotIn`).
4. **Nobody weakens a gate to turn it green.** A worker satisfies the gate, never
   edits it — gate changes are the orchestrator's call. Three corollaries:
   - For an *immutable policy-checker* (not an ordinary test), run it from a
     pinned trusted base — `git show <base-SHA>:<gate>` or the protected ref's
     copy — against the PR's content as *data*, so the same PR can't edit the
     rules it must pass; pin the checker's dependencies too (a base script that
     imports PR-controlled helpers is still compromised), and protect the workflow
     path itself with branch rulesets / required reviewers, not CODEOWNERS alone.
     Ordinary tests need only independent approval to change, not this.
   - Recompute any integrity value (hash, fingerprint) from a trusted base;
     never trust the value an artifact carries about itself.
   - A test edit is a contract edit: to change a pinned/assertion test, state
     which contract changed and who approved it (ADR/owner). If you can't, you
     are fixing the wrong direction.
5. For important behavior claims, prefer **two independent truth sources**
   (e.g., client output + server state, logs + durable artifact). Two sources
   that agree with each **other** but only moderately with ground truth are
   correlated bias, not independence — score cross-source and same-source
   agreement separately (two models agreeing is one lens, not two). A metric
   clearing a threshold is *evidence*, never *authorization*: keep the go/no-go a
   separate recorded decision.

**A red result is not automatically a real defect** — but ruling one
"environmental" is a gate change, not the worker's call (rule 4): quarantine it
with dated evidence and orchestrator sign-off; never silence it by weakening the
assertion. Use explicit states instead of one red/green axis: **PASS**
(dated evidence), **EXPECTED-FAIL** (a known environmental gap carried in a
visible non-blocking lane — not turned green), **N/A** (the environment
structurally cannot exercise it), **BLOCKED** (couldn't run — authorization,
cost, or side-effect).
- ✅ "Fails only on the sandbox's missing GPU → EXPECTED-FAIL, reason logged,
  orchestrator confirmed."
- ❌ "This fail looks environmental — I'll relax the assertion so it goes green"
  (that deletes the safety check the test was proving).

**Evidence class matters:** a mock / proxy / staging pass is not real-environment
sign-off — never let one launder into the other. A "live smoke" run itself needs
an authorized environment and still obeys the spending/destructive gates;
without that the item stays BLOCKED, not Pass.

Preserve evidence: the command run, the log, the artifact, or the CI URL —
so the next session can re-check the claim instead of trusting it.

If a judgment step's outputs are compared across time, **version it** — a
threshold or rule change is a version bump, not an edit (it changes the meaning
of every prior comparison); keep a pinned canonical scorer separate from a
mutable what-if mode, and require deterministic output on identical input (or a
declared tolerance for a stochastic scorer). If a generated file is committed,
gate on regenerate-and-`git diff --exit-code`; edit
the source and regenerate, never hand-edit the artifact, and run the gate even
on changes you believe don't touch it, to prove no accidental perturbation.

## Designing the guard itself

A gate proves a claim; a guard (a hook, middleware, validator, auth check)
enforces one at runtime — and has its own failure design:

- **Verify the guard along its real exposed path**, not a convenient internal
  call. A guard can pass its own unit test yet be **dormant on the entry
  surface** — the untrusted HTTP/MCP/CLI/webhook boundary where its parameter
  was never wired. Exercise it through that surface; malformed / typo /
  explicit-null input there must fail **closed**, never be silently treated as
  "omitted" — except a guard that itself gates every action, whose fail-direction
  (and its documented fail-open gap) is the next bullet. A CI that mocks the
  external dependency proves your logic, not the live integration — run a live
  smoke before trusting it.
- **Choose the fail-direction per failure mode and record why.** A security,
  integrity, destructive, spending, publishing, or gate-enforcement control fails
  **closed** on the threats and malformed input it detects — deny, don't wave
  through. The hard case is a guard that *itself gates every action* (a Bash
  pre-tool hook): it can't hard-fail-closed on every internal error without
  bricking the agent, so it fails closed on what it detects and raw-scans an
  unparseable *command*, while a malformed envelope or other internal error still
  fails open — a documented gap to narrow, never a licence to widen. Keep that
  fail-open surface minimal. A purely-advisory guard (telemetry) may fail open
  freely; when unsure, treat it as fail-closed. ✅ "the credential gate blocks the
  deletion it detects and raw-scans an unparseable command; its malformed-envelope
  path fails open today — a disclosed gap." ❌ "the hook is flaky and blocks my
  commands, so I'll make it fail-open" — that converts a guard into a
  rationalized bypass.
- **A relief valve is a pre-existing, owner-designed, friction-plus-log override
  — never one an agent invents to unblock itself**, and never added to a control
  the owner designated non-bypassable (an immutable policy-checker). Security /
  destructive / spending controls default to non-bypassable *unless* the owner
  ships such an override (like this pack's own `CRED_GATE_APPROVED`, whose value
  is the friction and the audit line, not tamper-proofing — a determined agent
  can still set it). Removing an existing owner-shipped valve "to harden"
  re-creates the deadlock it was designed to prevent; *adding* an `*_ACK` /
  `--force` path to get past a gate is the confirmation-gate violation
  (operational-rigor §2), not hardening.
- **State what the guard does NOT guarantee** and its known-accepted bypasses in
  its header, so maintainers neither over-trust it nor destabilize it by chasing
  inherent bypasses into the parser. (At a trust boundary, prefer structural
  prevention over a content classifier — see security-architect's "Secure
  ingestion"; don't re-derive it here.)

## When NOT to build a gate

Do not add ceremony to a one-off script or an exploratory spike. The gate
pays where the same judgment or transform will be edited repeatedly, or
where a regression would be silent. One gate that is actually run beats five
that are aspirational.

## Provenance

Distilled 2026-07 from: private checks/-harness design notes (the
prose-vs-ground-truth finding, plus — same author's 2026-07 harness export —
cost-asymmetric scoring, shape-preserving anonymization, hard negatives, the
experiment-grader rule), fable-agent-orchestration `935e4a3`
(task-relative-test-gate, fail-under-broken, two truth sources).
The project-gate SCA example (2026-07-12) mirrors security-architect's
SCA-in-CI line (same 12-source audit; ideas only, no code).
The 2026-07-13 additions (the parity replay-variant; the extended gate-real rules —
mock≠sign-off, error-path three-part assertion, base-ref execution,
correlated-model-bias, compiled-but-not-run, environmental-FAIL quarantine,
version-the-classifier, regenerate-and-diff; the "designing the guard itself"
section) distill a cross-repo mining pass over seven independent
retiring-architect `skills-staging/` libraries (class-distilled convergence — a
rule's weight is how many of the seven independently rediscovered it).
`template/` scripts are self-contained (Node + bash, zero deps) and were run
green on 2026-07-06 with Node v23; re-verify with `bash template/run-all.sh`.
