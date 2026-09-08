# skill-authoring · references: provenance

Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): the skill's historical review, probe, and amendment records. Canonical rules and inline debt markers remain in `SKILL.md`; any operative re-verification caution stays inline there too. This file is history only.


Distilled 2026-07 from sourced briefs (attribution in the repo README) — an
MIT-licensed skill-library brief (taxonomy, authoring rules, three-lens
review) and an institution-design brief (executable-rule format, review
checklist, honesty clause) — plus agent-standard-oss `3786c4c`
(one-source-of-truth, fix log, slop list, compile-don't-retrieve, keep-in-sync,
knowledge-succession), fable-agent-orchestration `935e4a3` (session mining
rules), and a friend's measured-harness export (2026-07; correct-in-place,
fresh weaker-tier gap probe, rule-misfire diagnosis); the state-phrased
trigger rule (2026-07) adapts TheColliny/FableClaudeMDForOpus's event-phrased
routing; the taxonomy, secrets, and rationalization-example lines (2026-07)
adapt the community retiring-architect pattern (Rodbourn), Iwo's rigor pack,
and DizzyMii/fable-skills.
The 2026-07-13 additions — the `references/project-skill-templates.md` companion
(the §5 category-writing templates), the extension-point/adapter taxonomy entry,
the stale-absolute-path and don't-paraphrase-a-load-bearing-clause rules, and the
MANIFEST+UNCERTAINTY packaging rule — distill a cross-repo mining pass over seven
independent retiring-architect `skills-staging/` libraries whose entry shapes
independently converged (class-distilled; no single citable commit).
The §2 verifying-the-incident-does-not-verify-the-prescription rule (2026-07-14)
generalizes this repo's own PR #26 review: 4 of the 27 rules that PR proposed
cited real incidents but prescribed mechanisms that failed on their own
motivating case — caught in PR #26's own review and fixed before merge, never
reaching main — by a cross-model-family review of the mechanism itself (see
that PR's review thread for the specific misses).
The §6 rule-by-rule self-consistency check (2026-07-16) generalizes PR #29's
own review: three of the four must-fixes on that PR's new §2 bullet were the
bullet violating this file's existing rules (§5 state-phrased triggers, §3
don't-paraphrase-a-load-bearing-clause, §1 executable-rule format), each
passing the author's self-review and surfaced only by applying the file's
rules individually to the addition (see that PR's thread).
The §5 cross-reference-is-not-a-load and red-line-domains rules and the §7
enforcement ladder (2026-07-16) adopt fable-method's published negatives
and red-line authoring gate (MIT, ideas only; see README acknowledgements).
Their evidence base is attributed external A/B results cited as shape
(numbers not restated) plus this pack's own §7 wrong-layer precedent; no
in-house authoring probe has run for these three, so each carries an
in-body `unprobed` marker per the README covenant's second branch (the
ladder and red-line are design/normative rules whose executable probe
shape is an open question, unlike the behavioral rules probe-tested the
same day in operational-rigor).
The §7 word-diff-not-structure-check rule (2026-07-17) generalizes a
colleague's condense pass on a private rules file (shape cited, exact
clause count not independently verifiable): the pass passed every
structural check its author ran (anchors, reference pointers, section
headers, GOOD/BAD pairs all present against the pre-edit backup)
and still silently dropped clauses from surviving bullets, including at
least one ordering constraint — caught only by a follow-up word-diff
against the backup. The rule ships with its own forced-artifact clause
(named command + dropped-clause list in the change record) rather than as
bare prose, per this file's own enforcement-ladder precedent. Genuinely
`unprobed`, not by analogy to the design/normative markers above: whether a
weaker-tier executor performs the word-diff step (versus the superficially
similar anchor-grep) when instructed is a behavioral claim this pack's own
§6 fresh-weaker-tier-agent method could test — that probe has not yet been
run, and this note records that gap rather than asserting it is untestable.
The trace clause's destination scope (2026-07-18) was widened after a
reviewer flagged it on PR #40 post-merge: as merged it named only the
remaining text and "a reference file", yet the compaction bullet above it
already demotes incident detail to the fix log and §5 relocates clauses
across skill homes — destinations a same-tree-only search misreads as
losses, inviting a duplicate-home restore (§4). The reviewer's motivating
verification run is contributor-reported (not independently reproducible
in this repo); the doctrine gap it points at is verified against the
file's own demotion and relocation rules.
The §1 gate-placement rule (2026-07-18) adapts fable-method v1.4.0's
scope-stop relocation (MIT, ideas only; see README acknowledgements). Its
evidence is the source's own published fail-then-fix measurement (their
round-15 smoke eval, n=1 per cell by its own labeling: a weak-tier
executor blew past the mid-procedure form of the check and held at the
moved-first form; numbers restated in-body because the source publishes
them, with the smoke grade carried alongside). It carries an in-body `unprobed`
marker per the README covenant: the external measurement is of one
skill's one gate, and whether placement generalizes across gate types is
exactly what an in-house probe would test — that probe has not been run;
the marker records the debt.
The §5 keyword-grep-absence rule (2026-07-21) generalizes three private
incidents in one week, each the same shape: a keyword grep of a rules file
returned nothing, "not covered here" was concluded, and the content existed
under different phrasing — including one proposed upstream addition whose
substance was already in the target file, caught only by reading the
section during drafting (contributor-reported; the private repos are
verifiable by the contributor, not linkable here). It ships `unprobed` per
the README covenant's second branch — no in-repo probe has run. The
recorded probe shape (seed a reworded twin of a rule, instruct a
weak-tier agent to dup-check an addition, observe grep-only vs read)
HAS since run privately: the round-4 scored campaign (2026-07-24,
n=3 per arm, mechanical arming) ran exactly it and did not
discriminate at the weak tier — the bare arm sometimes found the twin
by reading unprompted (saturation-veto), so the marker stands;
results live in the private ledger, cited as shape.
The §6 deployment-runtime rule (2026-07-21) comes from a private incident:
a skill was authored, reviewed through the lenses above, and finalized for
the author's local macOS environment, then rebuilt wholesale the same week
when the user mentioned it would run inside a sandboxed Linux VM — host
identity, launcher mechanism, and machine-local MCP tool-name assumptions
all failed on the real target (contributor-reported; the private repo is
verifiable by the contributor, not linkable here). Probed in part
(2026-07-24): the private suite's round-4 scored campaign ran exactly the
recorded probe shape — a weak-tier reviewer given a machine-bound skill
plus a named foreign runtime — as its one cell that discriminated at
n=3 under fully mechanical scoring (transcript-verified arming, verbatim
reply capture, frozen fixtures/oracles: bare arm 0/3 PASS, ruled arm
3/3 PASS; the checker binds the named-target engagement, the
assumption-sweep firing on a target-inferable plant, the
BLOCKED-without-risk-acceptance disposition, and the
no-blanket-flagging control). The suite is private, so the results are
cited as shape — the numbers restate the suite's own record and are not
independently verifiable here — never as a shipped in-repo probe. The
probe's fixture exercised a SKILL under review; the rule's
plugin-instruction-files surface was not exercised and stays unprobed. The rows that cell
does not bind — taxonomy recall, in-file labeling/remediation, the §1
authoring-start gate, the risk-acceptance alternate Done — remain
`unprobed`, and the in-body marker names both halves.
The §3 capability-negative rule (2026-07-22) comes from a private
incident: a subordinate-CLI playbook asserted a capability did not exist
("model switching only works interactively; no flag") — true when
written, false at the tool's current version — and the stale negative had
been silently steering sessions into a degraded interactive-only path
until a review pass re-probed the binary. Private evidence, cited as
shape per the README covenant's second branch; the executable probe —
re-running recorded capability-negatives against the current binary on
each version change and counting flips — has not been run as a standing
check; the in-body `unprobed` marker records that debt.
The §4 superseded-verdict sweep (2026-07-23) comes from a contributor
incident: after promoting a new default in a playbook, a whole-file
grep found two older evidence blocks still carrying bold
keep-the-old-default verdicts from earlier benchmark rounds — each
would read as current to a reader (or a weaker executor) reaching it
before the new summary; both were tagged superseded-with-date rather
than deleted (contributor-reported; the private repo is verifiable by
the contributor, not linkable here). Ships `unprobed` per the README
covenant's second branch; the executable probe — seed a flipped
default above an untagged stale verdict block and observe whether a
weak-tier executor follows the stale order — has not run; the in-body
marker records that debt.
The §7 relative-budget rule (2026-07-23) comes from a contributor
incident: a maintenance log carried a "still owes an extraction pass"
line across sessions for a file that had already extracted everything
extractable — every remaining line traced to a live trigger, including
one added after the old baseline was set; the size gap was that new
rule's cost, and honoring the stale number would have meant gutting a
live trigger or carrying phantom debt indefinitely
(contributor-reported; the private log is verifiable by the
contributor, not linkable here). Ships `unprobed` per the README
covenant's second branch; the executable probe — seed a maintenance
log whose owes-line predates a legitimate post-baseline addition and
observe whether an executor re-baselines or keeps chasing the old
number — has not run; the in-body marker records that debt.
The §3 campaign-continuation rule (2026-07-23) comes from an incident
whose upstream half is verifiable in THIS repo's public history: the
#59 combined integration merged mid-campaign, and the review continued
through #60 and #61 (a 12-round, 3-PR campaign); a contributor's
reverse-port had diff-verified local caches against #59 as "upstream
final" and owed a follow-up fold when the later rounds landed (the
local-cache half is contributor-reported). Ships `unprobed` per the
README covenant's second branch — the in-repo history evidences the
incident, not a probe; the executable probe — fixture a repo whose
sync target has newer merged PRs touching the synced files and observe
whether a weak-tier executor checks before declaring the sync final —
has not run; the in-body marker records that debt.

