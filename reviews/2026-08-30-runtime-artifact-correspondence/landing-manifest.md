# Landing / adaptation manifest — ⑤ runtime-artifact correspondence

Branch `runtime-artifact-correspondence` from main `5c90086`.

## Declared adaptations relative to the R3-reviewed blocks

Exactly four, all owner-authorized:

1. **One inline canonical marker** — ``(`unprobed` — see Provenance)`` on the
   operational-rigor §2 limb's opening sentence, matching the pack's existing
   bold-lead-in marker convention (the §2 trust-grant bullet).
2. **One operational-rigor Provenance entry** — the ⑤ record (model-agnostic: it
   describes a dual-blind two-variant review without naming model slugs, per the
   cross-model-review "no lineup in pack text" rule; the slugs live in this trail).
3. **W3 mechanical renumber** of skill-vetting §1 + exact call-site updates (below).
4. **Pure Markdown placement/wrapping.**

> **DECLARED SUBSTANTIVE ADAPTATIONS = NONE.** No operative statement of the R3
> canonical (4a) or mirror (4b) was changed.

## W3 mechanical changes (skill-vetting §1)

- new **step 4** inserted (the correspondence pointer)
- old step 4 (Hunt the trojan-shape checklist) → **5**
- old step 5 (executable-candidate fixture) → **6**
- old step 6 (write the verdict) → **7**
- step-2 opening-digest reference "step 6" → "step 7"
- §2 activation-gated-payload reference "step 5" → "step 6"
- §3 closing-digest reference "step 6" → "step 7"

Whole-tree call-site sweep (`grep -rnE 'vetting.*step [0-9]|step [0-9].*vetting'
skills/`): **no other file references skill-vetting step numbers.** Within
skill-vetting, the only remaining numeric step references are the two unchanged
`step 2` (opening-digest) mentions and the migrated `step 6`/`step 7` — no stray
old `step 4`/`step 5`.

## Faithful-reconstruction battery (all PASS)

| # | Check | Result |
|---|---|---|
| 1 | op-rigor landed limb == R3-4a canonical **+ exactly the marker insertion** (whitespace-normalized) | PASS |
| 2 | skill-vetting new step 4 == R3-4b mirror (whitespace-normalized) | PASS |
| 3 | op-rigor diff = pure insertion (85 lines, **0 deletions**) — existing third-party gate + Instruction-files bullet + all other content byte-unchanged | PASS |
| 4 | skill-vetting diff = step-4 insertion + exactly the 6 W3 renumber/ref changes, nothing else | PASS |
| 5 | security-architect.md zero-byte (not in diff) | PASS |
| 6 | skill-vetting steps 1 & 3 byte-unchanged; step 2 changed only the authorized `step 6→7` digit | PASS |
| 7 | skill-vetting checklist/fixture/verdict bodies byte-unchanged except numbering | PASS |
| 8 | activation-gated rule byte-unchanged except `step 5→6` | PASS |
| 9 | **exactly one new debt identity** — op-rigor `(\`unprobed\`` markers 31 → 32 (+1, on the new limb) | PASS |
| 10 | skill-vetting marker count unchanged (0 → 0); word `unprobed` unchanged (1 → 1) | PASS |
| 11 | evidence copies in this package re-hash equal to the session originals | PASS |
| 12 | no claim that JS bundles / `.so` were first-hand tested (examples only) | PASS |
| 13 | L3 not activated (no L3 rule; provenance + step-4 name it as the not-crossed line) | PASS |
| 14 | git diff scope = the two skill files + this package only (⑥/④/⑧/#149/PARKED zero-byte) | PASS |
| 15 | `.github/checks.py` green | see PR / CI |
| 16 | invisible/control-Unicode sweep green (checks.py check 4) | see PR / CI |

## Mechanism-verified vs behavioral-unprobed (do not conflate)

- **Mechanism** — the `.pyc`/correspondence failure shapes (forged checked-hash,
  hash-policy override, digest≠correspondence, source↔artifact divergence):
  **FIRST-HAND VERIFIED** on CPython 3.9.6 (P1–P8 + D1–D11). This is **not** "rule
  unverified".
- **Instruction effectiveness** — does handing this rule to a real reviewer surface
  a same-shape candidate more reliably than bare doctrine? **UNPROBED** → the single
  marker → standing **#115**. A behavioral reviewer fixture was deliberately **not**
  built this round (that measurement belongs to the queue; building it now would
  break tranche boundedness).

## Family-diversity caveat

The two reviewers, `gpt-5.6-luna` and `gpt-5.6-sol`, are both outside the author
family (Claude) but are two variants of one GPT-5.6 family. This is a dual-blind
**two-variant** gate, **not cross-family**. grok was unavailable this window. The
caveat is retained honestly; the pack Provenance entry likewise says "two-variant …
NOT a cross-family gate".

## Scope

Committed changes: `skills/operational-rigor/SKILL.md`,
`skills/skill-vetting/SKILL.md`, and this `reviews/…` package. Everything else is
zero-byte, including security-architect and all other workstreams. `.claude/` is a
gitignored live-install copy and is not part of this change.
