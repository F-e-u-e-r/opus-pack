# skill-vetting advisory hook — threat model and snapshot invariants

2026-07-25. Written before the round-3 rework of `hooks/skill-vetting-advisory.py`,
as the design record the implementation and its tests are held against. The
round-1/round-2 cross-family security gate (grok-4.5 high + gpt-5.6-luna ultra +
gpt-5.6-sol max) returned ~24 mechanism findings against the first two cuts of
this hook; this rework rebuilds the observation layer instead of patching the
findings one at a time.

## Component and purpose

A **pure-advisory** `SessionStart` tripwire: when an installed skill appears,
changes, disappears, or cannot be fully observed, inject one advisory line
routing to the `skill-vetting` skill. It never blocks (SessionStart cannot
deny), never emits a "safe" line, and does not attempt to detect malice —
signature scanning is not a security boundary and has been removed; the
`skill-vetting` skill's full read is the actual check.

Two files:

- `hooks/skill_snapshot.py` — the **observation and persistence primitive**:
  root enumeration (`scan_root`), tree snapshot, canonical digest,
  baseline load/store, and a small CLI (`digest` / `record` / `status`).
  Library-shaped and unit-testable; its library core decides no verdicts (the
  CLI adds a thin verdict-recording convenience so the skill's §3 binding is
  executable).
- `hooks/skill-vetting-advisory.py` — the **thin hook**: resolves watch roots
  from the harness environment, orchestrates snapshot-vs-baseline comparison,
  composes and delivers the advisory, then advances the baseline. Contains no
  filesystem-walking logic of its own.

This mirrors the pack's existing split (`gate-before-commit.sh` dispatching
`parse-commit-command.py`). The primitive is imported in-process, not spawned:
passing attacker-controlled path bytes across an argv/JSON process boundary
would add an encoding surface for no isolation gain (both files run at the same
privilege either way).

## Assets

- **A1 — session integrity.** Installed skills steer every later session; a
  trojan edit that evades the tripwire gets standing authority silently.
- **A2 — advisory-channel integrity.** The advisory text itself reaches the
  model as context; attacker-authored strings inside it are prompt injection.
- **A3 — baseline integrity/availability.** The baseline file decides what
  counts as "unchanged".
- **A4 — session availability.** A SessionStart hook that hangs or stalls
  denies the whole session.

## Adversaries and trust boundaries

- **ADV-1: the author of watched content.** Controls every byte, name, type,
  and shape under the watched skill trees (and can update them between
  sessions). Goal: change or plant content without an advisory firing, or use
  the hook's own output as an injection channel. **In scope.**
- **ADV-2: same-privilege local code.** Can rewrite the baseline, the skills,
  or this hook itself. **Out of scope for resistance** — a user-level script
  cannot defend against its own privilege level; the baseline is *not*
  tamper-evident and is never presented as such. Honest documentation is the
  whole mitigation.

Trust classes: bytes and names under watched roots = untrusted data (never
echoed, never interpreted). Harness stdin + environment = harness-controlled
(parsed defensively, trusted for root resolution). The baseline file = an
availability artifact, not security evidence: its absence or corruption is an
observable, advisable event, never a silent state.

## Security goals

- **G1 — change visibility.** Any observable difference between the current
  watched trees and the last *delivered* baseline produces an advisory this
  session: add, modify, delete, rename, type change, symlink change — any file,
  not just `SKILL.md`. The safe failure direction is over-advising.
- **G2 — observation honesty (fail closed).** Anything the scanner cannot
  fully and unambiguously observe is an **anomaly** and always advises:
  unreadable file or directory, oversize file, entry/byte/depth budget breach,
  any symlink, any non-regular file (FIFO/socket/device), undecodable or
  hostile name, unreadable root, corrupt baseline. An anomalous tree is never
  "unchanged" and is never silently baselined as clean.
- **G3 — injection containment.** Advisory text is built from fixed template
  strings, counts, and validated identifiers only. A directory name is
  displayed only if it matches a conservative ASCII allowlist; otherwise an
  opaque digest-derived id is shown (and the hostile name is itself an
  anomaly). File paths and file content are never echoed.
