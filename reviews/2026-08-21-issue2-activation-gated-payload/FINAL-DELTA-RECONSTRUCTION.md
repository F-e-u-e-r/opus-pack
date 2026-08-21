# Final-delta reconstruction — landed wording vs R3-reviewed wording

Proves: **landed canonical/mirror bytes = R3-reviewed bytes + the two
owner-adjudicated deltas + named adaptations to the canonical home**, with zero
unaccounted *wording* drift. Word-level diff (whitespace/wrap normalized) run in
the gate; every hunk annotated below. R3-reviewed source = the exact packet Luna
and Sol saw in round 3 (preserved in the private evidence package).

## Canonical (operational-rigor §2) — R3 → landed

| Hunk | R3 | Landed | Accounted as |
|---|---|---|---|
| 1 | `**disclosure … effect**` | `disclosure … effect` | Formatting only — words identical; inline bold dropped to match op-rigor §2 style (emphasis via CAPS/plain, not mid-bullet bold). Zero wording change. |
| 2 | *(absent)* | "Here, harmful means unauthorized, deceptive, or adverse to the user contrary to the candidate's authorized, disclosed purpose; high-impact behavior is not harmful merely because it is destructive or powerful when it is expressly authorized and within that purpose." | **Owner Decision 1** (the adjudicated `harmful` boundary, verbatim). |
| 3 | "…live gate (the exfiltration rule's data-vs-live distinction)." | "…live gate." | **Named adaptation**: operational-rigor §2 has no exfiltration rule (that bullet lives in skill-vetting §2), so the dangling citation is dropped and the data-vs-live point stands self-contained. |
| 4 | *(absent)* | "(`unprobed` — see Provenance.)" | **Owner land-unprobed decision**: the single marker on the canonical rule. |

No other canonical difference. Similarity 0.905; hunks 2 and 4 are additions, 1
is formatting, 3 is a forced correctness fix for the canonical home.

## Mirror (skill-vetting §2) — R3 → landed

The mirror was rewritten to a **bare pointer** — this IS **Owner Decision 2**, so a
large diff is expected and intended. Every hunk maps to that decision or a named
adaptation; none adds criterion content (mechanically confirmed: the mirror
contains no harmful-definition / predicate-list / clearance / fail-closed text).

- **Decision 2 (bare pointer)**: removed the entire criterion parenthetical
  ("that clause owns the criterion (harmful…; trace…; disclosure and labels never
  clear…; opaque-material logic fails closed)"); adopted the owner's specified
  verbs "**Apply** operational-rigor §2's activation-gated-payload **check**" and
  "**It supplements** the exfiltration bullet…"; and "skill prose as much as to
  **executable helpers**".
- **Named adaptations**: `§1.5` → `§1's fixture obligation (step 5: …)` —
  skill-vetting has no `### 1.5` heading and refers to procedure steps as "step N"
  (also keeps the normative-reference gate non-dangling); `exfil` → `exfiltration`
  to match the referenced bullet's name; incidental de-capitalisation (`SHAPE` →
  `shape`).

No criterion text migrated into the mirror; the canonical remains the sole home.

## Fixture-set provenance
- R3 fixture set (8): the original inert set plus the R3 cheap-fix additions
  (inspectable ungated flip; non-exfiltration config-self-prop FAIL; the "deferred"
  wording correction on the mixed fixture) — all applied before owner adjudication.
- **+1 (Decision 1)**: `benign-authorized-highimpact` — the authorized-high-impact
  control the owner approved. Total = 9, all inert, discriminating 9/9
  (`STATIC-DISCRIMINATION.md`).

## Conclusion
Landed = R3-reviewed + Decision 1 + Decision 2 + land-unprobed marker + the two
named canonical-home adaptations (drop the non-existent-rule citation; §1/step-5
and exfiltration-spelling in the mirror). **Zero unaccounted wording drift.**
