#!/usr/bin/env python3
"""Observation/persistence primitive for the skill-vetting advisory hook.

This module owns everything that touches the filesystem for
`hooks/skill-vetting-advisory.py`: the whole-tree snapshot, the canonical
digest encoding, and the hardened baseline load/store. The hook itself is a
thin dispatcher and contains no observation logic. Design record:
`reviews/2026-07-25-skill-vetting-snapshot-threat-model.md` (threat model,
goals G1-G6, invariants I1-I7). A deliberate naming deviation: this file uses
an underscore (not the hooks/ hyphen convention) because the hook imports it
as a Python module; install it NEXT TO the hook (same directory).

Contract highlights (the tests in hooks/test-skill_snapshot.py hold each):

- INJECTIVE ENCODING (I1): the manifest serializes as a length-prefixed binary
  stream (fixed header + schema version + sorted entries, every field
  length-prefixed). There are no delimiter characters to collide with path or
  symlink-target bytes; two distinct observed trees cannot share a digest.
- FD-VERIFIED OBSERVATION (I2): type from lstat, re-verified by fstat on an fd
  opened O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC (O_NONBLOCK so a planted
  FIFO cannot hang the open); only regular files are hashed, from that fd.
  Symlinks record raw target bytes and are ANOMALIES - their referent can
  change outside the tree, so they can never be certified unchanged.
  Directories are entries too (empty-dir adds/removes change the digest).
- FAIL CLOSED (G2/I5): anything not fully observable - unreadable file/dir,
  oversize file, entry/byte/depth budget breach, symlink, special file
  (FIFO/socket/device), hostile or undecodable name - is an ANOMALY with a
  stable reason code. An anomalous snapshot never counts as "unchanged".
- HARDENED BASELINE I/O (I6): read via O_NOFOLLOW with a size cap and strict
  schema/shape validation (any deviation -> "corrupt", a visible state, never
  a silent re-baseline); write via same-directory mkstemp(0600) + os.replace
  into a 0700, caller-owned, non-group/world-writable directory; a symlinked
  baseline path or untrusted directory refuses the write.
- WHAT THIS DOES NOT GUARANTEE: no resistance to same-privilege tampering
  (the baseline is NOT tamper-evident - local code with your authority can
  rewrite it, the skills, or this file); no malice detection (the
  skill-vetting skill's full read is the actual check); no observation of
  roots outside the watched set; TOCTOU perfection is out of scope - every
  hash is computed from the exact bytes read off an opened fd, so races
  degrade to an extra advisory next run, not a silent miss.

CLI (used by the skill-vetting skill's verdict procedure, §3):
  python3 skill_snapshot.py digest <dir>            # canonical digest + anomalies (exit 3 if anomalous)
  python3 skill_snapshot.py record --scope <global|proj:PATH> --name <name> \
      --dir <dir> --verdict <SAFE-TO-PROPOSE|SUSPECT|BLOCK>   # bind a verdict to the exact snapshot
  python3 skill_snapshot.py status                  # list baseline entries and vetting statuses

Python 3.8+, stdlib only. POSIX (macOS/Linux); Windows is untested and out of
scope for the O_NOFOLLOW/ownership checks.
"""

import hashlib
import json
import os
import re
import stat
import struct
import sys
import tempfile

SCHEMA_VERSION = 1   # versions the manifest encoding + digest; change -> visible re-baseline
POLICY_VERSION = 1   # versions the advisory/verdict policy; change -> visible re-baseline

MAX_ENTRIES = 4096          # per-candidate manifest entries
MAX_FILE_BYTES = 8 << 20    # per-file content cap; larger is an anomaly, never a partial hash
MAX_TOTAL_BYTES = 64 << 20  # per-candidate content budget
MAX_DEPTH = 24              # per-candidate directory depth
MAX_BASELINE_BYTES = 4 << 20

