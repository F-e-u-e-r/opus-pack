#!/usr/bin/env bash
# Regression tests for verify-before-stop.py — the hook always exits 0;
# a block is signaled by {"decision": "block"} on stdout. Tests cover both
# the allow path and the block path, per operational-rigor §2's install gate.
set -eu

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

command -v python3 >/dev/null 2>&1 || {
  echo "SKIP: python3 is required by verify-before-stop.py" >&2
  exit 0
}

tmp=$(mktemp -d "${TMPDIR:-/tmp}/opus-pack-vbs-test.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# Build a transcript JSONL: a real user prompt, then tool_use blocks.
transcript_with() {
  # $1 = output path; remaining args = tool_use JSON blocks (already JSON)
  out="$1"; shift
  {
    printf '%s\n' '{"type":"user","message":{"content":"please do the task"}}'
    for block in "$@"; do
      printf '{"type":"assistant","message":{"content":[%s]}}\n' "$block"
    done
  } > "$out"
}

EDIT_PY='{"type":"tool_use","name":"Edit","input":{"file_path":"/work/app.py"}}'
EDIT_MD='{"type":"tool_use","name":"Edit","input":{"file_path":"/work/README.md"}}'
BASH_PYTEST='{"type":"tool_use","name":"Bash","input":{"command":"pytest -q"}}'
BASH_CAT_PYTEST_INI='{"type":"tool_use","name":"Bash","input":{"command":"cat pytest.ini"}}'
AGENT_VERIFY='{"type":"tool_use","name":"Task","input":{"prompt":"verify the fix: run the tests and report"}}'

run_hook() {
  # $1 = transcript path; $2 = stop_hook_active (true/false)
  TRANSCRIPT="$1" ACTIVE="$2" python3 - <<'PY' | HOME="$tmp" python3 "$root/hooks/verify-before-stop.py"
import json
import os

print(json.dumps({
    "transcript_path": os.environ["TRANSCRIPT"],
    "stop_hook_active": os.environ["ACTIVE"] == "true",
}))
PY
}

assert_block() {
  name="$1"; out="$2"
  # the whole stdout must be one valid JSON object with decision == "block"
  if printf '%s' "$out" | python3 -c '
import json, sys
d = json.load(sys.stdin)
sys.exit(0 if d.get("decision") == "block" and d.get("reason") else 1)
' 2>/dev/null; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected a valid block JSON, got: $out" >&2
    exit 1
  fi
}

assert_pass() {
  name="$1"; out="$2"
  if [ -z "$out" ]; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected pass-through (empty stdout), got: $out" >&2
    exit 1
  fi
}

# --- block path: code edited, no verification ---
transcript_with "$tmp/t1.jsonl" "$EDIT_PY"
assert_block "code edit without verification blocks" "$(run_hook "$tmp/t1.jsonl" false)"

# cat pytest.ini is not running tests (command-position match)
transcript_with "$tmp/t2.jsonl" "$EDIT_PY" "$BASH_CAT_PYTEST_INI"
assert_block "cat pytest.ini does not count as tests" "$(run_hook "$tmp/t2.jsonl" false)"

# --- allow path ---
transcript_with "$tmp/t3.jsonl" "$EDIT_PY" "$BASH_PYTEST"
assert_pass "code edit + pytest passes" "$(run_hook "$tmp/t3.jsonl" false)"

transcript_with "$tmp/t4.jsonl" "$EDIT_PY" "$AGENT_VERIFY"
assert_pass "code edit + verification-intent agent passes" "$(run_hook "$tmp/t4.jsonl" false)"

transcript_with "$tmp/t5.jsonl" "$EDIT_MD"
assert_pass "doc-only edit never blocks" "$(run_hook "$tmp/t5.jsonl" false)"

transcript_with "$tmp/t6.jsonl" "$EDIT_PY"
assert_pass "second Stop (relief valve) passes" "$(run_hook "$tmp/t6.jsonl" true)"

# Write counts as a code edit too (hook covers Edit/Write/NotebookEdit/MultiEdit)
WRITE_PY='{"type":"tool_use","name":"Write","input":{"file_path":"/work/new_module.py"}}'
transcript_with "$tmp/t7.jsonl" "$WRITE_PY"
assert_block "Write without verification blocks" "$(run_hook "$tmp/t7.jsonl" false)"

# Windowing: only tool calls after the LAST real user prompt count
{
  printf '%s\n' '{"type":"user","message":{"content":"first request"}}'
  printf '{"type":"assistant","message":{"content":[%s]}}\n' "$EDIT_PY"
  printf '%s\n' '{"type":"user","message":{"content":"second request, no edits after this"}}'
} > "$tmp/t8.jsonl"
assert_pass "edits before the last user prompt are out of window" "$(run_hook "$tmp/t8.jsonl" false)"

echo "OK: all verify-before-stop tests passed"
