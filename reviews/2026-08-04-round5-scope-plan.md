# Round-5 probe campaign — SCOPE PLAN (planning only; not an authorization to run)

**Status:** scope-only. This PR ships two artifacts — this scope note and the
frozen target manifest `reviews/2026-08-04-round5-targets.json` — and nothing
else. It runs **no probes**, changes **no marker**, upgrades/demotes **no rule**,
writes **no ledger**, and touches **no skill or runtime**. Probes are owner-run on
the private successor suite (#115 §A); **executing round-5 requires a separate
owner authorization** after this PR merges.

Anchored to `main` @ **78e05a8** (the verification-time HEAD; the manifest pins the
same SHA).

## 0. Scope and non-goals

**In scope (this PR):** define round-5's fixed target set, freeze it as a manifest
with drift-resistant identity, and fix the probe protocol / reproducibility
contract / dual-axis verdict / stop conditions / finding-routing.

**Out of scope / excluded:** probe execution; marker changes; rule upgrade,
demotion, or edit; ledger writes; any skill or runtime change. Also excluded:
- **#117** — the three `ground-truth-gates` round-12 folds are already 3-family
  gate-confirmed (grok-high + luna-ultra + sol-max, closed 2026-08-04). Not a
  round-5 target; do not re-litigate.
- **#115 §C** — the 11 candidates from #112 were **shipped** as rules on 2026-08-01
  (commit `ab177d3`, "#115 Phase 1") and carry in-body `unprobed` markers, so they
  ARE live §A probe debt — but they sit **outside round-5's 10-rule slice** (round-5
  = only the #110/#111 batch). They are a later campaign's work, tracked in #115 §A.

## 1. #115 is the canonical backlog; ROUND-5 IS A FIXED 10-RULE SLICE

**The full #115 §A queue is NOT the round-5 target set.** The `unprobed` grep
surface at `78e05a8` is **177 occurrences across 11 files** (≈96 parenthetical
rule-labels plus non-parenthetical marker forms, minus Provenance prose; §2 tiers
these). Treating that whole surface as one campaign would make
round-5 an open-ended, terminus-free effort.

So round-5 is defined as a **fixed, finite slice**: the **10 rules** shipped by
**PR #110 (`security-architect` ×5)** and **PR #111 (review/handoff ×5)** on
2026-08-01, whose discriminating probe shapes are already designed in **#114**.
Every other real marker stays in **#115** for a later campaign and is **not** in
round-5's execution scope.

This bounds cost: 10 rules × {bare, ruled} × `n ≥ 3` ≈ **60 core runs**, plus
necessary retries and adjudication — not the hundreds-to-thousands a whole-queue
campaign would imply.

**#115 remains open and canonical.** Completing round-5 does not close it; new
markers keep entering under the covenant. Round-5 **evaluates** only the 10 frozen
targets, and settlement is governed by §5 — SUPPORT/DEMOTE remove a marker;
SATURATED / INCONCLUSIVE / ROUTE_TO_FIX leave it in place (recorded in the ledger).
"Evaluated" is not "cleared".

## 2. Frozen target manifest — `reviews/2026-08-04-round5-targets.json`

The 10 targets are frozen in the manifest, reconciled before freeze (all 10
verified `new_unprobed` against their Provenance entries — none duplicate,
historical, or path-3-ledger-settled).

**Identity (not line numbers).** Each target's identity is
`id` (stable campaign key) + `path` + `heading` (verbatim semantic anchor) +
`marker_text_hash` (sha256 of the normalized marker line(s)). `marker_line_numbers`
are **auxiliary**, valid only at the pinned SHA. The bare `` (`unprobed` — see
Provenance) `` fragment is byte-identical across 9 of 10 rules, so the hash is over
the **whole marker line**, not the fragment; all 10 hashes are verified unique.
Re-verify a target by relocating its `heading` in `path` and re-hashing its marker
line(s); a mismatch on either means the target drifted and must be re-frozen.

**Freeze rules (binding once execution is authorized):**
1. The target set is frozen **before** any probe runs.
2. **No target may be swapped** for an unfavorable or incomplete result after
   probing begins.
3. Duplicate / historical / path-3-settled candidates are excluded **before**
   freeze (done — all 10 are `new_unprobed`).
4. **No backfill** with other #115 markers without a **new owner-approved
   manifest**.

The manifest is one-campaign frozen evidence, **not** a new canonical ledger; #115
stays the standing source and the round-5 campaign ledger holds the outcomes.

## 3. Probe protocol (pack standard; owner-run, private suite)

- **Runner:** owner-run on the private successor suite — the round-5 counterpart of
  `evals/round4/PROBES.md`. This plan does not run it.
- **Arms:** **bare vs. ruled**, per skill-authoring §7 — environment-relative
  baseline, audience tier held constant, symmetric leakage controls,
  expected-before-actual recorded.
- **Budget + scoring (frozen before any run):** `n ≥ 3` **valid samples per arm**
  (bare and ruled each). A SUPPORT upgrade requires a **pre-registered** promotion
  threshold fixed before execution — the round-4 standard is a `0/n` vs `n/n`
  discrimination (bare fails the measured clause on all n, ruled passes it on all
  n); any weaker rule (e.g. a stated majority) is valid only if registered before
  runs, never chosen after seeing results. A single smoke (`n = 1`) is
  discovery-only, never a marker change (round-4 precedent).
- **Shapes:** each target's discriminating shape is #114's per-rule design (what a
  bare weak-tier arm should fail that a ruled arm catches).

## 4. Reproducibility contract (fixed before execution)

The campaign must record and hold, per target:
- **Executor identity:** an exact model **slug + effort** (a concrete, reproducible
  configuration — the "weak tier" is pinned here, **never chosen at runtime**), plus
  an acceptable **version-drift policy** (re-probe the slug at run time; a slug that
  no longer resolves invalidates that run, not the target).
- **Arm parity:** bare and ruled use **identical inputs**; the *only* difference is
  the rule injection. Same fixture, same task framing, same tier.
- **Isolation:** each run in a **fresh context** (no carry-over between arms or
  samples); the isolation mechanism is stated.
- **Order:** arm/sample order is **interleaved or randomized** and recorded, so
  order is not a confound.
- **Sample validity + invalid budget:** `n ≥ 3` **valid** samples per arm. INVALID
  samples (never scored, never counted toward `n`), per round-4's discard paths:
  transport/provider errors (rate-limit, aborted stream, 5xx, timeout),
  empty/garbled output (INVALID-infra), a contaminated context (CONTAMINATED), or a
  trap that failed to present the test (UNARMED). Each invalid slot is retried up to
  a **fixed cap** (default 3 retries per slot); if a target cannot collect `n` valid
  samples per arm within the cap — a persistent outage, or a fixture that will not
  arm — it is recorded **INCOMPLETE / NONE** and the loop ends. Invalid runs never
  loop without bound and never inflate or deflate `n`.
- **Join:** raw output + model receipt + adjudicated verdict are joined to the
  target by its **stable `id`** (not prompt text, not line number).
- **Adjudication:** a named adjudicator scores each sample against the
  expected-before-actual; **ambiguous** results are resolved by a recorded rule
  (e.g. escalate to a second lens or mark INCOMPLETE), never silently.
- **Fixture pre-registration:** before any run, each target's fixture + oracle are
  content-**hashed and frozen**, with its expected-before-actual and a two-sided
  arming proof recorded (the round-4 frozen-fixture standard). Every scored sample
  binds to that frozen fixture hash; a run against an unfrozen or changed fixture is
  invalid.
- **Fixture repair (gated on a mechanical defect, never on a score):** a repair is
  permitted **only** on independently-recorded evidence that the fixture is
  mechanically defective (the trap did not arm — UNARMED — or the oracle
  demonstrably tests the wrong property), **never** in response to an
  unfavorable-but-valid result. Record the defect evidence, the fixture content
  **hash before and after**, and a two-sided self-proof that the repaired fixture
  now arms (and can still go red). A fixture may be repaired **at most once**; the
  repair **re-runs the whole target** (all samples), so no target mixes pre- and
  post-repair samples; if the repaired fixture also fails to arm, the target is
  recorded INCOMPLETE. An unbacked repair is forbidden — it would be a target swap
  by the back door (§2 freeze rule 2).

## 5. Dual-axis outcome — execution status × rule disposition

Record **two orthogonal axes** so "PASS" is never misread as "the rule passed":

- `execution_status` ∈ { **PASS**, **FAIL**, **INCOMPLETE** } — the experiment's
  top-level outcome: **PASS** = concluded on valid samples, no defect surfaced;
  **FAIL** = concluded but a rule defect surfaced (the rule is harmful, or an
  adjudicated rule-text / runtime defect) → routed, never a marker upgrade;
  **INCOMPLETE** = could not conclude (unsound fixture, or `n` valid samples not
  collected).
- `rule_disposition` ∈ { **SUPPORT**, **UNCHANGED**, **ROUTE_TO_FIX**, **NONE** } for
  a probe outcome; **DEMOTE** is a governance decision (below), never an
  `execution_status`.

**Disposition classes** (the priority procedure below maps counts to one of these):
| Class | execution_status | rule_disposition | #115 §A path |
|---|---|---|---|
| Support | PASS | SUPPORT | path 1 — marker updated in place |
| Unchanged | PASS | UNCHANGED | path 3 — marker STAYS (SATURATED or INCONCLUSIVE; ledger records which + the counts) |
| Route-to-fix | FAIL | ROUTE_TO_FIX | §7 routing event, **not** a #115 settlement — settles only after the routed fix lands |
| Incomplete | INCOMPLETE | NONE | path 3 — marker STAYS (unsound fixture / `n` not collected) |
| Demote | — (off the execution axis) | DEMOTE | path 2 — owner governance, below |

**The scoring procedure is pre-registered before runs and must satisfy these
invariants** (this note fixes the contract; the exact per-count table is registered
at execution authorization, per §4):
- **Total + disjoint** — every (bare-pass, ruled-pass) pair maps to exactly one class
  by a strict first-match priority; no pair is unmapped or double-mapped.
- **Harm is never masked** — a rule that lowers the weak arm is caught before any
  saturated or inconclusive reading.
- **Saturation needs both arms** — SATURATED (fixture too easy) means **both** arms
  pass all `n`, not the bare arm alone.
- **Defects route, not settle** — a harmful result or an adjudicated
  rule-text/runtime defect is Route-to-fix, never a marker change.
- **Fixture-soundness is independent** — FLOOR / UNARMED is a fixture verdict (§4),
  not inferred from counts; a valid hard fixture where neither arm passes is
  INCONCLUSIVE (marker stays), not FLOOR.
- **Escalation before disposition** — a pre-registered larger-`n` (for a
  near-threshold band) runs first; the priority is applied **once** to the full
  sample; the result is terminal, never assigned then re-opened.

A **canonical priority order** meeting the invariants (first match wins):
1. **Unsound fixture** (independent FLOOR / UNARMED check fails) → Incomplete.
2. **Adjudicated defect** (rule text non-binding/misleading, or a runtime-gate defect)
   → Route-to-fix.
3. **Harmful** (`ruled_pass < bare_pass`) → Route-to-fix.
4. **Saturated** (`bare_pass == n` **and** `ruled_pass == n`) → Unchanged.
5. **Support** (the clean §3 threshold, e.g. `bare_pass == 0` and `ruled_pass == n`)
   → Support.
6. **Inconclusive** (every remaining pair) → Unchanged.
**Governance disposition (orthogonal).** A `DEMOTE` (#115 §A path 2) is an owner
decision, recorded on a separate governance line — never an `execution_status`. A
post-probe demotion records the probe's class **and** a separate DEMOTE note; a
pre-execution decline is governance-only (path 2, with a reason) and carries **no**
execution_status (the target never ran). The execution axis stays exactly
{PASS, FAIL, INCOMPLETE}; there is no `N/A` value on it. A DEMOTE that follows a
`FAIL + ROUTE_TO_FIX` is the owner **deliberately dropping** a harmful/defective
rule (a valid resolution) — the ROUTE_TO_FIX outcome and its reason **stay
recorded** in the ledger; the drop never silently erases the defect finding, and a
defect never self-settles into a marker removal without that explicit owner
decision.

## 6. Bounded loop + stop conditions

- **Per target:** the probe loop ends at any one recorded disposition from §5 — a
  scored SUPPORT (path 1), a SATURATED/UNCHANGED, an INCOMPLETE/NONE, a **FAIL +
  ROUTE_TO_FIX** (the loop ends here; the target resumes only after the fix PR
  lands, under a fresh authorization + re-freeze), or an owner DEMOTE (path 2). Do
  not re-run a target that already carries one of these.
- **Per round:** bounded by skill-authoring §7 and cross-model-review §4. If a
  lens's finding counts do **not** converge (the recorded 2026-07-23 / #117
  non-convergence precedent — each pass opening a new surface), **stop and record**,
  do not chase to zero.
- **Fixture:** repaired at most once; the post-repair re-run scores normally
  (SUPPORT / SATURATED / …), and only if the repaired fixture ALSO fails to arm is
  the target recorded INCOMPLETE (§4).
- **Campaign done** when each of the 10 targets carries exactly one recorded
  disposition from that same set. #115 is **not** closed by this.

## 7. Finding routing (three destinations, never collapsed)

- **Runtime-correctness defect** (a rule's executable gate/template is wrong) → the
  probe records `FAIL + ROUTE_TO_FIX` in the ledger (route = runtime); the **fix
  itself** is a scoped runtime PR to the owning skill, gated by the cross-model
  ladder — separate from the ledger, never a marker change. The target settles only
  after the fix lands.
- **Doc/wording defect** (text misleads, runtime is right) → the probe records
  `FAIL + ROUTE_TO_FIX` in the ledger (route = doc); the **fix itself** is a doc PR
  (like the #104 / #120 reconciliations), separate from the ledger. The target
  settles only after the fix lands.
- **Probe-debt-only** (rule is correct; only evidence is owed) → ledger outcome +
  marker update-or-stay per §5; no repo behavior change.

A probe that surfaces a runtime bug is a **routing event**, not a marker upgrade.

## 8. Preserved boundaries (unchanged, restated)

- #117 fully excluded; path-3 SATURATED/NULL not re-probed; runtime / doc /
  probe-debt kept separate; the queue is **not** chased to zero; this PR changes no
  `skills/` or runtime; execution needs a separate owner authorization; **#115 is
  not closed** by round-5 completion.

## 9. Execution gate

Complete at the scope level. **Executing round-5 requires a separate owner
authorization.** On that authorization the first step is to **re-verify the
manifest** at the then-current SHA (relocate each `heading`, re-hash each marker;
any drift → re-freeze), then run the 10 frozen targets under §3–§7. Until then: no
probes, no marker changes, no ledger.
