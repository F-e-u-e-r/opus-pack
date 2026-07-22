# delegation-and-review · references: recurring-sweep ledgers

The lifecycle behind §2's recurring-ledgers field (`unprobed` — see the
skill's Provenance; protocol body placed here per the pack's split
precedent). Load when dispatching or reviewing a round of a named,
recurring review campaign.

**The artifact.** Every recurring campaign keeps ONE durable ledger file
at a concrete repository-relative path, named in every round's packet
(files are state; context is not). First pass: create it at that path
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
  re-check to the judged-against set; it never skips the locus).
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
rejected").

**Two phases, two checks.** Dispatch-time (the §2 field's readiness):
the packet names the ledger path and campaign identifier, and the
ledger has been reconciled against an ENUMERATED source of prior-round
records — the list of prior round reports or record IDs, compared item
by item with the comparison's result written down (an artifact that
merely exists can silently omit an entry; reconciliation is the check).
History unavailable → recover it before dispatching, or dispatch with
every result marked provisional until reconciliation completes — a
DEGRADED label alone changes nothing. Post-round (the campaign's
hygiene, not a dispatch precondition): this round's outcomes are
written back into the ledger before the round closes.
