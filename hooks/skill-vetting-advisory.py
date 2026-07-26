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
budget breach (every candidate enumerated after it then advises too; a walkable
DIRECTORY among them is `partial` and its baseline write is skipped, while a
symlink or special file is a complete observation and IS baselined), ANY symlink, a special file (FIFO/socket/device), a hostile or
undecodable TOP-LEVEL candidate name (shown only as an opaque id; NESTED names
are deliberately not gated, since they are never echoed and their bytes are
already bound into the digest); an unreadable/corrupt/stale baseline. An anomalous tree can never be certified unchanged, so it re-advises
EVERY session until the anomaly is resolved — deliberate for a tree that cannot
be fully observed. A clean, unchanged tree is SILENT, and so is a first run
that found nothing to baseline; a first run that HAS something to baseline
emits one labelled bootstrap line naming that count. The line is emitted BEFORE
the store and says so ("are being baselined"): under G5 the advisory is a single
JSON object, so nothing can correct it afterwards. A store that then fails is
NOT announced separately - it cannot be, once a line has been printed - and does
not need to be: nothing was written, so the next session sees the same state and
says the same thing again. The hook NEVER blocks and NEVER emits a "safe" line.

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
- First run (no baseline file) baselines the installed skills it could snapshot
  WITHOUT reviewing them, and emits ONE line saying so with that count. The line
  is emitted BEFORE the write and is worded that way on purpose: G5 makes the
  advisory a single JSON object, so a store that then fails cannot be corrected
  afterwards and is not announced separately. It does not need to be - nothing
  was written, so the next session sees the same state and says the same thing
  again. "Snapshot" is wider than "observe": the count ALSO includes candidates
  whose observation was complete but adverse - an unreadable directory, a
  symlink, a special file, a hostile name - because for each of those the scan
  established everything it could about THAT candidate, so recording it is
  meaningful. What it EXCLUDES is a candidate lost to a resource-budget
  short-circuit, whose digest would describe the state of the RUN rather than
  the tree; recording that would make a later real observation compare equal to
  a placeholder. Every excluded candidate still advises through its own anomaly
  line, so nothing in the count, and nothing left out of it, is trusted
  silently. So a first run over EMPTY or
  missing skills roots is fully silent - there is nothing recorded without
  review, hence nothing to announce - and a first run in which candidates
  existed but none was observable emits their anomaly lines and no count line.
  What round 6 removed was the case that mattered: a bootstrap that RECORDED
  skills while saying nothing, which was reachable a second time after a failed
  first write and then swallowed a change. A run that records nothing cannot
  swallow anything, so its silence is not that defect. Run the
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
        # The fallback runs exactly when the companion module failed to
        # import - the degraded path - and it must still honour
        # CLAUDE_CONFIG_DIR, or the one run that most needs its log written
        # writes it to the wrong place (round-8 screen, pass 14). Inline rather
        # than shared, because snapmod is what is unavailable here.
        if snapmod:
            cfg = snapmod.config_root()
        else:
            _env = os.environ.get("CLAUDE_CONFIG_DIR", "")
            cfg = _env if (_env and os.path.isabs(_env)) else os.path.join(
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


_ANY_BYTES_WRITTEN = False


def _emit(lines):
    """Print the advisory JSON. True only if the whole write succeeded — the
    caller advances the baseline only on True (delivery before advance). Writes
    the raw fd, not sys.stdout: a broken pipe then fails HERE, atomically with
    the delivery decision, instead of lingering in a buffer whose exit-time
    flush would flip the interpreter's exit code.

    It also records that stdout is no longer pristine. `main` guards its
    last-resort advisory on that, and used to guard it on a LOCAL `printed`
    flag that only `_run`'s same-named local was ever assigned — so the guard
    read False no matter what had been delivered, and an exception raised after
    a successful emit put a SECOND JSON object on stdout, which G5 forbids
    (round 8). The flag lives with the write it describes: a caller cannot set
    it out of step, and there is only one to keep in step.

    PARTIAL is deliberately truthful rather than optimistic: a write that died
    mid-payload emitted bytes, so a second object would corrupt what is already
    there even though nothing complete was delivered."""
    global _ANY_BYTES_WRITTEN
    payload = (json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": _PREFIX + " | ".join(lines)}},
        ensure_ascii=True) + "\n").encode("utf-8")
    try:
        off = 0
        while off < len(payload):
            n = os.write(1, payload[off:])
            off += n
            if n:
                _ANY_BYTES_WRITTEN = True
        return True
    except Exception:
        return False


