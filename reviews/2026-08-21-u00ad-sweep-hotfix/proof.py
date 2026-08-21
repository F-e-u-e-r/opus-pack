#!/usr/bin/env python3
"""Two-sided proof engine for the U+00AD sweep hotfix (issue: mining-intake
2026-08-21 item 7). ASCII-only source: every non-ASCII character under test
is constructed via chr(); no literal invisible or non-ASCII characters
appear in this file (self-checked at import).

Modes:
  python3 proof.py baseline <rev>   # expect 145-set x3, set-equal, U+00AD ABSENT
  python3 proof.py post <base-rev>  # expect 146-set x3, set-equal, delta == {U+00AD}
Exit non-zero on any failed expectation (fail-loud).
"""
import os, re, subprocess, sys

SELF = os.path.abspath(__file__)
for i, ch in enumerate(open(SELF, encoding="utf-8").read()):
    if ord(ch) > 127:
        sys.exit("SELF-CHECK FAIL: non-ASCII char U+%04X at offset %d in proof.py" % (ord(ch), i))

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
SURFACES = {
    "op-rigor":      "skills/operational-rigor/SKILL.md",
    "skill-vetting": "skills/skill-vetting/SKILL.md",
    "checks.py":     ".github/checks.py",
}
FAILS = []

def check(label, expect, actual):
    ok = (expect == actual)
    print("%-4s %-58s EXPECT %-28s ACTUAL %s" % ("PASS" if ok else "FAIL", label, repr(expect), repr(actual)))
    if not ok:
        FAILS.append(label)
    return ok

def load(path, rev=None):
    if rev:
        return subprocess.run(["git", "show", "%s:%s" % (rev, path)],
                              capture_output=True, text=True, check=True).stdout
    return open(os.path.join(ROOT, path), encoding="utf-8").read()

def compile_bad(source):
    m = re.search(r'^BAD = re\.compile\("(.+)"\)$', source, re.M)
    assert m, "BAD pattern line not found in checks.py source"
    return re.compile(m.group(1).encode().decode("unicode_escape"))

def enumerate_set(pat):
    out = set()
    for cp in range(0x110000):
        if 0xD800 <= cp <= 0xDFFF:
            continue
        if pat.match(chr(cp)):
            out.add(cp)
    return frozenset(out)

DASH_CLASS = "[-" + chr(0x2013) + "]"  # ASCII hyphen or en dash (both appear in prose)
RANGE_RE = re.compile(r"U\+([0-9A-Fa-f]{4,6})" + DASH_CLASS + r"U\+([0-9A-Fa-f]{4,6})")
SINGLE_RE = re.compile(r"U\+([0-9A-Fa-f]{4,6})")

def parse_prose_region(text, start_marker, end_marker):
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    return text[i:j + len(end_marker)]

def parse_prose_set(region):
    out, spans = set(), []
    for m in RANGE_RE.finditer(region):
        a, b = int(m.group(1), 16), int(m.group(2), 16)
        assert a <= b, "inverted range"
        out |= set(range(a, b + 1))
        spans.append(m.span())
    for m in SINGLE_RE.finditer(region):
        if any(s <= m.start() and m.end() <= e for s, e in spans):
            continue
        out.add(int(m.group(1), 16))
    return frozenset(out)

def ranges_str(s):
    cps, out = sorted(s), []
    a = b = cps[0]
    for c in cps[1:]:
        if c == b + 1:
            b = c
        else:
            out.append((a, b)); a = b = c
    out.append((a, b))
    return " ".join("U+%04X" % a if a == b else "U+%04X-U+%04X" % (a, b) for a, b in out)

def surfaces_sets(rev):
    op = load(SURFACES["op-rigor"], rev)
    sv = load(SURFACES["skill-vetting"], rev)
    ck = load(SURFACES["checks.py"], rev)
    op_region = parse_prose_region(op, "Sweep for zero-width/bidi Unicode", "sweep misses).")
    sv_region = parse_prose_region(sv, "**Invisible-Unicode smuggling.**", "ranges in sync with it.")
    pat = compile_bad(ck)
    return parse_prose_set(op_region), parse_prose_set(sv_region), enumerate_set(pat), pat

LEGIT = [(9, "TAB"), (10, "LF"), (13, "CR"), (0xA0, "NBSP"), (0xE9, "e-acute"),
         (0x4E2D, "CJK zhong"), (0x2013, "en dash"), (0x2014, "em dash"),
         (0xB7, "middle dot"), (0x2192, "rightwards arrow"), (0x2713, "check mark")]

def run_common(tag, op_s, sv_s, ex_s, pat, expect_n, expect_ad):
    print("== %s ==" % tag)
    check("op-rigor prose |set|", expect_n, len(op_s))
    check("skill-vetting prose |set|", expect_n, len(sv_s))
    check("checks.py executable |set|", expect_n, len(ex_s))
    check("op-rigor == skill-vetting", True, op_s == sv_s)
    check("op-rigor == executable", True, op_s == ex_s)
    check("U+00AD in executable set", expect_ad, 0xAD in ex_s)
    check("U+00AD in op-rigor prose set", expect_ad, 0xAD in op_s)
    check("U+00AD in skill-vetting prose set", expect_ad, 0xAD in sv_s)
    check("U+0085 excluded (all surfaces)", True, all(0x85 not in s for s in (op_s, sv_s, ex_s)))
    check("U+180E excluded (all surfaces)", True, all(0x180E not in s for s in (op_s, sv_s, ex_s)))
    check("known-bad U+200B caught by regex", True, bool(pat.search("ab" + chr(0x200B) + "cd")))
    check("U+00AD caught by regex (live probe)", expect_ad, bool(pat.search("ab" + chr(0xAD) + "cd")))
    check("plain ASCII not caught", False, bool(pat.search("plain ascii text 123")))
    for cp, name in LEGIT:
        check("legit %s U+%04X not caught" % (name, cp), False, bool(pat.search("x" + chr(cp) + "y")))
    print("executable set = %s" % ranges_str(ex_s))

def main():
    mode, rev = sys.argv[1], sys.argv[2]
    if mode == "baseline":
        op_s, sv_s, ex_s, pat = surfaces_sets(rev)
        run_common("BASELINE (RED side) at %s" % rev, op_s, sv_s, ex_s, pat, 145, False)
    elif mode == "post":
        b_op, b_sv, b_ex, _ = surfaces_sets(rev)
        op_s, sv_s, ex_s, pat = surfaces_sets(None)
        run_common("POST-PATCH (GREEN side), working tree vs base %s" % rev, op_s, sv_s, ex_s, pat, 146, True)
        check("baseline executable |set| (re-derived)", 145, len(b_ex))
        check("after == before | {U+00AD}", True, ex_s == b_ex | {0xAD})
        delta = sorted(ex_s - b_ex)
        check("exact set delta == [U+00AD]", ["U+00AD"], ["U+%04X" % c for c in delta])
        check("nothing removed from old set", True, b_ex - ex_s == frozenset())
        check("all old 145 still individually caught", True,
              all(bool(pat.search(chr(cp))) for cp in sorted(b_ex)))
    else:
        sys.exit("unknown mode")
    if FAILS:
        print("RESULT: FAIL (%d failed expectations): %s" % (len(FAILS), FAILS))
        sys.exit(1)
    print("RESULT: ALL EXPECTATIONS PASS")

if __name__ == "__main__":
    main()
