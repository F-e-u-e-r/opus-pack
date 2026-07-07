#!/usr/bin/env bash
# Claude Code PreToolUse hook (matcher: Bash).
# Blocks `git commit` while the repo's ground-truth gates are red.
# Uses jq when available to parse the tool call JSON from stdin.
# Exit 0 = allow the tool call. Exit 2 = block it (stderr is fed back to the model).
# BLOCK/anomaly events append to ~/.claude/hooks/hooks.log for human audit.
set -u

log() {
  # Best-effort audit trail; logging failure must never affect the gate itself.
  { mkdir -p "$HOME/.claude/hooks" &&
    printf '%s gate-before-commit: %s\n' "$(date +%Y-%m-%dT%H:%M:%S)" "$1" \
      >> "$HOME/.claude/hooks/hooks.log"; } 2>/dev/null || true
}

gates="${CLAUDE_PROJECT_DIR:-.}/checks/run-all.sh"
[ -f "$gates" ] || exit 0 # repo has no gates — nothing to enforce

input=$(cat)

raw_looks_like_commit() {
  case "$input" in
    *git*commit*) return 0 ;;
    *) return 1 ;;
  esac
}

if command -v jq >/dev/null 2>&1; then
  if ! cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null); then
    if raw_looks_like_commit; then
      log 'BLOCK jq parse failed on a likely git commit'
      echo 'gate-before-commit hook: could not parse hook JSON for a likely git commit — blocking until fixed' >&2
      exit 2
    fi
    exit 0
  fi
else
  if raw_looks_like_commit; then
    log 'BLOCK jq missing on a likely git commit'
    echo 'gate-before-commit hook: jq is not installed — blocking likely git commit until jq is installed or the hook is removed' >&2
    exit 2
  fi
  exit 0
fi

# Heuristic match; a false positive merely runs the gates, which is the safe direction.
case "$cmd" in
  *git*commit*) ;;
  *) exit 0 ;;
esac

if out=$(bash "$gates" 2>&1); then
  exit 0
fi
log 'BLOCK gates red on git commit'
{
  echo 'GATES RED — commit blocked by PreToolUse hook. Fix the gates, then retry:'
  printf '%s\n' "$out" | tail -n 20
} >&2
exit 2