LOCK_WAIT_S = 5.0     # bounded: a SessionStart hook must never stall a session
LOCK_STALE_S = 60.0   # a lock older than this belonged to a run that died


def _acquire(lockpath):
    """ATTEMPT to serialize load -> scan -> deliver -> store across concurrent
    hooks. It does not achieve it, and the threat model records I11 as NOT MET:
    on the stale-takeover path both racers are granted the lock (40/40 measured),
    `_release` unlinks by path rather than the file it created, and `_cli_record`
    - the other writer of the same baseline - takes no lock at all. Replacing
    this with fcntl.flock is design item D2;
    `test_lock_stale_takeover_is_KNOWN_BROKEN` pins the broken shape so that
    landing D2 forces this docstring to change with it.

    load_baseline/store_baseline are a read-modify-write with no lock,
    generation or compare-and-swap, so two SessionStart hooks racing (two
    sessions started at once — ordinary, not adversarial) LOSE an update: the
    slower one writes its stale merge over the faster one's, and the delta the
    faster one advised is un-recorded and never re-advises (round 6). Atomic
    replace prevents a torn file; it does not prevent a lost update.

    O_EXCL create, bounded wait, and takeover of a stale lock so a process that
    died holding it cannot wedge every later session.

    Returns (fd, state): ("held" with an fd) | (None, "contended") when the
    lock path still exists after the bounded wait - which does NOT establish a
    live holder, since the file carries no pid and liveness is never checked, so
    a lock left by a process that died under LOCK_STALE_S lands here too |
    (None, "unavailable") when the lock file cannot be created at all. Those last two are NOT the same thing and must not share a
    message: an unwritable config directory is a degraded run to be reported on
    its own terms, not a peer session doing the work."""
    deadline = time.time() + LOCK_WAIT_S
    while True:
        try:
            return os.open(lockpath,
                           os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_CLOEXEC,
                           0o600), "held"
        except FileExistsError:
            # The stale branch used to `continue` straight back to the create,
            # jumping over the deadline check below - so a lock that kept being
            # recreated stale spun this loop with no sleep and no bound, and the
            # bounded wait the docstring and LOCK_WAIT_S both promise did not
            # hold on that path (round 8). Now EVERY failure path passes the
            # deadline exactly once; takeover only skips the SLEEP, because
            # having just removed the lock there is nothing to wait for.
            took_over = False
            try:
                if time.time() - os.lstat(lockpath).st_mtime > LOCK_STALE_S:
                    os.unlink(lockpath)
                    took_over = True
            except OSError:
                pass
            if time.time() >= deadline:
                return None, "contended"
            if not took_over:
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
        # touch the baseline. It does NOT claim the holder is alive or that it
        # will advise: `contended` means only that the lock path still existed
        # after the bounded wait, and an abandoned lock younger than
        # LOCK_STALE_S lands there too.
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
            _log("SKIPPED scan — vetting lock held")
            _emit(["the skills directories were not scanned this session "
                   "because the vetting lock was held — treat "
                   "installed skills as unverified for this session and run "
                   "the skill-vetting skill on anything you did not install "
                   "yourself"])
            return 0
        # "unavailable" (the lock file cannot be created at all) is a degraded
        # run, not contention: proceed unlocked. _run then puts the "could not
        # be saved" text into head_lines BEFORE the emit, which is the only
        # place it can go: the store fails for the same underlying reason, but
        # by then a line has printed, so the post-store fallback is unreachable
        # and the failure reaches the session only through that anticipatory
        # head line (round-8 screen, pass 14). The store failure is still
        # logged.
        try:
            return _run(snapmod, roots, bpath, cfg, lock_state)
        finally:
            if lock_fd is not None:
                _release(lock_fd, lockpath)
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        if not _ANY_BYTES_WRITTEN:
            _emit(["the skill-vetting advisory hook could not complete "
                   "(internal error) — skill changes may be UNOBSERVED this "
                   "session; run the skill-vetting skill manually on anything "
                   "new or changed"])
        return 0


