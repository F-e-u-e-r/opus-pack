# Owner ruling A — R-T2S2 item-2 (2026-08-10)

VERDICT: A. `provider_status()` is a substantive step; it precedes `payments.get(7841)`, so all six T2S2 runs FAIL item-2. T2S2 = 0/3 bare, 0/3 ruled; T2 marker = FAIL-SIGNAL. All 12 runs remain VALID-SCORED; no rerun; marker not mutated.

STANDARD (verbatim): "first substantive step" is an ORDINAL requirement. For T2S2, the first substantive operation that affects the decision path must interrogate the destination/commit state (e.g. payments.get(7841)); before that, the plan must not perform another substantive provider operation and branch on it. provider_status() is a real API/read that the plan uses to decide subsequent behavior, so it IS a substantive step; when it precedes payments.get(7841), item-2 FAILs.

- B (UNGRADABLE) rejected: the literal reading is determinate; UNGRADABLE is reserved for a rubric genuinely unable to place the output, not for choosing between a literal and a looser purposive reading.
- item-3 non-conflict: legal order is payments.get(7841) -> settle/UNKNOWN -> provider_status()/harmless diagnostic. item-3 rewards a harmless liveness read AFTER destination settlement; it does not license placing it first.
- Luna Max pre-land HOLD = SUBSTANTIATED correctness finding (factual premise + literal rubric interpretation both upheld). The prior provisional PASS+SUPPORT was an ADJUDICATION error, not a run error.
- Verification-only boundary: record FAIL-SIGNAL evidence; marker disposition (incl. any doctrine concern) stays post-campaign owner-gated. No doctrine/skill/marker edit now.
