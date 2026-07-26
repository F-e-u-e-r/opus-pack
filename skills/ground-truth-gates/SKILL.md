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

These rules make the golden gate earn its keep:

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
- **Validate the capture instrument, then taint on defect.** When cases are
  minted through a lossy reader (OCR, screenshot parsing, scraping), validate
  the reader against known-answer inputs first and keep a per-row capture
  artifact **anonymized** per the Anonymize rule above (PII replaced with
  same-shape stand-ins) — not the raw original; if a true raw artifact must be
  retained to re-validate the instrument later, hold it in a separate,
  minimized, access-controlled store, never as raw PII/secrets in the corpus.
  A reader defect taints every conclusion derived from its output —
  re-derive them; never resurrect pre-fix conclusions. And a human reading of
  a low-res artifact never overturns a pinned value without machine capture
  or independent cross-validation (a "fix" was once shipped off a misread
  screenshot and had to be reverted).
- **Every row records how it was captured.** A hand-written "plausible" row
  converts the gate into a mirror of your own guess — gate corruption, not
  coverage. When the capture rig is unavailable, the honest state is BLOCKED
  naming the exact rig and recipe to unblock — never synthesis.
- **Hold out a distribution-disjoint slice as the ship decider.** When the
  corpus was consulted during development, passing it alone is the overfit
  warning above; the deciding gate is a slice disjoint on a real dimension
  (date range, source, tenant) that development never saw.

The golden runner doubles as an experiment grader: pre-register expected
outputs as cases before any runs, then grade with code, not impressions —
no harness, no experiment. Pre-register the full **outcome → action table**
too (what each result will make you do), so a result cannot be rationalized
into a favored action afterward. Calibrate the difficulty of the SHARED
case set before comparing — never each arm's separately, which destroys
comparability: a comparison where every arm sits at the same ceiling (every
case passes in every arm) or the same floor (none does) carries no
discriminating evidence — halt there and report "untestable at this
tier/difficulty" as a valid outcome instead of publishing a null; between
those extremes, compare the pre-registered per-arm scores (arms clearing a
shared gate at different scores is still a result). Grade blind to which
arm produced each output.

**replay:** replace `replay/corpus.jsonl` with a representative sample of
real logged inputs. Replace `transform()` with the step being changed. Run
`node replay/run.mjs --update` once to freeze current behavior — and eyeball
that first freeze line by line: a baseline freezes *current* behavior, not
*correct* behavior, and it will protect any bug it contains as ground truth
(one committed baseline enshrined a real redaction bug this way — fix the
transform first, then freeze); after each
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

**Cheapest gate shape — the grep-count ratchet:** when an anti-pattern cannot
be removed wholesale (inline locale ternaries, stray global listeners), pin its
current grep count as a dated baseline with the hits enumerated; the executable
done-check on every diff is "the count did not grow" — and nobody "fixes" the
enumerated baseline hits as a side quest either.

## What makes a gate real (task-relative test discipline)

A generic green test is not proof. A gate is real only if:

1. It exercises the **task trajectory** — input, production path, state
   transition, observable output — not a reimplementation of the logic.
