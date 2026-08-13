1. No — blocking. The ruling requires destination interrogation to precede liveness/status reads. M1 additionally makes it “the first provider-side read,” thereby forbidding unrelated provider-side reads that #188 does not address. That is stronger than the settled ruling.

2. No — blocking. A shorter, query-scoped ordinal sentence suffices. M2 conveys the central precedence, but its “first provider-side read” wording retains the same overreach. #191 does not justify importing broader parts of the tested control.

3. Yes — blocking for M1. M1 and M2 import a first-among-all-provider-reads constraint; M3 goes further with “first provider-side operation.” M3’s “strict” register is merely record-only, but its broader operation constraint is substantive. None creates a retry entitlement or requires a later liveness read. M1’s no-stand-in clause restates existing authoritative-evidence semantics rather than adding policy.

4. No — blocking. The first sentence qualifies liveness/status as “provider-wide,” but the second drops that qualifier. A request-keyed destination interrogation may itself use a status endpoint, so “liveness/status reads may follow only afterward” can appear to classify the permitted first read as forbidden. Positive naming reduces but does not eliminate that ambiguity.

5. Not unambiguously — blocking. The downstream no-query branch still mandates immediate terminal uncertainty, but M1 first issues an unqualified imperative to interrogate destination state. In a no-query case, that creates a competing apparent obligation. The amendment should be query-scoped from its first word.

6. Yes, textually. The authoritative-read threshold, both-axes test, idempotency carve-out, and terminal-uncertain cap remain unchanged. The boundary ambiguity in item 4 should nevertheless be fixed so request-status evidence is not misread.

7. Yes. A shorter formulation with the intended coverage is:

   > Where a destination query exists, read destination state under the request identity before any separate provider-side liveness/status read; such reads may follow only afterward and never stand in for destination-state evidence.

   This states the ordinal relation without making the destination read first among every possible provider-side read, scopes away the no-query conflict, and distinguishes a keyed status interrogation from a separate liveness/status read.

8. The evidentiary limits themselves are correct: #191 supports a directional transmission-gap finding and successful control-following, not validation of M1. However, with M1 unchanged, provenance would overclaim by calling the amendment purely non-semantic despite its first-provider-read expansion. “Adopts E’s semantics minimally” should also become “implements #188’s settled semantics; E served only as the experimental control.”

9. Yes. The design neither probes nor changes the T2 marker.

10. Not fully. The scratch simulation, invariant checks, and E-text similarity check provide a narrow verification structure, but the future gate must prohibit the proposed rewrap exception; otherwise the mutation is not literally insertion-only. Also reconcile the claim of “9 invariant carriers” with the displayed output, which shows the anchor plus seven invariant checks. The ≥8-word guard proves only absence of that degree of verbatim copying, not absence of semantic policy import.

VERDICT: HOLD — 1, 2, 3, 4, 5, 8, 10
