---
name: mutation-matrix-evidence-discipline
description: Load when editing hooks/mutation_matrix.py or hooks/mutations.json, running or citing an "authoritative"/"55/55 killed" mutation result, marking a mutation equivalent/unreachable, adding a test whose name asserts a property class, building any verification probe or self-check, or correcting a threat-model/README overclaim. A runtime-hook change that also adds/edits a test or makes a test/evidence claim ALSO loads skill-vetting-security-invariants. Harness-only work uses this skill rather than the security skill — that split does not suppress security-hardening-review-ops during a hardening campaign or a security-sensitive push/PR/merge.
---

# Mutation-matrix and evidence-integrity discipline

`hooks/mutation_matrix.py` (data in `hooks/mutations.json`) reverts each landed
fix one at a time inside a throwaway git worktree at a named commit and requires
the test suites to go red. It is this repo's instance of the pack's proof-gate
doctrine (`ground-truth-gates`: a gate must be able to FAIL under the broken
behavior, and "proof gate" is defined there) — but the tool that measures the
tests is itself security-relevant, and during PR #83 it produced a false "55/55
killed" more than once. These rules make an authoritative result trustworthy;
each traces to a defect the campaign hit and fixed.

## Two commands, do not confuse them
- **`python3 hooks/mutation_matrix.py --authoritative`** — the closure run a
  report may cite: on a clean committed checkout it reverts every landed fix in a
  throwaway worktree and requires the suites to go red (`--help`: "the mode a
  closure report may cite"). Slow; produces the run-scoped record.
- **`bash hooks/test-mutation_matrix.sh`** — the harness's own UNIT suite (it
  `exec`s `hooks/test-mutation_matrix.py`). It tests the tool, NOT your code, and
  is NOT an authoritative mutation run. Do not cite it as one.

## The core principle
**A verification tool must be proven able to FAIL before its "pass" is trusted**
(`ground-truth-gates`), and the evidence it emits must be bound to the exact code
and run it claims. A mutation harness, a closure verifier, a status check — each
is a claim generator, and a broken one confabulates a clean result.

## Rules

### R1 — the tool proves it can fail (two-sided), with structural anchors
- **Trigger:** adding a mutation to `mutations.json`, or a text-anchor
  (`replace`, `rindex`) that locates code.
- **Do:** every mutation's anchor must match exactly one site — `check_mutation`
  raises `MatrixError` when an anchor matches ≠1 site
  (`hooks/mutation_matrix.py:86-98`); confirm a mutation actually flips behavior
  by watching the suite go red on it, not by trusting the count.
- **Done:** a planted no-op mutation is reported as such (not "survived"); an
  ambiguous anchor is refused, not silently applied to the wrong site.
- **Incident:** `rindex("]\n")` once matched `survived = []` in `main()` instead
  of the target list, so 4 new mutations were pushed into the survivors' initial
  value and never executed — reported as surviving without running.
  `replace(old,new,1)` hit an unreachable guard in `main()` instead of the live
  one in `_run` for two rounds.
- ❌ "the harness says these 4 survived, go fix the tests" — inspect the harness
  first when a batch of survivors appears at once.

### R2 — a pristine control is bound into the evidence; the oracle checks two signals
- **Trigger:** editing `run_suite`, the control, or the pass/fail oracle.
- **Do:** run each suite UNMUTATED first (the `pristine-control`); if it is not
  green the whole matrix is refused (`pristine_red` abort,
  `hooks/mutation_matrix.py:583,608-612`). A suite's pass requires BOTH a zero
  exit code AND its `OK` marker — either alone misjudges in one direction.
- **Done:** with a suite forced to fail unconditionally, the matrix reports TOOL
  ERROR / refuses, not "55/55 killed".
- **Incident:** with no pristine control, an always-red suite made every mutation
  look "killed" → a perfect score with zero discriminating power; the oracle also
  ignored exit codes. Found by cross-family review, raised HARDENING→BLOCK.

