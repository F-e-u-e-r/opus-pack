REVIEW TASK — a SHIPPED pull request to a rules pack. Review the material inlined
below directly. Do NOT run commands or read files; everything is here.

Your job is to find what is WRONG or UNSUPPORTED, in the rule text, in the trail
document, in the PR body's claims, and in the harness script. Report NOT CONFIRMED
for anything you cannot derive from the material below.

## Context
Repo: a portable "skills pack" whose rule files later AI sessions obey as doctrine.
File changed: skills/operational-rigor/SKILL.md §2 (third-party install gate).
The limb being amended landed 3 days ago and says: a source review clears
executable BEHAVIOR only when the runtime-selected bytes are bound to what was
reviewed. It offers clearance paths (a)/(b)/(c). This PR amends ONLY path (a).

HOUSE RULE binding this PR: pack text must stay portable. One person's machine
paths, OS, vendor builds, or tool lineup must NOT appear in rule text; such
specifics belong in the review trail.

## PRIOR ROUND (dedup context only — NOT authority; current evidence overrides it)
One earlier review by a sibling model of the same family returned FIX with three
findings, all since fixed: (1) an over-claim that the digest confirmation makes
EVERY incomplete removal detectable; (2) an unevidenced "central cache"
generalization; (3) a redundant rationale clause. Do not assume those fixes are
correct — re-judge the shipped text. Re-raising something is fine if the current
text still has it.

## 1. THE SHIPPED DIFF
diff --git a/skills/operational-rigor/SKILL.md b/skills/operational-rigor/SKILL.md
index 710a090..ed94ef7 100644
--- a/skills/operational-rigor/SKILL.md
+++ b/skills/operational-rigor/SKILL.md
@@ -415,9 +415,16 @@ When rigor conflicts with finishing sooner, rigor wins.
   runtime-selected bytes are themselves reviewed, or an independent path
   establishes those *exact* bytes were produced from the reviewed source
   under a named build/compile recipe. Legitimate clearance: (a) remove any
-  competing shipped or cached artifact, regenerate from the exact reviewed
-  source under a named toolchain/recipe, and confirm the bytes the runtime
-  then selects match the regenerated artifact by digest; (b) bind the
+  competing shipped or cached artifact — LOCATE it rather than assume its
+  conventional in-tree path, because a runtime may use an out-of-tree
+  cache (path-mirrored, or under a per-user cache root), and deleting the
+  in-tree one then silently no-ops, leaving a visibly clean tree that
+  still executes stale bytes — regenerate from the exact reviewed source
+  under a named toolchain/recipe, and confirm the bytes the runtime then
+  selects match the regenerated artifact by digest; for this failure mode
+  that confirmation is what exposes the failed removal, so run it against
+  the bytes the runtime actually selects, never against the tree's
+  appearance; (b) bind the
   exact artifact bytes by digest to the reviewed source + recipe via
   reproducible/attested build evidence; or (c) review the runtime-selected
   artifact itself, when it is reviewable as source-equivalent, as the

## 2. THE TRAIL DOCUMENT (reviews/2026-08-31-out-of-tree-cache-removal/README.md)
# Out-of-tree bytecode cache defeats the in-tree removal (op-rigor §2, path (a))

Amends ONE clearance path of the runtime-selected-artifact correspondence limb
landed by #230. Not a correction — the limb is sound, and its digest step already
catches the case below. The patch makes the *removal* half self-aware, because a
reviewer who performs it the conventional way can believe it succeeded when it
did nothing.

## What was probed

`harness/pycache_prefix_probe.py`, self-contained, prints its own verdict and
reports "not reproduced" on interpreters that do not set a cache prefix.
Captured run: `harness/result-macos-cltools-3.9.6.txt`.

Environment binding for that capture: macOS 26.6.2 arm64, `/usr/bin/python3` =
CPython 3.9.6 as shipped by Apple CommandLineTools.

1. That interpreter reports `sys.pycache_prefix` set to a per-user, path-mirrored
   cache root by default. Bytecode never lands in `__pycache__` beside the source.
   - `python3 -S -c` prints the same value, so it is not site configuration.
   - `python3 -E -S -c` prints `None`.
   - No `PYTHON*` variable exists in the parent shell or the child's `os.environ`,
     and a full env diff between the normal and `-E` child shows zero differing
     keys. **The mechanism was NOT established** — only the observed effect is
     claimed here.
2. End to end: compile an `UNCHECKED_HASH` `.pyc` for a module returning `OLD`,
   rewrite the source to return something of a different length, `rm -rf
   __pycache__`, confirm `find . -name '*.pyc'` returns nothing — and the import
   still prints `OLD`.

## Review

One round, one reviewer: codex `gpt-5.6-luna`, read-only, self-contained inlined
packet (`packets/packet-r1.md`), verdict `verdicts/r1-luna.md`. **FIX**, three
findings, all reproduced by derivation from the packet's own evidence and all
fixed. Single-lens: this did not get a second model family, which is a recorded
gap, not a claimed dual gate.

