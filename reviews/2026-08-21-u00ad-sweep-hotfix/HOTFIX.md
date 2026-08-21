# U+00AD sweep hotfix - evidence record (2026-08-21)

Base: main @ 6069aad4a408994076ccf96ce8ab79a1a4199369 (clean tree).
Provenance: mining-intake batch 2026-08-21, item 7 (P0 MUST-FIX / sole
first-thaw item; owner-granted bounded hotfix). Scope grant: U+00AD only;
canonical-set derivation machinery explicitly OUT of scope; U+0085/U+180E
(whitespace-padding class, adjacent but different threat class) boundary-
adjudicated OUT - the pre-fix contract never included them on any surface.

## Semantic target (locked)

new set == old 145-set union {U+00AD} == 146, on all three carriers.
Nothing else changes: no other ranges, no severity/failure wording, no
detector refactor, no historical provenance/reviews edits, no distribution-
copy sync.

## Substantive edits (exactly 3 carriers, canonical propagation order)

1. skills/operational-rigor/SKILL.md section 2 (CANONICAL prose, per the
   in-file sync contracts in skill-vetting): adds "the soft hyphen (U+00AD)"
   to the sweep enumeration.
2. skills/skill-vetting/SKILL.md section 2 (synced copy; its own text names
   operational-rigor section 2 as canonical): mirrors the same item.
3. .github/checks.py: BAD character class gains the U+00AD token; the
   adjacent enumeration comment gains "soft hyphen" (same carrier, same
   semantic item - comment kept truthful to the class it describes).

## Evidence index (this directory)

- proof.py            two-sided proof engine; ASCII-only source (self-checked
                      at import), every probed character constructed via
                      chr() - no literal invisible characters anywhere.
- RED-baseline.txt    baseline @ 6069aad: 145 x3 surfaces, set-equal;
                      U+00AD absent everywhere and NOT caught by the live
                      regex; known-bad U+200B caught; legit controls clean.
- gate-demo-RED-full.txt   tracked mutant containing chr(0xAD) + baseline
                      bytes: "all checks passed", exit 0, sweep counted it
                      among 1444 clean files - the live gate was blind.
- GREEN-post.txt      patched tree: 146 x3 surfaces, set-equal; U+00AD
                      caught; exact set delta == [U+00AD]; nothing removed;
                      all old 145 individually still caught; legit controls
                      still clean.
- gate-demo-GREEN-full.txt same mutant + patched bytes: FAIL
                      "hidden-directive/zero-width char in .../mutant-
                      fixture.md", exit 1. Mutant was transient proof
                      material only - untracked and deleted afterwards,
                      never committed.
- checks-final-green.txt   clean patched tree: "all checks passed", exit 0;
                      sweep line covers 1443 tracked text files, which with
                      the patched detector doubles as the tree-wide proof
                      that no tracked file carries U+00AD (no remediation
                      needed).
- hotfix.diff         the exact 3-carrier working diff against 6069aad.
- gate/               cross-model review packet + reviewer verdicts.

## File hashes (sha256, script-generated - see stamp below)

    a76198769b954c086aabed1a28c300a67cff38cb2527b4645cc861cc835aa854  skills/operational-rigor/SKILL.md
    819963c127eecce5befc7dd56b67b412f9ce7a7619f73bbaa62935a3b8b36a12  skills/skill-vetting/SKILL.md
    578255f2ecda544434e249560532c167d7e2e3573d7af61847d6a64df9068047  .github/checks.py
    90535a40fbca299a163d2f2a784bb4335d821a29c9b620374028a3cad69f0bf3  reviews/2026-08-21-u00ad-sweep-hotfix/proof.py
    982fef7de32922e53ae025010eb637be0ed427f4128cf5ef0ebed30698ab100a  reviews/2026-08-21-u00ad-sweep-hotfix/RED-baseline.txt
    4be9a01b90c101c4b04744ae68f87b4a4ea26d365321ddde1cc519e0de823c3c  reviews/2026-08-21-u00ad-sweep-hotfix/GREEN-post.txt
    02b4754b92b19c7b83d4a88b389fca10f47df1b98c480c2eb5cf8aed792fb5fb  reviews/2026-08-21-u00ad-sweep-hotfix/gate-demo-RED-full.txt
    40dc5ff76b9f44d670f04e78e43396a3097c095e17f5dfc6b44624f553181081  reviews/2026-08-21-u00ad-sweep-hotfix/gate-demo-GREEN-full.txt
    b6b359c5bfe7146e8eada7d419a9e9ae4e30361809d087731eaeacd9300027bf  reviews/2026-08-21-u00ad-sweep-hotfix/checks-final-green.txt
    d38abbcec8b185a73224460638785028af2699b4d9d1d08bfd78a0de4cfe8f14  reviews/2026-08-21-u00ad-sweep-hotfix/hotfix.diff

## Cross-model gate outcome (appended post-review)

gpt-5.6-luna (max) + gpt-5.6-sol (max), mutually blind, round 1:
PROCEED x2, zero findings, Q1-Q8 clean on both. Identity banners,
verdict lines, and gate-file hashes: gate/RECORD.md. Reviewed-bytes
check: packet-pinned sha256 of all three carriers matched the
committed blobs and working tree at landing time (3/3 OK).
