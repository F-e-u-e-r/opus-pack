# ① Exfiltration-channel reframe — doctrine gate evidence

**What landed** (narrow, single-carrier): the `skill-vetting §2` "Exfiltration-shaped
**commands**" bullet is reframed to "Exfiltration-shaped **channels**" — judging the
data flow and the disclosure, not the transport name. `operational-rigor §2` and
`security-architect` are untouched (op-rigor §2 has no exfil rule; security-architect
owns the design lens, not the vetting shape).

**Two layers (Option X, owner-adjudicated):**
- **(a) Legacy high-signal triggers** — an external `curl/wget/nc` command or a
  sensitive-credential read stays a §2 finding that must be explained, and need not
  first be shown to carry a secret (a hit is not automatic proof — it blocks unless the
  disclosed purpose explains it). No regression of the inherited detection.
- **(b) Generalized criterion** — for every other channel, a hit is a private-data
  disclosure the disclosed purpose does not need, over any path: renderer/resource
  auto-fetch (secret in a URL/`Referer`), DNS-label (secret in a hostname), header
  metadata, or presence/count/order. The tell is the disclosure, not the recipient — a
  secret piggybacked on a legit API call is a hit; a disclosed purpose never launders an
  unnecessary export. No-secret images/DNS/library calls and own-credential auth clear.
  Pure timing/cache side-channels are honestly scoped out.

**Review status — NOT a joint PROCEED.** Three-round cross-family gate (gpt-5.6-luna +
gpt-5.6-sol, max effort, mutually blind): R1 luna PROCEED / sol FIX → R2 both FIX
(convergent) → **R3 luna PROCEED / sol FIX**. The round cap was reached with no final
2/2. Sol's factual/precision items were folded each round; the final bounded precision
fixes (Sol-1 predicate keys on disclosure not path; Sol-2 curl/safe-harbor
reconciliation) and the finding-to-explain layering (**Option X**) were
owner-adjudicated, **not represented as 2/2 consensus**. Full per-round verdicts in
`verdicts/`.

**Probe status.** Behavioral transmission/effectiveness is NOT probed. This reframe
extends `skill-vetting §2`'s existing trojan-shape checklist and relies on this skill's
**existing `unprobed` covenant** — it adds **no new marker**; a future ①-specific probe
is a #115 routing decision, not a second inline marker. Status: **SHIPPED candidate
wording / UNPROBED EFFECTIVENESS**.

**Static discrimination.** 10 inert synthetic fixtures (`fixtures/`) discriminate 10/10
under the landed wording — see `STATIC-DISCRIMINATION.md`. This establishes only that
the wording distinguishes the intended threat shapes with no obvious blanket-ban
regression; it does NOT prove a weaker reviewer will find the exfil, that effectiveness
is demonstrated, or that all covert channels are covered.

**Reconstruction.** `FINAL-DELTA-RECONSTRUCTION.md` proves landed = R3-reviewed +
named precision fixes + Option X, with the current-bullet preimage pinned, zero
unaccounted drift.
