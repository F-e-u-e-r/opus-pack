# Round-5 campaign — RECEIPTS (durable evidence)

Results-only publication of the Round-5 probe campaign executed 2026-08-04. This
directory saves execution EVIDENCE only. It changes no marker, skill, runtime,
`reviews/2026-08-04-round5-targets.json`, or adjudication; nothing here re-scores
or re-selects a result.

## Baseline + frozen inputs (identity)

- **Execution baseline:** `main @ 6619d9c97f4058929e53776a892fb1d21a9727c0` (the merged Round-5 scope PR #139).
- **Frozen target manifest:** `reviews/2026-08-04-round5-targets.json`
  - SHA-256 `7fd6e64f0913e58bc5a12536357f12b09b21e947338e8ff9d087c9855574a4cf`
- **Pre-registration:** `PREREG.md` (copied here), SHA-256
  `5861a42ac6ca5432c39478b1f77ceeff179856d20be28130b44cbd79ae57a162` (see `PREREG.sha256`).
- **Full per-artifact byte-parity record:** `MANIFEST.sha256` (SHA-256 of every file in this directory).

## Harness receipts

- **Executor (weak tier, pinned):** `claude-haiku-4-5` (haiku), invoked as an
  isolated fresh-context subagent per sample, **0 tools**, self-contained fixture
  prompt (no repository or filesystem access), default reasoning effort.
- **Arms:** `bare` = the frozen fixture task alone; `ruled` = the same task with the
  target's rule text injected verbatim as an operating instruction. Only the rule
  injection differs.
- **Adjudicator:** opus (the session model), scoring each raw output against the
  frozen oracle in `PREREG.md` (`smoke-ledger.md` records each adjudication).

## Valid / invalid run accounting

- **Total arms: 38** — smoke n=1 (20 arms, all 10 targets × bare/ruled) + scored n=3
  (18 arms, the 3 discriminators T4/T8/T10 × bare×3 + ruled×3).
- **Invalid runs: 0** (no transport/provider error, no empty/garbled output, no
  UNARMED fixture, no CONTAMINATED context). Retry budget untouched.
- **Fixtures repaired: 0.** Bounded-stop: not triggered (ran to completion).

## Raw output provenance (arm → source subagent)

Each `raw/<label>.txt` is the **last assistant message** (the final answer / return
value) extracted from that arm's subagent transcript
(`agent-<id>.jsonl`). No content was edited; only the final message was extracted.

| arm (raw/*.txt) | source agent id |
|---|---|
| T01-threat-model.smoke.bare | aba7077d26d4d9461 |
| T01-threat-model.smoke.ruled | a459679ba823d12d4 |
| T02-severity-confidence.smoke.bare | a6a9cbf8704dd2b45 |
| T02-severity-confidence.smoke.ruled | ae6214a2229cd22c6 |
| T03-audience-check.smoke.bare | a55c61428485264fa |
| T03-audience-check.smoke.ruled | a6560ebb41f0a08b7 |
| T04-subprocess-env.smoke.bare | afc17f3e36ee380d4 |
| T04-subprocess-env.smoke.ruled | a0477d9cdfda6a04d |
| T05-policy-shaped-data.smoke.bare | a5bd76edab11e8b3c |
| T05-policy-shaped-data.smoke.ruled | a90a94754073c8a1f |
| T06-handoff-compression.smoke.bare | a930d6094a8c18e99 |
| T06-handoff-compression.smoke.ruled | af2657a8664707e1f |
| T07-costumed-completion.smoke.bare | a373eb6439f805e75 |
| T07-costumed-completion.smoke.ruled | a35f1f54bdbf3d47e |
| T08-absence-not-resolution.smoke.bare | a202673ebc88de345 |
| T08-absence-not-resolution.smoke.ruled | a6dce6fbe1b49b470 |
| T09-convergence.smoke.bare | a0ef77e8f26b1b710 |
| T09-convergence.smoke.ruled | a65bdc0f8fdb01d27 |
| T10-consumer-position.smoke.bare | a201199d669d46624 |
| T10-consumer-position.smoke.ruled | a8d12222570d2fb5e |
| T04-subprocess-env.scored.bare.s1 | ae134c5c1058880af |
| T04-subprocess-env.scored.bare.s2 | a4d8ce7ce2d78faaa |
| T04-subprocess-env.scored.bare.s3 | a4db165a0348ddebc |
| T04-subprocess-env.scored.ruled.s1 | a4edcd9bdee65eca0 |
| T04-subprocess-env.scored.ruled.s2 | a94ea7a87c8e7bac7 |
| T04-subprocess-env.scored.ruled.s3 | a827718ae5a0c8545 |
| T08-absence-not-resolution.scored.bare.s1 | a83839ae9f071eb96 |
| T08-absence-not-resolution.scored.bare.s2 | a2e78faa5c27c395a |
| T08-absence-not-resolution.scored.bare.s3 | acb6e6e1323363252 |
| T08-absence-not-resolution.scored.ruled.s1 | aea85014013b1763c |
| T08-absence-not-resolution.scored.ruled.s2 | a5b30439ac8559dc8 |
| T08-absence-not-resolution.scored.ruled.s3 | add54d455680a7b68 |
| T10-consumer-position.scored.bare.s1 | a50d485ebc9994ba1 |
| T10-consumer-position.scored.bare.s2 | a6b2733327073ddd8 |
| T10-consumer-position.scored.bare.s3 | abacc48dfe1c1bb0c |
| T10-consumer-position.scored.ruled.s1 | ab82fd4d87f5df6aa |
| T10-consumer-position.scored.ruled.s2 | a4963de57f1f25160 |
| T10-consumer-position.scored.ruled.s3 | a66a4306add7e6945 |
