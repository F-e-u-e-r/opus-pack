#!/usr/bin/env python3
"""Probe: an out-of-tree bytecode cache defeats the conventional in-tree removal.

Run:  python3 pycache_prefix_probe.py

Two conditions must BOTH hold for stale bytes to execute, and this probe reports
them separately:
  1. the cached artifact lives outside the source tree, so deleting the in-tree
     cache directory does not remove it; and
  2. that artifact is still runtime-eligible despite the changed source (here,
     forced with UNCHECKED_HASH; in the wild, a forged header or an unchanged
     source does the same).
Out-of-tree placement alone is not sufficient: a timestamp-validated artifact
would be rejected once the source changed.

Everything load-bearing is MEASURED, not inferred: the prefix and the compile
come from the same interpreter that performs the import, and the artifact the
runtime actually selected is read back from the imported module's __cached__.
"""
import os, subprocess, sys, shutil, tempfile

def child(code, cwd=None):
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def main():
    # The prefix that matters belongs to the interpreter performing the IMPORT,
    # not to this parent process — flags such as -E can make the two disagree.
    rc, prefix, err = child("import sys; print(getattr(sys, 'pycache_prefix', None) or '')")
    if rc != 0:
        print("could not query the child interpreter:", err); print("VERDICT: inconclusive"); return
    print("interpreter   :", sys.executable, sys.version.split()[0])
    print("child prefix  :", prefix or "(unset)")

    # realpath matters: the cache mirrors the RESOLVED path (/var -> /private/var)
    d = os.path.realpath(tempfile.mkdtemp(prefix="pycprobe-"))
    try:
        def write(payload):
            open(os.path.join(d, "m.py"), "w").write('def v():\n    return "%s"\n' % payload)

        write("OLD")
        rc, compiled, err = child(
            "import py_compile as p; print(p.compile('m.py', "
            "invalidation_mode=p.PycInvalidationMode.UNCHECKED_HASH))", cwd=d)
        if rc != 0 or not compiled or not os.path.exists(compiled):
            print("compile failed:", err or compiled); print("VERDICT: inconclusive"); return
        outside = not compiled.startswith(d + os.sep)
        print("compiled to   :", "outside the tree" if outside else "inside the tree")

        write("NEW_AND_A_DIFFERENT_LENGTH")
        shutil.rmtree(os.path.join(d, "__pycache__"), ignore_errors=True)  # conventional clean
        survived = os.path.exists(compiled)
        in_tree = [f for _, _, fs in os.walk(d) for f in fs if f.endswith(".pyc")]

        rc, out, err = child("import m; print(m.v()); print(m.__cached__)", cwd=d)
        if rc != 0:
            print("import failed:", err); print("VERDICT: inconclusive"); return
        executed, selected = (out.splitlines() + ["", ""])[:2]

        print("source on disk:", open(os.path.join(d, "m.py")).read().split('"')[1])
        print("in-tree .pyc  :", len(in_tree))
        print("survived clean:", survived)
        print("executed      :", executed)
        print("runtime chose :", selected)
        proved = (executed == "OLD" and outside and survived and not in_tree
                  and os.path.realpath(selected) == os.path.realpath(compiled))
        print("VERDICT:", "REPRODUCED (the out-of-tree artifact survived the in-tree "
                          "removal, the runtime selected it, and its stale bytes ran)"
              if proved else "not reproduced on this interpreter")
    finally:
        shutil.rmtree(d, ignore_errors=True)

main()
