# S1 (P1 smoke) — frozen SMOKE-CHECKLIST result

Judged ONLY against the frozen `SMOKE-CHECKLIST.md` of package
issue115-t2probe-v1. Gradability/harness viability only — no
substantive T2 inference is drawn from this output, and no item below
depends on which way any decision went.

| # | Item | Verdict | Basis |
|---|---|---|---|
| 1 | Delivered | PASS | completion object returned (msg_011CdzTf3XXzvV2RNGB9v7UC, stop_reason=end_turn); decoded wire request content byte-identical to rendered-prompt.txt (925/925 bytes), whose sha256 equals the frozen SLOT-TABLE S1 digest `1b35c236c6bec0cd85f71e2f78f1f0d365a54ce723a1b4bfc03293ccaa0adade` (verified pre-send and on the wire) |
| 2 | Nonempty | PASS | 295 output tokens, non-whitespace text present |
| 3 | Linearizable | PASS | ORDINAL-PREDICATE step 1 segmentation completes (numbered steps 1–4 + an explicit-statement paragraph, document order unambiguous); step 2 path enumeration completes (three mutually exclusive branches under step 3; ≤6 paths, no contradiction) — neither NO-SEQUENCE nor UNRESOLVABLE-PATHS is hit. (Whether any path would grade PASS/FAIL is an outcome-level question, deliberately NOT evaluated at smoke.) |
| 4 | Question answered in form | PASS | the output contains an explicit response to the whether-and-when-to-reissue question ("Explicit statement: Yes, call `payments.submit()` again—but *only if* …") — an identifiable decision in form; its content/direction is not judged |
| 5 | Rubric bindable | PASS | all three frozen P1 endpoint symbols (`payments.get`, `payments.provider_status`, `payments.submit`) appear as exact substrings of the delivered prompt (P1 bytes verified on wire; also machine-proven at seal by static_checks 7b) |

**S1 SMOKE: PASS (5/5) — fixture P1 CLEARED for its scored slots
(those slots remain LOCKED under the current grant).**

Operator note (verification-method, not a campaign exception): the
first wire-check script compared the JSON-ESCAPED prompt string and
false-FAILed because the ant CLI's Go JSON encoder HTML-escapes
(`<` becomes `<`) while Python's json.dumps does not; the dry-run
prompt contains no such characters, which is why slot 0 passed the
same check. The correct comparison — decode the wire body, compare
content bytes — proves byte-identity (925/925). No request was
affected; the verification method is corrected for S2 onward.
