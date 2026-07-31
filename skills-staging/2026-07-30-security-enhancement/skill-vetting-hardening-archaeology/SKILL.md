---
name: skill-vetting-hardening-archaeology
description: Load before re-attempting any skill-vetting fix or design, or when reaching for a buried idea — "just add quotes / escape the name", "normpath will clean this path up", "just reject the .. case the reviewer found", "mark it equivalent / it can't be reached", "the sidecar/record proves it", "the commit message says it's fixed", "just run all the test scripts in a loop", "fixed the doc the reviewer flagged", a repro command writing under ~/.claude, editing delta_lines/anomaly_lines ordering, a fold that adds a novel algorithm, or "let me finish the D1–D5 design". Do NOT load to learn the current invariants (skill-vetting-security-invariants) or harness rules (mutation-matrix-evidence-discipline).
---

# skill-vetting hardening — failure archaeology

Dead ends from the PR #83 campaign (branch `workstream-b-skill-vetting-2026-07-25`,
merged `7cd2af6` 2026-07-26). Most were caught PRE-MERGE by cross-family review,
so the residue is in commit history and in-code comments, not `revert`s. Read the
disposition tag first — it says what kind of corpse this is.

**What to DO at any tripwire below (the Done for every entry).** When a tripwire
fires: (1) STOP the proposed mechanism/idea; (2) read the entry's disposition tag,
standing rule, and residue; (3) load the owning skill the entry names, or — most
entries name none — the skill that owns the affected surface (a live invariant →
`skill-vetting-security-invariants`; the harness/evidence →
`mutation-matrix-evidence-discipline`; neither → follow the fallback); (4) either
satisfy that skill's Done-check for the real change, or record the item unresolved
and escalate. **Done:** no dead mechanism survives in the plan or diff, AND either a
named owning-rule check passes or the item is recorded unresolved with its
disposition. An entry with no explicit **Residue** line has none tracked — treat
that absence as "no residue recorded", not "nothing to check".

**Owner map (each dead end → the installed rule that owns its current surface):**
quoting → `skill-vetting-security-invariants` INV-7; normpath & dot-path → INV-4;
transient/steady-state ordering → INV-3 (`partial`/`skip_baseline`); unreachable/
equivalent → `mutation-matrix-evidence-discipline` R3; evidence-artifacts
(tee/record) → R4; CI ordering → the harness suites (mutation-matrix) +
`.github/workflows/checks.yml`; doc-drift → R7/R8 or operational-rigor §5
twin-sweep. No installed owner (follow the fallback — record unresolved + escalate):
the config-dir scratch-write hygiene (its inspect-only procedure is UNCERTAINTY #9,
review-only — inline it if you act) and the deliberately-not-done D1–D5 designs.

## The one meta-signal above all — `recurring-trap`

**A fix invented as a NEW MECHANISM at fold time, under review pressure, is the
defect.** Of round-6's twelve fixes, 3 were defective and 6 more incomplete; the
3 defective ones shared exactly one property — each was a new mechanism invented
while folding, not a mechanical correction
(`reviews/2026-07-25-skill-vetting-round8-design.md`, the round-5/6/7 table).
**Standing rule:** when a fix requires inventing a mechanism (a new lock scheme, a
shape heuristic, a path guard), do not fold it under pressure — design it, attack
the design first, THEN implement. Three-defects-one-mechanism (operational-rigor
§5) is the signal: the mechanism, not the patch list, is wrong.
- **Tripwire:** any fold that adds a novel algorithm rather than correcting an
  existing one.

## Dead ends

### `dead` + `recurring-trap` — quoting to stop shell injection (commit 550689d)
- **Tried:** double-quoting the candidate-name placeholders in SKILL.md §3;
  commit `550689d` message CLAIMED the RCE fixed.
- **Why it died:** double quotes do not stop `$(...)`, backticks, `${…}`, or an
  embedded `"`; the RCE stayed live. The author's own verification used a
  candidate named with only `;` — the one class quotes DO neutralize — so the
  test was chosen to agree. Five independent round-7 lenses reproduced the bypass
  (`b427bf8`).
- **Standing rule:** quoting/escaping is the wrong abstraction for
  attacker-controlled shell input; its failure mode is invisible, so it is not a
  control. Verify an injection fix with `$()`/backtick samples, never a `;`-only
  one. The real fix is structural (bytes never reach the shell as syntax).
- **Residue:** `550689d` kept in history, corrected in the next commit
  (`b427bf8`) by owner decision — not rewritten. **Residue, not in-progress work.**
- **Tripwire:** "just add quotes / escape the name."

