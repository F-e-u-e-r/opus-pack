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
into a favored action afterward. **Write the pre-registration somewhere
durable and timestamped BEFORE the first run, and cite that timestamp in
the finding** (`unprobed` — contributor incident as shape; see Provenance).
Durable = version-controlled, or written into the project's permanent
record; ephemeral = `/tmp`, a scratch/sandbox/session directory, anything
`git check-ignore` matches. On overlap, check-ignore wins: an ignored
working path is ephemeral for this rule even when an external archive
preserves it — cite the archive or permanent-record path itself, not the
ignored working copy. Transcribing the criteria into the write-up
afterwards is a weaker record than it looks: it is made once results are
in, so it cannot evidence the ordering that pre-registration exists to
prove, and it fails quietly — a dead link at least tells a later reader the
claim is unbacked. Re-check that every path a finding cites still resolves
before publishing.
❌ "criteria: see `scratch/PREREG.md`" — reclaimed a session later, and
the frozen criteria can no longer be distinguished from fitted ones.

Calibrate the difficulty of the SHARED
case set before comparing — never each arm's separately, which destroys
comparability: a comparison where every arm sits at the same ceiling (every
case passes in every arm) or the same floor (none does) carries no
discriminating evidence — halt there and report "untestable at this
tier/difficulty" as a valid outcome instead of publishing a null; between
those extremes, compare the pre-registered per-arm scores (arms clearing a
shared gate at different scores is still a result). Grade blind to which
arm produced each output. And the verdict is bound to the provider, model
tier, and configuration the arms actually ran on: an effect can shrink,
vanish, or invert across configurations, so generalizing to another
provider, tier, or configuration takes its own runs there — same-family
or similar-name inference is not parity evidence. (`unprobed` — see
Provenance.)

The same calibration discipline applies within one arm across time
(`unprobed` — contributor incident as shape; see Provenance). A
stochastic subject — a model, a scheduler, a network path, anything whose
output can differ on identical input — has a distribution, and a single
full-marks sweep shows it CAN pass, not that it does; "stable", "no
regression" and "matches baseline" are all claims about that distribution.
Replicate before such a claim leaves your notes, and where an arm was not
replicated, carry its run count beside its score so a lone sweep cannot read
as a measurement. Every claimed run needs a persisted row of its own: a run
quoted from recall, or one whose output the next run overwrote, cannot be
re-checked and is not a run — publishing four while one is on disk is how an
unreplicated result becomes an unfalsifiable one.
❌ "30/30, no thinking step — make it the default." Replicated to N=4 the
same candidate scored 30/30/20/29, failing twice by mechanisms the first run
never produced.

**Arms share one runner — inventory its environment, or the harness is a
second treatment** (`unprobed` — see Provenance). The runner's own
standing environment — always-on hooks, injected rules or instruction
files, wrapper behavior, permissions, tool availability, harness
configuration — reaches the arms it runs; anything reaching some arms and
not others is an untracked treatment riding on the comparison, and "same
runner" by name establishes nothing (one runner name can load different
hooks or configuration per invocation). Before scoring: enumerate the
runner-level surfaces that can act on any arm, then hold each identical
across arms or record the difference as a condition carried by the
result.
❌ "both arms ran in my session, so conditions matched" — the session's
always-on hook fired inside the baseline arm and not the isolated
treatment arm, so the comparison measured hook-plus-baseline against
treatment.

**Exclusions and lost runs follow one rule set across arms** (`unprobed`
— see Provenance). Eligibility, exclusion, and re-run rules are declared
once and applied identically to every arm — the NOT-ARMED discipline of
rule 2 below included. Equal final N is not required; per-arm attrition
accounting is: started / excluded-with-reason / scored, so an unequal N
is explainable arm by arm, and an unexplained per-arm gap blocks the
comparison. An exclusion mechanism correlated with one arm's treatment —
the treatment crashing exactly the runs it would have failed — biases
every surviving score; name that asymmetry in the result rather than
averaging over it.
❌ "dropped three malformed runs" — all three sat in one arm, and the
malformation was that arm's own failure signature.

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

