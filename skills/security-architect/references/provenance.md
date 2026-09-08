# security-architect · references: provenance

Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): the skill's historical review, probe, and amendment records. Canonical rules and inline debt markers remain in `SKILL.md`; any operative re-verification caution stays inline there too. This file is history only.


Authored 2026-07 from the user's security-skill reference draft (kept:
method pipeline, severity tiers, platform table skeleton, JWT checklist, DB
default-deny + negative tests, MCP risk ladder, never-paste-secrets rule;
added: IDOR, injection, password hashing, cert-validation bypasses, secret
incident response, PKCE rationale; fixed: EncryptedSharedPreferences now
deprecated) and standard references (OWASP Top 10, RFC 8252, RFC 7636).
The unprompted-load triggers, minimal-contact rule, and injection-surfacing
line (2026-07) come from the pack's own eval rounds 1–2
(reviews/2026-07-11-pack-eval-rounds-1-2.md): this skill fired 0/24 under
user-ask-shaped triggers while injections were actively being handled; the
strongest model refused an embedded directive without surfacing it; one run
read a credentials file it did not need.
The JWT key-resolution item, the SCA-in-CI line, and the magic-byte upload
wording (2026-07-12) adopt ideas surfaced in a 12-source community
security-skill audit (mukul975 / gitgoodordietrying / jgarrison929 — ideas
only, no code; see README acknowledgements).
The 2026-07-13 additions (subprocess-secret-via-stdin; the "secure ingestion of
untrusted contributions" section — reviewer-sees-equals-what-runs, allowlist
projection, prevention-by-construction, self-downgrade-only, minimize-by-type)
distill a cross-repo mining pass over seven independent retiring-architect
`skills-staging/` libraries (class-distilled convergence; no single citable commit).
The 2026-07-13 spend/abuse-bounds section, SSRF redirect clause, webhook
ack/atomic-dedup, dispatcher-auth, proxy-IP-trust, presigned-URL, log-sink
amplification, and MCP-stdio-timeout items are mined from four further private
production retiring-architect libraries (a link-shortener service, a market
dashboard, a Telegram bot post-security-audit, an engine-parity port); each
rule is backed by a cited incident commit or audit finding in its source
library (private repos — incidents verifiable by the contributor, not linkable
here).
A 2026-07-16 two-family post-merge review (grok-4.5 + gpt-5.6-sol;
trail in `reviews/2026-07-16-post-merge-validation-pr25-29.md`) made the
webhook dedup row the enqueued event itself and added the
reconcile-before-reclaim precondition on expiring spend holds.
The capability-triangle rule (2026-07-24) adapts agent-standard-oss's §10
capability-triangle bullet (MIT, ideas only; see README acknowledgements —
a founding source's post-anchor delta, fetched and quote-verified at their
HEAD 2d3bcb5), adopted for its composition framing: break-one-side is both
the design duty and the exception mechanism for systems that legitimately
need all three capabilities somewhere. Ships `unprobed` per the covenant;
its probe joins the private round-5 queue.
The AI-agent guardrail/denial-of-wallet rule (2026-07-24) adapts
cloudflare/security-audit-skill's AI-and-LLM findings bar (MIT, ideas only; see
README acknowledgements) — the ideas that a prompt-embedded guardrail is not an
enforced control and that an unbounded agent-tool loop is a denial-of-wallet
class, bounded here to enforcement (the triangle/ladder) versus prompt; its
task-scoped-credential point was already covered by this section's per-tool
minimum-scoping and is not restated. Ships `unprobed` per the covenant; its probe
joins the private round-5 queue. The same pass sharpened the Web-checklist SSRF
clause to name the loopback / link-local / private ranges and the cloud metadata
endpoint `169.254.169.254` explicitly — standard SSRF hardening the existing
"block internal ranges" clause already implied, enumerated after
Nutlope/hallmark's URL-fetch checklist surfaced the metadata-endpoint omission
(MIT, ideas only); a sharpening of an existing rule, not a new behavioral rule.
The 2026-07-31 additions (threat-model system-scoping, severity-binds-to-
evidence, audience-check-on-disclosure, subprocess-environment
minimization, the policy-shaped-data tier) distill a two-repo mining pass
over public Apache-2.0 sources — an agentic security-scanning product's
threat model, runtime security notes, bundled review doctrine, and
tracker-intake rules (ideas
only, no text; see README acknowledgements). The evaluation behind the
batch ran a ten-agent verbatim scan across two model families plus a
third-family cross-check, with every load-bearing citation re-verified
against the source; it kept only concepts the adjudication found no
existing-skill equivalent for. All five ship `unprobed` per the covenant; their
probes join the private round-5 queue.
The rule-7 boundary-crossing-diagnostic clause (2026-08-01) is the
security-architect slice of the same pass's deferred backlog (opus-pack
#112, triaged under #115 Phase 1; ideas only, no text — sourcing as above).
It was deferred at the original gate for wording that would not outlaw
legitimate inner-boundary debug logging; the crossing/inner split here is
that wording. Ships `unprobed` per the covenant; its probe joins the
private round-5 queue.
The AI-agent/MCP admission rule — verification surface must cover the mutation
surface, deny-by-default when it cannot (2026-08-04) — is mined from
sd0xdev/sd0x-dev-flow's `orchestrate` skill (MIT, ideas only; see README
acknowledgements): its deny-by-default admission gate keyed on whether
monitoring covers what a worker/tool class can mutate. It closes a gap this
section's least-privilege ladder left open — scoping bounds what a tool MAY
change, not whether you can observe what it did. Surfaced by a cross-family
review (gpt-5.6-luna) that caught it where a first pass had wrongly judged it
already covered by least-privilege plus fail-closed-on-unknown. Ships `unprobed`
per the covenant; its probe joins the standing #115 queue — a future
campaign, not round-5, which was a completed, frozen ten-target slice
this rule was not part of.

