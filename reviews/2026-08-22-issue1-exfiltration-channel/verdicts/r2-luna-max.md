1. Yes. The current sole rule is explicitly “Exfiltration-shaped commands” and lists only `curl/wget/nc` plus sensitive-store reads. The image fixture uses a renderer fetch; the DNS fixture uses a secret hostname with `getaddrinfo`. The sibling design text is not a §2 vetting rule.

2. The channel clause catches both target shapes and does not inherently ban ordinary images or DNS. However, the full wording conflicts internally: `(a)` flags every non-placeholder HTTP/socket-library call “payload or not,” while later text says secret-free API calls and legitimate auth are not hits.

3. Conceptually, this correctly generalizes the existing carrier and does not duplicate the security-architect design lens. But the unconditional HTTP/socket-library addition is broader than a reframe and creates the false-positive problem above.

4. The examples cover the two target shapes, metadata, request patterns, standalone reads, and legitimate auth; “illustrative, not exhaustive” is appropriate. Remaining boundaries are pure timing/cache channels, which are explicitly excluded, and potentially fixed tracking pixels that disclose only render/presence. Also clarify that a channel caused by a renderer/client counts as live behavior.

5. Not fully. The benign fixtures use only `.test`/`.example` hosts, so they do not test ordinary HTTP/auth calls to a real host. A real documented API call using `requests` would be flagged by `(a)` despite carrying no secret; the piggyback fixture correctly shows that a legitimate endpoint must still be flagged when it carries a secret.

6. Yes, one §2 bullet remains the minimal amendment surface. `operational-rigor §2` has no exfil rule, and the security-architect material is a different design lens. The wording and fixture corrections can remain within this carrier.

7. None. This is prose plus inert fixtures; no runtime or tooling mechanism is proposed.

8. Yes. The packet explicitly labels the incident as attested rather than first-hand reproduced, marks the change `unprobed`, and limits the gate to static discriminating power.

The `flip-curl` fixture also has a literal inconsistency: its `.test` host is declared a placeholder, so the current rule’s “non-placeholder external host” condition would not make it an existing hit. The proposed channel clause would catch it, but the “current BLOCK” claim or fixture host must be corrected.

Required fixes:

1. Narrow `(a)` so ordinary purpose-required HTTP/socket API and auth calls are not unconditional hits; preserve no-payload detection only for genuinely unneeded beacon/callback behavior, and add a real-host benign control.
2. Resolve the scope of passive no-secret beacons and clarify that renderer/client actions caused by the skill count as live; correct the `flip-curl` placeholder/current-guidance mismatch.

FIX 1, 2