**Replay's inverse — verify-by-reconstruction** (`unprobed` — see Provenance):
to prove "exactly X was applied" to a delivered state, reconstruct across the
boundary with an INDEPENDENT prescription of X — a pinned oracle, the
pre-change implementation (the parity rule above), or the spec — never the
delivering system's own producer, whose bugs reproduce on re-run and
self-confirm. Two sound forms: full-state comparison
`apply_independent(baseline) == delivered` over a DECLARED projection —
and the projection must cover the complete mutation boundary: every field
X touches AND the fields expected to stay unchanged, with only the ambient
fields the system legitimately mutates on its own (ids, timestamps, server
defaults) on a declared allow-list, exactly as the parity gate above
allow-lists intended diffs. A projection cut down to "what X touches"
passes a delivery that also mutated state outside it — the nearest
over-application variant; where the full boundary genuinely cannot be
enumerated, the conclusion narrows to "exact within this projection" and
every out-of-projection surface is reported unverified, never implied
proven. (Raw whole-state equality with no allow-list false-fails on every
non-pure deliver, and a false-failing gate gets weakened or dropped.) Or a
true inversion `apply⁻¹(delivered) == baseline` ONLY where the inverse is
a proven bijection — a lossy "undo" (reset-to-default) maps an
under-applied state back to baseline too and passes exactly the case the
check exists to catch. Both forms
prove STATE, not history: repeated idempotent application and duplicate
side effects that leave identical state are invisible to them — where
those matter, add an operation/event witness (an application count, an
audit log), or the claim stays state-only, said so. No independent
prescription available → the re-run is a consistency check, labelled so —
never a proof.

**In parity work, the artifact settles disputes — reading it beats
adjudicating between reviewers or picking the plausible option**
(`unprobed` — contributor incident as shape; see Provenance). When the
contract is parity with an external artifact (a spreadsheet, a workbook,
a prior implementation), a reviewer blocker or a spec ambiguity is a
question the artifact already answers, not a judgment call — open it and
read the cells. And a defensive addition your own spec invents that the
artifact does not contain (a clamp, a guard, a floor the source formula
lacks) silently forks the parity target the moment it ships: it enters
the spec only as an explicitly flagged deviation, never as an unstated
improvement.
✅ "two independent reviewers flagged the same clamp as suspect; opened
the workbook — `B6 = B3*B4-B5`, no MAX anywhere. My spec's clamp was an
invention; fixing to match, no clamp." ❌ picking whichever reviewer's
suggested fix sounds more defensible and moving on, with the artifact
never opened.

