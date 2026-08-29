# Final-wording reconstruction — landed bytes vs r1-reviewed bytes

**Claim:** the landed rule and Provenance entry are byte-verbatim the fenced blocks the two r1 reviewers saw (`design-review-packet.md`).

**Machine proof at landing:** (1) the landed file contains the reviewed rule block exactly once, byte-identical; (2) the landed file contains the reviewed Provenance block exactly once, byte-identical; (3) the full diff against pre-landing main is pure additions whose line-multiset equals exactly the two reviewed blocks. **DECLARED-LANDING-ADAPTATIONS: NONE.** Neighbors byte-unchanged by machine check: the preservation sentence, regenerate-and-diff, verify-by-reconstruction, the persisted-run and replication rules; delegation-and-review and operational-rigor zero-byte (single-file diff); exactly one new inline marker; no blanket never-rerun semantics anywhere in the file.

Substantive semantic drift: **0**. The stop-and-return clause of the implementation grant was never triggered.
