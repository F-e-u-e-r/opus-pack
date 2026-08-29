# Final-wording reconstruction — landed bytes vs r2-reviewed bytes

**Claim:** the landed operational-rigor §2 canonical rule and the landed
skill-vetting §2 mirror are byte-verbatim the two fenced blocks of the r2
review packet (`design-review-packet-r2.md`) that both PROCEED verdicts
reviewed.

**Machine proof at landing** (pre-commit, against pre-landing main
`5824f30222124c6e474e49f6c94b8923592550b6`): (1) the landed operational-rigor file contains the
reviewed canonical block exactly once, byte-identical — block sha256
`7b566804084eec8df77e667a7be435ec1ed3630026fa6323126984e565ce003d`; (2) the landed skill-vetting file
contains the reviewed mirror block exactly once, byte-identical — block
sha256 `b1a1779a2f2ba478e683ff44494dc38a087104abd7617da4723953e719effb2d`; (3) the full diff against
pre-landing main is pure additions (zero deletions), the operational-rigor
added-line multiset equals exactly the canonical block plus the owner-settled
Provenance entry (sha256 `559727bf29b51b767d1b1da0b4c9ddce14113f88ccb05b487eacb26ba03400f0`) plus one
separating blank line, and the skill-vetting added-line multiset equals
exactly the mirror block.

**DECLARED-LANDING-ADAPTATIONS (exhaustive):** (1) the single inline
`unprobed` marker — already inside the r2-reviewed canonical bytes, zero byte
delta; (2) the owner-settled Provenance entry (adjudication layer; it carries
the file's second `unprobed` occurrence — the same one marker identity); (3)
placement — canonical between the instruction-files install-gate block and
the activation-gated-payload rule, mirror between MCP/tool auto-registration
and self-vouching; no re-wrapping was needed. Substantive semantic drift:
**0** — the implementation grant's stop-and-return clause (any third
substantive wording change) was never triggered.

**Neighbors byte-unchanged (explicitly extracted and matched):** the
instruction-files bullet, the activation-gated-payload rule, skill-vetting's
config-self-propagation and authorization-default-flip bullets, its MCP/tool
auto-registration bullet, and its self-vouching + activation-gated-payload
pointer block are each present verbatim in the landed files, and the
pure-addition multiset proof above excludes any other change. Exactly two
canonical files touched; the only other landed paths are this evidence
package. Marker accounting: operational-rigor `unprobed` occurrences 59 → 61
(inline marker + Provenance sentence — one marker identity), skill-vetting
1 → 1 (the mirror carries none).

**Special verifications (all machine-checked PASS):** the mirror carries no
criterion copy ("effective granted capability set" absent), no clearers, no
own fail-closed semantics ("nothing is restated here" present), and no
marker; the canonical carries the independent-policy limb in the headline,
disclosure-cannot-launder, human-typed-is-not-independent-authorization,
fail-closed-without-enumeration, the authorized-as-a-class verdict language,
and the deny/bounded/exact-grant protections; static controls W1–W8 + W2b
9/9 (`STATIC-CONTROLS.md`).

**Gate-artifact integrity (byte-verbatim copies of the review trail):**

```
3cee1e81272f5966ebf083a31d2fee1132c969b6b7008f772ea787e19eab06d0  design-review-packet-r1.md
d19b06726713837db4999f6afc22ba1be4bdcc2f8bb638d868e5c1c2ba895a04  design-review-packet-r2.md
059583f7d5856edc9e062795d9ee184676b2bd3f2c93e642db3b447061d4fc67  verdicts/r1-luna-max.md
187a04f32e9803cb3ee54d6b9c7154f632f4c9dcec4f7e0405cb3d08273cd50c  verdicts/r1-sol-max.md
bbbcf838f01bbd954a1f8d0e712254264db54bc47e936e269c254ba05437d277  verdicts/r2-luna-max.md
e759f2a537d8d79b867059f136b6ae732bd790bf8ad5eefbda1212108794ec42  verdicts/r2-sol-max.md
```

Per-reviewer packet copies in the gate's isolated dirs were byte-identical to
the canonical packets in both rounds (r1 packet sha256
`3cee1e81272f5966ebf083a31d2fee1132c969b6b7008f772ea787e19eab06d0`, r2 packet sha256
`d19b06726713837db4999f6afc22ba1be4bdcc2f8bb638d868e5c1c2ba895a04`); reviewer identity is from the tool
banners recorded per run (`model: gpt-5.6-luna` / `model: gpt-5.6-sol`,
`reasoning effort: max`, all four runs).