| Finding | Disposition |
|---|---|
| **High, over-claim.** "that digest confirmation is what makes an incomplete removal detectable" is not true of every incomplete removal — a byte-identical leftover leaves nothing to detect. | fixed; scoped to "for this failure mode" |
| **Medium, generalization.** "a central or path-mirrored cache directory, a per-user cache root" — the evidence establishes one cache that is both path-mirrored and per-user; "central" is unevidenced. | fixed; narrowed to "path-mirrored, or under a per-user cache root" |
| **Low, redundancy.** The rationale clause added no clearance condition the landed digest step lacked. | fixed by conversion, not deletion: the clause now carries an operational constraint (run the digest against the bytes the runtime actually selects, not against the tree's appearance) — which also closes the second mechanism named in the High finding |

Remedies were authored here, not pasted: the reviewer's proposed wording for the
Low finding deleted the clause outright, which would have dropped the
actually-selected-bytes constraint that the High finding's own mechanism argues
for.

An earlier draft named the vendor, the OS and a `~/Library/...` path inside the
rule text. That was removed before review as a portability violation; the machine
specifics live in this trail instead. The reviewer independently confirmed no
scope violation remained.

## What would change the conclusion

- An interpreter or runtime where the conventional in-tree removal is always
  sufficient would not falsify the "may" — but a demonstration that no mainstream
  runtime caches out of tree would make the clause dead weight.
- The capture is one interpreter on one OS. The probe is written to be run
  elsewhere; more captures would widen the evidence base.

## 3. THE HARNESS SCRIPT the trail and PR body offer as the reproducible check
#!/usr/bin/env python3
"""Probe: an out-of-tree bytecode cache defeats the conventional in-tree removal.

Run:  python3 pycache_prefix_probe.py
Reports the interpreter's sys.pycache_prefix, then demonstrates that deleting
__pycache__ can leave a visibly clean tree that still executes stale bytecode.
Exits 0 with VERDICT: on the last line.
"""
import os, sys, shutil, subprocess, tempfile, py_compile

def main():
    print("interpreter :", sys.executable, sys.version.split()[0])
    print("pycache_prefix:", repr(sys.pycache_prefix))
    d = tempfile.mkdtemp(prefix="pycprobe-")
    os.chdir(d)
    cache = os.path.join(sys.pycache_prefix, os.getcwd().lstrip("/")) if sys.pycache_prefix else "__pycache__"

    def write(payload):
        open("m.py", "w").write('def v():\n    return "%s"\n' % payload)

    shutil.rmtree(cache, ignore_errors=True)
    write("OLD")
    py_compile.compile("m.py", invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
    write("NEW_AND_A_DIFFERENT_LENGTH")

    shutil.rmtree("__pycache__", ignore_errors=True)          # the conventional clean
    in_tree = [p for _, _, fs in os.walk(".") for p in fs if p.endswith(".pyc")]
    got = subprocess.run([sys.executable, "-c", "import m; print(m.v())"],
                         capture_output=True, text=True, cwd=d).stdout.strip()

    print("source on disk :", open("m.py").read().split('"')[1])
    print("in-tree .pyc   :", len(in_tree))
    print("executed       :", got)
    shutil.rmtree(d, ignore_errors=True)
    print("VERDICT:", "REPRODUCED (stale bytes ran from an out-of-tree cache)"
          if got == "OLD" and not in_tree else "not reproduced on this interpreter")

main()

## 4. ITS CAPTURED RUN (checked into the trail)
interpreter : /Library/Developer/CommandLineTools/usr/bin/python3 3.9.6
pycache_prefix: '<HOME>/Library/Caches/com.apple.python'
source on disk : NEW_AND_A_DIFFERENT_LENGTH
in-tree .pyc   : 0
executed       : OLD
VERDICT: REPRODUCED (stale bytes ran from an out-of-tree cache)

## 5. LOAD-BEARING CLAIMS THE PR BODY MAKES TO THE MAINTAINER
 C1 "Not a correction — the limb is sound, and its digest step already catches
     the case below."
 C2 "a runtime may cache out of tree, so deleting the conventional in-tree cache
     directory can silently no-op and leave a visibly clean tree that still
     executes stale bytes"
 C3 "The mechanism that sets it was NOT established — only the observed effect
     is claimed."
 C4 "self-contained, prints its own verdict, and reports 'not reproduced' on
     interpreters without a cache prefix, so it is runnable as a check elsewhere"
 C5 "One paragraph, no new clearance condition, no change to (b) or (c)."
 C6 "Remedies were authored here, not pasted."

## WHAT TO CHECK
A. Is the amended path (a) TRUE as written, and does it survive its own examples?
B. Does the harness script actually demonstrate what claims C2/C4 say it does?
   Walk its control flow. Would it behave as claimed on an interpreter with NO
   cache prefix? Is its VERDICT line derivable from what it measured? Does its
   use of UNCHECKED_HASH confound the result it reports?
C. Is the trail README accurate about its own evidence, including what it admits
   it did NOT establish?
D. Any remaining machine/OS/vendor specifics smuggled into the RULE text?
E. Does the insertion break the (a)/(b)/(c) structure or change what (a) requires?
F. Is anything in C1-C6 over-claimed relative to the material above?

## COST ASYMMETRY
The expensive failure is a false or over-broad empirical claim landing in doctrine
that later sessions obey without re-deriving it, or a harness that appears to
prove something it does not. A pedantic nit costs nothing. Probe the over-claim
and the harness-validity sides hardest.

## REPORTING FORMAT
Severity-ranked findings: LOCATION (quote it) + MECHANISM (why wrong/unsupported)
+ CONCRETE FIX (minimal wording). Tag each claim [verified: how] / [unverified].
State explicitly where you checked and found nothing. Report uncertainty honestly
rather than manufacturing findings.
LAST LINE exactly: PROCEED   or   FIX <comma-separated list>
