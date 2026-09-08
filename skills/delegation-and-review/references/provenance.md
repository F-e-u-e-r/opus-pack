# delegation-and-review · references: provenance

Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): the skill's historical review, probe, and amendment records. Canonical rules and inline debt markers remain in `SKILL.md`; any operative re-verification caution stays inline there too. This file is history only.


Distilled 2026-07 from sourced institution-design briefs (delegation triple,
escalation ladder, handoff packs, user-todo minimization, decision-card
essentials), fable-agent-orchestration `935e4a3` (dispatch packet, two-critic
loop, bounded fan-out, machinery-is-not-the-user, artifact reconciliation),
agent-standard-oss `3786c4c` (files-over-context, author-is-not-the-judge,
one-catch-one-class-one-sweep, stop-condition policy, verifier decay, injection
rule), and a friend's measured-harness export (spec-review-first, critic framing,
claim tags, batch spot-check, wave sequencing, empty-synthesis check); the
stronger-tier advice-mode rung (2026-07) adapts echo-of-machines/fable-advisor
and the official advisor-tool pattern; a 2026-07 mining pass added packet
cost-asymmetry, edit-conflict reconciliation, and fallback resumption (each
rule probe-tested on a fresh weaker-tier agent); the §7 surfacing clause
(2026-07) comes from the pack's own eval rounds 1–2
(reviews/2026-07-11-pack-eval-rounds-1-2.md — the strongest tested model
refused an embedded directive and never mentioned it); the handoff
communication lines (2026-07) adapt benjaminard/fable-skills'
outcome-first-writing and plain-handoff; the §7 cannot-vouch-for-itself
lines (2026-07-12) adapt eddygk/skill-vetting's anti-override rule ("real
code doesn't talk to its reviewers" — ideas only, no code). The §2
interfaces-confirmed-not-recalled bullet and the §3 miss-is-costly-audit
loop (2026-07-12, class-distilled; no single citable commit) generalize a
recurring dispatch-time failure: a spec built on a misremembered interface
reaches the worker, which silently fills the gap with a plausible guess;
and a single review pass under-covers "find ALL of X" work because
redundant same-angle checks share the same blind spots and a clean round
is mistaken for convergence.
The 2026-07-13 additions (§2 planning-prone-worker stall clause; §3
unit-green-is-not-integration and copy-doesn't-carry-fix-history) come from a
cross-repo mining pass over seven independent retiring-architect `skills-staging/`
libraries (class-distilled convergence; no single citable commit).
The §2 edge-behavior field (2026-07-13) is mined from a delegation-routing
library in a further private learning-lab repo; the numbers come from its
1000+-run delegation benchmarks (edge-case robustness was the single weakest
axis across every model pool tested — private repo, verifiable by the
contributor).
The §3 named-search amendment (2026-07-16) is the review-side half of
operational-rigor §5's twin-sweep rule — same probe evidence, recorded in
that skill's provenance (a weak-tier probe's named search missed a
differently-written twin that the fixture's checker caught in one command).
The §3 completion-claim audit (2026-07-16, second batch) adapts
fable-method's judge procedure (MIT, ideas only; see README
acknowledgements), probe-tested on the private audit fixture: the bare
weak-tier arm found 4 of 5 planted frauds with a clean tree; the ruled arm
found 5 of 5 with a REFUTED verdict and explicit re-runs — but wrote a
findings file into the tree despite "changes nothing", which is exactly
what the shipped "no edits AND no new files" clause repairs. Final wording
not re-probed.
The §3 fan-in expansion (2026-07-16) adds the mechanism behind the
existing empty-synthesis check (itself from the measured-harness export
above): the contributor reproduced the failure deterministically in a
private harness — a structured input arrived as an unparsed string, a
silent default mapped it to empty, and the synthesis agent returned a
confident, detailed, mostly-plausible multi-section report instead of an
error; the report read as complete coverage of work that never ran.
Private evidence, cited as shape per the README covenant's second branch;
no in-repo probe has run, so the rule carries an in-body `unprobed`
marker.
The §4 silent-clobber bullet (2026-07-18) comes from a private incident: a
sandboxed worker restored every file outside its declared write scope to the
last commit on exit, silently discarding the orchestrator's concurrent edits
in the same tree. One observed occurrence; whether the restore is scope
enforcement or a defect in that sandbox is unestablished, so the rule
prescribes only the defensive split. Private evidence, cited as shape per
the README covenant's second branch; no in-repo probe has run — in-body
`unprobed` marker.
The §3 settled-tree review bullet (2026-07-21) comes from a private
mining pass over two independent incidents in the same review-fan-out
harness: a refuter critic re-read a file the orchestrator had already
fixed mid-dispatch and voted REFUTED on an already-confirmed bug, and a
separate critic committed the reviewed worktree to a branch mid-review,
leaving the requested end-state unreachable. Both observed in a private
audit harness (contributor-verifiable, not linkable here); the fix
(recorded baseline over the protected read set, enforced-copy-or-
frozen-tree with write withheld and no third writer, two return
comparisons that void a moved verdict) is the defensive split, not a
mechanism finding, mirroring how the §4 silent-clobber bullet above
handles its own single-sandbox observation. Private evidence, cited as
shape per the README covenant's second branch; no in-repo probe has
run — in-body `unprobed` marker. The protocol body lives in
`references/settled-tree-review.md` per the pack's split precedent
(protocol out of the lean core; the §3 bullet keeps the trigger, the
claim, the incidents, and the pointer).
The §2 sweep-scope additions (2026-07-21; search-scope/write-scope split,
axis-diverse inventory closed per §3's discovery loop, effect-per-surface
proof gate, and the §3 pointer) come from a private incident: a
find-and-fix-every-instance styling sweep (53 files), three review rounds, and
a merged fix all missed the actual defect — it lived in a shared global
utility class the token grep pattern never touched, and each follow-up round's
"still broken?" surfaced a different category (a color-tier band, a
class-emitting helper function) the prior round's search structurally
excluded. Private evidence, cited as shape per the README covenant's second
branch; no in-repo probe has run — in-body `unprobed` marker.
The §1 port-contention bullet (2026-07-21) comes from a private incident in
a multi-worktree fan-out: a dev server displaced from its configured port
by auto-port-fallback left a hardcoded same-port proxy in the app config
pointing at a concurrent sibling session's server — blank app, all
requests 200, roughly forty lines of in-your-own-code diagnosis before the
cross-port reference was checked (contributor-reported; the private repo
is verifiable by the contributor, not linkable here). Ships `unprobed` per
the README covenant's second branch: no in-repo probe has run — a probe
would need two live servers and a displaced port, a fixture this pack does
not yet carry; the marker records that debt.
The §1 pinned-string bullet (2026-07-22) generalizes two private incidents
from one contributor's subordinate-CLI benchmarks: a pre-registered
re-measurement of one CLI's unstated-edge guard rate, run one day after the
original probe with the model flag and prompt battery unchanged, flipped
the result enough to force retraction of the prior day's published
regression claim; and a second vendor's endpoint, over twelve days behind
unchanged model strings, inverted a reproduced infinite-loop failure into a
fully guarded pass. Both are contributor-reported (private harnesses,
verifiable by the contributor, not linkable here); benchmark rates are not
restated, and the elapsed intervals are contributor-reported shape — cited
per the README covenant, in-body `unprobed` marker. The executable probe
debt is behavioral: fixture a stale dated measurement beside a changed
same-slug probe result and observe whether a weak executor re-runs before
routing — distinct from re-verifying the drift premise itself, which only
longitudinal re-measurement of live endpoints can do. That fixture shape
HAS since run privately (round-4 scored campaign, 2026-07-24, n=3,
mechanical arming): the bare arm never re-ran the probe in any run — the
predicted failure mode, reproduced — while the ruled arm re-ran with full
citation discipline in one of three; no discrimination at the
pre-registered bar, so the marker stands (results in the private ledger,
cited as shape). The
decision-binding sentence in the unknown-fallback (2026-07-23)
repairs a clause a private smoke fixture caught under-binding: the fixture's
probe-unavailable cell caught a ruled weak-tier arm writing
"adverse-assumption-applied" while still routing the risky batch on
the dated note's authority (costume adverse); re-run with the binding
sentence, the same tier held the batch and routed away (n=1 each arm,
private fixture — smoke grade, recorded in the private probes ledger;
the probe is private, so per the covenant's second branch this
clause too remains `unprobed` — the observation is cited as shape,
never as a shipped in-repo probe). The round-4 scored campaign
(2026-07-24) then re-ran the probe-unavailable cell at n=3: the
decision BOUND in every ruled run — the risky batch never routed to
the flagged model — while the cell FLOORed on the evidence-trail duty
(the invocation-attempt record), so the clause stays `unprobed`; the
binding behavior itself is the positive signal, cited as shape.
The §2 recurring-sweep ledgers rule (2026-07-22) comes from a private
incident: across iterations of a repeated review sweep, one reviewer
re-raised a finding class an earlier iteration had refuted against the
dependency's source, and a second flagged as a defect the exact code an
earlier iteration had shipped as a fix; a do-not-re-flag block already
present in one packet prevented exactly this on its surfaces, and both
misses occurred where the block was absent. Private evidence, cited as
shape per the README covenant's second branch; the executable probe — the
same sweep run with and without ledgers, counting re-litigated findings —
has not been run; the in-body `unprobed` marker records that debt. The
lifecycle body lives in `references/recurring-sweep-ledgers.md` per the
pack's split precedent; the §2 field keeps the trigger, the claim, the
category names, and the pointer.
The §1 labels-and-listing rule (2026-07-22) comes from two private
incidents in one contributor's subordinate tooling: a model entry listed
by one wrapper CLI's lineup failed hard on its first real invocation (the
second such ghost entry observed across two independent tools), and a
session caught itself about to treat another wrapper's model strings as
provider API IDs for a quota lookup before verifying they are the
wrapper's internal routing names. Private evidence, cited as shape per
the README covenant's second branch; two probes owed, one per boundary —
invoke every listed model once and diff claimed-vs-callable (the listing
half), and seed an alias-collision fixture and observe whether the
mapping is resolved before a namespace crossing (the provider-ID half).
Neither has run in-repo. The provider-ID shape HAS since run privately:
the round-4 scored campaign (2026-07-24, n=3, mechanical arming) seeded
exactly that alias-collision fixture and it SATURATED at the weak tier
(the bare arm resolved the two-hop mapping unprompted) — no
discrimination, so the marker stands; results in the private ledger,
cited as shape. The listing half's inventory probe remains unrun, and
the in-body `unprobed` marker stands until both boundaries have
discriminating coverage.
The §1 empty-output differential rule (2026-07-23) comes from two
contributor incidents in one day's sessions: a probe's empty output
file was traced through a raw re-probe (no response at the transport),
a gateway check (a models-list call answering 200), and a successful
call to a different model on the same key before the failure was
isolated to the target's route; and a batch bench where one model's
empty slot MOVED between two runs (intermittent) while another model's
same-task failure reproduced identically (a stable per-task failure)
(contributor-reported; the private repos are verifiable by the
contributor, not linkable here). Ships `unprobed` per the README
covenant's second branch; the executable probe — fixture a dead
endpoint beside a healthy sibling on one key, plus a moving-slot
battery, and observe whether a weak-tier agent runs the ladders before
routing — has not run; the in-body marker records that debt.
The §3 reported-failure rule (2026-07-23) comes from a contributor
incident: a sandboxed subordinate CLI reported a verbatim "GATES RED —
do not ship" because its test runner could not create IPC pipes under
the sandbox's restrictions; the same gate re-run on the host was green
both times, and the subordinate's own report had disclosed the sandbox
limitation honestly — the risk was a reader trusting the RED verdict
without reading that far (contributor-reported; the private repo is
verifiable by the contributor, not linkable here). Ships `unprobed`
per the README covenant's second branch; the executable probe — a
fixture whose subordinate report carries a sandbox-caused RED over
green code, observing whether the orchestrator re-runs the gate before
reverting — has not run; the in-body marker records that debt.
The §4 self-report-vs-re-verification rule (2026-07-24) adapts two ideas
from hamanpaul/testpilot-core's tier-2 environment-recovery design (MIT,
ideas only; see README acknowledgements): its escalation counter resets
only when the orchestrator's own deterministic `verify_env` gate passes and
increments on each real re-verification failure — a subordinate executor's
optimistic self-reported success cannot reset or suppress it (verified in
that repo's `remediation.py`: the streak zeroes on the core gate pass and
increments on the real verify failure, never on the executor's self-report)
— and its `agent_recovered` marker records that an agent intervened, never
that the gate passed. Only the counter-integrity and intervention-marker
ideas are adopted; the source's capability-catalog / tool-denied one-shot
recovery machinery is its own design, not installed by this rule. Ships
`unprobed` per the README covenant's second branch: adapted external design
cross-checked against this pack's existing rules (this section's §3
completion-claim audit; operational-rigor §2 two-failure and §5 completion
honesty; ground-truth-gates rule 4), not probed on this pack's private
fixtures.
The §1 dispatch-naming rule and §4 ceiling-inversion rule (2026-07-24) come
from a delta pass over two founding-era sources' post-anchor commits (both
MIT, ideas only; see README acknowledgements): the dispatch rule is a
two-source convergence — agent-standard-oss §8's quota-watching +
reasoning-effort dial and curtischoutw/claude-institution's dispatch.md
explicit-model + user-visible-labeling rules, whose changelog records the
named incident (an Explore dispatch silently inheriting the commander's
expensive model) — bounded here to observable signals only; the
ceiling-inversion rule generalizes claude-institution's 「Fable 起手」
mechanism (ladder inverts when the commander IS the ceiling model),
model-agnostic with a bounded no-viable-delegate exception added at this
pack's gate review. Both ship `unprobed` per the covenant; their probes
join the private round-5 queue.
The §3 read-only-critic rule, §4 fix-the-contract-before-compute rule, and §4
no-silent-backfill rule (2026-07-24) come from a starred-repo mining pass (ideas
only, no text; see README acknowledgements). The read-only-critic rule adapts
NYCU-Chung/my-claude-devteam's per-role tool scoping — its reviewer/planner
agents are granted no Edit/Write (MIT); this pack's rule strengthens that (since
Bash mutates too) into "no file-mutating tool at all" and reconciles it with the
write-capable-critic path (§1 and §3's settled-tree independent copy). The
fix-the-contract rule is a two-source convergence — openai/codex-plugin-cc's
guidance to sharpen the prompt and its checks before dialing up reasoning
effort (Apache-2.0) and addyosmani/agent-skills (MIT) — bounded here to the
contract-has-slack case, not capability/context failures. The no-silent-backfill
rule adapts openai/codex-plugin-cc's rule that a failed or never-invoked delegate
run is reported rather than quietly finished on your own side, reconciled with
§1's sanctioned manual-finish trigger by requiring disclosure. All three ship
`unprobed` per the covenant; their probes join the private round-5 queue. The §2
Rules bullet was also extended from "do not merge" to "do not commit, push, or
merge" (generalizing mindfold-ai/Trellis's check-agent forbidden-operations
list, AGPLv3 — strictly ideas only) — a widening of an existing prohibition, not
a new standalone rule, so it owes no separate probe.
The §3 survey-reports-leads bullet (2026-07-24) is class-distilled from a
private mining pass over the owner's own sessions (no code taken): a single
codebase-lightening session whose read-only fan-out survey was wrong four
separate ways, each over-claiming — a substring count of "66 three.js sites"
that was 2 files, "byte-identical" components that diverged on a prop and a
fallback, a "NumField duplication" that dissolved into two incompatible
families, and a "dead" component with a live registry entry — each reversal
re-ordering the tiered plan. Distinct from the synthesizer-fed-nothing bullet
above (empty input → confident synthesis) and the settled-tree bullet
(re-reading an already-fixed file): here the survey ran and returned
non-empty, confidently wrong leads. Private evidence, cited as shape per the
README covenant's second branch; no in-repo probe has run — in-body
`unprobed` marker.
The §5 handoff-compression bullets, the §2 blocked-substitutes clause,
and the ledger reference's absence-is-not-resolution rule (2026-07-31)
distill a two-repo mining pass over public Apache-2.0 sources (ideas
only, no text; see README acknowledgements): a
session-transcript compression tool's decision records — retention
keyed on re-derivability rather than on success/failure; same-failure-only
merging (that tool's decision record notes its first draft of the
merge rule lacked the condition and could have hidden a distinct
earlier error behind the last one — their adversarial review caught it
before anything shipped; the incident is theirs, adopted here as the
rule's motivation); honest,
executable omission markers; and an
audit mode that samples what compression dropped — and an agentic
security-scanning product's completion rules — the named fake-success
shapes a blocked run must refuse (schema-satisfying output included),
and differential-comparison semantics where a finding absent from an
incomplete re-review stays unknown rather than resolved. The evaluation
behind the batch ran a ten-agent verbatim scan across two model
families plus a third-family cross-check, every load-bearing citation
re-verified against the source. All ship `unprobed` per the covenant;
their probes join the private round-5 queue.
The §5 terminal-marker-loop bullet and the §7 marker-framed-packet recipe
(2026-08-01) are the delegation-and-review slice of the same mining pass's
deferred backlog (opus-pack #112, triaged under #115 Phase 1; ideas only, no
text — sourcing and acknowledgements as above). Both were deferred at the
original gate as small/recipe-level items to bundle with the next
handoff-discipline batch — this batch. Both ship `unprobed` per the
covenant; their probes join the private round-5 queue.
The §4 worktree-base-skew bullet (2026-08-04) comes from a private incident,
a positive case: a parent session had spun two tasks into separate spawned
worktree sessions and was then told to "pick up" both. It declined to
re-implement (naming the double-edit collision that would guarantee),
supervised instead — re-ran each child's suite itself, wrote its own parity
probe, fixed one integration bug a child had introduced — and flagged at
pick-up time that both worktrees had branched from HEAD without its own
still-uncommitted fixes, declaring a conflict audit for integration time.
The predicted conflict then actually occurred during the merge and was
resolved cleanly because it had been anticipated. Private evidence, cited as
shape per the README covenant's second branch; no in-repo probe has run —
in-body `unprobed` marker.
The §3 blame-shift-to-pre-existing and dirty-tree-diff-misattribution
bullets (2026-08-04) come from one contributor session's implementation
dispatch onto a live tree: a subordinate CLI attributed a failing test to
"a pre-existing" state, refuted in one comparison against a full gate run
the contributor had captured nine minutes before dispatch (200/0 passing);
minutes later the same contributor caught its own reflex to flag a
subordinate's file touch as out-of-scope before realizing `git diff`
against bare HEAD was crediting the subordinate with the contributor's
own uncommitted edit in that file — and later in the same session used a
pre-dispatch backup correctly, diffing a return against it instead of HEAD
to confirm a golden snapshot truly hadn't moved. Contributor session,
cited as shape; the private repo is verifiable by the contributor, not
linkable here. Ships `unprobed` per the README covenant's second branch;
no in-repo probe has run.
The §3 checkpoint-batching rule and §6 live-exchange rule (2026-08-06)
adapt two disciplines from gsd-build/get-shit-done, verified in its
successor open-gsd/gsd-core (MIT, ideas only, no text; see README
acknowledgements), mined in the 2026-08-02 dual-model evaluation and
kept through the 2026-08-06 batch-1 re-verification — a design-level
disposition review, not a behavioral probe — in which two model
families converged (the checkpoint rule's never-batch carve-outs were
that review's one scope-widening FIX, converged across both families).
The source's shapes: a recorded defect class naming the hidden token
cost of a checkpoint pattern that discards subagent context across
pause-and-respawn (the cold-start economics), and human-verify
checkpoints that stop and surface even in autonomous mode and are
never auto-approved (the never-fabricate boundary). Both ship
`unprobed` per the covenant; their probes join the standing #115
queue — a future campaign, not part of any completed campaign.
The §1 cold-start ladder (2026-08-07) comes from two contributor
incidents in different environments (contributor-reported, not
linkable): four separate false "model dead" verdicts were each revived
by a second, warmed probe — sometimes an identical retry, sometimes the
same call with streaming enabled — rather than trusting the first
non-streaming timeout, and a scheduled tool-search gate stalled on its
first cold invocation of a session before succeeding on re-entry. Both
share the same shape — the first
touch of a lazily-initialized subsystem timing out for reasons
unrelated to the target's reachability — which the existing
differential-diagnosis bullet's two ladders (single endpoint empty,
model empty on some tasks) did not name; this adds it as a third,
narrower ladder rather than folding it into either, since its remedy
(one warm re-invocation in the same session) differs from both.
Bounded at gate: the warm re-invocation applies only to invocations
safe to repeat (read-shaped, idempotent, or explicitly retriable) — a
timed-out side-effecting call has unknown commit state and settles what
landed at the destination instead of being replayed, so the ladder can
never read as an at-least-once mutation license.
Ships `unprobed` per the covenant; its probe joins the standing #115
queue.
The packet-error-propagates-to-verdict bullet (2026-08-12) comes from
contributor incidents (contributor-reported, not linkable), two
instances in one project: a dispatch packet overstated a contract, and
two independently run reviewers each flagged the identical CRITICAL
derived from that overstatement — read as corroboration until the
packet's own claim was checked; separately, a packet's wrong premise
about where state was held inflated a different reviewer's finding,
and in the same project a subordinate placed a new test file in a
directory the packet's own instruction had specified incorrectly,
which the project's test runner's include pattern then silently
excluded. Ships `unprobed` per the covenant; its probe — plant a
dispatch packet with one incorrect premise, observe whether a ruled
reviewer's adjudication checks the premise before crediting a finding
derived from it, where a bare one credits it outright — joins the
standing #115 queue.
The weak-model-tool-surface bullet (2026-08-12) comes from a
contributor's own design principle, applied and observed working
(contributor-reported, not linkable): a tool surface built for a
free-tier subordinate to drive a multi-step automated flow was
explicitly redesigned around "expose high-level task tools, keep the
mechanism hidden, and surface the recurring precondition as first-class
state rather than letting each tool silently fail on it" — a sweep
after the redesign caught two of the wrapped mechanism tools not yet
returning the shared precondition state, and a dedicated cheap-probe
step was added ahead of the expensive path for exactly this reason.
Design guidance rather than an incident report; ships `unprobed` per
the covenant, its probe — a weak-tier subordinate driving a
mechanism-level tool surface with a swallowed precondition vs. one
with the precondition promoted to a named return, comparing task
completion — joins the standing #115 queue.
The §3 misconduct-verdict-plumbing rule (2026-08-15) comes from a
contributor incident (contributor-reported, not linkable): during a
model bench, a subordinate CLI resolved its working directory from the
inherited `$PWD` env var instead of the real process cwd (which the
harness's directory-changing spawn never rewrote), and one session
recorded both a fabrication verdict and a scope-violation verdict
against two different models — both retracted the same day after a
deliberate real-cwd-vs-fake-`$PWD` split run isolated the channel. The
first worker's transcript had self-reported the wrong directory's file
listing from the start; the mtime-forensics limit was learned
attempting (and failing) to rehabilitate the fabrication verdict after
the fact. Kin to the reported-FAILURE rule (environment fabricating a
RED) but placed separately because the object differs: that rule
audits the worker's claim, this one audits the dispatcher's own
verdict about the worker. Ships `unprobed` per the covenant; its
probe — a spawn with mismatched real-cwd/`$PWD` and a grader that
checks only the real cwd, does a ruled reviewer suspect the plumbing
before the worker — joins the standing #115 queue.
The §4 dead-delegate-launch-plumbing bullet (2026-08-28) comes from a
contributor incident (contributor-reported, not linkable): two background
CLI dispatches in one session died with no output file while
identically-shaped controls succeeded; direct reproduction isolated
open-pipe-on-fd0 (write end never closing) as the hang mechanism, a paired
with/without-`</dev/null` control REFUTED the redirect as the diagnosis of
the original failures, and the EXIT=0-was-tail's misread occurred live in
the same investigation. Two independent cross-family lenses converged on
launcher descriptor topology as the likely wiring variable, but WHY the
wiring varied remains unresolved — the rule prescribes pinning and correct
status reads, deliberately not a topology claim. Ships `unprobed` per the
covenant; its probe — a weak-tier arm dispatching a background delegate
through a pipeline, bare vs ruled, scored on whether it pins stdin and
reads the delegate's own status — joins the standing #115 queue.
The coverage-before-clearance rule (2026-08-29) comes from a first-hand
orientation over this file's own review-lane semantics, after an intake
question asked whether brief-vs-diff reconciliation was already covered:
the dispatch-side scope declaration (§2), the completion-claim audit
(dishonesty-bound, bound to an execution deliverable, and claim-side),
the packet-errors rule (finding-side), and the settled-tree protocol
(motion-bound) each pass a constructed counterexample in which an honest
reviewer PROCEEDs over a silently-truncated packet (a pagination cap
dropping one requested file's diff) and the orchestrator reads the
verdict as full-scope clean — a false clearance with zero rule
violations. The rule closes the consumption-side gap; the locked
invariant is credited-scope ⊆ actually-covered-scope,
explanation-based, deliberately not path-set equality. Ships `unprobed`
per the covenant; its probe — a bare vs ruled orchestrator handed a
truncated packet's PROCEED and a broader requested scope, scored on
whether the absent path gets credited clean — joins the standing #115
queue.
The §3 reviewer-execution-principal bullet and
`references/reviewer-capability-receipt.md` (2026-09-01) come from a
first-hand orientation over this pack's own review-dispatch machinery,
classified **B. PARTIAL-GAP**: the adjacent substrate is real (this
section's read-only critic, independent copy, and settled tree;
cross-model-review §2's packet duties and §3's compromised-reviewer
handling; security-architect's general least-privilege line), and the rule
raises it to one new object at abstraction L2 — reviewer execution-principal
confinement: artifact isolation is not principal confinement. The harness
facts behind it are evidence-tiered and must stay so: FIRST-HAND CURRENT at
adoption time (the reviewer CLI's config default `workspace-write`; its help
text defining the sandbox as the policy for executing model-generated shell
commands — write-restricted, not exec-restricted; a broad-read permission
surface; run banners recording model, effort, and sandbox mode); RECORDED
HISTORICAL (a reviewer re-planting a repo test file mid-review, 2026-07-19;
a shared-cwd read of a sibling reviewer's verdict, 2026-07-17; cross-vendor
operator-config auto-ingestion — the folded #213 evidence, provenance only);
and UNKNOWN (model-generated-command egress; exec-mode tool loading; the
effective host-wide write bound under read-only — declared posture, denial
never probed). Gate history, recorded honestly: a three-round adversarial
design gate (two same-provider-family variants at max effort — a
two-variant gate, cross-family only versus the author, never a cross-family
pair) returned FIX/FIX in every round and ended CAP-REACHED / NOT-PASSED at
revision v3, with zero frame objections across six verdicts; the owner
adjudicated the final round's twelve corrections into a v4 candidate; a
one-round narrow convergence confirmation returned PROCEED + FIX —
NOT-PASSED (1/2): the second variant caught what the first passed, a schema
gloss equating `read_reach: none` with packet-only mode against the
any-reviewer-directed-capability live trigger. The owner refuted that gloss
and authored the exact one-line repair; final acceptance is owner
adjudication plus a mechanical closure gate (sealed-archive hash chain, a
proven single-line byte delta, an eight-row mode/receipt truth table, and a
same-shape conflation sweep with a planted-mutant control that demonstrably
fails on the unrepaired bytes) — not reviewer consensus, and no gate in
this lineage is recorded as passed. One round-1 sub-claim was rejected with
reason and stands: a reviewer proposing a probe and the operator explicitly
granting it afterwards is a legal path — the anti-laundering rule (a
preauthorization whose content is artifact-selected is not a grant) does
not close it. A shared-account quota collision voided one round-3 attempt
with zero verdicts (round not consumed) — operational evidence only. The
receipt is doctrine plus a harness-assertion CANDIDATE: nothing claims it
is automated or enforced; the capability-receipt harness follow-up is a
separate owner-gated item, not started; the general sandbox/zero-trust
reviewer-runtime layer is deliberately not activated. Full trail — four
design revisions, five packets, eight verdicts, per-round adjudications,
fifteen probes, and the closure record — is
`reviews/2026-09-01-reviewer-execution-principal-c8/`. Ships `unprobed`
per the covenant: the marker records that the doctrine's behavioral
effectiveness on reviewer/orchestrator conduct is unprobed (its probe joins
the standing #115 queue); it does not mark the harness observations, the
receipt design, or the repair, which carry the evidence above.



The §2 re-delegation bullet, §3 first-person/accounting bullet, and
cross-model-review §1's transitive family clause (2026-09-02) land the ⑫
recursive-delegation design: orientation verdict B (PARTIAL-GAP) at
abstraction L2 (delegated-authority / contribution-provenance propagation)
over the existing substrate (this skill's bounded fan-out, claims-audit,
and settled-tree machinery; cross-model-review's contributing
author-family precedent; §3's execution-principal envelope), closing four
missing semantics: re-delegation grant, subset propagation,
contribution/first-hand provenance, and nested budget/family accounting.
First-hand evidence: an inert two-level nested-spawn probe succeeded in
the dispatching harness (the mechanical fact the rule governs), and an
orphan-principal lifecycle window was DISCOVERED and expressly NOT
ACTIVATED into doctrine. No runtime/tooling change is required; there is
deliberately NO hard max-depth rule — judgment contribution, not process
depth, is the criterion; deterministic helpers are never judgment
principals; an operator-approved multi-agent tree remains legitimate.
Design trail (honest): round 1 dual-blind (two same-provider variants at
max effort — NOT cross-family) split 1/2 — one PROCEED, one FIX with two
findings the owner validated first-hand: F1, the retrospective
contribution criterion incorrectly used at the prospective authorization
boundary; F2, budget-consuming non-contributing judgment principals
lacked a compact reporting channel. The owner authorized exactly two
semantic corrections (prospective invocation-based authorization;
two-tier compact/rich accounting) plus pinning control cases; round 2 on
the frozen v2 design returned PROCEED from both reviewers, whose
nearest-failure sections independently converged on the same control-case
reading (budget-axis-only vs authorization) and both judged it sound —
wording frozen as reviewed, zero polish. Behavioral effectiveness of the
shipped wording is unprobed (the single in-body marker in §2); its probe
joins the standing #115 queue. Evidence package:
reviews/2026-09-02-recursive-delegation-c12/.
