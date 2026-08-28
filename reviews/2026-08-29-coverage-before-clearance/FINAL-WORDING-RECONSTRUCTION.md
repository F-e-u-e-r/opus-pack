# Final-wording reconstruction — landed bytes vs r1-reviewed bytes

**Claim:** the landed §3 rule and its Provenance entry are byte-verbatim the blocks the two r1 reviewers saw (`design-review-packet.md`, its two fenced blocks).

**Machine proof at landing:** (1) the landed file contains the reviewed rule block exactly once, byte-identical; (2) the landed file contains the reviewed Provenance block exactly once, byte-identical; (3) the full diff against pre-landing main is pure additions whose line-multiset equals exactly the two reviewed blocks — zero other insertions, zero deletions. **DECLARED-LANDING-ADAPTATIONS: NONE** (the `unprobed` marker and the Provenance entry were already inside the reviewed blocks; placement required no re-wrap). Neighboring doctrine byte-unchanged: packet-errors rule, completion-claim audit, settled-tree protocol (blob-identical), the two #219 units; single canonical file touched; exactly one inline marker in the new rule.

Substantive semantic drift: **0**. No substantive criterion change was needed — the stop-and-return clause of the implementation grant was never triggered.
