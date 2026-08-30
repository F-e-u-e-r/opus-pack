# My own adversarial read of the ⑥ wording (pre-reviewer baseline)

Formed BEFORE reading luna/sol R1, so convergence is meaningful and I hold my own
reproduction of each candidate defect.

## Candidate weaknesses

- **W1 (3a density).** The op-rigor sub-bullet is one long chain. A weaker executor
  could lose the three-limb requirement or the machine-identity precision. Watch a
  reviewer readability flag; a sentence-structure split (obligation / what-is-a-finding
  / what-is-NOT / normalization) may help without changing meaning.
- **W2 (machine-identity concreteness).** "verify the token's actual machine identity
  under the relevant boundary" is the owner's precision correction (raw code points ≠
  universal identity). It is abstract; a weak executor may not know what to *do*. The
  intended act: compare against the identity the security decision's consumer actually
  uses (the bytes/normalized/parsed form at that boundary), not the glyphs. If a
  reviewer asks for a concrete anchor, a short "(compare what the consumer of the
  decision actually keys on)" could help — but must not collapse back into
  "raw code points", which the owner explicitly rejected.
- **W3 (three-limb enforcement).** "needs all three" is explicit and the carve-out
  sentence blocks presence-only firing. Likely sufficient; watch for a reviewer who
  thinks a weak model still fires on non-ASCII presence.
- **W4 (co-fire naming).** Naming exfiltration/trust-grant/fabricated-authority is
  good for axis 7 but couples to three specific rules; acceptable and matches the
  owner's dedup intent.
- **W5 (sv pointer reference).** "Apply operational-rigor §2's visual-identity rule" —
  the op-rigor sub-bullet has no formal title; the reference is by content. Minor;
  a reviewer might want the reference disambiguated, but the mirror must stay bare.
- **W6 (scanner exclusion in wording).** "no character class decides this — a
  per-identity comparison, not a sweep" signals not-a-scanner. It does not literally
  say "not a whole-repo CI gate" — that architectural decision is deliberately NOT in
  the canonical wording (it belongs to the scanner-architecture ruling, already
  SUPPORTING-ONLY). Leave out of wording unless a reviewer reproduces a real risk that
  the wording reads as mandating a scan.

## Axes I judge already satisfied (my read)
1 new C-principle (explicit "sweep catches what you can't see; this catches what you
can") ✓; 2 machine-identity avoids raw-code-points-universal ✓ (see W2 concreteness);
3 three limbs required ✓; 4 multilingual/accented/mixed carve-out ✓; 5 cross-script
not necessary (examples `rn`→`m`, `1`→`l`) ✓; 6 invisible rule independent + co-fire
✓; 7 ①/③/fabricated co-fire not subsumed ✓; 8 normalization supporting-only ✓; 9
op-rigor sole authority, sv bare ✓; 10 per-identity comparison not a sweep ✓ (see W6);
11 material identity decision required ("security decision depends on recognizing …
as a particular … identity") ✓.

Net: no correctness defect I can reproduce yet; W1/W2 are the most likely
reviewer-polish targets.
