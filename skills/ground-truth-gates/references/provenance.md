# ground-truth-gates · references: provenance

Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): the skill's historical review, probe, and amendment records. Canonical rules and inline debt markers remain in `SKILL.md`; any operative re-verification caution stays inline there too. This file is history only.


Distilled 2026-07 from: private checks/-harness design notes (the
prose-vs-ground-truth finding, plus — same author's 2026-07 harness export —
cost-asymmetric scoring, shape-preserving anonymization, hard negatives, the
experiment-grader rule), fable-agent-orchestration `935e4a3`
(task-relative-test-gate, fail-under-broken, two truth sources).
The project-gate SCA example (2026-07-12) mirrors security-architect's
SCA-in-CI line (same 12-source audit; ideas only, no code).
The 2026-07-13 additions (the parity replay-variant; the extended gate-real rules —
mock≠sign-off, error-path three-part assertion, base-ref execution,
correlated-model-bias, compiled-but-not-run, environmental-FAIL quarantine,
version-the-classifier, regenerate-and-diff; the "designing the guard itself"
section) distill a cross-repo mining pass over seven independent
retiring-architect `skills-staging/` libraries (class-distilled convergence — a
rule's weight is how many of the seven independently rediscovered it).
The 2026-07-13 case-set integrity rules (instrument validation + taint,
row capture-provenance, distribution-disjoint holdout), the two-sided
suite-soundness and fire-path clauses, the saturation/blind-grading and
outcome→action pre-registration lines, the first-freeze eyeball, the
grep-count ratchet, and three of the added fake-pass shapes (warm-state,
never-executed CI config, snapshot re-freeze) are mined from five
further private retiring-architect libraries (an engine-parity port, a market
dashboard, a learning-lab experiment harness, a Telegram bot, a link-shortener);
each is backed by a cited incident or experiment in its source library (private
repos — verifiable by the contributor, not linkable here).
A 2026-07-16 two-family post-merge review (grok-4.5 + gpt-5.6-sol;
trail in `reviews/2026-07-16-post-merge-validation-pr25-29.md`) scoped
experiment calibration to the shared case set and confined synthesized
fire-path inputs to a labeled test set, never the captured corpus.
The rule-2 behavioral trap-armed clause (2026-07-16) adapts a published
negative from Sahir619/fable-method's eval log — safe outcomes produced by
runs that never read the prescribing doc, blindness scored as discipline
until a transcript check was added (MIT; ideas only, no files copied; see
README acknowledgements).
The rule-3 zero-input-scanner shape (2026-07-18) comes from a private
incident: a worker-written guard's `**` pattern expanded empty under an old
shell dialect with nullglob, and the guard "passed" while scanning zero
files, including the one its outage check existed for. Private evidence,
cited as shape per the README covenant's second branch; no in-repo probe
has run, so the shape carries an in-body `unprobed` marker.
The rule-2 reuse-time re-validation clause (2026-07-23) comes from a
contributor incident: before a new batch, a grader re-validation fed a
directory to a grader that takes a file path; the harness threw a
module-load error for every case before any candidate code ran, the
known-bad reference scored 2/6 against a recorded 0/6, and the two
spurious passes were exactly the two capacity-edge cases whose
accepted-throw branch absorbed the harness's own load failure
(contributor-reported; the private harness is verifiable by the
contributor, not linkable here). Ships `unprobed` per the README
covenant's second branch; the executable probe — seed an
invocation-shape mismatch against a two-sided-proven grader and observe
whether reuse-time re-validation catches it before scoring — has not
run; the in-body marker records that debt.
Rule 2's decision-vs-bug clause (2026-07-24) adapts obra/superpowers
v6.2.0's writing-good-tests rebuild (MIT, ideas only; see README
acknowledgements): the string-presence trap ("the source is the source")
and the change-detector trap — failure shapes the two-sided protocol alone
cannot screen, since a source-echo test genuinely fails the old arm and
passes the new one. Ships `unprobed` per the covenant; its probe joins the
private round-5 queue.
Numbered items 6 (deterministic block-on-fail + independent recompute) and 7
(external-anchor over mutual agreement) under "What makes a gate real"
(2026-07-24) come from a starred-repo mining pass (ideas only; see README
acknowledgements). Item 6 is a four-source convergence —
s0912758806p/agentic-sop-to-work (hard gates hermetic and LLM-free, self-eval
advisory-and-capped), cloudflare/security-audit-skill and
vercel-labs/agent-skills (a mechanical structural check kept separate from model
judgment), and DietrichGebert/ponytail (self-verified good/bad instruments) —
its independent-recompute clause adapting agentic-sop's `recompute_gate` and
per-value trace gate (all MIT — vercel's MIT is declared in its README with no
LICENSE file; ideas only, no text). Item 7 adapts ponytail's `check-versions.js`,
whose comment records the real incident (every manifest shipped stale at one
version together while a mutual-consistency test passed — its #260/#262),
generalized from version manifests to any mutual-agreement check. The guard
opt-in rule under "Designing the guard itself" (2026-07-24) adapts
s0912758806p/agentic-sop-to-work's globally-installed hook that silent-no-ops
unless the project opted in (MIT, ideas only), corroborated by
NYCU-Chung/my-claude-devteam's bypassPermissions-hook framing (MIT) — it
matches this pack's own no-auto-registered-hooks invariant. All three ship
`unprobed` per the covenant; their probes join the private round-5 queue.
Rule 8 (fact-anchoring; 2026-07-24) is class-distilled from a mining pass
over the owner's own sessions (no code taken): hardcoded public-holiday dates
were cross-checked against four independent sources, but a cross-model
reviewer noted the suite validated structure only — "tests check shape, not
date-truth" — so the truth evidence lived in the conversation, not the gate;
the fix added anchor-date assertions as a regression guard against a future
bad edit. Ships `unprobed` per the covenant; its probe joins the private
round-5 queue.
The item-3 substring-grader-token-collision shape (2026-07-28) comes from one
downstream consumer's A/B probe (contributor-reported, not linkable): the
grader for a "did the arm record the
change?" axis scanned each arm's output file for the word `drift`, which the
fixture's own body text already contained ("a batch that drifts model
mid-run"). Every arm passed, including three that recorded nothing — the run
read as a 4/4 null result and would have retired a rule that did in fact
discriminate 0/3 vs 1/1 once regraded on a port-note heading. Ships
`unprobed` per the covenant.
The pre-registration-ordering clause (2026-07-28) comes from a contributor
incident (contributor-reported, not linkable). Three pre-registered probe
rounds in one session wrote their
pre-regs to a session scratch directory, which was later reclaimed — leaving
five citations across a finding file, an always-loaded rules file, and a
maintenance ledger pointing at paths that no longer existed. The criteria
had genuinely been frozen before each run, which is the point: nothing that
survived could show it. Ships `unprobed` per the covenant; its probe joins
the private round-5 queue.
Item 9 (pairwise independence; 2026-07-30) comes from a contributor incident
(contributor-reported, not linkable). Four API keys were probed for separate
rate-limit accounting by exhausting the first alone and observing the other
three keep serving; the finding published "four independent organizations, 4x
throughput", which that probe cannot support. A fresh-context review caught
the inference and the pairwise re-measure came back 6/6 — the conclusion was
right and the method was not, which is the shape worth recording, since a
lucky confirmation is what keeps the method in use. Ships `unprobed` per the
covenant; its probe joins the private round-5 queue.
The single-arm replication clause under the experiment-grader rules
(2026-07-30) comes from a contributor's model battery (contributor-reported,
not linkable). A model written up at N=1 as "30/30, no thinking step, the
default for anything" scored 30/30/20/29 once replicated to N=4 — an invalid
emitted regex that threw, and a null-handling edge case — and was retracted
as a default; a second model in the same battery moved from 4/4 to 3/4 the
same way, its control green on the failing run. The same write-up had
quoted four runs while only one was on disk. Ships `unprobed` per the
covenant; its probe joins the private round-5 queue.
Item 10 (subject identity; 2026-07-30) comes from a contributor incident
(contributor-reported, not linkable). A utility module was moved into a shared
library directory and its suite passed 30/30 afterwards — but nothing asserted
the module's own `__file__`, so the same 30 would have passed against the copy
still sitting in the old directory; a fresh-context review found the hole and
the suite grew a canonical-path plus no-shadowing-copy check (32/32). Scoped
honestly: the review caught it before it certified a wrong artifact, so the
harm — a green run reported for code that was never exercised — is reasoned
from the mechanism, not observed. It is placed as its own item rather than
folded into operational-rigor §4 because the remedy differs in kind: §4 traces
a run to a change at citation time, this asserts the subject inside the suite
on every run. Ships `unprobed` per the covenant; its probe joins the private
round-5 queue.
The detector-positives bullet under "Designing the guard itself" (2026-07-30)
comes from two contributor incidents in one environment (contributor-reported,
not linkable), which is why it is stated as a class rather than as either
symptom. A credential scanner's assignment-tier pattern was written lowercase
while every credential on that host is uppercase, so it reported clean across
all of them; it was caught before deployment by trying it against a known-live
key. A meeting-summary pipeline's corruption check scored the most frequent
single token where the real corruption is a repeated multi-word phrase; a
transcript that was roughly one third watermark junk scored 0.078 against a
0.30 threshold and passed, and summaries derived from such transcripts were
published for weeks before the mismatch was diagnosed — the observed half of
the pair. A cross-family review of this addition corrected its first draft,
which claimed a token statistic "can never fire" on a phrase: the statistic
does respond, and the real barrier is separability, not response. Ships
`unprobed` per the covenant; its probe joins the private round-5 queue.
The verify-by-reconstruction recipe, the item-11 self-benefit-metric rule,
and the sentinel-tagged-fixtures bullet (2026-08-01) are the
ground-truth-gates slice of the deferred-candidate backlog from the
2026-07-31 two-repo mining pass (opus-pack #112, triaged under #115 Phase 1;
ideas only, no text — same sourcing and acknowledgements as the two
2026-07-31 PRs). Each was deferred at the original gate as recipe-level or
needing generalized wording; the wording here is this pack's. All three ship
`unprobed` per the covenant; their probes join the private round-5 queue.
The downstream-observable-differential bullet (2026-08-12) comes from
contributor incidents (contributor-reported, not linkable), two
instances in one project: an application setting with no reliable
direct readback was proven applied by a control/treatment run over a
downstream calculation the setting must move; separately, an auth
protocol bug was pinned by diffing an outgoing request byte-for-byte
against the target application's own observed working request for the
same operation, the byte-length delta decoding directly to the missing
field. Ships `unprobed` per the covenant; its probe — a state change
with no reliable readback, does a ruled reviewer demand a
control/treatment differential before crediting "applied" where a
bare one accepts a single successful-looking run — joins the standing
#115 queue.
The artifact-settles-disputes and derive-the-derivable-constant bullets
(2026-08-04) come from one contributor session's parity-implementation
work against a financial workbook: two independent reviewers flagged a
spec-invented clamp as suspect, and opening the workbook's actual formula
(no clamp) settled the dispute the reviewers themselves had only guessed
at — contributor-reported, not linkable here. The derive-the-derivable
half comes from a separate check in the same session: a stale hand-typed
constant, only ever wrong in policy-year rows no test scenario exercised,
was caught by recomputing it from other cells rather than trusting the
sheet; a second, distinct case in the same pass found two unrelated
quantities sharing one hand-typed value by coincidence, renamed apart to
stop future conflation. Ships `unprobed` per the covenant; their probes
join the standing #115 queue — a future campaign, not round-5, which was
a completed, frozen ten-target slice these rules were not part of.
The experiment-grader arm-environment and attrition-parity rules, the
calibration block's configuration-binding clause, and the fail-direction
bullet's placement clause (2026-08-06) adapt four disciplines mined from
gsd-build/get-shit-done (MIT, ideas only, no text; upstream archived —
successor open-gsd/gsd-core; see README acknowledgements) in the
2026-08-02 dual-model mining evaluation of owner-named repositories, and
kept through a 2026-08-06 re-verification pass — a design-level
disposition review, not a behavioral probe — in which two model families
converged on all four dispositions against the then-current main. All
four ship `unprobed` per the covenant; their probes join the standing
#115 queue — a future campaign, not round-5, which was a completed,
frozen ten-target slice these rules were not part of.
The rule-3 partial-input twin of the zero-input scanner shape
(2026-08-07) comes from the review history of a staged-and-declined
scanner candidate (PR #129, closed unmerged, retained as historical
evidence): two reproduced silent-omission defects — an unreadable
subtree swallowed by the walker's error handler, and a single unreadable
file dropped the same way one level down — each made a partially-read
tree report as clean until folded into an explicit incomplete result
class. A three-lens cross-family duplication audit (grok-4.5 high;
gpt-5.6-luna at ultra and max) agreed the zero-input remedy — a non-zero
matched count — passes the partial case; the lenses split on whether
adjacent semantics (the sentinel bullet's INCOMPLETE bound, scoped to
its declared surface manifest; operational-rigor's fail-closed and
labelled-degradation rules) already covered it, and the owner
adjudicated a one-sentence fold: the semantic doctrine exists elsewhere,
but the local gate-design checklist lacked this named shape, and the
remedy differs in kind (cf. item 10's placement note). Ships `unprobed`
per the covenant; its probe — a grader shape of partial consumption with
a non-zero matched count — joins the standing #115 queue.
Item 12 (multi-name dependency strip; 2026-08-07) comes from a contributor
incident (contributor-reported, not linkable): a test titled "verifies the
fallback path with the primary key absent" stripped one env-var name while
the machine also exported the plural pool form, which the loader checked
first — the fallback the title named had never executed once. Found by a
fresh-context review; fixed by stripping every name the loader reads,
after which the test failed honestly, then passed for the right reason.
Compressed at gate from the contributed draft (same shape, remedy, and
probe; shorter comparison prose). Ships `unprobed` per the covenant; its
probe — seed a suite stripping one alias of a two-alias dependency,
confirm a ruled reviewer catches the live second alias where a bare one
does not — joins the standing #115 queue.
Item 13's wrong-entity-under-success clause (2026-08-12) comes from a
contributor incident (contributor-reported, not linkable): a query
against a data provider's series-lookup API returned a sibling series
under the queried id family with an unqualified success status — the
call itself gave no signal the returned entity differed from the one
requested; caught only by reading the returned record's own name field
against the query intent, then confirmed by harvesting the provider's
canonical id/name mapping directly. Ships `unprobed` per the covenant;
its probe — an ambiguous-id lookup seeded to return a sibling entity,
does a ruled reviewer check the response's own identity field before
crediting the fetch where a bare one accepts any 200 — joins the
standing #115 queue.
The FP-noise numeric-contract clause (2026-08-07; maintainer fold
2026-08-08) comes from a contributor incident (contributor-reported,
not linkable): a golden projection snapshot frozen under one Node major
failed CI under another, every diff an iteratively-solved IRR field at
~1e-13; the first fix pinned CI's runtime (stopgap), the durable fix
rounded the field to 10 dp in the snapshot mapper, removed the pin, and
re-ran green on the very major that had failed. The incident evidences
the rounding remedy and the pin-first shape; the numeric-contract form
and the claimed-portability/pinned-contract boundary are the fold's.
Ships `unprobed` per the covenant; its probe — freeze a solver output
on one runtime, grade on a second the baseline claims to support,
observe whether a ruled reviewer reaches for a declared numeric
contract where a bare one reaches for the pin — joins the standing
#115 queue.
The coupled-edit early-check bullet (2026-08-07; maintainer fold
2026-08-08) comes from a contributor rollout (contributor-reported, not
linkable): tripwire hooks installed across five repos in one day, each
verified two-sided by piped synthetic edit events; one repo's suite was
already red with three unrelated failures — a naive full-suite hook
would have blocked every edit, which is the baseline-first clause. The
earliest-reliable-layer form and the hook-as-example scoping are the
fold's; the original's edit-time-hook mandate, coupling-doc mining
recipe, dead-gate resurrection, and CI-twin pairing were trimmed as
duplicating existing rules (item 3, rule 4) or over-generalizing the
rollout. Ships `unprobed` per the
covenant; its probe — seed a two-file coupling with a red baseline
sub-check, observe whether a ruled reviewer demands the baseline run
before the check may block where a bare one wires it straight in —
joins the standing #115 queue.
The verbatim-output amendment to that bullet (2026-08-12) comes from a
contributor incident (contributor-reported, not linkable) on the same
deployed hook, first-hand: an edit to a translations file re-ran the
coupled type check, which failed on a fixture in an unrelated,
unwatched file drifted by an earlier edit in the same session — the
hook's canned "you changed X" reason named the triggering edit, not
the actual break, and recovery depended on the verbatim compiler
output the block also carried. Ships `unprobed` per the covenant; its
probe — armed with only the canned reason, does a bare model self-blame
the trigger and stall, where a ruled one reads the attached raw output
and finds the real site — joins the standing #115 queue.
The dead-source-level-assertion fake-pass shape (2026-08-12) comes from
the same contributor rollout as the coupled-edit bullet above
(contributor-reported, not linkable): one repo's cross-language parity
invariant was written as a type-level const in production source, and
the repo's build script ran a transpiler that never invoked the
typechecker — the const sat unenforced from the day it was written
until an edit-time hook started running the checker directly, deriving
the same file's coupling that motivated the coupled-edit bullet. It is
adjacent to, not a restatement of, the existing compiled-but-never-
registered-test shape earlier in this item: that one is a test a
maintainer wrote and forgot to wire, discoverable by deliberately
breaking the code; this one is an assertion a *later* reader inherits
and trusts as live, so nobody thinks to break it. Ships `unprobed` per
the covenant; its probe — seed a repo whose build path can succeed
without the typechecker, plant an unenforced type-level assertion,
observe whether a ruled reviewer demands proof the checker runs where
a bare one takes the assertion's presence as enforcement — joins the
standing #115 queue.
The void-amend-disclose-rerun rule comes from a contributor's
measured-harness export (2026-08-18, N=30 ledger items/arm over 6
real-repo review packets, agy gemini-3.7-flash-high vs
gemini-3.6-flash-high; contributor-reported, not linkable — the harness
is not in this repo): Run 1 tripped its own
pre-registered validity clause (>4 dead cells voids the run) after
losing 6/36 cells to empty returns, all six on the two largest prompt
packets. Rather than patching the harness for empty-return retry and
letting the same in-flight run continue, the run was voided outright;
the amendment adding retry-on-empty was logged in the same durable
record as the pre-registration, with an explicit disclosure that Run
1's per-arm scores had already been seen before the amendment was
written, plus the argument for why that could not have manufactured
the eventual result — Run 1's direction favored the incumbent arm, and
the pre-registered decision table treats both arms symmetrically, so a
peek biased toward one arm cannot explain a verdict that didn't move
in that arm's favor. Run 2 re-ran the full battery under the amended
method and lost only 1/36 cells; the verdict cites Run 2 alone. Ships
`unprobed` per the covenant; its probe — seed a run whose validity
clause fires after partial results are visible, observe whether a
ruled agent voids and re-runs versus patching the live run and
netting the fixed cells against the broken ones — joins the standing
#115 queue.
The item-3 gate-runner-aggregation-fails-open shape and items 14–15
(2026-08-20) come from a contributor's TG-bot-helper- unit-test/gate runner,
`checks/run-all.sh` (contributor-reported, not linkable). The runner shape:
one PR (#80) fixed a crashed test dying before printing its own `❌` marker,
leaving the marker-grep matching nothing and the runner reporting a bare,
diagnostic-free `FAIL <file>`; reviewing that fix, one subordinate model
flagged — and the contributor independently reproduced 5/5 with an 820KB
string — that the fix's own `printf | grep -q "❌"` could SIGPIPE-fail under
`pipefail` on large output, contradicting pass/fail independent of the
underlying test result; a second, pre-existing instance of the same SIGPIPE
pattern was found in the runner's outer aggregate condition but deliberately
left out of that PR (scope discipline, item 4) and chipped separately, where
a different subordinate session went beyond the chip's spec and additionally
found the runner's `return`/`exit` truncating its failure count mod 256 (PR
#81) — an exact-256-failures input would have reported success. Item 14
(absence positive-control) and item 15 (type-valid-sentinel-for-absence)
generalize two further incidents mined from the same contributor's session
history: a zero-row database query that silently always-false'd on an
epoch-millis/`Timestamp` type mismatch, and a schema-required field where a
model, finding no data, emitted the literal string `"null"` past every
downstream truthy guard. All three ship `unprobed` per the covenant; their
probes join the standing #115 queue.
The population-claim rule and the run-keyed-artifacts amendment
(2026-08-21) are mined from one contributor bench session
(contributor-reported, not linkable): a 4-probe free-model bench whose
edge probe separates models had twice yielded a universal claim from a
subset — most recently "no model in the pool defends this edge" off 3
of 7 members, undone days later when a whole-pool run under one
harness build found one member guarding it 2/2 and another 1/2 — and
the same session's harness, writing to a hardcoded results filename,
silently replaced the prior week's scorecard on re-run, leaving those
rows recoverable only from a duplicate log. The amendment extends this
section's existing persisted-row clause (a run whose output the next
run overwrote is not a run) from the epistemic consequence to the
design prescription; it is adjacent to, not a restatement of, that
clause. Both ship `unprobed` per the covenant; the population-claim
probe — hand a reviewer a k-of-M bench table plus a "does anything in
the pool do X?" question and observe whether a ruled reviewer bounds
the answer to the tested subset where a bare one publishes the law —
joins the standing #115 queue.
The rerun-is-new-evidence rule (2026-08-29) comes from a first-hand
orientation over this file's own evidence semantics: nine adjacent
passages (preservation, persisted rows, regenerate-and-diff,
verify-by-reconstruction's state-not-history clause, and the
delegation/operational-rigor neighbors) each individually pass a
constructed counterexample in which an auditor never opens a cited
36/36 ledger, re-runs the recipe, gets a fresh 36/36, and declares the
historical report verified — a substitution every current rule
permits. The rule adds the consumption-side dual of the preservation
sentence above; evidence identity is content-verified, never
pathname-bound. Ships `unprobed` per the covenant; its probe — a bare
vs ruled auditor handed a cited-ledger claim and a runnable recipe,
scored on whether the ledger is opened before the claim is credited —
joins the standing #115 queue.

