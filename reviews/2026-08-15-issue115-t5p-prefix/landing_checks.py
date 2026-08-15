#!/usr/bin/env python3
"""Landing gate for the issue115-t5pprobe-v1 PREFIX evidence.

Every assertion is RECOMPUTED FROM THE ARTIFACTS — never from a
session narrative. `prefix_checks.py` stays frozen at its 37
assertions and is executed here as one item; this file adds the
remaining landing conditions. Read-only; exits non-zero on failure."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PKG = os.path.join(REPO, "reviews", "2026-08-14-issue115-t5-placement-probe-prereg")
MERGE = "6fe6813bcc35edb86a8b92b4aaaa7f9ba3459ef7"
PIN = "claude-haiku-4-5-20251001"
# The identity-probe anchor: byte-identical to the sealed campaign's and
# the T2 probe's dry-run prompt. Recomputed from that campaign's own
# committed artifact, not transcribed.
T2_DRYRUN = os.path.join(REPO, "reviews", "2026-08-13-issue115-t2probe-prefix",
                         "dryrun", "dryrun-prompt.txt")
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

SLOTS = [("dryrun", "dryrun-receipt.json"), ("smoke-s1", "s1-receipt.json"),
         ("smoke-s2", "s2-receipt.json")]
receipts = {s: json.load(open(os.path.join(ROOT, s, r))) for s, r in SLOTS}
raws = {s: json.load(open(os.path.join(ROOT, s, "raw-output.json"))) for s, _ in SLOTS}

# 1. Composition: exactly 1 dry-run + 2 smokes, 0 scored.
kinds = sorted(r["execution_kind"] for r in receipts.values())
check("exactly 1 DRY-RUN + 2 SMOKE, 0 SCORED",
      kinds == ["DRY-RUN", "SMOKE", "SMOKE"], kinds)

# 2. Three unique API message ids, receipts agreeing with raw outputs.
ids = [raws[s]["id"] for s, _ in SLOTS]
check("exactly 3 unique API message ids", len(set(ids)) == 3, ids)
check("every receipt id equals its raw-output id",
      all(receipts[s]["api_message_id"] == raws[s]["id"] for s, _ in SLOTS))

# 3. Identity pin on every invocation.
check("all resolved identities == the prereg pin",
      all(raws[s]["model"] == PIN for s, _ in SLOTS),
      {s: raws[s]["model"] for s, _ in SLOTS})

# 4. Dry-run digest equals the frozen identity-probe anchor.
dry = rd(os.path.join(ROOT, "dryrun", "rendered-prompt.txt"))
check("dry-run prompt == frozen identity-probe anchor bytes",
      dry == rd(T2_DRYRUN))

# 5/6. Smoke digests == frozen SLOT-TABLE; decoded wire byte equality.
table = rd(os.path.join(PKG, "SLOT-TABLE.md")).decode()
EXPECT_BYTES = {"smoke-s1": ("P1", 1580), "smoke-s2": ("P2", 1399)}
for slot, row in (("smoke-s1", "S1"), ("smoke-s2", "S2")):
    fid, nbytes = EXPECT_BYTES[slot]
    exp = re.search(r"^\| " + row + r" \| SMOKE \| P\d \|[^|]*\|[^|]*\| ([0-9a-f]{64}) \|$",
                    table, re.M).group(1)
    p = rd(os.path.join(ROOT, slot, "rendered-prompt.txt"))
    w = wire(slot)
    decoded = w["messages"][0]["content"].encode()
    check(f"{row}: digest == frozen SLOT-TABLE row",
          hashlib.sha256(p).hexdigest() == exp)
    check(f"{row}: decoded wire == prompt, {nbytes}/{nbytes} bytes",
          decoded == p and len(decoded) == nbytes and len(p) == nbytes,
          f"{len(decoded)}/{len(p)}")
    check(f"{row}: wire shape — 1 user turn, no system, 0 tools, no sampling override",
          len(w["messages"]) == 1 and w["messages"][0]["role"] == "user"
          and "system" not in w and "tools" not in w
          and not any(k in w for k in ("temperature", "top_p", "top_k")))

# 7. Zero retries / exceptions / pre-send aborts, asserted from the ledger.
led = rd(os.path.join(ROOT, "LEDGER.md")).decode()
check("ledger: retries 0, exceptions 0, pre-send aborts 0, zero-request 0",
      "retries used: 0" in led and "campaign exceptions: 0" in led
      and "pre-send aborts: 0" in led and "zero-request preflight events: 0" in led)
check("ledger carries the capacity-is-not-reserve sentence verbatim",
      "hard-cap remaining physical capacity is not an available reserve\n  and does not itself authorize execution." in led)
check("ledger retains the verifier-only correction (not laundered into a clean first pass)",
      "verifier-only correction" in led and "SLOT-TABLE.md" in led
      and "not a campaign exception" in led)

# 8. Smoke verdicts are 5/5 from the frozen checklist.
for slot, row in (("smoke-s1", "S1"), ("smoke-s2", "S2")):
    r = receipts[slot]
    check(f"{row}: smoke verdict PASS 5/5 with all five items PASS",
          r["smoke_verdict"] == "PASS 5/5"
          and all(v == "PASS" for v in r["smoke_checklist"].values()),
          r["smoke_checklist"])

# 9. NO substantive placement grading anywhere in the prefix records.
GRADING = [r"PASS-OWNER", r"FAIL-WRONG-OWNER", r"FAIL-STANDALONE",
           r"FAIL-OMIT", r"\bO1\b", r"\bO2\b", r"\bO3\b", r"\bO4\b",
           r"\bH1\b", r"\bH2\b", r"\bH3\b", r"folded into",
           r"correct(ly)? placed", r"owning bullet"]
records = [os.path.join(dp, fn) for dp, _, fns in os.walk(ROOT) for fn in fns
           if fn.endswith((".md", ".json")) and fn != "raw-output.json"]
hits = []
for f in records:
    t = rd(f).decode("utf-8", "replace")
    for pat in GRADING:
        if re.search(pat, t):
            hits.append((os.path.relpath(f, ROOT), pat))
check("no substantive placement grading in any prefix record "
      "(raw completions excluded — preserved verbatim, ungraded)",
      not hits, hits)

# 10. Credential scan: only explicit redaction markers.
leak = subprocess.run(
    ["grep", "-rEl", r"sk-ant-[A-Za-z0-9_-]{8,}|Bearer [A-Za-z0-9._-]{12,}", ROOT],
    capture_output=True, text=True).stdout.strip()
check("credential scan clean apart from redaction markers", leak == "", leak)
check("each debug transcript shows the Authorization header redacted",
      all("Bearer <REDACTED>" in rd(os.path.join(ROOT, s, "debug-transcript.log")).decode()
          for s, _ in SLOTS))

# 11. Nothing outside this evidence package changed.
dirty = subprocess.run(
    ["git", "-C", REPO, "diff", MERGE, "--",
     "reviews/2026-08-14-issue115-t5-placement-probe-prereg",
     "reviews/2026-08-08-issue115-stage2",
     "reviews/2026-08-13-issue115-t2probe-prefix",
     "skills", "metadata"], capture_output=True, text=True).stdout
check("prereg / sealed campaign / T2 prefix / skills / metadata bytes unchanged",
      dirty == "", dirty[:200])
m = json.load(open(os.path.join(PKG, "MANIFEST.json")))
check("T2 headroom 11 and stage-2 reserve 18 both still NOT USED",
      "NOT USED" in m["budget"]["t2probe_headroom_11"]
      and "NOT USED" in m["budget"]["stage2_reserve_18"])
check("#115 still OPEN",
      json.loads(subprocess.run(
          ["gh", "api", "repos/F-e-u-e-r/opus-pack/issues/115"],
          capture_output=True, text=True).stdout)["state"] == "open")

# 12. The frozen prefix suite still passes, unmodified.
r = subprocess.run([sys.executable, os.path.join(ROOT, "prefix_checks.py")],
                   capture_output=True, text=True)
npass = r.stdout.count("\nPASS  ") + (1 if r.stdout.startswith("PASS  ") else 0)
check("prefix_checks.py: 37/37 PASS, unmodified",
      r.returncode == 0 and npass == 37, f"exit={r.returncode} passes={npass}")

print()
if FAILURES:
    print("LANDING GATE: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("LANDING GATE: ALL PASS")
