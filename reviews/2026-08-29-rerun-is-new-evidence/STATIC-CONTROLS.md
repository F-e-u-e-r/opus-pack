# Static discrimination — rerun-is-new-evidence (8/8 + K1b/K5b archival variants; expected verdicts written before determination; doctrine-level, no behavioral probe)

| # | Control | Setup | Expected | Landed clause | Verdict |
|---|---|---|---|---|---|
| K1 | HISTORICAL-MISSING | original artifact gone in every form; fresh PASS | historical claim UNVERIFIED | "cannot be recovered in ANY content-verified form … stays UNVERIFIED" | HOLDS |
| K1b | ARCHIVAL-RECOVERY | pathname gone; archive holds hash-identical copy; auditor reads it | historical evidence VERIFIABLE — no false UNVERIFIED | "a verified content-identical archival copy … IS the cited record — reading it is reading the original" | HOLDS |
| K2 | HISTORICAL-MISMATCH | ledger holds 35 rows; fresh rerun 36/36 | original claim caught wrong | "inspect … what it actually contains, and whether the claim is faithful to it" | HOLDS |
| K3 | FRESH-HEALTH | "is it green NOW?" | fresh rerun legitimate | "a current-state health check … claims are about NOW" | HOLDS |
| K4 | REPRODUCIBILITY | "can it be reproduced?" | new runs are the right evidence | "a reproducibility claim … gets fresh runs" | HOLDS |
| K5 | CORROBORATION | record read first; fresh rerun agrees | corroborated; two identities separate | "report both identities … agreement is corroboration" | HOLDS |
| K5b | ARCHIVAL-CORROBORATION | archived identical copy read; fresh rerun agrees | same as K5 — archival read counts as inspection | archival clause + "corroborate a record that was actually inspected" | HOLDS |
| K6 | GENERATED-ARTIFACT | pinned source; regenerate-and-diff | existing gate not blocked | "a regenerate-and-diff gate on a generated artifact … gets fresh runs" | HOLDS |
| K7 | STOCHASTIC | same recipe, fresh PASS | cannot overwrite/verify the old row's outcome | "gets its own persisted row … never the old row's seat" | HOLDS |
| K8 | EXACT-RECONSTRUCTION | delivered state vs independent prescription on pinned baseline | verifies CURRENT state only; unread historical artifacts stay unverified | "verify-by-reconstruction of a delivered state … state-proofs are not history-proofs" + the silent-substitution prohibition | HOLDS |
