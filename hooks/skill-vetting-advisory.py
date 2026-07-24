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

_PREFIX = ("skill-vetting advisory (tripwire only, NOT a safety verdict — the "
           "skill-vetting skill's full read is the actual check): ")


def _log(msg):
    """Best-effort audit line; never raises AND never blocks. Opens the log
    O_NOFOLLOW|O_NONBLOCK|O_APPEND via a raw fd, so a planted symlink or a FIFO
    at the log path cannot redirect the write or hang SessionStart (a blocking
    open on a reader-less FIFO would otherwise wedge the whole session)."""
    try:
        cfg = snapmod.config_root() if snapmod else os.path.join(
            os.path.expanduser("~"), ".claude")
        d = os.path.join(cfg, "skill-vetting")
        os.makedirs(d, mode=0o700, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        if hasattr(os, "O_NONBLOCK"):
            flags |= os.O_NONBLOCK
        fd = os.open(os.path.join(d, "advisory.log"), flags, 0o600)
        try:
            os.write(fd, (msg + "\n").encode("utf-8", "replace"))
        finally:
            os.close(fd)
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


def _same_dir(a, b):
    """True only when a and b are the SAME directory inode, by lstat identity
    (no symlink following) - so a symlinked root never dedups away a scope."""
    try:
        sa, sb = os.lstat(a), os.lstat(b)
        return (sa.st_dev, sa.st_ino) == (sb.st_dev, sb.st_ino)
    except OSError:
        return False


def _resolve_project_root(payload):
    env = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if env and os.path.isabs(env):
        return env
    cwd = payload.get("cwd") if isinstance(payload, dict) else None
    if isinstance(cwd, str) and os.path.isabs(cwd):
        return cwd
    return os.getcwd()


_ROOT_ANOMALY_LINE = {
    "root-symlink": "the %s skills directory is a symlink (not a real directory) "
                    "— its skills cannot be trusted; run the skill-vetting skill",
    "root-notdir": "the %s skills path is not a directory — run the "
                   "skill-vetting skill before trusting anything there",
    "root-unreadable": "the %s skills directory could not be read — treat its "
                       "skills as changed; run the skill-vetting skill",
    "root-overfull": "the %s skills directory holds more entries than the scan "
                     "limit — entries beyond it were NOT scanned; run the "
                     "skill-vetting skill on them manually",
}


def _scan_root(scope, label, root, budget):
    """Enumerate one skills root via the hardened primitive (the hook owns no
    filesystem walking of its own). Returns (candidates, root_lines, complete):
    candidates = [(key, display, snap)]; complete=False means enumeration
    failed/was truncated, so baseline pruning for this scope must be skipped
    (a removal cannot be told from not-scanned). A symlinked or unreadable
    root, or a hostile top-level skill NAME, becomes a root/anomaly line here —
    never a silent pass."""
    listing = snapmod.list_candidates(root)
    lines, badnames = [], set()
    for reason, name in listing["anomalies"]:
        if reason in _ROOT_ANOMALY_LINE:
            lines.append(_ROOT_ANOMALY_LINE[reason] % label)
        elif reason == "badname":
            badnames.add(name)
    candidates = listing["candidates"]
    out = []
    try:
        for i, (nameb, dir_fd) in enumerate(candidates):
            try:
                snap = snapmod.snapshot_fd(dir_fd, budget)
            finally:
                os.close(dir_fd)                 # consumed: closed exactly once
                candidates[i] = (nameb, -1)      # mark closed so the sweep skips it
            disp, disp_ok = snapmod.display_name(nameb)
            key = "%s|%s" % (scope, snapmod.name_key(nameb))
            # a hostile top-level name is an anomaly the snapshot cannot carry
            # (it is about the name, not the tree) — force it onto the snap so
            # the candidate can never settle into silence.
            if not disp_ok or nameb in badnames:
                snap = dict(snap)
                snap["anomalies"] = list(snap["anomalies"]) + [("badname", nameb)]
            out.append((key, "%s:%s" % (label, disp), snap))
    finally:
        for _nameb, dir_fd in candidates:        # any fd not yet consumed
            if dir_fd is not None and dir_fd >= 0:
                try:
                    os.close(dir_fd)
                except OSError:
                    pass
    return out, lines, listing["complete"]


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
        global_skills = os.path.join(cfg, "skills")
        roots = [("global", "global", global_skills)]
        proj_skills = os.path.join(proj, ".claude", "skills")
        # Dedup by lstat IDENTITY, not realpath: a realpath compare follows a
        # symlink, so a project skills dir replaced by a symlink to the global
        # root would compare-equal and be silently skipped (sol#3). lstat
        # identity only matches when the two paths are literally the same
        # directory inode - a symlinked project root then differs, is NOT
        # deduped, gets scanned, and its symlink surfaces as an anomaly.
        if not _same_dir(proj_skills, global_skills):
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
        budget = {"bytes": 0, "entries": 0, "stop": False}  # shared across ALL candidates
        for scope, label, root in roots:
            candidates, root_lines, complete = _scan_root(scope, label, root, budget)
            head_lines.extend(root_lines)
            prev = scanned_scopes.get(scope, True)
            scanned_scopes[scope] = prev and complete
            for key, disp, snap in candidates:
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

        # Deliver BEFORE advancing the baseline (G5/R2-08): a failed delivery
        # must leave the old baseline so the same deltas re-advise next run.
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

        # Now advance the baseline. A store that cannot persist is a DETECTION
        # failure for next session — so when this was a SILENT run (nothing
        # delivered, e.g. a first-run bootstrap), a store failure fails CLOSED
        # with its own advisory rather than repeating a silent bootstrap that
        # would swallow any change made before the next run (sol#2 / luna F4).
        merged = snapmod.fresh_baseline()
        merged["entries"] = new_entries
        if state != "ok" or merged["entries"] != data["entries"]:
            store_ok, reason = snapmod.store_baseline(merged, bpath)
            if not store_ok:
                _log("WARN baseline write refused/failed (%s)" % reason)
                if not printed:
                    _emit(["the vetting baseline could not be saved (%s) — a "
                           "skill change before the next session may go "
                           "UNOBSERVED; fix the <config>/skill-vetting "
                           "directory, and vet currently installed skills with "
                           "the skill-vetting skill" % reason])
                    printed = True
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
