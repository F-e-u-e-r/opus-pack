#!/usr/bin/env python3
"""Claude Code SessionStart hook: a PURE-ADVISORY tripwire for unvetted or
changed third-party skills. Companion to the `skill-vetting` skill; enforces
nothing. THIN BY DESIGN: every filesystem observation and every baseline
read/write lives in the sibling module `hooks/skill_snapshot.py` (install both
files together, same directory); this file only resolves the watch roots,
compares snapshots to the baseline, composes the advisory, and orders delivery
before baseline advance. Design record:
`reviews/2026-07-25-skill-vetting-snapshot-threat-model.md`.

Signature scanning is not a security boundary and has been removed. The hook
detects complete skill-tree changes and requires full skill vetting against the
exact content snapshot before trust or reuse of a cached verdict. It does not
attempt to decide whether a skill is malicious — a regex over skill text has low
recall on fluent-prose / cross-file / split / indirect payloads and would only
create false assurance (and, by echoing skill text, an injection surface). The
real defense is the `skill-vetting` skill: a full, human-grade read. This hook
only routes to it.

What fires an advisory (each covers EVERY file in the tree, not just SKILL.md):
a new, changed, or removed top-level entry under a watched skills root; any
observation anomaly — an unreadable file or directory, an oversize file, a
budget breach, ANY symlink, a special file (FIFO/socket/device), a hostile or
undecodable name (shown only as an opaque id); an unreadable/corrupt/stale
baseline. An anomalous tree can never be certified unchanged, so it re-advises
EVERY session until the anomaly is resolved — deliberate for a tree that cannot
be fully observed. A clean, unchanged, or (documented limit) first-run
bootstrap is SILENT; the hook NEVER blocks and NEVER emits a "safe" line.

Watched roots: `$CLAUDE_CONFIG_DIR/skills` (default `~/.claude/skills`) and
`$CLAUDE_PROJECT_DIR/.claude/skills` (falling back to the hook payload's `cwd`,
then the process cwd). Baseline: `<config>/skill-vetting/baseline.json`,
schema- and policy-versioned; a version change resets it VISIBLY.

Ordering guarantee: the advisory is printed FIRST and the baseline advances
only after that print succeeds — a failed delivery (or a refused/failed
baseline write) leaves the old baseline, so the same deltas re-advise next
session. Fail directions (both hold, they are not in tension):
- Robustness = the hook never breaks session start: it always exits 0, and an
  unexpected internal error emits a LABELLED degraded advisory ("changes may
  be unobserved") when nothing was printed yet — degraded visibly, not silent.
- Detection = FAIL CLOSED: whatever cannot be fully observed advises; nothing
  is silently baselined as clean.

Known limits (documented, not hidden):
- The baseline is NOT tamper-evident: it, the skills, and this hook share one
  trust level, and same-privilege local code can rewrite any of them. The
  advisory posture is a tripwire against upstream/content changes, not a
  defense against code already running as you.
- First run (no baseline file) bootstraps SILENTLY — a skill already present
  at install time is baselined, not flagged. Run the `skill-vetting` skill on
  anything present but not yet reviewed; `skill_snapshot.py status` lists
  entries never recorded as vetted.
- A delivered advisory is not re-raised once baselined (advisory posture): the
  skill's §3 verdict binding, not this hook, carries the re-vet duty. The
  baseline records per-skill status (baseline/seen/vetted; `record` flips to
  vetted) for on-demand audit.
- SessionStart only: a skill installed after the scan is seen next session,
  and plugin-managed skills (e.g. under a plugin cache) are outside the
  watched roots — vet those manually.

Ships UNREGISTERED (per-user opt-in; the plugin registers no hooks by design) —
see the README hooks section for manual wiring. Python 3.8+, stdlib only. The
demoted signature patterns are NOT here by design: they live privately as
regression fixtures for the skill-vetting skill, never as a runtime detector.
"""

import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
try:
    import skill_snapshot as snapmod
    _IMPORT_ERROR = None
except Exception:
    snapmod = None
    _IMPORT_ERROR = traceback.format_exc()

