# Issue #115 closure assessment (PROPOSED — recomputed against the issue's own recorded conditions)

Method: the issue body at assessment time (state OPEN) was re-read in full
and each section's recorded exit condition was checked against durable
evidence — not against the fact that "8/8 campaign outcomes exist".

**Bottom line (proposed): #115 is NOT closeable now.** The completed
verification-only campaign advances exactly one slice of section A; sections
B, C, D, and E have their own exits, none of which this campaign satisfies,
and section A is by its own text a standing queue.

## Section-by-section recomputation

### A. Probe debt — the global `unprobed` queue (standing queue)

- Recorded semantics: a marker settles by path 1 (probe + marker updated),
  path 2 (recorded demotion/decline), or path 3 (honest non-upgrade outcome
  recorded in the campaign ledger, marker stays `unprobed`); "this section
  as a whole is the standing queue and keeps the tracker open as long as
  any unsettled marker exists — new rules keep entering under the
  covenant; that is the queue working as designed."
- Campaign contribution: sealed evidence + ledger records now exist for
  **8 markers** (the seven-target slice at frozen baseline `fac48c20…`).
  After the later owner disposition gate acts on the proposal matrix, up to
  7 markers could settle via path 3 and 1 (T4) via path 1. None is settled
  yet — dispositions are not executed, markers discharged = 0.
- Scale check (the issue's own command, machine-run at merged main,
  informational): `grep -rn 'unprobed' skills/ --include='*.md'` returns
  **234 occurrences across 12 files** at `ac38c3a…` (occurrences include
  Provenance prose per the issue's own snapshot logic; the issue's last
  snapshot was 161/11 at 097a253, so the covenant has kept adding rules —
  the queue working as designed). The queue remains populated regardless
  of this campaign.
- Verdict: **not a closure condition that can complete** in the ordinary
  course (standing queue); and even its current slice awaits the
  disposition gate.

### B. Round-5 work-list — 10 rules from PRs #110/#111

- Recorded exit: each of the 10 rules has a recorded probe outcome or
  demotion/decline.
- Recomputation: this campaign's targets were the seven PR-batch markers
  (#151/#152/#153/#157/#159/#160/#161) — a DIFFERENT slice. None of
  section B's 10 shaped rules was probed by this campaign.
- Verdict: **exit not met; untouched by this campaign.**

### C. Doctrine backlog — 11 deferred candidates (from #112)

- Recorded exit: every item has a recorded disposition (ship / merge /
  decline) recorded in the issue.
- Recomputation: the issue body carries no recorded dispositions for the
  11 items; this campaign neither adjudicated nor shipped any of them
  (verification-only boundary).
- Verdict: **exit not met.**

### D. Environment limitation — nested headless `claude -p` abort (#113)

- Recorded exit: failure classified by the Phase-0b experiments, then
  either an upstream bug report or a documented nesting limitation in the
  review recipes.
- Recomputation: no Phase-0b classification record exists in the durable
  tree; this campaign ran its executor via the `ant` CLI and its reviewers
  via the codex CLI, neither of which performs the #113 experiments.
- Verdict: **exit not met.**

### E. Harness blocker — round-5 sandbox root (run4.sh:26)

- Recorded exit: the RELOCATION.md §3 fix contract satisfied, including a
  decided repo-internal-root policy with its expected test result recorded.
- Recomputation (machine-checked): the entire `evals/` directory is
  git-ignored and absent from the merged tree at `ac38c3a…` — the
  RELOCATION.md §3 record, run4.sh, and any fix state exist only on local
  disk / archive, not in durable repo bytes. The LOCAL run4.sh line 26 now
  reads an ABORT-if-unset guard requiring `--sandbox-root` /
  `R4_SANDBOX_ROOT` with no default — the surface shape of the §3 fix
  contract's core clause — but no durable record establishes the full exit
  (the test matrix over old/new/symlink/in-repo/out-of-repo roots and the
  decided repo-internal-root policy with its expected test result).
- Verdict: **exit not verifiable from durable bytes** (and therefore not
  recordable as met). The local disk suggests partial or complete fix work
  whose completion record, if it exists, lives outside this repo; owner
  confirmation against the local/archive state is required before treating
  section E as closed. Either way, this campaign contributed nothing to
  section E.

## Relationship of this campaign to #115 (scope honesty)

The sealed PREREG titles itself the "Issue-115 Evidence Cycle", but its
seven targets are one slice of section A's standing queue — not section B's
work-list, not section C's backlog, not the section D/E environment items.
Completing it (a) produces sealed evidence + a durable ledger for 8 markers,
(b) queues 1 path-1 and 7 path-3 settlement candidates for the disposition
gate, and (c) leaves every other section exactly where it was.

## Proposed closure treatment

- **Do not close #115.** Propose instead: after the owner disposition gate
  acts, record the 8-marker settlement outcomes in section A's terms (the
  campaign ledger is the authoritative path-3 record), and leave the
  tracker open per its standing-queue semantics with sections B–E as the
  live remainder.
- **Reserve 18:** propose recording as unused and not needed for this
  completed planned campaign; any future spend requires a new explicit
  owner exception-campaign grant. No current fact supports reserve use.
- **No budget-completion runs:** the 18 unspent reserve slots are not a
  target; 92/110 is the campaign's complete and final execution record.
