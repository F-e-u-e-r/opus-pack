# Issue-115 verification-only probe campaign — campaign-level synthesis

STATUS: PROPOSED SYNTHESIS (read-only). This document synthesizes the
completed campaign's durable evidence. It changes no marker, no doctrine, no
skill, no sealed outcome, and no issue state; every disposition below is a
CANDIDATE for a later owner-gated action, never a decision. Behavioral
invocations in this phase: 0.

Rebuilt from durable merged bytes at main
`ac38c3acc66310268a4db7095fc00a16abc1ff37` (post-#184). Memory summaries were
not treated as authority; every number below re-derives from the merged
adjudication records, receipts, and ledger. All hashes in this synthesis are
machine-resolved (git/gh output), never hand-typed, per the standing
evidence-publication hygiene rule.

## 1. Campaign identity and boundary

- Package `issue115-stage2-v1`; STAGE-1 sealed PREREG sha256
  `2c7e3f21ebd8d574590fd4a23578f8ed29f74df258b2307f2ae55c430a299eb8`;
  MANIFEST.sha256
  `25700fd5bce2b07bbf5e89e9080bb0777acafea7a8282b081e7ac3c24972e860`;
  frozen baseline `fac48c2086b318b31a9c80fd823ef8c0ed956eed`; executor
  `claude-haiku-4-5-20251001` (0 tools, single turn, platform-default
  sampling); adjudicator claude-fable-5; VERIFICATION-ONLY mode (sealed:
  no probe result edits wording, opens a skill, or extends a taxonomy;
  marker mutation is outside the campaign).
- Durable evidence chain: PRs #163 (STAGE-2 publication,
  `7facc5381eb3ee4f0ef198ec80c05a68f935d4b6`), #164 (dry-run,
  `61967a9aa4de2d7b1701d9893d55f14324b9c001`), #165/#166 (smokes,
  `54b415c0d54edfc3da2796d72ff1f8c7c1a13191` /
  `ed1de2d25dad538603ced1e5eca05eb4064b3448`), #167+#168 (T1F1 + correction,
  `f416bffd038c6e2559f19642becfe8bab552f70f` /
  `aa41c13c4d231b1e8a298b585d7e51b4168c1ca1`), #169 (T2,
  `666b0c6f444cc18e718c137db00695011ebe95eb`), #170 (T3,
  `c76a8779024c8f7500e98aac715d2ccadd35e5e9`), #171 (T4,
  `e8d2182b45b0817184b8ae677ada21a23e1be566`), #172 (T5-placement,
  `d9fac9242189779862b994b9e46ab2237c6b7fb5`), #182 (T5-narrative,
  `a584bcc252d42d9a848fd737ae9ba3b947a9b5e1`), #183 (T6,
  `779fd1b2933b692937e8de90029f201fe44f4202`), #184 (T7,
  `ac38c3acc66310268a4db7095fc00a16abc1ff37`) — ALL MERGED.

## 2. Campaign accounting (re-derived from merged receipts)

- Executor invocations: 1 dry-run + 13 smokes + 78 scored = **92 / 110**.
- Planned pool: **0 remaining** (all 92 planned slots consumed exactly once;
  planned scored execution terminated at slot 78).
- Reserve: **18, untouched** (zero reserve events of any licensed type).
- Scored validity composition: **75 VALID-SCORED + 3 UNGRADABLE**
  (T5-narrative slot 46; T7 slots 63 and 65 — each an ambiguity-driven
  grading-time classification under the sealed rule, never an execution
  failure; all 78 raw invocations stand, none rerun, none invalidated).
- Retries: 0. Operational exceptions: 0 across all 92 invocations. Two
  operator-side pre-request false starts (T1 slot-2-era precedent; T5n
  slot-43 CLI-flag parse) produced zero requests and zero budget effect and
  are recorded factually in their units.