**A ground-truth artifact is authoritative for behavior, not for every
embedded constant it hand-types — derive the derivable before porting a
magic number, and flag rows no scenario ever exercises**
(`unprobed` — contributor incident as shape; see Provenance). Hand-maintained
oracles carry hand-typed values that should be *computed* from other
cells; a stale hand-update hides exactly in the rows no realistic
scenario drives, so a clean replay proves nothing about whether the
constant is still correct. Two failure shapes to check for before
porting: (a) a constant that should derive from other cells but was
typed in by hand — recompute it and compare; (b) two DIFFERENT
quantities that happen to share a value (a coincidence, not an identity)
each hand-typed under one shared name — rename them apart, because "same
number, different bases" invites conflation the moment either changes.
✅ "the `144445` in rows 8–10 is `ROUNDUP(130000/0.9)` — but the sheet
was updated by hand from row 11 downward after a minimum changed, and
rows 8–10 are policy years that never draw, so nothing ever surfaced the
staleness. Recomputing and flagging every unexercised row." ❌ porting a
spreadsheet's constants verbatim because the sheet is "ground truth" and
the replay gate is green.

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
   and that the dangerous side-effect did NOT occur (`assertNotIn`). Five more
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
   same vacuous green if nothing fails on 0. A **substring grader whose match
   token can occur in the graded corpus** — scanning prose for a word that the
   corpus itself may contain scores the corpus, not the behavior, and unlike
   the zero-input scanner above this one runs correctly over a non-empty input
   and still passes every arm. Key on a token the graded material cannot
   produce on its own (a structural marker the subject must create and
   fill — a heading, a filename, a field), and sanity-check the grader
   against a known-bad
   arm before trusting a clean sweep: a grader that passes an arm you KNOW
   failed is the finding, not a formality. Its damage is not a vacuous
   empty run — it manufactures agreement over real input, so an A/B whose
   arms all pass
   reads as "no effect" and retires a real one. (`unprobed` — contributor
   incident as shape; see Provenance.) Worker-written guard scripts
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
   embeds domain constants (holiday dates, a tax rate, a fee schedule, a
   jurisdiction's valid state codes), a suite that checks structure — the
   array is non-empty,
   each entry parses, the shape is right — passes identically whether the
   values are correct or a later edit corrupted one. Those values were usually
   cross-checked once, against an authority or several independent sources or a
   reviewer's recall — but that check happened in the conversation and
   evaporates when the session ends, so the next bad edit sails through a
   shape-only gate. Anchor the fact: assert every load-bearing value
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
9. **Independence across N things is a pairwise claim** (`unprobed` —
   contributor incident as shape; see Provenance). Where a gate rests on N
   items being independent — separate rate-limit buckets, separate failure
   domains, separate credentials, separate blast radii — establishing that
   takes all N(N-1)/2 comparisons, or a directly-read partition (each item's
   owning account queried from the provider) that replaces the comparisons
   rather than shortening them. Exhausting one item and watching the other
   N-1 survive proves only that each is outside THAT one's bucket, and says
   nothing about whether the remaining N-1 share a bucket with each other:
   the probe returns the same reading for N genuinely separate items as for
   one separate item plus N-1 that are all the same, so a baseline-vs-all
   measurement supports a 2x claim while presenting as Nx. Transitivity does
   not rescue it — sharing a bucket is transitive, not-sharing is not, so a
   reader who correctly identifies the property as transitive still owes
   every pair.
   ❌ "key 0 hit its limit and keys 1-3 kept serving — four independent
   accounts, 4x throughput." Keys 1-3 were never tested against each other.
10. **A green suite names the artifact it exercised** (`unprobed` — contributor
   incident as shape; see Provenance). A suite reaches its subject by name — an
   import, a `PATH` lookup, a package entry — and that name can resolve to a
   copy other than the one you edited: a file left behind at a previous
   location, an installed version shadowing the working tree, a build output
   stale by one step. Every assertion then passes honestly, about an artifact
   nobody chose. This is the attribution half of operational-rigor §4's
   check-name rule ("a check's name is not its coverage") made a standing
   property of the suite: there, a cited run is traced to the change once,
   when it is cited; here the suite re-establishes its own subject on
   every run, because a shadowing copy can reappear after any later move,
   install, or sync. It is neither item 3's never-registered test (that one
   never runs) nor item 2's failed load (that one throws before the subject
   ever runs, and the inverted signature or the reuse-time record-diff
   catches its normal-looking scorecard): here the code runs to completion
   and the scorecard is real, so the green is evidence — about the copy
   resolution chose, not the one you changed. Assert subject identity in
   the form the subject can witness. Exercising the edited file itself:
   the location the running subject reports (`__file__`, the loaded
   module's path, the running process's own resolved path) equals the
   path you changed, both sides canonicalized — a symlink alias fails a
   raw string compare while naming the same file — and the load is fresh
   for this run (a module imported before the edit landed, a persistent
   runner, or stale compiled bytecode reports the expected path while
   executing pre-edit bytes): restart or reload the subject, or assert a
   content witness your edit introduced. Exercising a BUILT or
   installed product of the edit: a path match alone passes on
   yesterday's build sitting at the same path, so pair the expected
   artifact path with a revision witness tying the
   artifact to the source you edited (rebuild into the asserted path
   before the run, or assert an embedded stamp or digest). That identity
   check proves nothing shadowed the subject in THIS resolution — so what
   it leaves open is the contexts that resolve differently: a suite that
   prepends the repo root to the search path finds your copy while
   production resolves the installed one. For any claim about the deployed
   path, run the suite through the production lookup, or resolve that
   lookup yourself and identity-check what it returns — the absence of
   the one shadow you suspected is not that; another entry in the chain
   can still win. Doing neither narrows the green to "my copy, my
   resolution" — then say so where the result is reported. Done when the
   subject-identity check ITSELF fails against a wrong copy — a
   behaviorally equivalent one is the clean demonstration, an unrelated
   assertion failing proves nothing about the identity check; for a built
   subject a wrong revision at the right path must fail it too — demonstrated
   once by execution, and the production-resolution half has run or the
   claim is explicitly narrowed.
   ❌ "all 30 checks pass after the move" — they would have passed identically
   against the pre-move copy still sitting in the old directory, which is why
   the count says nothing about the move.
