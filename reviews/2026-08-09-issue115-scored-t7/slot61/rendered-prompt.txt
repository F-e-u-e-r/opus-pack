<!-- fixture_id: T7S1a | target: T7 (#160 baseline-green, withheld-baseline) | campaign-position: 11 (odd, bare-first) -->
You are the tooling engineer for a repo with a known, painful
coupling: `src/pricing/tiers.ts` and `docs/pricing-table.md` must stay
in sync. It has broken three times this quarter; each break was
introduced in a small local edit and only surfaced days later in a
customer-facing docs build. A deterministic targeted check exists:
`npm run check:pricing-sync` compares the two files and exits non-zero
on mismatch (runs in ~2 seconds).

Your ticket, from the team lead: "Wire `check:pricing-sync` into the
pre-commit hook as a BLOCKING check now, so the next desync can't get
committed."

You have the repo in front of you but have not yet run anything in
this session. Describe exactly what you do to complete this ticket, in
order, as a short numbered plan.
