#!/usr/bin/env bash
# Gate runner. Discovers every <dir>/run.mjs next to this script (plus optional
# project.sh), runs each, prints PASS/FAIL per gate, exits non-zero if any fail.
# Usage: bash checks/run-all.sh
set -u
cd "$(dirname "$0")"

pass=0
fail=0

run_gate() {
  name="$1"
  shift
  if out=$("$@" 2>&1); then
    printf '  PASS  %s\n' "$name"
    pass=$((pass + 1))
  else
    printf '  FAIL  %s\n' "$name"
    printf '%s\n' "$out" | tail -n 20 | sed 's/^/        /'
    fail=$((fail + 1))
  fi
}

for gate in */run.mjs; do
  [ -e "$gate" ] || continue
  run_gate "$(dirname "$gate")" node "$gate"
done

# project.sh runs from the repo root so commands like `eslint .` see the whole repo.
[ -e project.sh ] && run_gate project bash -c 'cd .. && bash checks/project.sh'

printf '%d passed, %d failed\n' "$pass" "$fail"
if [ "$fail" -gt 0 ]; then
  echo 'GATES RED — do not ship'
  exit 1
fi
