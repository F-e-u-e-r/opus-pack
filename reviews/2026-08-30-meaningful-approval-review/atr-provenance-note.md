# ATR-2026-00118 provenance note

**Source:** ATR-2026-00118 (approval-fatigue), an external agent-threat rule.

**How it was used:**
- **Threat-shape taxonomy** — its enumeration (repeated / blanket approval,
  auto-approve / bypass, minimizing language paired with approval cues, bulk
  execution, discouraging individual review) informed the shape of the inert A1–A14
  controls.
- **False-positive lesson** — its v2 revision, which removed mass false positives on a
  bare `routine` / `normal` / `standard`, informed the bare-minimizer carve-out (A3)
  and the "urgency/batching/routine is not itself a finding" clause.

**What was NOT done (explicitly not claimed as first-hand):**
- The ATR detector was **not run** by us.
- Its regex / pattern-detection **efficacy or hit-rates were not first-hand
  validated**.
- ATR is **not** treated as a canonical oracle; it is external threat evidence and
  fixture-shaping only.

**Consistent with the pack's architecture:** ATR self-describes as experimental
pattern detection, and the ④ decision is a review-time semantic judgment
(SUPPORTING-ONLY), not a mechanical phrase scan. No `.github/checks.py` change, no CI
gate, and no runtime scanner was added.
