#!/usr/bin/env python3
"""Claude Code SessionStart hook: a PURE-ADVISORY tripwire for unvetted or
changed third-party skills. Companion to the `skill-vetting` skill; enforces
nothing.

Signature scanning is not a security boundary and has been removed. The hook
detects complete skill-tree changes and requires full skill vetting against the
exact content snapshot before trust or reuse of a cached verdict. It does not
attempt to decide whether a skill is malicious — a regex over skill text has low
recall on fluent-prose / cross-file / split / indirect payloads and would only
create false assurance (and, by echoing skill text, an injection surface). The
real defense is the `skill-vetting` skill: a full, human-grade read. This hook
only routes to it, on a change.

What it does: for each installed skill it computes a SNAPSHOT hash over EVERY
file in the skill's directory tree (relative path + file type + content or
symlink target), so an add, modify, delete, rename, or symlink/filetype change
anywhere under the skill — not just in SKILL.md — changes the snapshot. On a new
or changed skill it injects ONE advisory line routing to the `skill-vetting`
skill. It NEVER blocks (SessionStart cannot deny) and NEVER emits a "safe" line;
a clean, unchanged, first-run baseline is SILENT.

Fail directions (both hold, they are not in tension):
- Robustness = FAIL OPEN: an unexpected internal crash exits 0 with no output, so
  it can never break session start (best-effort logged).
- Detection = FAIL CLOSED: a file read error, a hash it cannot compute, or a
  CORRUPT (present-but-unparseable) cache does NOT silently baseline — it ADVISES,
  so an unreadable or tampered state surfaces rather than passing as trusted.

Known limits (documented, not hidden):
- First run (the cache FILE is absent) establishes the baseline SILENTLY, so a
  skill already present at install time is baselined, not flagged. Run the
  `skill-vetting` skill on anything present but not yet reviewed.
- SessionStart only: a skill installed AFTER the scan is seen next session, and
  plugin-managed skills under `~/.claude/plugins/.../skills` are outside the two
  watched roots — vet those manually.

Ships UNREGISTERED (per-user opt-in; the plugin registers no hooks by design) —
see the README hooks section for manual wiring. Python 3.8+, stdlib only.

The demoted signature patterns are NOT here by design: they live as regression
fixtures for the skill-vetting skill (to test that the agent catches prose /
cross-file / split / indirect payloads), never as a runtime detector.
"""

import hashlib
import json
import os
import re
import sys
import traceback

MAX_LISTED = 8          # cap the DISPLAY only; the full count is always surfaced
MAX_FILE_BYTES = 8 << 20  # per-file read cap (skills are small; guards a pathological file)
_SAFE = re.compile(r"[^\w.-]")


def _log(msg):
    """Best-effort audit line; never raises (preserves fail-open)."""
    try:
        with open(os.path.join(os.path.expanduser("~"), ".claude",
                               "skill-vetting-advisory.log"), "a") as fh:
            fh.write(msg + "\n")
    except Exception:
        pass


def _safe_name(name):
    """Sanitize an untrusted skill directory name before it reaches the model:
    restrict to a safe charset and cap length, so a name containing newlines,
    backticks, bidi controls, or `SYSTEM: ...`-style text cannot be echoed into
    the advisory context as an injection."""
    return _SAFE.sub("?", name)[:64] or "?"


def _snapshot(skill_dir):
    """Hash the WHOLE skill tree: (type, relpath, content-hash-or-target) for
    every file and symlink, sorted. Covers add / modify / delete / rename /
    symlink / filetype change anywhere under the skill. Returns (hex, ok);
    ok=False on any read error so the caller can FAIL CLOSED (advise), never
    silently baseline an unreadable skill."""
    entries = []
    ok = True
    try:
        for dirpath, dirnames, filenames in os.walk(skill_dir):  # followlinks=False: no escape/loop
            dirnames.sort()
            for dn in list(dirnames):
                full = os.path.join(dirpath, dn)
                if os.path.islink(full):
                    try:
                        entries.append(("LD", os.path.relpath(full, skill_dir), os.readlink(full)))
                    except OSError:
                        ok = False
                        entries.append(("E", os.path.relpath(full, skill_dir), ""))
            for fn in sorted(filenames):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, skill_dir)
                try:
                    if os.path.islink(full):
                        entries.append(("L", rel, os.readlink(full)))
                    elif os.path.isfile(full):
                        with open(full, "rb") as fh:
                            data = fh.read(MAX_FILE_BYTES + 1)
                        tag = "F" if len(data) <= MAX_FILE_BYTES else "F+"
                        entries.append((tag, rel, hashlib.sha256(data).hexdigest()))
                    else:
                        entries.append(("?", rel, ""))
                except OSError:
                    ok = False
                    entries.append(("E", rel, ""))
    except OSError:
        ok = False
    blob = "\n".join("%s|%s|%s" % e for e in sorted(entries))
    return hashlib.sha256(blob.encode("utf-8", "replace")).hexdigest(), ok


