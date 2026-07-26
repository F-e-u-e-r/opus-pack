#!/usr/bin/env bash
# Unit matrix for hooks/skill_snapshot.py — the observation/persistence
# primitive behind the skill-vetting advisory hook. Proves the injective
# manifest encoding (crafted collision pairs), fd-verified reads (FIFO cannot
# hang, type swaps are anomalies), fail-closed anomalies (oversize, budgets,
# permission denied, symlinks; hostile/non-UTF-8 NESTED names are
# bytes-faithful and NOT anomalies since round 6 removed that gate), the
# hardened baseline
# I/O (symlinked cache/tmp attacks refused, corrupt vs absent vs stale
# distinguished), and the two-sided CLI (digest exit codes; record refusing
# SAFE-TO-PROPOSE on an anomalous tree). The matrix lives in
# hooks/test-skill_snapshot.py.
set -eu
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
command -v python3 >/dev/null 2>&1 || { echo "SKIP: python3 required" >&2; exit 0; }
exec python3 "$root/hooks/test-skill_snapshot.py"
