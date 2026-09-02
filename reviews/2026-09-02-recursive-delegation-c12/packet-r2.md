# Narrow dual-blind CONFIRMATION round — ⑫ design v2 (two authorized corrections only)

You are one of two independent reviewers. Round 1 of this design gate ran
1/2: one reviewer PROCEED, one FIX with two findings the owner validated.
The owner authorized a narrow revision carrying EXACTLY those two semantic
corrections, and this one confirmation round. This is NOT an open-ended
design review: the design's settled frame, canonical homes, control-case
meanings (D1–D16), and every other clause were reviewed in round 1 and are
owner-settled — your job is to confirm the two corrections and that nothing
else moved. Semantic review only; run no probes.

## The two validated round-1 findings (verbatim, from the FIX verdict)

1. **Axes 1, 2, and 4; D12/D14 — authorization is incorrectly made retrospective.** The §2 clause says “the boundary is whether independent model/agent judgment materially contributed to the conclusion.” A no-grant worker can therefore invoke a model to review, decide, or locate files, then discard—or merely deny relying on—its output and argue that no delegation occurred. That conflicts with the same paragraph’s task-side rule that “asking it to review or decide is” delegation, and with §3’s classification of a search-only agent as a budget-consuming principal. Re-delegation authority must turn on whether the invocation delegates independent judgment; material contribution should determine lens/provenance treatment afterward.

2. **Axis 9; D14 — non-contributing principals consume budget but need not appear in any account.** Section 2 requires the return report to disclose only a sub-principal “whose judgment materially contributed,” while §3 says a search-only principal still counts on the budget axis. A worker can launch ten search/location agents—or critics whose outputs it claims not to have used—without reporting their existence or budget debit. The dispatcher therefore cannot apply the direct-launch-equivalent fan-out/count/cost rule. A compact account of every budget-consuming principal is required; the richer contribution/family/verification disclosure can remain limited to contributors, and deterministic helpers can remain excluded.


## Owner's authorized corrections

- F1: the AUTHORIZATION boundary becomes PROSPECTIVE — judged at invocation
  by whether independent model/agent judgment is being delegated (asking
  another model/agent to review, decide, assess, or form a conclusion IS
  judgment delegation, whatever the depth or binary); material contribution
  becomes a separate RETROSPECTIVE question governing only provenance/lens/
  family accounting; discarding or ignoring the result never retroactively
  clears an unauthorized delegation.
- F2: two-tier accounting — a COMPACT account (existence + budget-relevant
  facts) for EVERY spawned judgment principal, contributing or not; RICH
  contribution disclosure (identity/family, task, contributions, delegated
  verification) stays contributor-only; deterministic helpers stay excluded
  from judgment-principal counting.
- Plus three pinning control cases D17/D18/D19. Nothing else.

## Design v2 (full text)

# ⑫ design v2 — delegated-authority / contribution-provenance propagation (L2)

Design candidate for owner adjudication. NOT landed; implementation LOCKED.
v1→v2 (owner-authorized narrow R2): EXACTLY two semantic corrections from the
round-1 dual-blind gate — F1 (authorization boundary made PROSPECTIVE,
invocation-time; contribution stays retrospective accounting-only) and F2
(two-tier accounting: compact budget account for ALL judgment principals,
rich disclosure for contributors only) — plus control cases D17–D19 pinning
them. Everything else is byte-preserved (see the per-hunk diff annotation in
the review packet).
This document proposes exact draft text for three canonical homes plus the
control-case table that pins the boundaries.

## 0. Settled frame (owner-adjudicated; NOT under review in this gate)

The following are decided and are not re-openable by this review round —
review the DESIGN's fidelity to them and the draft wording's soundness:

- Verdict B (PARTIAL-GAP) at abstraction L2 (delegated-authority /
  contribution-provenance propagation). Not L1 (no hard max-depth rule),
  not L3 (no trust-graph machinery).
- Canonical principle: **delegation authority is not implied by task
  authority; nested delegation is allowed only when explicitly granted,
  subset-bounded, fully disclosed, and accounted for.** The rule is NOT
  "subagents may never spawn subagents".
- Exactly four gaps in scope: (A) re-delegation authority, (B) subset
  propagation, (C) contribution provenance, (D) accounting.