- **G4 — bounded work, visible degradation.** Entry-count, per-file-byte,
  total-byte, and depth caps bound the scan; opens use `O_NOFOLLOW|O_NONBLOCK`
  so a planted FIFO cannot hang SessionStart; the walk is iterative. An
  unexpected internal error exits 0 (never breaks session start) but emits a
  generic "hook could not complete — changes may be unobserved" advisory when
  nothing has been printed yet: degraded, and labelled as such, never silent.
- **G5 — delivery before advance.** The baseline advances only after the
  advisory covering those deltas has been successfully written to stdout. A
  failed print leaves the baseline untouched, so the same deltas re-advise
  next session. A failed baseline write after a successful print re-advises
  too (stderr-logged); both failure orders converge on re-advising.
- **G6 — versioned binding.** One canonical, schema-versioned encoder produces
  every digest, shared by the hook and by the `skill-vetting` skill's verdict
  procedure through the same CLI. The baseline records the schema and policy
  versions; a version change invalidates it visibly (advisory + re-baseline),
  never silently.

## Non-goals (documented limits, not defects)

- **N1 — malice detection.** Removed by design; the skill's full read is the
  defense.
- **N2 — resisting ADV-2.** See above.
- **N3 — roots outside the watched set.** Plugin-managed skill caches are not
  watched; vet those manually.
- **N4 — same-session installs.** SessionStart-only; content landing after the
  scan is seen next session.
- **N5 — enforcing follow-through.** Once a delta has been delivered, the hook
  does not re-raise it every session (advisory posture, owner-chosen). The
  compensating, non-nagging control: the baseline records a per-skill vetting
  status (`baseline`/`seen`/`vetted`), the skill's §3 records verdicts through
  `skill_snapshot.py record`, and `skill_snapshot.py status` lists anything
  seen-but-never-vetted on demand.
- **N6 — TOCTOU perfection.** A tree mutating during the scan may straddle two
  runs' digests. Every content hash is computed from the exact bytes read off
  an opened fd, so each run is self-consistent; a mid-scan mutation lands as a
  delta on this run or the next. The residual failure direction is an extra
  advisory, not a miss; non-regular-file swap tricks are excluded by G2
  (fd-verified type, anomaly otherwise).
- **N7 — intermediate path-component symlinks on the watched-root PATH.**
  `O_NOFOLLOW` guards the final root component and every in-tree descent, but
  the ancestor path of a watched root (`$CLAUDE_CONFIG_DIR`, or
  `$CLAUDE_PROJECT_DIR/.claude`) is resolved normally. An attacker who can
  replace `.claude` itself (or the config dir) with a symlink already controls
  the agent's entire configuration — settings, hooks, every skill — which is
  ADV-2 (out of scope): defeating this tripwire is moot once that directory is
  theirs. We harden the final `skills` component and each skill dir; we do not
  build a component-by-component openat walk to defend a boundary whose breach
  is already full compromise.

## Snapshot invariants (the primitive's contract)

- **I1 — injective encoding.** The manifest serializes as a length-prefixed
  binary stream: a fixed header + schema version, then entries sorted by raw
  path bytes, each field (path, kind tag, payload) length-prefixed. No
  delimiter characters exist to collide with path or target bytes; two
  distinct observed trees cannot encode to the same stream. The digest is
  SHA-256 over that stream. (The round-2 collision repro — `a|b -> c` vs
  `a -> b|c` — must produce distinct digests, by construction and by test.)
- **I2 — fd-verified observation.** Type is decided by `lstat` and then
  re-verified by `fstat` on an fd opened with
  `O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC`; only regular files are hashed,
  from that fd's bytes. Symlinks record their raw target bytes and are
  anomalies (target *content* is intentionally never followed or hashed — a
  link's referent can change outside the tree, which is exactly why a symlink
  cannot be certified unchanged). Directories are manifest entries too, so
  empty-directory adds/removes change the digest.
- **I3 — byte-faithful names.** Paths are handled as bytes end to end
  (`os.fsencode`); undecodable names still hash exactly and are displayed only
  as opaque ids.
