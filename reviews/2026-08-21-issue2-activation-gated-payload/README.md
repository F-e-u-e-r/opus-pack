# ② Activation-gated / dormant-branch trojan shape — doctrine gate evidence

**What landed** (narrow doctrine change):
- `operational-rigor §2` — a new canonical bullet **"Activation-gated payload
  (dormant branch)"** naming the shape, with the criterion (harmful defined by
  authorization/adversity not impact magnitude; indirect/deferred predicates
  traced to material effect; disclosure and labels never clear a harmful branch;
  opaque-material logic fails closed), carrying a single `unprobed` marker + the
  Provenance entry.
- `skill-vetting §2` — a short **bare-pointer mirror** that routes to the canonical
  clause and adds only skill-vetting-specific context (applies to skill prose as
  well as executable helpers; supplements the exfiltration bullet's default-path
  scope; the §1 fixture obligation still holds for executable candidates) + one
  ✅/❌ pair. It owns **no** criterion copy and **no** second marker/debt.

**The gap it closes.** The install-gate checklist named effect-shapes (exfil,
config self-propagation, obfuscation) but not the *gating dimension*. The
exfiltration coverage is scoped to the *default* execution path, so a payload
gated behind an activation predicate (a date, a trigger word, an env value, an
Nth-run count, a dormant branch) evaded it; the fail-closed read blocks such a
payload only if the reviewer *notices* the branch, which no rule directed them to
enumerate. This is a **discovery** gap, not a permission gap.

**Provenance / honesty.** Distilled from an attested incident family of
time/trigger-gated skill trojans (cited as shape, not first-hand reproduced — no
such artifact was cloned or executed).

**Review trail — NOT a joint PROCEED.** A three-round cross-family review
(gpt-5.6-luna + gpt-5.6-sol, both max effort, mutually blind). Rounds:
R1 luna FIX / sol PROCEED → R2 luna FIX / sol FIX → **R3 luna PROCEED / sol FIX**.
The 2–3 round cap was reached without a joint PROCEED. Sol's remaining round-3
items split into factual corrections (accepted and folded: an inspectable ungated
flip fixture, a non-exfiltration failing fixture, and a "permits" → "does not
direct discovery" recast) and two substantive policy splits, which the owner
adjudicated:
1. **Harmful** is defined by authorization and adversity, not impact magnitude (a
   disclosed, user-authorized high-impact tool doing its stated job is not
   harmful; a euphemistically-disclosed exfil still is).
2. **Placement** is Option A: one canonical rule in operational-rigor §2 + a
   bare-pointer mirror in skill-vetting §2 (no duplicated criterion).

This record is **not** a reviewer-consensus claim. Full per-round verdicts are in
`verdicts/` (r1–r3 × luna/sol).

**Behavioral effectiveness is NOT probed.** No bare-vs-ruled behavioral probe was
run — that measures transmission/effectiveness, a separate question from whether
the shape is real and the checklist lacked it. The canonical rule therefore ships
`unprobed`; its probe joins the standing #115 queue. This is reviewed security
doctrine whose behavioral effectiveness has not yet been probed — not unreviewed.

**Static discrimination.** 9 inert synthetic fixtures (`fixtures/`) discriminate
9/9 as intended under the landed criterion — see `STATIC-DISCRIMINATION.md`.
