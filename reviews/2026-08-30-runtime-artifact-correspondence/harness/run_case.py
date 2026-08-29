#!/usr/bin/env python3
# D1-D10 first-hand mechanical controls for the
# reviewed-source  <->  runtime-selected-executable-artifact  correspondence gap (L2).
#
# Each case sets up a divergent-or-clean on-disk state, drives the real CPython import
# machinery, and reports first-hand observations as one JSON line on stdout.
# Invoked (one fresh subprocess per case) as:
#     python3 -X pycache_prefix=<PYCACHE> run_case.py <CASE> <WORKDIR>
import sys, os, json, struct, marshal, importlib, importlib.util, hashlib, py_compile, traceback

MAGIC = importlib.util.MAGIC_NUMBER  # 4 bytes, this interpreter's bytecode magic


def sh(b):
    # The exact 8-byte source hash CPython embeds in / validates hash-based pycs against.
    return importlib.util.source_hash(b)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def hash_pyc(code, src_hash, checked):
    # PEP 552 hash-based pyc: magic(4) + flags(4) + source_hash(8) + marshal(code)
    # flags bit0 = hash-based(1); bit1 = check_source(1=CHECKED,0=UNCHECKED)
    assert len(MAGIC) == 4 and len(src_hash) == 8
    flags = 1 | (2 if checked else 0)
    return MAGIC + struct.pack('<I', flags) + src_hash + marshal.dumps(code)


def ts_pyc(code, mtime, size):
    # Timestamp-based pyc: magic(4) + flags(4)=0 + mtime(4) + size(4) + marshal(code)
    return (MAGIC + struct.pack('<I', 0)
            + struct.pack('<II', mtime & 0xFFFFFFFF, size & 0xFFFFFFFF)
            + marshal.dumps(code))


def wr(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data if isinstance(data, (bytes, bytearray)) else data.encode())


def imp(modname, dirpath):
    sys.path.insert(0, dirpath)
    importlib.invalidate_caches()
    sys.modules.pop(modname, None)
    return importlib.import_module(modname)


def payload_src(sentinel, marker="PAYLOAD", gated=False):
    # Stands in for malicious executable content: a top-level side effect (write a
    # sentinel file) plus an observable MARKER. `gated` hides the side effect behind
    # an env trigger (activation-gated payload, the (2) axis).
    if gated:
        return ("import os\n"
                f"MARKER = {marker!r}\n"
                f"if os.environ.get('SECRET_TRIGGER') == '1':\n"
                f"    open({sentinel!r}, 'w').write('x')\n")
    return (f"MARKER = {marker!r}\n"
            f"open({sentinel!r}, 'w').write('x')\n")


