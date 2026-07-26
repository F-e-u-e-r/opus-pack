#!/usr/bin/env python3
"""Mutation matrix for the skill-vetting hooks: a DEVELOPMENT tool, not a hook.

Each entry reverts exactly one landed fix and asserts the suites go red. A
mutation that SURVIVES means the fix it reverts has no executing test - the
defect could return and the suite would stay green. That is the only thing this
tool measures, and it is worth nothing unless the tool itself is trustworthy.

Three times during the round-8 gate it was not, and each failure had the same
shape: an anchor that was not what it claimed, applied silently.

  1. Entries were appended with a textual `rindex("]\\n")`, which matched the
     close of `survived = []` inside main() rather than the end of MUTATIONS.
     Four mutations were injected as the survivors list's INITIAL VALUE. They
     never ran, and the tool reported them as unprotected fixes with complete
     confidence.
  2. An anchor that occurred TWICE was applied with `replace(old, new, 1)`, so
     it mutated the first site rather than the named one. The named property
     went unmeasured across two rounds while the tool printed a verdict for it.
  3. A mutation was written as `lines.extend([]) or lines.append(x)`, which
     still appends x. It could not have failed, and was reported as a survivor.

So the checks below are not defensive garnish; each one is a bug this tool
actually shipped. They run BEFORE any suite does, and a violation is a hard
error rather than a survivor, because "the tool is broken" and "the fix is
unprotected" are different findings and must never share an exit path.

Exit codes, in priority order. 2 the measurement did not happen or did not
finish - a refused invocation, a tool error, or a run that stopped partway;
this outranks a survivor, because exit 1 asserts that the full matrix ran.
1 the full matrix ran and a landed fix has no executing test. 3 the full matrix
ran and everything died, but the repository moved during the run, so the result
is authoritative for the frozen snapshot and for nothing else. 0 the full matrix
ran, everything died, and nothing moved.

Every input that can change what is measured is a command-line option. There
are no environment variables, no config file, and no hidden defaults, which is
what lets the authoritative gate work by comparing the parsed namespace against
the parser's own defaults.

Usage:  python3 hooks/mutation_matrix.py [--check-only] [--only M52,M60]

An AUTHORITATIVE run - the one a closure report may cite - is `--authoritative`,
which REFUSES to combine with any override and refuses if the runner or the
mutation definitions on disk differ from HEAD, so subject, runner and
definitions are one snapshot. --check-only validates anchors and measures
nothing; --allow-dirty-head-only measures HEAD while your uncommitted work sits
outside the run. Neither can be part of an authoritative run, and that is
enforced here rather than asked for in prose.
"""
import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid

HOOKS = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.dirname(HOOKS)
SS = os.path.join(HOOKS, "skill_snapshot.py")
HK = os.path.join(HOOKS, "skill-vetting-advisory.py")
SUITES = (os.path.join(HOOKS, "test-skill_snapshot.sh"),
          os.path.join(HOOKS, "test-skill-vetting-advisory.sh"))


class MatrixError(Exception):
    """The TOOL is wrong, not the artifact. Never reported as a survivor."""


def enclosing_def(src, offset):
    """Name of the innermost function containing `offset`, or '<module>'."""
    line = src.count("\n", 0, offset) + 1
    best = None
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.lineno <= line <= (node.end_lineno or node.lineno):
                if best is None or node.lineno > best.lineno:
                    best = node
    return best.name if best else "<module>"


def check_mutation(src, old, new, expect_def=None):
    """Raise MatrixError unless this mutation is well formed against `src`.

    Returns the name of the function it lands in, so the caller can record
    where a mutation actually applied rather than where its label says."""
    n = src.count(old)
    if n == 0:
        raise MatrixError("anchor not found (the source moved under it)")
    if n > 1:
        raise MatrixError("anchor matches %d sites; replace(old, new, 1) would "
                          "silently mutate the first, which may not be the one "
                          "named" % n)
    mutated = src.replace(old, new, 1)
    if mutated == src:
        raise MatrixError("replacement produces no diff (a no-op mutation "
                          "cannot fail, so a green suite proves nothing)")
    where = enclosing_def(src, src.find(old))
    if expect_def is not None and where != expect_def:
        raise MatrixError("lands in %s, expected %s" % (where, expect_def))
    return where


def authoritative_conflicts(chosen, defaults, flag_of, output_only):
    """Which supplied options are incompatible with --authoritative.

    An ALLOWLIST: anything not named in `output_only` is incompatible the
    moment it differs from its default. Enumerating the overrides that exist
    today would put the burden on whoever adds the next one, and a forgotten
    entry lets a partial run be reported as a whole one - the exact failure the
    mode exists to prevent."""
    return sorted(flag_of.get(d, d) for d, v in chosen.items()
                  if d not in output_only and d in defaults
                  and v != defaults[d])


