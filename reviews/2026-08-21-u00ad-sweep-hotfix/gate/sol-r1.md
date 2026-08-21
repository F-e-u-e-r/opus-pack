### Per-question answers

- **Q1 — Yes.** Baseline enumeration shows all three surfaces held the identical 145-code-point set, excluded U+00AD, and the live regex did not match it. No broader drift was found.
- **Q2 — Yes.** Both prose contracts add “soft hyphen (U+00AD),” and the regex adds only `\u00ad`.
- **Q3 — Yes.** Post-patch enumeration reports 146 code points and proves the exact delta is `['U+00AD']`.
- **Q4 — No loss.** The evidence confirms nothing was removed and all original 145 code points remain individually caught.
- **Q5 — No silent widening.** U+0085 and U+180E remain excluded, and exact-set comparison shows no addition besides U+00AD.
- **Q6 — Yes.** The patched gate rejects a tracked mutant containing a literal character constructed with `chr(0xAD)`, while the baseline gate accepts the same mutant.
- **Q7 — Yes.** Exact-set verification plus probes for ASCII, standard whitespace, NBSP, accented Latin, CJK, punctuation, arrows, and symbols show no detector-wide false-positive regression.
- **Q8 — No scope creep.** The diff changes only the three specified carriers and keeps the scanner comment truthful. Other behavior and architecture remain untouched.

### Findings

No correctness defects, carrier drift, false-positive regressions, or scope creep are evidenced by the packet. The clean patched gate also passes all 1,443 tracked text files.

PROCEED
