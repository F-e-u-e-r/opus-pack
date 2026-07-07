#!/usr/bin/env bash
# Claude Code PreToolUse hook (matcher: Bash).
# Blocks `git commit` while any TARGET repo's ground-truth gates are red.
# Uses jq when available to parse the tool call JSON from stdin, and python3
# to safely tokenize the shell command (quotes, heredocs, operators) so commit
# detection and target-repo resolution work on command STRUCTURE, not raw
# text. Exit 0 = allow the tool call. Exit 2 = block it (stderr fed back to
# the model). BLOCK/anomaly events append to ~/.claude/hooks/hooks.log.
#
# Design points (each fixes a real misfire found in production use, plus a
# second round found by an adversarial review — see hooks.log history):
# 1. The gates that run are the ones in every repo a commit TARGETS — each
#    target is resolved from `git -C <dir>` on that git invocation, else the
#    most recent preceding `cd <dir>` — not the session's $CLAUDE_PROJECT_DIR
#    (which is only the fallback for a bare commit with no directory hints). A
#    `-C` on some OTHER command (`make -C`, `tar -C`) must not be mistaken for
#    git's.
# 2. Commit DETECTION and directory extraction run on a real shell tokenizer
#    (Python's shlex, no code execution — command substitutions and variables
#    are left as inert literal text), not sed/grep substring matching. This is
#    what makes quoted commit messages, printf/heredoc payloads, apostrophes,
#    escaped quotes, and single- vs double-quoted directory args all behave
#    correctly instead of relying on hand-rolled quote-stripping regexes that
#    can mis-pair on apostrophes or drop everything after a heredoc marker.
# 3. Gates run with cwd set to the target repo root, so a checks/run-all.sh
#    that uses relative paths evaluates against the right repo.
# 4. `git log --grep commit` / `git help commit` are not commits — only the
#    token immediately after git's global options (skipping recognized
#    value-taking flags) counts as the subcommand.
# A command Python can't tokenize (unbalanced quoting) is treated as "can't
# tell" and fails toward blocking a likely commit, same posture as jq/python3
# being absent. False positives that survive all this just run the gates
# (safe direction); a commit hidden inside `bash script.sh` or behind a shell
# alias (e.g. `gc`) bypasses the hook entirely — inherent to any
# text/structure-level hook, out of scope.
set -u

log() {
  # Best-effort audit trail; logging failure must never affect the gate itself.
  { mkdir -p "$HOME/.claude/hooks" &&
    printf '%s gate-before-commit: %s\n' "$(date +%Y-%m-%dT%H:%M:%S)" "$1" \
      >> "$HOME/.claude/hooks/hooks.log"; } 2>/dev/null || true
}

fallback_dir="${CLAUDE_PROJECT_DIR:-.}"
fallback_has_gates() { [ -f "$fallback_dir/checks/run-all.sh" ]; }

input=$(cat)

raw_looks_like_commit() {
  case "$input" in
    *git*commit*) return 0 ;;
    *) return 1 ;;
  esac
}

# Fail-closed paths: without a parsable command we can't resolve a target repo
# or check its structure, so these fall back to a raw text guess against the
# session project dir — the same degraded posture on every "can't tell" exit.
block_fallback_guess() {
  if fallback_has_gates && raw_looks_like_commit; then
    log "BLOCK $1"
    echo "gate-before-commit hook: $2 — blocking a likely git commit until fixed" >&2
    exit 2
  fi
  exit 0
}

command -v jq >/dev/null 2>&1 ||
  block_fallback_guess 'jq missing on a likely git commit' \
    'jq is not installed'
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null) ||
  block_fallback_guess 'jq parse failed on a likely git commit' \
    'could not parse hook JSON'

command -v python3 >/dev/null 2>&1 ||
  block_fallback_guess 'python3 missing on a likely git commit' \
    'python3 is not installed — cannot safely parse the command'

hook_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
parsed=$(python3 "$hook_dir/parse-commit-command.py" "$cmd" 2>/dev/null) ||
  block_fallback_guess 'parser crashed on a likely git commit' \
    'the command parser failed'

verdict=$(printf '%s\n' "$parsed" | sed -n '1p')
target_lines=$(printf '%s\n' "$parsed" | sed -n '2,$p')

[ "$verdict" = "UNPARSEABLE" ] &&
  block_fallback_guess 'unparseable command on a likely git commit' \
    'could not safely parse this command (e.g. unbalanced quoting)'

[ "$verdict" = "COMMIT" ] || exit 0

[ -n "$target_lines" ] || target_lines='DIR:'

while IFS= read -r target_line; do
  case "$target_line" in
    DIR:*) dir="${target_line#DIR:}" ;;
    *) continue ;;
  esac

  [ -n "$dir" ] || dir="$fallback_dir"
  case "$dir" in "~") dir="$HOME" ;; "~/"*) dir="$HOME/${dir#\~/}" ;; esac
  [ -d "$dir" ] || dir="$fallback_dir"

  # The gate lives at the target repo's root; fall back to the dir itself.
  repo=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null) || repo="$dir"
  gates="$repo/checks/run-all.sh"
  [ -f "$gates" ] || continue # target repo has no gates — nothing to enforce

  if out=$(cd "$repo" && bash "$gates" 2>&1); then
    continue
  fi
  log "BLOCK gates red on git commit (repo: $repo)"
  {
    echo 'GATES RED — commit blocked by PreToolUse hook. Fix the gates, then retry:'
    printf '%s\n' "$out" | tail -n 20
  } >&2
  exit 2
done <<EOF
$target_lines
EOF

exit 0
