# ⑫ design v1 — delegated-authority / contribution-provenance propagation (L2)

Design candidate for owner adjudication. NOT landed; implementation LOCKED.
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
>   bullet adds no second definition). The return report discloses every
>   sub-principal whose judgment materially contributed: its identity/model
>   family, the delegated task, which findings/conclusions it contributed,
>   and — where relevant — which verification actions it performed; a
>   sub-principal's judgment is never presented as the parent's own
>   independent judgment. Deterministic helpers and ordinary tool execution
>   (a parser, grep, a compiler, a test runner, a mechanical transformation)
>   are not delegation merely because another process performs the work: the
>   boundary is whether independent model/agent judgment materially
>   contributed to the conclusion — process depth is not the criterion, on
>   either side (asking another model CLI to transform mechanically is not
>   delegation; asking it to review or decide is, whatever the depth).

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
>   a contributing lens. When a CONTRIBUTING sub-principal surfaces
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
