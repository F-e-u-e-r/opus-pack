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
import json
import os
import shutil
import subprocess
import sys
import tempfile

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


def run_suite(script, cwd=REPO):
    r = subprocess.run([script], capture_output=True, text=True, cwd=cwd,
                       timeout=900)
    return "\nOK" in (r.stdout + r.stderr)


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
        conflicts = [n for n, v in (("--check-only", args.check_only),
                                    ("--allow-dirty-head-only",
                                     args.allow_dirty_head_only),
                                    ("--only", bool(args.only))) if v]
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

    matrix = load_matrix()
    wanted = {x.strip() for x in args.only.split(",") if x.strip()}
    if wanted:
        matrix = [m for m in matrix if m[0].split()[0] in wanted]

    # PHASE 1 - shape. Every entry is validated against the pristine sources
    # before anything is mutated, so a broken tool is reported as a broken tool
    # and never as a finding about the artifact.
    pristine = {SS: open(SS).read(), HK: open(HK).read()}
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
    print("subject commit      %s" % head)
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
    killed, survived, equivalent, unexpected = [], [], [], []
    try:
        for name, path, old, new, _expect, equiv in matrix:
            target = wt_file[path]
            pristine_src = open(target).read()
            open(target, "w").write(pristine_src.replace(old, new, 1))
            reds = [s for s in wt_suites if not run_suite(s, cwd=wt)]
            open(target, "w").write(pristine_src)
            tag = name.split(" (")[0][:60]
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
    finally:
        # Best effort: if this is skipped by a signal that cannot be handled,
        # what is left behind is a disposable directory, not a modified source.
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO,
                       capture_output=True)
        shutil.rmtree(parent, ignore_errors=True)
        subprocess.run(["git", "worktree", "prune"], cwd=REPO,
                       capture_output=True)

    # Report every category separately. Collapsing them into one ratio is how a
    # tool error, an unkillable mutant and an unprotected fix come to look alike.
    print()
    print("commit measured     %s" % head)
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
    return 1 if (survived or unexpected) else 0


if __name__ == "__main__":
    sys.exit(main())