def restore_summary(restores):
    """The one-line summary, derived from the SAME list the record stores.

    It used to be printed from a separate count, before the mutation loop had
    run - so an authoritative run reported "1 (1 control + 0 mutations)" while
    its record held 56. The machine evidence was right and the sentence a human
    reads was wrong, which is the defect class this whole branch exists to
    remove, appearing in its own summary. One source, computed once."""
    control = sum(1 for r in restores if r.get("before") == "pristine-control")
    mutations = len(restores) - control
    return ("restores           %d (%d control + %d mutations), all ok=%s"
            % (len(restores), control, mutations,
               all(r.get("ok") for r in restores)))


def restore_worktree(wt, sha, run):
    """Rebuild the worktree to `sha` EXACTLY, ignored files included.

    `git status --porcelain` was the earlier gate and it is not enough: it
    cannot see ignored paths, so a suite's __pycache__, .pytest_cache or any
    generated fixture would survive into the next mutant and become part of its
    input. A verdict would then be about the mutation plus whatever the last
    run left behind.

    Observing "no residue" does not close this. On the machine where that was
    measured, sys.pycache_prefix is /Users/.../Library/Caches/com.apple.python,
    so this interpreter writes bytecode OUTSIDE the tree - a property of the
    platform, not of the tool. Anywhere else the cache lands in the worktree.
    So the state is rebuilt rather than inspected.

    SCOPE, stated because the guarantee travels with the repository and the
    evidence for it does not: this restores REPO-LOCAL state. It does not touch
    $HOME, $TMPDIR, XDG caches or platform caches. Measured on the two suites
    this matrix runs: $TMPDIR showed 0 new and 0 changed files across a full
    run (they use mktemp and clean up), and the only ~/.claude deltas were this
    session's own transcript and usage file - confirmed by a control that
    waited the same interval WITHOUT running them and saw the same two files
    move. Python bytecode goes to sys.pycache_prefix on this platform and is
    not shown to change any verdict. A suite that later grows external state
    would need its own isolation; this function would not provide it.

    -> None on success, or a reason string."""
    for cmd in (["git", "reset", "--hard", sha], ["git", "clean", "-fdx"]):
        r = run(cmd, wt)
        if r.returncode != 0:
            return "%s failed in the worktree: %s" % (" ".join(cmd[:3]),
                                                      r.stderr.strip()[:200])
    # POSTCONDITION. Two commands exiting 0 is a claim about the commands, not
    # about the tree: "restore ok" meant only that git returned zero (raised by
    # a cross-family review). Check the state the restore was for.
    r = run(["git", "status", "--porcelain"], wt)
    if r.returncode != 0 or r.stdout.strip():
        return ("the worktree is not clean after reset+clean: %s"
                % (r.stdout.strip().splitlines() or [r.stderr.strip()])[0][:120])
    r = run(["git", "rev-parse", "HEAD"], wt)
    if r.stdout.strip() != sha:
        return ("the worktree is at %s, not the frozen subject"
                % r.stdout.strip()[:12])
    return None


def write_record(path, payload):
    """Write the run's durable evidence. Exclusive create, so a second run can
    never silently take an earlier one's place.

    A separate function because the orchestration has to be shown CONSUMING a
    failure, not just holding a rule about one. Testing `unrecorded_run_is_fatal`
    proves the rule; patching this proves main() actually asks it."""
    with open(path, "x") as fh:
        json.dump(payload, fh, indent=1)
    return path


def unrecorded_run_is_fatal(authoritative, exc):
    """-> the incompleteness reason, or None.

    An authoritative run that leaves no durable record has produced a claim
    with nothing behind it, and it used to exit 0 after printing one line
    nobody downstream reads. Reachable without malice: a PID reused at the same
    commit with the same selection collides under the exclusive create, and a
    read-only temp directory does it too."""
    if not authoritative:
        return None
    return ("the per-mutant record could not be written (%s), so this run has "
            "no durable evidence" % exc)