The threat-model bullet's untagged-example clause (2026-08-04) comes from a
contributor incident (contributor-reported, not linkable): a PII sweep over a
private automation repo cleared an `examples/*.json` fixture on the strength
of its path and a README calling it a placeholder; it held a real family —
names, national ID numbers, dates of birth — used once because a working
end-to-end case was needed, and a path-based skip would have shipped it. The
incident evidences the default direction only; the non-ingesting
classification method, the escalation exit that routes discharge to
the owner, and the tag-at-mint pointer are this pack's reconciliation
with the never-read-contents rule and with ground-truth-gates' sentinel
bound, not incident findings — the contributor in fact established
provenance by reading the values, which is the route this clause routes
to the owner instead. Ships `unprobed`
per the covenant; its probe joins the standing #115 queue — a future
campaign, not round-5, which was a completed, frozen ten-target slice
this rule was not part of.

The scanner-suppression bullet and the incident-response scan-scope
clause (2026-08-07) are the redesigned landing of contributed PR #152
(firaen22), dispositioned in the 2026-08-07 #151–#158 batch
reconciliation as that PR's owner-authorized surviving items. The
measured incident stands as contributed: a staged secret scanner, green
through three adversarial review rounds, tested its placeholder pattern
against the whole line, so a real format-valid AKIA-shaped key scored 0
actionable off a trailing "example" comment; the same cluster surfaced
credential-shaped self-test fixtures blocking an unrelated fail-closed
vault-sync guard, and a 2026-06 audit's one still-live leaked credential
existing only in git history (contributor-reported, not linkable). The
contribution's remedy for the fixture collision — lexically transforming
fixture literals until sibling guards stop matching — was REJECTED at
reconciliation as a guard-evasion pattern (it manufactures the blind
spot the guards exist to close) and is recorded here as that rejection,
not as a rule, so it carries no probe debt; the shipped remedy is the
existing sentinel/manifest fixture-provenance discipline
(ground-truth-gates' sentinel-tagged-fixture rule) that both new
clauses key on. Each surviving clause ships `unprobed` per the
covenant; their probes join the standing #115 queue — a future
campaign, not round-5, which was a completed, frozen ten-target slice
these clauses were not part of.


