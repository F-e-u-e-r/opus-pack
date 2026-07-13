#!/usr/bin/env bash
# Regression tests for gate-credential-destruction.py — both the allow path
# and the block path, per operational-rigor §2's install gate.
set -eu

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

command -v python3 >/dev/null 2>&1 || {
  echo "SKIP: python3 is required by gate-credential-destruction.py" >&2
  exit 0
}

tmp=$(mktemp -d "${TMPDIR:-/tmp}/opus-pack-credgate-test.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

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

  set +e
  out=$(json_for "$command_text" | HOME="$tmp" python3 "$root/hooks/gate-credential-destruction.py" 2>&1)
  code=$?
  set -e

  if [ "$code" -ne "$expected" ]; then
    echo "FAIL $name: expected exit $expected, got $code" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  echo "PASS $name"
}

# Feed RAW stdin straight to the hook (bypasses json_for) — for malformed
# envelopes and non-JSON input that exercise the degraded-scan / fail path.
assert_exit_raw() {
  expected="$1"
  name="$2"
  raw_stdin="$3"

  set +e
  out=$(printf '%s' "$raw_stdin" | HOME="$tmp" python3 "$root/hooks/gate-credential-destruction.py" 2>&1)
  code=$?
  set -e

  if [ "$code" -ne "$expected" ]; then
    echo "FAIL $name: expected exit $expected, got $code" >&2
    printf '%s\n' "$out" >&2
    exit 1
  fi
  echo "PASS $name"
}

# --- allow path ---
assert_exit 0 "benign rm"                    'rm build/cache.txt'
assert_exit 0 "read-only on credential file" 'ls -la tmp/credentials.bak'
assert_exit 0 "cat env is not destructive"   'cat .env'
assert_exit 0 "env example is exempt"        'rm .env.example'
assert_exit 0 "public key is exempt"         'rm ~/.ssh/id_rsa.pub'
assert_exit 0 "verb in argument position"    'echo "never run: rm credentials.bak"'
assert_exit 0 "git rm non-credential"        'git rm old_module.py'
assert_exit 0 "approved override passes"     'CRED_GATE_APPROVED=1 rm tmp/credentials.bak'
assert_exit 0 "wrapper + non-destructive"    'sudo ls ~/.ssh'
assert_exit 0 "empty input"                  ''

# --- block path ---
assert_exit 2 "rm credentials backup"        'rm tmp/credentials.bak'
assert_exit 2 "rm -f ssh private key"        'rm -f ~/.ssh/id_rsa'
assert_exit 2 "shred a pem"                  'shred -u server.pem'
assert_exit 2 "git rm secrets file"          'git rm config/secrets.yaml'
assert_exit 2 "git -C repo rm secrets"       'git -C backend rm config/secrets.yaml'
assert_exit 2 "second command after ;"       'rm notes.txt; rm .env'
assert_exit 2 "rm under .aws dir"            'rm -rf ~/.aws/credentials'
assert_exit 2 "unlink a keystore"            'unlink app/release.jks'
assert_exit 2 "env prod variant blocked"     'rm .env.production'
assert_exit 2 "unparseable + suspicious"     'rm "tmp/credentials.bak'

# --- adversarial-review regressions (grok 4.5 findings F1-F7, all
# --- reproduced before fixing; these pin the fixes) ---
assert_exit 2 "override after destructive op does not launder (F1)" \
  'rm tmp/credentials.bak; CRED_GATE_APPROVED=1 true'
assert_exit 2 "override scopes to its own command only (F2)" \
  'CRED_GATE_APPROVED=1 true; rm tmp/credentials.bak'
assert_exit 0 "override + later benign command still passes" \
  'CRED_GATE_APPROVED=1 rm tmp/credentials.bak; ls'
assert_exit 2 "env safe-suffix is exact, not endswith (F3)" \
  'rm .env.notexample'
assert_exit 2 "credential directory itself (F4)"        'rm -rf ~/.ssh'
assert_exit 2 "aws directory itself (F4)"               'rm -rf ~/.aws'
assert_exit 2 "sudo wrapper (F5)"                       'sudo rm tmp/credentials.bak'
assert_exit 2 "path-qualified verb (F5)"                '/bin/rm .env'
assert_exit 2 "command builtin wrapper (F5)"            'command rm ~/.ssh/id_rsa'
assert_exit 2 "busybox wrapper (F5)"                    'busybox rm .env'
assert_exit 2 "uppercase verb (F6)"                     'RM .env'
assert_exit 2 "unparseable + id_dsa (F7)"               'rm "id_dsa'
assert_exit 2 "exec wrapper"                            'exec rm .env'
assert_exit 2 "override does not extend across &&"      'CRED_GATE_APPROVED=1 rm .env && rm id_rsa'

# --- second-reviewer regressions (gpt-5.5 findings, reproduced before fixing) ---
assert_exit 2 "secret.pub is not an ssh pubkey (G1)"    'rm secret.pub'
assert_exit 2 "credentials.pub under .aws (G1)"         'rm ~/.aws/credentials.pub'
assert_exit 0 "ssh public key stays exempt (G1)"        'rm ~/.ssh/id_rsa.pub'
assert_exit 2 "if-then control syntax (G2)"             'if rm .env; then echo ok; fi'
assert_exit 2 "brace group (G2)"                        '{ rm .env; }'
assert_exit 2 "negation (G2)"                           '! rm .env'
assert_exit 2 "for-do loop (G2)"                        'for x in 1; do rm .env; done'
assert_exit 2 "double-dash filename (G3)"               'rm -- -secret.key'
assert_exit 0 "double-dash benign filename"             'rm -- notes.txt'

# --- malformed envelope / internal-error degraded scan (raw stdin) ---
# the pre-fix hook returned 0 (fail-open) on these; the degraded raw-scan blocks
# a clearly-destructive one while still allowing a benign / unreadable one.
assert_exit_raw 2 "malformed JSON, destructive payload" '{"tool_input": {"command": "rm ~/.ssh/id_rsa"'
assert_exit_raw 0 "malformed JSON, benign payload"      '{"tool_input": {"command": "ls -la build"'
assert_exit_raw 2 "non-JSON stdin but destructive text" 'oops rm ~/.aws/credentials oops'
assert_exit_raw 0 "unrelated field mentions rm (command-scoped)" \
  '{"tool_input": {"command": "echo ok"}, "description": "rm ~/.ssh/id_rsa"}'
assert_exit_raw 2 "command is a non-string (JSON array) -> raw scan" \
  '{"tool_input": {"command": ["rm ~/.ssh/id_rsa"]}}'
assert_exit_raw 0 "command is a benign non-string" \
  '{"tool_input": {"command": ["ls", "-la"]}}'

# oversized envelope: a destructive command hidden past the 1 MiB read cap must
# block, not scan a truncated benign prefix and allow.
set +e
python3 -c "import sys; sys.stdout.write('{\"tool_input\": {\"command\": \"echo ' + 'x'*1100000 + '; rm .env\"}}')" \
  | HOME="$tmp" python3 "$root/hooks/gate-credential-destruction.py" >/dev/null 2>&1
oversize_code=$?
set -e
[ "$oversize_code" -eq 2 ] && echo "PASS oversized envelope blocks" \
  || { echo "FAIL oversized envelope: expected 2, got $oversize_code" >&2; exit 1; }

echo "OK: all gate-credential-destruction tests passed"
