---
name: skill-vetting-security-invariants
description: Load when editing hooks/skill_snapshot.py or hooks/skill-vetting-advisory.py, changing the digest/baseline/anomaly logic, editing skills/skill-vetting/SKILL.md §3, touching the display allowlist or the digest/record/status CLI, or about to cite G3/G3-SHELL/any I-numbered invariant as met. A runtime-hook change that also adds/edits a test or makes a test/evidence claim ALSO loads mutation-matrix-evidence-discipline. Behavior-only runtime work uses this skill rather than mutation-matrix (and vice-versa) — that split is only about the security↔mutation pair and does not suppress security-hardening-review-ops during a hardening campaign or a security-sensitive push/PR/merge.
---

# skill-vetting security invariants

The `skill-vetting` advisory tripwire is a SessionStart hook that watches
installed skills and injects one advisory line when one appears, changes,
disappears, or cannot be fully observed. Its threat model treats **the author of
watched content (ADV-1) as controlling every byte, name, type and shape** under
the watched trees; same-privilege local code (ADV-2) is out of scope by design.
These invariants shipped hardened in **PR #83 (`7cd2af6`, merged 2026-07-26)**
over a multi-round cross-family campaign; the design record
`reviews/2026-07-25-skill-vetting-snapshot-threat-model.md` defines **goals
G1–G6 + G3-SHELL and invariants I1–I11** (I12–I17 belong to the *unimplemented*
round-8 design — see the last section). Each invariant below violates "breaks
users you cannot see": a silently-missed trojan edit, a discarded BLOCK, a hung
session start.

## Boundary map

| Path | Role |
|---|---|
| `hooks/skill_snapshot.py` | observation + persistence primitive: `scan_root`, `snapshot_tree`, canonical digest, baseline I/O, and the `digest`/`record`/`status` CLI. Decides no verdicts. |
| `hooks/skill-vetting-advisory.py` | thin SessionStart hook: resolves roots, compares snapshot vs baseline, composes/delivers the advisory, advances the baseline. No filesystem-walking of its own. |
| `skills/skill-vetting/SKILL.md` | the procedure an agent follows to vet a candidate; §3 binds a verdict to an exit-0 digest. |

The two files are imported in-process, never spawned — passing attacker
path-bytes across an argv/JSON boundary would add an encoding surface for no
isolation gain (both run at the same privilege). Do not "improve" this into a
subprocess split.

## Invariants

### INV-1 — a structural refusal must never set the shared budget (I8)
- **Trigger:** any change to the walk budget, `MAX_DEPTH`/`MAX_OPEN_DIRS`, or a
  thought like "unify the caps so exhaustion is handled in one place".
- **Invariant:** `MAX_ENTRIES`/`MAX_TOTAL_BYTES` are SHARED across candidates and
  set `budget["stop"]`; `MAX_DEPTH`/`MAX_OPEN_DIRS` are PER-CANDIDATE structural
  refusals that do NOT DIRECTLY set `budget["stop"]` — they mark that candidate
  anomalous (`hooks/skill_snapshot.py:82-89`; the `budget` dict at `:326`). Their
  anomaly record still flows through `_entry`, which increments the shared entry
  counter and CAN trip `MAX_ENTRIES` at the boundary like any other entry
  (`:209-214`); what is forbidden is a structural cap poisoning the budget merely
  because it fired.
- **Done-check:** `grep -n 'budget\["stop"\] = True' hooks/skill_snapshot.py` —
  every set (at `:214`/`:256`) traces to a resource cap
  (`MAX_ENTRIES`/`MAX_TOTAL_BYTES`), never to depth/fanout.
- **Incident:** conflating them let one skill holding 31 empty nested directories
  hand every LATER candidate the same constant, content-independent digest, so
  `is_changed` was permanently False for them (round-6 "budget poisoner"; I8 in
  the threat model).
- **Don't simplify back to:** "a breach stops that skill's scan" — a shared stop
  poisons siblings.
- ✅ depth breach → that candidate is anomalous but NOT `partial` (`partial` is
  budget truncation, INV-3); it doesn't DIRECTLY stop the shared budget (its
  anomaly entry is still counted normally). ❌ "one exhaustion flag is cleaner" —
  that flag is the poisoner.

### INV-2 — CLI and hook are different entry points that converge on shared encoding (G6/I1)
- **Trigger:** adding a branch for a new file type in `snapshot_tree` or
  `scan_root`, or "the CLI and hook can each format this case".
