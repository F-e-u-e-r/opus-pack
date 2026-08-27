1. **Yes.** The current rule is explicitly “Exfiltration-shaped commands” and enumerates `curl`/`wget`/`nc` plus sensitive-store reads. Neither the passive Markdown-image fetch nor DNS resolution in the two FAIL fixtures is covered by a general vetting rule.

2. **No, not consistently as written.** The new wording catches both target fixtures and the piggybacked-secret case. However, clause (a) independently flags every HTTP/socket-library call to a real external host, conflicting with the later “API call … carrying NO secret is not” and ordinary-auth carve-outs.

3. **It correctly generalizes the sole carrier.** The CLI and standalone credential-read fixtures preserve existing findings. Security-architect discusses system design (“break the triangle”), while skill-vetting examines untrusted source; these are distinct lenses.

4. **Yes, the examples are broad but expressly non-exhaustive.** URL components, headers/`Referer`, DNS labels, and presence/count/order are covered, while timing/cache channels are explicitly identified as outside static review.

5. **No.** The static-CDN image control clears cleanly, but real-host equivalents of the benign weather `requests.get` and authenticated `requests.post` satisfy clause (a) despite being declared “not a hit.” Their inert placeholder hosts mask this conflict rather than resolving it.

6. **Yes.** Replacing the sole skill-vetting bullet is the minimal structural surface. Operational-rigor contains no exfiltration rule, so a mirror or additional bullet is unwarranted.

7. **No unnecessary mechanism is proposed.** This remains a wording-only design gate with inert fixtures and no runtime detector or behavioral probe.

8. **Yes.** ATR-2026-00261 is described only as owner-attested, explicitly “NOT first-hand reproduced,” with `unprobed` status and behavioral effectiveness deferred.

The remaining ambiguous channel is a fixed-URL renderer beacon whose conditional presence itself leaks private state: the presence/count/order clause catches it, but the later address/payload/metadata-only safe harbor can clear it. The concrete benign misfire is any purpose-required HTTP/socket-library call to a genuine documented host. Pure timing/cache exfiltration is also missed, but that boundary is candidly declared.

FIX 1. Reconcile the unconditional HTTP/socket-library-call finding with the benign API/auth safe harbors, preferably by limiting library-call hits to unexplained or purpose-unneeded beacons while preserving the legacy CLI/read findings. 2. Rewrite the no-secret safe harbor to consider invocation presence/count/order, so a fixed-address beacon is not cleared merely because its address, payload, and metadata are constant.
