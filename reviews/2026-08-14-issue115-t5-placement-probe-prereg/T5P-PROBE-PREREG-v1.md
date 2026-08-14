# T5-placement ownership probe — preregistration PROPOSAL v1 (design gate only)

Package id: `issue115-t5pprobe-v1`. Status: **PROPOSAL — zero
behavioral execution.** This gate designs and preregisters; it
executes nothing. Even a fully sealed, fully reviewed version of this
prereg authorizes no invocation: execution requires a separate,
future owner grant.

## 0. Frozen baseline and authorization boundary

- Baseline main at authoring:
  `c2fc127d7d2d6263439094553e4a6aa1575eeaee` (#163–#197 durable).
- Target doctrine file: `skills/skill-authoring/SKILL.md`, git blob
  `caa2bcb5832fa5fe688763e97cdc1e6ff99317d4` at the baseline. The
  probed clause is §4's placement test (~lines 499–511).
- **Clause-level pin, not file-level.** The sealed campaign pinned
  this file at blob `e49c7d9f782d628758db59d5207d9185884e46fa`; the
  file has since changed elsewhere (PR #196, triage batch C), but the
  probed clause's bytes are IDENTICAL at both blobs and occur exactly
  once in each (machine-checked, `static_checks.py`). The load-bearing
  pin for this campaign is therefore the clause sha256
  `3bdeaec5543000b993dfe9ef925b844f37a1e2e961646e5a7c92e2fc1fd8cebc`;
  the file blob is recorded for provenance. Drift semantics are in §9.
- Settled premises this prereg BUILDS ON and never re-opens:
  - T5-placement sealed campaign outcome = **FAIL-SIGNAL** (T5S1:
    item-1 6/6 PASS; item-2 6/6 FAIL; bare 0/3 · ruled 0/3; CLEAN).
  - Section-A disposition = **path-3**; the T5-placement marker
    remains **unprobed** and undischarged.
  - Concern adjudication (PR #187) = **NEEDS-NEW-PROBE**, which this
    prereg responds to; routing is not a probe authorization, and
    neither is this document.
  - **FAIL-SIGNAL ≠ doctrine defect.** No doctrine defect has been
    established, and nothing here presumes one.
  - Reserve 18 of `issue115-stage2-v1` = LOCKED and NOT used (§10).
    Headroom 11 of `issue115-t2probe-v1` = CLOSED and NOT used (§10).
    Issue #115 = OPEN.
  - T2 (cold-start / safe-retry) is fully OUT-OF-SCOPE: its chain is
    closed (#188 → #189 → #190 → #191 → #192 → #193) and nothing here
    consolidates, reuses, or reopens any part of it.
- This campaign, if ever executed, changes NO doctrine text, NO
  marker, NO sealed evidence, and NO #115 state. Its
  ownership-criterion wording (§3) is never written into any skill
  file. No outcome authorizes any of those actions — every routing in
  §8 ends at a RECOMMENDATION for separate owner review.

## 1. Decision question (single; locked)

> **Is the sealed T5-placement failure — the ruled arm repeatedly
> folding a retry-loop wall-clock bound into `Timeouts are explicit`
> — primarily an executor/tier surface association, or is the current
> "fold into the host bullet that owns it" guidance itself
> insufficient to convey semantic ownership reliably?**

Questions this probe is FORBIDDEN to re-open (all settled; each has a
durable record):

1. Whether the sealed T5-placement campaign's grading was correct
   (settled; grids sealed, PR #186 path-3).
2. Whether `Retries are bounded and jittered` is the owning bullet
   for the T5S1 rule — this is the FROZEN RUBRIC's test target,
   carried verbatim into R-P1, and is not re-argued here.
3. Whether a doctrine defect has been demonstrated (it has not;
   NEEDS-NEW-PROBE is precisely the finding that current evidence
   cannot decide).
4. Whether the clause's wording should change now (no; any amendment
   is a separate, later, owner-gated design gate — §8 routes to it,
   never past it).

## 2. Competing explanations the design must separate

- **H1 — current guidance sufficient.** With lexical cues controlled,
  the current clause reliably steers placement to the true owning
  bullet; the sealed `ruled 0/3` was mainly fixture difficulty and/or
  small-sample noise.
- **H2 — guidance-disambiguation gap.** The executor CAN identify an
  owning bullet by governance, but the generic phrase "the host
  bullet that owns it" does not reliably transmit the ownership
  criterion; a more explicit — but non-answer-leaking — criterion
  succeeds where the current phrasing fails.
- **H3 — surface/tier association dominates.** Even given an explicit
  ownership criterion, the executor still attaches the new statement
  by surface association — shared vocabulary or a salient topical
  link — rather than by governed subject; the failure then cannot be
  attributed to the current doctrine wording.

"Surface association" is deliberately NOT defined as raw token
overlap. In the sealed fixture (P1) the OWNING bullet actually shares
MORE content tokens with the new rule than the competitor does
(machine-recomputed: owner 7, competitor 4), yet every sealed run
went to the competitor — so the pull there was a topical association
(wall-clock/elapsed time ↔ "timeout"), not token counting. P2's
lexical invariant (§4) sweeps a measure FAMILY and removes every
measured surface route to its owner, so a correct placement there
cannot have been produced by any of them; the residual that no scan of this kind can
exclude — synonym and conceptual proximity — is recorded in §12/12.

Identification strategy: a three-arm design (§3) in which E is the
positive control for OWNER IDENTIFICATION — reaching the pre-declared
owner (separating H3 from H2 WHEN E succeeds) — C vs B measures the
current clause's effect (separating H1 from H2), and a second fixture
(§4) whose owner is DOCUMENTED IN ITS OWN WORDS while every measured
surface cue points elsewhere tests whether the executor can reach a
pre-declared owner at all. Neither control establishes the MECHANISM
by which a correct placement was reached; what P2 excludes is the
measured surface routes, and every claim is held to that (§12/12).

Preregistered identification bounds (stated before any result):

- When E fails, H3 is observationally equivalent to a failed positive
  control (an addendum too weak, dilution behind a long clause,
  fixture difficulty). The design then EXCLUDES H1/H2 attribution and
  leaves H3-vs-design-weakness UNRESOLVED. It never claims to
  uniquely establish H3.
- "Surface association" here bundles vocabulary proximity and
  positional habit (§4, §12/5). Both are non-semantic cues and the
  design does not separate them; the decision question contrasts
  governance-based attachment with surface attachment as a class, so
  the bundle does not threaten the H2-vs-H3 discrimination — but a
  confirmed H3 reading may not be attributed to vocabulary alone.

## 3. Arms (three; wrapper spec in `wrappers/WRAPPER.md`)

- **B — bare:** fixture bytes only; no placement guidance.
- **C — current:** the sealed ruled-arm wrapper byte-identically
  (preamble, delimiters, and `CURRENT-clause.txt` = sealed
  `T5-placement-clause.txt`, sha256
  `3bdeaec5543000b993dfe9ef925b844f37a1e2e961646e5a7c92e2fc1fd8cebc`,
  which is also byte-identical to the live doctrine clause). For P1
  this renders a prompt byte-identical to the sealed campaign's ruled
  T5S1 prompt — the H1 anchor, machine-proven at seal: the rendered
  P1×C prompt sha256
  `d54597ec0b36f3e9d52d8564ee750ebc5507bd989f9f4b0e49ef48959de83663`
  equals the sealed manifest's recorded ruled-T5S1 rendered-prompt
  hash, and P1×B equals its recorded bare hash
  (`static_checks.py`, section 11b).
- **E — ownership-criterion control:** C plus one addendum block
  (`OWNERSHIP-CRITERION-addendum.txt`) stating a general
  subject-over-vocabulary criterion: fold into the bullet whose own
  governed subject the new statement further constrains; shared
  vocabulary is not ownership. E−C is a minimal delta: the ONLY
  difference is the explicitness of that criterion.
  **E is an experimental positive control, NOT a proposed doctrine
  amendment**: it is never written into any skill file, and an E-arm
  success licenses no doctrine edit — it only informs whether a
  transmission gap exists (§8 routes any amendment work to a separate
  owner gate).

**Anti-leakage constraints on E (all machine-checked):** the addendum
names no bullet, no section, no fixture, and no domain vocabulary
from either fixture; it contains none of the tokens that would point
at an answer (`retry`/`retries`, `timeout`, `attempt`, `wall-clock`,
`elapsed`, `flag`, `rollout`, `release`, `delete`/`deleted`,
`codebase`); and it is fixture-general — the identical bytes are
served for P1 and P2. A criterion that named the answer bullet would
destroy the arm's identification value; this constraint is what keeps
E a control rather than a hint.

## 4. Fixtures (two; deliberately asymmetric roles)

### P1 — the anchor: implicit owner under surface competition

`fixtures/P1.md` is the sealed T5S1, byte-identical (sha256
`9617591bc3fe0655ab9539d07212aed0b1e03de971009eed9769e343099fe13b`;
machine-checked against the sealed file). Candidate A = `Retries are
bounded and jittered` (the frozen owner); candidate B = `Timeouts are
explicit` (the surface-similar competitor); the new rule bounds the
whole retry loop's wall-clock time.

Reuse rationale (design decision, not drift): H1 names the sealed
fixture and the sealed sample specifically; only the identical fixture
under the identical C-arm presentation can test the
noise/fixture-specificity reading against the sealed `ruled 0/3`. New
observations form a NEW evidence unit — no pooling with sealed runs,
no re-grading of sealed runs (§13).

### P2 — the capability control: documented owner, surface pull elsewhere

`fixtures/P2.md` is newly authored. It holds P1's task structure
(same instruction paragraph, same "approved 4-line rule" framing,
same file shape: two §1 bullets, two bolded §2 bullets, one §3
bullet) and shifts every surface:

- domain: external service calls → feature-flag management;
- governed object: retry-loop timing → a flag's removal from the
  codebase;
- vocabulary: none of `retry`/`retries`, `timeout`, `attempt`,
  `wall-clock`, `elapsed`, `backoff`, `jitter`, `call site`,
  `endpoint`, `wrapper`, `bounded`, `cap`, `hang`, `service`,
  `sandbox`, `disposition` appears anywhere in P2 (machine-checked
  forbidden-token scan, `static_checks.py`).

and adds the property this probe most needs — the **documented-owner**
case the concern adjudication could not test:

- the owning bullet 2.1 `No flag outlives its purpose` declares its
  span in its own words ("A flag exists from the change that
  introduces it until the day no path in the source can still reach
  it"), so ownership is explicit rather than inferable;
- **the lexical invariant is machine-enforced on a MEASURE FAMILY,
  not asserted and not on one chosen metric:** `static_checks.py`
  recomputes, between the new rule and every bullet, (i) content-token
  TYPE overlap (stopword-filtered and plural-stemmed — the filter is
  named because it hides function words, which axis (iv) then
  catches), (ii) a frequency-weighted score (stemmed term-frequency
  dot product), (iii) shared word BIGRAMS, (iv) RAW word tokens
  (unfiltered, unstemmed), and (v) word-internal CHARACTER N-GRAMS at
  EVERY width from 3 to 8. It requires all of: content-token
  overlap(rule, OWNER) = exactly `{flag}` (the single type every
  bullet in the file carries) while both plausible competitors share
  strictly more (2.2: `{flag, rollout, figure}`; 3.1:
  `{flag, release, figure}`); the OWNER's TF score strictly BELOW
  both competitors' (owner 2, each competitor 4); ZERO bigrams shared
  between the rule and the OWNER; and — the class-closing property —
  NO OWNER-EXCLUSIVE feature on axis (iv) or at any width of axis
  (v): nothing may be shared by the rule and the OWNER while absent
  from every other bullet. The owner therefore offers no DIFFERENTIAL
  surface route anywhere in the measured family; the competitors do.
  Four successive drafts failed this invariant at the design gate —
  sharing the token `codebase` with its own owner; tying a competitor
  on frequency while uniquely sharing two word bigrams; leaking a
  subword route (`alive` ↔ `outlives`) with no shared token at all;
  and leaking `its`/`one` at width 3 plus a raw `its` the
  content-token filter had hidden. Each time the measure FAMILY was
  widened rather than the wording patched, until it became an
  exhaustive owner-exclusivity sweep;
- the rule's closing sentence ("Record the clearing release beside
  the figure") deliberately touches the competitor's object,
  mirroring P1's closing sentence ("Declare both … at the call
  site"), which touches both candidates;
- the rule body is three lines like P1's, under the same "4-line
  rule" framing sentence — P1's own framing/length mismatch is a
  sealed-bytes artifact, reproduced identically in P2 so it cannot
  become a between-fixture difference.

Consequently a PASS on P2 is evidence of a placement NOT reachable by
the measured surface routes — the owner offers none of them
differentially — and a FAILURE on P2 is, in the first instance,
only evidence that the executor did not reach a documented owner
under this presentation. Only the FAIL-WRONG-OWNER subtype directed
at a competitor speaks to surface attachment specifically;
FAIL-STANDALONE, FAIL-OMIT, and UNGRADABLE establish no mechanism at
all, and §8/R5 accordingly leaves the mechanism unresolved. Scoped
precisely: no scan of this kind can exclude synonym or conceptual
proximity (`deleted` ↔ `retired`), so P2 licenses "not reachable by
the measured surface routes", never "governance attachment proven"; §8's branch texts and §12/12 hold every claim to that
boundary.

**Owner position.** In BOTH fixtures the owner is the FIRST bullet of
§2. This is deliberate: the sealed runs folded into the SECOND §2
bullet, so placing P2's owner second would let a "pick the later
bullet" habit manufacture a PASS. The cost is that the design does
not separate vocabulary attraction from positional preference
(§12/5).

**Two axes vary between P1 and P2** — surface domain AND ownership
explicitness. The design cannot attribute a P1/P2 difference to one
axis alone; §8 handles this by giving the two fixtures explicitly
different ROLES rather than treating them as replicates (see §8's
preamble), and §12/4 records the residue.

**Metadata hygiene.** P2's HTML comment is minimized to
`fixture_id: P2` — no experiment vocabulary (probe, control, arm,
bare, ruled, campaign, placement, ownership) enters the
executor-visible bytes (machine-checked cue-word scan). P1's comment
is the sealed campaign's own and stays byte-identical BY DESIGN (the
H1 anchor requires it); it contains the token `placement`, an
arm-constant, fixture-constant artifact recorded in §12/6.

## 5. Primary outcome (rubrics frozen at this seal)

One primary outcome per SCORED run: **PASS-OWNER / FAIL-WRONG-OWNER /
FAIL-STANDALONE / FAIL-OMIT / UNGRADABLE**, graded by
`rubrics/OWNERSHIP-PREDICATE.md` (canonical mechanical procedure:
reconstruct the proposed file state → enumerate loci → match each
fold host to exactly one frozen inventory id → classify by fixed
precedence) with per-fixture inventories and owner declarations in
`rubrics/R-P1.md` / `rubrics/R-P2.md`.

Fixed rule, written into the predicate:

> The semantic owner of each fixture is FIXED IN THE PER-FIXTURE
> RUBRIC AT PREREG SEAL, before any run exists. The adjudicator never
> determines, revises, or re-argues ownership after seeing an output.

An output's own ownership argument is a descriptive field, never a
grading input. Ambiguity at any predicate step is UNGRADABLE with a
reason code, never adjudicator discretion. The sealed campaign's
two-item conjunctive rubric is NOT re-used and NOT re-graded; its
section item (which saturated 6/6) survives only as a descriptive
field.

Predicate/anchor compatibility, stated for reviewers and derived ONLY
from the sealed adjudication's own recorded per-run descriptions (no
sealed output is re-read, re-scored, or pooled): the sealed record
describes four runs as folding into the non-owning `Timeouts are
explicit` bullet and two as adding a new standalone bullet — classes
this predicate would call FAIL-WRONG-OWNER and FAIL-STANDALONE
respectively. All six are non-PASS under both formulations, so the
qualitative anchor comparison in §7 is meaningful; no sealed verdict
is changed by saying so.

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

- n=3 is rejected for the primary question: the sealed unit's
  0/3-vs-0/3 contrast is marker-level signal, not reliability
  evidence, and this probe's question ("does an explicit criterion
  change behavior?") needs a band that a single deviant run cannot
  flip. Design sensitivity under n=6 with the §8 bands: IF the true
  PASS-rate were 0.9 the arm-fixture lands HIGH with probability
  ≈ 0.886; IF it were 0.2 it lands LOW with probability ≈ 0.901
  (both recomputed by `static_checks.py`). These are design-planning
  numbers only — no observed count is ever converted into a true-rate
  claim.
- Claim strength is preregistered as **DIRECTIONAL**: scoped to this
  executor tier, these two fixtures, n=6, this presentation. No
  cross-tier and no cross-surface generalization; no reliability
  probability is ever stated. Every conclusion is phrased as "met /
  did not meet the preregistered HIGH (or LOW) criterion".
- Dialogue with the sealed `ruled 0/3` (H1): a C-on-P1 HIGH result
  would sit in QUALITATIVE tension with the sealed observation (same
  fixture bytes, same presentation, same tier). No probability
  statement is attached to that tension — sealed and new samples are
  NEVER pooled; the record states the two observed counts side by
  side and stops there.

## 8. Pre-registered outcome mapping (locked before any result)

Per fixture per arm: PASS-OWNER count over 6 counted runs (every
non-PASS class, UNGRADABLE included, counts in the denominator).
Bands: **HIGH** ⇔ ≥5/6; **LOW** ⇔ ≤2/6; 3–4 = **MID**.

Per-fixture pattern (computed only if that fixture is CLEAN, §9):

- **O1** ⇔ C HIGH ∧ E HIGH ∧ B LOW
- **O2** ⇔ E HIGH ∧ C LOW ∧ B LOW
- **O3** ⇔ B LOW ∧ C LOW ∧ E LOW
- **O4** ⇔ B HIGH ∧ C HIGH ∧ E HIGH (saturated)
- **MIXED** ⇔ anything else — any arm in MID, and every
  interference-shaped pattern (e.g. B HIGH while C/E are LOW:
  guidance-correlated degradation is an anomaly to record, never an
  O3). MIXED patterns are never force-fitted into O1–O4.

**Why the campaign mapping is role-asymmetric rather than a
both-fixtures-agree rule.** P1 and P2 are not replicates: P2 is built
to be the case where ownership is documented, so its arms may
legitimately saturate while P1's do not. Requiring both fixtures to
show the same pattern would make the H2 branch nearly unreachable by
construction and would convert the control's designed behavior into
an INCONCLUSIVE verdict. Instead P1 carries the primary attribution
(it is the anchor to the sealed observation) and P2 GATES it (a
positive-control check on whether OWNER IDENTIFICATION is achievable
at all at this tier, on a fixture whose owner offers no measured
surface route). Both fixtures' full distributions are always
reported; nothing is pooled, and no fixture's result is dropped.

Mechanical decision procedure (ordered; first match wins):

1. Either fixture ¬CLEAN → **INCONCLUSIVE** (+tags).
2. Any arm of any fixture with ≥3 runs classed FAIL-OMIT and
   `flag-outlet-used = yes` → **INCONCLUSIVE(FLAG-OUTLET-LOADED)**
   (+any other tags). Rationale fixed in advance: the clause licenses
   flagging for a reviewer, so an arm that mostly flags is not
   measuring ownership identification, and its LOW band must not be
   read as a transmission failure.
3. P2 pattern = MIXED → **INCONCLUSIVE(MIXED-P2)** (+tags).
4. P2 pattern = O3 (E(P2) LOW — the positive control fails on the
   documented-owner case, where the owner offers no differential
   route on any measured surface axis) → **R5 / CONTROL-FAILED**: no attribution to the current
   wording is licensed on either fixture; H3-vs-probe-weakness
   UNRESOLVED. Recommendation: record and stop; a redesigned control
   or a different tier is a NEW owner gate.
5. Otherwise P2 ∈ {O1, O2, O4} — the executor reaches P2's
   pre-declared owner, which under P2's five-axis lexical
   invariant (§4) is a placement NOT reachable by the measured
   surface routes; synonym/conceptual routes remain unexcluded
   (§12/12), so this is a capability FLOOR, never "governance
   proven" — and
   P1's pattern decides:
   - **P1 = O1 → R1 / CURRENT-GUIDANCE-SUFFICIENT ON THE ANCHOR**
     (H1-consistent). The claim is explicitly P1-scoped: the sealed
     `ruled 0/3` reads as more fixture/sample-specific than
     wording-bound ON THIS FIXTURE. If P2 is simultaneously O2 — the
     current wording failing where an explicit criterion succeeds on
     the documented-owner case — R1 carries that qualifier verbatim
     in the report and the two fixture results stand side by side; no
     "the guidance is sufficient" claim is made beyond P1.
     Recommendation: record; the owner may re-weigh the retained
     concern's standing. **No doctrine action.**
   - **P1 = O2 → R2 / GAP-SUPPORTED (DIRECTIONAL)** (H2-consistent):
     an explicit ownership criterion transmits where the current
     phrasing does not. Recommendation: this becomes EVIDENCE for a
     future doctrine-amendment DESIGN GATE (owner-gated, separate).
     **This campaign authorizes no doctrine change**, and E's wording
     is not the amendment.
   - **P1 = O3 → R3 / SURFACE-SPECIFIC** (the "P1 fails, P2 succeeds"
     pattern): the tier reaches a pre-declared owner that offers no
     measured surface route (P2), yet under P1's topical
     competition no
     arm — the explicit criterion included — reaches the owner. H1
     and H2 are excluded FOR P1; the residue between H3 and "this
     criterion wording was too weak for the competition case" stays
     UNRESOLVED (§2's bound), and the P2 leg is stated at its own
     boundary (not reachable by the measured surface routes;
     governance not proven). Recommendation: record; a narrower follow-up design is
     a separate owner gate.
   - **P1 = O4 → R4 / ANCHOR-SATURATED**: the anchor fixture no
     longer discriminates under this presentation, so the design
     cannot judge the clause here; the qualitative tension with the
     sealed `ruled 0/3` is recorded without pooling or probability.
     Recommendation: record; a harder or re-matched fixture is a new
     design gate.
   - **P1 = MIXED → INCONCLUSIVE(MIXED-P1)** (+tags).

INCONCLUSIVE tags, carried in this fixed order (multi-tag; zero
selection discretion), each with a mechanical trigger:

1. **INCOMPLETE** — any arm of any fixture has < 6 counted runs;
2. **UNGRADABLE-LOADED** — any arm has ≥3 UNGRADABLE runs;
3. **FLAG-OUTLET-LOADED** — any arm has ≥3 FAIL-OMIT runs with
   `flag-outlet-used = yes`;
4. **MIXED-P1** — P1 is CLEAN and its pattern is MIXED;
5. **MIXED-P2** — P2 is CLEAN and its pattern is MIXED.

Report format: `INCONCLUSIVE(tag[+tag…])`, with both fixtures'
per-arm distributions recorded descriptively. INCONCLUSIVE recommends
nothing.

Always reported, never branch-altering: P2's own pattern in full
(O4 — bare already succeeds — versus O1/O2 — guidance needed — is a
descriptive fact about the documented-owner case); every FAIL subtype
distribution (wrong-owner vs standalone vs omit); the WHICH-BULLET
histogram for FAIL-WRONG-OWNER; and all §5 descriptive fields.
Anomalous secondary observations never re-route the mapping.

Every branch ends at a recommendation for owner review. No branch
changes the sealed FAIL-SIGNAL, any marker, any doctrine text, or
#115 state.

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
  before the slot proceeds. Bounded: 3 consecutive pre-send aborts on
  one slot, or 6 total in the campaign → HOLD(campaign).
- UNGRADABLE: counted in the denominator, NEVER re-run (an
  unjudgeable completion may itself be a treatment effect).
- Grading-time ambiguity → UNGRADABLE with code; never rerun, never
  adjudicator discretion.
- CLEAN(fixture) ⇔ every arm has exactly 6 counted runs AND every arm
  has ≤2 UNGRADABLE. ¬CLEAN → the fixture is INCONCLUSIVE (subtype
  recorded); an arm with ≥3 UNGRADABLE is UNINTERPRETABLE (subtype
  UNGRADABLE-LOADED).
- Dry-run: executor identity must equal the §11 exact model id; one
  retry; second failure → campaign does not start.
- Smoke: judged ONLY against the frozen `SMOKE-CHECKLIST.md`
  (mechanical items; INFRA-FAIL vs CAPABILITY-FAIL taxonomy defined
  there; substantive performance never conditions fixture survival).
  INFRA-FAIL → one rerun; second → HOLD(campaign). CAPABILITY-FAIL →
  HOLD(campaign) for EITHER fixture — there is NO in-campaign repair
  path. P1 is never editable (its bytes are the sealed H1 anchor). A
  P2 defect is repaired only through a DESIGN-GATE AMENDMENT outside
  the campaign: a versioned P2-v2, full static-check re-run,
  independent re-review by both design reviewers of the amended
  fixture, and owner sign-off — then a fresh execution grant. No
  behavior-driven in-campaign rewrite exists, so smoke output can
  never adaptively shape a fixture mid-campaign.
- Drift: before slot 0 and at campaign close, machine-verify that the
  clause bytes (sha256
  `3bdeaec5543000b993dfe9ef925b844f37a1e2e961646e5a7c92e2fc1fd8cebc`)
  still occur exactly once in `skills/skill-authoring/SKILL.md`, and
  record the file's blob sha1 at both points. A CLAUSE mismatch at
  any point → HOLD + DRIFT-SHADOWED semantics (evidence barred from
  the decision question; descriptively valid for the old wording
  only). A file-blob change with the clause bytes intact is RECORDED,
  not a HOLD — the probed unit is the clause, and the file
  legitimately evolves elsewhere (§0).
- **No optional stopping. Substantive result direction never controls
  continuation** — stops are operational-exception-only (the triggers
  above), the schedule is the SLOT-TABLE, and the campaign runs to
  its end or to a triggered HOLD/CAP close. No run-until-PASS, no
  adaptive expansion, no post-hoc thresholds, no fixture repair in
  flight.
- Cap exhaustion (§10): remaining slots NOT-RUN in order, affected
  fixtures INCONCLUSIVE(INCOMPLETE), campaign closes CAP-EXHAUSTED —
  never a quiet extension.

## 10. Proposed budget (NEW; no prior pool is inherited)

- Planned: **39** (1 dry-run + 2 smokes + 36 scored).
- Hard cap: **50**, including every rerun. Contingency headroom = 11,
  spendable ONLY on: INVALID-RUN reruns, the dry-run retry, and
  INFRA-FAIL smoke reruns. (An amended P2-v2 after a design-gate
  amendment runs under a FRESH grant and fresh accounting, never
  under this cap.) Atomicity: a licensed rerun the remaining budget
  cannot fund in full does not start.
- Retry entitlement: exactly as §9 — nothing else is retriable.
- **Funding: this is a NEW campaign budget requiring its own owner
  grant. It does NOT draw on `issue115-stage2-v1`'s reserve 18, and
  it does NOT draw on `issue115-t2probe-v1`'s unused headroom 11.
  Both stay locked and untouched under every branch of this design —
  including any cap-exhaustion state. If the owner declines the new
  budget, this campaign simply does not run; neither prior pool is
  ever a fallback.**

## 11. Execution integrity (preregistered protocol — NOT an authorization)

Carried from the sealed campaign's and the T2 probe's operative
discipline; binding on any future execution grant:

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
  sending (no invocation, no budget; operator note + §9 bounds); only
  a post-send bytes mismatch is INVALID-RUN.
- Wire verification is DECODE-then-compare on the delivered-prompt
  record, never a comparison of escaped transport text.
- Exact slot order per SLOT-TABLE; no reordering, no skipping except
  a triggered HOLD.
- Receipts per invocation, written at execution time: run id;
  fixture/arm/n; attempt + retry linkage; exact model id; resolved
  request parameters; prompt sha256; MANIFEST sha256; timestamp; raw
  output path (verbatim, never overwritten); execution-kind;
  retry-role; validity (+ reason); adjudication rows (the locus list
  with host ids, the class + reason code, every §5 descriptive field,
  one-sentence rationale); opaque-id ↔ arm map with rejoin timestamp.
  A second operator can recompute every outcome from receipts alone.
- Raw/debug/receipt artifacts land at execution time, BEFORE grading;
  adjudication is a separate later pass over label-stripped outputs
  (procedural stripping, not true blinding — C/E outputs can quote
  the injected clause; the frozen predicate is the load-bearing
  control).
- Zero-request CLI failures: mechanical proof required (§9), filed
  before proceeding.
- All hashes and git ids in every derived record are script-generated
  (compute-and-paste; `static_checks.py` re-verifies the full pin set,
  and the same recompute runs pre-commit and against hosted bytes
  post-push per the standing hygiene rule). No numeral in any derived
  record is hand-typed.
- Repo commands run with `git -C <repo>` or a verified cwd.
- Adjudicator (proposed): `claude-fable-5`, single, hypothesis-aware
  (preregistered limitation; §12/2), grading all rows of a fixture
  before any arm-map rejoin.

## 12. Uncertainty ledger (preregistered limitations)

1. 0-tool single-turn fixtures measure STATED placement decisions,
   not enacted edits (sealed §I carry-over).
2. Single hypothesis-aware adjudicator; label-stripping is
   procedural, not true blinding — the frozen mechanical predicate
   and the pre-declared owners are the load-bearing controls.
3. Scope: haiku tier, two fixtures, n=6, this presentation —
   DIRECTIONAL evidence only; no cross-tier generalization.
4. P1→P2 varies TWO axes jointly (surface domain and ownership
   explicitness). A P1/P2 difference cannot be attributed to one
   axis; §8's role-asymmetric mapping is the mitigation, not a
   solution, and a matched implicit-owner surface-shifted fixture
   would be needed to separate them (a larger design, deliberately
   not proposed here).
5. Vocabulary attraction and positional habit are not separated:
   both fixtures place the owner first, which prevents a
   later-bullet habit from manufacturing a P2 PASS but leaves the two
   surface cues bundled (§2's bound, R-P2's note).
6. P1's sealed HTML comment (old-campaign metadata, including the
   token `placement`) is executor-visible, arm-constant, and
   fixture-constant; P2's comment is minimized. The asymmetry is a
   known artifact of anchoring on sealed bytes — identical across all
   three arms, so it cannot produce a between-arm difference; a
   between-fixture contribution cannot be excluded and is subsumed in
   §8's role-asymmetric handling.
7. E is additive (C + addendum) and is a BUNDLE: an explicit
   ownership criterion PLUS the salience of "more than one bullet
   could host this". An E success therefore shows that THIS addendum
   works, not that the criterion alone does; an E failure cannot
   fully separate tier limitation from dilution behind a long clause
   (§8/R5 names probe weakness as a live alternative).
8. The C-arm clause block carries its inline `unprobed` marker
   verbatim (arm-constant artifact, sealed-campaign precedent).
9. P1 reuse carries any intrinsic quirk of the sealed fixture into
   this campaign by design (the H1 anchor requires it); P2 is the
   control for exactly that.
10. The predicate's nested-sub-item ruling (FOLD-INTO, not
    STANDALONE) is a design choice made at seal; it can move a run
    between FAIL subtypes and, in the nested-under-owner case,
    between PASS and FAIL. It is fixed in advance, applied
    mechanically, and recorded per run as `fold-form` so the
    alternative reading is recoverable from the record.
11. The FLAG-OUTLET-LOADED tag (§8/2) treats heavy use of the
    doctrine-licensed flagging outlet as uninterpretable rather than
    as failure. This is conservative by choice: it can convert an
    otherwise clean result into INCONCLUSIVE.
12. P2's lexical invariant is enforced on a MEASURED family (content
    token types, frequency, word bigrams, raw tokens, and character
    n-grams at every width 3–8, the last two under an exhaustive
    owner-exclusivity sweep). No scan of this kind can exclude
    synonym or conceptual proximity between the new rule and its
    owner (`deleted` ↔ `retired`; the idea of code ↔ `source`), nor
    position, nor a mechanism no listed axis measures, so a P2 PASS
    licenses "not reachable by the measured surface routes" and
    never "governance-based attachment proven". Symmetrically, a P2 FAILURE
    licenses only "did not reach the documented owner": of the FAIL
    subtypes, only FAIL-WRONG-OWNER directed at a competitor speaks
    to surface attachment; FAIL-STANDALONE, FAIL-OMIT, and UNGRADABLE
    establish no mechanism. Every §8 branch text is written to those
    boundaries. Separating conceptual proximity from governance would
    need a further fixture family; it is deliberately not proposed
    here. (This limitation supersedes four earlier drafts caught at
    the design gate — one whose rule shared the token `codebase` with
    its own owner; one whose owner tied a competitor on the frequency
    measure and uniquely shared two word bigrams with the rule; one
    whose owner shared the subword `live` with the rule through
    `alive`/`outlives` while sharing no token at all; and one leaking
    `its`/`one` at n=3 plus a raw `its` hidden by the content-token
    filter. All four are now barred by `static_checks.py`, and the
    last of them is why the sweep is exhaustive over the family
    rather than fixed at one width.)

## 13. Relationship to the sealed campaign (hard walls)

- New evidence unit; NO pooling with sealed runs; NO re-grading, NO
  re-running, NO re-adjudication of any sealed observation. §5's
  predicate-compatibility note is derived from the sealed record's own
  descriptions and changes no sealed verdict.
- Sealed grids, receipts, the FAIL-SIGNAL outcome, the #186 path-3
  disposition, and the #187 NEEDS-NEW-PROBE adjudication: all
  byte-untouched under every branch.
- The T5-placement marker stays exactly as it is; marker disposition
  remains post-campaign owner-gated business outside this design.
- Reserve 18 and T2 headroom 11: untouched (§10). Issue #115: stays
  OPEN regardless of outcome.

## 14. Out of scope

T2 and its closed chain; any doctrine/skill edit; any marker edit;
any sealed-evidence edit; any #115 state change; any execution (this
gate); the scratchpad-only contributor-triage residuals; any claim
beyond §7's directional scope.

