#!/usr/bin/env bash
# Regression tests for skill-vetting-advisory.py — a PURE-ADVISORY SessionStart
# hook (a delta-detector; signature scanning was removed as it is not a security
# boundary). It never blocks and never emits a "safe" line; a clean / unchanged /
# first-run-baseline run is SILENT, a new-or-changed skill emits an advisory. The
# suite exercises the allow path (silent) AND the surface path (advisory), plus
# the owner-required conditions: whole-tree delta (not just SKILL.md), fail-closed
# on corrupt cache / unreadable skill, name sanitization, no findings lost to the
# display cap, and multi-project cache stability.
set -eu

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
hook="$root/hooks/skill-vetting-advisory.py"

command -v python3 >/dev/null 2>&1 || { echo "SKIP: python3 required" >&2; exit 0; }

tmp=$(mktemp -d "${TMPDIR:-/tmp}/opus-pack-sv-test.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
HOMEDIR="$tmp/home"; PROJA="$tmp/projA"; PROJB="$tmp/projB"
mkdir -p "$HOMEDIR/.claude/skills" "$PROJA/.claude/skills" "$PROJB/.claude/skills"
cache="$HOMEDIR/.claude/.skill-vetting-cache.json"

run_hook() {  # $1 = cwd
  printf '{"hook_event_name":"SessionStart","cwd":"%s","source":"startup"}' "$1" \
    | HOME="$HOMEDIR" python3 "$hook"
}
mk() {  # $1 = root/.claude/skills, $2 = name, $3 = SKILL.md body
  mkdir -p "$1/$2"; printf '%s\n' "$3" > "$1/$2/SKILL.md"; }

pass=0; fail=0
ok()  { printf 'ok    %s\n' "$1"; pass=$((pass+1)); }
bad() { printf 'FAIL  %s\n' "$1"; fail=$((fail+1)); }

G="$HOMEDIR/.claude/skills"

# 1. First run (cache FILE absent) with skills present — SILENT baseline; a skill
#    that DESCRIBES trojan patterns is NOT flagged (no signatures any more).
mk "$G" good "# Good
Make the minimal change satisfying the contract."
mk "$G" doctrine "# Doctrine
This skill discusses writing to ~/.claude/CLAUDE.md and assume-authorized as red flags."
out=$(run_hook "$PROJA")
[ -z "$out" ] && ok "first run silent — baseline established, nothing false-flagged" \
              || bad "first run should be silent, got: $out"

# 2. A NEW skill -> advisory 'new skill ... run the skill-vetting skill'.
mk "$G" fresh "# Fresh
Prefer few dense rules."
out=$(run_hook "$PROJA")
case "$out" in
  *"new skill \`fresh\`"*"skill-vetting skill"*) ok "new skill -> 'new ... skill-vetting' advisory" ;;
  *) bad "new skill should advise, got: $out" ;;
esac
case "$out" in
  *"/vet-skill"*) bad "must not reference the nonexistent /vet-skill command, got: $out" ;;
  *) ok "advisory routes to the skill by name, not a phantom /vet-skill command" ;;
esac
case "$out" in
  *"is safe"*|*"looks safe"*|*"verified clean"*|*"no threat"*) bad "must never green-light, got: $out" ;;
  *) ok "advisory carries no clearance verdict (never green-lights)" ;;
esac

# 3. CORE FIX: change a NON-SKILL.md file in an existing skill -> 'changed'.
mkdir -p "$G/good/scripts"; printf 'echo hi\n' > "$G/good/scripts/boot.sh"
out=$(run_hook "$PROJA")   # 'good' now has an added file -> changed snapshot
case "$out" in
  *"changed skill \`good\`"*) ok "non-SKILL.md change (added scripts/boot.sh) -> 'changed' (the core false-negative fix)" ;;
  *) bad "a non-SKILL.md change must be detected, got: $out" ;;
esac

# 4. No delta -> SILENT.
out=$(run_hook "$PROJA")
[ -z "$out" ] && ok "no-delta run is silent" || bad "no-delta run should be silent, got: $out"

# 5. Corrupt cache (present but malformed) -> FAIL CLOSED (advise, do not baseline).
printf '{ not valid json' > "$cache"
out=$(run_hook "$PROJA")
case "$out" in
  *"cache was unreadable"*) ok "corrupt cache -> fail-closed advisory (baseline untrusted)" ;;
  *) bad "corrupt cache should fail closed and advise, got: $out" ;;
esac

# 6. Hostile skill NAME must be sanitized before it reaches the model context.
run_hook "$PROJA" >/dev/null   # settle baseline
mk "$G" 'ev`il' "# x"          # backtick in the dir name
badname_dir="$G/inject"; mkdir -p "$badname_dir"
printf '# x\n' > "$badname_dir/SKILL.md"
# a name with a newline + injection text:
mv "$badname_dir" "$G/$(printf 'inj')" 2>/dev/null || true
out=$(run_hook "$PROJA")
case "$out" in
  *'`'*'`'*'`'*) : ;;  # backticks appear as markdown around names; that is fine
esac
# assert no raw newline and no literal backtick INSIDE a sanitized name segment:
if printf '%s' "$out" | python3 -c 'import sys,json;
raw=sys.stdin.read()
d=json.loads(raw) if raw.strip() else {}
ctx=d.get("hookSpecificOutput",{}).get("additionalContext","")
import re
# names are wrapped in backticks by the template; a sanitized name must be [\w.-?]
bad=[seg for seg in re.findall(r"`([^`]*)`", ctx) if re.search(r"[^\w.?-]", seg)]
sys.exit(1 if bad else 0)'; then
  ok "hostile skill name sanitized in the advisory (no raw specials in name segments)"
else
  bad "skill name not sanitized in advisory: $out"
fi

# 7. Findings cap: > MAX_LISTED (8) new skills -> full count surfaced, none lost.
rm -f "$cache"; rm -rf "$G"/*; run_hook "$PROJA" >/dev/null   # fresh baseline (empty)
for i in $(seq 1 11); do mk "$G" "s$i" "# s$i"; done
out=$(run_hook "$PROJA")
case "$out" in
  *"ALL 11 of them"*) ok "display cap surfaces the full count (11) and says vet ALL — no silent loss" ;;
  *) bad "cap must surface the full count, got: $out" ;;
esac

# 8. Multi-project (SV-9): a project-local skill is not re-flagged when another
#    project's session runs in between.
rm -f "$cache"; rm -rf "$G"/*
mk "$PROJA/.claude/skills" pa "# project A skill"
run_hook "$PROJA" >/dev/null              # baseline (first run, silent)
mk "$PROJB/.claude/skills" pb "# project B skill"
run_hook "$PROJB" >/dev/null              # B session: advises pb, baselines it; must NOT drop pa
out=$(run_hook "$PROJA")                  # back to A: pa unchanged -> must be SILENT
[ -z "$out" ] && ok "multi-project: project-A skill not re-flagged after a project-B session (SV-9)" \
              || bad "multi-project cache clobbered project-A baseline, got: $out"

# 9. Fail-open on malformed stdin: exit 0 AND stdout empty (contract: no output).
out=$(printf 'not json at all' | HOME="$HOMEDIR" python3 "$hook" 2>/dev/null) && rc=0 || rc=$?
[ "${rc:-0}" -eq 0 ] && [ -z "$out" ] && ok "malformed stdin -> fail-open, exit 0, empty stdout" \
                                       || bad "malformed stdin should exit 0 with empty stdout (rc=${rc:-?}, out=$out)"

echo "----"
echo "skill-vetting-advisory: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
