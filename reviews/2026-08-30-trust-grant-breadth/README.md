# Trust-grant breadth — design + landing record (candidate ③)

**Landed rule:** `operational-rigor` §2 canonical — *a trust or allow rule is
judged by its effective grant expansion, never its syntax* — placed between the
instruction-files install-gate block and the activation-gated-payload rule;
plus a bare-pointer mirror in `skill-vetting` §2 (**Over-broad trust grant**,
between MCP/tool auto-registration and self-vouching). Invariant: **the
effective granted capability set must stay within what was actually vetted, or
what an independent trusted policy explicitly authorizes as a class.**

## Trail

1. **Orientation (read-only, adjudicated PARTIAL-GAP).** Existing doctrine
   catches config WRITES (config self-propagation), authorization RHETORIC
   (authorization-default flip), and tool REGISTRATION (MCP rule) — but no rule
   anywhere evaluated whether a persistent trust/allow entry's EFFECTIVE GRANT
   SET exceeds the actually-vetted set, and a candidate that merely instructs
   the human to paste a broad grant intercepted nothing. External threat
   evidence cited as shape (ATR-2026-02192; AWS Kiro AWS-2025-019) — not
   first-hand reproduced (no such artifact was cloned or executed).
2. **Owner-settled semantics.** Judge effective expansion, never wildcard
   syntax (wildcards, prefixes, globs, inherited namespaces, future-name
   patterns are examples, not the criterion); a candidate's own disclosure
   never launders the breadth; a human typing the entry on the candidate's
   instructions is not independent authorization; an independent trusted
   owner/project policy CAN authorize the broader class — the verdict then
   says authorized-as-a-class, never individually-vetted; bounded globs and
   deny patterns are protected from false hits; undeterminable expansion fails
   closed with no exhaustive future-name enumeration burden.
3. **Design review — two rounds, dual-blind** (mutually blind, isolated dirs;
   identity from tool banners in all four runs: `model: gpt-5.6-luna` /
   `model: gpt-5.6-sol`, `reasoning effort: max`). **r1 = luna FIX-1 + sol
   FIX-2**: convergent finding — the mirror restated the operative criterion
   and clearance fragments, an incomplete second authority; sol additionally
   flagged the headline ("silently" wrongly implied disclosure could matter,
   and the independently-authorized limb was missing). Both findings were
   reproduced first-hand and fixed. **r2 = luna PROCEED + sol PROCEED — 2/2,
   zero findings**, all ten mandatory axes line-anchored by both reviewers
   (canonical/mirror separation and the authorized-as-a-class verdict language
   explicitly confirmed by both). Packets in `design-review-packet-r1.md` /
   `design-review-packet-r2.md`; verdicts in `verdicts/`; per-reviewer packet
   copies were byte-identical per round (hashes in
   `FINAL-WORDING-RECONSTRUCTION.md`).
4. **Owner adjudication.** Final wording ratified; implementation and
   landing-to-PR authorized, with reviewer closure conditioned on the landed
   blocks proving byte-identical to the r2-reviewed blocks (any third
   substantive wording change → STOP; never triggered). Marker/provenance
   shape settled: exactly one inline `unprobed` marker on the canonical rule;
   an owner-settled Provenance entry in operational-rigor; the mirror owns no
   criterion copy, no clearers, no fail-closed wording, and no marker.
5. **Landing.** Both reviewed blocks landed **byte-verbatim**
   (`FINAL-WORDING-RECONSTRUCTION.md`); declared landing adaptations: the
   Provenance entry and placement only — the inline marker was already inside
   the r2-reviewed bytes.

## Status

The rule carries **exactly one** new `unprobed` marker (canonical only; the
mirror has none). **Behavioral transmission/effectiveness remains unprobed**;
the future behavioral probe joins the standing #115 queue. Static
discriminating power only — see `STATIC-CONTROLS.md` (W1–W8 + W2b, 9/9). The
three locked sibling candidates (compiled-bytecode/decoy-source divergence;
visible homoglyph deception; approval-fatigue reviewer-targeting) remain
LOCKED — zero of their content here. Target runtime: runtime-agnostic (pure
instruction text; no executable dependency).
