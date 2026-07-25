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
a new, changed, or removed top-level DIRECTORY, symlink or special file under a
watched skills root — a top-level regular FILE is deliberately not a candidate,
because a loose `.md` beside the skill directories is not loadable as a skill; any
observation anomaly — an unreadable file or directory, an oversize file, a
budget breach, ANY symlink, a special file (FIFO/socket/device), a hostile or
undecodable name (shown only as an opaque id); an unreadable/corrupt/stale
baseline. An anomalous tree can never be certified unchanged, so it re-advises
EVERY session until the anomaly is resolved — deliberate for a tree that cannot
be fully observed. A clean, unchanged tree is SILENT; a first run emits one
labelled bootstrap line. The hook NEVER blocks and NEVER emits a "safe" line.

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
- First run (no baseline file) records what is already installed as the
  baseline WITHOUT reviewing it, and emits ONE line saying so with the count.
  It is not silent (round 6: a silent bootstrap was reachable a second time
  after a failed first write, which then swallowed a change). Run the
  `skill-vetting` skill on anything present but not yet reviewed;
  `skill_snapshot.py status` lists entries never recorded as vetted.
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
import time
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


LOCK_WAIT_S = 5.0     # bounded: a SessionStart hook must never stall a session
LOCK_STALE_S = 60.0   # a lock older than this belonged to a run that died


def _acquire(lockpath):
    """Serialize load -> scan -> deliver -> store across concurrent hooks.

    load_baseline/store_baseline are a read-modify-write with no lock,
    generation or compare-and-swap, so two SessionStart hooks racing (two
    sessions started at once — ordinary, not adversarial) LOSE an update: the
    slower one writes its stale merge over the faster one's, and the delta the
    faster one advised is un-recorded and never re-advises (round 6). Atomic
    replace prevents a torn file; it does not prevent a lost update.

    O_EXCL create, bounded wait, and takeover of a stale lock so a process that
    died holding it cannot wedge every later session.

    Returns (fd, state): ("held" with an fd) | (None, "contended") when another
    live hook holds it | (None, "unavailable") when the lock file cannot be
    created at all. Those last two are NOT the same thing and must not share a
    message: an unwritable config directory is a degraded run to be reported on
    its own terms, not a peer session doing the work."""
    deadline = time.time() + LOCK_WAIT_S
    while True:
        try:
            return os.open(lockpath,
                           os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_CLOEXEC,
                           0o600), "held"
        except FileExistsError:
            try:
                if time.time() - os.lstat(lockpath).st_mtime > LOCK_STALE_S:
                    os.unlink(lockpath)
                    continue
            except OSError:
                pass
            if time.time() >= deadline:
                return None, "contended"
            time.sleep(0.05)
        except OSError:
            return None, "unavailable"


def _release(fd, lockpath):
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        os.unlink(lockpath)
    except OSError:
        pass


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
    """Enumerate + snapshot one skills root via the primitive's streaming
    `scan_root` (the hook owns no filesystem walking of its own; the primitive
    holds the fds and returns finished snaps). Returns (candidates, root_lines,
    complete): candidates = [(key, display, snap)] for EVERY top-level entry -
    a directory, a symlink, a special file, or an open-failure - so none is
    silently dropped (round-4 SV4-01); complete=False means enumeration
    failed/was truncated, so baseline pruning for this scope must be skipped."""
    scanned = snapmod.scan_root(root, budget)
    lines = [_ROOT_ANOMALY_LINE[r] % label
             for r, _n in scanned["anomalies"] if r in _ROOT_ANOMALY_LINE]
    out = []
    for nameb, snap in scanned["candidates"]:
        disp, disp_ok = snapmod.display_name(nameb)
        key = "%s|%s" % (scope, snapmod.name_key(nameb))
        # a hostile top-level NAME is an anomaly about the name, not the tree -
        # force it onto the snap so the candidate can never settle into silence.
        if not disp_ok:
            snap = dict(snap)
            snap["anomalies"] = list(snap["anomalies"]) + [("badname", nameb)]
        out.append((key, "%s:%s" % (label, disp), snap))
    return out, lines, scanned["complete"]


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
        # Everything from here to the store is one critical section: see
        # _acquire. A hook that cannot take the lock does NOT scan and does NOT
        # touch the baseline — the holder is doing exactly this work and will
        # advise — but it says so rather than looking clean.
        lockpath = bpath + ".lock"
        try:
            os.makedirs(os.path.dirname(bpath), mode=0o700, exist_ok=True)
        except OSError:
            pass
        lock_fd, lock_state = _acquire(lockpath)
        if lock_state == "contended":
            # The lock is HELD by someone. We deliberately do not claim the
            # holder is alive or that it will advise: the lock file carries no
            # pid and liveness is never checked, so a lock left by a process
            # that died under LOCK_STALE_S reaches here too. Say only what is
            # known — this session did not scan — which is the fail-closed
            # statement either way. (Replacing this with fcntl.flock, which the
            # kernel releases on death, is design item D2.)
            _emit(["the skills directories were not scanned this session "
                   "because another run holds the vetting lock — treat "
                   "installed skills as unverified for this session and run "
                   "the skill-vetting skill on anything you did not install "
                   "yourself"])
            return 0
        # "unavailable" (the lock file cannot be created at all) is a degraded
        # run, not contention: proceed unlocked. The store will fail for the
        # same underlying reason and take its own fail-closed advisory path.
        try:
            return _run(snapmod, roots, bpath, cfg, lock_state)
        finally:
            if lock_fd is not None:
                _release(lock_fd, lockpath)
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        if not printed:
            _emit(["the skill-vetting advisory hook could not complete "
                   "(internal error) — skill changes may be UNOBSERVED this "
                   "session; run the skill-vetting skill manually on anything "
                   "new or changed"])
        return 0