- **Invariant:** the CLI (`digest`/`record`) enters through `snapshot_tree`
  (`hooks/skill_snapshot.py:289`; callsites `:912,:1055`); the hook enters
  through `scan_root` (`:551`, called from `skill-vetting-advisory.py:303`). They
  are DIFFERENT entry points that AGREE because both route every terminal
  (non-regular) case through the shared `_anomaly_snap` (`:526`) — `snapshot_tree`
  at `:328-383`, `scan_root` at `:617-634` (plus `:649`) — rather than
  hand-rolling. A regular file is encoded via `_entry` (`:209`): the CLI's
  top-level loose-file case at `:365`, nested files/anomalies in `_walk_dir`
  (`:390`) at `:413-515`. The invariant is the shared terminal encoder, not a
  single entry function.
- **Done-check:** `grep -n '_anomaly_snap(' hooks/skill_snapshot.py` shows every
  terminal case in BOTH `snapshot_tree` and `scan_root` going through it; neither
  entry point hand-rolls a divergent terminal tuple.
- **Incident:** round-5 unified only the symlink branch; FIFO and unreadable-dir
  still diverged, so a CLI-recorded BLOCK was judged "changed" and discarded next
  session.
- **Don't simplify back to:** two hand-written encoders "kept in sync by tests",
  or hand-rolling a terminal case in one entry point.
- ✅ new terminal type → one `_anomaly_snap(kind,…)` case reached by BOTH entry
  points. ❌ a bespoke tuple in `snapshot_tree` "just for FIFOs" that `scan_root`
  doesn't match.

### INV-3 — a partial snapshot is never stored as a real digest (I9)
- **Trigger:** touching baseline write, the `partial` flag, or `skip_baseline`.
- **Invariant:** a budget-truncated snapshot is `partial` (its digest describes
  the SCAN STATE, not the tree); the hook sets `skip_baseline = partial and old
  is None` and skips only the baseline WRITE, never the advisory
  (`hooks/skill-vetting-advisory.py:489`); a `partial` re-observation of a known
  candidate keeps the prior record (`entry = dict(old)` at `:491`). The `record`
  CLI likewise refuses to bind a verdict to a `partial` digest.
- **Done-check:** `grep -n 'skip_baseline\|partial' hooks/skill-vetting-advisory.py`
  — a `partial and old is None` candidate is advised but not baselined.
- **Incident (a fix that regressed):** an earlier guard did `continue` here,
  skipping the whole candidate — a single 4200-file skill (vs `MAX_ENTRIES=4096`)
  then made the hook emit ZERO bytes every session, taking every candidate after
  it into silence (documented inline at `:480-488`).
- **Don't simplify back to:** "skip the candidate if we couldn't fully read it."
- ✅ skip the baseline write only. ❌ `continue` — that is the silent-miss the
  whole component exists to prevent.

### INV-4 — path identity comes from proven arrival, dot-paths fail closed
- **Trigger:** editing `_resolve_dot_base`, `_strip_trailing`, or any path
  normalization; or reaching for `os.path.normpath`.
- **Invariant:** `_resolve_dot_base` (`hooks/skill_snapshot.py:847`, predicate at
  `:894-903`) resolves a `.`-form path ONLY on ARRIVAL EVIDENCE, not spelling:
  `$PWD` is set, `realpath($PWD) == realpath(the path)`, and `$PWD` is not itself a
  symlink. So a bare `.` — OR a `child/..` that resolves back to the current
  non-symlink `$PWD` — passes; a `..` that resolves AWAY from `$PWD` (the common
  case: cwd IS the candidate, so `..` is the parent≠`$PWD`), unset `$PWD`, and
  `$PWD`≠the-path all return `_REFUSE` → the CLI prints "REFUSED" and exits **2**
  (`:929-937` digest, `:1008-` record), distinct from a badname ANOMALY (exit 3,
  `:938-949`). It is NOT "`..` always refuses" — that is the very oversimplification
  the incident below rejects. `normpath` is never CALLED (`_strip_trailing` at
  `:187` does only trailing-slash stripping; sole normalization entry, callsites
  `:324/577/919/996`).
- **Done-check:** `grep -nE 'normpath\(' hooks/skill_snapshot.py` returns nothing
  (the word survives only in comments `:189/190/192/323`); AND drive the resolver
  BOTH ways from the repo root, where subdir `skills/` is directly under `$PWD` so
  `skills/..` resolves back to `$PWD`: `python3 hooks/skill_snapshot.py digest
  skills/..` RESOLVES (exit 3 by content, arrival evidence — a `..` that does NOT
  refuse), while `env -u PWD python3 hooks/skill_snapshot.py digest skills/..`
  REFUSES (exit 2, no `$PWD`). The regression is
  `test_every_dot_spelling_without_arrival_evidence_refuses`
  (`hooks/test-skill_snapshot.py:1317`).