## 15. Deliverable map (this gate)

- `T5P-PROBE-PREREG-v1.md` (this file)
- `fixtures/P1.md` (byte-identical sealed T5S1), `fixtures/P2.md`
- `rubrics/OWNERSHIP-PREDICATE.md`, `rubrics/R-P1.md`,
  `rubrics/R-P2.md`
- `wrappers/WRAPPER.md`,
  `wrappers/clauses/CURRENT-clause.txt` (byte-identical sealed
  T5-placement-clause), `wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt`
- `SMOKE-CHECKLIST.md` (frozen mechanical smoke criteria)
- `SLOT-TABLE.md` + `MANIFEST.json` + `MANIFEST.sha256` (generated by
  `make_manifest.py`)
- `static_checks.py` (pin set + forbidden-token + cue-word + leakage +
  assembly + design-sensitivity checks)
- `_gate/` — independent design-review verdicts (Luna Max + Sol Max,
  same packet, verdicts not shared) + GATE-CLOSURE record.

**Review gate protocol.** Both reviewers independently answer the
same twelve questions:

1. Does the design genuinely separate a lexical/tier effect from a
   guidance gap?
2. Is P2 something other than a lexical clone of P1?
3. Is E free of answer leakage?
4. Is the semantic owner predeclared and immune to post-hoc
   adjudication?
5. Is the C arm byte-exact current doctrine?
6. Is the outcome mapping closed before execution?
7. Is fixture divergence preserved rather than pooled?
8. Do the sample size and the DIRECTIONAL claim match?
9. Are saturation, failed-control, and surface-specific patterns all
   classifiable?
10. Are the retry / UNGRADABLE / stop / budget rules complete?
11. Is this campaign fully isolated from the T2 probe and every
    existing reserve?
12. Is this still only a probe — no smuggled doctrine amendment?

HOLD is licensed ONLY for identifiability, correctness, leakage, or
overclaim. Substantive design-direction disagreement between the two
→ one Luna Ultra pass is added; identifiability defects are FIXED,
never outvoted. After 2/2 PROCEED the reviews-only prereg PR opens
and everything STOPS at merge authorization — no execution, no
doctrine mutation, no marker mutation, no #115 closure, no use of any
existing headroom or reserve.
