# Issue #115 — tracker closure-state record (owner-adjudicated, additions-only)

Durable statement of issue #115's tracker state after the closure-oriented
triage of 2026-08-16. Every section's exit was recomputed first-hand against
current main, the issue's own recorded conditions, and the full durable
evidence surface — merged repository bytes, merged pull requests, and the
issue's own comment track.

**Headline: Sections B, C, D and E are TERMINAL. Section A remains an
intentionally open standing queue. Issue #115 therefore stays OPEN by design.**

Baseline main: `dd052c46b27bdebb8378aa21adeab4902bc54bd6`.
Machine-derived values cited here are frozen in `RECEIPTS.json` and
re-derived-and-compared by `closure_checks.py`; no value in this record is
hand-transcribed.

## 0. What this record is, and is not

This record is an adjudication-layer addition. It:

- changes no marker, no doctrine, no skill text, and no historical evidence
  package — repository skills bytes are unchanged by this package;
- runs no behavioral probe and authorizes none (invocations this phase: 0);
- consumes no reserve and no campaign budget;
- does not edit, comment on, or close issue #115 itself.

It records tracker state that had already been reached but was never written
down in one durable, forward-facing place.

## 1. Relationship to the closure assessment in PR #185

`reviews/2026-08-13-issue115-campaign-synthesis/CLOSURE-ASSESSMENT.md` is
**not corrected, not contradicted, and not modified**. Its bytes are pinned
unchanged by this package's checks.

That document states its own evidence surface openly: it re-read the issue
body and recomputed each section against the contribution of the verification
campaign it was synthesising. Within that declared surface its verdicts are
accurate — the #115 verification campaign genuinely contributed nothing to
sections B, C, D or E.

Two durable surfaces lay outside that declaration:

1. the issue's own comment track, which carries the owner execution record of
   2026-08-01 (Phases 0a, 0b and 1);