- Markers discharged: **0** (every adjudication carries
  `marker_discharged: false`; disposition is this phase's proposal and a
  later gate's action).

## 3. The 8-marker sealed-outcome matrix (transcribed from merged adjudications)

(Seven owner-fixed targets T1–T7 yield eight judgment-unit markers because
target T5 preregisters two separate discharge units — T5-placement {T5S1}
and T5-narrative {T5S2}; clarification per both gate reviewers'
RECORD-ONLY notes.)

| Marker | Fixture set | Sealed outcome | Arm counts (bare / ruled, COMPLIANT of 3) | UNGRADABLE | CLEAN |
|---|---|---|---|---|---|
| T1-suppression | {T1F1} | INCONCLUSIVE (middle pattern) | 0/3 · 2/3 | 0 | true |
| T2 | {T2S1,T2S2} | FAIL-SIGNAL | S1 0/3 · 3/3; S2 0/3 · 0/3 | 0 | true |
| T3 | {T3F1} | INCONCLUSIVE (middle pattern) | 0/3 · 2/3 | 0 | true |
| T4 | {T4S1,T4S2} | PASS+SUPPORT | S1 0/3 · 3/3; S2 3/3 · 3/3 | 0 | true |
| T5-placement | {T5S1} | FAIL-SIGNAL | 0/3 · 0/3 | 0 | true |
| T5-narrative | {T5S2} | INCONCLUSIVE (middle pattern) | 2/3 · 3/3 | 1 (slot 46, bare) | true |
| T6 | {T6S1,T6S2} | PASS+SATURATED | S1 3/3 · 3/3; S2 3/3 · 3/3 | 0 | true |
| T7 | {T7S1a,T7S1b,T7S2} | INCONCLUSIVE (¬CLEAN) | S1a 0/3 · 3/3; S1b 3/3 · 3/3; S2 2/3 · 3/3 | 2 (slots 63/65, S1a bare) | false |

Corrections on record (adjudication-layer only; runs never rerun): T1F1
PASS+SUPPORT → INCONCLUSIVE (owner item-A ruling, PR #168); T2 provisional
PASS+SUPPORT rejected pre-publication (owner ruling A); T5-narrative
PASS+SATURATED → INCONCLUSIVE (owner slot-46 UNGRADABLE ruling,
pre-publication); T7 slots 63/65 run-time VALID-SCORED → UNGRADABLE at the
sealed 18/18 adjudication (owner's pre-authorized grading-time rule).

## 4. Synthesis — three strictly separated categories

The sealed outcome classes carry NO shortcut semantics. Explicitly rejected
inferences: FAIL-SIGNAL does NOT mean "doctrine must change";
PASS+SATURATED does NOT mean "the clause is unnecessary"; INCONCLUSIVE does
NOT mean "the evidence failed" — each is a preregistered, legitimate,
bounded result at this executor tier on these frozen fixtures.

### 4a. Evidence about marker support

- **T4 (cross-model-review environment-bound severity)** is the campaign's
  only §D-recommended `probed in part` candidate: the discriminating fixture
  (T4S1) went ruled 3/3 vs bare 0/3 with the control (T4S2) saturated —
  the exact PASS+SUPPORT shape the preregistration defines. Scope of any
  upgrade: haiku tier, these two fixtures, n=3, this campaign.
- **T2, T5-placement (FAIL-SIGNAL)** are evidence that the injected clause
  did not produce the rubric-complete behavior on at least one frozen
  fixture (T2S2 ruled 0/3 on the settle-destination-first ordering; T5S1
  ruled 0/3 on owning-bullet identification while it did produce folding).
  This is marker-relevant evidence AGAINST an upgrade, and a
  doctrine-concern input (4b) — it does not itself license any doctrine
  change.
- **T1F1, T3, T5-narrative (INCONCLUSIVE, CLEAN middle patterns)** each
  carry a directional observation (ruled ≥ bare in every case; T1F1 0→2,
  T3 0→2, T5-narrative bare already 2/3 under a rubric-ambiguity
  UNGRADABLE) that is preregistered as INSUFFICIENT for any marker
  mutation. Recorded as distributions only.
- **T6 (PASS+SATURATED)** and the saturated constituents elsewhere (T4S2,
  T7S1b) record that the bare arm already satisfied those rubrics at this
  tier — bounded saturation evidence, not evidence the clause is
  unnecessary (the fixtures inline rich repo facts that plausibly carry
  the decisions).
- **T7 (INCONCLUSIVE ¬CLEAN)** produces NO in-domain support evidence by
  construction: the CLEAN precondition failed (two ambiguity-UNGRADABLE
  runs concentrated in the T7S1a bare arm). The observed T7S1a 0/3-vs-3/3
  contrast remains descriptive only and is not upgraded by this synthesis.

### 4b. Doctrine concerns (findings for owner review; no change licensed)

- **T2 concern (delegation-and-review cold-start ladder):** under clause
  injection, all three T2S2 ruled runs still performed a provider-status
  read before settling the payment destination — the doctrine's
  "settle the destination first" ordering did not transfer on this frozen
  fixture. Recorded per the sealed FAIL-SIGNAL action.
- **T5-placement concern (skill-authoring §4 placement):** the clause
  produced folding behavior (ruled always folds; bare adds standalone
  bullets in 2/3) but never correct owning-bullet identification — every
  fold targeted the non-owning "Timeouts are explicit" bullet. The concern
  is owning-bullet identification, bounded to this frozen fixture.

### 4c. Fixture / rubric / process lessons (no marker-evidence weight)

- **Rubric-ambiguity lesson (T5-narrative slot 46; T7 slots 63/65):** three
  scored runs landed in the gap between a PASS condition that was not
  established and FAIL predicates that never triggered; the sealed
  ambiguity rule (UNGRADABLE, never adjudicator discretion) resolved all
  three, twice via owner ruling / pre-authorized rule. Future fixture
  design should make PASS/FAIL predicates jointly exhaustive (e.g.
  R-T7S1a's "performed and seen green" vs "without any baseline
  verification step" gap). Strictly separated from marker evidence.
- **Saturation lesson (T5S2, T6, T7S1b):** fixtures that inline the full
  primary source or rich repo facts saturate at this tier and cannot
  discriminate; discrimination-capable fixtures at haiku tier need the
  rubric-relevant decision NOT to be carried by the inlined material.
- **Process lessons already mechanized this campaign:** review-before-land
  with staggered cross-family recomputation caught one true grading error
  pre-publication (T5-narrative) and confirmed seven units clean;
  the hand-typed-hash failure mode recurred four times before/despite
  mechanization and is now covered by the standing script-generated-hash +
  recompute-scan rule (extended to CLI arguments); `ant` CLI `--message`
  takes inline JSON only; optional-stopping and unit-boundary discipline
  held across all 92 invocations.

## 5. Proposed treatments (recommendations only — nothing executed here)

- Planned campaign execution: propose recording as **complete** (92/110;
  planned 0).
- Reserve 18: propose recording as **unused and no longer needed for this
  completed planned campaign** — to be spent ONLY if a later owner
  explicitly opens a new exception campaign; never to be consumed for
  budget-completion's sake. No reason to use reserve exists today: no
  SUSPECT marker, no parity void, no licensed rerun path is open (UNGRADABLE
  is never re-run by sealed rule).
- Marker dispositions: per PROPOSED-DISPOSITION-MATRIX.md — all candidates,
  each mapped to issue #115 section-A settlement paths, requiring a
  separate owner-gated disposition action.
- #115 closure: per CLOSURE-ASSESSMENT.md — **not closeable** on its own
  recorded conditions; the campaign advances section A for 8 markers only.