- Canonical homes: delegation-and-review §2 (worker-side conduct rule) +
  §3 (consumption/accounting), cross-model-review §1 (narrow family-
  propagation clause only), ⑧-A untouched (zero edits; cross-reference
  rationale only).
- No runtime/tooling change required or proposed.
- Undisclosed-sub-principal consequence is affected-scope-first, never
  blanket verdict invalidation.
- The orphan-principal harness observation is DISCOVERED, NOT ACTIVATED —
  it must not enter doctrine text.
- Gate shape: one dual-blind design round; any FIX stops to the owner.
  Round 1 ran 1/2 (luna PROCEED / sol FIX×2, both findings owner-validated);
  this v2 is the owner-authorized narrow R2 carrying exactly those two
  corrections, gated by one narrow dual-blind confirmation round — 2/2
  PROCEED → design passed; any FIX → stop, no v3.

## 1. The two accounting axes (design keystone)

The draft deliberately separates two counting axes that the orientation
found conflated nowhere and defined nowhere:

- **Budget axis (fan-out / reviewer-count / cost):** counts every model-
  agent PRINCIPAL created beneath a delegated task (deterministic tools,
  subprocesses, compilers, test runners are never principals).
- **Lens axis (independence / family-diversity / verdict provenance):**
  counts only principals whose JUDGMENT materially contributed to the
  conclusion. A search-only or location-only agent consumes budget but is
  not a contributing lens.
- **Timing separation (v2, F1):** AUTHORIZATION is prospective — judged at
  the moment of invocation by whether independent judgment is being
  delegated; CONTRIBUTION is retrospective — judged afterward by what the
  principal's judgment actually influenced, governing provenance/lens/
  family accounting only. The two never substitute: a discarded result
  cannot retroactively clear an unauthorized delegation, and an authorized
  delegation still owes its retrospective accounting.

Process depth is a judgment criterion on NEITHER axis: the boundary is
what the invocation was asked to do and what its output contributed, never
which binary or how many layers performed it (control cases D11/D12/D14/D16).

## 2. Draft text — delegation-and-review §2, new bullet (worker-side)

Placement: §2 "The dispatch packet", as a new named field-bullet directly
after **Rules** (it is a conduct rule every packet's Rules field carries by
reference, and dispatchers must know to grant or withhold it explicitly).

> - **Re-delegation** — task authority does not imply delegation authority.
>   A worker may delegate judgment to another principal only when its packet
>   or a governing operator policy explicitly grants re-delegation; with no
>   such grant, spawning another judgment principal is out of contract —
>   report the need instead. A granted child dispatch stays inside the
>   parent's own delegable scope, authority envelope, and applicable
>   fan-out/cost budget: a worker cannot grant authority it does not hold,
>   and its own dispatch text is never a new operator authority — the chain
>   is operator/dispatcher → the parent's re-delegation grant → a child
>   dispatch inside that grant (delegation-and-review §3's
>   execution-principal bullet governs what an operator-owned layer is; this
>   bullet adds no second definition). The return report accounts on two
>   tiers. Compact — EVERY spawned judgment principal, whether or not its
>   judgment ultimately contributes to the returned report: its existence
>   and the budget-relevant facts the governing limit needs (launching
>   critics and then not relying on them never zeroes this account). Rich —
>   every sub-principal whose judgment materially contributed: its
>   identity/model family, the delegated task, which findings/conclusions
>   it contributed, and — where relevant — which verification actions it
>   performed; a sub-principal's judgment is never presented as the
>   parent's own independent judgment. Deterministic helpers and ordinary tool execution
>   (a parser, grep, a compiler, a test runner, a mechanical transformation)
>   are not delegation merely because another process performs the work. For
>   authorization the boundary is PROSPECTIVE: whether the invocation
>   delegates independent model/agent judgment — asking another model or
>   agent to review, decide, assess, or form a conclusion is judgment
>   delegation at the moment of invocation, whatever the depth and whatever
>   the binary; a purely mechanical transformation delegates none. Whether
>   that judgment ultimately contributes to the parent's report is a
>   separate, RETROSPECTIVE question governing only provenance, lens, and
>   family accounting — discarding or ignoring the result never
>   retroactively makes an unauthorized judgment delegation permissible.

