#!/usr/bin/env python3
"""Faithful-reconstruction battery for the ⑫ recursive-delegation landing.

Machine-proves: landed operative doctrine text == frozen v2 design blocks
(+ exactly one marker + provenance + Markdown placement adaptations), with
zero collateral. Run from the repository root:  python3 reviews/2026-09-02-recursive-delegation-c12/c12_checks.py

Checks (owner-mandated battery):
 1  base lineage contains a51396d (the authorized base)
 2  design-v2.md matches its MANIFEST hash (frozen bytes loaded, not typed)
 3  D&R §2 canonical block == v2 §2 block + exactly the single marker
 4  D&R §3 block == v2 §3 consumption/accounting block
 5  CMR §1 sentence == v2 §4 family-propagation sentence
 6  F1 prospective semantics complete (invocation-time; no retro-clear)
 7  material contribution retrospective-only
 8  compact account covers EVERY spawned judgment principal
 9  rich disclosure contributor-only
10  deterministic/mechanical helper carve-out intact
11  child scope/envelope/budget subset-only
12  D17/D18/D19 intact in the frozen design
13  D14 wording zero-polish (byte-equal v1 == v2 row; present in v2)
14  [verified: ran/read] first-principal semantics intact
15  CMR transitive reviewer-family accounting intact
16  no hard depth rule in any landed operative block
17  ⑧-A zero-byte (receipt reference + execution-principal bullet untouched)
18  no runtime/tooling/harness mutation (file-list confinement)
19  orphan-principal discovery NOT activated into doctrine text
20  exactly one new canonical marker in D&R; CMR marker delta 0
21  #115 route intact in the provenance entry
22  zero collateral beyond the three authorized paths
23  repo checks.py green (includes the Unicode/control hygiene sweep)
24  MANIFEST.sha256 verifies every package file
"""
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PKG = os.path.dirname(os.path.abspath(__file__))
DR = os.path.join(ROOT, "skills/delegation-and-review/SKILL.md")
CMR = os.path.join(ROOT, "skills/cross-model-review/SKILL.md")
RECEIPT = os.path.join(ROOT, "skills/delegation-and-review/references/reviewer-capability-receipt.md")
BASE = "a51396d"

fails = []


def check(n, name, cond, detail=""):
    print("%s %02d %s" % ("PASS" if cond else "FAIL", n, name) + ("" if cond else "  -- " + str(detail)[:300]))
    if not cond:
        fails.append(n)