### `dead` — `os.path.normpath` for symlink/trailing-slash laundering (round 5)
- **Tried:** `normpath` to canonicalize a trailing-slash symlink laundering case.
- **Why it died:** `normpath` does textual `..` folding (wrong across symlinks)
  AND `normpath(b"") == b"."`, so an empty/unset path (e.g. `$SKILL_DIR` unset)
  became a clean digest of the CWD with exit 0 — a fail-closed→fail-open
  regression, straight onto §3's SAFE-TO-PROPOSE green light.
- **Standing rule:** never borrow a general path util for a security path — write
  the minimal function that does only what is needed (`_strip_trailing`). Empty and
  unset paths fail CLOSED; dot-resolution is gated on ARRIVAL EVIDENCE, not on the
  `..` spelling (a `..` that resolves to the current non-symlink `$PWD` passes —
  see `skill-vetting-security-invariants` INV-4; "just reject `..`" is the refuted
  narrow fix in the next entry).
- **Tripwire:** "normpath will clean this path up."

### `recurring-trap` — dot-path addressing, mis-fixed one spelling at a time
- **Tried:** guard `..` laundering by rejecting the reported spelling; reviewers
  proposed "unconditionally reject `..`".
- **Why it died:** each narrow fix left a sibling spelling open —
  `<link>/sub/../.` (the `/.` stripped back to `..`), unset `$PWD` laundering with
  bare `.`, `$PWD`≠cwd. "Reject `..`" closed only ~1/3.
- **Standing rule:** a guard that compares two derived values must be tested
  against EVERY input class that makes the compare vacuous; converge on "evidence
  of arrival" (`$PWD` is the candidate, non-symlink), not on enumerating bad
  spellings. `_resolve_dot_base` is the converged form.
- **Tripwire:** "just reject the `..` case the reviewer found."

### `recurring-trap` — transient-vs-steady-state classification, mis-fixed 3×
- **Tried (three axes):** round-6 "anomalous vs clean" → pass-8 "transient vs
  steady-state" → pass-9 "will THIS run's baseline advance consume it".
- **Why the first two died:** a `partial` candidate is "new" every run (never
  consumed), so classifying it transient let it re-claim the front display slots
  forever and starve a genuinely new skill.
- **Standing rule:** display/notification priority keys on "is this event consumed
  this run" (`skip_baseline`), not on how it looks; a one-shot signal missed is
  lost forever, a steady-state one only delayed. When a subtle classifier is
  "not wrong, just not narrow enough" twice, suspect the third fix too.
- **Tripwire:** editing `delta_lines`/`anomaly_lines` ordering or `MAX_LISTED`.

### `dead` — "this branch is unreachable, no test needed"
- **Tried:** marking the `_resolve_dot_base` `except OSError` branch an equivalent
  mutant on call-graph reasoning.
- **Why it died:** deleting the working directory makes `os.getcwd()` raise
  `FileNotFoundError` (an `OSError`) — reachable — and the mutant failed OPEN.
- **Standing rule:** "unreachable/equivalent" is empirical; prove it with the
  input that would reach it before excluding it from testing.
- **Tripwire:** "mark it equivalent / it can't be reached."

### `dead` — evidence artifacts that lie (tee exit code, commit-named records)
- **Tried:** `echo "exit=$?" | tee` to capture a subprocess exit code; per-mutant
  records named only by commit hash.
- **Why they died:** the pipeline's status is `tee`'s, not the tool's (forced a
  child exit 7, wrapper still reported 0); a later partial run on the same commit
  silently overwrote a 55-row record down to 1 — after the closure report cited
  its hash.
- **Standing rule:** capture exit status without a pipe (`status=$?; … ; exit
  "$status"`); name evidence by RUN id + exclusive-create. (Full set:
  `mutation-matrix-evidence-discipline` R4.)
- **Tripwire:** "the sidecar/record proves it."

### `recurring-trap` — scratch writes into the real config dir (twice)
- **Tried:** ad-hoc verification commands without setting `CLAUDE_CONFIG_DIR`.
- **Why it recurred:** the isolation var was inherited-or-forgotten; the SECOND
  occurrence was a real product bug — the `_log` fallback hard-coded `~/.claude`
  instead of honoring `CLAUDE_CONFIG_DIR` — and was caught by a third-party review
  lens finding stray files in the real home dir.
- **Standing rule:** every test/verify subprocess touching config/state paths sets
  `CLAUDE_CONFIG_DIR` explicitly; audit the real dir after any manual repro. The
  `_log` bug is fixed + regression-tested.
- **Residue:** two stray files were left in the real `~/.claude/skill-vetting/`
  during the session and moved out; the session reported the component was not
  installed there (so they would be inert), but that cannot be confirmed from the
  repo — a maintainer inspects the real dir on the session machine (UNCERTAINTY #9
  gives the inspect-only, do-not-delete procedure). **Operator hygiene,
  history-only.**
- **Tripwire:** any repro command writing under `~/.claude`.