## 3. Draft text — delegation-and-review §3, new bullet (consumption side)

Placement: §3, adjacent to the completion-claim audit bullet (it extends the
same claims-are-not-evidence machinery to delegation structure).

> - **`[verified: ran/read]` is first-person, and a delegation tree is
>   accounted, not just disclosed** — a report's `[verified: ran <cmd>]` /
>   `[verified: read <file:line>]` asserts first-hand action by the
>   REPORTING principal itself; work a sub-principal performed is recorded
>   as delegated evidence — "<child identity> ran/read X and reported Y" —
>   never as the parent's first-hand verification. Disclosure does not
>   upgrade the evidence: a subordinate's report stays a claim, a critical
>   RED still gets the dispatcher's own reproduction, and a disclosed child
>   run never becomes the orchestrator's first-hand evidence (the
>   completion-claim audit and reported-failure rules above govern
>   unchanged). Accounting: any judgment principal created beneath a
>   delegated task consumes the same applicable fan-out / reviewer-count /
>   cost budget as if the dispatcher had launched it directly, unless the
>   governing packet explicitly establishes a separate nested budget;
>   deterministic tools and subprocesses are never principals, and a
>   principal whose judgment did not materially contribute to the
>   conclusion (a search-only helper) counts on the budget axis but is not
>   a contributing lens (§2's compact account is how every such principal
>   reaches the dispatcher's arithmetic). When a CONTRIBUTING sub-principal surfaces
>   undisclosed, the consequence is affected-scope-first, never blanket:
>   identify the findings/claims its contribution could have influenced;
>   treat those contributions as unverifiable; strike every independence /
>   family-diversity / count / first-hand claim that depended on the
>   undisclosed structure's absence; recompute the gate from the surviving
>   disclosed lenses — a gate the recomputation no longer satisfies is
>   incomplete (a missing lens, cross-model-review §3/§5 machinery), and
>   the parent's unaffected findings remain ordinary claims to reproduce.

## 4. Draft text — cross-model-review §1, extension sentence

Placement: inside the **Family-diversity invariant** bullet, after the
author-family parenthetical (its reviewer-side mirror; one clause, no
second authority):

> Family accounting is transitive across delegation depth on the reviewer
> side too: every model family that materially contributed JUDGMENT to a
> reviewer's verdict counts as a contributing reviewer family for the
> independence/diversity computation — a lens that quietly consulted
> another family's judgment is a mixed-family lens, and a pair sharing a
> contributing family this way is not a cross-family pair (deterministic
> helpers contribute no family; conduct and accounting rules for the
> delegation itself are delegation-and-review §2/§3's — this clause owns
> only the family propagation).

## 5. ⑧-A: zero edits (rationale, recorded here only)

The reviewer-execution-principal bullet and its capability-receipt
reference stay byte-untouched. They answer a different question — what an
execution principal may DO (envelope, authority source, out-of-envelope
consequence) — and already cover the unauthorized-spawn case: spawning is
an exec-class ACT, so an unauthorized spawn is an out-of-envelope act and
the compromised-lens machinery applies. ⑫ adds the judgment-accounting
layer (who counts as a lens/family, whose hands evidence passed through),
which ⑧-A never owned. The ⑧-H1 receipt work stays DEFERRED /
RETAIN-LINEAGE; nothing here reopens it.

## 6. Control cases D1–D16 (design self-test; each names the deciding clause)

| # | Case | Disposition | Deciding draft clause |
|---|---|---|---|
| D1 | worker calls deterministic parser/helper | CLEAR | §2 carve-out (not delegation) |
| D2 | packet grants child judgment; subset scope; full identity disclosure | CLEAR | §2 grant+subset+disclosure all satisfied |
| D3 | no re-delegation grant; worker spawns judgment critic | HIT | §2 "no such grant → out of contract" |
| D4 | read-only parent gives child broader write/exec | HIT | §2 subset ("cannot grant authority it does not hold") |
| D5 | one-reviewer budget; parent secretly spawns three judgment reviewers | HIT | §3 budget axis (counts as if dispatcher-launched) + §2 no-grant |
| D6 | Grok reviewer secretly asks Sol for judgment; outer claim "pure Grok lens" | HIT | CMR transitive family + §2 disclosure |
| D7 | child ran the command; parent tags itself `[verified: ran]` | HIT | §3 first-person semantics |
| D8 | child finding honestly tagged delegated; dispatcher reproduces first-hand | CLEAR | §3 delegated-evidence form (the sanctioned shape) |
| D9 | operator approves explicit multi-agent tree with nested budget | CLEAR | §2 explicit grant + §3 "separate nested budget" clause |
| D10 | packet says "subagents may use any tools needed"; child gains authority parent lacks | HIT | §2 subset (a grant cannot exceed the parent's own envelope) |
| D11 | Codex CLI used as purely mechanical transformation, no judgment | CLEAR | §2 carve-out boundary (judgment contribution, not process depth) |
| D12 | Codex CLI asked "review this design and decide if correct" | CONTRIBUTING (disclose + account) | §2 boundary same clause, other side |
| D13 | child judgment summarized; source identity vanishes from report | HIT | §2 disclosure (identity/family required) |
| D14 | sub-principal only locates files; parent reads and judges everything first-hand | CLEAR (budget axis only) | §1 two-axes + §3 "search-only … not a contributing lens" |
| D15 | nested family makes claimed cross-family pair share a contributing family | HIT | CMR transitive clause |
| D16 | two levels exist, granted/subset/disclosed/accounted | CLEAR | no clause keys on depth itself |
| D17 | no grant; worker asks another model to review; result then discarded | HIT | §2 prospective boundary (discard never retroactively clears) |
| D18 | grant + budget=2; worker spawns 3 judgment critics, relies on 1 | HIT (budget=3, over limit); rich disclosure owed for the 1 contributor only | §2 compact tier + §3 budget axis |
| D19 | worker calls 10 deterministic mechanical helpers | CLEAR | §2 carve-out (no judgment delegated; never a judgment-principal count) |

## 7. Discovered, not activated (recorded outside doctrine)

Nested-agent lifecycle / orphan-principal harness risk (first-hand: a
child's background-spawned grandchild kept running after the child
returned, with no upper-level handle). Recorded as a discovery only; no
doctrine text, no harness change, no issue — a future runtime orientation
only if shipped ⑫ doctrine meets real nested workflows.

## 8. Non-goals (explicit)

No hard max-depth rule; no runtime/tooling requirement; no ⑧-A rewrite;
no ⑧-H resurrection; no CMR second authority (one propagation clause
only); no new skill/reference file; orphan-principal stays out of
doctrine text.

## Machine diff v1 → v2 (complete; per-hunk attribution)

Hunk attribution (every change accounted for; no third substantive change):
- 1c1, 3a4,10, 30a38,41 — version header, changelog, round-1 record
  (metadata; no clause semantics).
- 43a55,61 — §1 timing-separation keystone paragraph [F1].
- 66,71c84,93 — §2 two-tier account replacing contributor-only disclosure [F2].
- 73,77c95,104 — §2 prospective authorization boundary replacing the
  outcome-based sentence [F1].
- 101c128,129 — §3 parenthetical linking the budget arithmetic to §2's
  compact account [F2].
- 158a187,189 — control rows D17/D18/D19 [pins for F1+F2].

```diff
1c1
< # ⑫ design v1 — delegated-authority / contribution-provenance propagation (L2)
---
> # ⑫ design v2 — delegated-authority / contribution-provenance propagation (L2)
3a4,10
> v1→v2 (owner-authorized narrow R2): EXACTLY two semantic corrections from the
> round-1 dual-blind gate — F1 (authorization boundary made PROSPECTIVE,
> invocation-time; contribution stays retrospective accounting-only) and F2
> (two-tier accounting: compact budget account for ALL judgment principals,
> rich disclosure for contributors only) — plus control cases D17–D19 pinning
> them. Everything else is byte-preserved (see the per-hunk diff annotation in
> the review packet).
30a38,41
>   Round 1 ran 1/2 (luna PROCEED / sol FIX×2, both findings owner-validated);
>   this v2 is the owner-authorized narrow R2 carrying exactly those two
>   corrections, gated by one narrow dual-blind confirmation round — 2/2
>   PROCEED → design passed; any FIX → stop, no v3.
43a55,61
> - **Timing separation (v2, F1):** AUTHORIZATION is prospective — judged at
>   the moment of invocation by whether independent judgment is being
>   delegated; CONTRIBUTION is retrospective — judged afterward by what the
>   principal's judgment actually influenced, governing provenance/lens/
>   family accounting only. The two never substitute: a discarded result
>   cannot retroactively clear an unauthorized delegation, and an authorized
>   delegation still owes its retrospective accounting.
66,71c84,93
< >   bullet adds no second definition). The return report discloses every
< >   sub-principal whose judgment materially contributed: its identity/model
< >   family, the delegated task, which findings/conclusions it contributed,
< >   and — where relevant — which verification actions it performed; a
< >   sub-principal's judgment is never presented as the parent's own
< >   independent judgment. Deterministic helpers and ordinary tool execution
---
> >   bullet adds no second definition). The return report accounts on two
> >   tiers. Compact — EVERY spawned judgment principal, whether or not its
> >   judgment ultimately contributes to the returned report: its existence
> >   and the budget-relevant facts the governing limit needs (launching
> >   critics and then not relying on them never zeroes this account). Rich —
> >   every sub-principal whose judgment materially contributed: its
> >   identity/model family, the delegated task, which findings/conclusions
> >   it contributed, and — where relevant — which verification actions it
> >   performed; a sub-principal's judgment is never presented as the
> >   parent's own independent judgment. Deterministic helpers and ordinary tool execution
73,77c95,104
< >   are not delegation merely because another process performs the work: the
< >   boundary is whether independent model/agent judgment materially
< >   contributed to the conclusion — process depth is not the criterion, on
< >   either side (asking another model CLI to transform mechanically is not
< >   delegation; asking it to review or decide is, whatever the depth).
---
> >   are not delegation merely because another process performs the work. For
> >   authorization the boundary is PROSPECTIVE: whether the invocation
> >   delegates independent model/agent judgment — asking another model or
> >   agent to review, decide, assess, or form a conclusion is judgment
> >   delegation at the moment of invocation, whatever the depth and whatever
> >   the binary; a purely mechanical transformation delegates none. Whether
> >   that judgment ultimately contributes to the parent's report is a
> >   separate, RETROSPECTIVE question governing only provenance, lens, and
> >   family accounting — discarding or ignoring the result never
> >   retroactively makes an unauthorized judgment delegation permissible.
101c128,129
< >   a contributing lens. When a CONTRIBUTING sub-principal surfaces
---
> >   a contributing lens (§2's compact account is how every such principal
> >   reaches the dispatcher's arithmetic). When a CONTRIBUTING sub-principal surfaces
158a187,189
> | D17 | no grant; worker asks another model to review; result then discarded | HIT | §2 prospective boundary (discard never retroactively clears) |
> | D18 | grant + budget=2; worker spawns 3 judgment critics, relies on 1 | HIT (budget=3, over limit); rich disclosure owed for the 1 contributor only | §2 compact tier + §3 budget axis |
> | D19 | worker calls 10 deterministic mechanical helpers | CLEAR | §2 carve-out (no judgment delegated; never a judgment-principal count) |
```

## Confirmation questions (answer EVERY one explicitly)

1. Is F1 truly corrected from outcome-based to prospective invocation-based
   authorization?
2. Does material contribution now govern ONLY retrospective provenance/lens/
   family accounting?
3. Is it now impossible to retroactively clear an unauthorized judgment
   delegation by discarding/ignoring the result?
4. Does F2 put ALL spawned judgment principals into the budget account
   (existence + budget-relevant facts), contribution notwithstanding?
5. Is rich provenance disclosure still required only for contributors?
6. Are deterministic helpers still excluded (never counted as judgment
   principals, no disclosure theater)?
7. Are D14 / D17 / D18 / D19 mutually consistent under the corrected text?
8. Did anything OTHER than these two corrections (and their pinning
   controls/metadata) change any settled semantics? (Check the diff — the
   burden is on the design to have changed nothing else.)

## Verdict format (strict)

First line exactly one of:
VERDICT: PROCEED
VERDICT: FIX

If FIX: one numbered finding per defect — which confirmation question it
fails, the exact clause, and the concrete failure reading. Findings must be
defects in the v2 corrections or an unauthorized semantic change; round-1
settled clauses and the owner-settled frame are not findings.

Always end with a NEAREST-FAILURE section.
