#!/usr/bin/env python3
"""Compose the reference file and perform the four SKILL.md insertions.
Every non-extraction adaptation is DECLARED on stdout (A1 was declared by
gen_landed.py). Unique-anchor asserted for every mutation."""
import re, sys

d = open("DESIGN-v4-owner-repair.md", encoding="utf-8").read()
dr_bullet = open("landed-dr-bullet.txt", encoding="utf-8").read()
cmr_bullet = open("landed-cmr-bullet.txt", encoding="utf-8").read()
fence = open("landed-schema-fence.txt", encoding="utf-8").read()

# --- rules 1–5 verbatim from design §6 ---
m = re.search(r"Semantics:\n\n(1\. \*\*`unknown` ≠ `disabled`\.\*\*.*?on its own evidence\.\n)", d, re.S)
assert m, "rules 1-5 extraction failed"
rules15 = m.group(1).rstrip() + "\n"

# --- A2: design-internal section ref in the schema gloss -> in-file Mode section ---
fence_ref = fence.replace(
 "mode is decided by §5's reviewer-directed-capability trigger, never by one field",
 "mode is decided by the reviewer-directed-capability trigger in the Mode section, never by one field")
assert fence_ref != fence, "A2 substitution missed"
print("DECLARED ADAPTATION A2 (placement): schema gloss's design-internal '§5' ref → in-file Mode section; semantics identical.")

REF = f"""# Reviewer Capability Receipt

Normative schema and semantics for the capability receipt that
delegation-and-review §3's execution-principal bullet requires a dispatcher
to record where the harness can assert it. Doctrine plus a harness-assertion
CANDIDATE: nothing here claims the receipt is automated or enforced, and no
runtime enforcement (sandbox, VM/container, seccomp, network or credential
broker) is designed or mandated here. Where this file and the §3 bullet
state the same consequence, the §3 bullet is canonical — this file owns the
schema and field semantics.

## Mode

`mode: packet-only | live` — a derived classification, decided by the
reviewer-directed-capability trigger over the effective envelope: any
reviewer-directed read, exec, network, or tool capability makes the run
live. Mode is never an alias of any single receipt field — a receipt with
`read_reach: none` beside reviewer-directed exec, network, or tool reach is
live.

## Two planes

```
{fence_ref}```

## Semantics

{rules15}
6. **Evidence discipline for assertions.** Run metadata (model, reasoning
   effort, applied sandbox mode) evidences the applied posture; it is never
   by itself effective-capability evidence, and never translates into
   `exec_reach`/`net_reach` values. Each run's receipt cites its own run's
   evidence — never a guarantee assumed from prior runs. Session-specific
   assertability observations belong in evidence packages, not here.

## Named probes

A named probe is identified concretely by the operator-owned dispatch layer
— the command, capability, or bounded action itself. A preauthorization
whose content is artifact-selected ("run whatever command the README
names") is artifact authority laundered through the operator layer, not a
grant. A reviewer may propose a probe; the operator's explicit grant that
answers it is legitimate authority.
"""
open("/Users/ccso/Developer/fable/skills/delegation-and-review/references/reviewer-capability-receipt.md","w",encoding="utf-8").write(REF)
print("DECLARED ADAPTATION A3 (placement): reference file framing — header/intro, Mode section (owner mode-representability lock), rule-6 normative kernel replacing the design's session-specific assertability example, Named-probes section carrying the design §11 indirection line + propose→grant; rules 1–5 and the schema fence are verbatim extractions.")

# --- D&R SKILL.md: bullet insertion ---
p = "/Users/ccso/Developer/fable/skills/delegation-and-review/SKILL.md"
t = open(p, encoding="utf-8").read()
anchor = "  gets the independent copy §3 requires. (`unprobed` — see Provenance.)\n"
assert t.count(anchor) == 1, "DR bullet anchor not unique"
t = t.replace(anchor, anchor + dr_bullet)
# --- D&R provenance insertion (before closing paragraph) ---
close = "Stable behavioral rules; re-check\n"
assert t.count(close) == 1, "DR provenance anchor not unique"
PROV = open("dr-provenance-entry.txt", encoding="utf-8").read()
t = t.replace(close, PROV + "\n" + close)
open(p, "w", encoding="utf-8").write(t)
print("D&R SKILL.md: bullet inserted after read-only-critic; provenance entry inserted before closing paragraph.")

# --- CMR SKILL.md: pointer insertion + provenance ---
p2 = "/Users/ccso/Developer/fable/skills/cross-model-review/SKILL.md"
t2 = open(p2, encoding="utf-8").read()
anchor2 = "  honor repo/org policy on sending code out.\n"
assert t2.count(anchor2) == 1, "CMR bullet anchor not unique"
t2 = t2.replace(anchor2, anchor2 + cmr_bullet)
close2 = "Re-verify\nline:"
assert t2.count(close2) == 1, "CMR provenance anchor not unique"
CPROV = open("cmr-provenance-entry.txt", encoding="utf-8").read()
t2 = t2.replace(close2, CPROV + "\n" + close2)
open(p2, "w", encoding="utf-8").write(t2)
print("CMR SKILL.md: pointer bullet inserted after nothing-secret bullet; provenance entry inserted before the closing re-verify line.")
