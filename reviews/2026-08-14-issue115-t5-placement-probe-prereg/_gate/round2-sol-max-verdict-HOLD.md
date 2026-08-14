1. The repair removes the original distinct-token overlap, but it does not fully resolve the defect. Under `content_tokens()`’s set metric, the reported overlaps are correct and competitors 2.2/3.1 share more token types. However, the invariant discards frequency and order:

   - The rule contains `flag` twice.
   - Owner 2.1 contains it three times; 2.2 twice; 3.1 once.
   - A stemmed term-frequency dot product scores 2.1 and 2.2 equally at 6, with 3.1 at 5.
   - The exact bigram `flag is` also occurs in the rule and uniquely in 2.1.

   Thus a token-level surface matcher can still reach the owner. The check establishes only “less distinct content-token-set overlap,” not “no token-level surface route,” so it is insufficient for the claim currently licensed from P2.

2. No new owner ambiguity or leakage blocks:

   - 2.1 remains a clear, documented, pre-declarable semantic owner. It explicitly governs the flag’s lifetime and terminal reachability condition; the new rule constrains that endpoint. 2.2 governs exposure figures and their recording.
   - The `deleted`/`retired` conceptual relationship is an intentional, arm-constant feature and is correctly acknowledged as residual conceptual proximity, not answer leakage.

   Claim scoping is nevertheless incomplete. The formal §8 branch preamble and ledger mostly use the proper “not token-level” boundary, but other passages still overclaim:

   - R-P2 says P2 “discriminates governance-based attachment.”
   - Prereg §2 calls it a positive control “for governance-based attachment.”
   - §8 calls it a check whether governance-based attachment “is available at all.”
   - §4 says any P2 failure evidences surviving surface attachment, although FAIL-STANDALONE, FAIL-OMIT, and UNGRADABLE do not establish that mechanism—and §8/R5 correctly leaves the mechanism unresolved.

3. I find no additional blocking defect on these bytes. No additional fixture, arm, or run is required; the blockers concern the lexical invariant and its associated claims.

HOLD: 1. P2 still permits token-level surface routes that the set-overlap invariant does not detect. 2. Several P2 result interpretations still overclaim governance or surface attribution.