def _skill_dirs(root):
    """Yield (name, dir) for each immediate skill dir (one holding a SKILL.md)."""
    try:
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if os.path.isfile(os.path.join(d, "SKILL.md")):
                yield name, d
    except OSError:
        return


def _write_atomic(path, obj):
    """Atomic cache write (tmp + replace). Returns True on success. A failed
    write leaves the OLD baseline, so the next run RE-detects the same deltas
    (re-advises) rather than silently baselining them."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(obj, fh)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def main():
    """Always exits 0 (fail-open on crash); advisories via stdout JSON. Detection
    uncertainty (read error / corrupt cache) FAILS CLOSED = advises."""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        cwd = data.get("cwd") or os.getcwd()
        home = os.path.expanduser("~")
        roots = [os.path.join(home, ".claude", "skills"),
                 os.path.join(cwd, ".claude", "skills")]

        cache_path = os.path.join(home, ".claude", ".skill-vetting-cache.json")
        cache, cache_corrupt = {}, False
        cache_present = os.path.exists(cache_path)
        if cache_present:
            try:
                with open(cache_path) as fh:
                    cache = json.load(fh)
                if not isinstance(cache, dict):
                    raise ValueError("cache is not an object")
            except (OSError, ValueError):
                cache, cache_corrupt = {}, True   # present-but-unreadable -> FAIL CLOSED
        first_run = not cache_present            # only a genuinely absent cache baselines silently

        current = {}
        advisories = []
        for root in roots:
            for name, d in _skill_dirs(root):
                key = os.path.join(root, name)
                snap, ok = _snapshot(d)
                current[key] = snap
                sn = _safe_name(name)
                if not ok:
                    # Could not fully read the tree -> fail closed, always advise.
                    advisories.append(
                        "skill `{}` could not be fully read (a file errored) — "
                        "re-vet it with the skill-vetting skill before trusting it".format(sn))
                    continue
                is_new = key not in cache
                is_changed = (not is_new) and cache.get(key) != snap
                if first_run:
                    pass  # silent baseline of the existing setup (documented limit)
                elif cache_corrupt:
                    advisories.append(
                        "skill `{}` — the vetting cache was unreadable, so its baseline "
                        "is untrusted; re-vet it with the skill-vetting skill".format(sn))
                elif is_new or is_changed:
                    advisories.append(
                        "{} skill `{}` — run the skill-vetting skill on it before trusting "
                        "it or reusing a prior verdict".format("new" if is_new else "changed", sn))
                # baselined, unchanged -> silent

        # Merge, do not clobber: preserve baselines for skills in OTHER projects
        # or roots not seen this run, so alternating projects (A -> B -> A) does
        # not re-flag project-local skills as "new" (a single global cache keyed
        # by full path). current wins for keys seen this run.
        merged = dict(cache)
        merged.update(current)
        wrote = _write_atomic(cache_path, merged)
        if not wrote:
            _log("WARN cache write failed " + cache_path + " (deltas will re-advise next run)")

        if not advisories:
            return 0  # clean / unchanged / first-run baseline -> SILENT; never a "safe" line

        shown = advisories[:MAX_LISTED]
        hidden = len(advisories) - len(shown)
        if hidden > 0:
            # Truncate DISPLAY only — never lose a finding silently (condition 7).
            shown.append("...and {} more new/changed skill(s) not shown — run the "
                         "skill-vetting skill on ALL {} of them".format(hidden, len(advisories)))
        context = ("skill-vetting advisory (tripwire only, NOT a safety verdict — the "
                   "skill-vetting skill's full read is the actual check): " + " | ".join(shown))
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context}}, ensure_ascii=True))
        _log("ADVISED {} item(s)".format(len(advisories)))
        return 0
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
