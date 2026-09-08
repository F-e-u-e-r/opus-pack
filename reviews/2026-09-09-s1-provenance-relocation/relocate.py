#!/usr/bin/env python3
"""S1 provenance relocation + fidelity checker.

Rule: Historical provenance moves to references/provenance.md; operative
re-verification cautions stay inline; canonical markers untouched; stub = locator.

Per skill, `retained` is a list of (start_anchor, end_anchor) verbatim pairs
identifying operative-footer spans that STAY. Everything else in the
## Provenance body MOVES. Master proof: reassembling moved+retained segments
in source order reproduces the source provenance body byte-for-byte.

Usage: s1_relocate.py [--apply]   (default = dry-run, writes nothing)
"""
import sys, os

import subprocess as _sp
ROOT = _sp.run(["git","rev-parse","--show-toplevel"],capture_output=True,text=True,check=True).stdout.strip()
APPLY = "--apply" in sys.argv
HEAD = "## Provenance"
LOCATOR = ("Detailed historical review, probe, and amendment records for this "
           "skill are retained in `references/provenance.md`.")

def refnote(name):
    return (f"# {name} · references: provenance\n\n"
            "Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): "
            "the skill's historical review, probe, and amendment records. Canonical "
            "rules and inline debt markers remain in `SKILL.md`; any operative "
            "re-verification caution stays inline there too. This file is history only.\n")

# retained operative-footer spans (verbatim start/end anchors); [] => move all
CONFIG = {
    "operational-rigor": [("Stable behavioral rules; the environment-specific facts to re-verify",
                           "`df`) inline here.")],
    "delegation-and-review": [("Stable behavioral rules; re-check",
                               "against the current environment.")],
    "skill-authoring": [("Re-verify against current tooling:",
                         "everything else is stable method.")],
    "ground-truth-gates": [("`template/` scripts are self-contained",
                            "re-verify with `bash template/run-all.sh`.")],
    "security-architect": [("Volatile facts to re-verify yearly:",
                            "platform storage APIs and deprecations.")],
    "cross-model-review": [("Re-verify\nline: model families",
                            "recalled from here.")],
    "skill-vetting": [("Re-verify\nthe §2 checklist's invisible-Unicode range",
                       "canonical sweep on any change.")],
    "product-roadmap": [],
    "domain-evidence-discipline": [],
    "personal-goal-planning": [],
}

def rp(s, n=90):
    return repr(s if len(s) <= 2*n else s[:n] + " …[+%dB]… " % (len(s)-2*n) + s[-n:])

fail = 0
summary = []
for name, retained_pairs in CONFIG.items():
    path = os.path.join(ROOT, "skills", name, "SKILL.md")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    marker = "\n" + HEAD + "\n"
    idx = text.find(marker)
    assert idx >= 0, f"{name}: no provenance heading"
    operative = text[:idx + 1]                     # ends with '\n' before '## Provenance'
    prov_full = text[idx + 1:]                     # '## Provenance\n....'
    assert prov_full.startswith(HEAD + "\n")
    prov_body = prov_full[len(HEAD) + 1:]          # after the heading line

    # resolve retained spans
    spans = []
    for start, end in retained_pairs:
        if prov_body.count(start) != 1:
            print(f"!! {name}: start anchor not unique ({prov_body.count(start)}x): {rp(start)}"); fail += 1; continue
        si = prov_body.find(start)
        ei = prov_body.find(end, si)
        if ei < 0:
            print(f"!! {name}: end anchor not found after start: {rp(end)}"); fail += 1; continue
        if prov_body.count(end) != 1:
            print(f"!! {name}: end anchor not unique ({prov_body.count(end)}x): {rp(end)}"); fail += 1; continue
        spans.append((si, ei + len(end)))
    spans.sort()
    # non-overlap
    for a, b in zip(spans, spans[1:]):
        assert a[1] <= b[0], f"{name}: overlapping retained spans"

    # build ordered segments
    segs = []      # (tag, text)
    cur = 0
    for (s, e) in spans:
        if s > cur:
            segs.append(("MOVE", prov_body[cur:s]))
        segs.append(("KEEP", prov_body[s:e]))
        cur = e
    if cur < len(prov_body):
        segs.append(("MOVE", prov_body[cur:]))

    # MASTER FIDELITY PROOF: reassembly == source
    reassembled = "".join(t for _, t in segs)
    ok = reassembled == prov_body
    if not ok:
        print(f"!! {name}: REASSEMBLY MISMATCH"); fail += 1

    moved = "".join(t for tag, t in segs if tag == "MOVE")
    keeps = [t for tag, t in segs if tag == "KEEP"]

    # build new SKILL.md
    new_prov = HEAD + "\n\n" + LOCATOR + "\n"
    if keeps:
        new_prov += "\n" + "\n\n".join(k.strip("\n") for k in keeps) + "\n"
    new_text = operative + new_prov

    # build reference file (verbatim moved history + declared header)
    ref_text = refnote(name) + "\n" + moved
    if not ref_text.endswith("\n"):
        ref_text += "\n"

    # report
    print("=" * 78)
    print(f"{name}: prov_body={len(prov_body)}B  moved={len(moved)}B  "
          f"kept={sum(len(k) for k in keeps)}B  reassembly={'PASS' if ok else 'FAIL'}")
    for i, k in enumerate(keeps):
        # show the byte immediately before and after the kept span for a clean-cut check
        s, e = spans[i]
        before = prov_body[max(0, s-15):s]
        after = prov_body[e:e+15]
        print(f"  KEEP[{i}] {len(k)}B  before={rp(before,20)}  after={rp(after,20)}")
        print(f"          text={rp(k,120)}")
    print("  --- new SKILL.md tail (from ## Provenance) ---")
    print("  " + new_text[len(operative):].replace("\n", "\n  "))
    summary.append((name, len(prov_body), len(moved), sum(len(k) for k in keeps), len(text), len(new_text)))

    if APPLY and ok:
        # word-diff baseline is the clean branch-base SHA (skill-authoring §7),
        # so no .bak debris is written into the tree.
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        refdir = os.path.join(ROOT, "skills", name, "references")
        os.makedirs(refdir, exist_ok=True)
        with open(os.path.join(refdir, "provenance.md"), "w", encoding="utf-8") as fh:
            fh.write(ref_text)

print("=" * 78)
print(f"{'skill':28} {'provB':>7} {'moved':>7} {'kept':>6} {'skillMd':>8} {'newMd':>8}")
tot_prov = tot_moved = 0
for n, pb, mv, kp, om, nm in summary:
    print(f"{n:28} {pb:7} {mv:7} {kp:6} {om:8} {nm:8}")
    tot_prov += pb; tot_moved += mv
print(f"{'TOTAL':28} {tot_prov:7} {tot_moved:7}")
print(f"\nmode={'APPLY' if APPLY else 'DRY-RUN'}  failures={fail}")
sys.exit(1 if fail else 0)