def closure_exit(survived, unexpected, drifted, authoritative, incomplete=None):
    """The run's exit code. Pure, so the contract a CI gate reads is tested
    rather than described.

    The priority is deliberate and the top of it is the subtle part:

      2  the measurement did not happen or did not finish - a refused
         invocation, a tool error, or a run that stopped partway. This outranks
         a survivor, because exit 1 asserts "the full matrix ran and something
         lived", and a half-finished run has not earned that sentence. Any
         survivors already seen are still printed; they are just not the
         headline.
      1  the full matrix ran and a landed fix has no executing test.
      3  the full matrix ran, everything died, but the repository moved
         underneath - true of the frozen snapshot, not evidence about the
         checkout in front of you. Collapsing this into 0 with a printed note
         leaves a warning nothing downstream reads.
      0  the full matrix ran, everything died, nothing moved."""
    if incomplete:
        return 2
    if survived or unexpected:
        return 1
    if drifted and authoritative:
        return 3
    return 0


# THE authoritative set. Every stage - preflight concealment check, blob
# equality, and the end-of-run drift check - reads THIS and nothing else.
#
# It listed the .sh wrappers and not the .py bodies, which is where all the
# test logic lives: the wrappers are twelve lines that `exec` the sibling .py.
# So concealing a modification to test-skill_snapshot.py bypassed the check
# entirely - the fix for the first concealment finding protected the shell and
# missed the substance (found by a cross-family verifier review). Keeping one
# list, read by every stage, is what stops the next path from being covered in
# one place and not another.
MEASUREMENT_PATHS = ("hooks/skill_snapshot.py", "hooks/skill-vetting-advisory.py",
                     "hooks/test-skill_snapshot.py",
                     "hooks/test-skill-vetting-advisory.py",
                     "hooks/test-skill_snapshot.sh",
                     "hooks/test-skill-vetting-advisory.sh",
                     "hooks/mutation_matrix.py", "hooks/mutations.json")


def identity_snapshot(paths, ls_files_v, blob_of_disk, blob_at_head, head):
    """Everything that must not move during a run, captured the same way at
    both ends. The start check covered all measurement paths; the end check
    covered HEAD, the runner and the definitions only - so a concealment flag
    set AFTER preflight left the run printing AUTHORITATIVE FOR CURRENT
    CHECKOUT while the checkout held unmeasured edits (cross-family review).
    Asymmetry between two checks of the same property is the defect; one
    function used twice is the fix."""
    snap = {"head": head}
    for path in paths:
        flag = (ls_files_v(path) or " ").split()[0] if ls_files_v(path) else ""
        snap[path] = (flag, blob_of_disk(path), blob_at_head(path))
    return snap


def identity_drift(start, end):
    """-> list of what moved between two snapshots."""
    out = []
    if start.get("head") != end.get("head"):
        out.append("canonical HEAD")
    for key in sorted(set(start) | set(end)):
        if key == "head":
            continue
        if start.get(key) != end.get(key):
            out.append(key)
    return out


def porcelain_paths(porcelain):
    """Paths out of `git status --porcelain`, tolerating a stripped first line.

    `dirty` is stored .strip()ed for display, which eats the LEADING space of
    the first entry - so a fixed `line[3:]` slice returned "ooks/x.py" for the
    first path and the right answer for every other one. My probe fed the raw
    output and looked correct; the code fed the stripped one."""
    out = set()
    for line in porcelain.splitlines():
        line = line.strip()
        if not line or " " not in line:
            continue
        path = line.split(None, 1)[1].strip().strip('"')
        if " -> " in path:                      # rename: the destination is live
            path = path.split(" -> ", 1)[1].strip().strip('"')
        out.add(path)
    return out


def hidden_modifications(paths, ls_files_v, blob_of_disk, blob_at_head,
                         reported=()):
    """-> list of paths whose on-disk content can differ from HEAD INVISIBLY.

    `git status --porcelain` is not a sufficient definition of a clean tree.
    `git update-index --assume-unchanged` and `--skip-worktree` tell git to stop
    reporting a path, so an edit to it never appears in porcelain - while the
    worktree the matrix measures is checked out at HEAD and therefore never
    contains that edit. The run would then be presented as AUTHORITATIVE FOR
    CURRENT CHECKOUT while the checkout held unmeasured modifications: the same
    hazard --allow-dirty-head-only exists to make loud, reached silently.

    Found by a cross-family verifier review and reproduced before this fix:
    porcelain empty, `ls-files -v` showing `h`, disk blob != HEAD blob,
    dirty_gate proceeding with no warning.

    The blob comparison is the check that does not depend on knowing every flag
    git might grow; the flag check is what names the cause when it fires.

    `reported` is what porcelain already named. A path in it is not HIDDEN -
    dirty_gate has already refused it, or the caller knowingly accepted its
    exclusion - and re-refusing it here made --allow-dirty-head-only
    unusable."""
    problems = []
    for path in paths:
        if path in reported:
            continue
        flag = (ls_files_v(path) or " ").split()[0] if ls_files_v(path) else ""
        if flag and (flag.islower() or flag == "S"):
            problems.append("%s is marked %s (assume-unchanged/skip-worktree), "
                            "so git will not report changes to it" % (path, flag))
            continue
        disk, head = blob_of_disk(path), blob_at_head(path)
        if disk and head and disk != head:
            problems.append("%s on disk differs from HEAD without appearing in "
                            "`git status`" % path)
    return problems


