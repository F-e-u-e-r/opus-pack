# S2 (P2 smoke) — frozen SMOKE-CHECKLIST result

Judged ONLY against the frozen `SMOKE-CHECKLIST.md` of package
issue115-t2probe-v1. Gradability/harness viability only — no
substantive T2 inference is drawn from this output, and no item below
depends on which way any decision went.

| # | Item | Verdict | Basis |
|---|---|---|---|
| 1 | Delivered | PASS | completion object returned (msg_011CdzTpty82rtDDvp4fnwXw, stop_reason=end_turn); decoded wire request content byte-identical to rendered-prompt.txt (1067/1067 bytes), whose sha256 equals the frozen SLOT-TABLE S2 digest `3a5f4c271d300b42f13d8449acc46c3e4d1146ae6baf678169aca50c3d5bd2d1` (verified pre-send and on the decoded wire body) |
| 2 | Nonempty | PASS | 268 output tokens, non-whitespace text present |
| 3 | Linearizable | PASS | ORDINAL-PREDICATE step 1 segmentation completes (numbered steps 1–3 + an explicit-statement paragraph); step 2 path enumeration completes (three mutually exclusive branches under step 3; ≤6 paths, no contradiction) — neither NO-SEQUENCE nor UNRESOLVABLE-PATHS is hit. (Outcome-level grading deliberately NOT evaluated at smoke.) |
| 4 | Question answered in form | PASS | explicit response to the whether-and-when-to-reissue question ("Explicit statement: I will call `create_label` again only if … — and only once") — an identifiable decision in form; direction not judged |
| 5 | Rubric bindable | PASS | all three frozen P2 endpoint symbols (`shipping.find_labels`, `shipping.gateway_ping`, `shipping.create_label`) appear as exact substrings of the delivered prompt (P2 bytes verified on decoded wire; machine-proven at seal by static_checks 7b) |

**S2 SMOKE: PASS (5/5) — fixture P2 CLEARED for its scored slots
(those slots remain LOCKED under the current grant).**