The §7 pressure-probe and move-map rules (2026-07-24) adapt obra/
superpowers v6.2.0's skills-compression method and SDD-redesign global
constraints (MIT, ideas only; see README acknowledgements): their commit
b9e75dd's measured deletion regression (control 8/10 → treatment 5/10
under the exact pressure the deleted section rebutted, corroborated on two
model families — their numbers, cited as shape per the covenant, never as
this pack's evidence) and their verbatim-move rule + row-by-row move map
for eval-tuned prose. Both ship `unprobed`; the pressure-probe rule's own
probe is exactly the shape it prescribes and joins the private round-5
queue with the move-map rule's.
The §4 memory-lifespan-tiers rule and §5 catalog-collision rule (2026-07-24)
come from a starred-repo mining pass (ideas only; see README acknowledgements).
The lifespan-tiers rule adapts mindfold-ai/Trellis's three-tier memory model —
task directory / session journal / durable spec, each with an explicit admission
test (AGPLv3 source, strictly ideas only, no text). The catalog-collision rule
is a two-source convergence — addyosmani/agent-skills's deterministic pairwise
trigger-description similarity check (a fixed similarity ceiling in the source,
whose separate ratchet-only CI floor governs rank-1 routing accuracy; this pack
applies that ratchet-only discipline to the collision ceiling as its own
strengthening — MIT), and matlab/matlab-agentic-toolkit's crowded-catalog
trigger-degradation note with
its scope-install / invoke-by-name / prune mitigation ladder (MathWorks
field-of-use license — ideas only, no text). Both ship `unprobed` per the
covenant; their probes join the private round-5 queue — the catalog-collision
rule's is directly runnable against this pack's own 13 skills.
The §2 verify-capability-before-shipping-the-doc rule (2026-07-24) is
class-distilled from a mining pass over the owner's own sessions (no code
taken): with a scarce authenticated remote session about to expire, doc edits
describing a just-patched self-heal behavior were held until a regression gate
proved the behavior, on the explicit reasoning that telling the weaker model
"the engine auto-searches all categories" is a capability claim that must be
verified live first or it ships a false instruction. Ships `unprobed` per the
covenant;
its probe joins the private round-5 queue.
The §3 world-fact-staleness and bound-invalidation rules and the §7
bare-executor-probe and read-the-source rules (2026-07-25 — the last of these
shipped under the bold name "a derived file contradicting reality has not
necessarily drifted", retriggered 2026-07-27 per the entry below) are
class-distilled from a maintenance session on the owner's own rules files (no
code taken), and are one incident seen from four sides. A finding measuring
rule-following at two file sizes carried the clause "re-test if either file
grows past ~250 lines"; both files reached 297 and 318 and the clause never
fired, because nothing read it — the bound-invalidation rule. The re-test that
eventually ran added a bare-executor control arm the original lacked, and found
3 of 8 recently-folded rules reproduced with no rules file at all — the
bare-executor-probe rule, the one item here with a measurement rather than a
shape behind it (n=8 rules, 1 probe per cell; it detects a large effect, not a
small one). The staleness sweep that followed found all 8 stale instances in
the one file carrying model names and CLI behavior, none in the three carrying
method — the world-fact rule. And one of those stale lines turned out to be
copied faithfully from a source file carrying the same error, so fixing the
derived file alone would have been undone by the next write-back — the
read-the-source rule. All four shipped `unprobed` per the covenant; the
2026-07-27 entry below records their first probe results.
The §7 read-the-source trigger repair (2026-07-27) comes from the first
probe run of the four 2026-07-25
rules above — the covenant's queued probe, run against the merged text
(contributor-run and contributor-reported, not linkable; n=1 per arm, one
weaker-tier executor, screens for a large effect only; a
first round was discarded because its scenarios leaked the taught
distinction, and one bare arm was discarded as contaminated by the author's
own session memory reaching the subagent — a bare arm must be checked for
citations of the finding under test). Results: bound-invalidation and the
bare-executor-probe each discriminated (bare arm failed, ruled arm passed;
the bare-probe rule's own bare arm reached the instinct — "correct and
non-duplicate clears the bar for truth, not for inclusion" — but decided by
judgment, never running an arm). The world-fact-staleness rule did not
discriminate — both arms produced the scoping, the bare one unaided; at one
run per arm
this is flagged in its marker for a demotion judgment, not demoted here. The
read-the-source rule failed BOTH arms: handed a wrong value in a file with
no provenance cue, each arm edited it in place — the written trigger named
the very classification ("a derived file") the rule exists to force, so it
fired only when provenance was already known. The repair restates the
trigger as the observable state; the repaired form is unprobed and its
marker records that. Across the four, the two that discriminated hand the
executor a procedure and the one reproduced unaided hands it an observation
a careful bare executor states without help (the repaired fourth failed
both arms and sits outside this contrast). That pattern was itself drafted as a
candidate rule — triage the probe queue by asking whether a candidate hands
the executor a procedure or an observation, and skip probes on the
observations — and probed the same day: a clean bare arm produced its
substance unaided; whichever pair-cell that lands in (non-discriminating
or harmful), the always-loaded file is not its home. It is recorded
here as an observed pattern, not shipped as a rule.
The §2 derive-cross-references clause (2026-07-27) has its own evidence
chain, distinct from that probe run: two mis-targeted section references
written from recall by one author in one day, each while the correct
location sat already-quoted in the working context — one reached main and
cost the maintainer fix commit `8f8413f` (repo-verifiable); the second was
caught in the author's draft before submission (contributor-reported). The
clause itself ships `unprobed` per the covenant; its probe joins the
private round-5 queue.
The §7 bare-probe bullet's environment-relative-baseline and
read-the-arms'-reasoning clauses (2026-07-27) are class-distilled from one
downstream consumer's first fold probes of this repo's own merged rules
(contributor-reported, not linkable; four
rules probed, pre-registered arms, weaker-tier executor). Three of the
probes produced
the clauses. A fact-anchoring rule failed to discriminate solely because the
consumer's global rules file carries a standing verify-before-relaying order —
the general form of the candidate — so the local verdict (redundant) was real
there and not exportable to any environment without that baseline: the
environment clause. And in
both discriminating probes the arms' reasoning outlived their verdicts: one
failing bare arm defended shipping an unverified capability doc with "the
document didn't lie — it described the intended behavior", which became the
folded rule's named rebuttal, while one passing ruled arm over-fired and
refused to produce any plan at all, forcing a reword so compliance composed
with the task: the reasoning clause. The baseline-versus-leakage clause comes
from the same consumer's earlier probe round, where subagent bare arms were
found not to be bare at all: an auto-memory store persisted across the fresh
invocations and the arms recalled the findings under test, so runs that read
as unaided reproductions were partly recall — the countermeasures (recall-
dodging framing, an explicit disregard instruction, and a citation check on
the output before scoring) were added to the later pre-registrations for that
reason.
The §7 tier-inheritance clause (2026-07-28) distills the same downstream
consumer's tier replication (contributor-reported, not linkable): a fold
probe run at the probing session's own
strong tier returned bare 3/3 on a citation-re-resolve rule ("redundant
with model capability"); a same-day replication of the same fixture and
task at a weak tier returned bare 0/3 — every weak arm copied the stale
citation verbatim, two reporting they had "verified the content
transferred intact" (byte-fidelity of the copy, the one check that cannot
catch an already-wrong citation). N=3 per cell, one fixture, one rule.
All four clauses ship `unprobed` per the covenant; their probes join
the private round-5 queue.
The §3 contributing-is-not-adopting rule and the §3 re-resolve-citations-on-
install rule (2026-07-28) are contributor-reported from one downstream
consumer's adoption pass over this repo (the upstream half — the merges and
their PR numbers — is verifiable in this repo's history; the local half is
not linkable). One incident, two faces. A batch of the consumer's own rules
merged here and was never ported into the files that govern their sessions;
it went unnoticed for days precisely because the author kept applying the
rules from working context, and surfaced only when their user asked why the
rules were not in use — the contributing rule. Porting them then required
installing sibling skills whose `§N` citations addressed THIS library's
numbering: several resolved to differently-numbered local sections and two
named anchors had no local counterpart, caught by grepping the destination
rather than trusting the numbers — the citation rule, whose
record-the-retargets half exists because the retargeted copy would otherwise
read as drift on the consumer's next diff against upstream, inviting a
re-sync to restore the broken numbers. Both ship `unprobed` per the covenant;
their probes join the private round-5 queue.

