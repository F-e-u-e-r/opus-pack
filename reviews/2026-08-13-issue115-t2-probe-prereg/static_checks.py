#!/usr/bin/env python3
"""Mechanical self-checks for the issue115-t2probe-v1 prereg package.
Read-only; exits non-zero on any failure. Run from anywhere:
paths resolve relative to this file. Covers the standing hygiene
rule: every hash cited in the package is re-derivable by script."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
SEALED = os.path.join(REPO, "reviews", "2026-08-08-issue115-stage2")
DOCTRINE_BLOB = "896f7478172ae2c8f6c9d5bb6f54c2f2976beff6"
ANCHOR = "settle what actually landed at the destination first"
FAILURES = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)

def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def rd(path):
    with open(path, "rb") as f:
        return f.read()

# 1. Byte-identity of the sealed anchors (recomputed from BOTH sides).
check("P1 == sealed T2S2 (bytes)",
      rd(os.path.join(ROOT, "fixtures/P1.md"))
      == rd(os.path.join(SEALED, "fixtures/T2S2.md")))
check("CURRENT-clause == sealed T2-clause (bytes)",
      rd(os.path.join(ROOT, "wrappers/clauses/CURRENT-clause.txt"))
      == rd(os.path.join(SEALED, "wrappers/clauses/T2-clause.txt")))

# 2. Forbidden-token scan on P2 (lexical independence from P1/T2S1).
p2 = rd(os.path.join(ROOT, "fixtures/P2.md")).decode("utf-8").lower()
for tok in (r"\bpayments?\b", r"\bsubmit\b", r"\bprovider\b",
            r"\bstatus\b", r"\bhealth\b", r"\bget\b", r"7841",
            r"\bcold\b", r"\border\b"):
    check(f"P2 forbidden token absent: {tok}",
          re.search(tok, p2) is None)

# 3. No ordering hint in either fixture (no 'first call X' coaching).
for fid in ("P1", "P2"):
    fx = rd(os.path.join(ROOT, f"fixtures/{fid}.md")).decode("utf-8").lower()
    check(f"{fid} carries no 'call ... first' ordering hint",
          re.search(r"(first[^.\n]{0,40}\bcall\b)|(\bcall\b[^.\n]{0,40}first)", fx) is None)

# 3b. No experiment-cue vocabulary in P2's executor-visible bytes
#     (P1 is sealed bytes and carries its recorded historical comment).
for cue in (r"\bprobe\b", r"\bcontrol\b", r"\bconfound\b",
            r"\bexperiment\w*\b", r"\barms?\b", r"\bbare\b",
            r"\bruled\b", r"\bcampaign\b", r"needs-new-probe",
            r"\btransmission\b"):
    check(f"P2 experiment-cue absent: {cue}",
          re.search(cue, p2) is None)

# 4. Doctrine pin: blob at HEAD matches the recorded sha1, anchor
#    sentence present exactly once in the working-tree doctrine file.
blob = subprocess.run(
    ["git", "-C", REPO, "rev-parse",
     "HEAD:skills/delegation-and-review/SKILL.md"],
    capture_output=True, text=True).stdout.strip()
check("doctrine blob @HEAD == recorded pin", blob == DOCTRINE_BLOB, blob)
doc = rd(os.path.join(REPO, "skills/delegation-and-review/SKILL.md")).decode("utf-8")
check("anchor sentence occurs exactly once in doctrine",
      doc.count(ANCHOR) == 1, str(doc.count(ANCHOR)))

# 5. Explicit-control wording never appears in any skill file.
hits = subprocess.run(
    ["grep", "-rl", "ADDITIONAL ORDERING REQUIREMENT",
     os.path.join(REPO, "skills")],
    capture_output=True, text=True).stdout.strip()
check("explicit-control addendum absent from skills/", hits == "", hits)

# 6. MANIFEST consistency: regenerating in a temp comparison must
#    match committed bytes (run make_manifest.py first; here we only
#    recompute the recorded hashes).
mpath = os.path.join(ROOT, "MANIFEST.json")
if os.path.exists(mpath):
    m = json.load(open(mpath))
    ok = True
    for fx in m["fixtures"]:
        for key in ("file", "clause_file", "addendum_file", "rubric",
                    "predicate"):
            skey = {"file": "content_sha256",
                    "clause_file": "clause_sha256",
                    "addendum_file": "addendum_sha256",
                    "rubric": "rubric_sha256",
                    "predicate": "predicate_sha256"}[key]
            if sha(os.path.join(ROOT, fx[key])) != fx[skey]:
                ok = False
    for p, h in m["documents"].items():
        if sha(os.path.join(ROOT, p)) != h:
            ok = False
    check("MANIFEST recorded hashes match recomputation", ok)
    check("MANIFEST.sha256 matches MANIFEST.json",
          open(os.path.join(ROOT, "MANIFEST.sha256")).read().split()[0]
          == sha(mpath))
    # Sealed-anchor values inside the manifest re-derive.
    sa = m["sealed_anchors"]
    check("manifest sealed anchor T2S2 re-derives",
          sa["T2S2_content_sha256"] == sha(os.path.join(SEALED, "fixtures/T2S2.md")))
    check("manifest sealed anchor T2-clause re-derives",
          sa["T2_clause_sha256"] == sha(os.path.join(SEALED, "wrappers/clauses/T2-clause.txt")))
else:
    check("MANIFEST.json exists", False)

# 7. Every 64-hex hash cited in the prereg main document is a member
#    of the recomputed value set (no hand-typed hashes).
prereg = rd(os.path.join(ROOT, "T2-PROBE-PREREG-v1.md")).decode("utf-8")
known64 = {
    sha(os.path.join(ROOT, "fixtures/P1.md")),
    sha(os.path.join(ROOT, "wrappers/clauses/CURRENT-clause.txt")),
    sha(os.path.join(SEALED, "fixtures/T2S2.md")),
    sha(os.path.join(SEALED, "wrappers/clauses/T2-clause.txt")),
}
check("SMOKE-CHECKLIST.md exists and nonempty",
      os.path.exists(os.path.join(ROOT, "SMOKE-CHECKLIST.md"))
      and len(rd(os.path.join(ROOT, "SMOKE-CHECKLIST.md"))) > 0)

# 7b. Smoke item-5 satisfiability: every frozen endpoint symbol is an
#     exact substring of its fixture's bytes.
SMOKE_SYMBOLS = {
    "P1": ["payments.get", "payments.provider_status",
           "payments.submit"],
    "P2": ["shipping.find_labels", "shipping.gateway_ping",
           "shipping.create_label"],
}
for fid, symbols in SMOKE_SYMBOLS.items():
    fx_bytes = rd(os.path.join(ROOT, f"fixtures/{fid}.md")).decode("utf-8")
    for sym in symbols:
        check(f"smoke item-5 satisfiable: {fid} contains {sym}",
              sym in fx_bytes)
cited64 = set(re.findall(r"\b[0-9a-f]{64}\b", prereg))
check("all 64-hex hashes in prereg re-derive", cited64 <= known64,
      str(cited64 - known64))
head_of_branch = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "b68a4fb25b796a9bcf4be9eb7aa8d45de322cc19"],
    capture_output=True, text=True).stdout.strip()
cited40 = set(re.findall(r"\b[0-9a-f]{40}\b", prereg))
check("all 40-hex ids in prereg re-derive",
      cited40 <= {head_of_branch, DOCTRINE_BLOB}, str(cited40))

print()
if FAILURES:
    print("STATIC CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("STATIC CHECKS: ALL PASS")
