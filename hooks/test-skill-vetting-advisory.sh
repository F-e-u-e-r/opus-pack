#!/usr/bin/env bash
# Regression suite for hooks/skill-vetting-advisory.py — a PURE-ADVISORY
# SessionStart delta-detector (signature scanning removed: not a security
# boundary). Covers both sides of the advisory contract (silent and advisory)
# and the fail-closed paths the threat model promises, with the two exceptions
# it records as open (G3-SHELL has no test in either suite; I11 is NOT MET, so
# the lock carries a known-broken pin rather than an assertion): whole-tree deltas (add/modify/delete/rename,
# not just SKILL.md), anomalies (symlink/special/unreadable/oversize/hostile
# names) always advising, corrupt/stale baseline surfacing visibly,
# delivery-before-baseline-advance, env-based root resolution
# (CLAUDE_CONFIG_DIR / CLAUDE_PROJECT_DIR), multi-project stability, the
# display cap never hiding counts or anomalies, and the degraded-mode
# advisory. The matrix lives in hooks/test-skill-vetting-advisory.py.
set -eu
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
command -v python3 >/dev/null 2>&1 || { echo "SKIP: python3 required" >&2; exit 0; }
exec python3 "$root/hooks/test-skill-vetting-advisory.py"
