#!/usr/bin/env python3
"""Mechanical integrity gate for the issue115-t2probe-v1 SCORED-unit
evidence package (36 observations + adjudication + gate trail).
Read-only; exits non-zero on any failure. Paths resolve relative to
this file; re-runnable on hosted bytes via a checkout containing this
directory plus the sibling prereg package."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PREREG = os.path.join(REPO, "reviews", "2026-08-13-issue115-t2-probe-prereg")
EXPECT_MODEL = "claude-haiku-4-5-20251001"
FAILURES = []

def chk(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def decode_wire(log):
    i = log.find("Request Content:")
    j = log.find("{", i)
    while j != -1:
        try:
            obj, _ = json.JSONDecoder().raw_decode(log[j:])
            if "messages" in obj:
                return obj
        except Exception:
            pass
        j = log.find("{", j + 1)
    return None

# Frozen slot table
rows = []
for line in open(os.path.join(PREREG, "SLOT-TABLE.md")):
    m = re.match(r"\| (\d+) \| SCORED \| (P[12]) \| ([BCE]) \| (\d) \| ([0-9a-f]{64}) \|", line)
    if m:
        rows.append((int(m.group(1)), m.group(2), m.group(3), int(m.group(4)), m.group(5)))
chk("frozen SLOT-TABLE yields exactly 36 scored rows", len(rows) == 36)

slot_dirs = sorted(os.listdir(os.path.join(ROOT, "slots")))
chk("exactly 36 slot directories, no extra behavioral observation",
    slot_dirs == [f"slot{i:02d}" for i in range(1, 37)])
chk("zero EXCEPTION records",
    not any("EXCEPTION" in f for _, _, fs in os.walk(ROOT) for f in fs))

ids, models, last_end = [], [], ""
for slot, f, arm, n, digest in rows:
    d = os.path.join(ROOT, "slots", f"slot{slot:02d}")
    r = json.load(open(os.path.join(d, "receipt.json")))
    raw = json.load(open(os.path.join(d, "raw-output.json")))
    log = open(os.path.join(d, "debug-transcript.log")).read()
    rp = open(os.path.join(d, "rendered-prompt.txt")).read()
    ids.append(raw["id"]); models.append(raw["model"])
    ok_slot = (
        (r["fixture_id"], r["arm"], r["n_index"], r["retry_role"], r["attempt_number"])
        == (f, arm, n, "original", 1)
        and sha(os.path.join(d, "rendered-prompt.txt")) == digest == r["rendered_prompt_sha256"]
        and raw["model"] == EXPECT_MODEL == r["executor_reported_model"]
        and raw["stop_reason"] == "end_turn" and raw["content"][0]["text"].strip()
        and sha(os.path.join(d, "raw-output.json")) == r["raw_output_sha256"]
        and sha(os.path.join(d, "debug-transcript.log")) == r["debug_transcript_sha256"]
        and "Bearer <REDACTED>" in log
        and not re.search(r"Bearer [A-Za-z0-9_\-\.]{20,}", log)
        and raw["usage"]["input_tokens"] == r["usage"]["input_tokens"]
        and raw["usage"]["output_tokens"] == r["usage"]["output_tokens"]
        and raw["id"] == r["api_message_id"]
    )
    wire = decode_wire(log)
    ok_wire = (wire is not None and wire["messages"][0]["content"] == rp
               and wire["model"] == "claude-haiku-4-5" and wire["max_tokens"] == 4096
               and "tools" not in wire and "system" not in wire)
    if not (ok_slot and ok_wire):
        chk(f"slot {slot} integrity", False)
    last_end = max(last_end, r["timestamp_utc"].split(" to ")[1].split(" ")[0])
chk("per-slot integrity (receipt/digest/identity/hashes/credential/usage/wire) all 36", not FAILURES or all("slot " not in f for f in FAILURES))
chk("36 unique message ids", len(set(ids)) == 36)
chk("all resolved identities exact", set(models) == {EXPECT_MODEL})

# Adjudication recomputation from rows
A = os.path.join(ROOT, "adjudication")
mp = json.load(open(os.path.join(A, "opaque-map.json")))["map"]
chk("opaque map covers exactly the 36 slots",
    sorted(v["slot"] for v in mp.values()) == list(range(1, 37)))
counts, ungr, rat, skip, replay = {}, 0, {"B": 0, "C": 0, "E": 0}, {"P1": 0, "P2": 0}, {}
for oid, m in mp.items():
    row = json.load(open(os.path.join(A, "rows", f"{oid}.json")))
    chk_ok = row["fixture"] == m["fixture"]
    if not chk_ok:
        chk(f"row {oid} fixture matches map", False)
    key = (m["fixture"], m["arm"])
    counts.setdefault(key, {"PASS": 0, "FAIL-ORDER": 0, "FAIL-NO-SETTLE": 0})
    if row["run_class"] == "UNGRADABLE":
        ungr += 1
    else:
        counts[key][row["run_class"]] += 1
    s = row["secondary"]
    if s["ordering_rationale"] == "yes":
        rat[m["arm"]] += 1
    if s["branch_settle_skip"] == "yes":
        skip[m["fixture"]] += 1
    replay[s["replay_conditioning"]] = replay.get(s["replay_conditioning"], 0) + 1
chk("36 VALID-SCORED / 0 UNGRADABLE", ungr == 0)
grid = {(f, a): counts[(f, a)]["PASS"] for f in ("P1", "P2") for a in "BCE"}
chk("P1 = B0/C1/E6", (grid[("P1","B")], grid[("P1","C")], grid[("P1","E")]) == (0, 1, 6), grid)
chk("P2 = B0/C1/E6", (grid[("P2","B")], grid[("P2","C")], grid[("P2","E")]) == (0, 1, 6), grid)
def band(p): return "HIGH" if p >= 5 else ("LOW" if p <= 2 else "MID")
bands = {k: band(v) for k, v in grid.items()}
chk("bands LOW/LOW/HIGH on both fixtures",
    all(bands[(f, "B")] == "LOW" and bands[(f, "C")] == "LOW" and bands[(f, "E")] == "HIGH"
        for f in ("P1", "P2")))
chk("O2 mechanical recomputation holds (both fixtures)",
    all(bands[(f, "E")] == "HIGH" and bands[(f, "C")] == "LOW" and bands[(f, "B")] == "LOW"
        for f in ("P1", "P2")))
chk("all FAILs are FAIL-ORDER (0 FAIL-NO-SETTLE)",
    all(c["FAIL-NO-SETTLE"] == 0 for c in counts.values()))
chk("rationale statistic canonical B0/C1/E11", (rat["B"], rat["C"], rat["E"]) == (0, 1, 11), rat)
chk("settle-skip statistic canonical P1=3/P2=2", (skip["P1"], skip["P2"]) == (3, 2), skip)
chk("replay-conditioning 35 yes + 1 no-replay-planned",
    replay.get("yes") == 35 and replay.get("no-replay-planned") == 1, replay)

# slot-04 corrected record consistent with raw evidence
s4 = [k for k, v in mp.items() if v["slot"] == 4][0]
row4 = json.load(open(os.path.join(A, "rows", f"{s4}.json")))
raw4 = json.load(open(os.path.join(ROOT, "slots", "slot04", "raw-output.json")))["content"][0]["text"]
chk("slot-04 corrected: unconditional get on status-fail path, class FAIL-ORDER, skip=no",
    row4["run_class"] == "FAIL-ORDER" and row4["secondary"]["branch_settle_skip"] == "no"
    and "correction_note" in row4 and row4["paths"][2]["pos"]["D"] == 2)
chk("slot-04 raw evidence has unconditional step-2 get",
    re.search(r"2\.\s+\*\*Call `payments\.get", raw4) is not None)

# Grading strictly after 36/36
adj = json.load(open(os.path.join(A, "T2PROBE-ADJUDICATION.json")))
chk("grading timestamp after last invocation end",
    adj["graded_at"] > last_end, f"{adj['graded_at']} vs {last_end}")
chk("summary matches recomputation",
    adj["campaign_outcome"] == "O2" and adj["CLEAN"] is True
    and adj["validity_composition"] == {"VALID-SCORED": 36, "UNGRADABLE": 0})

# RESULTS canonical claims
R = open(os.path.join(ROOT, "RESULTS.md")).read()
chk("RESULTS carries O2 + directional + machine-reconciled stats",
    "O2" in R and "directional" in R.lower() and "11/12 E-arm" in R and "1/12 C-arm" in R
    and "P1: 3, P2: 2" in R)
chk("RESULTS does not adopt E wording as doctrine",
    "replacement" not in R.lower() and "adopt" not in R.lower().replace("adoption", ""))

# Gate trail: HOLD history preserved, final PROCEED x2
G = os.path.join(ROOT, "_gate")
need = ["round1-luna-max-recompute-PROCEED.md", "round1-sol-max-recompute-HOLD.md",
        "round2-sol-max-recompute-PROCEED.md", "GATE-CLOSURE.md"]
chk("gate trail files present incl. round-1 Sol HOLD", all(os.path.exists(os.path.join(G, f)) for f in need))
chk("verdict lines: Luna r1 PROCEED, Sol r1 HOLD, Sol r2 PROCEED",
    open(os.path.join(G, need[0])).read().strip().endswith("VERDICT: PROCEED")
    and "VERDICT: HOLD" in open(os.path.join(G, need[1])).read()
    and open(os.path.join(G, need[2])).read().strip().endswith("VERDICT: PROCEED"))

# Ledger accounting
L = open(os.path.join(ROOT, "LEDGER-SCORED.md")).read()
for needle in ("dry-run: **1**", "smoke: **2**", "scored: **36**", "total: **39/50**",
               "planned remaining: **0**", "headroom: **11 untouched**",
               "reserve: **18 untouched**", "B 0/12 · C 1/12 · E 11/12"):
    chk(f"ledger line: {needle}", needle in L)

# Package boundaries: prereg + prefix untouched; E wording not in skills
r = subprocess.run([sys.executable, os.path.join(PREREG, "static_checks.py")],
                   capture_output=True, text=True)
chk("prereg static checks 39/39 ALL PASS", "ALL PASS" in r.stdout and r.returncode == 0)
g = subprocess.run(["git", "-C", REPO, "status", "--porcelain",
                    "reviews/2026-08-13-issue115-t2-probe-prereg",
                    "reviews/2026-08-13-issue115-t2probe-prefix",
                    "skills"], capture_output=True, text=True)
chk("prereg + prefix evidence + skills untouched in working tree", g.stdout.strip() == "", g.stdout)

print()
if FAILURES:
    print("SCORED CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("SCORED CHECKS: ALL PASS")
