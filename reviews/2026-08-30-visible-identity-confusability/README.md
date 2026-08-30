# ⑥ Visible identity confusability (homoglyph) — evidence package (2026-08-30)

Full audit trail for the operational-rigor §2 visible-identity-confusability limb and
its skill-vetting §2 pointer. Branch `visible-identity-confusability` from main
`0913e4b`.

## What the change does

The pack already had an **invisible-Unicode** rule (zero-width / bidi / Tag Block —
characters you cannot see, that hide or reorder directives). It had **no** rule for
the opposite deception: characters you *can* see, where a homoglyph renders like a
trusted token but is a **different machine identity** (Cyrillic `а` for Latin `a`;
`scоpe` for `scope`; `rn` for `m`; a digit `1` for `l`). A reviewer can read every
visible character and still mistake one identity for another.

Disposition: **GENUINE-DISTINCT-GAP** (no existing rule carried a "verify identity,
don't trust appearance" principle — the invisible rule is concealment; exfiltration
needs a secret in an address; fabricated-authority is a semantic claim; the
full-source read reads glyphs without comparing identity). Abstraction: **L2 —
security-relevant identity confusability**. A finding requires all three of a
**distinct machine identity + plausible visual impersonation + security-relevant
reference identity**.

The canonical rule lives in operational-rigor §2 (immediately after the
invisible-Unicode sweep); skill-vetting §2 carries a bare routing pointer.

## Two load-bearing statements

> **A mechanical confusable signal is evidence for review, not the verdict.**

> **No claim is made that the full Unicode / IDNA spoofing space was first-hand
> tested.**

The scanner architecture is **SUPPORTING-ONLY**: no `.github/checks.py` change, no CI
gate, no runtime scanner, no canonical confusables table. The canonical decision is a
review-time per-identity comparison.

## Contents

- `orientation-summary.md` — the GENUINE-DISTINCT-GAP orientation.
- `harness/h_probe.py` + `harness/h_result.json` — the H1–H11 first-hand mechanism /
  semantic-discrimination battery and its results. **Evidence, not production
  enforcement** — deliberately not wired into CI. (`h_result.json` is emitted
  `ensure_ascii`, so it carries no literal invisible/control code points; the
  `codepoints[]` fields keep the U+XXXX record.)
- `design-packet.md` — the self-contained review packet.
- `verdicts/luna.md`, `verdicts/sol.md` — the two reviewer verdicts.
- `gate-trail.md` — the design-gate trail (R1 PROCEED × 2).
- `self-review-notes.md` — the author's pre-reviewer adversarial read.
- `final-wording.md` — the R1-reviewed canonical block as landed + the marker note.
- `landing-manifest.md` — declared adaptations and the faithful-reconstruction battery.
- `MANIFEST.sha256` — hashes of every file in this package.

## Key first-hand results (CPython 3.9.6, unicodedata Unicode DB 13.0.0)

- **H1–H4:** a visible homoglyph passes the shipped `.github/checks.py` invisible
  sweep unflagged (first-hand), while **H8** (zero-width / bidi) is caught by that
  sweep — the two mechanisms are orthogonal.
- **H5/H6/H7:** legitimate multilingual / accented / mixed-script text is **not** a
  finding for its Unicode alone.
- **H9:** NFC/NFKC folds a compatibility ligature but **never** a cross-script
  look-alike — normalization is supporting only.
- **H10:** the same confusable in decorative prose vs a `trustedCommands` entry —
  severity scales with the reference boundary, not mere presence.
- **H11:** `rnicrosoft`→`microsoft`, `paypa1`→`paypal` impersonate a trusted identity
  **without crossing scripts** (a cross-script-only rule misses them); `teh` with no
  reference identity is CLEAR (not generic typo policing).

**Mechanism and semantic discrimination = first-hand verified.** The rule's
**behavioral effectiveness = unprobed → one canonical marker → standing #115.** These
are separate: the marker does not mean the mechanism is unverified.

## Review

Dual-blind **two-variant** review (two variants of one GPT-5.6 family, both at max
effort) — both outside the author family; **NOT a cross-family gate** (grok
unavailable this window; family-diversity caveat retained). **R1 PROCEED × 2**, all
eleven review axes passing.
