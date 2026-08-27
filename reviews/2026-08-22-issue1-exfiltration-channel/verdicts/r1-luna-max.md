1. Yes. Current text is explicitly command-framed: “**Exfiltration-shaped commands.** `curl`/`wget`/`nc`.” The markdown fixture has no transport command, and the DNS fixture uses `socket.getaddrinfo`; both therefore slip through. The `curl` flip remains covered.

2. Yes. “Any outbound channel … carries the secret” covers the image URL/query and DNS label. “NOT the mere presence of a remote image or a DNS lookup” preserves legitimate image and DNS use.

3. It correctly generalizes the existing bullet. The security-architect text’s “a path that sends data out” is a system-design capability lens, while secure-ingestion’s `src`/redirect rule concerns provenance and substitution. The existing CLI and credential-read checks remain present.

4. Yes. “Not only” plus “any outbound channel” makes the listed markdown images, `src`, preload, redirect, and DNS labels examples rather than an exhaustive transport list. Email, webhooks, HTTP libraries, and WebSockets would also fit the semantic rule.

5. Yes for the supplied controls. The remote-image fixture uses a fixed CDN asset with “no secret in its address”; the DNS fixture uses `api.example.com` with “no local secret” in the hostname. Neither should be flagged.

6. Yes. `CURRENT-TEXT.md` identifies this exfil bullet as the “sole carrier,” and operational-rigor §2 contains no exfiltration rule. Reframing that bullet is the smallest non-duplicative amendment.

7. None is needed. This is a static checklist wording change; the fixtures are explicitly inert and no runtime probe or tooling mechanism is introduced.

8. Yes. The packet labels the incident as an attested shape but explicitly says it was not firsthand reproduced, no artifact was executed, and the gate is only static discriminating power. That is appropriately honest.

Residual boundary: pure non-network covert channels such as timing, cache, acoustic, or power side channels remain outside this outbound-channel rule. No supplied benign case misfires. The “ordinary API endpoint” carve-out should be read as exempting endpoint presence alone—not an unnecessary secret sent through that endpoint.

PROCEED
