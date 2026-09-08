# skill-vetting · references: provenance

Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): the skill's historical review, probe, and amendment records. Canonical rules and inline debt markers remain in `SKILL.md`; any operative re-verification caution stays inline there too. This file is history only.


Operationalizes operational-rigor §2's third-party-executable-content and
instruction-files install gate (canonical home; quoted verbatim where a clause is
load-bearing per skill-authoring §5). The trojan-shape checklist (§2) is distilled
from two live incidents: the 2026-07-12 twelve-source community-security-skill audit
(3 live trojans; loader-run `!` syntax, invisible-Unicode, and agent-config vectors
observed - see README acknowledgements) and a 2026-07-24 starred-repo mining pass
that caught a 4th (self-propagation into `~/.claude/CLAUDE.md`, an authorization
flip, and an agent-obedience-engineering manual with fabricated authority
citations). Ships `unprobed` per the covenant - the discriminating probe is a
weak-tier arm given the caught trojan as a candidate (its payload spread across
RULES.md, precedent-auth.md, and a kali README - none in the top-level entry
file): does the ruled arm read the whole tree, reach BLOCK, and surface it, versus
a bare arm that installs it? Those files are retained privately as the vetting
skill's regression fixtures (they are not shipped in this tree); that probe joins
the private round-5 queue.

The §2 exfiltration bullet was reframed from *commands* to *channels* (2026-08-22,
issue ①) — covering renderer/resource auto-fetch (secret in a passively-fetched
URL/`Referer`), DNS-label exfil (secret in a hostname, carried by name resolution),
and request-metadata / presence-count-order encodings, while keeping the legacy
`curl`/`wget`/`nc` + credential-read triggers as findings-to-explain. It adds no
separate probe marker: its behavioral transmission/effectiveness debt is the same
skill-level covenant this skill already carries above, and a future issue-①-specific
probe is a #115 routing decision, not a new inline marker. Design review was a
three-round cross-family gate (gpt-5.6-luna + gpt-5.6-sol, max effort, mutually
blind) that ended at the round cap with luna PROCEED / sol FIX; the final bounded
precision fixes and the finding-to-explain layering (Option X) were owner-adjudicated,
not a 2/2 consensus. Evidence: `reviews/2026-08-22-issue1-exfiltration-channel/`.

The companion hook `hooks/skill-vetting-advisory.py` is a delta-detector, not a
scanner: signature scanning was removed at the 2026-07-25 cross-family security
gate (grok-4.5 high + gpt-5.6-luna ultra + gpt-5.6-sol max) because a text regex
is not a security boundary - low recall on prose / cross-file / split payloads,
plus false assurance and an injection surface. The demoted patterns live as this
skill's §2 checklist (the agent's full read) and as private regression fixtures,
never as a runtime detector. The same gate's rounds 2-3 drove the observation
layer into the separately-tested `hooks/skill_snapshot.py` primitive (injective
length-prefixed encoding, fd-verified reads, fail-closed anomalies, hardened
baseline I/O, delivery-before-advance ordering); the threat model and invariants
live in `reviews/2026-07-25-skill-vetting-snapshot-threat-model.md`. 
