1. No. The 4-gram assertions are correctly directed and close the exact `{live}` defect. They do not close its class. Using the same word-internal extractor at `n=3` gives the owner-exclusive set `{its, one}`:

   - `its`: rule “once its rollout” / “beside its figure”; owner “outlives its purpose”; absent from every other bullet.
   - `one`: rule “done — one”; owner “none is exempt”; absent from every other bullet.

   Moreover, raw word-token overlap has owner-exclusive `its`; the script hides it because `its` is a stopword, while the 4-gram check cannot see three-character words. Thus a standard token- or character-trigram-sensitive matcher retains a differential route to 2.1.

2. No. Most of R-P2 and prereg §§2, 4, and 12 correctly say “measured surface routes.” However, locked §8 still says:

   - R5: “the owner offers no token-level route”
   - R3: “not token-level surface attachment”

   Both exceed and differ from the four-axis claim—and the first is concretely false under raw tokenization because of `its`. “Shared token types” must also be qualified as stopword-filtered, stemmed content-token types if that remains the implemented measure.

3. These are blocking identifiability/correctness issues, but no additional fixtures, arms, or runs are needed. They can be repaired within P2, the invariant implementation, and the two §8 branch statements. I found no separate new leakage defect.

HOLD: 1. The character-ngram class remains open through owner-exclusive trigrams `{its, one}` and the raw-token route `its`. 2. The locked §8 mapping retains overbroad token-level claims inconsistent with the implemented four-axis boundary.
