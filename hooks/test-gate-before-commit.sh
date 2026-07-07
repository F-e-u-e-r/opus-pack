#!/usr/bin/env bash
# Regression tests for gate-before-commit.sh and parse-commit-command.py.
set -eu

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

command -v jq >/dev/null 2>&1 || {
  echo "SKIP: jq is required by gate-before-commit.sh" >&2
  exit 0
}
command -v python3 >/dev/null 2>&1 || {
  echo "SKIP: python3 is required by gate-before-commit.sh" >&2
  exit 0
}

tmp=$(mktemp -d "${TMPDIR:-/tmp}/opus-pack-hook-test.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

red="$tmp/red"
green="$tmp/green"
gateless="$tmp/gateless"
mkdir -p "$red/checks" "$green/checks" "$gateless"
printf '%s\n' '#!/usr/bin/env bash' 'echo red gate' 'exit 1' > "$red/checks/run-all.sh"
printf '%s\n' '#!/usr/bin/env bash' 'echo green gate' 'exit 0' > "$green/checks/run-all.sh"

json_for() {
  COMMAND_TEXT="$1" python3 - <<'PY'
import json
import os

print(json.dumps({"tool_input": {"command": os.environ["COMMAND_TEXT"]}}))
PY
}

assert_exit() {
  expected="$1"
  name="$2"
  command_text="$3"
  fallback="${4:-$gateless}"

  set +e
  out=$(json_for "$command_text" | CLAUDE_PROJECT_DIR="$fallback" bash "$root/hooks/gate-before-commit.sh" 2>&1)
  code=$?
  set -e

  if [ "$code" -ne "$expected" ]; then
    echo "FAIL $name: expected $expected, got $code" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  printf 'PASS %s\n' "$name"
}

assert_exit 0 "non-commit allowed" "git status"
assert_exit 2 "single red commit blocked" "git -C $red commit -m x"
assert_exit 2 "bare red fallback blocked" "git commit -m x" "$red"
assert_exit 0 "single green commit allowed" "git -C $green commit -m x"
assert_exit 0 "single gateless commit allowed" "git -C $gateless commit -m x"

assert_exit 2 "red then gateless compound blocked" \
  "git -C $red commit -m x; git -C $gateless commit -m y"
assert_exit 2 "gateless then red compound blocked" \
  "git -C $gateless commit -m y; git -C $red commit -m x"
assert_exit 0 "green then gateless compound allowed" \
  "git -C $green commit -m x; git -C $gateless commit -m y"

assert_exit 2 "env wrapper red commit blocked" "env FOO=1 git -C $red commit -m x"
assert_exit 2 "env -- red commit blocked" "env -- git -C $red commit -m x"
assert_exit 2 "command wrapper red commit blocked" "command git -C $red commit -m x"
assert_exit 2 "command -p red commit blocked" "command -p git -C $red commit -m x"
assert_exit 2 "assignment-prefixed red commit blocked" "FOO=1 git -C $red commit -m x"

assert_exit 0 "printf prose does not trigger" "printf '%s\n' 'git commit -m nope'"
assert_exit 0 "heredoc prose does not trigger" "cat <<EOF
git commit -m nope
EOF"
assert_exit 0 "git log grep commit is not a commit" "git log --grep commit"
assert_exit 0 "git help commit is not a commit" "git help commit"
assert_exit 2 "make -C does not poison later cd commit" \
  "make -C $gateless; cd $red; git commit -m x"
assert_exit 2 "subshell cd does not leak to later bare commit" \
  "(cd $gateless && git commit -m x); git commit -m y" "$red"
assert_exit 2 "--git-dir target resolves .git parent" \
  "git --git-dir=$red/.git commit -m x"
assert_exit 2 "--work-tree target resolves work tree" \
  "git --work-tree=$red commit -m x"
assert_exit 0 "alias-shaped command is not structurally knowable" "gc -m x" "$red"

echo "gate-before-commit tests passed"