- **Incident:** `normpath(b"") == b"."` turned a fail-closed empty/unset path into
  a clean digest of the CWD with exit 0 — the exact green light §3 binds
  SAFE-TO-PROPOSE to; dot-path laundering recurred across ~5 spellings before
  converging on "evidence of arrival, not spelling".
- **Don't simplify back to:** "just reject `..`" — `<link>/sub/../.` and unset
  `$PWD` still launder (the reviewers' own proposed narrow fix, refuted).
- ✅ `$PWD`-proven, non-symlink → resolve. ❌ text-level `..` handling.

### INV-5 — a failed first write is ADVISED, not silent; the baseline stays absent (N-CORRECTION)
- **Trigger:** editing baseline bootstrap / the `absent` state.
- **Invariant:** first-run bootstrap announces its count BEFORE the write. If that
  first write FAILS, the run still ADVISES (it is not silent) and does NOT write
  the baseline — so the next session sees `absent` again and re-advises rather
  than silently bootstrapping whatever the content has become (G5
  deliver-before-advance makes the un-written baseline safe). There is no
  GUARANTEED baseline-state failure marker; `_log` may leave a best-effort warning
  in `advisory.log` (`hooks/skill-vetting-advisory.py:120-150`, called at
  `:701-704`), but that is a forensic trace, not the safety mechanism — safety
  comes from advise-and-don't-advance. (Known doc-defect: the repo's canonical
  docs OVERSTATE this — threat-model I6 `:296` says a failed write "is logged" and
  both READMEs call advisory logging "auditable" — while `_log` swallows all
  exceptions (`advisory.py:149-150`, def at `:120`). The CODE is authoritative;
  the docs are an upstream fix — see UNCERTAINTY.md.)
- **Done-check:** run the regression — `python3 hooks/test-skill-vetting-advisory.py
  HookE2E.test_failed_first_write_does_not_silently_bootstrap_a_change` prints `OK`
  (it lives at `hooks/test-skill-vetting-advisory.py:132` and asserts the advisory
  context is non-empty — "a failed first write must not be silent" — AND that the
  baseline file was not written).
- **Incident:** a transient first-write failure used to leave no trace and emit
  nothing, so the next session treated changed content as a fresh silent bootstrap
  and never advised it (round-6; the inline test comment records this).
- **Don't simplify back to:** silently writing the baseline on a first run before
  the advisory is delivered, or treating a failed write as a completed one.

### INV-6 — audit visibility is monotone with severity, and fails closed (`status`)
- **Trigger:** editing `_cli_status`, its partition, or its exit codes.
- **Invariant:** `status` splits `unvetted` / `adverse_verdicts_in_baseline` /
  `vetted_safe`; `absent`→exit 0 (truthful empty BASELINE state — nothing recorded
  yet; NOT a claim that no skills are installed — `status` reads the baseline and
  never lstats, `:1170`), `corrupt`/`stale`→exit 4 (audit could not be performed),
  any adverse verdict→exit 3 (`hooks/skill_snapshot.py:1152-1189`).
- **Done-check:** two ways. (1) Isolated live fixture (nothing real touched):
  `CLAUDE_CONFIG_DIR=$(mktemp -d) python3 hooks/skill_snapshot.py status; echo $?`
  → prints `{"baseline": "absent"}` (json.dumps spacing) and exit 0 on an empty
  world. (2) Drive the absent/unusable AND adverse branches via the regressions —
  `python3 hooks/test-skill_snapshot.py
  CommandLine.test_status_exit_code_separates_absent_from_unusable
  CommandLine.test_status_surfaces_an_adverse_verdict_instead_of_hiding_it` prints
  `OK` (a corrupt/stale baseline exits 4; a recorded BLOCK shows in
  `adverse_verdicts_in_baseline` and exits 3).
- **Incident:** the old partition was `status != "vetted"` and never printed the
  verdict, so recording BLOCK on a live trojan REMOVED it from the only list the
  command printed — the more damning the verdict, the cleaner the report. The
  field was renamed off `_still_installed` because `status` reads the baseline and
  never lstats (`:1170-1173`).
- **Don't simplify back to:** "one list of the unvetted."
- ✅ severity raises visibility + a nonzero exit. ❌ a success exit when the audit
  itself could not run.

### INV-7 — a hostile candidate name never becomes shell syntax; `digest`/hook anomaly it, `record` refuses only SAFE (G3)
- **Trigger:** editing SKILL.md §3, or "add quoting so the candidate name is safe
  on the command line".