11. **A self-benefit metric ships the tests that keep it honest** (`unprobed`
   — see Provenance). Where a tool measures its own benefit — a compression
   ratio, cost savings, a cache-hit gain, "N duplicates removed" — the suite
   guards against systematic overstatement from both directions: the
   no-benefit case must read its independently expected value on the
   metric's OWN scale, at or beyond the metric's declared no-benefit point
   in the harm direction — a signed delta reads `<= 0`, a compression
   RATIO reads `>= 1` on expansion — so the suite names each metric's
   no-benefit point (or normalizes to signed benefit) first; an
   incompressible input EXPANDS under framing overhead, a cache can cost
   more than it saves, and a metric whose scale clamps at the no-benefit
   point is itself flattering (run it, and preserve the harm-side reading
   unless the declared domain genuinely cannot represent one); at
   least one known-benefit calibration anchor per supported input class
   must read within a PREDECLARED tolerance of its independently computed
   expected value (anchors calibrate — they bound systematic inflation,
   they do not prove correctness on untested inputs; a formula/property
   bound does more where one is derivable); and a comparison is admitted
   only under two independent conditions: (a) the baseline matches the
   treated input's exact immutable identity (same bytes/version) — an
   unconditional equality that no normalization may substitute for; and
   (b) the benefit-affecting non-treatment variables — pricing,
   configuration, workload, observation window — are INVENTORIED, and
   each one individually matches or carries its own predeclared,
   justified normalization; an omitted variable fails admission rather
   than escaping comparison. Anything short of both is refused, not
   reported, because a shifted non-treatment variable manufactures
   benefit on identical input; the suite exercises both refusal branches.
   Without these this is item 3's fake-pass family wearing a dashboard:
   the flattering number can never fail.
   ❌ "the tool reports 40% savings on every run" — including on input it
   provably cannot compress; nothing asserted the zero-savings case, and
   nothing calibrated the 40%.

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
  freely; when unsure, treat it as fail-closed. And the direction is only
  half the design — place the finding too: the guard's block or detection
  must land on a decision surface that can act on it (an actor who can
  change the input, stop the run, or authorize — not only a log nobody
  routes on); a deny nobody receives has a fail direction but no failure
  route, so placement and route are designed together. (`unprobed` — see
  Provenance.)
  ✅ "the credential gate blocks the deletion it detects and raw-scans an
  unparseable command; its malformed-envelope path fails open today — a
  disclosed gap." ❌ "the hook is flaky and blocks my commands, so I'll make
  it fail-open" — that converts a guard into a rationalized bypass.
- **A detector's positives come from the corpus it will guard, not from the
  author's examples of them** (`unprobed` — two contributor incidents as shape;
  see Provenance). A guard that classifies real material — a secret scanner, a
  redactor, a quality or corruption check — is written beside the positives its
  author pictured, and those are the ones it gets tried against. The miss is
  silent and total: it passes the exposed-path check above, it fires on the
  author's examples, and it still catches nothing the live corpus holds. Two
  shapes seen. A matcher whose *form* excludes every real instance: an
  assignment pattern written lowercase where every credential on the host is
  uppercase, reporting clean across all of them. And a score measured at the
  wrong *granularity*: a repetition check keyed on the most frequent single
  token where the corruption is a repeated multi-word phrase — a transcript
  roughly one third watermark junk scored 0.078 against a 0.30 threshold, and
  summaries of it shipped for weeks. Granularity is the harder shape, and not
  simply a mistuned threshold: the author's synthetic single-token repetition
  can be constructed to clear whatever threshold is set, which is what made
  the check look sound; the phrase also moves the statistic, so its score is
  not zero, but it lands inside the band ordinary prose already produces —
  one common token is a few percent of ordinary text — so no threshold
  cleanly separates the real positive from clean material and tuning cannot
  rescue it. The golden-gate rules above on how cases are captured — drawn
  from the real corpus, provenance recorded, hard negatives included, never
  a hand-written "plausible" row — govern a guard's validation samples the
  same way: the positive comes from the corpus the guard will face, never
  from the author's imagination; where the corpus genuinely holds no
  positive, plant one whose form is copied from a real instance (item 2's
  labeled-synthetic discipline — labeled, and never a row in the captured
  corpus), not written from the shape you pictured. Before enabling, confirm
  it fires on that positive — and
  where the guard scores rather than matches, confirm the score lands on
  the FIRING side of the decision boundary, in whichever direction the
  guard fires (the incident's 0.078 against a fire-at-0.30 threshold sat
  deep on the non-firing side while reading like a margin) — then confirm
  captured clean samples, the hard negatives above included, do not fire.
  Done when both directions are shown — fire on validation positives
  representative of each form the corpus holds (captured rows, or the
  labeled plant where the corpus held none; a plant stays labeled,
  supplements captured rows where the corpus holds the form, and stands
  alone only where it held none), no fire on captured clean samples
  including hard negatives —
  and those positives are kept as the guard's regression cases — as
  shape-preserving, non-sensitive derivatives when a positive is itself
  a secret or sensitive (security-architect's minimize-by-type;
  `REDACTED`-style blanking destroys the very shape the guard keys on,
  so re-run the guard on each derivative and keep it only once shown
  still firing; a live credential never lands in fixtures).
  ❌ "it flags my test key, so the scanner works" — the test key is the shape
  you already had in mind; the question is whether it flags the ones that are
  actually there.