def sh(cmd):
    return subprocess.run(cmd, shell=True, cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def extract_block(v2_text, header):
    idx = v2_text.index(header)
    lines = v2_text[idx:].split("\n")
    out, started = [], False
    for ln in lines[1:]:
        if ln.startswith(">"):
            started = True
            out.append(ln[2:] if ln.startswith("> ") else ln[1:])
        elif started:
            break
    return "\n".join(out)


v2 = open(os.path.join(PKG, "design-v2.md"), encoding="utf-8").read()
v1 = open(os.path.join(PKG, "design-v1.md"), encoding="utf-8").read()
dr = open(DR, encoding="utf-8").read()
cmr = open(CMR, encoding="utf-8").read()

# landed operative extracts
m2 = re.search(r"(?ms)^- \*\*Re-delegation\*\*.*?(?=\n\nIf any field cannot be filled)", dr)
landed2 = m2.group(0) if m2 else ""
m3 = re.search(r"(?ms)^- \*\*`\[verified: ran/read\]` is first-person.*?(?=\n- \*\*\"That failure is pre-existing\")", dr)
landed3 = m3.group(0) if m3 else ""
m4 = re.search(r"(?ms)Family accounting is transitive across.*?only the family propagation\)\.", cmr)
landed4 = m4.group(0) if m4 else ""
operative = landed2 + "\n" + landed3 + "\n" + landed4

# 1
r = sh("git merge-base --is-ancestor %s HEAD && echo yes" % BASE)
check(1, "base lineage contains %s" % BASE, "yes" in r.stdout, r.stdout)

# 2
man = {}
for ln in open(os.path.join(PKG, "MANIFEST.sha256"), encoding="utf-8"):
    parts = ln.split()
    if len(parts) == 2:
        man[parts[1].lstrip("*")] = parts[0]
h = hashlib.sha256(open(os.path.join(PKG, "design-v2.md"), "rb").read()).hexdigest()
check(2, "design-v2.md == MANIFEST frozen hash", man.get("design-v2.md") == h,
      (man.get("design-v2.md"), h))

# 3
v2b2 = extract_block(v2, "## 2. Draft text — delegation-and-review §2")
MARKER = "(`unprobed` — see Provenance)."
stripped = landed2.replace("\n  " + MARKER, "").replace(" " + MARKER, "")
# v1's opening sentence carries the period the marker line absorbed
stripped = stripped.replace("delegation authority\n  A worker", "delegation authority.\n  A worker")
check(3, "D&R §2 == v2 §2 block + single marker",
      norm(stripped) == norm(v2b2) and landed2.count("`unprobed`") == 1,
      "normalized mismatch" if norm(stripped) != norm(v2b2) else "marker count %d" % landed2.count("`unprobed`"))

# 4
v2b3 = extract_block(v2, "## 3. Draft text — delegation-and-review §3")
check(4, "D&R §3 == v2 §3 block", norm(landed3) == norm(v2b3), len(landed3))

# 5
v2b4 = extract_block(v2, "## 4. Draft text — cross-model-review §1, extension sentence")
check(5, "CMR §1 sentence == v2 §4 sentence", norm(landed4) == norm(v2b4), len(landed4))

# 6
check(6, "F1 prospective semantics complete",
      "For\n  authorization the boundary is PROSPECTIVE" in landed2.replace("For\n  authorization", "For\n  authorization")
      and "moment of invocation" in landed2
      and "never\n  retroactively" in landed2 or
      ("boundary is PROSPECTIVE" in norm(landed2) and "moment of invocation" in norm(landed2)
       and "never retroactively makes an unauthorized judgment delegation permissible" in norm(landed2)))

# 7
check(7, "contribution retrospective-only",
      "RETROSPECTIVE question governing only provenance, lens, and family accounting" in norm(landed2))

# 8
check(8, "compact account: EVERY spawned judgment principal",
      "Compact — EVERY spawned judgment principal, whether or not its judgment ultimately contributes" in norm(landed2))

# 9
check(9, "rich disclosure contributor-only",
      "Rich — every sub-principal whose judgment materially contributed" in norm(landed2))

# 10
check(10, "deterministic helper carve-out intact",
      "Deterministic helpers and ordinary tool execution" in norm(landed2)
      and "purely mechanical transformation delegates none" in norm(landed2))

# 11
check(11, "subset-only propagation",
      "cannot grant authority it does not hold" in norm(landed2)
      and "delegable scope, authority envelope, and applicable fan-out/cost budget" in norm(landed2))

# 12
check(12, "D17/D18/D19 intact in frozen design",
      all("| D%d |" % n in v2 for n in (17, 18, 19)))

# 13
d14_v1 = [l for l in v1.split("\n") if l.startswith("| D14 |")]
d14_v2 = [l for l in v2.split("\n") if l.startswith("| D14 |")]
check(13, "D14 zero-polish (v1 row byte==v2 row)",
      len(d14_v1) == 1 and d14_v1 == d14_v2, (d14_v1, d14_v2))

# 14
check(14, "[verified] first-person semantics",
      "asserts first-hand action by the REPORTING principal itself" in norm(landed3)
      and "never as the parent's first-hand verification" in norm(landed3))

# 15
check(15, "CMR transitive reviewer-family accounting",
      "transitive across delegation depth on the reviewer side too" in norm(landed4)
      and "materially contributed JUDGMENT" in norm(landed4))

# 16
check(16, "no hard depth rule in landed operative text",
      not re.search(r"(?i)max[- ]?depth|depth (cap|limit)|depth\s*=\s*1", operative))

# 17
r = sh("git diff %s -- skills/delegation-and-review/references/reviewer-capability-receipt.md | wc -c" % BASE)
dr_diff = sh("git diff %s -- skills/delegation-and-review/SKILL.md" % BASE).stdout
check(17, "⑧-A zero-byte (receipt ref + bullet untouched)",
      r.stdout.strip() == "0" and "Artifact isolation is not principal confinement" not in dr_diff)

# 18/22
r = sh("git diff --name-only %s" % BASE)
files = sorted(f for f in r.stdout.strip().split("\n") if f)
allowed = all(f in ("skills/delegation-and-review/SKILL.md", "skills/cross-model-review/SKILL.md")
              or f.startswith("reviews/2026-09-02-recursive-delegation-c12/") for f in files)
check(18, "no runtime/tooling mutation (file confinement)", allowed, files)

# 19
added_doctrine = "\n".join(l for l in (dr_diff + sh("git diff %s -- skills/cross-model-review/SKILL.md" % BASE).stdout).split("\n")
                           if l.startswith("+") and not l.startswith("+++"))
check(19, "orphan-principal NOT activated into doctrine",
      "orphan" not in operative.lower()
      and os.path.exists(os.path.join(PKG, "orientation-report.md")))

# 20
new_markers_dr = added_doctrine.count("(`unprobed`")
cmr_added = sh("git diff %s -- skills/cross-model-review/SKILL.md" % BASE).stdout
cmr_markers = "\n".join(l for l in cmr_added.split("\n") if l.startswith("+")).count("(`unprobed`")
check(20, "exactly one new canonical marker (D&R); CMR delta 0",
      new_markers_dr == 1 and cmr_markers == 0, (new_markers_dr, cmr_markers))

# 21
check(21, "#115 route intact in provenance", "#115" in added_doctrine)

# 22
check(22, "zero collateral (same confinement, both skill files present in diff)",
      allowed and "skills/delegation-and-review/SKILL.md" in files
      and "skills/cross-model-review/SKILL.md" in files, files)

# 23
r = sh("python3 .github/checks.py")
check(23, "repo checks.py green (incl. hygiene sweep)", r.returncode == 0, r.stdout[-300:])

# 24
bad = []
for fname, want in sorted(man.items()):
    fp = os.path.join(PKG, fname)
    if not os.path.exists(fp):
        bad.append((fname, "missing"))
        continue
    got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    if got != want:
        bad.append((fname, "hash"))
check(24, "MANIFEST verifies every package file (%d entries)" % len(man), len(man) >= 15 and not bad, bad)

print()
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("c12_checks: all 24 PASS")
