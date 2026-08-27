# Static discrimination — exfiltration-channel reframe (① gate)

Applies the **landed** skill-vetting §2 "Exfiltration-shaped channels" bullet
first-hand to each inert fixture (doctrine, not executable — expected verdict written
before the determination, operational-rigor §4). All fixtures INERT (placeholder
`.test` / reserved `example.com` hosts, "NOT runnable", synthetic paths); none
executed. `.test` stands in for a real non-placeholder attacker host, `example.com`
for a real documented benign host — evaluate the SHAPE, not the literal host string.

Owner-locked classifications — all confirmed:

**BLOCK / finding**
| Fixture | Why | Verdict |
|---|---|---|
| fail-markdown-image-exfil | secret in a passively-fetched image URL (b) | **BLOCK** ✓ |
| fail-dns-label-exfil | secret encoded in a DNS hostname/label (b) | **BLOCK** ✓ |
| fail-piggyback-needed-endpoint | secret piggybacked on an otherwise-legit API call (b) | **BLOCK** ✓ |
| (markdown fixture also covers) header/`Referer` disclosure | request metadata carries the secret (b) | **finding** ✓ |
| fail-* presence/count/order (covered by wording) | secret bits in request presence/count/order (b) | **finding** ✓ |
| flip-curl-exfil | inherited external `curl` finding (a) | **BLOCK** ✓ |
| fail-credential-read-standalone | sensitive credential read (a) | **BLOCK** ✓ |

**CLEAR / non-hit or explained**
| Fixture | Why | Verdict |
|---|---|---|
| benign-remote-image-legit | ordinary remote image, no secret in the address (b safe harbor) | **not a hit** ✓ |
| benign-dns-legit | ordinary DNS use, no secret in the label (b safe harbor) | **not a hit** ✓ |
| benign-conditional-request-legit | request presence gated on a disclosed non-secret setting | **not a hit** ✓ |
| benign-auth-header-legit | own credential to own documented host for required auth | **not a hit** ✓ |
| benign-curl-nosecret-legit | no-secret external `curl` — a legacy (a) FINDING the disclosed purpose EXPLAINS → **not BLOCK** (still a finding, not silently ignored) | **explained/cleared** ✓ |
| (data-vs-live) security playbook describing an exfil technique | data, not a channel the skill opens | **not a hit** ✓ |

**Control** (owner-required): ordinary HTTP/socket **library** use is NOT blanket-flagged
by transport itself — clause (a) lists only `curl/wget/nc` CLIs; a library HTTP call that
carries no secret is cleared by (b)'s safe harbor (`benign-auth-header-legit`,
`benign-conditional-request-legit`, `benign-dns-legit` all use libraries and clear).

10/10 inert fixtures discriminate as intended. STATIC discriminating power only —
behavioral effectiveness NOT probed (see README).
