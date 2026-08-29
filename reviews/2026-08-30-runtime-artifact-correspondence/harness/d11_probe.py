#!/usr/bin/env python3
# D11: reproduce sol's r2 claim about --check-hash-based-pycs policy.
# Predictions (expected-before-actual):
#   unchecked-mismatch @ default -> PAYLOAD (hash field NOT compared)
#   unchecked-mismatch @ always  -> DECOY   (compared -> mismatch -> recompile)
#   checked-mismatch   @ default -> DECOY   (compared -> mismatch -> recompile)
#   checked-mismatch   @ never   -> PAYLOAD (comparison disabled)
import sys, os, struct, marshal, importlib, importlib.util, subprocess, json

MAGIC = importlib.util.MAGIC_NUMBER
PYC = sys.pycache_prefix  # this process launched with -X pycache_prefix=<PYC>


def hash_pyc(code, src_hash, checked):
    flags = 1 | (2 if checked else 0)
    return MAGIC + struct.pack('<I', flags) + src_hash + marshal.dumps(code)


def setup(d, modname, checked):
    os.makedirs(d, exist_ok=True)
    sentinel = os.path.join(d, 'RAN')
    modpy = os.path.join(d, modname + '.py')
    decoy = "MARKER = 'DECOY'\n"
    with open(modpy, 'w') as f:
        f.write(decoy)
    payload = compile("MARKER = 'PAYLOAD'\nopen(%r, 'w').write('x')\n" % sentinel, modpy, 'exec')
    wrong = importlib.util.source_hash(b"not the decoy source\n")   # MISMATCHED header hash
    pyc = hash_pyc(payload, wrong, checked=checked)
    cache = importlib.util.cache_from_source(modpy)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    return sentinel, cache, pyc, modname


def run(d, modname, sentinel, cache, pyc, extra):
    # restore the forged pyc and clear sentinel before each run
    if os.path.exists(sentinel):
        os.remove(sentinel)
    with open(cache, 'wb') as f:
        f.write(pyc)
    runner = "import %s,sys; sys.stdout.write(%s.MARKER)" % (modname, modname)
    args = [sys.executable] + extra + ['-X', 'pycache_prefix=' + PYC, '-c', runner]
    p = subprocess.run(args, cwd=d, capture_output=True, text=True)
    return {'marker': p.stdout.strip(), 'payload_ran': os.path.exists(sentinel), 'rc': p.returncode,
            'stderr_tail': p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ''}


base = sys.argv[1]
du = os.path.join(base, 'D11u')
s, c, pyc, mn = setup(du, 'd11u', checked=False)
unchecked_default = run(du, mn, s, c, pyc, [])
unchecked_always = run(du, mn, s, c, pyc, ['--check-hash-based-pycs', 'always'])

dc = os.path.join(base, 'D11c')
s2, c2, pyc2, mn2 = setup(dc, 'd11c', checked=True)
checked_default = run(dc, mn2, s2, c2, pyc2, [])
checked_never = run(dc, mn2, s2, c2, pyc2, ['--check-hash-based-pycs', 'never'])

result = {
    'py': sys.version.split()[0],
    'unchecked_mismatch_default': unchecked_default,   # expect PAYLOAD/True
    'unchecked_mismatch_always': unchecked_always,     # expect DECOY/False
    'checked_mismatch_default': checked_default,        # expect DECOY/False
    'checked_mismatch_never': checked_never,            # expect PAYLOAD/True
}
exp = (unchecked_default['marker'] == 'PAYLOAD' and unchecked_always['marker'] == 'DECOY'
       and checked_default['marker'] == 'DECOY' and checked_never['marker'] == 'PAYLOAD')
result['ALL_MATCH_PREDICTION'] = exp
print(json.dumps(result, indent=2))
