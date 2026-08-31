NOT CONFIRMED as written; one over-claim needs narrowing.

1. **High — OVER-CLAIM**

   **LOCATION:** “that digest confirmation is what makes an incomplete removal detectable”

   **MECHANISM:** [verified: derived from the supplied evidence] The digest check detects this failure only when the stale runtime-selected bytes differ from the regenerated artifact. It does not detect every incomplete removal—for example, if the leftover artifact is byte-identical, or if the comparison itself is not performed against the actually selected bytes.

   **CONCRETE FIX:** Replace with: “for this stale-byte failure mode, that digest confirmation is what exposes a failed removal, so it is load-bearing rather than redundant.”

2. **Medium — GENERALIZATION**

   **LOCATION:** “a central or path-mirrored cache directory, a per-user cache root”

   **MECHANISM:** [verified: compared with E1] E1 establishes one path-mirrored, per-user out-of-tree cache. It does not establish “central” caches generally. The modal “may” makes the broader possibility defensible, but the examples exceed the evidence slightly.

   **CONCRETE FIX:** Use: “an out-of-tree cache, including a path-mirrored or per-user cache root”.

3. **Low — REDUNDANCY / WORD BUDGET**

   **LOCATION:** “the digest confirmation is what makes … detectable, so it is load-bearing rather than a second opinion on the removal”

   **MECHANISM:** [verified: compared with the landed text and E2] The existing digest requirement already operationally catches the demonstrated stale-byte case. The insertion adds rationale and warns against trusting a clean tree, but it adds no new clearance condition.

   **CONCRETE FIX:** Retain only the concise operational warning: “locate it rather than assume its conventional in-tree path, because a runtime may use an out-of-tree cache; the subsequent digest check must still confirm the selected bytes.”

4. **No scope violation found**

   **LOCATION:** Entire insertion.

   **MECHANISM:** [verified: direct text inspection] No machine path, operating system, vendor, interpreter name, or tool-specific lineup remains. “In-tree,” “out-of-tree,” “path-mirrored,” and “per-user cache root” are portable concepts.

   **CONCRETE FIX:** None.

5. **No internal-consistency break found**

   **LOCATION:** The `(a)` limb through “`; (b) bind the exact artifact bytes…”

   **MECHANISM:** [verified: direct text inspection] The `(a)/(b)/(c)` structure remains grammatical and ordered. The patch makes locating competing artifacts explicit but does not contradict regeneration or digest matching.

   **CONCRETE FIX:** None.

FIX OVER-CLAIM, GENERALIZATION, REDUNDANCY