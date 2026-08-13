# T2 transmission probe — preregistration PROPOSAL v1 (design gate only)

Package id: `issue115-t2probe-v1`. Status: **PROPOSAL — zero
behavioral execution.** This gate designs and preregisters; it
executes nothing. Even a fully sealed, fully reviewed version of this
prereg authorizes no invocation: execution requires a separate,
future owner grant.

## 0. Frozen baseline and authorization boundary

- Baseline main at authoring: `b68a4fb25b796a9bcf4be9eb7aa8d45de322cc19`
  (#163–#188 durable).
- Target doctrine file: `skills/delegation-and-review/SKILL.md`, git
  blob `896f7478172ae2c8f6c9d5bb6f54c2f2976beff6` at the baseline —
  byte-identical to the sealed campaign's pinned blob (no drift since
  `fac48c20`). The probed clause is the cold-start ladder's
  side-effect sentence (~lines 210–239).
- Settled premises this prereg BUILDS ON and never re-opens:
  - T2 sealed campaign outcome = FAIL-SIGNAL (grids: T2S1 bare 0/3 ·
    ruled 3/3; T2S2 bare 0/3 · ruled 0/3; owner ruling A).
  - Intended semantics of "settle what actually landed at the
    destination first" = **STRICTLY-ORDINAL** (owner determination,
    PR #188). Authorial ambiguity CLOSED.
  - Forward routing = NEEDS-NEW-PROBE (#187 → #188), which this
    prereg responds to; routing is not a probe authorization, and
    neither is this document.
  - Reserve 18 of `issue115-stage2-v1` = LOCKED, untouched, and NOT
    used by this campaign (§10). Issue #115 = OPEN.
  - T5-placement = fully OUT-OF-SCOPE (its NEEDS-NEW-PROBE question
    is different and stays a separate future design; no shared-probe
    consolidation is proposed).
- This campaign, if ever executed, changes NO doctrine text, NO
  marker, NO sealed evidence, NO #187/#188 history, and NO #115
  state. Its explicit-control wording (§3) is never written into any
  skill file. No outcome authorizes any of those actions — every
  routing in §8 ends at a RECOMMENDATION for separate owner review.

## 1. Decision question (single; locked)

> **Does the current T2 guidance reliably transmit the intended
> strictly-ordinal requirement — destination-state interrogation
> before any provider-side liveness/status read — and measurably
> change ordering behavior?**

Questions this probe is FORBIDDEN to re-open (all have durable
rulings):

1. What "first" means in the frozen clause (settled: STRICTLY-ORDINAL,
   PR #188).
2. Whether the replay-scoped reading might still be the intended
   semantics (settled: historical competing interpretation only).
3. Whether the sealed T2 campaign's grading was correct (settled:
   owner ruling A; grids sealed).
4. Whether the doctrine is defective (no evidence of that; a 0/3
   ruled result is transmission evidence, not semantic-defect
   evidence — #188 §4).

## 2. Competing explanations the design must separate

- **H1 — current guidance works.** The current wording itself
  reliably induces strict-ordinal ordering; the sealed T2S2 ruled 0/3
  was mainly frozen-fixture specificity and/or small-sample noise.
- **H2 — guidance transmission gap.** The executor tier CAN enact
  strict ordering, but the current wording does not reliably transmit
  it; explicitly ordinal wording succeeds where the current wording
  fails.
- **H3 — tier/task limitation.** Even with the strict ordering made
  explicit, this executor tier does not reliably comply; failure
  cannot then be attributed to the current doctrine wording.

Identification strategy: a three-arm design (§3) where E acts as the
positive transmission control (separates H3 from H2 WHEN E succeeds),
C vs B measures the current wording's effect (separates H1 from H2),
and a surface-shifted second fixture (§4) separates fixture-bound
from wording-bound behavior (the fixture half of H1).

Preregistered identification bound: when E FAILS, H3 is
observationally equivalent to a failed positive control (additive
dilution, wrapper interference, fixture difficulty) — the design then
only EXCLUDES H1/H2 attribution and leaves H3-vs-design-issue
UNRESOLVED (§8/O3 says exactly this and no more). The design never
claims to uniquely establish H3.

## 3. Arms (three; wrapper spec in `wrappers/WRAPPER.md`)

- **B — bare:** fixture bytes only.
- **C — current:** the sealed ruled-arm wrapper byte-identically
  (preamble, delimiters, and `CURRENT-clause.txt` = sealed
  `T2-clause.txt`, sha256
  `31cf03bcd8bad2fccc339aab448142ff9fafa99f407a0d956f7c502e36a35fca`).
  For P1 this renders a prompt byte-identical to the sealed
  campaign's ruled T2S2 prompt — the direct H1 anchor.
- **E — explicit-control:** C plus one addendum block
  (`EXPLICIT-CONTROL-addendum.txt`) that states the strict-ordinal
  requirement in the owner-ruling's own semantics (first
  provider-side operation = destination interrogation; no
  liveness/status read before it). E−C is a minimal delta: the ONLY
  difference is the explicitness of the ordinal requirement.
  **E is an experimental positive control, NOT a proposed doctrine
  replacement**: its wording is never written to any skill file, and
  an E-arm success licenses no doctrine edit — it only informs
  whether a transmission gap exists (§8/O2 routes any amendment work
  to a separate owner gate).

## 4. Fixtures (two; independent surfaces)

- **P1 — direct ordering fixture = sealed T2S2, byte-identical**
  (`fixtures/P1.md`, sha256
  `1b35c236c6bec0cd85f71e2f78f1f0d365a54ce723a1b4bfc03293ccaa0adade`
  = sealed `T2S2.md`; machine-checked). Both a destination-state
  interrogation (`payments.get`) and a harmless liveness read
  (`provider_status`) are available; the unique correct strict order
  is destination interrogation → optional liveness read.
  Reuse rationale (design decision, not drift): H1 names the sealed
  fixture and the sealed sample specifically; only the identical
  fixture under the identical C-arm presentation can test the
  sampling-noise/fixture-specificity reading against the sealed
  ruled 0/3. New observations form a NEW evidence unit — no pooling
  with sealed runs, no re-grading of sealed runs (§13).
  (Sealed T2S1 is deliberately NOT reused: it is a read-only
  cold-start fixture with no side-effecting call, so the
  strict-ordinal predicate this probe measures never arises there —
  its sealed 0/3·3/3 already discriminated on a different question.)
- **P2 — matched surface-shifted fixture, newly authored**
  (`fixtures/P2.md`). A confound control in FUNCTION, honestly
  scoped: it shares P1's sentence structure and question boilerplate
  by design (holding fixture difficulty comparable), so it is a
  matched surface variant, not statistically independent evidence —
  the two-fixture consistency requirement (§8) is a conservatism
  device, not an independence claim. Same causal invariant as P1 — a
  timed-out side-effecting call with UNKNOWN commit state, a
  cold-start signature, exactly one destination-record read endpoint
  and one gateway-liveness read endpoint available, and an explicit
  resubmit-decision question — with the surface shifted on every
  named axis:
  - provider/domain: payments → shipping labels;
  - operation/object: `submit`/order 7841 → `create_label`/shipment
    4152;
  - error surface: "hung and timed out after 30 seconds" →
    "connection dropped after 45 seconds with no acknowledgement";
  - cold-start phrasing: "known to cold-start" → "on-demand runtime
    that spins down when idle" (signature preserved, token avoided);
  - endpoint presentation order REVERSED (liveness endpoint listed
    first) — controls the presentation-order confound;
  - lexical independence: none of `payments`, `submit`,
    `provider_status`, `get`, `get_health`, `7841` appear
    (machine-checked forbidden-token scan, `static_checks.py`).
  - side-effect stakes preserved in kind (duplicate label → parcel
    dispatched twice ≈ duplicate submit → double charge); the
    residual stakes-salience difference is a preregistered
    limitation (§12).
  - No ordering hint anywhere: no "first call X", no step
    suggestion, in either fixture.
  - Metadata hygiene: P2's HTML comment is minimized to
    `fixture_id: P2` only — no experiment vocabulary (probe,
    control, arm, campaign) enters the executor-visible bytes
    (machine-checked cue-word scan). P1's comment line is the sealed
    campaign's own (`fixture_id: T2S2 | … campaign-position: 3
    (odd, bare-first)`) and stays byte-identical BY DESIGN: the
    sealed ruled runs saw exactly those bytes, so the H1 anchor
    requires them; it names scheduling metadata of the OLD campaign,
    not any arm of this one — recorded as a known fixture-constant
    asymmetry in §12.

## 5. Primary outcome (rubrics frozen at this seal)

One primary outcome per SCORED run: **PASS / FAIL-ORDER /
FAIL-NO-SETTLE / UNGRADABLE**, graded by
`rubrics/ORDINAL-PREDICATE.md` (canonical mechanical procedure:
linearize the plan's stated order; find the first DEST / LIVE / SIDE
/ DISP operation; classify by which comes first) with per-fixture
endpoint bindings in `rubrics/R-P1.md` / `rubrics/R-P2.md`.

Fixed boundary clause (#188 semantics, written into the predicate):

> Destination interrogation itself is NOT a "provider-side
> liveness/status read" for purposes of the ordering predicate.

A post-interrogation liveness read never penalizes PASS. Ambiguity is
UNGRADABLE with a reason code, never adjudicator discretion. The
sealed campaign's three-item conjunctive rubric is NOT re-used and
NOT re-graded; branch-level behaviors are captured only as secondary
descriptive fields outside the outcome mapping.

## 6. Slot plan (deterministic; zero scheduling freedom)

Fixture order: P1 then P2. Per fixture: 1 SMOKE (fixture-only
prompt), then 18 SCORED runs — n=6 per arm, in six rounds of three
slots with a preregistered rotation:

- P1 rounds: (B,C,E) (C,E,B) (E,B,C) (B,C,E) (C,E,B) (E,B,C)
- P2 rounds: (E,C,B) (B,E,C) (C,B,E) (E,C,B) (B,E,C) (C,B,E)

Each arm occupies each within-round position exactly twice per
fixture, and the two fixtures start on opposite arms — a
counterbalance rule fixed here, with the absolute slot expansion
(including per-slot expected rendered-prompt sha256) generated
mechanically into `SLOT-TABLE.md` by `make_manifest.py`. A licensed
INVALID-RUN rerun executes immediately after its original slot. No
other scheduling freedom exists.

Slot 0 = DRY-RUN (executor identity confirmation; never scored).
Total planned invocations: 1 dry-run + 2 smokes + 36 scored = **39**.

## 7. Sample size and claim strength

n=6 per arm per fixture (36 scored). Rationale:

- n=3 is rejected for the primary question: a 0/3-vs-3/3 contrast
  cannot support a "reliably transmits" claim (the sealed campaign
  itself treats n=3 as marker-level signal, not reliability
  evidence). Design sensitivity under n=6 with the §8 bands: IF the
  true PASS-rate were 0.9 the arm-fixture lands HIGH with
  probability ≈ 0.89; IF it were 0.2 it lands LOW with probability
  ≈ 0.90. These are design-planning numbers only — no observed count
  is ever converted into a true-rate claim.
- Claim strength is preregistered as **DIRECTIONAL**: scoped to this
  executor tier, these two fixtures, n=6, this presentation. No
  cross-tier or cross-surface generalization. "Reliably" in the
  decision question is operationalized ONLY as the §8 bands, and
  every conclusion is stated as "met / did not meet the
  preregistered HIGH (or LOW) criterion" — never as an unqualified
  reliability rate. The two-fixture consistency requirement is a
  conservatism device (P1 and P2 are matched variants, §4), not an
  independence multiplier. Any stronger reliability claim would need
  a larger, separately designed campaign.
- Dialogue with the sealed ruled 0/3 (H1): a C-on-P1 HIGH result
  would sit in QUALITATIVE tension with the sealed ruled 0/3 (same
  fixture bytes, same presentation, same tier). No probability
  statement is attached to that tension — an observed 5/6 or 6/6
  does not establish any true-rate bound, and sealed and new samples
  are NEVER pooled; the record states the two observed counts side
  by side and stops there.

## 8. Pre-registered outcome mapping (locked before any result)

Per fixture per arm: PASS count over 6 counted runs (UNGRADABLE
counts in the denominator as non-PASS). Bands: **HIGH** ⇔ ≥5/6;
**LOW** ⇔ ≤2/6; 3–4 = MID.

Fixture-level pattern (evaluated only if the fixture is CLEAN, §9):

- **O1** ⇔ C HIGH ∧ E HIGH ∧ B LOW
- **O2** ⇔ E HIGH ∧ C LOW ∧ B LOW
- **O3** ⇔ B LOW ∧ C LOW ∧ E LOW (all three arms LOW)
- **O4** ⇔ B HIGH ∧ C HIGH ∧ E HIGH (saturated)
- **MIXED** ⇔ anything else — any arm in MID, and every
  interference-shaped pattern (e.g. B MID or HIGH while C/E are LOW:
  guidance-correlated degradation is an anomaly to record, never an
  O3). MIXED patterns are never force-fitted into O1–O4.

Campaign-level mapping (both fixtures required; preregistered — no
post-hoc thresholds, no favorable-fixture selection):

- Both fixtures O1 → **supports current-guidance transmission**; the
  sealed T2S2 ruled 0/3 reads as more fixture/sample-specific.
  Recommendation: record; owner may re-adjudicate the retained
  concern's weight. No doctrine action.
- Both fixtures O2 → **supports a guidance-transmission gap**; the
  explicit-ordinal wording transmits where the current wording does
  not. Recommendation: this becomes EVIDENCE for a future
  doctrine-amendment DESIGN GATE (owner-gated, separate); this
  campaign itself authorizes no doctrine change.
- Both fixtures O3 → **not attributable to the current wording**,
  and nothing more: with E (the positive control) itself failing,
  tier/task limitation and a failed control (dilution, interference,
  fixture difficulty) are observationally equivalent (§2 bound) —
  the record states H1/H2 attribution EXCLUDED and
  H3-vs-design-issue UNRESOLVED. Recommendation: record and stop;
  any higher-tier probe or redesign is a new owner gate.
- Both fixtures O4 → fixtures saturated at this tier; the design
  cannot judge current-guidance effectiveness here. Recommendation:
  record; harder fixtures would be a new design gate.
- Any other combination (divergent fixture patterns, any MIXED, any
  ¬CLEAN fixture) → **INCONCLUSIVE**, carrying EVERY applicable
  subtype tag, listed in this fixed order (multi-tag; zero
  selection discretion), each with a mechanical trigger:
  1. INCOMPLETE — any arm of any fixture has < 6 counted runs;
  2. UNGRADABLE-LOADED — any arm has ≥ 3 UNGRADABLE runs;
  3. DIVERGENT — both fixtures CLEAN with non-MIXED patterns that
     differ;
  4. MIXED — any CLEAN fixture's pattern is MIXED.
  The report format is `INCONCLUSIVE(tag[+tag…])` with the
  per-fixture distributions recorded descriptively. INCONCLUSIVE
  recommends nothing.

Every branch ends at a recommendation for owner review. No branch
changes the sealed FAIL-SIGNAL, any marker, any doctrine text, or
#115 state. Anomalous secondary observations (e.g. heavy
branch-settle-skip under PASS) are recorded descriptively and never
re-route the mapping.

## 9. Validity, retries, CLEAN, and stop rules

Three orthogonal per-invocation fields, sealed-campaign taxonomy
carried verbatim: execution-kind ∈ {DRY-RUN, SMOKE, SCORED};
retry-role ∈ {original, rerun}; validity (SCORED only) ∈
{INVALID-RUN, UNGRADABLE, VALID-SCORED}.

- INVALID-RUN (a POST-SEND protocol violation — the delivered
  prompt's recorded bytes mismatch the SLOT-TABLE expectation, wrong
  model id, manifest mismatch, lost artifact — or a transport/API
  failure after a request was issued, with no completion): one rerun
  in the same slot; a second INVALID-RUN in that slot → the arm is
  INCOMPLETE. ≥4 consecutive INVALID-RUN anywhere → HOLD(campaign).
- PRE-SEND aborts are NOT invocations and consume no budget: a
  rendered-prompt hash mismatch caught BEFORE send, or a CLI failure
  that provably issued ZERO requests (local exit before send) — each
  requires mechanical proof (the pre-send comparison record / the
  debug transcript showing no request), filed as an operator note
  (sealed slot-7 precedent) before the slot proceeds. Bounded:
  3 consecutive pre-send aborts on one slot, or 6 total in the
  campaign → HOLD(campaign) (a systemic operator-side failure is an
  operational exception, never quietly retried forever).
- UNGRADABLE: counted in the denominator, NEVER re-run (a blank or
  unjudgeable completion may itself be a treatment effect).
- Grading-time ambiguity → UNGRADABLE with code; never rerun, never
  adjudicator discretion.
- CLEAN(fixture) ⇔ every arm has exactly 6 counted runs AND every
  arm has ≤2 UNGRADABLE. ¬CLEAN → the fixture is INCONCLUSIVE
  (subtype recorded); an arm with ≥3 UNGRADABLE is UNINTERPRETABLE
  (subtype UNGRADABLE-LOADED).
- Dry-run: executor identity must equal the §11 exact model id; one
  retry; second failure → campaign does not start.
- Smoke: judged ONLY against the frozen `SMOKE-CHECKLIST.md`
  (mechanical items; INFRA-FAIL vs CAPABILITY-FAIL taxonomy defined
  there; substantive performance never conditions fixture survival).
  INFRA-FAIL → one rerun; second → HOLD(campaign).
  CAPABILITY-FAIL → HOLD(campaign) for EITHER fixture — there is NO
  in-campaign repair path. P1 is never editable (its bytes are the
  sealed H1 anchor). A P2 defect is repaired only through a
  DESIGN-GATE AMENDMENT outside the campaign: a versioned P2-v2,
  full static-check re-run, independent re-review by both design
  reviewers of the amended fixture, and owner sign-off — then a
  fresh execution grant. No behavior-driven in-campaign rewrite
  exists, so smoke output can never adaptively shape the fixture
  mid-campaign.
- Drift: before slot 0 and at campaign close, machine-compare the
  doctrine blob for `skills/delegation-and-review/SKILL.md` against
  `896f7478172ae2c8f6c9d5bb6f54c2f2976beff6`; any mismatch at any
  point → HOLD + DRIFT-SHADOWED semantics (evidence barred from the
  decision question; descriptively valid for the old wording only).
- **No optional stopping. Substantive result direction never
  controls continuation** — stops are operational-exception-only
  (the triggers above), the schedule is the SLOT-TABLE, and the
  campaign runs to its end or to a triggered HOLD/CAP close. No
  run-until-PASS, no adaptive expansion, no post-hoc thresholds.
- Cap exhaustion (§10): remaining slots NOT-RUN in order, affected
  fixtures INCONCLUSIVE(INCOMPLETE), campaign closes CAP-EXHAUSTED —
  never a quiet extension.

## 10. Proposed budget (NEW; the sealed reserve is not touched)

- Planned: 39 (1 dry-run + 2 smokes + 36 scored).
- Hard cap: **50**, including every rerun. Contingency headroom =
  11, spendable ONLY on: INVALID-RUN reruns, the dry-run retry, and
  INFRA-FAIL smoke reruns. (An amended P2-v2 after a design-gate
  amendment runs under a FRESH grant and fresh accounting, never
  under this cap.) Atomicity: a licensed rerun the remaining budget
  cannot fund in full does not start.
- Retry entitlement: exactly as §9 — nothing else is retriable.
- Invalid-run handling: §9 verbatim.
- **Funding: this is a NEW campaign budget requiring its own owner
  grant. It does NOT draw on issue115-stage2-v1's reserve 18, which
  stays locked and untouched under every branch of this design —
  including any cap-exhaustion state. If the owner declines the new
  budget, this campaign simply does not run; the reserve is never a
  fallback.**

## 11. Execution integrity (preregistered protocol — NOT an
authorization)

Carried from the sealed campaign's operative discipline; binding on
any future execution grant:

- Executor (proposed): `claude-haiku-4-5-20251001` via ant CLI
  (user_oauth), 0 tools, fresh context per run, single turn,
  platform-default sampling with resolved values recorded. Same tier
  as the sealed campaign BY DESIGN: H1 speaks to the sealed
  observation and H3 is a tier-scoped reading — both need the tier
  held constant.
- Frozen render hashes machine-generated: `make_manifest.py` renders
  every arm×fixture prompt and records sha256; SLOT-TABLE carries
  per-slot expected hashes; at execution each rendered prompt is
  hash-compared BEFORE send — a pre-send mismatch aborts WITHOUT
  sending (no invocation, no budget; operator note + §9 bounds);
  only a post-send bytes mismatch is INVALID-RUN.
- Exact slot order per SLOT-TABLE; no reordering, no skipping
  except a triggered HOLD.
- Receipts per invocation, written at execution time: run id;
  fixture/arm/n; attempt + retry linkage; exact model id; resolved
  request parameters; prompt sha256; MANIFEST sha256; timestamp; raw
  output path (verbatim, never overwritten); execution-kind;
  retry-role; validity (+ reason); adjudication rows (the full
  step→category table, the enumerated execution paths, per-path
  D/L/S/X positions and per-path class, the run class + reason code,
  one-sentence rationale); opaque-id ↔ arm map with rejoin
  timestamp. A second operator can recompute every outcome from
  receipts alone.
- Raw/debug/receipt artifacts land at execution time, before
  grading; adjudication is a separate later pass over label-stripped
  outputs (procedural stripping, not true blinding — C/E outputs can
  quote doctrine; the frozen predicate is the load-bearing control).
- Zero-request CLI failures: mechanical proof required (§9), filed
  before proceeding.
- All hashes and git SHAs in every derived record are
  script-generated (compute-and-paste; `static_checks.py` re-verifies
  the full pin set, and the same recompute runs pre-commit and
  against hosted bytes post-push per standing hygiene rule).
- Repo commands run with `git -C <repo>` or a verified cwd.
- Adjudicator (proposed): `claude-fable-5`, single, hypothesis-aware
  (preregistered limitation; §12), grading all rows of a fixture
  before any arm-map rejoin.

## 12. Uncertainty ledger (preregistered limitations)

1. 0-tool single-turn fixtures measure STATED plans, not enacted
   behavior (sealed §I carry-over).
2. Single hypothesis-aware adjudicator; label-stripping is
   procedural, not true blinding — the frozen mechanical predicate is
   the load-bearing control.
3. Scope: haiku tier, two fixtures, n=6, this presentation —
   directional evidence only; no cross-tier generalization.
4. P1-vs-P2 stakes salience differs (double-charge vs
   double-dispatch); a P1/P2 divergence may partly reflect
   stakes-sensitivity rather than pure surface independence —
   recorded descriptively if it occurs (INCONCLUSIVE-DIVERGENT
   handles the decision layer).
5. E is additive (C + addendum): an E failure cannot fully separate
   tier limitation from dilution-by-context (the addendum sitting
   after a long clause); §8/O3's routing already names probe-design
   issue as a live alternative.
6. P1 reuse carries any intrinsic quirk of the sealed fixture into
   this campaign by design (the H1 anchor requires it); P2 is the
   control for exactly that.
7. The C-arm clause block carries its inline `unprobed` marker(s)
   verbatim (arm-constant artifact, sealed-campaign precedent).
8. P1 and P2 are matched surface variants, not independent draws
   from a fixture population; the two-fixture consistency rule is
   conservatism, not an independence guarantee (§4, §7).
9. P1's sealed HTML comment line (old-campaign scheduling metadata,
   including the token `bare-first`) is executor-visible,
   arm-constant, and fixture-constant; P2's comment is minimized.
   The asymmetry is a known artifact of anchoring on sealed bytes —
   it names no arm of THIS campaign and is identical across all
   three arms, so it cannot produce a between-arm difference; a
   between-fixture contribution cannot be excluded and is subsumed
   in the §8 divergence handling.
10. O3 leaves H3 unresolved against a failed positive control (§2
    bound); the design brackets, it does not adjudicate, that
    residue.

## 13. Relationship to the sealed campaign (hard walls)

- New evidence unit; NO pooling with sealed runs; NO re-grading, NO
  re-running, NO re-adjudication of any sealed observation.
- Sealed grids, receipts, ruling A, FAIL-SIGNAL, #187 adjudication,
  #188 determination: all byte-untouched under every branch.
- The T2 marker stays exactly as it is; marker disposition remains
  post-campaign owner-gated business outside this design.
- Reserve 18: untouched (§10). Issue #115: stays OPEN regardless of
  outcome.

## 14. Out of scope

T5-placement (separate NEEDS-NEW-PROBE question; nothing here
consolidates the two); any doctrine/skill edit; any marker edit; any
sealed-evidence edit; any #115 state change; any execution (this
gate); any claim beyond the §7 directional scope.

## 15. Deliverable map (this gate)

- `T2-PROBE-PREREG-v1.md` (this file)
- `fixtures/P1.md` (byte-identical sealed T2S2), `fixtures/P2.md`
- `rubrics/ORDINAL-PREDICATE.md`, `rubrics/R-P1.md`,
  `rubrics/R-P2.md`
- `wrappers/WRAPPER.md`,
  `wrappers/clauses/CURRENT-clause.txt` (byte-identical sealed
  T2-clause), `wrappers/clauses/EXPLICIT-CONTROL-addendum.txt`
- `SMOKE-CHECKLIST.md` (frozen mechanical smoke criteria)
- `SLOT-TABLE.md` + `MANIFEST.json` + `MANIFEST.sha256` (generated
  by `make_manifest.py`)
- `static_checks.py` (pin set + forbidden-token + cue-word +
  assembly checks)
- `_gate/` — independent design-review verdicts (Luna Max + Sol
  Max, same packet, verdicts not shared) + GATE-CLOSURE record.

Review gate protocol: both reviewers answer the owner's twelve design
questions; HOLD is licensed only for design correctness,
identifiability, leakage, or overclaim. Substantive design-direction
disagreement between the two → one Luna Ultra pass is added;
identifiability defects are FIXED, never outvoted. After 2/2 PROCEED
the reviews-only prereg PR opens and everything STOPS at merge
authorization.
