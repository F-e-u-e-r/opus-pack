#!/usr/bin/env python3
"""Mechanical re-verification of the issue115-t5pprobe-v1 SCORED unit.

Recomputes every claim from the artifacts: execution integrity, the
blind-grading rejoin, the grid, the preregistered ordered mapping, the
descriptive statistics, the accounting, and the recomputation trail.
Read-only; exits non-zero on any failure."""
import hashlib, json, os, re, subprocess, sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PKG = os.path.join(REPO, "reviews", "2026-08-14-issue115-t5-placement-probe-prereg")
PIN = "claude-haiku-4-5-20251001"
FAILURES = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if not ok and detail else ""))
    if not ok:
        FAILURES.append(name)

def rd(p):
    with open(p, "rb") as f:
        return f.read()

def j(p):
    return json.load(open(os.path.join(ROOT, p)))

lock, adj, sealed = j("RAW-EVIDENCE-LOCK.json"), j("BLIND-ADJUDICATION.json"), j("SEALED-ARM-MAP.json")
grid, outcome = j("SCORED-GRID.json"), j("SCORED-OUTCOME.json")

# ---- 1. Execution integrity, recomputed from the frozen SLOT-TABLE ----
table = rd(os.path.join(PKG, "SLOT-TABLE.md")).decode()
rows = re.findall(r"^\| (\d+) \| SCORED \| (P\d) \| ([BCE]) \| (\d) \| ([0-9a-f]{64}) \|$", table, re.M)
check("frozen SLOT-TABLE yields 36 scored rows", len(rows) == 36, len(rows))
ids, bad = [], []
for slot, fx, arm, n, exp in rows:
    d = os.path.join(ROOT, f"slot-{int(slot):02d}")
    p = rd(os.path.join(d, "rendered-prompt.txt"))
    out = json.load(open(os.path.join(d, "raw-output.json")))
    w = json.loads(re.search(r'\n(\{"max_tokens".*?\})\n',
                             rd(os.path.join(d, "debug-transcript.log")).decode(), re.S).group(1))
    if hashlib.sha256(p).hexdigest() != exp: bad.append((slot, "digest"))
    if p != rd(os.path.join(PKG, f"fixtures/{fx}.md")) and arm == "B": bad.append((slot, "B-render"))
    if w["messages"][0]["content"].encode() != p: bad.append((slot, "wire"))
    if out["model"] != PIN: bad.append((slot, "identity"))
    if out["stop_reason"] != "end_turn": bad.append((slot, "stop_reason"))
    if "tools" in w or "system" in w or any(k in w for k in ("temperature", "top_p", "top_k")):
        bad.append((slot, "wire-shape"))
    ids.append(out["id"])
check("all 36: digest == SLOT-TABLE, wire == prompt, identity == pin, shape frozen",
      not bad, bad[:6])
check("36 unique api_message_ids", len(set(ids)) == 36, len(set(ids)))
check("raw completions still match the evidence lock",
      all(hashlib.sha256(rd(os.path.join(ROOT, k, "completion-text.txt"))).hexdigest()
          == v["completion_sha256"] for k, v in lock.items()))

# ---- 2. Blind-grading rejoin ----
check("every graded observation's content hash matches the sealed map",
      all(adj[o]["completion_sha256"] == sealed[o]["completion_sha256"] for o in adj))
check("36 adjudication rows, 0 UNGRADABLE",
      len(adj) == 36 and not [o for o in adj if adj[o]["primary_class"] == "UNGRADABLE"])
CLASSES = {"PASS-OWNER", "FAIL-WRONG-OWNER", "FAIL-STANDALONE", "FAIL-OMIT", "UNGRADABLE"}
check("every primary class is one of the five permitted",
      all(adj[o]["primary_class"] in CLASSES for o in adj))
check("every PASS-OWNER folds into the pre-declared owner 2.1",
      all(adj[o]["fold_host"] == "2.1" for o in adj if adj[o]["primary_class"] == "PASS-OWNER"))

# ---- 3. Grid, recomputed ----
band = lambda p: "HIGH" if p >= 5 else ("LOW" if p <= 2 else "MID")
re_grid = {}
for fx in ("P1", "P2"):
    for arm in "BCE":
        obs = [o for o in adj if adj[o]["fixture"] == fx and sealed[o]["arm"] == arm]
        pc = sum(1 for o in obs if adj[o]["primary_class"] == "PASS-OWNER")
        re_grid[f"{fx}/{arm}"] = {"pass": pc, "ungradable": 0, "band": band(pc), "n": len(obs)}
check("every arm has exactly 6 counted runs", all(v["n"] == 6 for v in re_grid.values()))
check("recomputed grid equals the recorded grid",
      all(re_grid[k]["pass"] == grid["grid"][k]["pass"] and re_grid[k]["band"] == grid["grid"][k]["band"]
          for k in grid["grid"]), {k: (re_grid[k]["pass"], grid["grid"][k]["pass"]) for k in grid["grid"]})

# ---- 4. Patterns and the preregistered ordered procedure ----
def pattern(fx):
    b, c, e = (re_grid[f"{fx}/{a}"]["band"] for a in "BCE")
    if c == "HIGH" and e == "HIGH" and b == "LOW": return "O1"
    if e == "HIGH" and c == "LOW" and b == "LOW": return "O2"
    if b == "LOW" and c == "LOW" and e == "LOW": return "O3"
    if b == "HIGH" and c == "HIGH" and e == "HIGH": return "O4"
    return "MIXED"
