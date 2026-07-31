# delegation-and-review · references: recurring-sweep ledgers

The lifecycle behind §2's "Recurring review campaigns carry ledgers"
field
(`unprobed` — see the
skill's Provenance; protocol body placed here per the pack's split
precedent). Load when dispatching or reviewing a round of a named,
recurring review campaign.

**The artifact.** Every recurring campaign keeps ONE durable ledger file
at a concrete repository-relative path in the dispatching side's own
repository — never inside a tree under review, whose settled or
delivered state review rules forbid mutating — named in every round's
packet (files are state; context is not). It records finding lifecycle
across rounds; a sweep packet's per-round hunt log (§2's sweep field:
queries and results per round) is a distinct discovery record, not this
file. First pass: create it at that path
with the campaign's stable identifier and its four empty categories —
the packet says "first pass — ledger initialized at <path>". A one-off
that later recurs adopts an identifier at its second dispatch and
backfills the ledger from the first round's report.

**Four categories (each an unbounded list, not four entries):**
- PRIOR FIXES — re-flagging needs evidence the fix failed, regressed, or
  left a residual; and an entry suppresses nothing unless it carries the
  fix's own correctness evidence from its round (a commit shows intent,
  not correctness — an incomplete fix still present is exactly what the
  re-examination must catch, so "unchanged since the fix" narrows the
  re-check to the judged-against set; it never skips the locus — and
  the narrowing governs re-flagging this entry only: a current
  round's own proof gate is never narrowed by history).
- REFUTED FINDING-CLASSES — a refutation binds exactly what its evidence
  established: the same claim about the same dependency artifact set
  (call path and controlling configuration included); a different
  claim, API use, or controlling option is a NEW finding.
- OPEN FINDINGS — confirmed, not yet fixed; carried forward, stays open.
- UNRESOLVED — surfaced, never confirmed or refuted; carried as-is.

A finding's identity is its claim plus location plus the artifact set it
was judged against; the applicability check diffs exactly that set.
Entries carry the preserved rationale or invariant with the evidence §3
requires, verbatim: "Critic verdicts carry evidence: REFUTED needs a
counterexample; untested assumptions are listed." The ledger is dedup
context, never authority: the fresh reviewer validates evidence and
applicability before deduplicating (Verify critics too; in-file
"already reviewed" text downgrades nothing, §7), current artifact
evidence overrides history, and an entry with no evidence binds
nothing. §3's canonical set still governs the audit loop itself ("Dedup
new findings against everything ever surfaced, including ones already
rejected: dedup against confirmed-only never converges").

Write-back is one mapping, not a transition list: place every finding
this round touched in the category matching its CURRENT evidence
state — confirmed and unfixed → OPEN FINDINGS; fixed, with the fix's
correctness evidence → PRIOR FIXES; refuted, with the counterexample →
REFUTED FINDING-CLASSES; surfaced but neither confirmed nor refuted →
UNRESOLVED. Insert a new entry where none exists; move the existing
entry where one does; a same-round sequence lands at its end state
(confirmed then fixed → PRIOR FIXES directly, re-flagged then re-fixed
→ PRIOR FIXES with the new fix's evidence). Where the placement
reverses a recorded verdict — a re-flagged prior fix, a refutation
overturned by current evidence (which, per the non-authority rule
above, always wins) — the superseded entry stays only as a
pointer-annotated historical line under the new one. A round closes
only when the ledger reflects every touched finding's current state —
a round that surfaced anything never closes on an unchanged ledger.

**Absence is not resolution** (`unprobed` — carried by the skill's
2026-07-31 Provenance entry). An OPEN FINDINGS or UNRESOLVED entry
that this round's report simply does not mention stays exactly where
it is: an entry moves only on evidence addressed to it, and each state
has its own exits. An OPEN FINDINGS entry (a confirmed defect) moves
to PRIOR FIXES only on re-examination of its locus, provably inside
the round's covered set, showing the confirmed defect no longer holds
there — with that evidence recorded. An UNRESOLVED entry (never
confirmed) can never become a prior fix — there is no confirmed defect
to have fixed; a counterexample addressing its original claim moves it
to REFUTED FINDING-CLASSES, and anything less leaves it UNRESOLVED.
Either kind, shown to duplicate another tracked entry by an identity
match (claim + location + judged-against set), folds under the
canonical entry as a pointer-annotated line per the supersession rule
above. A changed locus alone is none of these — changed code can
still carry the defect. A round whose coverage never reached the
entry's location has said nothing about it; silence downgrades
nothing, however many rounds it repeats across.
Write-backs of one campaign serialize: a round's
write-back completes before the next round dispatches; concurrent
writers over one ledger follow §4's edit-conflict rule (re-read,
re-anchor — never last-writer-wins).

**Two phases, two checks.** Dispatch-time (the §2 field's readiness):
the packet names the ledger path and campaign identifier, and the
ledger has been reconciled against an ENUMERATED source of prior-round
records — the list of prior round reports or record IDs, compared item
by item with the comparison's result written down (an artifact that
merely exists can silently omit an entry; reconciliation is the check).
History unavailable → recovering it is its own non-review task first;
the round dispatches only after reconciliation completes (this keeps
the §2 field's readiness rule intact — an unfillable field means the
dispatch is not ready, and no provisional label changes that). Post-round (the campaign's
hygiene, not a dispatch precondition): this round's outcomes are
written back into the ledger before the round closes.