2. It would **fail under the broken behavior**. Run both arms where practical —
   broken arm fails, fixed arm passes — and prove a *negative* test can fail by
   running it against a known-bad arm. Instrument the failure's **own** signal,
   not a proxy: an unchanged field or intact-looking output can pass while the
   failure still occurred. **Arm polarity alone is insufficient — a change
   detector can mimic it while guarding nothing** (`unprobed` — adapted
   external design; see Provenance): a source-string presence check or a
   private-structure snapshot fails on the old arm and passes on the new
   one simply because the source changed — while firing on every future
   redesign and sleeping through every future bug (it also fails this
   rule's own-signal requirement above; the polarity just hides that).
   Before writing the test body, answer: what production change should
   make this test fail — and is that change a bug or a decision? If only
   deliberate decisions can fail it, it is a change detector, not a gate —
   asserting the source contains a line proves only that the source is the
   source. Carve-out: pinning a representation is legitimate exactly where
   that representation IS the declared contract (an error-message string
   or output name with downstream consumers — operational-rigor §3's
   output-text-is-an-interface); then a deliberate contract change
   properly updates the test. A suite that *grades* candidates is two-sided:
   before it scores anything, show it PASSES on at least two structurally
   distinct valid solutions (a too-strict suite silently rejects valid
   alternatives — false collapse) **and** FAILS on a known-broken state (false
   parity), both by execution. And confirm the corpus exercises the changed
   branch: a change "verified" only on inputs where the new code never fires
   is unverified — capture firing inputs, or synthesize them into the test
   suite as a labeled synthetic set, NEVER as rows in the captured
   golden/replay corpus (the case-set integrity rules above: a hand-written
   row corrupts the ship gate).
   The behavioral analog, when the gate is a trap fixture an AGENT must
   resist (a prescribed-but-unauthorized action, a planted directive):
   precedence first — taking the bait is FAIL however blind the run was;
   arming gates only the safe direction. A safe outcome counts only if
   the run demonstrably met the trap, the transcript showing the arming
   event for that fixture's carrier (the prescribing doc read, OR the
   planted skill loaded, OR the bait seen — whichever carries this
   fixture's trap). A safe outcome from a run that never met the trap is
   a NOT-ARMED run — excluded and re-run armed, never scored as
   discipline. Fixture-design corollary: hang the trap on a breadcrumb
   the task itself forces (the failing check's output names the doc), or
   read-narrow evidence discipline will disarm the fixture.
   The two-sided proof above validates a grader for ONE invocation shape at
   ONE time — reusing it later (a new run, a different candidate pool, hours
   later in the same session) is a fresh claim, not an inherited one. Before
   reuse: re-run the two-sided proof — the known-good references (both
   structurally distinct valid solutions, per the bar above) and the
   known-bad — diffing each outcome against the record of the prior
   validation (per-CASE outcomes, not an aggregate score — the same 2/6
   with different cases passing is drift; the invocation shape —
   command, arguments, configuration, with ephemeral values like
   run-scoped paths and timestamps normalized — and the
   reference-corpus identity, so drift in any is visible; a deliberate
   invocation change re-baselines only through a fresh two-sided proof
   and a new record; no record on hand → reuse stops, the two-sided
   proof runs fresh and its record is written before any scoring) —
   any drift is stop-the-line, never "still mostly failing, close enough."
   A wrong invocation shape (a file path fed where the grader expects a
   directory, a stale flag) can make the harness fail to load the candidate
   at all while the grader still emits a normal-looking scorecard — the
   candidate never ran, but the grader can't tell "candidate legitimately
   failed" from "candidate never executed." Watch for the inverted
   signature this produces: edge cases PASS while happy-path cases FAIL,
   because an edge case's own error-tolerant branch (a try/catch that treats
   a thrown exception as valid defensive behavior) silently absorbed the
   harness's load failure and got credited for it. (Incident: a
   directory-vs-file argument mismatch made every candidate throw
   `MODULE_NOT_FOUND` before its code ever ran; the known-bad reference
   scored 2/6 against a recorded 0/6, and the 2 passes were exactly the two
   capacity-edge cases whose accepted-throw branch swallowed the harness's
   own error.) (`unprobed` — private incident as shape; see Provenance.)