- **Invariant (current, procedural):** a candidate name that fails the display
  allowlist is an anomaly (exit 3) for `digest` and for the hook; for `record` it
  refuses only SAFE-TO-PROPOSE — so a BLOCK/SUSPECT verdict CAN still be recorded
  against a hostile-named tree, which reports no anomaly. SKILL.md §3 directs: a
  hostile name is itself strong evidence → record BLOCK in prose with the reason,
  do NOT substitute it into any shell command (`skills/skill-vetting/SKILL.md`,
  the `$(...)`/backtick discussion at `:181-197`; the verdict-fail-closed note at
  `:111`).
- **Done-check:** the implemented half is executable —
  `python3 hooks/test-skill_snapshot.py CommandLine.test_record_refuses_safe_on_hostile_name`
  prints `OK`. That proves ONLY that `record` refuses SAFE-TO-PROPOSE for a hostile
  DISPLAY NAME; it does NOT prove shell non-substitution (G3-SHELL, still untested).
  What must hold: no
  basename that FAILS the display allowlist enters shell source, quoted or
  otherwise — it routes to a BLOCK-in-prose path; an allowlisted name relies on the
  inert alphabet (`[A-Za-z0-9._-]`), NOT quoting (never the control). **G3-SHELL
  itself has NO test** and remains open (below); in-tree filenames are a separate
  open hole.
- **Incident:** round-6 "fixed" the RCE by double-quoting placeholders and the
  commit message CLAIMED it fixed — false: quotes do not stop `$()`/backticks, and
  the verification used a candidate named with only `;` (the one class quotes DO
  block). **Five** independent round-7 lenses reproduced the bypass (`b427bf8`).
- **Don't simplify back to:** quoting/escaping — the failure mode is invisible, so
  it is not a control. **G3-SHELL remains NOT MET, and its subject is exactly this
  candidate-name substitution:** the shipped procedure STILL puts the (quoted)
  candidate directory name into the `digest`/`record` command templates
  (`skills/skill-vetting/SKILL.md:204-224`; the threat model at `:127-138`).
  The display-gate + BLOCK-in-prose + inert allowlist is a PROCEDURAL mitigation
  that relies on the agent, NOT the structural fix (D1 self-minted addressing, no
  name on the command line). In-tree filenames are an ADDITIONAL open surface
  (round8-design), not the definition of G3-SHELL. See UNCERTAINTY.md.
- ✅ hostile name → BLOCK in prose, no shell interpolation. ❌ `"$(...)"` "is
  quoted, so it's safe."

## Known open items (do not claim these are met — see UNCERTAINTY.md)

At PR #83 merge these were documented `NOT MET`/OPEN in the threat model and
remain so in HEAD: **G3-SHELL** (the procedure substitutes the candidate
directory name into `digest`/`record` command templates; quoting is insufficient;
no test; D1 closes it — with in-tree filenames as an additional surface),
**the §1 procedure boundary** (reads then executes untrusted content before the
verdict — a separate open item, UNCERTAINTY #3), **G3 prose-injection** via an
allowlisted name (pinned open by
`test_prose_injection_via_an_allowlisted_name_is_STILL_OPEN`), **I11** full
concurrency serialization (the lock is hand-rolled `O_EXCL` at `:226`;
`fcntl.flock`/design D2 not landed), and the **I2** mid-scan swap window and
**I10** partial-with-prior half. The round-8 design
`reviews/2026-07-25-skill-vetting-round8-design.md` (D1–D5, invariants I12–I17)
is an explicitly **unimplemented** design, not shipped code.

## When NOT to use

Trusting/extending the mutation harness, evidence integrity, OR test/doc honesty
(vacuous assertions, duplicate-def shadowing, name-is-a-claim) →
`mutation-matrix-evidence-discipline` — but if your runtime-hook change ALSO
adds/edits a test, **co-load both**, not one alone. Generic
fix-a-defect-then-sweep-for-twins →
operational-rigor §5. Why a fold itself was defective →
`skill-vetting-hardening-archaeology`.

## Re-verify (HEAD = 79ca49c, shipped 2026-07-26)

```
python3 .github/checks.py                       # repo consistency gate: all green
bash hooks/test-skill_snapshot.sh               # primitive suite: OK (skipped=1)
bash hooks/test-skill-vetting-advisory.sh       # hook suite: OK
grep -nE 'normpath\(' hooks/skill_snapshot.py   # expect: no output = no call (INV-4)
```
`checks.py` validates published-skill frontmatter and sweeps ALL tracked text for
hidden-directive chars (it does not validate this staged library's frontmatter —
that is checked by hand). If any symbol path above has moved, re-derive it before
trusting the rule.
