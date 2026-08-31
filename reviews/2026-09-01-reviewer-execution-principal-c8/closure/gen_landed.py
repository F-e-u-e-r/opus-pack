#!/usr/bin/env python3
"""Generate the landed doctrine texts FROM the repaired design bytes.

The generator IS the faithful-reconstruction proof: every landed block is a
mechanical extraction from DESIGN-v4-owner-repair.md plus the adaptations
DECLARED below (printed to stdout). Outputs:
  landed-dr-bullet.txt, landed-cmr-bullet.txt, landed-schema-fence.txt
"""
import re, sys
d = open("DESIGN-v4-owner-repair.md", encoding="utf-8").read()
lines = d.splitlines()

def quoted_block(start_marker, stop_marker):
    out, on = [], False
    for l in lines:
        if not on and l.startswith("> ") and start_marker in l:
            on = True
        if on:
            if l.startswith(">"):
                out.append(l[2:] if l.startswith("> ") else l[1:])
            elif out and l.strip() == "":
                break
        if on and stop_marker and stop_marker in l:
            break
    return "\n".join(out).rstrip() + "\n"

# --- D&R §3 bullet: the §4 candidate block ---
dr = quoted_block("- **Artifact isolation is not principal confinement", None)
ADAPT1 = ("The receipt's normative fields and semantics are\n"
          "  `references/reviewer-capability-receipt.md` — load it when recording or\n"
          "  consuming a reviewer capability receipt.")
anchor = "(surplus reach beyond the envelope is\n  a recorded risk, not a licensed power)."
assert dr.count(anchor) == 1, "DR anchor not unique"
dr = dr.replace(anchor, anchor + " " + ADAPT1)
open("landed-dr-bullet.txt", "w", encoding="utf-8").write(dr)
print("DECLARED ADAPTATION A1 (placement): reference-pointer sentence inserted after the surplus-reach clause.")

# --- CMR §2 bullet: the §5 candidate block, byte-exact, no polish ---
cmr = quoted_block("- **Packet-only is a mode, not a property", None)
open("landed-cmr-bullet.txt", "w", encoding="utf-8").write(cmr)
print("CMR bullet: extracted verbatim, ZERO adaptations (owner rule: no polish).")

# --- receipt schema fence from §6 (repaired) ---
m = re.search(r"```\n(# plane 1 — EFFECTIVE CAPABILITY.*?)```", d, re.S)
assert m, "schema fence not found"
open("landed-schema-fence.txt", "w", encoding="utf-8").write(m.group(1))
print("Schema fence: extracted verbatim (carries the MOD-AXIS-MODE read_reach line).")

for f in ("landed-dr-bullet.txt","landed-cmr-bullet.txt","landed-schema-fence.txt"):
    t=open(f,encoding="utf-8").read()
    print(f"{f}: {len(t.splitlines())} lines")
