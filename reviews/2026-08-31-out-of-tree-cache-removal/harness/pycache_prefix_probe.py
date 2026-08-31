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
