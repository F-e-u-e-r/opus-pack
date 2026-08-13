#!/usr/bin/env python3
"""Mechanical integrity gate for the issue115-t2probe-v1 execution
PREFIX evidence (slot 0 dry-run + S1 + S2). Read-only; exits non-zero
on any failure. Run from anywhere; paths resolve relative to this
file. Designed to be re-runnable on hosted bytes (a checkout of the
evidence directory plus the sibling prereg package)."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PREREG = os.path.join(REPO, "reviews", "2026-08-13-issue115-t2-probe-prereg")
EXPECT_MODEL = "claude-haiku-4-5-20251001"
S1_DIGEST = "1b35c236c6bec0cd85f71e2f78f1f0d365a54ce723a1b4bfc03293ccaa0adade"
S2_DIGEST = "3a5f4c271d300b42f13d8449acc46c3e4d1146ae6baf678169aca50c3d5bd2d1"
FAILURES = []

def chk(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)

def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def decode_wire(logpath):
    log = open(logpath).read()
    m = re.search(r'(\{[^\n]*"messages".*?\]\})', log, re.S) or \
        re.search(r'\n(\{.*?"messages".*?\})\s*\n', log, re.S)
    return (json.loads(m.group(1)) if m else None), log

# --- 1. Exact prefix identities: dry-run + S1 + S2, no scored slot dir
dirs = sorted(d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)))
chk("prefix directories exactly {dryrun, smoke-s1, smoke-s2}",
    dirs == ["dryrun", "smoke-s1", "smoke-s2"], dirs)
chk("no scored-slot artifact anywhere",
    not any("scored" in f.lower() or re.match(r"slot-?[1-9]", f) for f in
            [x for _, _, fs in os.walk(ROOT) for x in fs]))

R0 = json.load(open(os.path.join(ROOT, "dryrun/dryrun-receipt.json")))
R1 = json.load(open(os.path.join(ROOT, "smoke-s1/s1-receipt.json")))
R2 = json.load(open(os.path.join(ROOT, "smoke-s2/s2-receipt.json")))
RAW0 = json.load(open(os.path.join(ROOT, "dryrun/raw-output.json")))
RAW1 = json.load(open(os.path.join(ROOT, "smoke-s1/raw-output.json")))
RAW2 = json.load(open(os.path.join(ROOT, "smoke-s2/raw-output.json")))

# --- 2. Three unique actual message IDs (receipts == raw outputs)
ids = [RAW0["id"], RAW1["id"], RAW2["id"]]
chk("3 unique api message ids", len(set(ids)) == 3, ids)
chk("receipt msg ids match raw outputs",
    (R0["api_message_id"], R1["api_message_id"], R2["api_message_id"]) == tuple(ids))

# --- 3. Resolved model identity on all three
chk("all three resolved models == " + EXPECT_MODEL,
    all(r["model"] == EXPECT_MODEL for r in (RAW0, RAW1, RAW2)))
chk("receipts record the same reported model",
    all(r["executor_reported_model"] == EXPECT_MODEL for r in (R0, R1, R2)))

# --- 4. Retry 0 / exceptions 0
chk("all retry_role original, attempt 1",
    all(r.get("retry_role") == "original" and r.get("attempt_number") == 1
        for r in (R0, R1, R2)))
L = open(os.path.join(ROOT, "LEDGER.md")).read()
chk("ledger: exceptions 0 and retries 0",
    "campaign exceptions: 0" in L and "retries used: 0" in L)

# --- 5. Dry-run is identity/harness evidence only; no substantive use
chk("dry-run receipt declares no substantive inference",
    "NONE" in R0.get("substantive_inference", ""))
chk("smoke receipts declare no substantive inference",
    all("NONE" in r.get("substantive_inference", "") for r in (R1, R2)))
for nm in ("smoke-s1", "smoke-s2"):
    txt = open(os.path.join(ROOT, nm, "smoke-checklist-result.md")).read()
    chk(f"{nm} checklist judges form only (no H-hypothesis wording)",
        "H1" not in txt and "H2" not in txt and "H3" not in txt)

# --- 6. Frozen digests exact (files and receipts)
chk("S1 rendered prompt sha == frozen S1 digest",
    sha(os.path.join(ROOT, "smoke-s1/rendered-prompt.txt")) == S1_DIGEST
    and R1["rendered_prompt_sha256"] == S1_DIGEST)
chk("S2 rendered prompt sha == frozen S2 digest",
    sha(os.path.join(ROOT, "smoke-s2/rendered-prompt.txt")) == S2_DIGEST
    and R2["rendered_prompt_sha256"] == S2_DIGEST)
chk("S1/S2 rendered prompts byte-identical to prereg fixtures",
    open(os.path.join(ROOT, "smoke-s1/rendered-prompt.txt"), "rb").read()
    == open(os.path.join(PREREG, "fixtures/P1.md"), "rb").read()
    and open(os.path.join(ROOT, "smoke-s2/rendered-prompt.txt"), "rb").read()
    == open(os.path.join(PREREG, "fixtures/P2.md"), "rb").read())

# --- 7. Decoded wire payload byte-equivalence (925/925, 1067/1067)
w1, log1 = decode_wire(os.path.join(ROOT, "smoke-s1/debug-transcript.log"))
w2, log2 = decode_wire(os.path.join(ROOT, "smoke-s2/debug-transcript.log"))
p1 = open(os.path.join(ROOT, "smoke-s1/rendered-prompt.txt")).read()
p2 = open(os.path.join(ROOT, "smoke-s2/rendered-prompt.txt")).read()
chk("decoded S1 wire content == P1 bytes (925/925)",
    w1 and w1["messages"][0]["content"] == p1 and len(p1) == 925)
chk("decoded S2 wire content == P2 bytes (1067/1067)",
    w2 and w2["messages"][0]["content"] == p2 and len(p2) == 1067)
w0, log0 = decode_wire(os.path.join(ROOT, "dryrun/debug-transcript.log"))
chk("decoded dry-run wire content == dry-run prompt bytes",
    w0 and w0["messages"][0]["content"]
    == open(os.path.join(ROOT, "dryrun/dryrun-prompt.txt")).read())

# --- 8. Checklists 5/5 and CLEARED
for nm, fx in (("smoke-s1", "P1"), ("smoke-s2", "P2")):
    txt = open(os.path.join(ROOT, nm, "smoke-checklist-result.md")).read()
    chk(f"{nm} checklist 5/5 PASS and {fx} CLEARED",
        txt.count("| PASS |") == 5 and "PASS (5/5)" in txt and "CLEARED" in txt)

# --- 9. Raw/debug hashes recomputed == receipts
for r, nm in ((R0, "dryrun"), (R1, "smoke-s1"), (R2, "smoke-s2")):
    chk(f"{nm} raw-output sha re-derives",
        sha(os.path.join(ROOT, nm, "raw-output.json")) == r["raw_output_sha256"])
    chk(f"{nm} debug-transcript sha re-derives",
        sha(os.path.join(ROOT, nm, "debug-transcript.log")) == r["debug_transcript_sha256"])

# --- 10. Credential scan clean in all transcripts
for nm, lg in (("dryrun", log0), ("smoke-s1", log1), ("smoke-s2", log2)):
    chk(f"{nm} credential redacted",
        "Bearer <REDACTED>" in lg and not re.search(r"Bearer [A-Za-z0-9_\-\.]{20,}", lg))

# --- 11. Token usage machine-reconciled from raw responses
chk("S1 input_tokens canonical 260 (raw == receipt)",
    RAW1["usage"]["input_tokens"] == 260 == R1["usage"]["input_tokens"])
chk("S2 usage reconciles raw == receipt",
    RAW2["usage"]["input_tokens"] == R2["usage"]["input_tokens"]
    and RAW2["usage"]["output_tokens"] == R2["usage"]["output_tokens"])
chk("dry-run usage reconciles raw == receipt",
    RAW0["usage"]["input_tokens"] == R0["usage"]["input_tokens"]
    and RAW0["usage"]["output_tokens"] == R0["usage"]["output_tokens"])

# --- 12. Accounting lines in LEDGER
for needle in ("dry-run: **1**", "smoke: **2**", "scored: **0**",
               "total used: **3/50**", "planned remaining: **36**",
               "headroom: **11 untouched**",
               "reserve: **18 untouched**",
               "doctrine / marker mutation: **0**"):
    chk(f"ledger accounting line: {needle}", needle in L)

# --- 13. Prereg package integrity (39/39) + byte-identity vs HEAD
r = subprocess.run([sys.executable, os.path.join(PREREG, "static_checks.py")],
                   capture_output=True, text=True)
chk("prereg static checks ALL PASS (39/39)", "ALL PASS" in r.stdout and r.returncode == 0)
g = subprocess.run(["git", "-C", REPO, "status", "--porcelain",
                    "reviews/2026-08-13-issue115-t2-probe-prereg"],
                   capture_output=True, text=True)
chk("prereg package untouched in working tree", g.stdout.strip() == "", g.stdout)

print()
if FAILURES:
    print("PREFIX CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("PREFIX CHECKS: ALL PASS")