_HEADER = b"opus-pack-skill-snapshot\x00"
_STATUSES = ("baseline", "seen", "vetted")
_VERDICTS = ("SAFE-TO-PROPOSE", "SUSPECT", "BLOCK")
# Display allowlist for untrusted names: conservative ASCII, must start
# alphanumeric. Anything else is shown as an opaque id and flagged "badname".
_DISPLAY_OK = re.compile(rb"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_SCOPE_OK = re.compile(r"(?:global|proj:[0-9a-f]{16})\Z")


def config_root():
    """$CLAUDE_CONFIG_DIR when set to an absolute path, else ~/.claude."""
    env = os.environ.get("CLAUDE_CONFIG_DIR", "")
    if env and os.path.isabs(env):
        return env
    return os.path.join(os.path.expanduser("~"), ".claude")


def baseline_path(cfg_root=None):
    return os.path.join(cfg_root or config_root(), "skill-vetting", "baseline.json")


def name_key(name_bytes):
    """JSON-safe, collision-resistant key segment for an untrusted dir name."""
    return hashlib.sha256(name_bytes).hexdigest()[:16]


def scope_id(project_root_bytes=None):
    """'global', or a JSON-safe project scope derived from the real path bytes."""
    if project_root_bytes is None:
        return "global"
    real = os.path.realpath(project_root_bytes)
    return "proj:" + hashlib.sha256(real).hexdigest()[:16]


def display_name(name_bytes):
    """(display, ok): the name itself when it passes the ASCII allowlist, else
    an opaque digest-derived id - attacker-authored language never reaches the
    model (threat-model G3)."""
    if _DISPLAY_OK.match(name_bytes):
        return name_bytes.decode("ascii"), True
    return "id-" + hashlib.sha256(name_bytes).hexdigest()[:8], False


def _entry(entries, anomalies, budget, rel, kind, payload):
    entries.append((rel, kind, payload))
    if len(entries) > MAX_ENTRIES:
        anomalies.append(("budget", rel))
        budget["stop"] = True


def _read_regular(full, lst, anomalies, rel, budget):
    """Hash a regular file from an O_NOFOLLOW|O_NONBLOCK fd; None on anomaly.
    fstat on the opened fd is authoritative for type and size - a path swapped
    to a symlink/FIFO between lstat and open fails the open or the S_ISREG
    check and lands as an anomaly, and O_NONBLOCK keeps a FIFO from hanging."""
    try:
        fd = os.open(full, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
    except OSError:
        anomalies.append(("unreadable", rel))
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            anomalies.append(("special", rel))
            return None
        if st.st_size > MAX_FILE_BYTES:
            anomalies.append(("oversize", rel))
            return None
        h = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FILE_BYTES:          # grew past the cap mid-read
                anomalies.append(("oversize", rel))
                return None
            h.update(chunk)
        budget["bytes"] += total
        if budget["bytes"] > MAX_TOTAL_BYTES:
            anomalies.append(("budget", rel))
            budget["stop"] = True
        execbit = b"x" if (lst.st_mode & 0o111) else b"-"
        return struct.pack(">Q", total) + h.digest() + execbit
    except OSError:
        anomalies.append(("unreadable", rel))
        return None
    finally:
        os.close(fd)


def snapshot_tree(root):
    """Snapshot one top-level skill candidate (dir, file, or symlink) at
    bytes-path `root`. Returns {"digest", "entries", "anomalies"} where
    anomalies is a list of (reason, rel_path_bytes) with stable reason codes:
    unreadable / oversize / budget / symlink / special / badname / root.
    Anomalies are also manifest entries where they REPLACE an observation, so
    an anomaly appearing or healing changes the digest; comparison callers
    must treat ANY anomaly as "anomalous" regardless of digest equality (I5).
    """
    root = os.fsencode(root)
    entries = []      # (rel_bytes, kind_byte, payload_bytes)
    anomalies = []    # (reason_str, rel_bytes)
    budget = {"bytes": 0, "stop": False}

    try:
        lst = os.lstat(root)
    except OSError:
        anomalies.append(("root", b""))
        _entry(entries, anomalies, budget, b"", b"A", b"root")
        return _finish(entries, anomalies)

    if stat.S_ISLNK(lst.st_mode):
        try:
            target = os.readlink(root)
        except OSError:
            target = b""
        anomalies.append(("symlink", b""))
        _entry(entries, anomalies, budget, b"", b"S", target)
        return _finish(entries, anomalies)

    if stat.S_ISREG(lst.st_mode):
        payload = _read_regular(root, lst, anomalies, b"", budget)
        if payload is None:
            _entry(entries, anomalies, budget, b"", b"A", anomalies[-1][0].encode())
        else:
            _entry(entries, anomalies, budget, b"", b"F", payload)
        return _finish(entries, anomalies)

    if not stat.S_ISDIR(lst.st_mode):
        anomalies.append(("special", b""))
        _entry(entries, anomalies, budget, b"", b"A", b"special")
        return _finish(entries, anomalies)

    stack = [(root, b"", 0)]
    while stack and not budget["stop"]:
        dirpath, rel, depth = stack.pop()
        if depth > MAX_DEPTH:
            anomalies.append(("budget", rel))
            _entry(entries, anomalies, budget, rel, b"A", b"depth")
            budget["stop"] = True
            continue
        try:
            with os.scandir(dirpath) as it:
                dirents = sorted(it, key=lambda d: d.name)
        except OSError:
            anomalies.append(("unreadable", rel))
            _entry(entries, anomalies, budget, rel, b"A", b"unreadable")
            continue
        for de in dirents:
            if budget["stop"]:
                break
            name = de.name
            childrel = rel + b"/" + name if rel else name
            if not _DISPLAY_OK.match(name):
                anomalies.append(("badname", childrel))
            try:
                dst = de.stat(follow_symlinks=False)
            except OSError:
                anomalies.append(("unreadable", childrel))
                _entry(entries, anomalies, budget, childrel, b"A", b"unreadable")
                continue
            if stat.S_ISLNK(dst.st_mode):
                try:
                    target = os.readlink(de.path)
                except OSError:
                    target = b""
                anomalies.append(("symlink", childrel))
                _entry(entries, anomalies, budget, childrel, b"S", target)
            elif stat.S_ISDIR(dst.st_mode):
                _entry(entries, anomalies, budget, childrel, b"D", b"")
                stack.append((de.path, childrel, depth + 1))
            elif stat.S_ISREG(dst.st_mode):
                payload = _read_regular(de.path, dst, anomalies, childrel, budget)
                if payload is None:
                    _entry(entries, anomalies, budget, childrel, b"A",
                           anomalies[-1][0].encode())
                else:
                    _entry(entries, anomalies, budget, childrel, b"F", payload)
            else:
                anomalies.append(("special", childrel))
                _entry(entries, anomalies, budget, childrel, b"A", b"special")
    if budget["stop"]:
        _entry(entries, anomalies, budget, b"", b"A", b"budget")

    return _finish(entries, anomalies)


def _finish(entries, anomalies):
    h = hashlib.sha256()
    h.update(_HEADER)
    h.update(struct.pack(">I", SCHEMA_VERSION))
    for path, kind, payload in sorted(entries):
        h.update(struct.pack(">I", len(path)))
        h.update(path)
        h.update(kind)
        h.update(struct.pack(">I", len(payload)))
        h.update(payload)
    return {"digest": h.hexdigest(), "entries": len(entries), "anomalies": anomalies}


def _valid_entry(v):
    if not isinstance(v, dict):
        return False
    required = {"digest", "status", "name", "scope"}
    allowed = required | {"verdict"}
    if not required.issubset(v) or not set(v).issubset(allowed):
        return False
    return (isinstance(v["digest"], str) and _HEX64.match(v["digest"])
            and v["status"] in _STATUSES
            and isinstance(v["name"], str) and len(v["name"]) <= 80
            and re.match(r"[\x20-\x7e]{1,80}\Z", v["name"])
            and isinstance(v["scope"], str) and _SCOPE_OK.match(v["scope"])
            and ("verdict" not in v or v["verdict"] in _VERDICTS))


def load_baseline(path=None):
    """-> (state, data): ("ok", dict) | ("absent", None) | ("stale", reason)
    | ("corrupt", reason). "stale" = readable but written under a different
    schema/policy version (visible re-baseline); "corrupt" = anything else
    wrong, including a symlinked baseline path - never silently treated as a
    first run (that distinction is load-bearing: round-1 B4/SV-4)."""
    path = path or baseline_path()
    try:
        lst = os.lstat(path)
    except FileNotFoundError:
        return "absent", None
    except OSError:
        return "corrupt", "unreadable"
    if stat.S_ISLNK(lst.st_mode):
        return "corrupt", "symlink"
    if not stat.S_ISREG(lst.st_mode) or lst.st_size > MAX_BASELINE_BYTES:
        return "corrupt", "shape"
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
    except OSError:
        return "corrupt", "unreadable"
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_BASELINE_BYTES:
            return "corrupt", "shape"
        raw = b""
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            raw += chunk
            if len(raw) > MAX_BASELINE_BYTES:
                return "corrupt", "shape"
    except OSError:
        return "corrupt", "unreadable"
    finally:
        os.close(fd)
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return "corrupt", "parse"
    if not isinstance(data, dict) or set(data) != {"schema", "policy", "entries"}:
        return "corrupt", "shape"
    if data["schema"] != SCHEMA_VERSION or data["policy"] != POLICY_VERSION:
        return "stale", "version"
    ent = data["entries"]
    if not isinstance(ent, dict):
        return "corrupt", "shape"
    for k, v in ent.items():
        if not isinstance(k, str) or len(k) > 120 or not _valid_entry(v):
            return "corrupt", "shape"
    return "ok", data


def fresh_baseline():
    return {"schema": SCHEMA_VERSION, "policy": POLICY_VERSION, "entries": {}}


def store_baseline(data, path=None):
    """Atomic, symlink-refusing write. -> (ok, reason). Never raises. A False
    return leaves the previous baseline in place - safe under G5 (the same
    deltas simply re-advise next session)."""
    path = path or baseline_path()
    dirp = os.path.dirname(path)
    try:
        if not os.path.lexists(dirp):
            os.makedirs(dirp, mode=0o700, exist_ok=True)
        dst = os.lstat(dirp)
        if stat.S_ISLNK(dst.st_mode) or not stat.S_ISDIR(dst.st_mode):
            return False, "dir-untrusted"
        if dst.st_uid != os.geteuid() or (dst.st_mode & 0o022):
            return False, "dir-untrusted"
        if os.path.lexists(path) and os.path.islink(path):
            return False, "symlink"
        fd, tmp = tempfile.mkstemp(dir=dirp, prefix=".baseline-", suffix=".tmp")
        try:
            os.write(fd, json.dumps(data, sort_keys=True).encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)
        try:
            os.replace(tmp, path)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            return False, "replace"
        return True, ""
    except OSError:
        return False, "io"
    except Exception:
        return False, "internal"


def _fmt_path(rel_bytes):
    return rel_bytes.decode("utf-8", "backslashreplace")


def _cli_digest(argv):
    if len(argv) != 1:
        print("usage: skill_snapshot.py digest <dir>", file=sys.stderr)
        return 2
    snap = snapshot_tree(argv[0])
    print(json.dumps({
        "schema": SCHEMA_VERSION,
        "policy": POLICY_VERSION,
        "digest": snap["digest"],
        "entries": snap["entries"],
        "anomalies": [{"reason": r, "path": _fmt_path(p)} for r, p in snap["anomalies"]],
    }, ensure_ascii=True, indent=2))
    return 3 if snap["anomalies"] else 0


def _cli_record(argv):
    args = {}
    it = iter(argv)
    for a in it:
        if a in ("--scope", "--name", "--dir", "--verdict"):
            args[a[2:]] = next(it, None)
        else:
            print("unknown argument: " + a, file=sys.stderr)
            return 2
    if None in args.values() or set(args) != {"scope", "name", "dir", "verdict"}:
        print("usage: skill_snapshot.py record --scope <global|proj:PATH> "
              "--name <name> --dir <dir> --verdict <" + "|".join(_VERDICTS) + ">",
              file=sys.stderr)
        return 2
    if args["verdict"] not in _VERDICTS:
        print("verdict must be one of: " + ", ".join(_VERDICTS), file=sys.stderr)
        return 2
    scope = args["scope"]
    if scope != "global":
        if not scope.startswith("proj:"):
            print("scope must be 'global' or 'proj:<project-root-path>'", file=sys.stderr)
            return 2
        scope = scope_id(os.fsencode(scope[len("proj:"):]))
    snap = snapshot_tree(args["dir"])
    if snap["anomalies"] and args["verdict"] == "SAFE-TO-PROPOSE":
        print("REFUSED: the tree is anomalous (" +
              ", ".join(sorted({r for r, _ in snap["anomalies"]})) +
              ") - an anomalous tree cannot be recorded SAFE-TO-PROPOSE "
              "(fail closed); resolve the anomalies or record SUSPECT/BLOCK.",
              file=sys.stderr)
        return 3
    nb = os.fsencode(args["name"])
    disp, _ = display_name(nb)
    state, data = load_baseline()
    if state != "ok":
        print("note: baseline state was '%s' - rebuilding it fresh" % state,
              file=sys.stderr)
        data = fresh_baseline()
    key = "%s|%s" % (scope, name_key(nb))
    data["entries"][key] = {"digest": snap["digest"], "status": "vetted",
                            "verdict": args["verdict"], "name": disp, "scope": scope}
    ok, reason = store_baseline(data)
    if not ok:
        print("baseline write FAILED (%s) - verdict not recorded" % reason,
              file=sys.stderr)
        return 1
    print(json.dumps({"recorded": key, "digest": snap["digest"],
                      "schema": SCHEMA_VERSION, "policy": POLICY_VERSION,
                      "verdict": args["verdict"],
                      "anomalies": sorted({r for r, _ in snap["anomalies"]})},
                     ensure_ascii=True, indent=2))
    return 0


def _cli_status(_argv):
    state, data = load_baseline()
    if state != "ok":
        print(json.dumps({"baseline": state}, ensure_ascii=True))
        return 0
    unvetted = sorted(
        "%s %s (%s)" % (v["scope"], v["name"], v["status"])
        for v in data["entries"].values() if v["status"] != "vetted"
    )
    print(json.dumps({"baseline": "ok", "entries": len(data["entries"]),
                      "unvetted": unvetted}, ensure_ascii=True, indent=2))
    return 0


def main(argv):
    cmds = {"digest": _cli_digest, "record": _cli_record, "status": _cli_status}
    if not argv or argv[0] not in cmds:
        print("usage: skill_snapshot.py {digest|record|status} ...", file=sys.stderr)
        return 2
    return cmds[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