- **I4 — hard budgets.** `MAX_ENTRIES`, `MAX_FILE_BYTES`, `MAX_TOTAL_BYTES`,
  `MAX_DEPTH`. A breach stops that skill's scan (bounded work) and is an
  anomaly — never a silently-truncated hash (the round-2 oversize repro: a
  byte flipped beyond the old read window changed nothing; here oversize means
  anomaly, so it always advises).
- **I5 — anomaly dominates comparison.** Comparison yields
  `unchanged`/`changed`/`anomalous`; a snapshot containing any anomaly is
  `anomalous` regardless of digest equality, and always advises. Anomaly
  records (with stable reason codes) are part of the manifest, so an anomaly
  appearing or healing is itself a digest change.
- **I6 — hardened baseline I/O.** Read: `O_NOFOLLOW`, size-capped, strict JSON
  parse plus shape/enum/schema validation — any deviation is `corrupt`, which
  advises and rebuilds visibly. Write: same-directory `mkstemp` (0600) +
  `os.replace`; the parent directory is created 0700 and must be a real,
  caller-owned, non-group/world-writable directory; a symlinked baseline path
  or untrusted directory is an anomaly and the write is refused. A refused or
  failed write is logged and leaves the previous state (G5 makes that safe).
- **I7 — status lifecycle.** `baseline` (first-run bootstrap, silent by
  documented design), `seen` (delta observed and delivered), `vetted` (recorded
  only via the CLI `record` subcommand with a verdict). Statuses never affect
  delta detection — only reporting and the `status` listing.

## Architecture decision record

**Question.** Should the hook script itself hand-roll tree snapshotting,
caching, and hardened file I/O inline?

**Decision.** No. The observation/persistence layer moves into
`skill_snapshot.py` — small, policy-free, separately unit-testable, with the
encoding, budgets, anomaly taxonomy, and baseline I/O in one place — and the
hook becomes a thin dispatcher. Two rounds of cross-family review returning
~24 edge findings against one inlined function is the "three defects, one
mechanism" signal (operational-rigor §5): the mechanism, not the patch list,
was the problem.

**Rejected alternatives.**
- *Single-file monolith, patched per finding* — the shape that produced rounds
  1–2; interior functions were not independently testable and every fix risked
  its neighbors.
- *Subprocess separation* (hook shells out to the primitive) — real isolation
  gain is nil at equal privilege, while marshaling hostile path bytes across
  argv/JSON adds exactly the encoding-ambiguity surface I1 exists to kill.
- *No baseline at all* (advise everything every session) — maximally honest,
  but permanent alarm noise trains users to ignore the tripwire (the round-1
  cry-wolf finding, SV-8), and the owner explicitly chose silent-when-clean.
- *Baseline advances only on recorded vetting verdicts* (round-2 sol R2-08's
  strong form) — rejected for the hook: it converts the owner-chosen advisory
  tripwire into an enforcement loop, couples SessionStart output to a verdict
  store at the same trust level (no integrity gain against ADV-2), and nags
  authors of first-party skills every session. Its intent is honored
  non-naggingly by N5's status lifecycle + `record`/`status` + the skill's §3
  binding, and delivery-gating (G5) removes the silent-loss case that finding
  demonstrated.

## Verification obligations

Every goal and invariant above maps to a named executable test in
`hooks/test-skill_snapshot.sh` (primitive matrix) or
`hooks/test-skill-vetting-advisory.sh` (hook contract), covering at minimum:
add / modify / delete / rename / symlink / broken symlink / special filenames
(newline, backtick, injection text, non-UTF-8 bytes) / encoding-collision
pairs / oversize and budget breach / permission denied (file, subdir, root) /
mid-scan mutation / FIFO (no hang) / cache corruption, dangling-symlink cache,
symlinked tmp path / wrong or unset project-root env / delivery failure
(closed stdout ⇒ baseline not advanced) / version-change invalidation /
first-run bootstrap silence / multi-project baseline stability / display cap
with anomalies listed first and full count surfaced / advisory references the
real `skill-vetting` skill (no phantom command) / repo version sites agree
(checks.py). Anomaly ⇒ advise is asserted per class, not in aggregate.
