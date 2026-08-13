#!/usr/bin/env python3
"""Mechanical verification for the T2 amendment DESIGN gate.
Read-only over canonical files; patch simulation happens on an
in-memory scratch copy only. Exits non-zero on any failure."""
import hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
TARGET = os.path.join(REPO, "skills/operational-rigor/references/external-systems.md")
BLOB_PIN = "28216fd898ed7041e98d2286a824abc2147013c4"
ANCHOR = "Run such mutations serially (one in flight), then resolve in"
FAILURES = []

def chk(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)

def sha(b):
    return hashlib.sha256(b).hexdigest()

# 1. Fresh target pin
blob = subprocess.run(["git", "-C", REPO, "rev-parse",
                       "HEAD:skills/operational-rigor/references/external-systems.md"],
                      capture_output=True, text=True).stdout.strip()
chk("target blob at HEAD == recorded pin", blob == BLOB_PIN, blob)
doc = open(TARGET, encoding="utf-8").read()
chk("anchor sentence occurs exactly once", doc.count(ANCHOR) == 1, doc.count(ANCHOR))
lines = doc.split("\n")
entry = "\n".join(lines[122:154]) + "\n"
frozen = open(os.path.join(ROOT, "target-entry-frozen.txt"), encoding="utf-8").read()
chk("frozen entry bytes == target lines 123-154", entry == frozen)

# 2. Patch simulation on scratch copy (M1-r2 exact byte patch:
#    one seam line replaced by six lines; nothing else changes)
OLD_LINE = "  evidence. Run such mutations serially (one in flight), then resolve in"
NEW_LINES = ("  evidence.\n"
             "  Where the destination can be queried under the request identity,\n"
             "  that read-back precedes any separate provider-side liveness/status\n"
             "  read — and a liveness/status read never substitutes for\n"
             "  destination-state evidence.\n"
             "  Run such mutations serially (one in flight), then resolve in")
chk("seam line unique and byte-exact", doc.count("\n" + OLD_LINE + "\n") == 1)
patched = doc.replace("\n" + OLD_LINE + "\n", "\n" + NEW_LINES + "\n", 1)
chk("patch changes the file (scratch only)", patched != doc)
# Removal + seam-rejoin reproduces the original byte-exactly
rejoined = patched.replace("\n" + NEW_LINES + "\n",
                            "\n" + "  evidence." + " " +
                            "Run such mutations serially (one in flight), then resolve in" + "\n", 1)
chk("removing insertion and rejoining seam reproduces original",
    rejoined.replace("\n  evidence. Run such mutations serially (one in flight), then resolve in\n",
                      "\n" + OLD_LINE + "\n", 1) == doc)
chk("anchor is a whole line post-patch",
    "\n  Run such mutations serially (one in flight), then resolve in\n" in patched)
# Anchor + branch bodies byte-identical post-patch
for inv_name, needle in [
    ("anchor sentence retained", ANCHOR),
    ("inv1 serial execution", "Run such mutations serially (one in flight)"),
    ("inv2 blind-retry ban", "never blindly"),
    ("inv3 no-query immediate terminal", 'report "uncertain" as a\n  TERMINAL state immediately — never invent a probe loop, never retry'),
    ("inv6 authoritative-read rule", "only an AUTHORITATIVE read settles anything"),
    ("inv7 both-axes absence", "evidence that covers BOTH axes"),
    ("inv8 idempotency carve-out", "documented idempotency guarantee whose retention window covers"),
    ("inv9 terminal uncertain at cap", 'terminal\n  "uncertain" — a report value the caller decides on, never a retry\n  trigger'),
]:
    chk(f"post-patch invariant carrier present: {inv_name}", needle in patched)
# Branch bodies byte-identical: everything after the anchor text is
# unchanged between original and patched.
tail_orig = doc.split("Run such mutations serially", 1)[1]
tail_patched = patched.split("Run such mutations serially", 1)[1]
chk("branch bodies byte-identical from anchor onward",
    tail_orig == tail_patched)
# Everything before the seam is unchanged too.
head_orig = doc.split("\n" + OLD_LINE + "\n", 1)[0]
chk("bytes before the seam unchanged", patched.startswith(head_orig + "\n  evidence.\n"))

# 3. E-similarity: no >=8-word verbatim run shared with E bytes
E = open(os.path.join(ROOT, "E-arm-reference.txt"), encoding="utf-8").read().lower()
def words(t):
    return re.findall(r"[a-z0-9'-]+", t.lower())
ew = words(E)
egrams = {tuple(ew[i:i+8]) for i in range(len(ew) - 7)}
CANDS = {
    "M1": "Interrogate destination state before any provider-wide liveness/status read. Where a destination query exists, the read under the request identity is the first provider-side read; liveness/status reads may follow only afterward and never stand in for destination-state evidence.",
    "M1-r2": "Where the destination can be queried under the request identity, that read-back precedes any separate provider-side liveness/status read — and a liveness/status read never substitutes for destination-state evidence.",
    "M2": "Where a destination query exists, the read under the request identity is the first provider-side read — before any provider-wide liveness/status read.",
    "M3": "After such a timeout the destination read-back is the first provider-side operation — no provider-wide liveness or status read precedes it, and one may follow only after the interrogation. Provider health is never destination evidence; this ordering is strict.",
}
for name, text in CANDS.items():
    cw = words(text)
    shared = [g for g in (tuple(cw[i:i+8]) for i in range(len(cw) - 7)) if g in egrams]
    chk(f"{name}: no 8-word verbatim run shared with E", not shared, shared[:2])

# 4. No canonical mutation by this gate
g = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "skills"],
                   capture_output=True, text=True)
chk("skills/ untouched in working tree", g.stdout.strip() == "", g.stdout)

print()
if FAILURES:
    print("DESIGN CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("DESIGN CHECKS: ALL PASS")
