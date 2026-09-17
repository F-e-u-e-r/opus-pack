# Activation research — evaluation-state reconciliation (2026-09-18)

Purpose: fix the true research frontier from **preserved experiment evidence**
before publishing README / roadmap claims. Every figure below was read from the
on-disk scored return packets under `evals/round5-deployed/` (raw run artifacts
are gitignored / local-only; this note is the tracked summary). Where a summary
index disagreed with a detailed packet, **the packet wins**.

Model throughout: `claude-haiku-4-5-20251001` (weak tier). Every per-condition
sample is n=3 — **directional evidence, not population effect sizes**.

Each experiment records its **final owner disposition** below; the packet-level
"STOP for adjudication" is retained as provenance, distinct from the subsequent
owner adjudication.

## Baseline this all sits on

The round5-deployed **R2 primary baseline is complete and owner-accepted as
canonical** (2026-09-16): behavioral **96/96** valid, routing **171/171** valid
(267 total). It is not an open loop. Diagnosis: routing is strong (binary
**135/144 = 0.938**) while autonomous behavioral invocation was **0/48** — the
bottleneck is the **activation bridge**, not descriptions/content. Every
experiment below was run on top of this accepted baseline.

## Activation Bridge v1 — generic activation cue

- **Scored:** yes — `activation/ACTIVATION-RESULTS.md`, campaign dir
  `runs/activation-primary-20260917-015658/`.
- **Identity:** MANIFEST `68834b3d…`, cue `ff51c338…`, schedule `f279835b…`
  (seed 1961458304). Self-SHAs re-verified.
- **Counts:** 96 completed / **95 valid** / 1 incomplete (CUE-DEPLOYED, "UNARMED");
  0 invalid.
- **Activation (primary):** CUE-DEPLOYED appropriate activation **6/41 (0.146)**;
  CUE-BARE 0/42 (no pack by construction); 85% of required-skill runs did not
  activate. Per-family: T4 4/5, T5 1/6, T6 1/6; T1/T2/T3/T7 0/6.
- **Behavioral (contemporaneous, CUE-DEP vs CUE-BARE):** 28/47 vs 31/48 (Δ −3,
  n=3 noise).
- **Reading:** Pattern D — activation rose but stays low; no behavioral increment
  where it fires. Does **not** justify rewriting skill content.
- **Packet boundary (provenance):** data-only return packet stopped for owner
  adjudication; no pack mutation.
- **Final owner disposition:** WEAK-BUT-SELECTIVE BRIDGE — do not ship as a
  production treatment. S1 remains INCONCLUSIVE / minimally probed.

## Activation Bridge v2 — mandatory routing checkpoint

- **Scored:** yes — `activation-v2/ACTIVATION-V2-SCORED-RESULTS.md`, campaign dir
  `runs/activation-v2-primary-20260917-031438/`.
- **Identity — ambiguity resolved.** The scored identity is MANIFEST
  **`8724a640…`** (= `ACTIVATION-V2-MANIFEST.sha256`), cue `6632676c…`, schedule
  `9a5f210a…`. An earlier **pre-scored** manifest **`0656897634…`**
  (= `…MANIFEST.sha256.pre-repair-r1`, referenced only by the superseded
  `ACTIVATION-V2-RESULTS.md`) is **not** the scored identity. Cite `8724a640…`.
  Both self-SHAs re-verified by hash.
- **Counts:** 96 completed / **95 valid** / **1 invalid**
  (`T1a-checkpoint-deployed-T1ad2`, NO-RESULT-EVENT; preserved, not deleted).
- **Activation (primary):** CHECKPOINT-DEPLOYED appropriate activation
  **6/41 (0.146)**; 1/41 wrong-skill (T2a → operational-rigor); 34/41 no observable
  pack invocation. Per-family: T4 4/6, T5 1/6, T6 1/6; T1/T2/T3/T7 0.
- **Behavioral (contemporaneous, DEP vs BARE):** 33/47 vs 32/48 (Δ +1, n=3 noise).
- **T8 negative control:** 0/6 both arms — no over-fire (pack or ambient).
- **v1 vs v2:** appropriate activation is **6/41 in both**. v2 shows **no observed
  activation improvement over v1** — but this is **not a clean contemporaneous
  causal contrast** (v1 and v2 are separate cross-campaign experiments; the only
  within-experiment causal contrast is DEPLOYED vs BARE). Do not read it as a clean
  causal null.