def dirty_gate(dirty, allow_head_only, head):
    """-> (proceed, lines_to_print). Pure, so the decision is testable without
    building a repository in a fixture.

    The flag's whole hazard is its name. A worktree is checked out at a COMMIT,
    so uncommitted work is never measured; someone who has just edited a file
    and reached for a permissive-sounding flag would otherwise read a pass as
    being about that edit. So the refusal names the commit, and the override
    itemises exactly what it is leaving out."""
    if not dirty:
        return True, []
    if not allow_head_only:
        return False, [
            "REFUSED: the working tree has uncommitted changes, which a "
            "worktree checkout of %s would NOT include - the run would measure "
            "a tree that is not the one you are looking at. Commit first, or "
            "pass --allow-dirty-head-only to measure HEAD alone." % head[:12]
        ] + dirty.splitlines()
    return True, [
        "WARNING: --allow-dirty-head-only - measuring commit %s. The following "
        "uncommitted changes are NOT in this run:" % head[:12]
    ] + ["    " + line for line in dirty.splitlines()] + [
        "    (a result here says nothing about the edits above.)"]


def load_matrix():
    """Read MUTATIONS from the sibling data file.

    The data is JSON, not Python: it is pure data, and a data file that could
    execute would be one more thing to trust. `path` arrives as the symbol
    "SS" or "HK" and is resolved here."""
    with open(os.path.join(HOOKS, "mutations.json")) as fh:
        data = json.load(fh)
    files = {"SS": SS, "HK": HK}
    out = []
    for m in data["mutations"]:
        out.append(("%s %s" % (m["id"], m["desc"]), files[m["path"]],
                    m["old"], m["new"], m["where"], m.get("equivalent")))
    return out


def suite_is_green(returncode, output):
    """The oracle. Both signals must agree, because each alone misreads.

    It used to be `"\nOK" in (stdout + stderr)` with the return code ignored,
    and a cross-family review demonstrated the misreads in both directions: a
    suite exiting 0 without printing OK was scored RED, and one exiting 1 while
    printing OK was scored GREEN. The first inflates kills, the second hides a
    survivor."""
    return returncode == 0 and "\nOK" in output


