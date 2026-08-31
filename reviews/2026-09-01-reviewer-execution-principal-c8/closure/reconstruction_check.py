#!/usr/bin/env python3
"""Machine-proof: landed doctrine == archived v4 + exactly MOD-AXIS-MODE +
declared adaptations A1/A2/A3 (+ marker/provenance placement). Exit 0 = ALL PASS."""
import hashlib, re, sys
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def rd(p): return open(p, encoding='utf-8').read()
ok=[]
def chk(cid,desc,cond):
    ok.append(cond); print(("PASS" if cond else "FAIL"),f"{cid}: {desc}"); return cond

V4="../gate-record/DESIGN-v4.md"; REP="DESIGN-v4-owner-repair.md"
DR="/Users/ccso/Developer/fable/skills/delegation-and-review/SKILL.md"
CMR="/Users/ccso/Developer/fable/skills/cross-model-review/SKILL.md"
REF="/Users/ccso/Developer/fable/skills/delegation-and-review/references/reviewer-capability-receipt.md"

chk("R1","packaged v4 == frozen 07f53b8c…", sha(V4)=="07f53b8cf8b07065705df4d33c18fd09bab0f08816b063bc67e7d15bb68f7470")
old="read_reach:             none | <roots/breadth> | unknown   # none = packet-only: no repository/host read reach"
new="read_reach:             none | <roots/breadth> | unknown   # none = no repository/host read reach (this axis only — mode is decided by §5's reviewer-directed-capability trigger, never by one field)"
v4=rd(V4); chk("R2","MOD-AXIS-MODE unique target in packaged v4", v4.count(old)==1)
import hashlib as H
chk("R3","re-derived repair == frozen 788f80c7… == packaged repair file",
    H.sha256(v4.replace(old,new).encode()).hexdigest()=="788f80c7ac35178026b485f4ee11012a2308cc789eef70530ec5082a9fb0d97a"==sha(REP))

dr_b=rd("landed-dr-bullet.txt"); cmr_b=rd("landed-cmr-bullet.txt"); fence=rd("landed-schema-fence.txt")
dr=rd(DR); cmr=rd(CMR); ref=rd(REF)
chk("R4","D&R contains the generated bullet verbatim", dr_b in dr)
chk("R5","CMR contains the generated pointer verbatim (zero adaptations)", cmr_b in cmr)
A1=("The receipt's normative fields and semantics are\n"
    "  `references/reviewer-capability-receipt.md` — load it when recording or\n"
    "  consuming a reviewer capability receipt.")
rep=rd(REP)
raw_block="\n".join(l[2:] if l.startswith("> ") else l[1:] for l in rep.splitlines() if False) # placeholder
# re-extract §4 block from repair the same way gen_landed did:
out,on=[],False
for l in rep.splitlines():
    if not on and l.startswith("> ") and "- **Artifact isolation is not principal confinement" in l: on=True
    if on:
        if l.startswith(">"): out.append(l[2:] if l.startswith("> ") else l[1:])
        elif out and l.strip()=="": break
raw_dr="\n".join(out).rstrip()+"\n"
chk("R6","generated D&R bullet == raw §4 extraction + exactly A1 (no second substantive correction)",
    dr_b.replace(" "+A1,"")==raw_dr)
out,on=[],False
for l in rep.splitlines():
    if not on and l.startswith("> ") and "- **Packet-only is a mode, not a property" in l: on=True
    if on:
        if l.startswith(">"): out.append(l[2:] if l.startswith("> ") else l[1:])
        elif out and l.strip()=="": break
raw_cmr="\n".join(out).rstrip()+"\n"
chk("R7","generated CMR pointer == raw §5 extraction exactly", cmr_b==raw_cmr)
A2fence=fence.replace("mode is decided by §5's reviewer-directed-capability trigger, never by one field",
                      "mode is decided by the reviewer-directed-capability trigger in the Mode section, never by one field")
chk("R8","reference schema fence == design fence + exactly A2", A2fence in ref and fence not in ref)
m=re.search(r"Semantics:\n\n(1\. \*\*`unknown` ≠ `disabled`\.\*\*.*?on its own evidence\.\n)", rep, re.S)
chk("R9","reference rules 1–5 == design §6 rules verbatim", bool(m) and m.group(1).rstrip()+"\n" in ref)
chk("R10","exactly one marker added, in the D&R bullet; none in CMR pointer or reference",
    dr_b.count("(`unprobed` — see Provenance)")==1 and cmr_b.count("unprobed")==0 and ref.count("`unprobed`")==0)

# content pins (owner §7 + locks) on LANDED bytes
chk("P1","authority-provenance pin: operator-owned dispatch layer (D&R bullet)", "operator-owned dispatch layer" in dr_b)
chk("P2","propose→grant preserved (D&R bullet)", "the grant that answers it is still the operator's" in dr_b)
chk("P3","artifact-mention neither necessary nor sufficient (D&R bullet)", "even when the artifact also\n  mentions it" in dr_b)
chk("P4","unknown ≠ disabled (bullet + reference)", "unknown is never disabled" in dr_b and "**`unknown` ≠ `disabled`.**" in ref)
chk("P5","MOD-AXIS-MODE gloss present in reference (this-axis-only)", "this axis only — mode is decided by the reviewer-directed-capability trigger in the Mode section, never by one field" in ref)
chk("P6","indirection-laundering exclusion present (reference Named probes)", "run whatever command the README\nnames" in ref or "run whatever command the README names" in ref)
chk("P7","transport never a live-capability trigger (CMR pointer)", "transport is never a" in cmr_b and "live-capability trigger" in cmr_b)
chk("P8","two-plane separation landed (fence headers)", "# plane 1 — EFFECTIVE CAPABILITY" in ref and "# plane 2 — AUTHORIZED ENVELOPE" in ref)
chk("P9","credential material exposure representable (reference)", "material: opaque|reviewer-readable|unknown" in ref)
chk("P10","plane-2 closed-world (reference rules)", "closed-world" in ref)
chk("P11","mode derived, never single-field alias (reference Mode section)", "never an alias of any single receipt field" in ref)
chk("P12","no runtime-enforcement claim (reference intro)", "nothing here claims the receipt is automated or enforced" in ref)

print(f"\n{sum(ok)}/{len(ok)} PASS"); sys.exit(0 if all(ok) else 1)
