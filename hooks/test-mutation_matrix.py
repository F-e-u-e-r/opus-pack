#!/usr/bin/env python3
"""Tests for hooks/mutation_matrix.py - the tool the branch's coverage claims
rest on.

Every case here is a failure this tool actually shipped during the round-8
gate. It reported four mutations as unprotected fixes that had never run, kept
mutating one site while printing a verdict for another, and called a no-op
mutation a survivor. So these are regression tests in the strict sense, not
hypotheticals, and they matter as much as the product fixes: a mutation matrix
that lies is worse than no matrix, because it launders an untested fix into a
measured one.
"""
import ast
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

HOOKS = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HOOKS)
import mutation_matrix as mm            # noqa: E402

SAMPLE = '''\
def alpha():
    guard = 1
    if guard:
        return "a"
    return "b"


def beta():
    if guard:
        return "a"
    return "b"
'''


class ShapeChecks(unittest.TestCase):
    """check_mutation is the gate; each rejection below is a shipped bug."""

    def test_a_missing_anchor_is_a_tool_error(self):
        with self.assertRaises(mm.MatrixError) as cm:
            mm.check_mutation(SAMPLE, "no such text", "x")
        self.assertIn("not found", str(cm.exception))

    def test_an_anchor_matching_two_sites_is_rejected(self):
        """`replace(old, new, 1)` takes the FIRST match. An anchor that appears
        in both alpha and beta silently mutates alpha while the entry claims
        beta - which is exactly how M71 was measured against main's guard for
        two rounds while its label named _run's."""
        dup = '    if guard:\n        return "a"'
        self.assertEqual(2, SAMPLE.count(dup), "fixture premise")
        with self.assertRaises(mm.MatrixError) as cm:
            mm.check_mutation(SAMPLE, dup, dup.replace("guard", "True"))
        self.assertIn("2 sites", str(cm.exception))

    def test_a_replacement_that_changes_nothing_is_rejected(self):
        """M58 was `lines.extend([]) or lines.append(x)`, which still appends x.
        A green suite against a no-op mutant proves nothing at all, and it was
        reported as a survivor - i.e. as a finding about the artifact."""
        with self.assertRaises(mm.MatrixError) as cm:
            mm.check_mutation(SAMPLE, "guard = 1", "guard = 1")
        self.assertIn("no diff", str(cm.exception))

    def test_landing_in_the_wrong_function_is_rejected(self):
        with self.assertRaises(mm.MatrixError) as cm:
            mm.check_mutation(SAMPLE, "guard = 1", "guard = 0",
                              expect_def="beta")
        self.assertIn("lands in alpha", str(cm.exception))

    def test_a_well_formed_mutation_reports_where_it_landed(self):
        self.assertEqual("alpha",
                         mm.check_mutation(SAMPLE, "guard = 1", "guard = 0",
                                           expect_def="alpha"))

    def test_enclosing_def_picks_the_innermost_function(self):
        nested = "def outer():\n    def inner():\n        x = 1\n    return inner\n"
        self.assertEqual("inner", mm.enclosing_def(nested, nested.index("x = 1")))
        self.assertEqual("<module>", mm.enclosing_def("y = 2\n", 0))