def run_suite(script, cwd=REPO):
    r = subprocess.run([script], capture_output=True, text=True, cwd=cwd,
                       timeout=900)
    return suite_is_green(r.returncode, r.stdout + r.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--authoritative", action="store_true",
                    help="the mode a closure report may cite: clean tree, "
                         "every mutation, no overrides - ENFORCED, not merely "
                         "documented")
    ap.add_argument("--check-only", action="store_true",
                    help="validate every mutation's shape; run no suites")
    ap.add_argument("--only", default="",
                    help="comma-separated ids, e.g. M52,M60")
    # NAMED for what it actually does. "--allow-dirty" reads as "include my
    # uncommitted work"; the truth is the opposite - the worktree is checked
    # out at HEAD, so those changes are NOT measured. Someone who has just
    # edited a file and reaches for a permissive-sounding flag would be told
    # their edit passed when it was never run.
    ap.add_argument("--allow-dirty-head-only", action="store_true",
                    help="proceed with a dirty tree, measuring HEAD ONLY - "
                         "uncommitted changes are EXCLUDED from the run")
    args = ap.parse_args(argv)

    # This used to live in the docstring as "an authoritative run takes no
    # flags". A convention in prose is not a gate: anyone could pass an
    # override and still call the result authoritative, which is the same shape
    # of defect - a claim that does not match the artifact - that this whole
    # branch exists to remove. So the mode is a real flag and the exclusions
    # are checked here.
    if args.authoritative:
        # ALLOWLIST, not a list of known offenders. Enumerating the three
        # overrides that existed today would put the burden on whoever adds the
        # fourth to remember this spot - and a forgotten entry silently lets a
        # partial run be reported as a whole one. Anything that is not purely
        # about OUTPUT is incompatible by default, so a new flag is refused
        # until someone deliberately declares it harmless.
        defaults = {a.dest: a.default for a in ap._actions
                    if a.dest not in ("help",)}
        flag_of = {a.dest: (a.option_strings[0] if a.option_strings else a.dest)
                   for a in ap._actions}
        conflicts = authoritative_conflicts(vars(args), defaults, flag_of,
                                            {"authoritative"})
        if conflicts:
            print("REFUSED: --authoritative excludes %s. An authoritative run "
                  "measures EVERY mutation against a clean committed tree with "
                  "no overrides; anything less is a partial run and must not be "
                  "reported as one." % ", ".join(conflicts), file=sys.stderr)
            return 2

    # Which snapshot is the RUNNER, as distinct from the subject? The subject
    # is a worktree at a commit; the runner and the mutation definitions are
    # read from whatever checkout invoked this, which need not be the same one.
    # Compare the on-disk blobs against HEAD's so the report can state it
    # rather than assume it.
    def _blob_matches_head(rel):
        disk = subprocess.run(["git", "hash-object", rel], cwd=REPO,
                              capture_output=True, text=True).stdout.strip()
        committed = subprocess.run(["git", "rev-parse", "HEAD:" + rel], cwd=REPO,
                                   capture_output=True, text=True).stdout.strip()
        return bool(disk) and disk == committed

    run_id = uuid.uuid4().hex[:12]
    matrix = load_matrix()
    total_defined = len(matrix)
    # The digest binds a verdict to the FULL definition it measured - id, path,
    # landing function, both spans and the description - so a definitions file
    # with matching descriptions but rotated spans cannot pass for the one that
    # was measured (cross-family review).
    _defdigest = {}
    with open(os.path.join(HOOKS, "mutations.json")) as _fh:
        for _d in json.load(_fh)["mutations"]:
            _defdigest[_d["id"]] = hashlib.sha256(json.dumps(
                {k: _d.get(k) for k in ("id", "path", "where", "old", "new",
                                        "desc")},
                sort_keys=True, ensure_ascii=True).encode("utf-8")).hexdigest()
    wanted = {x.strip() for x in args.only.split(",") if x.strip()}
    if wanted:
        matrix = [m for m in matrix if m[0].split()[0] in wanted]

    # PHASE 1 - shape. Every entry is validated against the pristine sources
    # before anything is mutated, so a broken tool is reported as a broken tool
    # and never as a finding about the artifact.
    pristine = {}
    for _p in (SS, HK):
        with open(_p) as _fh:
            pristine[_p] = _fh.read()
    broken = []
    for name, path, old, new, expect, _eq in matrix:
        try:
            check_mutation(pristine[path], old, new, expect)
        except MatrixError as exc:
            broken.append((name, str(exc)))
    if broken:
        print("TOOL ERRORS (%d) - no suites were run:" % len(broken))
        for name, why in broken:
            print("  %-58s %s" % (name.split(" (")[0][:58], why))
        return 2
    print("shape check: %d/%d mutations are unique, non-empty and in-place"
          % (len(matrix), len(matrix)))
    if args.check_only:
        print("ANCHOR VALIDATION ONLY - no suite ran, nothing was mutated, and "
              "this is NOT an authoritative measurement.")
        return 0

    # The canonical tree is never mutated. Earlier versions edited
    # hooks/*.py in place and restored them in `finally`, which covers a normal
    # exception and a propagating KeyboardInterrupt or SystemExit - but NOT the
    # SIGTERM default action (what `pkill` sends, and what once left a mutated
    # skill_snapshot.py on disk), SIGKILL, a crash, or power loss. Rather than
    # add handlers for signals that cannot all be handled, put the mutations
    # somewhere losing them costs nothing: a throwaway git worktree.
    #
    # It also binds the run to a COMMIT rather than to whatever happened to be
    # on disk, so the report can name what it measured.
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                           capture_output=True, text=True).stdout.strip()
    proceed, notes = dirty_gate(dirty, args.allow_dirty_head_only, head)
    for line in notes:
        print(line, file=sys.stderr)
    if not proceed:
        return 2

    _lsv = lambda rel: subprocess.run(["git", "ls-files", "-v", rel], cwd=REPO,
                                      capture_output=True, text=True).stdout.strip()
    _disk = lambda rel: subprocess.run(["git", "hash-object", rel], cwd=REPO,
                                       capture_output=True, text=True).stdout.strip()
    _head = lambda rel: subprocess.run(["git", "rev-parse", "HEAD:" + rel], cwd=REPO,
                                       capture_output=True, text=True).stdout.strip()
    start_identity = identity_snapshot(MEASUREMENT_PATHS, _lsv, _disk, _head, head)

    # Porcelain is not the whole definition of clean - see hidden_modifications.
    hidden = hidden_modifications(
        MEASUREMENT_PATHS,
        lambda rel: subprocess.run(["git", "ls-files", "-v", rel], cwd=REPO,
                                   capture_output=True, text=True).stdout.strip(),
        lambda rel: subprocess.run(["git", "hash-object", rel], cwd=REPO,
                                   capture_output=True, text=True).stdout.strip(),
        lambda rel: subprocess.run(["git", "rev-parse", "HEAD:" + rel], cwd=REPO,
                                   capture_output=True, text=True).stdout.strip(),
        reported=porcelain_paths(dirty))
    if hidden:
        print("REFUSED: the working tree differs from %s in ways `git status` "
              "does not report, so a worktree checkout of it would exclude them "
              "while the run claimed to be authoritative for this checkout:"
              % head[:12], file=sys.stderr)
        for h in hidden:
            print("    " + h, file=sys.stderr)
        return 2

    # PHASE 2 - execute, inside a throwaway checkout of `head`.
    runner_ok = _blob_matches_head("hooks/mutation_matrix.py")
    defs_ok = _blob_matches_head("hooks/mutations.json")
    if args.authoritative and not (runner_ok and defs_ok):
        print("REFUSED: the runner or the mutation definitions on disk differ "
              "from HEAD, so subject, runner and definitions would not be the "
              "same snapshot.", file=sys.stderr)
        return 2
    if args.authoritative:
        print("MODE                AUTHORITATIVE")
        print("OVERRIDES           NONE")
    print("runner commit       %s%s" % (head, "" if runner_ok
                                        else "  (ON-DISK COPY DIFFERS)"))
    print("definitions commit  %s%s" % (head, "" if defs_ok
                                        else "  (ON-DISK COPY DIFFERS)"))
    print("measuring commit %s in an isolated worktree" % head[:12])
    parent = tempfile.mkdtemp(prefix="mutation-matrix-")
    wt = os.path.join(parent, "wt")
    add = subprocess.run(["git", "worktree", "add", "--detach", wt, head],
                         cwd=REPO, capture_output=True, text=True)
    if add.returncode != 0:
        print("REFUSED: could not create an isolated worktree:\n" + add.stderr,
              file=sys.stderr)
        shutil.rmtree(parent, ignore_errors=True)
        return 2
    wt_file = {SS: os.path.join(wt, "hooks", os.path.basename(SS)),
               HK: os.path.join(wt, "hooks", os.path.basename(HK))}
    wt_suites = [os.path.join(wt, "hooks", os.path.basename(x)) for x in SUITES]
    # THE CONTROL. Every verdict below is "the suite went red when this fix was
    # reverted", which means nothing unless the suite is GREEN when nothing is
    # reverted. Without this, suites that were red for an unrelated reason -
    # a broken environment, a missing dependency - would mark every mutant
    # killed and produce a flawless 55/55 with no discriminating power at all.
    # A cross-family review named this; the tool had exactly one run_suite call
    # site, inside the mutant loop.
    restores = []
    why = restore_worktree(wt, head, lambda c, d: subprocess.run(
        c, cwd=d, capture_output=True, text=True))
    restores.append({"before": "pristine-control", "ok": why is None,
                     "sha": head})
    if why:
        print("TOOL ERROR: could not establish the frozen snapshot before the "
              "control run (%s)" % why, file=sys.stderr)
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO,
                       capture_output=True)
        shutil.rmtree(parent, ignore_errors=True)
        return 2
    control = []
    for suite in wt_suites:
        r = subprocess.run([suite], capture_output=True, text=True, cwd=wt,
                           timeout=900)
        _out = r.stdout + r.stderr
        control.append({"suite": os.path.basename(suite),
                        "returncode": r.returncode,
                        "ok_marker": "\nOK" in _out,
                        "green": suite_is_green(r.returncode, _out),
                        # The evidence of WHY, not just that. A control that
                        # reports which suites were red and discards their
                        # output is an instrument that does not say what it
                        # measured - and it cost a CI cycle to notice, because
                        # the suites run inside the worktree and this is the
                        # only place their output exists.
                        "tail": _out.strip().splitlines()[-25:]})
    pristine_red = [c["suite"] for c in control if not c["green"]]
    if pristine_red:
        print("TOOL ERROR: the suites are not green on the UNMUTATED tree (%s), "
              "so 'the suite went red' cannot distinguish a killed mutant from "
              "a broken run." % ", ".join(pristine_red), file=sys.stderr)
        for c in control:
            if c["green"]:
                continue
            print("---- %s: rc=%d, ok_marker=%s ----"
                  % (c["suite"], c["returncode"], c["ok_marker"]),
                  file=sys.stderr)
            for line in c["tail"]:
                print("     " + line, file=sys.stderr)
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO,
                       capture_output=True)
        shutil.rmtree(parent, ignore_errors=True)
        return 2
    for c in control:
        print("control            %-34s rc=%d ok=%s green=%s"
              % (c["suite"], c["returncode"], c["ok_marker"], c["green"]))

    killed, survived, equivalent, unexpected = [], [], [], []
    record = []
    incomplete = None
    try:
        for name, path, old, new, _expect, equiv in matrix:
            # Every mutant shares one worktree, and the suites write into it.
            # A verdict is only about ITS mutation if the tracked content is
            # back at the frozen snapshot first; otherwise the previous
            # mutant's side effects are part of this one's input.
            why = restore_worktree(wt, head, lambda c, d: subprocess.run(
                c, cwd=d, capture_output=True, text=True))
            restores.append({"before": name.split()[0], "ok": why is None,
                             "sha": head})
            if why:
                incomplete = ("could not restore the frozen snapshot before "
                              "%s: %s" % (name.split()[0], why))
                break
            target = wt_file[path]
            pristine_src = open(target).read()
            open(target, "w").write(pristine_src.replace(old, new, 1))
            reds = [s for s in wt_suites if not run_suite(s, cwd=wt)]
            open(target, "w").write(pristine_src)
            tag = name.split(" (")[0][:60]
            record.append({"id": name.split()[0], "desc": name.split(" ", 1)[1],
                           "path": os.path.basename(path), "where": _expect,
                           "definition_digest": _defdigest[name.split()[0]],
                           "suites_red": [os.path.basename(r) for r in reds]})
            if reds:
                where = ", ".join(os.path.basename(r).replace("test-", "")
                                  .replace(".sh", "") for r in reds)
                if equiv:
                    # An entry declared unkillable that DIES is not good news:
                    # either the equivalence argument was wrong or the code
                    # moved. Both invalidate the record, so say so loudly.
                    print("  %-60s killed, but DECLARED EQUIVALENT" % tag)
                    unexpected.append(name)
                else:
                    print("  %-60s killed (%s)" % (tag, where))
                    killed.append(name)
            elif equiv:
                print("  %-60s equivalent (as declared)" % tag)
                equivalent.append(name)
            else:
                print("  %-60s ** SURVIVED **" % tag)
                survived.append(name)
    except Exception as exc:                      # noqa: BLE001 - reported, not hidden
        incomplete = "%s: %s" % (type(exc).__name__, exc)
    finally:
        # Best effort: if this is skipped by a signal that cannot be handled,
        # what is left behind is a disposable directory, not a modified source.
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO,
                       capture_output=True)
        shutil.rmtree(parent, ignore_errors=True)
        subprocess.run(["git", "worktree", "prune"], cwd=REPO,
                       capture_output=True)

    # The per-mutant verdicts existed only on stdout, so a pipeline as ordinary
    # as `| tail -20` destroyed them - which is exactly what happened to this
    # branch's first two checkpoint runs, leaving only totals to compare. A
    # comparison of totals cannot see a mutant that changed which suite killed
    # it. Write the record somewhere a pipe cannot reach.
    #
    # No flag: an option would be a non-default input, and the authoritative
    # gate refuses those. Outside the repo: a file in the tree would dirty it
    # and the NEXT authoritative run would refuse to start.
    for entry in record:
        entry["verdict"] = ("killed" if entry["suites_red"] else "survived")
    # The name was keyed on the COMMIT alone, so every run at that commit wrote
    # the same file - and a `--only M18` run silently replaced a full
    # authoritative run's 55 rows with one. It happened: the harness's own test
    # for this record destroyed the record two minutes after the closure
    # verifier had passed against it. A partial measurement occupying a full
    # one's path is the evidence-layer form of exactly what the authoritative
    # mode exists to prevent, so the name now carries the selection and the
    # process, and the body carries the mode - a reader can no longer mistake
    # one for the other, and a later run cannot overwrite an earlier one.
    # The uniqueness primitive is a NONCE, not the pid. A pid is reused, and a
    # leftover file from a dead run would then make a perfectly legitimate new
    # measurement fail closed for no reason - a false incomplete rather than a
    # false success, but still a wrong answer. The pid stays as diagnostics.
    #
    # The same id is printed, stored, and cross-checked, so a report cannot be
    # assembled from one run's stdout and another run's record.
    rec_path = os.path.join(
        tempfile.gettempdir(),
        "mutation-matrix-%s-%dof%d-%s.json"
        % (head[:12], len(matrix), total_defined, run_id))
    try:
        write_record(rec_path, {
            "run_id": run_id,
            "subject_commit": head,
            "mode": "authoritative" if args.authoritative
                    else "partial-or-unqualified",
            "measured": len(matrix),
            "total_definitions": total_defined,
            "pid": os.getpid(),
            "invocation": ["mutation_matrix.py"] + list(argv if argv is not None
                                                        else sys.argv[1:]),
            "pristine_control": control,
            "restores": restores,
            "restore_scope": "repo-local (git reset --hard + git clean -fdx); "
                             "$HOME, $TMPDIR and platform caches are NOT reset",
            "mutations": record})
        print("per-mutant record  %s" % rec_path)
    except OSError as exc:
        # An authoritative run that leaves no durable record has produced a
        # claim with nothing behind it - and it used to exit 0 anyway, printing
        # one line nobody downstream reads. Reachable without malice: a PID
        # reused at the same commit with the same selection collides under the
        # exclusive create this same fold introduced.
        print("per-mutant record  NOT WRITTEN (%s)" % exc)
        rec_path = None
        incomplete = unrecorded_run_is_fatal(args.authoritative, exc) or incomplete

    # The identity was frozen at startup and the worktree pinned to it, so a
    # commit landing mid-run cannot change what was measured. Re-read it anyway
    # and say so, because "the report shows the SHA it measured" is a claim
    # like any other and this is what makes it checkable.
    head_now = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                              capture_output=True, text=True).stdout.strip()
    end_identity = identity_snapshot(MEASUREMENT_PATHS, _lsv, _disk, _head,
                                     head_now)
    drifted = identity_drift(start_identity, end_identity)

    # Report every category separately. Collapsing them into one ratio is how a
    # tool error, an unkillable mutant and an unprotected fix come to look alike.
    print()
    # Drift is a STATUS, not a warning line. A note that leaves the run exiting
    # 0 as authoritative is a warning downstream ignores - the measurement stays
    # true of the frozen snapshot, but it stops being evidence about the tree in
    # front of you, and only one of those two facts survives a CI gate that
    # reads exit codes.
    print("run id             %s" % run_id)
    print("run identity       %s %s" % (run_id, head))
    print(restore_summary(restores))
    print("subject commit      %s  (frozen at start)" % head)
    print("MEASUREMENT         VALID FOR FROZEN SNAPSHOT")
    print("CURRENT CHECKOUT    %s" % ("DRIFTED (%s)" % ", ".join(drifted)
                                      if drifted else "UNCHANGED"))
    if args.authoritative:
        print("AUTHORITATIVE FOR CURRENT CHECKOUT  %s"
              % ("NO" if drifted else "YES"))
    print("mutation cases      %d" % len(matrix))
    print("  killed            %d" % len(killed))
    print("  survived          %d" % len(survived))
    print("  equivalent        %d  (declared unreachable, with an argument)"
          % len(equivalent))
    print("  no-op / invalid   0  (rejected before execution by the shape check)")
    print("  ambiguous anchor  0  (rejected before execution by the shape check)")
    print("  tool errors       0  (any would have aborted the run)")
    if unexpected:
        print()
        print("DECLARED EQUIVALENT BUT KILLED (%d) - the record is wrong:"
              % len(unexpected))
        for s in unexpected:
            print("  -", s)
    if survived:
        print()
        print("SURVIVORS (%d) - each means a landed fix has no executing test:"
              % len(survived))
        for s in survived:
            print("  -", s)
    if incomplete is None and len(killed) + len(survived) + len(equivalent) \
            + len(unexpected) != len(matrix):
        incomplete = ("only %d of %d mutations produced a verdict"
                      % (len(killed) + len(survived) + len(equivalent)
                         + len(unexpected), len(matrix)))
    if incomplete:
        print()
        print("INCOMPLETE          %s" % incomplete)
        print("  The matrix did not finish, so no verdict about coverage "
              "follows from it - not even from the mutations that did run.")
    code = closure_exit(survived, unexpected, drifted, args.authoritative,
                        incomplete)
    if code == 3:
        print()
        print("EXIT 3: the run is authoritative for %s and for nothing else. "
              "The repository moved while it ran, so this result cannot close "
              "out the current checkout - re-run against it." % head[:12])
    return code


if __name__ == "__main__":
    sys.exit(main())