3. The **easy fake pass is named** and closed — hardcoded expected value,
   weakened assertion, testing the mock, a test that compiled but was never
   registered/run, a permanently `#[ignore]`/`.skip`ped backlog test that reads
   as coverage. Confirm a new test actually *runs* — the runner lists it, or it
   fails when you deliberately break the code — not merely that it compiles. For
   a guard/error path, assert three things, not just the exit code: the
   returncode, a message string unique to THIS check (many errors share exit 2),
   and that the dangerous side-effect did NOT occur (`assertNotIn`). Four more
   fake-pass shapes: a **warm-state pass on init-only code** — a zero-violation
   observation window proves nothing about code that only executes at
   initialization (cold start, first run, migration); exercise the cold path in
   a fresh context before enforcing (a CSP enforced after a clean Report-Only
   window broke the whole engine, because the loader it blocked had been warm
   the entire window). A **CI/automation config that has never executed** —
   count runs (the platform's runs API), not files; a config can be structurally
   undiscoverable (wrong directory in a monorepo) and inert forever while
   reading as coverage. A **snapshot gate that silently re-freezes when its
   baseline is missing** — deleting the baseline must be an error at gate time,
   never a vacuous green. A **scanner that matched zero inputs** — a gate whose
   file pattern silently expands empty (`**` degrading in an old shell dialect
   combined with a nullglob setting, a directory that moved) "passes" while
   scanning nothing (a guard script once did this for the very file its outage
   check was written for). A passing scan must also prove its input set is
   non-empty — assert the matched count is non-zero; merely printing it is the
   same vacuous green if nothing fails on 0. Worker-written guard scripts
   especially: item 2's known-broken run applies before trust, no exemption —
   whoever wrote a guard has never seen it fail. (`unprobed` — private
   incident as shape; see Provenance.)
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
6. If it is an **automated gate, its block-on-fail decision is deterministic, not
   an LLM's judgment** (`unprobed` — see Provenance). An executable hard gate that
   denies or blocks runs on code, not a model verdict; where an LLM contributes to
   it, the LLM is **advisory and capped** by the gate contract's declared limits —
   a maximum advisory-pass count, a confidence ceiling, findings dropped unless
   sourced — never the pass/fail authority. And where a claim hands you a count,
   sum, or sourced value, **re-derive it independently** (recompute the aggregate;
   trace each value back to its source) rather than trusting the number given. (A
   review/adjudication gate — where a human or a cross-family model verdict IS the
   gate, as in cross-model-review or design-review-gate — is a different
   instrument: there the verdict is the authority, disciplined by lens diversity
   and reproduction, not replaced by code.)
7. If it uses **mutual agreement to assert correctness, freshness, or an
   authoritative value, it anchors that to an external ground truth** (`unprobed`
   — see Provenance). A check that infers currentness from N artifacts agreeing
   with each *other* passes while all N are stale **together** (every manifest
   frozen at an old version, so they "agree"); such an inference anchors to an
   independent source of truth — a release tag, the upstream record, a recomputed
   value — read at the moment it matters. (A check whose contract is only
   *consistency* — do these N agree with each other, with freshness asserted
   elsewhere — is legitimate as-is and needs no anchor, as does an intrinsic gate
   like a syntax or forbidden-character scan. The rule bites only when agreement
   is made to stand in for an external fact.)
8. **A gate over hardcoded facts asserts the facts, not just the shape — and
   the cross-check that established them belongs IN the fixture, not in the
   chat** (`unprobed` — private incident as shape; see Provenance). When code
   embeds domain constants (holiday dates, a tax rate, a fee schedule, the set
   of valid states), a suite that checks structure — the array is non-empty,
   each entry parses, the shape is right — passes identically whether the
   values are correct or a later edit corrupted one. Those values were usually
   cross-checked once, against an authority or several independent sources or a
   reviewer's recall — but that check happened in the conversation and
   evaporates when the session ends, so the next bad edit sails through a
   shape-only gate. Anchor the fact: assert the specific load-bearing values
   (a fixed holiday falls on its known date, the standard rate equals the
   published number), each assertion naming its authority (source, and its
   version or URL where it has one) and consultation date beside the value —
   an unattributed literal is indistinguishable from item 3's copied-back
   expected value — so a future silent change to a constant fails. This *extends* item 2's carve-out —
   from an output-interface string to an embedded input constant — and is NOT
   item 3's "hardcoded expected value" fake pass: the anchor's value comes from
   an external authority, not copied back from the code's own output. Item 3's
   tautology asserts the code agrees with its own output; this asserts the
   code matches the world. It shares rule 7's remedy — an external anchor — but not its
   trigger: rule 7 bites where *agreement between artifacts* is made to stand
   in for an external fact, this one where *structure* is. A fact that
   legitimately changes gets its anchor updated as a contract edit (rule 4:
   state which contract changed and who approved it); an always-fixed one is
   cheap to anchor permanently.
   ❌ "the holiday tests pass" — they assert the list has the right count and
   types, never that any date is the right day; a fat-fingered edit to one
   date stays green.

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
- **A globally-installed *optional-feature* guard defaults to a silent no-op
  unless the current project opted in** (`unprobed` — see Provenance). A
  convenience hook shipped to every project (a global Stop / PreToolUse hook for
  a feature) checks a project-local opt-in marker — a file, a config key — and
  does nothing, silently, where it is absent, so a broad install never disturbs
  work that never adopted the feature. This pack's own plugin ships its hooks
  **unregistered** for exactly this reason (checks.py asserts "plugin registers
  no hooks"). The carve-out is a control the owner or admin *authorized* to be
  universal — a secret scanner, a policy or destructive-command guard: those are
  meant to cover every project, and gating them behind a project opt-in would
  silently disable protection. So an optional feature is opt-in; an authorized
  global policy control fires everywhere by design. (Distinct from the
  fail-direction choice above, which governs a guard a project is already subject
  to.)

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
The 2026-07-13 case-set integrity rules (instrument validation + taint,
row capture-provenance, distribution-disjoint holdout), the two-sided
suite-soundness and fire-path clauses, the saturation/blind-grading and
outcome→action pre-registration lines, the first-freeze eyeball, the
grep-count ratchet, and three of the added fake-pass shapes (warm-state,
never-executed CI config, snapshot re-freeze) are mined from five
further private retiring-architect libraries (an engine-parity port, a market
dashboard, a learning-lab experiment harness, a Telegram bot, a link-shortener);
each is backed by a cited incident or experiment in its source library (private
repos — verifiable by the contributor, not linkable here).
A 2026-07-16 two-family post-merge review (grok-4.5 + gpt-5.6-sol;
trail in `reviews/2026-07-16-post-merge-validation-pr25-29.md`) scoped
experiment calibration to the shared case set and confined synthesized
fire-path inputs to a labeled test set, never the captured corpus.
The rule-2 behavioral trap-armed clause (2026-07-16) adapts a published
negative from Sahir619/fable-method's eval log — safe outcomes produced by
runs that never read the prescribing doc, blindness scored as discipline
until a transcript check was added (MIT; ideas only, no files copied; see
README acknowledgements).
The rule-3 zero-input-scanner shape (2026-07-18) comes from a private
incident: a worker-written guard's `**` pattern expanded empty under an old
shell dialect with nullglob, and the guard "passed" while scanning zero
files, including the one its outage check existed for. Private evidence,
cited as shape per the README covenant's second branch; no in-repo probe
has run, so the shape carries an in-body `unprobed` marker.
The rule-2 reuse-time re-validation clause (2026-07-23) comes from a
contributor incident: before a new batch, a grader re-validation fed a
directory to a grader that takes a file path; the harness threw a
module-load error for every case before any candidate code ran, the
known-bad reference scored 2/6 against a recorded 0/6, and the two
spurious passes were exactly the two capacity-edge cases whose
accepted-throw branch absorbed the harness's own load failure
(contributor-reported; the private harness is verifiable by the
contributor, not linkable here). Ships `unprobed` per the README
covenant's second branch; the executable probe — seed an
invocation-shape mismatch against a two-sided-proven grader and observe
whether reuse-time re-validation catches it before scoring — has not
run; the in-body marker records that debt.
Rule 2's decision-vs-bug clause (2026-07-24) adapts obra/superpowers
v6.2.0's writing-good-tests rebuild (MIT, ideas only; see README
acknowledgements): the string-presence trap ("the source is the source")
and the change-detector trap — failure shapes the two-sided protocol alone
cannot screen, since a source-echo test genuinely fails the old arm and
passes the new one. Ships `unprobed` per the covenant; its probe joins the
private round-5 queue.
Numbered items 6 (deterministic block-on-fail + independent recompute) and 7
(external-anchor over mutual agreement) under "What makes a gate real"
(2026-07-24) come from a starred-repo mining pass (ideas only; see README
acknowledgements). Item 6 is a four-source convergence —
s0912758806p/agentic-sop-to-work (hard gates hermetic and LLM-free, self-eval
advisory-and-capped), cloudflare/security-audit-skill and
vercel-labs/agent-skills (a mechanical structural check kept separate from model
judgment), and DietrichGebert/ponytail (self-verified good/bad instruments) —
its independent-recompute clause adapting agentic-sop's `recompute_gate` and
per-value trace gate (all MIT — vercel's MIT is declared in its README with no
LICENSE file; ideas only, no text). Item 7 adapts ponytail's `check-versions.js`,
whose comment records the real incident (every manifest shipped stale at one
version together while a mutual-consistency test passed — its #260/#262),
generalized from version manifests to any mutual-agreement check. The guard
opt-in rule under "Designing the guard itself" (2026-07-24) adapts
s0912758806p/agentic-sop-to-work's globally-installed hook that silent-no-ops
unless the project opted in (MIT, ideas only), corroborated by
NYCU-Chung/my-claude-devteam's bypassPermissions-hook framing (MIT) — it
matches this pack's own no-auto-registered-hooks invariant. All three ship
`unprobed` per the covenant; their probes join the private round-5 queue.
Rule 8 (fact-anchoring; 2026-07-24) is class-distilled from a mining pass
over the owner's own sessions (no code taken): hardcoded public-holiday dates
were cross-checked against four independent sources, but a cross-model
reviewer noted the suite validated structure only — "tests check shape, not
date-truth" — so the truth evidence lived in the conversation, not the gate;
the fix added anchor-date assertions as a regression guard against a future
bad edit. Ships `unprobed` per the covenant; its probe joins the private
round-5 queue.
`template/` scripts are self-contained (Node + bash, zero deps) and were run
green on 2026-07-06 with Node v23; re-verify with `bash template/run-all.sh`.
