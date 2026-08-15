#!/usr/bin/env python3
"""Landing gate for the T5-placement disposition record.

`disposition_checks.py` stays frozen at its 50 assertions and is
executed here as one item; this file adds the landing conditions —
record immutability since the review, the gate trail's completeness and
honesty, and the boundaries the disposition must not cross.
Read-only; exits non-zero on any failure."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
DOCTRINE = "skills/skill-authoring/SKILL.md"
PRE_DISPOSITION_MAIN = "66d9144a7cb49714cb2132280161c16b47924d96"
REVIEWED_DISPOSITION_SHA = "159a381fa20fe82f"          # prefix recorded at review time
FAILURES = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if not ok and detail else ""))
    if not ok:
        FAILURES.append(name)

def rd(p):
    with open(p, "rb") as f:
        return f.read()

def flatten(text):
    """Strip blockquote/list markers, THEN whitespace-normalise — the
    recurring trap: a wrapped or marker-prefixed phrase is invisible to
    a line-bounded comparison."""
    return re.sub(r"\s+", " ", re.sub(r"^\s*[>|-]\s?", "", text, flags=re.M))

def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout.strip()

# ---- 1. The record is byte-identical to what the reviewers cleared ----
disp = rd(os.path.join(ROOT, "DISPOSITION.md"))
check("DISPOSITION.md sha256 still starts with the reviewed value",
      hashlib.sha256(disp).hexdigest().startswith(REVIEWED_DISPOSITION_SHA),
      hashlib.sha256(disp).hexdigest()[:16])

# ---- 2. The frozen suite still passes, unmodified at 50 ----
r = subprocess.run([sys.executable, os.path.join(ROOT, "disposition_checks.py")],
                   capture_output=True, text=True)
npass = r.stdout.count("\nPASS  ") + (1 if r.stdout.startswith("PASS  ") else 0)
check("disposition_checks.py: 50/50 PASS, unmodified",
      r.returncode == 0 and npass == 50, f"exit={r.returncode} passes={npass}")
# Judge failure by LINE STRUCTURE, not substring: a passing check's own
# name can legitimately contain the token FAIL (e.g. "FAIL-SIGNAL").
_failing = [l for l in r.stdout.splitlines() if l.startswith("FAIL")]
check("the three mutant controls are present and passing",
      r.stdout.count("[mutant]") == 3 and not _failing, _failing[:2])

# ---- 3. Gate trail: complete, and honest about what happened ----
G = os.path.join(ROOT, "_gate")
for f in ("round1-luna-max-verdict-PROCEED.md", "round1-sol-max-verdict-HOLD.md",
          "round2-luna-max-verdict-HOLD.md", "round2-sol-max-verdict-HOLD.md",
          "GATE-CLOSURE.md"):
    check(f"gate trail present: {f}", os.path.exists(os.path.join(G, f)))
closure = flatten(rd(os.path.join(G, "GATE-CLOSURE.md")).decode())
for phrase, label in (
        ("There was NO round 3 and NO final 2/2 PROCEED", "no r3 / no 2/2 stated plainly"),
        ("Both reviewers returned HOLD", "r2 = HOLD x2 recorded"),
        ("was overstated", "the author's overclaim named"),
        ("outside the authorized blocking taxonomy", "owner adjudication recorded"),
        ("was BROADER than the owner contract it was serving", "packet over-widening owned by the author"),
        ("correctly identified two check-coverage weaknesses", "owner's framing carried"),
        ("do **not** prove that no semantically equivalent overclaim can ever be expressed",
         "checks described without overclaim"),
        ("not a semantic classifier", "content pin described precisely")):
    check(f"closure records: {label}", phrase in closure)
check("closure does NOT frame the reviewers as overruled or mistaken",
      not re.search(r"overrul|reviewers? (were )?(wrong|incorrect|mistaken)", closure, re.I))
# Both r2 verdicts must really be HOLDs, retained verbatim.
for f in ("round2-luna-max-verdict-HOLD.md", "round2-sol-max-verdict-HOLD.md"):
    check(f"{f} retains a HOLD verdict line",
          re.search(r"^HOLD:", rd(os.path.join(G, f)).decode().strip(), re.M) is not None)

# ---- 4. Disposition boundaries still hold ----
D = flatten(disp.decode())
scored = json.load(open(os.path.join(REPO, "reviews", "2026-08-15-issue115-t5p-scored",
                                     "SCORED-OUTCOME.json")))
check("outcome exact and unchanged", scored["outcome"] == "INCONCLUSIVE(MIXED-P1+MIXED-P2)"
      and "INCONCLUSIVE(MIXED-P1+MIXED-P2)" in D)
check("H1/H2/H3 still unresolved", "NONE" in scored["hypothesis_disposition"])
check("final disposition is RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)",
      "RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)" in D)
check("NEEDS-NEW-PROBE framed as obligation satisfied, not concern resolved",
      "execution obligation is therefore satisfied" in D
      and "underlying concern remains unresolved" in D
      and "RESOLVED` / `NO-CONCERN` is equally unavailable" in D)
reasoning = disp.decode().split("## Provenance")[0]
check("reasoning body carries no per-arm count and no band label",
      not re.findall(r"\b\d/6\b", reasoning) and not re.findall(r"\b(HIGH|LOW|MID)\b", reasoning))
check("39/50 closed and the remaining capacity carries no execution authority",
      "39/50 consumed" in D and "never an execution authority" in D)

# ---- 5. Nothing outside this record changed ----
check("canonical marker/doctrine blob identical to pre-disposition main",
      git("rev-parse", f"{PRE_DISPOSITION_MAIN}:{DOCTRINE}") == git("rev-parse", f"HEAD:{DOCTRINE}"))
dirty = git("diff", PRE_DISPOSITION_MAIN, "--", "skills", "metadata",
            "reviews/2026-08-09-issue115-scored-t5",
            "reviews/2026-08-13-issue115-doctrine-concern-adjudication",
            "reviews/2026-08-13-issue115-section-a-disposition",
            "reviews/2026-08-14-issue115-t5-placement-probe-prereg",
            "reviews/2026-08-15-issue115-t5p-prefix",
            "reviews/2026-08-15-issue115-t5p-scored")
check("doctrine, marker and every historical package byte-unchanged since #203",
      dirty == "", dirty[:200])
check("#115 still OPEN",
      json.loads(subprocess.run(["gh", "api", "repos/F-e-u-e-r/opus-pack/issues/115"],
                                capture_output=True, text=True).stdout)["state"] == "open")

print()
if FAILURES:
    print("CLOSURE CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("CLOSURE CHECKS: ALL PASS")
