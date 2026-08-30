# Landing / adaptation manifest — ⑥ visible identity confusability

Branch `visible-identity-confusability` from main `0913e4b`.

## Declared adaptations relative to the R1-reviewed blocks

Exactly three, all owner-authorized:

1. **One inline canonical marker** — ``(`unprobed` — see Provenance)`` on the
   operational-rigor §2 limb's opening sentence ("Do not trust visual sameness as
   identity").
2. **One operational-rigor Provenance entry** — the ⑥ record (model-agnostic: it
   describes a dual-blind two-variant review without naming model slugs; the slugs
   live in this trail's `verdicts/`).
3. **Pure Markdown placement/wrapping.**

> **DECLARED SUBSTANTIVE ADAPTATIONS = NONE.** No operative statement of the
> R1-reviewed canonical (3a) or mirror (3b) was changed. There is no W3-style
> renumber this time — both edits are pure insertions.

## Placement

- op-rigor §2: the new sub-bullet sits **immediately after the invisible-Unicode
  sweep sub-bullet and before the "Any read/write of CLAUDE.md …" sub-bullet**, under
  "Instruction files are executable content" — the semantic-sister position (invisible
  = can't-see; ⑥ = looks-same).
- skill-vetting §2: the bare pointer sits **immediately after "Invisible-Unicode
  smuggling" and before "Exfiltration-shaped channels"**.

## Faithful-reconstruction battery (all PASS)

| # | Check | Result |
|---|---|---|
| 1 | op-rigor landed limb == R1-3a canonical **+ exactly the marker insertion** (whitespace-normalized) | PASS |
| 2 | skill-vetting pointer == R1-3b mirror (whitespace-normalized) | PASS |
| 3 | op-rigor diff = pure insertion (72 lines, **0 deletions**) — invisible-Unicode sweep + adjacent CLAUDE.md/config rule + all other content byte-unchanged | PASS |
| 4 | skill-vetting diff = pure insertion (3 lines, **0 deletions**) — the invisible-Unicode bullet and everything else byte-unchanged | PASS |
| 5 | security-architect.md zero-byte (not in diff) | PASS |
| 6 | **exactly one new debt identity** — op-rigor `(\`unprobed\`` markers 32 → 33 (+1, on the new limb) | PASS |
| 7 | skill-vetting marker count unchanged (0 → 0); word `unprobed` unchanged (1 → 1) | PASS |
| 8 | skill-vetting mirror carries no criterion / machine-identity definition / clearer / normalization / fail-closed / marker | PASS |
| 9 | added-text Unicode hygiene — the new canonical, provenance, mirror, and this evidence carry **no invisible/control code points**; fixture code points are escaped (`h_result.json` `ensure_ascii`) or `chr()`-constructed (`h_probe.py`) | PASS |
| 10 | evidence copies re-hash equal to the session originals | PASS |
| 11 | H1–H11 saved evidence re-machine-checks PASS; H1–H4 still pass the shipped invisible sweep; H8 still hit by it; H5/H6/H7 controls preserved; H11 shows cross-script not necessary | PASS |
| 12 | L3 not activated; no full-repo confusable scanner; no `.github/checks.py` / tooling mutation | PASS |
| 13 | no claim that the full Unicode / IDNA spoofing space was first-hand tested | PASS |
| 14 | git diff scope = the two skill files + this package only (④/⑧/#149/PARKED zero-byte) | PASS |
| 15 | `.github/checks.py` green (incl. its invisible/control-Unicode sweep) | see PR / CI |

## Mechanism-verified vs behavioral-unprobed (do not conflate)

- **Mechanism / semantic discrimination** (visible homoglyph survives the invisible
  sweep; code-point↔glyph divergence; normalization partial; cross-script not
  necessary; multilingual carve-outs): **FIRST-HAND VERIFIED** (H1–H11, CPython
  3.9.6). Not "rule unverified".
- **Instruction effectiveness** (does the rule make a real reviewer catch a same-shape
  visual-identity deception better than bare doctrine?): **UNPROBED** → the single
  marker → standing **#115**.

## Scanner architecture

**SUPPORTING-ONLY.** A mechanical confusable / mixed-script signal is evidence for
review, not the verdict. No checks.py change, no CI gate, no runtime scanner, no
canonical confusables table. The L3 Unicode/IDNA/identifier-security framework was
discovered and deliberately **not activated**.

## Family-diversity caveat

The two reviewers are both outside the author family (Claude) but are two variants of
one GPT-5.6 family — a dual-blind **two-variant** gate, **not cross-family** (grok
unavailable this window). Recorded honestly; the pack Provenance entry says the same.

## Scope

Committed changes: `skills/operational-rigor/SKILL.md`,
`skills/skill-vetting/SKILL.md`, and this `reviews/…` package. Everything else is
zero-byte, including security-architect, `.github/checks.py`, and all other
workstreams. `.claude/` is a gitignored live-install copy and is not part of this
change.
