#!/usr/bin/env python3
"""Mechanical re-verification of the issue115-t5pprobe-v1 PREFIX
evidence. Read-only; exits non-zero on any failure. A second operator
can recompute every prefix claim from the artifacts alone."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PKG = os.path.join(REPO, "reviews", "2026-08-14-issue115-t5-placement-probe-prereg")
MERGE = "6fe6813bcc35edb86a8b92b4aaaa7f9ba3459ef7"
PIN = "claude-haiku-4-5-20251001"
FAILURES = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if not ok and detail else ""))
    if not ok:
        FAILURES.append(name)

def rd(p):
    with open(p, "rb") as f:
        return f.read()

def wire(slot):
    dbg = rd(os.path.join(ROOT, slot, "debug-transcript.log")).decode()
    return json.loads(re.search(r'\n(\{"max_tokens".*?\})\n', dbg, re.S).group(1))

# 1. The prereg package is the merged, unmodified one.
blob = subprocess.run(["git", "-C", REPO, "rev-parse", MERGE],
                      capture_output=True, text=True).stdout.strip()
check("merge commit resolves", blob == MERGE, blob)
dirty = subprocess.run(
    ["git", "-C", REPO, "diff", MERGE, "--",
     "reviews/2026-08-14-issue115-t5-placement-probe-prereg"],
    capture_output=True, text=True).stdout
check("prereg package byte-identical to the merged commit", dirty == "", dirty[:200])

# 2. Every rendered prompt matches its frozen SLOT-TABLE row.
table = rd(os.path.join(PKG, "SLOT-TABLE.md")).decode()
for slot, row, fid in (("smoke-s1", "S1", "P1"), ("smoke-s2", "S2", "P2")):
    exp = re.search(r"^\| " + row + r" \| SMOKE \| P\d \|[^|]*\|[^|]*\| ([0-9a-f]{64}) \|$",
                    table, re.M).group(1)
    p = rd(os.path.join(ROOT, slot, "rendered-prompt.txt"))
    check(f"{row}: rendered prompt == SLOT-TABLE digest",
          hashlib.sha256(p).hexdigest() == exp)
    check(f"{row}: rendered prompt == fixture {fid} bytes on the merged package",
          p == rd(os.path.join(PKG, f"fixtures/{fid}.md")))
    w = wire(slot)
    check(f"{row}: DECODED wire content == rendered prompt bytes",
          w["messages"][0]["content"].encode() == p)
    check(f"{row}: 0 tools, no system, platform-default sampling",
          "tools" not in w and "system" not in w
          and not any(k in w for k in ("temperature", "top_p", "top_k")))
    check(f"{row}: single-turn user message", len(w["messages"]) == 1
          and w["messages"][0]["role"] == "user")

# 3. Identity pin on every invocation, and message-id uniqueness.
ids = []
for slot, rc in (("dryrun", "dryrun-receipt.json"),
                 ("smoke-s1", "s1-receipt.json"),
                 ("smoke-s2", "s2-receipt.json")):
    out = json.load(open(os.path.join(ROOT, slot, "raw-output.json")))
    r = json.load(open(os.path.join(ROOT, slot, rc)))
    check(f"{slot}: reported model == prereg pin", out["model"] == PIN, out["model"])
    check(f"{slot}: receipt id == raw-output id", r["api_message_id"] == out["id"])
    check(f"{slot}: stop_reason end_turn", out["stop_reason"] == "end_turn",
          out["stop_reason"])
    check(f"{slot}: usage numerals machine-derived from raw output",
          r["usage"] == out["usage"])
    ids.append(out["id"])
check("all three api_message_ids distinct", len(set(ids)) == 3, ids)

# 4. Budget accounting: exactly three invocations, zero scored.
inv = [d for d in os.listdir(ROOT)
       if os.path.isdir(os.path.join(ROOT, d))]
check("exactly three invocation directories", sorted(inv) ==
      ["dryrun", "smoke-s1", "smoke-s2"], sorted(inv))
led = rd(os.path.join(ROOT, "LEDGER.md")).decode()
for claim in ("- dry-run: **1**", "- smoke: **2**", "- scored: **0**",
              "- total used: **3/50**",
              "old #115 reserve 18: **untouched**",
              "doctrine / marker / fixture / prereg / rubric mutation: **0**"):
    check(f"ledger states: {claim[:44]}", claim in led)

# 5. Smoke verdicts are the frozen checklist's, 5/5 each.
for slot, rc in (("smoke-s1", "s1-receipt.json"), ("smoke-s2", "s2-receipt.json")):
    r = json.load(open(os.path.join(ROOT, slot, rc)))
    check(f"{slot}: smoke verdict PASS 5/5", r["smoke_verdict"] == "PASS 5/5",
          r["smoke_verdict"])
    check(f"{slot}: all five checklist items PASS",
          all(v == "PASS" for v in r["smoke_checklist"].values()),
          r["smoke_checklist"])

# 6. No credential material anywhere in the evidence.
leak = subprocess.run(
    ["grep", "-rEl", r"sk-ant-[A-Za-z0-9_-]{8,}|Bearer [A-Za-z0-9._-]{12,}", ROOT],
    capture_output=True, text=True).stdout.strip()
check("no credential material in the evidence package", leak == "", leak)

print()
if FAILURES:
    print("PREFIX CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("PREFIX CHECKS: ALL PASS")