class DirtyTreeGate(unittest.TestCase):
    """A worktree is checked out at a COMMIT, so uncommitted work is never
    measured. The flag that overrides the refusal must not let anyone believe
    otherwise - it was first called --allow-dirty, which reads as "include my
    changes" and means the opposite."""

    HEAD = "abc123def4567890"

    def test_a_clean_tree_proceeds_silently(self):
        proceed, notes = mm.dirty_gate("", False, self.HEAD)
        self.assertTrue(proceed)
        self.assertEqual([], notes)

    def test_a_dirty_tree_is_refused_and_the_files_are_named(self):
        proceed, notes = mm.dirty_gate(" M hooks/x.py\n?? y.md", False, self.HEAD)
        self.assertFalse(proceed)
        body = "\n".join(notes)
        self.assertIn("REFUSED", body)
        self.assertIn("abc123def456", body, "the refusal must name the commit")
        self.assertIn("hooks/x.py", body)
        self.assertIn("y.md", body, "every excluded change must be listed")

    def test_the_override_itemises_what_it_leaves_out(self):
        proceed, notes = mm.dirty_gate(" M hooks/x.py", True, self.HEAD)
        self.assertTrue(proceed)
        body = "\n".join(notes)
        self.assertIn("WARNING", body)
        self.assertIn("NOT in this run", body,
                      "the override must say the changes are excluded, not "
                      "merely tolerated")
        self.assertIn("hooks/x.py", body)
        self.assertIn("abc123def456", body)

    def test_the_flag_is_not_named_allow_dirty(self):
        """The old name invited exactly the misreading this gate exists to
        prevent: a user who just edited a file, saw a pass, and concluded the
        edit was measured."""
        r = subprocess.run([sys.executable,
                            os.path.join(HOOKS, "mutation_matrix.py"), "--help"],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("--allow-dirty-head-only", r.stdout)
        self.assertNotIn("--allow-dirty ", r.stdout)
        self.assertIn("EXCLUDED", r.stdout)


class SuiteOracle(unittest.TestCase):
    """Every verdict the matrix produces is "the suite went red when this fix
    was reverted". That means nothing unless the suite is green when nothing is
    reverted, and it means nothing if the oracle misreads the suite."""

    def test_both_signals_must_agree(self):
        self.assertTrue(mm.suite_is_green(0, "...\nOK\n"))
        self.assertFalse(mm.suite_is_green(1, "...\nOK\n"),
                         "a suite that printed OK and then FAILED is not green "
                         "- scoring it green hides a survivor")
        self.assertFalse(mm.suite_is_green(0, "tests ran\n"),
                         "a suite that exited 0 without the OK marker is not "
                         "recognisably green - scoring it red inflates kills")
        self.assertFalse(mm.suite_is_green(2, "crash"))

    def test_the_control_is_recorded_not_merely_printed(self):
        """A control that exists only as a stdout line cannot be re-checked
        later, and the whole point of the record is that stdout is losable. The
        record must carry each suite's return code, marker and verdict, bound
        to the same run id and subject as the mutants."""
        r = subprocess.run([sys.executable,
                            os.path.join(HOOKS, "mutation_matrix.py"),
                            "--allow-dirty-head-only", "--only", "M18"],
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        path = [l.split(None, 2)[2].strip() for l in r.stdout.splitlines()
                if l.startswith("per-mutant record")][0]
        import json as _json
        with open(path) as fh:
            rec = _json.load(fh)
        control = rec.get("pristine_control")
        self.assertTrue(control, "the control must be in the record")
        for c in control:
            for field in ("suite", "returncode", "ok_marker", "green"):
                self.assertIn(field, c)
            self.assertTrue(c["green"], "a run whose control was red must not "
                                        "have produced mutant verdicts at all")

    def test_restore_clears_IGNORED_residue_not_just_tracked(self):
        """`git status --porcelain` cannot see ignored paths, so a suite's
        __pycache__ or generated fixture would survive into the next mutant.
        Measuring "no residue" does not close it either: on this machine
        sys.pycache_prefix redirects bytecode outside the tree, which is a
        property of the platform, not of the tool. So the state is REBUILT."""
        import tempfile
        repo = tempfile.mkdtemp(prefix="restore-")
        self.addCleanup(__import__("shutil").rmtree, repo, ignore_errors=True)
        run = lambda c, d=repo: subprocess.run(c, cwd=d, capture_output=True,
                                               text=True)
        run(["git", "init", "-q", "."])
        with open(os.path.join(repo, ".gitignore"), "w") as fh:
            fh.write("junk/\n")
        with open(os.path.join(repo, "f.py"), "w") as fh:
            fh.write("x = 1\n")
        run(["git", "add", "-A"])
        run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
             "commit", "-qm", "i"])
        sha = run(["git", "rev-parse", "HEAD"]).stdout.strip()

        os.makedirs(os.path.join(repo, "junk"))
        with open(os.path.join(repo, "junk", "cache"), "w") as fh:
            fh.write("left by the previous mutant\n")
        with open(os.path.join(repo, "f.py"), "w") as fh:
            fh.write("x = 999   # a mutation\n")
        self.assertEqual("", run(["git", "status", "--porcelain",
                                  "--"] + ["junk"]).stdout.strip(),
                         "premise: the ignored path is invisible to status")
        self.assertTrue(os.path.exists(os.path.join(repo, "junk", "cache")))

        self.assertIsNone(mm.restore_worktree(repo, sha, run))
        self.assertFalse(os.path.exists(os.path.join(repo, "junk")),
                         "ignored residue must be gone")
        with open(os.path.join(repo, "f.py")) as fh:
            self.assertEqual("x = 1\n", fh.read(), "tracked content restored")

    def test_the_record_shows_one_restore_per_case_plus_the_control(self):
        """"Restored before each mutation" must be re-derivable, not a
        procedural sentence in a report. The count is 1 + the number of cases
        measured, each naming what it preceded and the SHA it restored to."""
        r = subprocess.run([sys.executable,
                            os.path.join(HOOKS, "mutation_matrix.py"),
                            "--allow-dirty-head-only", "--only", "M18,M59"],
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        path = [l.split(None, 2)[2].strip() for l in r.stdout.splitlines()
                if l.startswith("per-mutant record")][0]
        import json as _json
        with open(path) as fh:
            rec = _json.load(fh)
        restores = rec["restores"]
        self.assertEqual(rec["measured"] + 1, len(restores),
                         "one restore per case, plus the control")
        self.assertEqual("pristine-control", restores[0]["before"])
        self.assertEqual(["M18", "M59"], [x["before"] for x in restores[1:]])
        self.assertTrue(all(x["ok"] for x in restores))
        self.assertTrue(all(x["sha"] == rec["subject_commit"] for x in restores),
                        "every restore must target the frozen subject")
        self.assertIn("repo-local", rec["restore_scope"])
        self.assertIn("$HOME", rec["restore_scope"],
                      "the scope must say what it does NOT reset")

    def test_a_failed_restore_is_reported_not_swallowed(self):
        class Fail:
            returncode = 1
            stderr = "fatal: cannot reset"
        why = mm.restore_worktree("/nowhere", "deadbeef", lambda c, d: Fail())
        self.assertIn("git reset --hard failed", why)
        self.assertEqual(2, mm.closure_exit([], [], [], True, incomplete=why),
                         "a run that could not establish its own starting "
                         "state must not produce verdicts")

    def test_each_mutation_starts_from_the_frozen_snapshot(self):
        """All mutants share one worktree and the suites write into it. A
        verdict is only about ITS mutation if the tracked content is back at
        the frozen snapshot first."""
        with open(os.path.join(HOOKS, "mutation_matrix.py")) as fh:
            src = fh.read()
        self.assertIn("could not restore the frozen snapshot before", src)
        gate = "why = restore_worktree(wt, head, lambda c, d: subprocess.run("
        self.assertEqual(2, src.count(gate),
                         "restore runs before the control AND before each "
                         "mutation")
        loop = "for name, path, old, new, _expect, equiv in matrix:"
        self.assertLess(src.index(loop), src.rindex(gate),
                        "the gate belongs INSIDE the loop, before each mutation")

    def test_the_matrix_runs_a_pristine_control(self):
        """The tool had exactly one run_suite call site, inside the mutant
        loop, so always-red suites would have marked every mutant killed and
        produced a flawless 55/55 with no discriminating power."""
        with open(os.path.join(HOOKS, "mutation_matrix.py")) as fh:
            src = fh.read()
        self.assertIn("pristine_red", src)
        self.assertIn("not green on the UNMUTATED tree", src)
        # The anchor must be UNIQUE, or this ordering assertion compares
        # against the wrong loop - "for name, path, old, new" also matches the
        # PHASE 1 shape check, which runs earlier, so the test failed while the
        # code was right. The same non-unique-anchor mistake the matrix's own
        # shape gate exists to reject.
        mutation_loop = "for name, path, old, new, _expect, equiv in matrix:"
        self.assertEqual(1, src.count(mutation_loop), "anchor is not unique")
        self.assertEqual(1, src.count("pristine_red = "))
        self.assertLess(src.index("pristine_red = "), src.index(mutation_loop),
                        "the control must run BEFORE the first mutation")


class HiddenModifications(unittest.TestCase):
    """`git status --porcelain` is not the whole definition of a clean tree.

    Found by a cross-family verifier review: `git update-index
    --assume-unchanged` (or --skip-worktree) tells git to stop reporting a
    path, so an edit to it never reaches porcelain - while the worktree the
    matrix measures is checked out at HEAD and never contains that edit. The
    run would be presented as AUTHORITATIVE FOR CURRENT CHECKOUT while the
    checkout held unmeasured modifications. Reproduced before the fix:
    porcelain empty, ls-files -v showing `h`, disk blob != HEAD blob,
    dirty_gate proceeding with no warning."""

    PATHS = ("hooks/skill_snapshot.py",)

    def _probe(self, flag, disk, head, reported=()):
        return mm.hidden_modifications(self.PATHS, lambda p: flag,
                                       lambda p: disk, lambda p: head,
                                       reported=reported)

    def test_porcelain_paths_survives_a_stripped_first_line(self):
        """`dirty` is stored stripped for display, which removes the leading
        space of the FIRST entry only. A fixed line[3:] slice then returned
        "ooks/x.py" for it and the correct path for every other line - so the
        first changed file silently stopped being recognised as reported."""
        raw = " M hooks/a.py\n?? hooks/b.md\n M hooks/c.py"
        self.assertEqual({"hooks/a.py", "hooks/b.md", "hooks/c.py"},
                         mm.porcelain_paths(raw.strip()))
        self.assertEqual({"hooks/a.py", "hooks/b.md", "hooks/c.py"},
                         mm.porcelain_paths(raw))
        self.assertEqual({"new.py"},
                         mm.porcelain_paths("R  old.py -> new.py"))
        self.assertEqual(set(), mm.porcelain_paths(""))

    def test_a_change_porcelain_ALREADY_reported_is_not_hidden(self):
        """The check is about what git does NOT report. Re-refusing a path
        porcelain already named made --allow-dirty-head-only unusable: the
        caller had knowingly accepted that exclusion one gate earlier."""
        self.assertEqual([], self._probe("H hooks/skill_snapshot.py", "abc",
                                         "def",
                                         reported=("hooks/skill_snapshot.py",)))
        self.assertEqual(1, len(self._probe("H hooks/skill_snapshot.py", "abc",
                                            "def")),
                         "and it still fires when porcelain is silent")

    def test_an_ordinary_matching_file_is_clean(self):
        self.assertEqual([], self._probe("H hooks/skill_snapshot.py",
                                         "abc", "abc"))

    def test_assume_unchanged_is_refused_even_when_blobs_match(self):
        """The flag alone is disqualifying: it means git has been told not to
        report future edits, so a later one would be equally invisible."""
        out = self._probe("h hooks/skill_snapshot.py", "abc", "abc")
        self.assertEqual(1, len(out))
        self.assertIn("assume-unchanged", out[0])

    def test_skip_worktree_is_refused(self):
        out = self._probe("S hooks/skill_snapshot.py", "abc", "abc")
        self.assertEqual(1, len(out))
        self.assertIn("skip-worktree", out[0])

    def test_a_blob_mismatch_is_refused_whatever_the_flag(self):
        """The blob comparison is the check that does not depend on knowing
        every flag git might grow; the flag check only names the cause."""
        out = self._probe("H hooks/skill_snapshot.py", "abc", "def")
        self.assertEqual(1, len(out))
        self.assertIn("without appearing in `git status`", out[0])

    def test_the_measured_paths_include_the_subjects_and_the_suites(self):
        """The authoritative blob check covered the runner and the definitions
        but NOT the files being mutated, which is what left the hole."""
        for rel in ("hooks/skill_snapshot.py", "hooks/skill-vetting-advisory.py",
                    "hooks/test-skill_snapshot.sh",
                    "hooks/test-skill-vetting-advisory.sh",
                    "hooks/mutation_matrix.py", "hooks/mutations.json"):
            self.assertIn(rel, mm.MEASUREMENT_PATHS)


class AuthoritativeMode(unittest.TestCase):
    """`--authoritative` is the mode a closure report may cite, so the thing
    that makes it authoritative has to be ENFORCED. It was first written as a
    docstring sentence saying an authoritative run takes no flags - a
    convention in prose, which anyone could ignore while still calling the
    result authoritative. That is the same shape of defect this branch exists
    to remove: a claim that does not match the artifact."""

    def _run(self, *flags):
        return subprocess.run([sys.executable,
                               os.path.join(HOOKS, "mutation_matrix.py")]
                              + list(flags),
                              capture_output=True, text=True, timeout=120)

    def test_it_refuses_every_override(self):
        for flag in ("--check-only", "--allow-dirty-head-only"):
            with self.subTest(flag=flag):
                r = self._run("--authoritative", flag)
                self.assertEqual(2, r.returncode, r.stdout)
                self.assertIn("REFUSED", r.stderr)
                self.assertIn(flag, r.stderr, "the refusal must name the flag")

    def test_it_refuses_a_partial_selection(self):
        r = self._run("--authoritative", "--only", "M18")
        self.assertEqual(2, r.returncode, r.stdout)
        self.assertIn("--only", r.stderr)
        self.assertIn("EVERY mutation", r.stderr)

    def test_a_flag_that_does_not_exist_yet_is_refused_by_default(self):
        """The gate is an ALLOWLIST. Enumerating today's three overrides would
        put the burden on whoever adds the fourth, and a forgotten entry lets a
        partial run be reported as a whole one - the exact failure the mode
        exists to prevent. So the property under test is about a flag nobody
        has written: it must be incompatible the moment it is supplied."""
        defaults = {"authoritative": False, "check_only": False,
                    "only": "", "some_future_bypass": False}
        flag_of = {"check_only": "--check-only", "only": "--only",
                   "some_future_bypass": "--some-future-bypass"}
        chosen = dict(defaults, authoritative=True, some_future_bypass=True)
        self.assertEqual(
            ["--some-future-bypass"],
            mm.authoritative_conflicts(chosen, defaults, flag_of,
                                       {"authoritative"}),
            "a new flag must be refused without anyone remembering to list it")

    def test_defaults_alone_are_not_conflicts(self):
        defaults = {"authoritative": False, "check_only": False, "only": ""}
        chosen = dict(defaults, authoritative=True)
        self.assertEqual([], mm.authoritative_conflicts(
            chosen, defaults, {}, {"authoritative"}))

    def test_drift_during_the_run_is_a_status_not_a_warning(self):
        """A measurement whose repository moved underneath it stays true of the
        frozen snapshot and stops being evidence about the current checkout.
        Printing that as a NOTE while exiting 0 leaves a warning nothing reads,
        so it gets its own exit code and a CI gate can act on it."""
        self.assertEqual(0, mm.closure_exit([], [], [], True),
                         "clean and authoritative")
        self.assertEqual(3, mm.closure_exit([], [], ["canonical HEAD"], True),
                         "all killed, but not about the tree you are looking at")
        self.assertEqual(0, mm.closure_exit([], [], ["canonical HEAD"], False),
                         "drift only matters to an authoritative claim")

    def test_a_survivor_outranks_drift(self):
        """A landed fix with no executing test is the more serious finding, and
        exit 1 must not be masked by the drift code."""
        self.assertEqual(1, mm.closure_exit(["M1"], [], ["runner"], True))
        self.assertEqual(1, mm.closure_exit([], ["M2"], ["runner"], True))

    def test_an_authoritative_run_that_records_nothing_is_incomplete(self):
        """The record is the durable half of the evidence. A run that could not
        write it has a claim with nothing behind it, and it used to exit 0 with
        one printed line - the same "warning nothing reads" shape as the drift
        note. Reachable without malice: a PID reused at the same commit with the
        same selection collides under the exclusive create introduced to stop a
        partial run overwriting an authoritative one."""
        why = mm.unrecorded_run_is_fatal(True, OSError("File exists"))
        self.assertTrue(why)
        self.assertIn("no durable evidence", why)
        self.assertEqual(2, mm.closure_exit([], [], [], True, incomplete=why),
                         "an unrecorded authoritative run must not exit 0")
        self.assertIsNone(mm.unrecorded_run_is_fatal(False, OSError("x")),
                          "a partial run's record is not a closure artifact, so "
                          "failing to write it is not a measurement failure")

    def _require_clean_authoritative_preconditions(self):
        """--authoritative refuses a dirty tree AND a runner blob that differs
        from HEAD, and both also return 2. So a writer-failure test run under
        either would pass for the wrong reason - which it did, until this guard
        existed. Skip rather than assert into ambiguity.

        The skip NAMES the unmet precondition. A closure run must show 0 skips
        here: a critical orchestration test that vanishes into a skip is not a
        pass, and "environment unsuitable" would not say which one to fix."""
        unmet = []
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                               capture_output=True, text=True).stdout.strip()
        if dirty:
            unmet.append("working tree is dirty (%s%s)"
                         % (dirty.splitlines()[0].strip(),
                            ", +%d more" % (len(dirty.splitlines()) - 1)
                            if len(dirty.splitlines()) > 1 else ""))
        for rel in ("hooks/mutation_matrix.py", "hooks/mutations.json"):
            disk = subprocess.run(["git", "hash-object", rel], cwd=REPO,
                                  capture_output=True, text=True).stdout.strip()
            head = subprocess.run(["git", "rev-parse", "HEAD:" + rel], cwd=REPO,
                                  capture_output=True, text=True).stdout.strip()
            if not disk or disk != head:
                unmet.append("%s on disk differs from HEAD" % rel)
        if unmet:
            self.skipTest("exit 2 would not distinguish the writer failure from "
                          "the refusal, because: " + "; ".join(unmet))

    def test_main_ACTUALLY_consumes_a_record_write_failure(self):
        """The rule test above proves `unrecorded_run_is_fatal` is right. It
        does not prove main() asks it - a runner that forgot to thread the
        writer's failure into the rule would keep exiting 0 while every unit
        test stayed green. So this drives the real main() control flow and only
        stubs what makes it slow or environment-dependent.

        The stubs are deliberately narrow: the matrix is reduced to one entry,
        the suites are not executed, and the dirty gate is satisfied. Everything
        else - the authoritative gate, the worktree, the record path, the
        completeness accounting and the exit contract - is the shipped code."""
        self._require_clean_authoritative_preconditions()
        one = mm.load_matrix()[:1]
        original = (mm.load_matrix, mm.run_suite, mm.dirty_gate, mm.write_record)
        try:
            mm.load_matrix = lambda: one
            mm.run_suite = lambda script, cwd=None: False      # every mutant dies
            mm.dirty_gate = lambda dirty, allow, head: (True, [])
            mm.write_record = self._explode
            rc = mm.main(["--authoritative"])
        finally:
            (mm.load_matrix, mm.run_suite, mm.dirty_gate,
             mm.write_record) = original
        self.assertEqual(2, rc,
                         "an authoritative run whose evidence could not be "
                         "written must report an incomplete measurement, not "
                         "a clean pass")

    @staticmethod
    def _explode(path, payload):
        raise OSError(17, "File exists")

    def test_the_same_stub_run_passes_when_the_record_IS_written(self):
        """The two-sided half: with the writer working, the identical stubbed
        run exits 0. Without this, the test above would also pass if main()
        were broken in some unrelated way that always returned 2."""
        self._require_clean_authoritative_preconditions()
        one = mm.load_matrix()[:1]
        original = (mm.load_matrix, mm.run_suite, mm.dirty_gate)
        try:
            mm.load_matrix = lambda: one
            mm.run_suite = lambda script, cwd=None: False
            mm.dirty_gate = lambda dirty, allow, head: (True, [])
            rc = mm.main(["--authoritative"])
        finally:
            mm.load_matrix, mm.run_suite, mm.dirty_gate = original
        self.assertEqual(0, rc, "the same run must pass when evidence lands")

    def test_an_incomplete_run_outranks_a_survivor(self):
        """Exit 1 asserts that the full matrix ran and something lived. A run
        that stopped partway has not earned that sentence, whatever it managed
        to observe first - so a tool error or a short run reports 2, and the
        survivors it did see are printed rather than promoted."""
        self.assertEqual(2, mm.closure_exit(["M1"], [], ["runner"], True,
                                            incomplete="OSError: boom"))
        self.assertEqual(2, mm.closure_exit([], [], [], True,
                                            incomplete="only 12 of 55"))
        self.assertEqual(2, mm.closure_exit([], [], [], False,
                                            incomplete="only 12 of 55"),
                         "an unfinished measurement is unfinished whether or "
                         "not anyone called it authoritative")

    def test_the_per_mutant_record_survives_a_truncated_stdout(self):
        """Per-mutant verdicts used to exist only on stdout, and a pipeline as
        ordinary as `| tail -20` destroyed them - which is what happened to
        this branch's first two checkpoint runs, leaving only totals to
        compare. Totals cannot show that a mutant changed which suite killed
        it, which is the difference worth catching.

        The record is written to a file no pipe can reach, with no flag (an
        option would be a non-default input the authoritative gate refuses) and
        outside the repository (a file in the tree would dirty it, and the next
        authoritative run would refuse to start)."""
        with open(os.path.join(HOOKS, "mutation_matrix.py")) as _fh:
            src = _fh.read()
        self.assertIn("tempfile.gettempdir()", src,
                      "the record must land outside the repository")
        self.assertIn('"x"', src,
                      "the record must be opened exclusively: a later run "
                      "overwriting an earlier one is how a 55-row "
                      "authoritative record became a 1-row partial one")
        self.assertNotIn('add_argument("--record', src,
                         "a flag for it would be refused by --authoritative")
        r = subprocess.run([sys.executable,
                            os.path.join(HOOKS, "mutation_matrix.py"),
                            "--allow-dirty-head-only", "--only", "M18"],
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        path = [l.split(None, 2)[2].strip() for l in r.stdout.splitlines()
                if l.startswith("per-mutant record")]
        self.assertTrue(path, "the run must say where the record went")
        import json as _json
        with open(path[0]) as fh:
            rec = _json.load(fh)
        self.assertTrue(rec["subject_commit"])
        got = {m["id"]: m for m in rec["mutations"]}
        self.assertIn("M18", got)
        for field in ("desc", "path", "where", "suites_red", "verdict"):
            self.assertIn(field, got["M18"],
                          "a comparison needs %s, not just a verdict" % field)
        # A PARTIAL run must be unable to occupy a full run's evidence path,
        # and must say what it is. Keying the name on the commit alone let a
        # `--only M18` run from THIS test destroy a 55-row authoritative
        # record two minutes after the closure verifier had passed against it.
        self.assertRegex(path[0], r"-1of\d+-[0-9a-f]{12}\.json$",
                         "the path must encode the selection and a per-run "
                         "nonce - a pid is reused, so a leftover file would "
                         "make a legitimate later run fail for no reason")
        self.assertEqual(12, len(rec.get("run_id", "")),
                         "the record must carry the same run id the path does")
        self.assertNotEqual("authoritative", rec.get("mode"),
                            "a --only run is not authoritative")
        self.assertEqual(1, rec["measured"])
        self.assertGreater(rec["total_definitions"], 1,
                           "the record must say how many it did NOT measure")

    def test_no_measurement_input_escapes_the_authoritative_gate(self):
        """The gate compares the parsed namespace against argparse's defaults,
        which is sound only while every measurement-changing input IS a
        command-line option. An environment variable would sit outside that
        comparison entirely."""
        with open(os.path.join(HOOKS, "mutation_matrix.py")) as _fh:
            src = _fh.read()
        for token in ("os.environ", "os.getenv", "configparser", "tomllib"):
            self.assertNotIn(token, src,
                             "%s is an input the authoritative gate cannot "
                             "see; add it to the gate before adding it here"
                             % token)

    def test_the_mode_is_a_flag_and_not_only_a_docstring(self):
        r = self._run("--help")
        self.assertIn("--authoritative", r.stdout)
        self.assertIn("ENFORCED", r.stdout,
                      "the help must not describe a convention as a gate")


class TheRealMatrix(unittest.TestCase):
    """The shipped data file must satisfy the gate it declares."""

    def setUp(self):
        self.matrix = mm.load_matrix()

    def test_every_entry_is_unique_non_empty_and_where_it_claims(self):
        src = {}
        for _p in (mm.SS, mm.HK):
            with open(_p) as _fh:
                src[_p] = _fh.read()
        for name, path, old, new, expect, _eq in self.matrix:
            with self.subTest(mutation=name.split()[0]):
                self.assertIsNotNone(expect,
                                     "every entry must declare its landing "
                                     "function, or the check is unenforced")
                mm.check_mutation(src[path], old, new, expect)

    def test_mutation_ids_are_unique(self):
        ids = [m[0].split()[0] for m in self.matrix]
        dupes = {i for i in ids if ids.count(i) > 1}
        self.assertFalse(dupes, "duplicate ids make the report unreadable: %s"
                         % dupes)

    def test_check_only_mode_runs_no_suites_and_passes(self):
        r = subprocess.run([sys.executable,
                            os.path.join(HOOKS, "mutation_matrix.py"),
                            "--check-only"],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        self.assertIn("shape check", r.stdout)

    def test_a_mutation_changes_only_its_own_span(self):
        """A mutation must not perturb anything but the lines it targets - a
        second, accidental edit would make the suite's red mean something other
        than the property under test."""
        for name, path, old, new, _expect, _eq in self.matrix:
            with self.subTest(mutation=name.split()[0]):
                with open(path) as _fh:
                    src = _fh.read()
                mutated = src.replace(old, new, 1)
                i = src.find(old)
                self.assertEqual(src[:i], mutated[:i], "prefix must be intact")
                self.assertEqual(src[i + len(old):],
                                 mutated[i + len(new):], "suffix must be intact")

    def test_any_equivalent_mutant_states_its_boundary(self):
        """An unkillable mutant is only acceptable with an argument attached,
        and the argument must name the runtime it holds for - "unreachable"
        without a boundary is a claim beyond its evidence.

        The matrix currently declares NONE, and that is the point of this test
        rather than an accident of it. Two were declared equivalent on the
        strength of an argument; one of them (the dot guard's OSError branch)
        was simply WRONG - a deleted working directory reaches it, and the
        mutant made a deleted directory digest with exit 0. The other was
        replaced by a test that injects the failure instead of arguing it away.
        So this test enforces the bar for any future declaration and records
        that the bar was not met twice."""
        import json
        with open(os.path.join(HOOKS, "mutations.json")) as fh:
            data = json.load(fh)
        equivalents = [m for m in data["mutations"] if m.get("equivalent")]
        for m in equivalents:
            with self.subTest(mutation=m["id"]):
                why = m["equivalent"]
                self.assertIn("EQUIVALENT", why)
                self.assertRegex(why, r"CPython 3\.\d",
                                 "must bound the Python version")
                self.assertRegex(why, r"prob|probe|reached|exercis",
                                 "must cite a dynamic probe, not only a "
                                 "reading of the call graph - the reading is "
                                 "what was wrong last time")
                self.assertGreater(len(why), 200,
                                   "a one-line assertion is not an argument")


if __name__ == "__main__":
    unittest.main(verbosity=2)
