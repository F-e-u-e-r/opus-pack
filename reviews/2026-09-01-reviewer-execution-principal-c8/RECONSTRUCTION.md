# Faithful reconstruction — landed doctrine from archived design bytes

Claim proven machine-checkably (`closure/reconstruction_check.py`, 22/22
PASS, log `closure/reconstruction.log`):

> landed design = archived v4 (sha256 `07f53b8c…`) + exactly MOD-AXIS-MODE
> (one `read_reach:` line; repaired design sha256 `788f80c7…`; single-line
> byte-delta proof `closure/mod-axis-mode.diff`) + the declared adaptations
> below. No second substantive correction exists (checks R6/R7 prove the
> landed bullets equal the raw candidate-block extractions modulo A1 only).

Declared adaptations (the only permitted classes: marker / provenance /
placement):

- **A1 (placement)** — one reference-pointer sentence inserted into the D&R
  §3 bullet after the surplus-reach clause, pointing to
  `references/reviewer-capability-receipt.md` (the pack's split precedent:
  protocol bodies live in references; the core bullet keeps trigger, claim,
  and pointer).
- **A2 (placement)** — the schema gloss's design-internal "§5" section
  reference retargeted to the reference file's own Mode section; wording
  otherwise identical, semantics identical (the design's §5 was its CMR
  section; landed, the trigger statement lives beside the schema).
- **A3 (placement)** — reference-file framing: header/intro; a Mode section
  making the receipt's mode representable as a DERIVED classification
  (owner mode-representability ruling) that is never a single-field alias;
  a rule-6 normative kernel replacing the design's session-specific
  assertability example (which lives in this package instead); a Named
  probes section carrying the design §11 indirection exclusion and the
  propose→grant path. Rules 1–5 and the schema fence are verbatim
  extractions (checks R8/R9).
- **Marker** — exactly one `unprobed` debt, in the D&R §3 bullet headline;
  none in the CMR pointer or the reference (check R10).
- **Provenance** — the D&R and CMR provenance entries are new text authored
  for landing (`closure/dr-provenance-entry.txt`,
  `closure/cmr-provenance-entry.txt`), recording the full honest history:
  original gate CAP-REACHED / NOT-PASSED, NC1 NOT-PASSED (1/2), owner
  repair + mechanical closure as the acceptance source.

Generator: `closure/gen_landed.py` (extraction IS the derivation);
composer: `closure/compose_landing.py` (unique-anchor asserted insertions).
Sealed sources: the two owner-held archives whose hashes and per-file
manifests are in `closure/` (`c8-design-gate-20260831.tar.gz` `9e32e4a4…`
86/86; `…20260831b-postNC1.tar.gz` `6841764f…` 104/104 — `gate-record/` is
the verified extraction of the latter). Tar binaries themselves are NOT
committed.