MAX_LISTED = 8        # display cap only; the full count is always surfaced
MAX_CANDIDATES = 256  # top-level entries scanned per root; more is a root anomaly

_PREFIX = ("skill-vetting advisory (tripwire only, NOT a safety verdict — the "
           "skill-vetting skill's full read is the actual check): ")


def _log(msg):
    """Best-effort audit line; never raises (preserves robustness fail-open)."""
    try:
        cfg = snapmod.config_root() if snapmod else os.path.join(
            os.path.expanduser("~"), ".claude")
        path = os.path.join(cfg, "skill-vetting", "advisory.log")
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        with open(path, "a") as fh:
            fh.write(msg + "\n")
    except Exception:
        pass


def _emit(lines):
    """Print the advisory JSON. True only if the whole write succeeded — the
    caller advances the baseline only on True (delivery before advance). Writes
    the raw fd, not sys.stdout: a broken pipe then fails HERE, atomically with
    the delivery decision, instead of lingering in a buffer whose exit-time
    flush would flip the interpreter's exit code."""
    payload = (json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": _PREFIX + " | ".join(lines)}},
        ensure_ascii=True) + "\n").encode("utf-8")
    try:
        off = 0
        while off < len(payload):
            off += os.write(1, payload[off:])
        return True
    except Exception:
        return False


def _resolve_project_root(payload):
    env = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if env and os.path.isabs(env):
        return env
    cwd = payload.get("cwd") if isinstance(payload, dict) else None
    if isinstance(cwd, str) and os.path.isabs(cwd):
        return cwd
    return os.getcwd()


def _scan_root(scope, label, root):
    """Enumerate one skills root. Returns (candidates, root_lines, complete):
    candidates = [(key, name_bytes, display, snap)]; complete=False means the
    enumeration itself failed or was truncated (baseline pruning for this
    scope must then be skipped — a removal cannot be distinguished from
    not-scanned)."""
    rootb = os.fsencode(root)
    try:
        with os.scandir(rootb) as it:
            dirents = sorted(it, key=lambda d: d.name)
    except FileNotFoundError:
        return [], [], True          # no such root: a complete, empty view
    except NotADirectoryError:
        return [], ["the %s skills path is not a directory — treat its skills "
                    "as changed; run the skill-vetting skill before trusting "
                    "them" % label], False
    except OSError:
        return [], ["the %s skills directory could not be read — treat its "
                    "skills as changed; run the skill-vetting skill before "
                    "trusting them" % label], False
    lines = []
    complete = True
    if len(dirents) > MAX_CANDIDATES:
        lines.append("the %s skills directory holds %d entries (limit %d) — "
                     "entries beyond the limit were NOT scanned; run the "
                     "skill-vetting skill on them manually"
                     % (label, len(dirents), MAX_CANDIDATES))
        dirents = dirents[:MAX_CANDIDATES]
        complete = False
    out = []
    for de in dirents:
        name = de.name
        disp, _ = snapmod.display_name(name)
        key = "%s|%s" % (scope, snapmod.name_key(name))
        out.append((key, name, "%s:%s" % (label, disp),
                    snapmod.snapshot_tree(de.path)))
    return out, lines, complete


