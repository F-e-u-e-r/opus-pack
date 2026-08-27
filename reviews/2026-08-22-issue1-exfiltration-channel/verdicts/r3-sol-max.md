1. **Yes.** The current sole carrier is explicitly “Exfiltration-shaped commands” and enumerates `curl`/`wget`/`nc` plus particular credential reads. Neither a rendered resource reference nor `socket.getaddrinfo` matches it. Security-architect’s “path that sends data out” is architectural guidance, not the vetting checklist.

2. **Yes, for the two target shapes.** The proposed text expressly covers renderer/client fetches and hostname/DNS-label transport, while the no-secret carve-out correctly clears `benign-remote-image-legit.md` and `benign-dns-legit.md`. However, its governing predicate is internally imprecise: “a channel the purpose doesn’t need” could clear `fail-piggyback-needed-endpoint.md`, whose API channel is needed but whose secret disclosure is not.

3. **It correctly generalizes the existing carrier.** Clause (a) retains the current command/read findings; clause (b) adds channel semantics. This does not duplicate security-architect’s prevention-oriented capability triangle or secure-ingestion guidance.

4. **Yes.** “Any outbound path,” followed by address, payload, metadata, DNS, and presence/count/order examples, is broad without claiming exhaustiveness. The timing/cache limitation is explicitly disclosed.

5. **Yes for remote-image and DNS expansion, but the controls expose no benign CLI case.** The fixed image and hostname remain clear, while the auth and conditional-request fixtures test two important boundaries. A legitimate no-secret API/update request made through `curl` or `wget` is nevertheless ambiguous under the proposed wording.

6. **Yes.** Replacing the sole exfiltration bullet is the minimal surface. Operational-rigor §2 contains no exfiltration rule to mirror.

7. **Yes—none is introduced.** The amendment is static doctrine with inert fixtures and requires no runtime detector, probe, or tooling.

8. **Yes.** The incident family is described as attested rather than reproduced, and `unprobed` is stated explicitly.

The expressly missed channel is pure secret-dependent timing/cache signaling. The concrete benign misfire is a disclosed, purpose-required, no-secret `curl`/`wget` API call: clause (a) makes it an independent hit “payload or not,” while the later safe harbor says a no-secret API call “is not,” yielding conflicting classifications.

FIX 1. Replace “a channel/path the disclosed purpose does not need” with “private-data disclosure the disclosed purpose does not need, over any outbound path,” preserving the piggyback fixture’s BLOCK result. 2. Reconcile clause (a)’s unconditional CLI hit with the no-secret API safe harbor, and add a benign CLI fixture establishing the intended classification.