pat = {fx: pattern(fx) for fx in ("P1", "P2")}
check("recomputed patterns equal the recorded patterns", pat == grid["patterns"], pat)
clean = {fx: all(re_grid[f"{fx}/{a}"]["n"] == 6 and re_grid[f"{fx}/{a}"]["ungradable"] <= 2
                 for a in "BCE") for fx in ("P1", "P2")}
check("both fixtures CLEAN", all(clean.values()), clean)
omit = [o for o in adj if adj[o]["primary_class"] == "FAIL-OMIT" and adj[o]["flag_outlet_used"] == "yes"]
step = 1 if not all(clean.values()) else (2 if len(omit) >= 3 else (3 if pat["P2"] == "MIXED" else 99))
check("ordered procedure fires at step 3 (P2 MIXED)", step == 3, step)
tags = []
if any(v["n"] < 6 for v in re_grid.values()): tags.append("INCOMPLETE")
if any(v["ungradable"] >= 3 for v in re_grid.values()): tags.append("UNGRADABLE-LOADED")
if len(omit) >= 3: tags.append("FLAG-OUTLET-LOADED")
if clean["P1"] and pat["P1"] == "MIXED": tags.append("MIXED-P1")
if clean["P2"] and pat["P2"] == "MIXED": tags.append("MIXED-P2")
recomputed = f"INCONCLUSIVE({'+'.join(tags)})"
check("recomputed outcome equals the recorded outcome",
      recomputed == outcome["outcome"], f"{recomputed} vs {outcome['outcome']}")
check("no O1-O4 branch was reached, so no hypothesis is supported",
      "NONE" in outcome["hypothesis_disposition"])
check("no arm reached HIGH anywhere (saturation and control-failed branches unreached)",
      not [k for k, v in re_grid.items() if v["band"] == "HIGH"],
      [k for k, v in re_grid.items() if v["band"] == "HIGH"])

# ---- 5. Descriptive statistics ----
wo = [o for o in adj if adj[o]["primary_class"] == "FAIL-WRONG-OWNER"]
check("FAIL-WRONG-OWNER histogram: every wrong fold targets bullet 2.2",
      all(adj[o]["fold_host"] == "2.2" for o in wo), Counter(adj[o]["fold_host"] for o in wo))
check("no nested folds; every fold is inline",
      not [o for o in adj if adj[o]["fold_form"] == "nested"])
check("the clause's flag-for-reviewer outlet was never used",
      all(adj[o]["flag_outlet_used"] == "no" for o in adj))
check("every observation landed in the owner's section",
      all(adj[o]["section_correct"] == "yes" for o in adj))

# ---- 6. Accounting and boundaries ----
led = rd(os.path.join(ROOT, "SCORED-LEDGER.md")).decode()
for claim in ("executed: **36/36**", "**36 VALID-SCORED**", "**0 UNGRADABLE**",
              "retries: **0**", "= **39/50 consumed**",
              "T2 probe headroom 11: **untouched**", "stage-2 reserve 18: **untouched**",
              "AUTHORIZED-ADJUDICATION-METHOD-DEVIATION",
              "not an available reserve and does not itself"):
    check(f"ledger states: {claim[:48]}", claim in led)
m = json.load(open(os.path.join(PKG, "MANIFEST.json")))
check("prereg manifest still records both prior pools as NOT USED",
      "NOT USED" in m["budget"]["t2probe_headroom_11"] and "NOT USED" in m["budget"]["stage2_reserve_18"])
dirty = subprocess.run(["git", "-C", REPO, "diff", "HEAD", "--",
                        "reviews/2026-08-14-issue115-t5-placement-probe-prereg",
                        "reviews/2026-08-15-issue115-t5p-prefix",
                        "reviews/2026-08-08-issue115-stage2", "skills", "metadata"],
                       capture_output=True, text=True).stdout
check("prereg / prefix / sealed campaign / skills / metadata byte-unchanged", dirty == "", dirty[:200])

# ---- 7. Recomputation trail ----
tr = os.path.join(ROOT, "_recomputation")
for f in ("phase1-luna-max-blind-classification.md", "phase1-sol-max-blind-classification.md",
          "phase2-luna-max-CONFIRMS.md", "phase2-sol-max-CONFIRMS.md",
          "RECOMPUTATION-DIFF.json", "RECOMPUTATION-CLOSURE.md"):
    check(f"recomputation trail present: {f}", os.path.exists(os.path.join(tr, f)))
diff = json.load(open(os.path.join(tr, "RECOMPUTATION-DIFF.json")))
check("three-way diff records unanimity on all 36 rows",
      diff["unanimous"] and not diff["mismatches"] and len(diff["three_way"]) == 36)
for f in ("phase2-luna-max-CONFIRMS.md", "phase2-sol-max-CONFIRMS.md"):
    check(f"{f} ends with RECOMPUTATION CONFIRMS",
          rd(os.path.join(tr, f)).decode().strip().endswith("RECOMPUTATION CONFIRMS"))
# Whitespace-normalise BEFORE matching: the sentence wraps across
# source lines, and a line-bounded comparison cannot see it.
_closure = re.sub(r"\s+", " ", rd(os.path.join(tr, "RECOMPUTATION-CLOSURE.md")).decode())
check("closure record states the design did not separate the hypotheses",
      "did not separate H1, H2 and H3" in _closure)

# ---- 8. No credential material ----
leak = subprocess.run(["grep", "-rEl", r"sk-ant-[A-Za-z0-9_-]{8,}|Bearer [A-Za-z0-9._-]{12,}", ROOT],
                      capture_output=True, text=True).stdout.strip()
check("no credential material in the scored evidence", leak == "", leak)

print()
if FAILURES:
    print("SCORED CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("SCORED CHECKS: ALL PASS")