### `mooted` — CI ordering hid the real Linux failure
- **Tried:** running `hooks/test-*.sh` in glob (alphabetical) order under `set -e`.
- **Why it died:** `test-mutation_matrix.sh` sorts BEFORE the two product suites
  its own pristine control depends on, so on Linux the first failure surfaced in
  the harness's control, `set -e` aborted, and the product suites never ran
  standalone — their real failure never appeared in the log.
- **Standing rule:** a suite whose control depends on other suites runs LAST; a
  diagnostic must preserve the underlying suite's output. Made moot by reordering
  the CI job (`.github/workflows/checks.yml` runs the matrix suite last).
- **Tripwire:** "just run all the test scripts in a loop."

### `recurring-trap` — one claim restated in many files drifts (~14×)
- **Tried:** correcting an overclaim by fixing the file the review pointed at.
- **Why it recurred:** the same claim lived in code comments, docstrings, README
  ×2, the threat model, and test-failure strings; ~14 passes each fixed the
  nearest copy and left a farther, more-authoritative one stale — twice a commit
  message claimed "all N fixed" when it wasn't.
- **Standing rule:** correct an overclaim by searching the WHOLE repo for the
  concept (not the literal string — paraphrases evade grep), fixing every
  restatement, and verifying zero residue before claiming "fixed everywhere."
  (`test-and-doc-consistency` if that skill is present; else operational-rigor §5
  twin-sweep.)
- **Tripwire:** "fixed the doc the reviewer flagged."

## Deliberately NOT done (do not "helpfully" finish these)

The round-8 design `reviews/2026-07-25-skill-vetting-round8-design.md` (D1–D5) is
an **unimplemented DESIGN**. It exists to be attacked BEFORE it is written,
because the campaign proved that folding these under pressure produces defective
fixes. None shipped in PR #83.

- **D1 self-minted selector addressing / D4 export-then-review** (closes G3-SHELL).
  ❌ "I'll just add the `--select`/`export` subcommands, the design is right
  there." — containment-by-enumeration, the `--dest` attack surface, and
  export/live digest coherence were ANSWERED by the round-8 first pass and folded
  in (`round8-design.md:462-483`); the ACTUAL still-open questions
  (`:485-505`) are flock portability on network mounts, false-BLOCKs from
  candidates that legitimately ship a symlink, the reviewer-attention cost of
  tokenized paths, unbounded growth of `prior_adverse_digests`, and whether the
  collapsed one-line judged-unsafe summary is informative enough. Implement only
  through a fresh design-then-attack gate that addresses those.
- **D2 `fcntl.flock`** (I11 serialization). ❌ "swap the hand-rolled lock for
  flock, done." — the design lists five things flock still gets wrong (never
  unlink on release, one lock path for hook+`record`, hold scope, network-mount
  no-op, merge-correctness). A naive swap reopens dual-holders.
- **D3 names-out-of-the-advisory** (G3 prose injection). ❌ "add a length/
  separator cap." — measured net-negative and REVERTED: it blocked legitimate
  names while admitting CamelCase imperatives. A shape heuristic cannot separate
  an identifier from compact natural language (3 lenses converged).
- **D5 judged-unsafe state machine** (adverse verdict stays loud). ❌ "make BLOCK
  re-advise every session." — the design shows the naive form is a fresh budget
  poisoner and is rename-erasable by ADV-1; it needs content-keyed stickiness,
  slot reservation + collapse, and a clearing path.

## Rejected options (do not refight)

- **Subprocess separation of hook↔primitive** — no isolation gain at equal
  privilege; adds the argv/JSON encoding surface I1 exists to kill.
- **No baseline / advise everything every session** — permanent alarm noise trains
  users to ignore the tripwire (round-1 cry-wolf, "SV-8"); owner chose
  silent-when-clean.
- **Baseline advances only on recorded vetting verdicts** (round-2 R2-08 strong
  form) — converts an advisory tripwire into an enforcement loop, nags first-party
  authors, no integrity gain vs ADV-2. Its intent is honored non-naggingly by the
  `status`/`record` lifecycle (untested — reconsider only with new evidence, not
  a re-proposal).

## When NOT to use

Current shipped invariants → `skill-vetting-security-invariants`. Harness/evidence
mechanics → `mutation-matrix-evidence-discipline`. Running the review campaign →
`security-hardening-review-ops`.

## Re-verify (HEAD = 79ca49c)

```
git show 550689d --stat && git show b427bf8 --stat   # the false-claim + its correction, both in history
grep -rn "NOT MET\|STILL_OPEN\|D1\|D2\|D3\|D4\|D5" reviews/2026-07-25-skill-vetting-*.md
```
If D1–D5 have since been implemented, the "deliberately not done" section is
stale — move each landed item to the invariants skill and re-verify its tests.
