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

# --- allow path ---
assert_exit 0 "benign rm"                    'rm build/cache.txt'
assert_exit 0 "read-only on credential file" 'ls -la tmp/credentials.bak'
assert_exit 0 "cat env is not destructive"   'cat .env'
assert_exit 0 "env example is exempt"        'rm .env.example'
assert_exit 0 "public key is exempt"         'rm ~/.ssh/id_rsa.pub'
assert_exit 0 "verb in argument position"    'echo "never run: rm credentials.bak"'
assert_exit 0 "git rm non-credential"        'git rm old_module.py'
assert_exit 0 "approved override passes"     'CRED_GATE_APPROVED=1 rm tmp/credentials.bak'
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

echo "OK: all gate-credential-destruction tests passed"