def _run(snapmod, roots, bpath, cfg, lock_state="held"):
    """The critical section: load the baseline, scan every watched root,
    deliver the advisory, then advance the baseline. Called with the lock held."""
    printed = False
    try:
        state, data = snapmod.load_baseline(bpath)
        old_entries = data["entries"] if state == "ok" else {}

        head_lines = []
        if lock_state == "unavailable":
            # We could not even create a lock file next to the baseline, so the
            # store below will fail for the same reason. Say it HERE, in the one
            # advisory this run emits: delivery-before-advance (G5) means the
            # store happens after the emit, and a second emit would put two JSON
            # objects on a stdout the harness reads as one.
            head_lines.append(
                "the vetting baseline directory is not writable — the baseline "
                "could not be saved, so a skill change before the next session "
                "may go UNOBSERVED; fix the <config>/skill-vetting directory, "
                "and vet currently installed skills with the skill-vetting skill")
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

        # delta_lines holds TRANSIENT events (new / changed / removed): each
        # fires once and is then consumed by the baseline advance. Every item is
        # (line, key, prior_entry_or_None) so a line that does not fit the
        # display cap can have its baseline entry put back, leaving the delta
        # undelivered and therefore still pending (G5, round 6).
        anomaly_lines, delta_lines = [], []
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
                # A `partial` snap's digest describes the SCAN STATE, not the
                # tree: a resource-budget short-circuit yields one constant,
                # content-independent digest. Never let it decide "changed", and
                # never let it overwrite a real recorded digest - otherwise a
                # later genuine change compares equal to the placeholder and is
                # invisible to the detector (round 6).
                partial = bool(snap.get("partial"))
                is_changed = (old is not None and not partial
                              and old["digest"] != snap["digest"])
                anomalous = bool(snap["anomalies"])
                if state == "absent" and not anomalous:
                    status = "baseline"          # first-run bootstrap: silent
                elif state == "absent":
                    status = "seen"              # anomalous first-run: advised, so seen (SV4-N1)
                elif state != "ok":
                    status = "seen"              # advised untrusted collectively
                elif is_new or is_changed:
                    status = "seen"
                else:
                    status = old["status"]       # unchanged: keep status+verdict
                if partial and old is None:
                    # Never seen before AND not observed this run: recording the
                    # content-independent placeholder as this skill's digest
                    # would make a later real observation compare equal to it.
                    # Leave it out of the baseline entirely so the next run
                    # treats it as new (round 7 - the round-6 fix only covered
                    # the case where a prior real record existed).
                    continue
                if partial and old is not None:
                    entry = dict(old)           # not observed: keep the real record
                else:
                    entry = {"digest": snap["digest"], "status": status,
                             "name": disp.split(":", 1)[1], "scope": scope}
                    if status == "vetted" and old:   # preserve the verdict record
                        for f in ("verdict", "provenance"):   # SV4-09: provenance too
                            if f in old:
                                entry[f] = old[f]
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
                    delta_lines.append((
                        "new skill %s — run the skill-vetting skill on it "
                        "before trusting it or reusing a prior verdict" % disp,
                        key, None))
                elif state == "ok" and is_changed:
                    delta_lines.append((
                        "changed skill %s — run the skill-vetting skill on it "
                        "before trusting it or reusing a prior verdict" % disp,
                        key, old))

        if state == "ok":
            for key, old in old_entries.items():
                scope = old["scope"]
                if scope in scanned_scopes and key not in new_entries:
                    if scanned_scopes[scope]:
                        # Carries `old` so an undelivered removal line can put
                        # the entry back instead of pruning it: a pruned entry
                        # can never re-fire, which made a lost removal line the
                        # one unrecoverable case (round 6).
                        delta_lines.append((
                            "skill %s was removed — baseline entry pruned"
                            % old["name"], key, old))
                    else:
                        new_entries[key] = old   # incomplete enumeration: keep
                elif scope not in scanned_scopes:
                    new_entries[key] = old       # other project: preserve
        elif state == "absent" and new_entries:
            # A first run used to be entirely silent, and that silence was
            # reachable a second time: if the very first baseline write failed
            # transiently, the next session saw "absent" again and silently
            # baselined whatever the content had become in between (round 6).
            # One honest line makes the bootstrap auditable and closes that
            # sequence without needing durable failure state.
            head_lines.append(
                "first run — %d installed skill(s) recorded as the baseline "
                "WITHOUT review; run the skill-vetting skill on any you have "
                "not vetted (`skill_snapshot.py status` lists them)"
                % len(new_entries))

        # Deliver BEFORE advancing the baseline (G5/R2-08): a failed delivery
        # must leave the old baseline so the same deltas re-advise next run.
        # Transient deltas outrank steady-state anomalies for the scarce display
        # slots. An anomaly line recurs every session until the condition is
        # fixed, so losing one costs a session; a delta line fires ONCE and is
        # then consumed by the baseline advance, so losing one costs it
        # permanently. The old order was the reverse, and eight recurring
        # anomalies were enough to evict every real add/change/removal forever
        # while the baseline advanced anyway (round 6). Any delta that still
        # does not fit is REVERTED in the baseline, so it is genuinely pending
        # rather than silently consumed — this is what makes G5 literal.
        # Budget the slots UP FRONT so the total can never exceed MAX_LISTED.
        # Round 7: truncating the composed list afterwards was wrong twice over
        # - it discarded the summary lines that carry the counts, and it dropped
        # delta lines whose baseline entries had already been advanced, which is
        # exactly the G5 hole round 6 closed. Reserve a slot for each summary
        # that will actually be needed, then allocate.
        room = max(1, MAX_LISTED - len(head_lines))
        anom_reserve = 1 if anomaly_lines else 0
        delta_room = max(0, room - anom_reserve)
        if len(delta_lines) > delta_room:
            shown_deltas = delta_lines[:max(0, delta_room - 1)]   # 1 slot: summary
        else:
            shown_deltas = delta_lines
        # Whatever did not fit is PUT BACK, so it is pending rather than
        # consumed - an undelivered add stays new, an undelivered change or
        # removal keeps its prior entry and re-advises next session.
        for _l, key, prior in delta_lines[len(shown_deltas):]:
            if prior is None:
                new_entries.pop(key, None)
            else:
                new_entries[key] = prior
        lines = head_lines + [l for l, _k, _p in shown_deltas]
        held = len(delta_lines) - len(shown_deltas)
        total = len(delta_lines) + len(anomaly_lines)
        if held:
            # The cap may hide LINES; it must never hide COUNTS.
            lines.append("...and %d further new/changed/removed skill(s) held "
                         "back for the next session — %d total; run the "
                         "skill-vetting skill on ALL of them" % (held, total))
        left = MAX_LISTED - len(lines)
        if anomaly_lines:
            if len(anomaly_lines) <= left:
                lines.extend(anomaly_lines)
            else:
                keep = max(0, left - 1)
                lines.extend(anomaly_lines[:keep])
                lines.append("...and %d more skill(s) that cannot be certified "
                             "unchanged — %d total; run the skill-vetting skill "
                             "on ALL of them"
                             % (len(anomaly_lines) - keep, total))
        if lines:
            shown = lines
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
