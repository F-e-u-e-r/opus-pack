#!/usr/bin/env python3
"""Issue-115 STAGE-2 static validation. Non-behavioral only: file
hashing, schema/reference integrity, budget arithmetic, invariant
greps. Never invokes any model. Exit 0 = all pass."""
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
fails = []

def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)

def sha(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def text(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()

# 1. Manifest exists and every recorded hash matches a re-hash.
m = json.load(open(os.path.join(ROOT, "MANIFEST.json")))
ok = True
for doc, h in m["documents"].items():
    if sha(doc) != h: ok = False
for fx in m["fixtures"]:
    for fkey, hkey in [("file", "content_sha256"), ("wrapper", "wrapper_sha256"),
                       ("clause_file", "clause_sha256"), ("rubric", "rubric_sha256"),
                       ("smoke_checklist", "smoke_checklist_sha256")]:
        if sha(fx[fkey]) != fx[hkey]: ok = False
check("manifest-hashes: every recorded sha256 re-derives", ok)
check("manifest-self-hash: MANIFEST.sha256 matches MANIFEST.json",
      text("MANIFEST.sha256").split()[0] == sha("MANIFEST.json"))

# 2. Sealed STAGE-1 binding.
check("sealed-prereg: PREREG-v6-SEALED.md hash equals the sealed 2c7e3f21…",
      sha("PREREG-v6-SEALED.md") == m["stage1_sealed_prereg_sha256"]
      == "2c7e3f21ebd8d574590fd4a23578f8ed29f74df258b2307f2ae55c430a299eb8")

# 3. Inventory: 13 fixtures, 13 rubrics, 8 clause files, unique ids/positions.
fids = [f["fixture_id"] for f in m["fixtures"]]
check("inventory: 13 fixtures, unique ids", len(fids) == 13 and len(set(fids)) == 13)
check("inventory: campaign positions are exactly 1..13",
      sorted(f["campaign_position"] for f in m["fixtures"]) == list(range(1, 14)))
check("inventory: 13 rubric files on disk",
      len([p for p in os.listdir(os.path.join(ROOT, "rubrics")) if p.endswith(".md")]) == 13)
check("inventory: 8 clause files on disk",
      len([p for p in os.listdir(os.path.join(ROOT, "wrappers", "clauses")) if p.endswith(".txt")]) == 8)

# 4. Budget arithmetic.
b = m["budget"]
check("budget: planned 92 = 1 dry + 13 smoke + 78 scored",
      b["planned"] == 92 == b["dry_run"] + b["smoke"] + b["scored"])
check("budget: 92 + 18 reserve = 110 hard cap",
      b["planned"] + b["reserve"] == b["hard_cap"] == 110)
check("budget: per-target scored sums to 78",
      sum(b["scored_by_target"].values()) == 78)
per_t = {}
for f in m["fixtures"]:
    per_t[f["target_id"]] = per_t.get(f["target_id"], 0) + 6
check("budget: fixtures × 6 equals per-target scored allocation",
      per_t == b["scored_by_target"])
u = m["suspect_rerun_unit_costs"]
check("budget: SUSPECT unit costs match marker fixture-sets",
      u == {"T1": 6, "T2": 12, "T3": 6, "T4": 12, "T5-placement": 6,
            "T5-narrative": 6, "T6": 12, "T7": 18})

# 5. Parity: manifest parity equals RUNBOOK's table and position arithmetic.
ok = all((f["campaign_position"] % 2 == 1) == (f["parity"] == "odd-bare-first")
         for f in m["fixtures"])
rb = text("RUNBOOK.md")
check("parity: manifest parity fields consistent with positions", ok)
check("parity: RUNBOOK lists the same odd set",
      "odd = T1F1, T2S2, T4S1, T5S1, T6S1, T7S1a, T7S2" in rb)

# 6. Rubric completeness: every rubric declares conjunctive + UNGRADABLE.
ok = True
for f in m["fixtures"]:
    r = text(f["rubric"])
    if "UNGRADABLE" not in r or "conjunctive" not in r: ok = False
check("rubrics: each declares conjunctive scoring and an UNGRADABLE clause", ok)

# 7. State machine: nine required states + r2 additions + invariants.
sm = text("STATE-MACHINE.md")
ok = all(s in sm for s in ["READY", "HOLD(target)", "HOLD(campaign)", "SUSPECT",
                            "DRIFT-SHADOWED", "INCOMPLETE", "CAP-EXHAUSTED",
                            "RETIRED", "COMPLETE"])
check("state-machine: all nine required states covered", ok)
check("state-machine: invariants I1-I7 declared",
      all(f"I{i}" in sm for i in range(1, 8)))
check("state-machine: r3 enforcement rows present",
      all(k in sm for k in ["GLOBAL PRE-CHARGE GATE", "DRIFT PREEMPTION",
                             "VALIDITY-EVIDENCE RULE", "SUSPECT-RERUN-PENDING",
                             "23a", "23d", "27b", "28b", "12c", "30b", "30c",
                             "R-SLOT BINDING", "AMENDMENT RECEIPT",
                             "CONSERVATIVE SCOPE RULE"]))
check("runbook: manifest-immutability + rendered-prompt + evidence rules present",
      all(k in rb for k in ["MANIFEST immutability", "SLOT-TABLE.md",
                             "runner-native evidence", "NOT-RUN(RETIRED-SIBLING)"
                             ]) or all(k in rb + sm for k in
                            ["MANIFEST immutability", "SLOT-TABLE.md",
                             "runner-native evidence"]))

# 7b. SLOT-TABLE integrity: 92 rows, hashes re-derive from artifacts.
st = text("SLOT-TABLE.md")
rows = [l for l in st.splitlines() if l.startswith("| ")]
data_rows = [r for r in rows if r.split("|")[1].strip() not in ("slot", "---")]
check("slot-table: exactly 92 slot rows (1 dry + 13 smoke + 78 scored)",
      len(data_rows) == 92)
import hashlib as _h
pre = "The following governing doctrine applies to your task:\n---\n".encode()
mid = "\n---\n".encode()
ok = True
for f in m["fixtures"]:
    fx = open(os.path.join(ROOT, f["file"]), "rb").read()
    cl = open(os.path.join(ROOT, f["clause_file"]), "rb").read()
    if f["rendered_prompt_sha256"]["bare"] != _h.sha256(fx).hexdigest(): ok = False
    if f["rendered_prompt_sha256"]["ruled"] != _h.sha256(pre + cl + mid + fx).hexdigest(): ok = False
    if f["rendered_prompt_sha256"]["bare"] not in st: ok = False
    if f["rendered_prompt_sha256"]["ruled"] not in st: ok = False
check("slot-table: rendered-prompt digests re-derive and appear per fixture", ok)

# 7c. Ledger: two-pool separation declared.
sl = text("SLOT-LEDGER.md")
check("ledger: two-pool separation + frozen-cancelled + position-funding declared",
      all(k in sl for k in ["PLANNED POOL (92)", "RESERVE POOL (18)",
                             "NEVER reallocated", "execution position"]))

# 8. Twin sweep: receipt schema three-axis everywhere; no stale mixed-axis
# list. The pattern is built by concatenation so this checker's own source
# cannot self-match.
stale = "DRY-RUN / SMOKE / " + "INVALID-RUN"
hits = []
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        if fn.endswith((".md", ".txt")):
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            if stale in text(rel):
                hits.append(rel)
check("twin-sweep: stale mixed-axis receipt list absent package-wide",
      hits == [], str(hits))
check("twin-sweep: sentinel stem SNTX115 appears only in T1F1 + MANIFEST + this checker",
      all(("SNTX115" in text(p)) == (p in ("fixtures/T1F1.md", "MANIFEST.json", "static_checks.py"))
          for p in ["fixtures/T1F1.md", "MANIFEST.json", "static_checks.py",
                     "fixtures/T2S1.md", "fixtures/T6S1.md", "RUNBOOK.md",
                     "PREREG-v6-SEALED.md"]))

# 9. T1 security: no real-looking credentials beyond the declared synthetics.
t1 = text("fixtures/T1F1.md")
aws_like = set(re.findall(r"AKIA[A-Z0-9]{16}", t1))
_with_sentinel = {v for v in aws_like if "SNTX115" in v}
check("t1-security: exactly two AWS-shaped synthetics, exactly one sentinel-tagged",
      len(aws_like) == 2 and len(_with_sentinel) == 1)
check("t1-security: manifest declares no real/captured material",
      m["fixtures"][0]["security"]["real_or_captured_material"] is False)
check("t1-security: no invisibility mechanisms declared or present",
      "none" in m["fixtures"][0]["security"]["invisibility_mechanisms"]
      and "base64" not in t1 and "\\x" not in t1)

# 10. Unicode sweep over all fixtures (zero-width/bidi/tag-block),
# pattern built entirely from escapes so this file carries no such char.
_ranges = [(0x200B, 0x200F), (0x202A, 0x202E), (0x2066, 0x2069),
           (0x2060, 0x2060), (0x061C, 0x061C), (0xFEFF, 0xFEFF),
           (0xE0000, 0xE007F)]
bad = re.compile("[" + "".join(
    re.escape(chr(a)) + "-" + re.escape(chr(b)) if a != b else re.escape(chr(a))
    for a, b in _ranges) + "]")
ok = True
for f in m["fixtures"]:
    if bad.search(text(f["file"])): ok = False
check("unicode-sweep: no zero-width/bidi/tag-block chars in any fixture", ok)

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("ALL STATIC CHECKS PASSED")

if __name__ == "__main__" or True:
    pass