def main():
    printed = False
    try:
        if snapmod is None:
            raise RuntimeError("companion module hooks/skill_snapshot.py "
                               "missing or unloadable (install both files "
                               "together): " + str(_IMPORT_ERROR))
        try:
            raw = sys.stdin.read()
            payload = json.loads(raw) if raw.strip() else {}
        except Exception:
            payload = {}

        cfg = snapmod.config_root()
        proj = os.path.realpath(_resolve_project_root(payload))
        roots = [("global", "global", os.path.join(cfg, "skills"))]
        proj_skills = os.path.join(proj, ".claude", "skills")
        if os.path.realpath(proj_skills) != os.path.realpath(roots[0][2]):
            roots.append((snapmod.scope_id(os.fsencode(proj)), "project",
                          proj_skills))

        bpath = snapmod.baseline_path(cfg)
        state, data = snapmod.load_baseline(bpath)
        old_entries = data["entries"] if state == "ok" else {}

        head_lines = []
        if state == "corrupt":
            head_lines.append(
                "the vetting baseline was unreadable and has been rebuilt — "
                "prior baselines are untrusted; re-vet currently installed "
                "skills with the skill-vetting skill")
        elif state == "stale":
            head_lines.append(
                "the vetting baseline predates the current snapshot "
                "schema/policy (now v%d/v%d) — baselines reset; re-vet "
                "currently installed skills with the skill-vetting skill"
                % (snapmod.SCHEMA_VERSION, snapmod.POLICY_VERSION))

        anomaly_lines, new_lines, changed_lines, removed_lines = [], [], [], []
        new_entries = {}
        scanned_scopes = {}   # scope -> enumeration complete?
        for scope, label, root in roots:
            candidates, root_lines, complete = _scan_root(scope, label, root)
            head_lines.extend(root_lines)
            prev = scanned_scopes.get(scope, True)
            scanned_scopes[scope] = prev and complete
            for key, _name, disp, snap in candidates:
                old = old_entries.get(key)
                is_new = old is None
                is_changed = (old is not None) and old["digest"] != snap["digest"]
                if state == "absent":
                    status = "baseline"          # first-run bootstrap: silent
                elif state != "ok":
                    status = "seen"              # advised untrusted collectively
                elif is_new or is_changed:
                    status = "seen"
                else:
                    status = old["status"]       # unchanged: keep status+verdict
                entry = {"digest": snap["digest"], "status": status,
                         "name": disp.split(":", 1)[1], "scope": scope}
                if status == "vetted" and old and "verdict" in old:
                    entry["verdict"] = old["verdict"]
                new_entries[key] = entry
                if snap["anomalies"]:
                    reasons = ",".join(sorted({r for r, _ in snap["anomalies"]}))
                    kind = "new " if (state == "ok" and is_new) else (
                        "changed " if (state == "ok" and is_changed) else "")
                    anomaly_lines.append(
                        "%sskill %s cannot be certified unchanged (%s) — run "
                        "the skill-vetting skill on it before trusting it"
                        % (kind, disp, reasons))
                elif state == "ok" and is_new:
                    new_lines.append(
                        "new skill %s — run the skill-vetting skill on it "
                        "before trusting it or reusing a prior verdict" % disp)
                elif state == "ok" and is_changed:
                    changed_lines.append(
                        "changed skill %s — run the skill-vetting skill on it "
                        "before trusting it or reusing a prior verdict" % disp)

        if state == "ok":
            for key, old in old_entries.items():
                scope = old["scope"]
                if scope in scanned_scopes and key not in new_entries:
                    if scanned_scopes[scope]:
                        removed_lines.append(
                            "skill %s was removed — baseline entry pruned"
                            % old["name"])
                    else:
                        new_entries[key] = old   # incomplete enumeration: keep
                elif scope not in scanned_scopes:
                    new_entries[key] = old       # other project: preserve

        lines = (head_lines + anomaly_lines + new_lines + changed_lines
                 + removed_lines)
        if lines:
            shown = lines[:MAX_LISTED]
            if len(lines) > len(shown):
                shown.append("...and %d more item(s) not shown — %d total; run "
                             "the skill-vetting skill on ALL of them"
                             % (len(lines) - len(shown), len(lines)))
            if not _emit(shown):
                _log("WARN advisory delivery failed — baseline NOT advanced "
                     "(will re-advise)")
                return 0
            printed = True
            _log("ADVISED %d item(s)" % len(lines))

        merged = snapmod.fresh_baseline()
        merged["entries"] = new_entries
        if state != "ok" or merged["entries"] != data["entries"]:
            ok, reason = snapmod.store_baseline(merged, bpath)
            if not ok:
                _log("WARN baseline write refused/failed (%s) — deltas will "
                     "re-advise next run" % reason)
        return 0
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        if not printed:
            _emit(["the skill-vetting advisory hook could not complete "
                   "(internal error) — skill changes may be UNOBSERVED this "
                   "session; run the skill-vetting skill manually on anything "
                   "new or changed"])
        return 0


if __name__ == "__main__":
    sys.exit(main())
