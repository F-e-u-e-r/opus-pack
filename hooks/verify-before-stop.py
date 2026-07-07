#!/usr/bin/env python3
"""Claude Code Stop hook: block ending the turn when code files were edited
but no test/verification command ran and no verification-intent subagent was
dispatched. Mechanically enforces operational-rigor §4 (verify by execution)
and §5 (independent verification for load-bearing work).

Adapted from `verify_gate.py` in curtischoutw/claude-institution @ 8dea062
(MIT License, Copyright (c) 2026 Curtis Chou), itself adapted from
Miguok/fable-harness. Detection logic preserved; messages rewritten to point
at this pack's rules. Python 3.8+, stdlib only.

Behavior:
- Only triggers when code-extension files were edited this turn AND no test
  command / verification-intent agent appeared. Doc/config edits never block.
- A dispatched subagent whose prompt shows verification intent counts as
  verification — the hook must not punish the pack's own delegate-the-check rule.
- Test commands match at command position (start of line or after ;|&|(),
  so `cat pytest.ini` does not count as running tests.
- stop_hook_active (the second Stop) always passes — relief valve so a
  blocked turn cannot deadlock; the pass is logged for audit.
- Fail-open: any internal error passes, with the traceback logged.

Known limits (mechanically unfixable; do not treat this hook as omniscient):
- It checks that a test command / verify agent APPEARED, not that tests
  passed or the verification was honest.
- Double-Stop escape: after a block, replying anything and stopping again
  passes (the relief valve). The audit log is the only compensation.
- The window covers only tool calls after the last real user prompt.
- Env-var-prefixed commands (FOO=1 pytest) are not matched.
"""

import datetime
import json
import os
import re
import sys
import traceback

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
AGENT_TOOLS = {"Task", "Agent"}

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".java", ".rb", ".php", ".c", ".cpp", ".cc", ".h", ".hpp",
    ".cs", ".swift", ".kt", ".kts", ".scala", ".sh", ".bash", ".zsh",
    ".sql", ".lua", ".ex", ".exs", ".clj", ".cljs", ".hs", ".ml", ".mli",
    ".r", ".m", ".mm", ".vue", ".svelte", ".dart", ".jl",
    ".ipynb", ".tf", ".pl", ".pm", ".groovy",
}

TEST_CMD_RE = re.compile(
    r"(?:^|[\n;&|(]\s*)"  # command position: line start or after a separator
    r"(?:(?:time|npx|uv\s+run|poetry\s+run|pdm\s+run)\s+)?"
    r"("
    r"pytest|py\.test|python3?\s+-m\s+pytest|"
    r"npm\s+(?:run\s+)?test|yarn\s+test|pnpm\s+test|"
    r"jest|vitest|"
    r"go\s+test|cargo\s+test|"
    r"mvn\s+test|gradle\s+test|\.\/gradlew\s+test|"
    r"rspec|bundle\s+exec\s+rspec|"
    r"dotnet\s+test|swift\s+test|phpunit|ctest|mix\s+test|"
    r"bash\s+checks/run-all\.sh"
    r")\b",
    re.IGNORECASE,
)

VERIFY_INTENT_RE = re.compile(
    r"(驗證|實跑|跑.{0,6}測試|read-?back|第二意見|"
    r"verif(?:y|ication)|run\s+(?:the\s+)?tests?)",
    re.IGNORECASE,
)

LOG_PATH = os.path.expanduser("~/.claude/hooks/hooks.log")
LOCAL_COMMAND_MARKERS = ("<local-command-stdout>", "<command-name>", "<local-command-caveat>")

BLOCK_REASON = (
    "Code files were edited this turn (Edit/Write/NotebookEdit), but no test "
    "or verification command ran and no verification-intent subagent was "
    "dispatched. This hook only checks that verification APPEARED — not that "
    "it passed.\n"
    "Per operational-rigor §4: verify by execution, never by inspection; "
    "'the code looks right' is not verification.\n"
    "Pick one before finishing: run the relevant tests or gates "
    "(e.g. bash checks/run-all.sh) and show the output; dispatch a "
    "fresh-context verification subagent (delegation-and-review §3); or, if "
    "this change genuinely needs no test (e.g. config-only, verified another "
    "way), state that reason explicitly in the final report."
)


def _log(line):
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{ts} verify-before-stop: {line}\n")
    except Exception:
        pass


def load_transcript(path):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def is_real_user_prompt(entry):
    if entry.get("type") != "user":
        return False
    content = (entry.get("message") or {}).get("content")
    if not isinstance(content, str):
        return False
    return not any(marker in content for marker in LOCAL_COMMAND_MARKERS)


def analyze(entries):
    """Return (edited_code, verification_seen) for the last turn."""
    last_idx = None
    for i, entry in enumerate(entries):
        if is_real_user_prompt(entry):
            last_idx = i
    if last_idx is None:
        return False, False  # degenerate transcript — fail-open by design

    edited_code = False
    verification_seen = False
    for entry in entries[last_idx + 1:]:
        content = (entry.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            name = block.get("name")
            tool_input = block.get("input") or {}
            if name in EDIT_TOOLS:
                path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
                if any(path.endswith(ext) for ext in CODE_EXTENSIONS):
                    edited_code = True
            elif name == "Bash":
                if TEST_CMD_RE.search(tool_input.get("command") or ""):
                    verification_seen = True
            elif name in AGENT_TOOLS:
                text = " ".join(str(tool_input.get(k) or "") for k in ("prompt", "description"))
                if VERIFY_INTENT_RE.search(text):
                    verification_seen = True
    return edited_code, verification_seen


def main():
    """Always exits 0 (fail-open); a block is signaled via stdout JSON."""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}

        if data.get("stop_hook_active"):
            _log("PASS stop_hook_active (second Stop — relief valve, logged for audit)")
            return 0

        transcript_path = data.get("transcript_path")
        if not transcript_path:
            return 0

        edited_code, verification_seen = analyze(load_transcript(transcript_path))
        if edited_code and not verification_seen:
            _log("BLOCK code edited with no test command / verification agent")
            print(json.dumps({"decision": "block", "reason": BLOCK_REASON}))
        return 0
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