def _run(snapmod, roots, bpath, cfg, lock_state="held"):
    """The critical section: load the baseline, scan every watched root,
    deliver the advisory, then advance the baseline.

    Called with the lock held WHEN ONE COULD BE TAKEN. `main()` returns early
    only on "contended"; on "unavailable" - the lock file cannot be created at
    all - it proceeds here UNLOCKED and says so in the advisory, because a
    degraded run that reports itself beats no run. So this is not a serialized
    critical section unconditionally, and lock_state records which case it is."""
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
                "the vetting baseline was unreadable and is being rebuilt — "
                "prior baselines are untrusted; re-vet currently installed "
                "skills with the skill-vetting skill")
        elif state == "stale":
            head_lines.append(
                "the vetting baseline predates the current snapshot "
                "schema/policy (now v%d/v%d) — baselines are being reset; re-vet "
                "currently installed skills with the skill-vetting skill"
                % (snapmod.SCHEMA_VERSION, snapmod.POLICY_VERSION))

        # delta_lines holds TRANSIENT events: those THIS RUN'S BASELINE ADVANCE
        # WILL CONSUME. That is narrower than new/changed/removed - a `partial`
        # candidate is "new" on every run precisely because it is never
        # baselined, so it belongs on the steady-state path (see the
        # classification below; getting this wrong livelocked the queue). Every item is
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
                # tree: the candidate the stop lands inside is incomplete, and
                # every candidate enumerated after it shares ONE constant,
                # content-independent digest. Never let it decide "changed", and
                # never let it overwrite a real recorded digest - otherwise a
                # later genuine change compares equal to the placeholder and is
                # invisible to the detector (round 6).
                partial = bool(snap.get("partial"))
                is_changed = (old is not None and not partial
                              and old["digest"] != snap["digest"])
                anomalous = bool(snap["anomalies"])
                if state == "absent" and not anomalous:
                    status = "baseline"          # first-run bootstrap (announced)
                elif state == "absent":
                    status = "seen"              # anomalous first-run: advised, so seen (SV4-N1)
                elif state != "ok":
                    status = "seen"              # advised untrusted collectively
                elif is_new or is_changed:
                    status = "seen"
                else:
                    status = old["status"]       # unchanged: keep status+verdict
                # Never seen before AND not observed this run: recording the
                # content-independent placeholder as this skill's digest would
                # make a later real observation compare equal to it, so it must
                # stay OUT of the baseline and be treated as new next run.
                #
                # ROUND-8 SCREEN: this used to `continue` here, which skipped the
                # candidate entirely - including the anomaly line composed below.
                # A single oversized skill (4200 files vs MAX_ENTRIES=4096) then
                # made the hook emit ZERO bytes, every session: the over-budget
                # skill was never reported, an ordinary skill enumerated after it
                # was never reported, and the first-run count line was suppressed
                # because new_entries ended up empty. A fix for "do not baseline a
                # placeholder" had become a silent miss, which is the one outcome
                # this component exists to prevent. Skip the BASELINE WRITE only.
                skip_baseline = partial and old is None
                if partial and old is not None:
                    entry = dict(old)           # not observed: keep the real record
                else:
                    entry = {"digest": snap["digest"], "status": status,
                             "name": disp.split(":", 1)[1], "scope": scope}
                    if status == "vetted" and old:   # preserve the verdict record
                        for f in ("verdict", "provenance"):   # SV4-09: provenance too
                            if f in old:
                                entry[f] = old[f]
                if not skip_baseline:
                    new_entries[key] = entry
                if snap["anomalies"]:
                    reasons = ",".join(sorted({r for r, _ in snap["anomalies"]}))
                    kind = "new " if (state == "ok" and is_new) else (
                        "changed " if (state == "ok" and is_changed) else "")
                    line = ("%sskill %s cannot be certified unchanged (%s) — run "
                            "the skill-vetting skill on it before trusting it"
                            % (kind, disp, reasons))
                    # ROUND-8 SCREEN. The split that matters for G5 is TRANSIENT
                    # vs STEADY-STATE, not anomalous vs clean. An anomalous
                    # candidate that is ALSO new or changed fires that news ONCE
                    # and the baseline then consumes it, exactly like a clean
                    # delta - so it needs the same slot priority and the same
                    # revert-if-undelivered protection. Sending it to
                    # anomaly_lines gave it neither: with nine or more anomalous
                    # candidates the overflow branch replaces named lines with a
                    # count, os.scandir order is stable so the SAME trailing
                    # candidates are never named, and a change to one of those
                    # advanced its stored digest with a byte-identical advisory
                    # and could never re-fire. That is the round-6 budget
                    # poisoner, residual: round 6 protected clean deltas from
                    # eviction and left changes riding on anomaly lines exposed.
                    # ...but ONLY if this run will actually consume it. A
                    # candidate whose baseline write is skipped (an unobservable
                    # `partial` one) is never consumed, so it re-appears as
                    # "new" every session: putting it in the transient queue
                    # made it re-claim the same front slots forever, and with
                    # enough of them a genuinely new, cleanly observed skill was
                    # reverted every run and NEVER named — while the advisory
                    # kept saying it was "held back for the next session".
                    # Round-8 screen, pass 9: the axis is not anomalous vs
                    # clean, and not even new vs unchanged — it is WILL THIS
                    # RUN'S BASELINE ADVANCE CONSUME IT.
                    if state == "ok" and (is_new or is_changed) and not skip_baseline:
                        # ...and it goes to the FRONT of the transient queue:
                        # among lines that fire once, one that also cannot be
                        # certified is the higher signal, which is the round-2/3
                        # "the highest-signal line must not be capped away"
                        # intent. Both kinds are revert-protected, so ordering
                        # here decides which is seen FIRST, never which is lost.
                        delta_lines.insert(0, (line, key, old))
                    else:
                        anomaly_lines.append(line)
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
                    if old.get("verdict") in ("BLOCK", "SUSPECT"):
                        # An ADVERSE verdict is the one record worth keeping,
                        # and this branch used to destroy it silently. §0's
                        # flow vets a candidate BEFORE the user installs it, so
                        # at `record` time it is legitimately not under a
                        # watched root - and the very next SessionStart pruned
                        # the BLOCK and announced a removal that had not
                        # happened. `--scope global` made it certain, since
                        # "global" is always in scanned_scopes (round 8).
                        # Keeping it costs one baseline entry and preserves the
                        # judgement if the tree ever appears: unchanged, the
                        # verdict still stands; changed, the hook says so and
                        # drops it, which is the correct direction. `status`
                        # already reports this as recorded-and-not-superseded
                        # rather than as still-installed.
                        new_entries[key] = old
                    elif scanned_scopes[scope]:
                        # Carries `old` so an undelivered removal line can put
                        # the entry back instead of pruning it: a pruned entry
                        # can never re-fire, which made a lost removal line the
                        # one unrecoverable case (round 6).
                        #
                        # The wording must hold for BOTH ways to reach here.
                        # "was removed" asserted a history this hook cannot
                        # know: an entry recorded for a candidate that was
                        # never installed had not been removed from anywhere,
                        # and the line put that falsehood into the session's
                        # context while the tree sat on disk elsewhere.
                        delta_lines.append((
                            "skill %s is not under the watched skills roots — "
                            "baseline entry pruned (removed, or recorded "
                            "without being installed)" % old["name"], key, old))
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
            # PERFECTIVE WORDING IS WRONG HERE: this line is composed and
            # emitted BEFORE store_baseline runs, and G5's single-JSON emit
            # means no correction can follow a successful print. A store that
            # then fails leaves the session told something was "recorded" when
            # nothing was (round-8 screen, pass 12).
            head_lines.append(
                "first run — %d installed skill(s) are being baselined WITHOUT "
                "review; run the skill-vetting skill on any you have not vetted "
                "(`skill_snapshot.py status` lists what was actually stored)"
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
        if held:
            # The cap may hide LINES; it must never hide COUNTS - and a count is
            # only a count OF something. Both overflow lines used to print
            # len(delta_lines) + len(anomaly_lines), so each named one category
            # and then reported the size of both: 10 changed skills and 5
            # anomalous ones produced "15 total" TWICE, a number that was the
            # size of neither group (round 8, reported independently by two
            # lenses). The suite could not catch it because its only count
            # assertion used a fixture with zero anomalies - the one shape where
            # the cross-category sum happens to equal the delta count.
            lines.append("...and %d further new/changed/removed skill(s) held "
                         "back for the next session — %d new/changed/removed in "
                         "all; run the skill-vetting skill on ALL of them"
                         % (held, len(delta_lines)))
        left = MAX_LISTED - len(lines)
        if anomaly_lines:
            if len(anomaly_lines) <= left:
                lines.extend(anomaly_lines)
            else:
                keep = max(0, left - 1)
                lines.extend(anomaly_lines[:keep])
                # "N more" is a lie when the cap left room for none of them:
                # there is nothing for them to be more THAN.
                lines.append("...and %d %s skill(s) that cannot be certified "
                             "unchanged — %d such in all; run the skill-vetting "
                             "skill on ALL of them"
                             % (len(anomaly_lines) - keep,
                                "more" if keep else "further unnamed",
                                len(anomaly_lines)))
        if lines:
            shown = lines
            if not _emit(shown):
                _log("WARN advisory delivery failed — baseline NOT advanced "
                     "(will re-advise)")
                return 0
            _log("ADVISED %d item(s)" % len(lines))

        # Now advance the baseline. A store that cannot persist is a DETECTION
        # failure for next session. Note exactly which runs reach the fallback
        # below: it needs stdout to still be PRISTINE. On a clean UNCHANGED tree
        # store_baseline is never called at all (the guard below), so nothing can
        # fail. A first run WITH skills is NOT one of these either - it emits its
        # bootstrap line, which writes bytes - so its failed store is not announced
        # separately, and does not need to be: nothing was written, so the next
        # session sees the same state and says the same thing again. What is
        # left for the fallback is a run that WROTE while printing nothing, e.g.
        # a first run over empty roots that still stores an empty baseline
        # (round-8 screen, pass 14 - this comment previously called a non-empty
        # first run silent and promised it an advisory it cannot get). There it
        # fails CLOSED
        # with its own advisory rather than repeating a silent bootstrap that
        # would swallow any change made before the next run (sol#2 / luna F4).
        merged = snapmod.fresh_baseline()
        merged["entries"] = new_entries
        if state != "ok" or merged["entries"] != data["entries"]:
            store_ok, reason = snapmod.store_baseline(merged, bpath)
            if not store_ok:
                _log("WARN baseline write refused/failed (%s)" % reason)
                # This fallback can ONLY fire on a run that printed nothing.
                # G5 allows one JSON object, so once any line was emitted -
                # including the first-run bootstrap line - a failed store cannot
                # be announced afterwards. That is why the pre-store lines are
                # worded in-progress: the safety property is not a correcting
                # message, it is that NOTHING WAS WRITTEN, so the next session
                # sees the same state and says the same thing again (round-8
                # screen, pass 13 - five documents had promised a "could not be
                # saved" line that is unreachable in exactly the case they
                # described).
                if not _ANY_BYTES_WRITTEN:
                    _emit(["the vetting baseline could not be saved (%s) — a "
                           "skill change before the next session may go "
                           "UNOBSERVED; fix the <config>/skill-vetting "
                           "directory, and vet currently installed skills with "
                           "the skill-vetting skill" % reason])
        return 0
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        if not _ANY_BYTES_WRITTEN:
            _emit(["the skill-vetting advisory hook could not complete "
                   "(internal error) — skill changes may be UNOBSERVED this "
                   "session; run the skill-vetting skill manually on anything "
                   "new or changed"])
        return 0


if __name__ == "__main__":
    sys.exit(main())
