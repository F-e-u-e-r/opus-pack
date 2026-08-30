# Final wording — R1-reviewed blocks as landed

Extracted verbatim from the landed skill files on branch
`visible-identity-confusability`. Both are byte-faithful (whitespace-normalized) to
the R1-reviewed blocks; the only adaptation is the single inline marker on the
op-rigor limb's opening sentence.

## operational-rigor §2 — canonical visible-identity-confusability limb (as landed)

- Do not trust visual sameness as identity (`unprobed` — see
    Provenance). The sweep above catches characters you cannot see; this
    catches characters you can — a homoglyph renders like a trusted token
    while being a different identity. Where a security decision depends on
    recognizing a name, identifier, command, path, host, tool,
    configuration key, or other authority-bearing token as a particular
    trusted, reviewed, expected, or authorized identity, verify the
    token's actual machine identity under the relevant boundary — parser,
    filesystem, case, and normalization rules may all take part, so raw
    code points are not a universal identity — rather than trusting its
    rendered glyphs. A distinct identity plausibly impersonating that
    reference identity by look-alike glyphs is a finding, whether or not
    the look-alike crosses scripts (a Cyrillic `а` for Latin `a`; equally
    `rn` for `m` or a digit `1` for `l`). The finding needs all three — a
    distinct machine identity, a plausible visual impersonation, and a
    security-relevant reference identity — so ordinary non-ASCII,
    multilingual, accented, or mixed-script text is not a finding merely
    for being Unicode. NFC/NFKC normalization is supporting evidence only
    and never clears a cross-script look-alike; no character class decides
    this — it is a per-identity comparison against the reference, not a
    sweep. The invisible-Unicode sweep above stays a separate finding, and
    this can co-fire with the exfiltration, trust-grant, and
    fabricated-authority findings without being subsumed by them.

## skill-vetting §2 — bare pointer (as landed; byte-identical to the R1 mirror)

- **Visible identity confusability (homoglyph).** A token can be fully visible yet a
  look-alike for a different identity. Apply operational-rigor §2's visual-identity
  rule; distinct from the invisible-Unicode rule above and may co-fire.

## Marker note

The R1 opening sentence was "Do not trust visual sameness as identity." The one
adaptation is the inline marker: "Do not trust visual sameness as identity
(`unprobed` — see Provenance)." — the terminal period moves after the parenthetical,
matching the pack's existing `unprobed` marker convention. Everything else in the
limb, and all of the pointer, is byte-identical (whitespace-normalized) to the
R1-reviewed text. The marker carries a single debt: the rule's behavioral
effectiveness is unprobed -> standing #115. The visible Cyrillic example glyph is an
intentional illustrative literal (a visible letter, outside every invisible/control
range); it is the only non-ASCII, non-em-dash character in the wording.