- **Packet boundary (provenance):** data-only return packet stopped for owner
  adjudication; no pack mutation.
- **Final owner disposition:** CANONICAL — NO OBSERVED ACTIVATION IMPROVEMENT over
  v1 (see the non-contemporaneous caveat above; not a causal null).

## Activation Localization Probe v1 — explicit-routing, per-surface

- **Scored:** yes — `localization-v1/LOCALIZATION-V1-SCORED-RESULTS.md`, campaign
  dir `runs/localization-v1-primary-20260917-154557/`.
- **Identity:** MANIFEST `7dff43e3…`, instruction `7bf2610c…`, schedule
  `e0e16d7d…`. Self-SHA re-verified.
- **Counts:** 48 completed / **45 valid** / **3 invalid** (T1b ×3, 180s wall
  timeout — the git-investigation surface provokes task execution despite the
  routing-only instruction; preserved).
- **Primary:** fixture_matched_routing_accuracy **17/45 (0.378)**; required-skill
  recall **11/39 (0.282)**; T8 correct-NONE 6/6; wrong-skill 10/45 (0.222).
- **By family:** T1 0/3, T2 0/6, T3 0/6, **T4 6/6**, T5 2/6, T6 2/6, T7 1/6,
  **T8 6/6**.
- **Ambient interference:** 6 runs invoked ambient `code-review` (counted
  wrong-skill): T1a×2, T3a×2, T3b, T6a.
- **Protocol:** stop-after-routing **9/21 (0.429)** — the routing-only instruction
  does not reliably stop the model (instrument weakness, separate from routing
  disposition).
- **Reading:** **L3 / MIXED** — skill-and-surface-specific. Strong: T4/gtg 6/6,
  T8/NONE 6/6. Weak even under explicit routing: T2/gtg 0/6 (same skill as T4,
  different surface), T3/cmr 0/6, T7/delegation 1/6, T1a/op-rigor 0/3. The gtg
  6/6-on-T4 vs 0/6-on-T2 split argues **against** a single pack-wide cause; no
  pack-wide treatment follows.
- **Packet boundary (provenance):** data-only return packet stopped for owner
  adjudication; no pack mutation.
- **Final owner disposition:** L3 / MIXED — ACCEPTED / CANONICAL. Skill-and-surface-
  specific; no pack-wide treatment follows.

## Two experiments that bound the T2 seam

Context for the README results section and the closed roadmap item.

- **Surface-Cue v1** (task-side; scored, `surface-cue-v1/…`): adding
  trust/verification task wording moved weak-T2 `ground-truth-gates` routing
  **0/6 → 4/6** (T2a 0/3 → 3/3 full; T2b 0/3 → 1/3 partial); T4 6/6 → 6/6
  (cue-reduced did not degrade). Verdict **G2 + G5**, canonical.
- **Description-Boundary v1** (description-side; scored, `desc-boundary-v1/…`):
  holding the natural task bytes fixed and narrowly expanding the gtg description
  left target routing **0/6 → 0/6** (T2a/T2b both 0/3 → 0/3) while T4 was retained
  **5/6 → 6/6**. Verdict **D2**, owner-adjudicated 2026-09-18: candidate
  description (`389884bc` / SKILL `ec660a81`) **rejected for shipment**; canonical
  gtg SKILL.md `29f2d5f9` **unchanged**; branch **complete**.
- **Net dissociation:** the T2 routing boundary is repairable from the **task**
  surface, not from this **description** expansion. Surface-Cue is not weakened by
  the null.

## Discrepancies found (resolved in favor of preserved evidence)

1. **v2 identity.** An earlier index cited `0656897634…` for v2; that is the
   pre-scored (pre-repair-r1) manifest. The scored identity is `8724a640…`.
   Resolved by re-hashing both manifest files.
2. **round5 baseline.** An earlier index described the 267 primary measurements as
   "stopped awaiting re-auth"; the detailed packets show them executed under R2 and
   owner-accepted as canonical. Resolved in favor of the packets.

No expected fact checked in this reconciliation conflicted with the preserved
packets.