def run(case, base):
    d = os.path.join(base, case)
    os.makedirs(d, exist_ok=True)
    sentinel = os.path.join(d, 'PAYLOAD_RAN')
    o = {'case': case, 'py': sys.version.split()[0], 'cache_tag': sys.implementation.cache_tag,
         'pycache_prefix': sys.pycache_prefix}

    if case == 'D1':  # UNCHECKED-DECOY  -> HIT
        modpy = os.path.join(d, 'd1mod.py'); decoy = "MARKER = 'DECOY'\n"; wr(modpy, decoy)
        code = compile(payload_src(sentinel), modpy, 'exec')
        pyc = hash_pyc(code, sh(decoy.encode()), checked=False)
        cache = importlib.util.cache_from_source(modpy); wr(cache, pyc)
        m = imp('d1mod', d)
        o.update(source_reviewer_sees=decoy.strip(), executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='hash/unchecked', cache=cache)

    elif case == 'D2':  # FORGED-CHECKED-HASH -> HIT while source-freshness check PASSES
        modpy = os.path.join(d, 'd2mod.py'); decoy = "MARKER = 'DECOY'\n"; wr(modpy, decoy)
        code = compile(payload_src(sentinel), modpy, 'exec')
        src_hash = sh(decoy.encode())                       # hash of the CLEAN decoy
        pyc = hash_pyc(code, src_hash, checked=True)        # checked; header=hash(decoy); body=PAYLOAD
        cache = importlib.util.cache_from_source(modpy); wr(cache, pyc)
        m = imp('d2mod', d)
        with open(modpy, 'rb') as f:
            on_disk = f.read()
        # Recompute, first-hand, the exact input the runtime's own validator compares:
        freshness_passes = (importlib.util.source_hash(on_disk) == pyc[8:16])
        o.update(source_reviewer_sees=decoy.strip(), executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='hash/checked',
                 header_source_hash=pyc[8:16].hex(),
                 recomputed_source_hash=importlib.util.source_hash(on_disk).hex(),
                 checked_hash_freshness_passes=freshness_passes, cache=cache)

    elif case == 'D3':  # CHECKED-HASH-MISMATCH -> runtime invalidates & recompiles -> DECOY
        modpy = os.path.join(d, 'd3mod.py'); decoy = "MARKER = 'DECOY'\n"; wr(modpy, decoy)
        code = compile(payload_src(sentinel), modpy, 'exec')
        wrong = sh(b"unrelated source that is not the decoy\n")
        pyc = hash_pyc(code, wrong, checked=True)
        cache = importlib.util.cache_from_source(modpy); wr(cache, pyc)
        m = imp('d3mod', d)
        with open(modpy, 'rb') as f:
            on_disk = f.read()
        o.update(source_reviewer_sees=decoy.strip(), executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='hash/checked-mismatch',
                 header_source_hash=pyc[8:16].hex(),
                 recomputed_source_hash=importlib.util.source_hash(on_disk).hex(),
                 header_matches_source=(importlib.util.source_hash(on_disk) == pyc[8:16]), cache=cache)

    elif case == 'D4':  # TIMESTAMP-COLLISION -> HIT (metadata forged, not correspondence)
        modpy = os.path.join(d, 'd4mod.py'); decoy = "MARKER = 'DECOY'\n"; wr(modpy, decoy)
        st = os.stat(modpy); mtime = int(st.st_mtime); size = st.st_size
        code = compile(payload_src(sentinel), modpy, 'exec')
        pyc = ts_pyc(code, mtime, size)
        cache = importlib.util.cache_from_source(modpy); wr(cache, pyc)
        m = imp('d4mod', d)
        o.update(source_reviewer_sees=decoy.strip(), executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='timestamp',
                 forged_mtime=mtime, forged_size=size, cache=cache,
                 caveat='mtime integer-second granularity is FS/ENV-sensitive; forged deterministically here')

    elif case == 'D5':  # SOURCELESS -> HIT
        pycpath = os.path.join(d, 'd5mod.pyc')
        code = compile(payload_src(sentinel), 'd5mod.pyc', 'exec')
        pyc = hash_pyc(code, b'\x00' * 8, checked=False)   # no source to validate against
        wr(pycpath, pyc)
        m = imp('d5mod', d)
        o.update(source_reviewer_sees='(no .py present — bare d5mod.pyc)', executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='sourceless', cache=pycpath)

    elif case == 'D6':  # SOURCE-ONLY -> CLEAR (rule must not degrade to "Python is dangerous")
        modpy = os.path.join(d, 'd6mod.py'); clean = "MARKER = 'CLEAN'\n"; wr(modpy, clean)
        m = imp('d6mod', d)
        o.update(source_reviewer_sees=clean.strip(), executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='none (compiled from source)')

    elif case == 'D7':  # LOCAL-REBUILD -> CLEAR after remediation
        modpy = os.path.join(d, 'd7mod.py'); decoy = "MARKER = 'DECOY'\n"; wr(modpy, decoy)
        code = compile(payload_src(sentinel), modpy, 'exec')
        forged = hash_pyc(code, sh(decoy.encode()), checked=True)
        cache = importlib.util.cache_from_source(modpy); wr(cache, forged)
        forged_digest = sha(forged)
        # Remediation: remove shipped artifact, regenerate from the exact reviewed source,
        # then verify the runtime selects the regenerated artifact.
        os.remove(cache)
        py_compile.compile(modpy, invalidation_mode=py_compile.PycInvalidationMode.CHECKED_HASH)
        with open(cache, 'rb') as f:
            regen = f.read()
        m = imp('d7mod', d)
        honest = hash_pyc(compile(decoy, modpy, 'exec'), sh(decoy.encode()), True)
        o.update(source_reviewer_sees=decoy.strip(), executed_marker=m.MARKER,
                 payload_ran=os.path.exists(sentinel), pyc_flavor='hash/checked (regenerated)',
                 forged_digest=forged_digest, regen_digest=sha(regen), honest_digest=sha(honest),
                 regen_corresponds_to_source=(sha(regen) == sha(honest)), cache=cache)

    elif case == 'D8':  # VERIFIED-BUILD-PROVENANCE -> CLEAR(good) / finding(forge) by reproduction digest
        name = 'd8mod.py'; decoy = "MARKER = 'DECOY'\n"; sentb = os.path.join(d, 'RAN')
        honest = hash_pyc(compile(decoy, name, 'exec'), sh(decoy.encode()), True)
        shipped_good = hash_pyc(compile(decoy, name, 'exec'), sh(decoy.encode()), True)
        shipped_forge = hash_pyc(compile(payload_src(sentb), name, 'exec'), sh(decoy.encode()), True)
        o.update(pyc_flavor='provenance-by-reproduction',
                 honest_digest=sha(honest), good_digest=sha(shipped_good), forge_digest=sha(shipped_forge),
                 good_matches_reproduction=(sha(shipped_good) == sha(honest)),
                 forge_matches_reproduction=(sha(shipped_forge) == sha(honest)),
                 note='a "generated" metadata claim alone cannot separate good from forge; only the reproduction digest does')

    elif case == 'D9':  # DIGEST-IDENTITY control
        modpy = os.path.join(d, 'd9mod.py'); decoy = "MARKER = 'DECOY'\n"; wr(modpy, decoy)
        code = compile(payload_src(sentinel), modpy, 'exec')
        pyc = hash_pyc(code, sh(decoy.encode()), checked=True)
        incache = os.path.join(d, '__pycache__', 'd9mod.' + sys.implementation.cache_tag + '.pyc')
        wr(incache, pyc)

        def tree_digest():
            h = hashlib.sha256()
            for root, _, files in os.walk(d):
                for fn in sorted(files):
                    p = os.path.join(root, fn)
                    with open(p, 'rb') as f:
                        b = f.read()
                    h.update(os.path.relpath(p, d).encode()); h.update(b)
            return h.hexdigest()

        d1d = tree_digest(); d2d = tree_digest()
        with open(incache, 'rb') as f:
            pb = bytearray(f.read())
        pb[-1] ^= 1
        with open(incache, 'wb') as f:
            f.write(bytes(pb))
        d3d = tree_digest()
        o.update(pyc_flavor='divergent tree (clean source + payload pyc in __pycache__)',
                 digest_stable=(d1d == d2d), digest_changes_on_byteflip=(d3d != d1d),
                 divergence_present=True, anomalies=[],
                 note='stable, non-anomalous whole-tree digest over a source/pyc-divergent tree: identity, not correspondence')

    elif case == 'D10':  # ACTIVATION-CROSS: (5) artifact-correspondence _|_ (2) activation-gated
        # (a) pure-(5): decoy source + UNGATED payload pyc  -> executed diverges, source has no gate
        da = os.path.join(d, 'a'); os.makedirs(da, exist_ok=True); sa = os.path.join(da, 'RAN')
        ap = os.path.join(da, 'd10a.py'); adecoy = "MARKER = 'DECOY'\n"; wr(ap, adecoy)
        wr(importlib.util.cache_from_source(ap),
           hash_pyc(compile(payload_src(sa), ap, 'exec'), sh(adecoy.encode()), True))
        ma = imp('d10a', da)
        a = {'executed_diverges_from_source': (ma.MARKER != 'DECOY'),
             'source_contains_gate': ('SECRET_TRIGGER' in adecoy)}
        # (b) pure-(2): clean source WITH a dormant gate, source-only (no pyc divergence)
        db = os.path.join(d, 'b'); os.makedirs(db, exist_ok=True); sb = os.path.join(db, 'RAN')
        bp = os.path.join(db, 'd10b.py'); bsrc = payload_src(sb, marker='CLEAN', gated=True); wr(bp, bsrc)
        mb = imp('d10b', db)
        b = {'executed_diverges_from_source': (mb.MARKER != 'CLEAN'),
             'source_contains_gate': ('SECRET_TRIGGER' in bsrc),
             'gate_dormant_ran': os.path.exists(sb)}
        # (c) co-fire: decoy source + GATED payload pyc -> executed diverges AND carries a gate
        dc = os.path.join(d, 'c'); os.makedirs(dc, exist_ok=True); sc = os.path.join(dc, 'RAN')
        cp = os.path.join(dc, 'd10c.py'); cdecoy = "MARKER = 'DECOY'\n"; wr(cp, cdecoy)
        wr(importlib.util.cache_from_source(cp),
           hash_pyc(compile(payload_src(sc, gated=True), cp, 'exec'), sh(cdecoy.encode()), True))
        mc = imp('d10c', dc)
        c = {'executed_diverges_from_source': (mc.MARKER != 'DECOY'),
             'executed_contains_gate': True,
             'source_contains_gate': ('SECRET_TRIGGER' in cdecoy)}
        o.update(pyc_flavor='orthogonality fixtures', a_pure5=a, b_pure2=b, c_cofire=c)

    else:
        o['error'] = 'unknown case ' + case
    return o


if __name__ == '__main__':
    case = sys.argv[1]; base = sys.argv[2]
    try:
        print(json.dumps(run(case, base)))
    except Exception as e:
        print(json.dumps({'case': case, 'error': repr(e), 'tb': traceback.format_exc()}))
