# Round-1 findings adjudication (owner ruling, recorded)

Round 1 (dual-blind, two same-provider variants at max effort — NOT
cross-family): luna PROCEED (15/15 axes) / sol FIX with two findings.
Both findings were reproduced first-hand by the operator via re-derivation
from the v1 draft text, then validated by the owner:

- **F1 VALID (axes 1/2/4; D12/D14).** v1's §2 carve-out sentence made the
  AUTHORIZATION boundary outcome-retrospective ("whether independent
  model/agent judgment materially contributed to the conclusion") — a
  no-grant worker could invoke a model to review/decide, discard or deny
  relying on the output, and argue no-contribution ⇒ no-delegation ⇒ no
  grant needed; it also conflicted with the same sentence's task-side
  parenthetical and §3's budget classification. Ruling: authorization
  turns PROSPECTIVE on whether the invocation DELEGATES independent
  judgment (review / decide / assess / form a conclusion = judgment
  delegation at the moment of invocation, whatever the depth or binary);
  material contribution governs only the retrospective provenance/lens/
  family accounting; a discarded or ignored result never retroactively
  clears an unauthorized delegation.
- **F2 VALID (axis 9; D14).** v1 required disclosure only for CONTRIBUTING
  sub-principals while charging every judgment principal to the budget —
  leaving non-contributing principals unreportable, so the dispatcher
  could not enforce "counts as if directly launched". Ruling: two-tier
  accounting — a COMPACT account (existence + the budget-relevant facts
  the governing limit needs) for EVERY spawned judgment principal,
  contributing or not; RICH contribution disclosure (identity/model
  family, task, contributions, delegated verification) stays
  contributor-only; deterministic helpers stay excluded.

Authorized revision: EXACTLY these two semantic corrections plus pinning
control cases D17/D18/D19; every other clause, the frame, the homes, and
D1–D16 meanings byte-preserved (machine diff v1-to-v2.diff, per-hunk
attribution in packet-r2.md). Gate: one narrow dual-blind confirmation
round — 2/2 PROCEED required; any FIX stops with no v3.

Round 2 on frozen v2: **PROCEED from both** (verdict-luna-r2.md,
verdict-sol-r2.md; sol — the original FIX author — confirmed both
findings substantively fixed and the diff free of third changes). Both
R2 nearest-failure sections independently converged on the same
control-case reading (D14 "budget axis only" vs prospective
authorization) and both judged it sound — D14 wording frozen as
reviewed, zero polish (owner ruling: re-editing reviewed bytes would
create unreviewed bytes).