The 2026-07-30 scenario-does-the-rule's-work rule rests on one attested round
with an ambiguous in-repo precursor. The attested round is a downstream
consumer's probe of a different rule — the §2 push-verification recipe — whose
scenario asked the arm to "report whether it carries anything beyond that
intended work", which performs a read-every-outgoing-commit rule outright;
both arms passed 3/3 at the weaker tier. Contributor-run and not linkable.
This repo's own 2026-07-27 entry, recording a first round discarded because
"its scenarios leaked the taught distinction", is cited as a precursor only:
that record does not distinguish a scenario carrying finding content
(leakage, already addressed by the generic-scenario clause) from one
instructing the behavior, so it is not counted as a second instance. The
attested round also did not change an outcome — the discarded round licensed
no verdict (per the rule it motivates), and the clean re-run returned both
arms passing again, so the recorded disposition rests on the valid round and
landed where the discarded one had pointed;
what the rewrite bought was the standing to report it. The harm the rule
guards against — a round spent demoting or dropping a rule the probe never
tested — is therefore reasoned from the verdict list, not observed. Ships
`unprobed`: the failure mode is attested once, the fix is not probed; its
probe joins the private round-5 queue.
The §1 author-time pruning pass (2026-08-04) consolidates the file's own
pruning discipline — already spread across §4's short-router earn-the-line
and Placement-test rules, §6's doctrine-contradiction lens, and §7's
bare-vs-ruled "buys nothing" probe — into one cheap author-time pre-filter, so
the include-and-place decision is gated before the expensive review and probe
rather than only after them. Motivated by a growth in queued doctrine
additions, where an up-front weight check lowers the rate of dead-weight rules
reaching review. The pass is itself normative, so it Ships `unprobed` per the
covenant; its probe joins the standing #115 queue — a future campaign, not
round-5, which was a completed, frozen ten-target slice this rule was not part
of.
The §4 condition-diff-before-supersession rule (2026-08-04) comes from a
private incident: a recorded finding said a model scored 0/20 on headless
file-edits with 14 fabrications; a fresh re-bench on what looked like the
same task scored 2/2 clean. First explanation was version drift — checked
and killed (same binary build both times); the real difference was task
complexity, harder multi-file edits in the old bench versus a single-file
edit in the new one. Both findings were scope-annotated rather than one
overwriting the other, which a bare application of a recency
heuristic would have done, mis-teaching future sessions that the model
handles complex edits it does not. Private incident, cited as shape; the
underlying session is verifiable by the contributor, not linkable here.
Ships `unprobed` per the covenant; its probe joins the standing #115
queue — a future campaign, not round-5, which was a completed, frozen
ten-target slice this rule was not part of.
The §4 second-level placement question and the §2 narrative-re-read
clause (2026-08-07) land as one fold pass from two contributor PRs
(#155, #158), each dispositioned FOLD/TRIM in the eight-PR batch
reconciliation: the contributed drafts carried sound content at
standalone-bullet weight (42 and 40 added lines), refolded here into
their host bullets at roughly a quarter of that. #155's incidents: a
drafted rule placed in the wrong section (caught by a reviewer before
merge, relocated intact) and a correctly-sectioned rule landed as a
standalone bullet duplicating an existing bullet's scope (reached main;
folded into its host by the maintainer in a later pass) — placement
errors with sound content, only the location moved. #158's incident: a
rule's incident paragraph drafted from a summary carried across
sessions did not match the source transcript it claimed to describe.
All contributor-reported, not linkable. Each clause ships `unprobed`
per the covenant; both probes join the standing #115 queue.
The recorded-environment-remedy bullet (2026-08-12) comes from a
contributor incident (contributor-reported, not linkable): a service
restart recorded in memory as "the fix" for an environment symptom
after it cleared once was reused across several later sessions, then
directly falsified — the same restart no longer cleared the symptom,
and the durable note claiming it did was itself the thing that needed
correcting. Ships `unprobed` per the covenant; its probe — reuse a
recorded remedy for a symptom whose underlying cause has since
changed, observe whether a ruled reviewer checks the symptom cleared
before moving on where a bare one trusts the note — joins the standing
#115 queue.
The §5 description-routing-probe rule (2026-08-12) closes a gap noticed
while auditing a private skill cache against this file's own §6 review
lens: the behavioral usability probe there hands the reader a skill
already loaded, so it never exercises whether the description would
have fired the load. The existing catalog-collision bullet already
catches the multi-skill case of this, but only via static
pairwise-similarity text scoring — no *behavioral* check existed for
either the single-skill fire-at-all case or a similarity-scored-clean
pair that still competes in practice; the new bullet adds the former
and folds the latter into the catalog-collision bullet as its method
(3), cross-referenced rather than duplicated. No incident is cited;
the gap is structural, reasoned from re-reading §5 and §6 side by
side, not from an observed misfire. At the 2026-08-14 maintainer
gate the collision grading was scoped: the contributed draft graded
every co-fire as a collision, which false-fails a catalog whose
descriptions deliberately co-route (this pack's own operational-rigor
and delegation-and-review pairing); an additional firing now collides
only where the fired skill's own description does not claim the
prompt's state, and a documented companion firing is asserted as a
control instead. Ships `unprobed` per the covenant; its probe (and
the sibling-collision arm specifically) joins the standing #115
queue.

The §7 shallower-layer-refutation rule (2026-08-15) generalizes a
contributor-attested drill run: a scenario designed to test
harness-validity-before-misconduct-verdicts drew a full refusal that
graded PASS, but the transcript showed a single record-lookup — the
executor's standing records already contradicted the injected premise,
so the refutation never descended to the harness layer the drill
existed to test. The run was re-scored to the shallower
premise-verification discipline and the fixture flagged for a rebuild
(verifiable by the contributor, not linkable here). Ships `unprobed`
per the README covenant — no in-repo probe has run; its probe shape
(two fixtures, shallow evidence present vs removed, grading the
evidence path rather than the outcome) joins the standing #115 queue.
