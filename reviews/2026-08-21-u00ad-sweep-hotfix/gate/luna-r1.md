Q1 — Yes. Baseline evidence shows all three sets were identical at 145, U+00AD was absent everywhere, and the live regex probe failed to match it.

Q2 — Yes. Both prose surfaces add “soft hyphen (U+00AD),” and the executable adds `\u00ad`; post-patch equality checks pass.

Q3 — Yes. Each post-patch set is 146, with the exact delta reported as `[U+00AD]`.

Q4 — No loss. Evidence says nothing was removed and all original 145 code points remain caught.

Q5 — No widening. U+0085 and U+180E remain excluded, and the exact set delta contains only U+00AD.

Q6 — Yes. The patched gate catches the literal U+00AD mutant fixture; baseline exits 0, while patched execution reports `FAIL` and exits 1.

Q7 — Yes. All listed legitimate controls remain uncaught in the patched probes, including whitespace, NBSP, accented Latin, CJK, punctuation, and symbols.

Q8 — No creep. The diff changes only the three required carriers and the truthful enumeration comment. No refactor, severity change, excluded-range addition, or architecture change is present.

Findings: None.

PROCEED
