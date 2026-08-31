# MOD-AXIS-MODE mechanical closure gate — REPORT (2026-09-01)

Authorization: owner ruling — Sol NC1 finding VALID, Δ10 gloss line REFUTED,
exact one-line owner repair (MOD-AXIS-MODE) approved; no further reviewer
loop; closure is mechanical, one-shot; a second substantive wording need =
STOP.

## Freeze chain (all hashes machine-generated)
- Source of truth: sealed pre-NC1 archive
  `~/Developer/fable-archive/c8-design-gate-20260831.tar.gz`
  sha256 9e32e4a4cfb165f070c748617f38a6e019f5a462d37d29b8093583bbad6796db —
  re-verified OK before extraction.
- Extracted `DESIGN-v4.md` sha256
  07f53b8cf8b07065705df4d33c18fd09bab0f08816b063bc67e7d15bb68f7470
  (matches the recorded v4 freeze).
- MOD-AXIS-MODE applied by script, unique-match asserted →
  `DESIGN-v4-owner-repair.md` sha256
  788f80c7ac35178026b485f4ee11012a2308cc789eef70530ec5082a9fb0d97a.
- Byte-delta proof (`mod-axis-mode.diff`): exactly 1 removed + 1 added line,
  both the `read_reach:` schema line; zero other hunks.

## Checks (`closure_checks.py`)
- REPAIRED arm: **23/23 PASS, exit 0** (`closure-repaired.log`) — C-series
  repair + same-shape sweep (no `axis-value → packet-only` implication
  anywhere; no plane-1 axis line carries mode words), A-series clause
  anchors (§5 any-reviewer-directed-capability live trigger; §9(i)
  mode-decided-by-capability; unknown≠disabled; affirmative-bound credit;
  banner-metadata non-evidence; operator-owned authority; indirection
  exclusion; propose→grant; transport-not-a-trigger), and the owner's
  eight-row truth table T1–T8, each row bound to the named clauses.
- MUTANT control arm (unrepaired v4): **8 FAIL, exit 1**
  (`closure-mutant.log`) — fails exactly on the conflation checks
  (C1/C2/C4/C5) and their dependent truth-table rows: the gate demonstrably
  can fail, and fails on the defect it exists to catch.
- Core invariant held: mode is a property of the effective
  reviewer-directed capability envelope, never an alias of any individual
  receipt field.

## Check-layer correction (disclosed; zero design bytes touched)
`closure_checks.py`'s first C6/T1 encoded a stale premise — a
`review_mode:` schema FIELD, which existed in design v1 only; the round-1
two-plane restructure made mode a §5-derived classification, not a receipt
axis. C6 was corrected to test the actual v2+ semantics (mode classification
defined and §5-derived); both arms re-ran after the fix. This was a defect
in the check, not in the design; it is not a substantive design correction.

## Result
ALL PASS → per the owner's pre-committed rule:
**⑧ design = OWNER-ACCEPTED-WITH-REPAIR; implementation / landing-to-PR
preauthorized (base main = b6da89b).** Final-acceptance source = owner
adjudication + this mechanical closure — NOT reviewer consensus; the
original gate stays CAP-REACHED/NOT-PASSED and NC1 stays NOT-PASSED (1/2)
in every durable record.
