1. Confirmed. O3/R3 now use bounded measured-surface language; no stale `token-level` wording remains in §8 or R-P2.

2. Confirmed for Blocker B. Literal `one` remains in the rule and `its` remains in the owner lead, but neither forms a shared owner-exclusive feature. The raw-token sweep catches these independently of stopword filtering.

3. Confirmed. `owner_exclusive()` compares raw tokens and every word-internal character n-gram from n=3 through 8, and subtracts every feature present in another bullet. It mechanically enforces emptiness.

4. Confirmed. The content-token axis is explicitly stopword-filtered and plural-stemmed; raw tokens are a separate axis.

5. Substantively confirmed: all four leakage episodes remain documented. Record-only inconsistency: a `static_checks.py` comment says “Three successive drafts” while listing four episodes.

6. Confirmed within the supplied packet. P1 and its anchor remain protected by byte-equality and rendered-prompt-hash checks.

7. The relevant invariant checks support the claims. Record-only caveat: the script does not itself count or assert “164,” and does not mechanically validate the historical prose or §8 terminology.

8. Confirmed within the preregistered bounds. P2 remains a documented-owner capability control; failed control results stop attribution, while passing control results permit the preregistered P1 branches. Synonym, conceptual, positional, and E-bundle limitations are already disclosed.

9. No new correctness, leakage, identifiability, or overclaim blocker. The residual `token-level` phrase in a code comment and the historical-count typo are record-only.

PROCEED