### R3 — "equivalent/unreachable" is empirical, proven by a probe not an argument
- **Trigger:** marking a mutation `equivalent`, or "this branch can't be reached".
- **Do:** attempt the specific input that would reach it before excluding it. The
  `equivalent` class exists but is deliberately UNUSED
  (`reviews/2026-07-25-skill-vetting-snapshot-threat-model.md`, "Verification
  obligations"): two were once declared equivalent on an argument and one argument
  was false.
- **Done:** if a probe reaches the branch and KILLS the mutant, add/retain the
  killing test and leave `equivalent` UNSET — the harness records killed+equivalent
  as `unexpected` and exits nonzero (`hooks/mutation_matrix.py`; the "killed, but
  DECLARED EQUIVALENT" path). Set `equivalent` ONLY for an otherwise-unkillable
  mutant backed by a runtime-scoped dynamic justification (the covenant in
  `hooks/test-mutation_matrix.py`).
- **On failure (reachability inconclusive):** leave `equivalent` unset, mark the
  case unresolved, and add instrumentation/test coverage or escalate — never
  exclude it by argument.
- **Incident:** the `_resolve_dot_base` `except OSError` branch was called
  unreachable by call-graph reasoning; deleting the working directory makes
  `os.getcwd()` raise `FileNotFoundError`, reaching it — and the mutant failed
  OPEN (clean digest, exit 0) for a deleted cwd (the
  `test_dot_fails_closed_when_the_working_directory_was_DELETED` case).
- ❌ "os.environ can't hold NUL and realpath won't raise, so it's unreachable."

### R4 — evidence is run-scoped, exclusive-create, and never self-verified
- **Trigger:** naming a per-run record, writing a summary, or a closure verifier.
- **Do:** identify every persistent artifact by a RUN id (`run_id =
  uuid.uuid4().hex[:12]`, `hooks/mutation_matrix.py:455`), not only the commit —
  and exclusive-create it. Never let a formatter be the sole oracle for its own
  output: prove the measured SET equals the intended set by comparing THREE
  independent sources of mutation IDs — (1) the IDs in the run-scoped record
  (`hooks/mutation_matrix.py` builds it at `:651-656` and exclusive-creates it via
  `write_record` at `:712-731`), (2) IDs parsed from raw stdout — the LEADING token
  of each per-mutant verdict line at `:651-673` (`killed`/`equivalent`/`SURVIVED`),
  NOT the summary block (`:761-790`) — its counts are at `:761-778` and it lists
  only the survivor/unexpected SUBSETS (`:779-790`), never the full killed set;
  capture the whole stdout directly (no `tee`) and read the run-id/commit from
  `:761-762` — and
  (3) the intended IDs from `git show <commit>:hooks/mutations.json`. Not the
  tool's own formatter cross-check.
- **Done:** a second (even partial `--only`) run on the same commit cannot
  overwrite the first's record; AND all THREE ID sets above are equal, with the
  record's run-id and commit matching the run under review — three self-consistent
  artifacts, not two, before a "measured == intended" claim.
- **Incident:** a per-mutant record named only by commit was silently truncated
  55→1 rows by a later partial run sharing that commit — the closure report had
  already cited a hash that no longer existed. A `restore_summary()` used to check
  its own printed output would agree with itself if buggy. A `tee`-piped exit code
  recorded `tee`'s status, not the tool's.
- ❌ "stdout and the record agree, so the run is sound" — two self-consistent
  artifacts can both miss one item and invent another.

### R5 — "clean git status" is not clean observable state
- **Trigger:** an "AUTHORITATIVE FOR CURRENT CHECKOUT" claim, or reworking the
  identity/drift check.
- **Do:** identity is a symmetric pre/post snapshot over the FULL
  `MEASUREMENT_PATHS` (the product code, not just the runner/definitions:
  `hooks/mutation_matrix.py:245`), comparing the on-disk blob to the HEAD blob
  (`_blob_matches_head`, `:448`; `identity_snapshot` at `:253` records the pair) —
  a check that does NOT depend on recognizing every git index flag — plus a scan
  for `assume-unchanged`/`skip-worktree` (`hidden_modifications`, `:300-335`,
  the scan at `:327-330`). The
  `--authoritative` run operates in a disposable worktree, never by in-place
  rewrite + `finally` restore.
- **Done:** an on-disk edit to `skill_snapshot.py` hidden by
  `git update-index --assume-unchanged` is caught; a SIGKILL mid-run leaves a
  throwaway worktree, not a mutated source on the branch.
- **Incident:** the blob check first covered only the runner and definitions, so a
  hidden edit to the actual subject went unmeasured while the tool printed
  AUTHORITATIVE: YES. `git status --porcelain` cannot see those flags. In-place
  rewrite + `finally` once left a mutated, unrestored source after a SIGTERM.
- ❌ "porcelain is clean, so the checkout matches HEAD."

### R6 — report categories separately; enforce authoritative mode in code
- **Trigger:** editing the result summary or the `--authoritative` gate.
- **Do:** keep `killed` / `survivor` / `tool-error` (and `equivalent`) SEPARATE,
  never a single ratio. The authoritative gate is a code-enforced ALLOWLIST
  (default-deny: the parsed namespace must equal the parser's own defaults), not a
  doc convention — sound only while every measurement-changing input is a CLI
  option. This premise is machine-guarded: `.github/checks.py` fails if
  `mutation_matrix.py` reads any env/config
  (`os.environ`/`getenv`/`configparser`/`tomllib`/`json.load(open`) (`checks.py:466-481`).
- **Done:** `python3 .github/checks.py` prints "mutation_matrix.py takes no
  env/config input …"; adding an env read there turns the check red.
- **Incident:** merged ratios ("97+55 both green") could not distinguish a broken
  tool from real coverage; a denylist of flags would miss a future one.

### R7 — a test's name/docstring/category comment is an unverified claim
- **Trigger:** adding a test whose name asserts a class ("…do_not_lose…",
  "…is_bounded…"), or reviewing a green suite as evidence.
- **Do:** confirm the fixture actually EXERCISES the asserted property — a
  substring/`"g" in r` check passes regardless; a test named for a race that only
  runs the no-contention path proves nothing. Duplicate test/class definitions
  silently shadow (Python keeps the last): `.github/checks.py` check 5 fails on
  duplicate `def test_*`/`class` IN THE TWO HOOK SUITES it names
  (`test-skill_snapshot.py`, `test-skill-vetting-advisory.py`), and it runs BEFORE
  the final `if failures:` decision (`checks.py:435-457` vs the decision at
  `:484-486`). It is not a repo-wide duplicate check.
- **Done:** `python3 .github/checks.py` reports "N tests, no shadowed duplicates"
  for those two suites; a test's assertion fails when its named property is
  violated (verify by mutation, R1).
- **Incident:** `test_concurrent_hooks_do_not_lose_an_update` asserted a property
  its fixture never reached (renamed to
  `test_concurrent_hooks_converge_and_at_least_one_advises_the_change` with an
  honest docstring); a duplicate-defined test was dead for several commits; an
  fd-count test asserted exact equality its own comment said didn't exist.
- ❌ "all its unit tests pass, so the property holds" — the name is not the
  coverage.

### R8 — the recurring meta-defect: verify with the shape the code actually eats
- **Trigger:** any verification probe, self-check, or "I tested it and it passed."
- **Do:** the input you verify with must match the input the code processes —
  same stripping, same indentation, same source. A probe that feeds an unstripped
  string to code that strips, or `seq -w 0 9` (yields `0..9`, not `00..09`) so
  both sides test nothing, or a `field()` regex anchored `^` against indented
  fields, "passes" while measuring nothing. Two-sided proof (a known-fail AND a
  known-pass input) is the discipline.
- **Done:** the probe fails on a known-bad input before you trust its pass.
- ❌ verifying a `;`-only candidate for a `$()` vulnerability — the sample avoided
  the hazard (INV-7 of the security skill; the same shape, at the evidence layer).

## When NOT to use

For runtime-invariant work on the hooks, **co-load** `skill-vetting-security-invariants`
— this skill stays required whenever the change adds/edits a test, or makes a
mutation/test-honesty/evidence claim (a runtime-hook change that adds a
property-asserting test needs BOTH). The campaign's dead ends and the
"fold-time-invented-mechanism" meta-signal → `skill-vetting-hardening-archaeology`.
Running the cross-model gate itself → `security-hardening-review-ops`.

## Re-verify (HEAD = 79ca49c, shipped PR #83 2026-07-26)

```
python3 .github/checks.py                     # check 5 + mutation_matrix env gate green
python3 hooks/mutation_matrix.py --help       # confirms --authoritative is the closure mode
bash hooks/test-mutation_matrix.sh            # HARNESS UNIT suite (tests the tool, not your code)
grep -n 'MEASUREMENT_PATHS' hooks/mutation_matrix.py   # includes both .py subjects
```
`bash hooks/test-mutation_matrix.sh` (the harness unit suite) can exceed a 2-min
local cap; CI budgets it 10 min. The authoritative mutation run is the separate
`python3 hooks/mutation_matrix.py --authoritative` on a clean checkout — do not
report either as the other, and do not claim an authoritative run happened unless
its run-scoped record was captured.