2. the round-5 campaign of 2026-08-04 (PRs #140 and #141), which is durable in
   the repository tree but is a different campaign from the one being
   synthesised.

Both bear directly on sections B–E. Stated precisely, so this record neither
whitewashes nor overstates: that document's **observations are accurate** —
the issue body genuinely records no section-C dispositions, the campaign
genuinely probed none of section B's ten rules, and no Phase-0b record
genuinely exists in the tree. Its **verdicts are stated tracker-wide** while
the surface it declared was narrower than tracker-wide, so each verdict
generalises past what that surface could settle. The correct characterisation
is therefore **evidence-scope incomplete for tracker-wide closure
adjudication**. For tracker-state purposes the B–E conclusions in that document
are superseded by this record; as a synthesis of its own campaign, and as an
accurate reading of the surface it named, it stands.

## 2. Section A — standing queue, and routing hygiene

### 2.1 Section A as a tracker condition

Section A is not an exit condition. Its own recorded semantics make it a
standing queue that keeps the tracker open while any unsettled marker exists,
with new rules continuously entering under the pack covenant. Its status is
**STILL-OPEN (BY DESIGN)** and that is the queue working as specified, not an
outstanding remediation debt.

Measured surface at baseline main: 251 `unprobed` grep occurrences across 12
files, of which 129 are canonical in-body markers. The issue's own snapshot at
`097a253` recorded 161 occurrences across 11 files. The queue has grown, which
is the covenant operating as designed.

### 2.2 Marker taxonomy versus execution routing

These are two different namespaces and this record keeps them apart.

- **Marker taxonomy** (`unprobed`, `probed in part`, ...) describes a marker's
  probe-evidence state.
- **Execution routing** (`NEEDS-NEW-PROBE`, `RETAIN-CONCERN-ONLY`, obligation
  satisfied, ...) describes what execution a deferred concern still owes.

An `unprobed` marker does **not** by itself denote an outstanding execution
obligation. Section A's own closure semantics settle a marker by any of three
paths, and path 3 — an honest non-upgrade outcome recorded in the campaign
ledger — deliberately leaves the in-body marker as `unprobed`. The grep surface
therefore overcounts open debt by design, and the ledger is authoritative. No
count of `unprobed` occurrences may be translated into a count of owed probes.

### 2.3 Routing entry — T2: TERMINATED

The Section-A disposition record registers exactly two deferred doctrine
concerns. The first is T2.

Routing history: PR #187 recorded `RETAIN-CONCERN-ONLY`; PR #188 updated the
routing to `NEEDS-NEW-PROBE` with a specific question — whether the wording
transmits the strict-ordinal requirement that determination fixed.

That execution obligation has been discharged in full:

- PR #189 landed the preregistration package;
- PR #190 landed the executed prefix (harness qualification);
- PR #191 landed the scored 36-observation unit returning outcome **O2**,
  guidance-transmission gap supported (directional);
- PR #192 landed the amendment design derived from that outcome;
- PR #193 landed the canonical doctrine mutation, whose sentence is verified
  present in `skills/operational-rigor/references/external-systems.md` at
  baseline main.

**T2 routing state: TERMINATED. There is no outstanding T2 execution
obligation.** The probe the routing called for was designed, executed, scored,
and its result drove a landed doctrine amendment.

Explicitly not claimed: the T2 **marker** is not upgraded by this record. Its
Section-A settlement stays exactly as the disposition record set it — path 3,
in-body marker `unprobed`, bytes untouched. A post-settlement probe does not by
itself promote a marker, and this record promotes nothing.

### 2.4 Routing entry — T5-placement: terminal already

The second registered concern reached a terminal routing record on its own in
PR #204: `RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)`, with the discharge of the
prior `NEEDS-NEW-PROBE` obligation stated explicitly and the marker left
unchanged. No action is owed here; it is cited as the completed form that
section 2.3 brings T2 into line with.

## 3. Section B — TERMINAL

Recorded exit: each of the ten rules from PRs #110 and #111 has a recorded
probe outcome, a scored marker upgrade committed in place, or a recorded
demotion/decline.

Satisfied by the round-5 campaign. Identity join is machine-verified, not
asserted: `reviews/2026-08-04-round5-targets.json` declares source issues
110 and 111, work-list index #114, and target count 10; all ten target headings
relocate in current main under the manifest's own whitespace normalisation.

Settlement split, machine-recomputed at baseline main: **3 path-1 / 7 path-3.**

- **3 scored upgrades committed in place** (`probed in part`): subprocess
  environment minimisation, absence-is-not-resolution, and consumer-position
  verification — each PASS with SUPPORT at bare 0/3 versus ruled 3/3, landed by
  PR #141.
- **7 honest non-upgrade settlements** recorded in the durable campaign ledger
  landed by PR #140, markers correctly left `unprobed` as path 3 requires.

Section B status: **TERMINAL.**

## 4. Section C — TERMINAL

Recorded exit: every one of the eleven deferred candidates from #112 has a
recorded disposition — shipped, merged into an existing rule, or declined with
the reason recorded on the tracker.

All eleven were dispositioned **SHIP**; none was declined, so the
record-the-reason clause attached to the decline branch never engaged. They
landed as PR #116. All eleven are verified present in current main, each
carrying its own in-body `unprobed` marker, and five skill files carry the
explicit provenance lineage naming #112 and #115 Phase 1 — semantic absorption
evidenced by recorded lineage, not by keyword resemblance.

Interaction worth carrying forward: candidate 9's external-systems entry is the
same entry the T2 chain amended in PR #193. One surface, two records; it must
not be double-counted as two separate obligations.

Section C status: **TERMINAL.**

## 5. Section D — TERMINAL

Recorded exit: the nested headless CLI failure is classified by the Phase-0b
experiments, then either an upstream bug report (if it reproduces from a clean
terminal) or a documented nesting limitation in this repository's review
recipes (if nested-only).

The Phase-0b experiments were executed on 2026-08-01 under the incident's own
CLI version and exact invocation shape. The large-stdin baseline, the exact
previously-failing shape, and a three-way concurrent fan-out all completed.
All three registered hypotheses were individually falsified.

**Evidence-basis note, so the reader can weigh each section correctly.**
Sections B, C, E and the T2 routing chain were re-verified first-hand at this
record's baseline — by machine join against merged bytes, by authenticated
lookup of every cited pull request, and, for section E, by executing the
contract suite. Section D is the one section whose underlying experiments were
not re-executed here: it rests on the durable execution record carried by the
tracker's own comment track, plus the first-hand observation that no
contradicting record exists in the tree. Re-running those experiments would be
a new behavioral probe, which this record is not authorized to perform and
does not claim to have performed.

**Owner-adjudicated terminal classification:
`FAILURE-NOT-REPRODUCIBLE / ALL-REGISTERED-HYPOTHESES-FALSIFIED`.**

Both downstream landing branches are **NOT APPLICABLE** under that
classification. They share one premise — that a classifiable failure survives
the experiments and needs a landing — and the experiments falsified it. Filing
an upstream bug for a defect that does not reproduce, or documenting a nesting
limitation that does not exist, would each manufacture a durable record known
to be untrue. Recording the terminal classification itself is what satisfies
this exit; this is not a fourth remediation route added after the fact, it is
the case the two drafted branches did not cover.

This is **not** a stale premise. The original failure was a real observation
when it was recorded; the later experiments establish only that it is not
reproducible today and does not fall under any of the three registered
hypotheses. If the signature recurs, the three-experiment procedure re-runs
against the failing state.

Separately noted, and not load-bearing for the exit: the second branch names a
landing surface the repository does not have. `cross-model-review` ships no
reviewer recipes by design, so a nesting-limitation note had no home in the
pack even had the branch engaged.

Section D status: **TERMINAL.**

## 6. Section E — TERMINAL

Recorded exit: the RELOCATION.md section-3 fix contract is satisfied, including
a decided repo-internal-root policy with its expected test result recorded.

The original blocker was real: the harness hardcoded its sandbox root under a
fixed home-directory path, so any rerun re-littered that directory. It was
fixed, not superseded — the file and its architecture still exist.

Contract state, re-verified by execution on 2026-08-16 against the local
harness:

- the sandbox root resolves in exactly one place;
- an explicit flag and an environment variable are the only two sources, with
  no default — absent both, the runner aborts;
- the root is canonicalised before any containment judgement;
- the deny-roots repository entry is derived from the script location rather
  than hardcoded, and the sandbox path and cell specification both derive from
  the one resolved root;
- the repo-internal-root policy is decided: a root inside the repository is
  refused at launch, with the expected test result recorded and observed;
- the contract suite returns **11/11 PASS**;
- the pre-fix control returns **10 FAIL / 1 PASS**, so the suite is
  demonstrably able to fail rather than vacuously green.

Method note on that control: the pre-fix runner creates its artifact directory
before reaching the resolve-only hook the fixed runner exits at, so running it
against the live tree would write into the repository. It was therefore
executed against an isolated replica outside the repository, and the repository
tree was proven byte-unchanged after both runs. The landing gate re-runs only
the side-effect-free positive suite; it does not re-run this control, and says
so rather than implying it did.

**Evidence-durability limitation, stated plainly.** The entire `evals/`
directory is git-ignored by design. The harness, its backup, the contract suite
and the relocation note exist only as local, untracked artifacts and in the
offline archive. Their SHA-256 values are recorded in `RECEIPTS.json` under a
key that marks them explicitly as local and untracked. **They are not
repository bytes and this record does not present them as such.** Any future
reader without the local tree or the archive can verify section E's contract
only from this record and the issue's execution record, not from the tree.

Section E status: **TERMINAL.**

## 7. Tracker lifecycle statement

**Sections B–E are terminal. Section A remains an intentionally open standing
queue. Therefore #115 remains OPEN by design; its OPEN state must not be
interpreted as unfinished B–E remediation.**

Closing #115 would require re-architecting the tracker — relocating the
standing queue to a separate issue — which is a change to the tracker's design,
not a repair of its records. That is not done here, and the issue's own text
already anticipates this state: sections close as their exits land while
section A continues.

The tracker's related-debt list still names issues #104 and #105 as open. Both
are closed. This is stale metadata in the issue body carrying no obligation,
recorded here so it is not mistaken for live debt.

## 8. Namespace guards

Two identity hazards are recorded so future joins do not silently go wrong.

- **The label `T4` denotes two different markers.** Round-5's `T04` is the
  security-architect subprocess-environment-minimisation rule. The #115
  verification campaign's `T4` is the cross-model-review environment-bound
  severity clause. They belong to different campaigns, different skills and
  different evidence packages, and must never be joined on the bare label.
- **`unprobed` is a marker-taxonomy term, not an execution-routing term.** See
  section 2.2. A marker reading `unprobed` may be fully settled under path 3.

## 9. Provenance and verification

- Machine-derived receipts: `RECEIPTS.json` (pull-request merge states and
  merge commits, blob pins, per-target marker states, candidate anchors,
  marker-surface counts, and the local-untracked harness hashes).
- Landing gate: `closure_checks.py`, which re-derives every cited value and
  compares it against the frozen receipts, pins the historical artifacts
  byte-unchanged, and asserts the boundaries this record must not cross.
- Cross-model review trail: `_gate/`.
