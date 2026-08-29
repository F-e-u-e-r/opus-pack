#!/usr/bin/env python3
# Orchestrates D1-D10 first-hand. Expectations are pre-registered (expected-before-actual);
# each case runs in a fresh subprocess with an isolated, self-contained pycache prefix.
import subprocess, sys, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PYCACHE = os.path.join(HERE, 'pyc')
WORK = os.path.join(HERE, 'work')
PY = sys.executable

# (label, predicate over the case's observed JSON) -- written BEFORE running.
EXPECTED = {
    'D1':  ('HIT (unchecked)',      lambda o: o.get('executed_marker') == 'PAYLOAD' and o.get('payload_ran') is True),
    'D2':  ('HIT + freshness PASS', lambda o: o.get('executed_marker') == 'PAYLOAD' and o.get('payload_ran') is True
                                              and o.get('checked_hash_freshness_passes') is True),
    'D3':  ('RECOMPILE -> DECOY',   lambda o: o.get('executed_marker') == 'DECOY' and o.get('payload_ran') is False
                                              and o.get('header_matches_source') is False),
    'D4':  ('HIT (ts collision)',   lambda o: o.get('executed_marker') == 'PAYLOAD' and o.get('payload_ran') is True),
    'D5':  ('HIT (sourceless)',     lambda o: o.get('executed_marker') == 'PAYLOAD' and o.get('payload_ran') is True),
    'D6':  ('CLEAR (source-only)',  lambda o: o.get('executed_marker') == 'CLEAN' and o.get('payload_ran') is False),
    'D7':  ('CLEAR (rebuild)',      lambda o: o.get('executed_marker') == 'DECOY' and o.get('payload_ran') is False
                                              and o.get('regen_corresponds_to_source') is True),
    'D8':  ('CLEAR/finding split',  lambda o: o.get('good_matches_reproduction') is True
                                              and o.get('forge_matches_reproduction') is False),
    'D9':  ('CONTROL (identity)',   lambda o: o.get('digest_stable') is True and o.get('digest_changes_on_byteflip') is True
                                              and o.get('divergence_present') is True),
    'D10': ('ORTHOGONAL 5 _|_ 2',   lambda o: (o['a_pure5']['executed_diverges_from_source'] and not o['a_pure5']['source_contains_gate']
                                               and not o['b_pure2']['executed_diverges_from_source'] and o['b_pure2']['source_contains_gate']
                                               and o['c_cofire']['executed_diverges_from_source'] and o['c_cofire']['executed_contains_gate'])),
}


def probe0():
    code = ("import sys,importlib.util,json;"
            "print(json.dumps({'py':sys.version.split()[0],'tag':sys.implementation.cache_tag,"
            "'magic':importlib.util.MAGIC_NUMBER.hex(),'pycache_prefix':sys.pycache_prefix,"
            "'has_source_hash':hasattr(importlib.util,'source_hash'),"
            "'sample_cache':importlib.util.cache_from_source('/x/y/mod.py')}))")
    p = subprocess.run([PY, '-X', 'pycache_prefix=' + PYCACHE, '-c', code], capture_output=True, text=True)
    return json.loads(p.stdout.strip())


def main():
    os.makedirs(WORK, exist_ok=True)
    pr = probe0()
    print('probe0:', json.dumps(pr))
    if not pr['py'].startswith('3.9.6'):
        print('ABORT: interpreter is not CPython 3.9.6'); return 2
    if not pr['has_source_hash']:
        print('ABORT: importlib.util.source_hash missing'); return 2
    if pr['pycache_prefix'] != PYCACHE:
        print('ABORT: pycache_prefix not honored:', pr['pycache_prefix']); return 2
    print()

    results = {}; allpass = True
    for case in ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10']:
        p = subprocess.run([PY, '-X', 'pycache_prefix=' + PYCACHE, os.path.join(HERE, 'run_case.py'), case, WORK],
                           capture_output=True, text=True)
        try:
            o = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception as e:
            o = {'case': case, 'error': 'parse fail: ' + repr(e), 'stdout': p.stdout, 'stderr': p.stderr}
        label, pred = EXPECTED[case]
        try:
            ok = bool(pred(o)) and 'error' not in o
        except Exception as e:
            ok = False; o.setdefault('pred_error', repr(e))
        allpass = allpass and ok
        results[case] = {'expect': label, 'pass': ok, 'obs': o}
        print('%-4s expect=%-22s %s' % (case, label, 'PASS' if ok else 'FAIL'))
        if not ok:
            print('     ', json.dumps(o)[:1000])

    with open(os.path.join(HERE, 'results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    seen = sorted({results[c]['obs'].get('py') for c in results if 'py' in results[c]['obs']})
    print('\ninterpreter(s) observed:', seen)
    print('OVERALL:', 'ALL PASS' if allpass else 'FAIL')
    print('D2 (critical, forged-checked-hash):',
          'REPRODUCED' if results['D2']['pass'] else 'NOT REPRODUCED -> STOP')
    return 0 if allpass else 1


if __name__ == '__main__':
    sys.exit(main())