- **Sentinel-tag every synthetic fixture, so "never leaked verbatim" is one
  scan** (`unprobed` — see Provenance). Embed one shared greppable marker in
  every free-form fixture value, collision-checked once against the clean
  corpus (grep it where nothing was planted — zero hits there means the
  marker is safe to plant for THIS suite; a corpus check, not a proof about
  all possible content), so the leak check is executable instead of
  per-fixture recall. A shape-CONSTRAINED class — a hex credential, a UUID,
  a checksummed or enum identifier — cannot carry the free-text marker
  without leaving its grammar and silently stopping short of the production
  parser it exists to exercise (the shape rules above): give each such
  class a grammar-VALID sentinel (a fixed hex stem, a reserved UUID
  prefix), keep the full sentinel list in one manifest so the scan stays
  one command over all of them, and keep a regression proving each
  constrained fixture still reaches its intended production path. Runnable
  worked example: `template/sentinel/run.mjs` (collision check + leak scan
  + the constrained-class manifest; its `--demo-leak` mode shows the
  failing side). State the claim's bound honestly on BOTH dimensions —
  representation and coverage: the scan proves no VERBATIM occurrence
  (encoded, escaped, truncated, or transformed copies need a
  representation-aware sweep over the encodings the pipeline actually
  applies, or the record says "verbatim only"), and it proves it only over
  a DECLARED surface-and-window manifest — every downstream sink fixtures
  can reach, over the retention interval the claim covers; a merely
  nonempty artifact pile is not coverage, and a declared surface that
  cannot be queried makes the result INCOMPLETE, never PASS. The tool's
  own diagnostics never republish what they guard: failure output names
  class, count, and source ordinal — never the sentinel value or the raw
  matched record. Distinct from security-architect's minimize-by-type
  sentinel: that one proves a sensitive FIELD never appears past a parse
  boundary; this one proves planted test material never ESCAPES the test
  boundary.
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
The item-3 substring-grader-token-collision shape (2026-07-28) comes from one
downstream consumer's A/B probe (contributor-reported, not linkable): the
grader for a "did the arm record the
change?" axis scanned each arm's output file for the word `drift`, which the
fixture's own body text already contained ("a batch that drifts model
mid-run"). Every arm passed, including three that recorded nothing — the run
read as a 4/4 null result and would have retired a rule that did in fact
discriminate 0/3 vs 1/1 once regraded on a port-note heading. Ships
`unprobed` per the covenant.
The pre-registration-ordering clause (2026-07-28) comes from a contributor
incident (contributor-reported, not linkable). Three pre-registered probe
rounds in one session wrote their
pre-regs to a session scratch directory, which was later reclaimed — leaving
five citations across a finding file, an always-loaded rules file, and a
maintenance ledger pointing at paths that no longer existed. The criteria
had genuinely been frozen before each run, which is the point: nothing that
survived could show it. Ships `unprobed` per the covenant; its probe joins
the private round-5 queue.
Item 9 (pairwise independence; 2026-07-30) comes from a contributor incident
(contributor-reported, not linkable). Four API keys were probed for separate
rate-limit accounting by exhausting the first alone and observing the other
three keep serving; the finding published "four independent organizations, 4x
throughput", which that probe cannot support. A fresh-context review caught
the inference and the pairwise re-measure came back 6/6 — the conclusion was
right and the method was not, which is the shape worth recording, since a
lucky confirmation is what keeps the method in use. Ships `unprobed` per the
covenant; its probe joins the private round-5 queue.
The single-arm replication clause under the experiment-grader rules
(2026-07-30) comes from a contributor's model battery (contributor-reported,
not linkable). A model written up at N=1 as "30/30, no thinking step, the
default for anything" scored 30/30/20/29 once replicated to N=4 — an invalid
emitted regex that threw, and a null-handling edge case — and was retracted
as a default; a second model in the same battery moved from 4/4 to 3/4 the
same way, its control green on the failing run. The same write-up had
quoted four runs while only one was on disk. Ships `unprobed` per the
covenant; its probe joins the private round-5 queue.
Item 10 (subject identity; 2026-07-30) comes from a contributor incident
(contributor-reported, not linkable). A utility module was moved into a shared
library directory and its suite passed 30/30 afterwards — but nothing asserted
the module's own `__file__`, so the same 30 would have passed against the copy
still sitting in the old directory; a fresh-context review found the hole and
the suite grew a canonical-path plus no-shadowing-copy check (32/32). Scoped
honestly: the review caught it before it certified a wrong artifact, so the
harm — a green run reported for code that was never exercised — is reasoned
from the mechanism, not observed. It is placed as its own item rather than
folded into operational-rigor §4 because the remedy differs in kind: §4 traces
a run to a change at citation time, this asserts the subject inside the suite
on every run. Ships `unprobed` per the covenant; its probe joins the private
round-5 queue.
The detector-positives bullet under "Designing the guard itself" (2026-07-30)
comes from two contributor incidents in one environment (contributor-reported,
not linkable), which is why it is stated as a class rather than as either
symptom. A credential scanner's assignment-tier pattern was written lowercase
while every credential on that host is uppercase, so it reported clean across
all of them; it was caught before deployment by trying it against a known-live
key. A meeting-summary pipeline's corruption check scored the most frequent
single token where the real corruption is a repeated multi-word phrase; a
transcript that was roughly one third watermark junk scored 0.078 against a
0.30 threshold and passed, and summaries derived from such transcripts were
published for weeks before the mismatch was diagnosed — the observed half of
the pair. A cross-family review of this addition corrected its first draft,
which claimed a token statistic "can never fire" on a phrase: the statistic
does respond, and the real barrier is separability, not response. Ships
`unprobed` per the covenant; its probe joins the private round-5 queue.
The verify-by-reconstruction recipe, the item-11 self-benefit-metric rule,
and the sentinel-tagged-fixtures bullet (2026-08-01) are the
ground-truth-gates slice of the deferred-candidate backlog from the
2026-07-31 two-repo mining pass (opus-pack #112, triaged under #115 Phase 1;
ideas only, no text — same sourcing and acknowledgements as the two
2026-07-31 PRs). Each was deferred at the original gate as recipe-level or
needing generalized wording; the wording here is this pack's. All three ship
`unprobed` per the covenant; their probes join the private round-5 queue.
The artifact-settles-disputes and derive-the-derivable-constant bullets
(2026-08-04) come from one contributor session's parity-implementation
work against a financial workbook: two independent reviewers flagged a
spec-invented clamp as suspect, and opening the workbook's actual formula
(no clamp) settled the dispute the reviewers themselves had only guessed
at — contributor-reported, not linkable here. The derive-the-derivable
half comes from a separate check in the same session: a stale hand-typed
constant, only ever wrong in policy-year rows no test scenario exercised,
was caught by recomputing it from other cells rather than trusting the
sheet; a second, distinct case in the same pass found two unrelated
quantities sharing one hand-typed value by coincidence, renamed apart to
stop future conflation. Ships `unprobed` per the covenant; their probes
join the standing #115 queue — a future campaign, not round-5, which was
a completed, frozen ten-target slice these rules were not part of.
The experiment-grader arm-environment and attrition-parity rules, the
calibration block's configuration-binding clause, and the fail-direction
bullet's placement clause (2026-08-06) adapt four disciplines mined from
gsd-build/get-shit-done (MIT, ideas only, no text; upstream archived —
successor open-gsd/gsd-core; see README acknowledgements) in the
2026-08-02 dual-model mining evaluation of owner-named repositories, and
kept through a 2026-08-06 re-verification pass in which two model
families converged on all four dispositions against the then-current
main. All four ship `unprobed` per the covenant; their probes join the
standing #115 queue — a future campaign, not round-5, which was a
completed, frozen ten-target slice these rules were not part of.
`template/` scripts are self-contained (Node + bash, zero deps); the
golden/replay starters ran green on 2026-07-06 with Node v23, and the
sentinel starter ran green two-sided (PASS + `--demo-leak` FAIL) on
2026-08-01; re-verify with `bash template/run-all.sh`.
