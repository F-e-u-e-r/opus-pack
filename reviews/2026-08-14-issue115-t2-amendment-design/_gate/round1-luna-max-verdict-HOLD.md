1. No. M1’s “first provider-side read” is stronger than the ruling, which orders destination interrogation before liveness/status reads specifically. “Provider-wide” also narrows the stated boundary.

2. No. M2 omits the explicit no-substitution guard, but M1 is not globally minimal; a single conditional sentence can preserve the required coverage.

3. M1 adds no retry entitlement or mandatory liveness read. M3 imports E-arm emphasis (“this ordering is strict”); M1’s broader “first provider-side read” also risks importing first-operation semantics.

4. No, not fully. The keyed read is named, but sentence two drops “provider-wide”; a destination endpoint returning status could be classified inconsistently.

5. No, not unambiguously. M1’s first sentence is unconditional, and its second conditions only on query existence—not on a usable request identity—so no-query/no-identity cases can be read as requiring an impossible interrogation.

6. Yes, byte-wise and substantively for invariants 6–9. The insertion point and checks preserve those downstream rules.

7. Yes:

   `Where the destination can be queried under the request identity, its read-back precedes any provider-side liveness/status read; provider-side liveness/status never substitutes for destination-state evidence.`

8. Yes. The provenance correctly limits #191 to directional evidence of a transmission gap and does not claim the new wording is proven correct.

9. Yes. The design leaves the T2 marker untouched and unprobed; the mutation gate should byte-check it.

10. Yes for scope and mechanical checks, though semantic tests for no-query/no-identity behavior should be added before mutation.

VERDICT: HOLD — 1, 2, 4, 5
