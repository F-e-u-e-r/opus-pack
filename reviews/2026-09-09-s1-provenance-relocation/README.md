# S1 — Provenance Relocation (M1 only)

Context-diet campaign, stage S1. Moves each skill's historical `## Provenance`
body out of the always-loaded `SKILL.md` hot layer into a per-skill
`references/provenance.md`, leaving a locator stub. Zero operative-rule
semantic change: this is a mechanical relocation proven by machine fidelity
gates, not a rewrite.

## Invariant

**Rules stay; markers stay; history moves.**

- Dated review / probe / amendment history → `references/provenance.md`.
- Live operative re-verification cautions (volatile-facts footers) → **stay inline** in `SKILL.md`.
- Canonical rules and inline debt markers → untouched in `SKILL.md`.
- Stub → a locator only, no history summary.

The classification criterion is **semantic role, not heading position**: a
sentence under `## Provenance` that still governs current behavior is not
provenance and does not move. Retained footers were selected per-skill by
meaning, never by a positional "keep the last N lines" rule (one footer —
delegation-and-review's — sits mid-history with dated entries both above and
below it).

## Per-skill disposition

| skill | MOVED-HISTORICAL | RETAINED-OPERATIVE (stays inline) | MARKER-UNCHANGED | STUB-ADDED |
|---|--:|---|:--:|:--:|
| operational-rigor | 44,035 B | volatile-facts footer (facts travel with citing rules; external-systems + §2 mount-check) | ✓ | ✓ |
| delegation-and-review | 34,759 B | re-check worktree/agent mechanics + hosted-endpoint claims *(mid-history)* | ✓ | ✓ |
| skill-authoring | 28,149 B | re-verify `gh pr list` default page size + hosted diff/file caps | ✓ | ✓ |
| ground-truth-gates | 25,606 B | `template/` scripts self-contained; re-verify via `bash template/run-all.sh` | ✓ | ✓ |
| security-architect | 8,407 B | volatile facts to re-verify yearly (platform storage APIs) | ✓ | ✓ |
| cross-model-review | 5,623 B | **session-time** model-family re-discovery caution (DO-NOT-MOVE runtime rule) | ✓ | ✓ |
| skill-vetting | 3,008 B | re-verify §2 invisible-Unicode range vs operational-rigor §2 sweep | ✓ | ✓ |
| product-roadmap | 1,674 B | none (null "nothing to re-verify" footer moved) | ✓ | ✓ |
| domain-evidence-discipline | 1,634 B | none | ✓ | ✓ |
| personal-goal-planning | 354 B | none | ✓ | ✓ |
| **total** | **153,249 B** | 1,351 B retained | | |

Hot-layer reduction across the ten `SKILL.md`: **~152 KB (~38k tokens)**.

Null/no-op footers (product-roadmap, personal-goal-planning: "nothing
environment-specific to re-verify") carry no behavioral obligation and moved
with the history. `external-systems.md` and `reviewer-capability-receipt.md`
already live in the reference layer and were **not** touched.

## Mechanical gates (all PASS — see `verify.py`)

1. **Operative-byte** — each `SKILL.md` up to `## Provenance` is byte-identical to base.
2. **Historical reconstruction** — each `references/provenance.md` body equals the base provenance with the retained footer(s) excised, byte-for-byte.
3. **Mixed-role / retained** — every retained footer is byte-identical in the new `SKILL.md` and occurs exactly once in the base provenance.
4. **Marker** — circled-marker, `unprobed`, and `#115` counts in the operative body are unchanged (guaranteed by gate 1; reported explicitly). Historical marker *mentions* inside moved provenance are citations, not canonical marker identity.
5. **Reachability** — each stub carries the `references/provenance.md` locator; the reference file exists; `<skill> §N` pointers stay non-dangling (checks.py reference gate, which scans `references/*.md`).
6. **No-hot-history** — dated-chronology density in `SKILL.md` collapses (e.g. operational-rigor 48→1, delegation-and-review 51→0); residuals are operative-body citations, not provenance.
7. **Repo gates** — `python3 .github/checks.py` green, including the zero-width/bidi sweep over the new reference files and the §7 reference-non-dangling gate.
8. **Token delta** — measured, not thresholded: ~38k tokens relocated out of the always-loaded layer.

Reference gate note: the ~134 prose `see Provenance` pointers across the
operative bodies are free-form (outside ARCHITECTURE §7's `<skill> §<number>`
grammar) and were never mechanically checked; they resolve to the retained
`## Provenance` heading, which now carries the locator onward to the reference
file.

## Reproduce

```
python3 reviews/2026-09-09-s1-provenance-relocation/verify.py      # re-derives base from 076f9d0, checks all gates; exit 0 == pass
```

`relocate.py` documents the transform (anchor-driven, dry-run by default;
`--apply` writes). Both anchor the repo root via `git rev-parse
--show-toplevel`.

## Out of scope (untouched this stage)

M2 / M3 / M4 (env-var) / M6 / M7, example compression (C1), marker boilerplate
(C2), README slimming, `description` / routing metadata, design-pack,
`external-systems.md`, wording polish, provenance rewrite/dedup, marker
cleanup, external mining. S1 takes only the clean provenance-relocation win.

Branch base: `076f9d0`. Reviewer: machine-fidelity gates (relocation-fidelity
proof object; no cross-model semantic review, by design for a mechanical move).
