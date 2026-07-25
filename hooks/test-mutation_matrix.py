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


class TheRealMatrix(unittest.TestCase):
    """The shipped data file must satisfy the gate it declares."""

    def setUp(self):
        self.matrix = mm.load_matrix()

    def test_every_entry_is_unique_non_empty_and_where_it_claims(self):
        src = {mm.SS: open(mm.SS).read(), mm.HK: open(mm.HK).read()}
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
                src = open(path).read()
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
