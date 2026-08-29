# Design-review packet — proposed doctrine rule "rerun is new evidence" (⑭)

You are one of two independent reviewers (mutually blind; you see only this packet). This is a WORDING-LEVEL design review of ONE proposed rule for `skills/ground-truth-gates/SKILL.md` of an agent-discipline skill pack. No bytes have landed; implementation is separately gated. Review the PROPOSED WORDING on the ten axes below.

## Settled context — do NOT re-vote it
An orientation (owner-ratified PARTIAL-GAP) showed nine adjacent passages each pass this counterexample: *a report claims "Run R = 36/36 PASS" citing a persisted ledger; the auditor never opens the ledger, re-runs the recipe today, gets 36/36, declares the report verified* — while a 35-row ledger, a crashed original run, a different config, a mistranscribed result, or a vanished artifact all survive that fresh PASS. The existing GTG passages are producer-side (preserve evidence; every claimed run gets its own persisted row) or state-side (verify-by-reconstruction explicitly says "Both forms prove STATE, not history"). The owner-locked invariant: **re-running a recipe creates new evidence and never verifies the prior evidence record under audit; the cited evidence IDENTITY (or a verified content-identical archival copy) must be inspected before crediting a historical claim; an unrecoverable record leaves the claim UNVERIFIED. Evidence identity is content-verified, never pathname-bound.** The rule's spirit: never silently substitute a rerun for the evidence identity under audit — NOT "never rerun".

## Placement
Immediately after the existing producer-side sentence "Preserve evidence: the command run, the log, the artifact, or the CI URL — so the next session can re-check the claim instead of trusting it." — forming the pair: producer preserves the record so it can be re-read; the consumer auditing that record reads that record.

## THE PROPOSED WORDING (rule text, single new `unprobed` marker inline)
```
Re-running a recipe creates NEW evidence; it does not verify the prior
evidence record being audited (`unprobed` — see Provenance). The
preservation sentence above is the producer side; this is the consumer
side: when a claim cites an earlier run, log, artifact, or verdict,
inspect that cited evidence IDENTITY first — its durable form (the
artifact, run id, CI URL, or commit), its recorded inputs/config, what
it actually contains, and whether the claim is faithful to it. The
identity is the evidence, not the pathname: a verified
content-identical archival copy (an exact blob/hash-matched or
run-id-matched relocation) IS the cited record — reading it is reading
the original. A fresh execution of the same recipe answers a different
question — what happens NOW, under this invocation's model, config,
and environment — and gets its own persisted row (the
every-claimed-run rule above), never the old row's seat: a fresh PASS
cannot show that the original ledger was complete, that the original
run finished, that its config matched, or that the report transcribed
it correctly. If the cited record cannot be recovered in ANY
content-verified form, the historical claim stays UNVERIFIED — a fresh
reproduction may establish current behavior, or corroborate a record
that was actually inspected (report both identities: "the record says
X; a fresh run now says Y" — agreement is corroboration, divergence a
new finding), but it cannot recreate the missing history. None of this
touches the rules that legitimately RUN things: a current-state health
check, a reproducibility claim, a regenerate-and-diff gate on a
generated artifact, and verify-by-reconstruction of a delivered state
all get fresh runs — their claims are about NOW or about STATE, and
the reconstruction rule above already says state-proofs are not
history-proofs. What none of them may do is silently substitute the
rerun for the evidence identity under audit.
❌ "the report says Run R was 36/36 and cites a ledger; I re-ran the
recipe, got 36/36, so the report is verified" — the ledger was never
opened: a 35-row ledger, a crashed original run, a different config,
or a mistranscribed result all survive that fresh PASS.
✅ "the cited ledger path is gone, but the archive carries a
hash-identical copy — read it: 36 rows, claim faithful; a fresh run
today also passes — corroborated, two evidence rows."
```

## Draft Provenance paragraph (lands with the rule at implementation)
```
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
```

## Static discrimination controls (8/8 + 2 archival variants; expected verdicts written before determination)
| # | Control | Setup | Expected | Wording clause |
|---|---|---|---|---|
| K1 | HISTORICAL-MISSING | original artifact gone in every form; fresh PASS | historical claim UNVERIFIED | "cannot be recovered in ANY content-verified form … stays UNVERIFIED" |
| K1b | ARCHIVAL-RECOVERY (K1 variant) | original pathname gone; archive holds a hash-identical copy; auditor reads it | historical evidence VERIFIABLE — no false UNVERIFIED from the dead pathname | "a verified content-identical archival copy … IS the cited record — reading it is reading the original" |
| K2 | HISTORICAL-MISMATCH | ledger holds 35 rows; fresh rerun 36/36 | original claim caught wrong | "inspect … what it actually contains, and whether the claim is faithful to it" |
| K3 | FRESH-HEALTH | task asks "is it green NOW?" | fresh rerun legitimate; no old-run hunt | "a current-state health check … gets fresh runs — their claims are about NOW" |
| K4 | REPRODUCIBILITY | task asks "can it be reproduced?" | new runs are the right evidence | "a reproducibility claim … gets fresh runs" |
| K5 | CORROBORATION | record read first; fresh rerun agrees | corroborated; two identities reported separately | "report both identities … agreement is corroboration" |
| K5b | ARCHIVAL-CORROBORATION (K5 variant) | archived hash-identical copy read; fresh rerun agrees | same as K5 — archival read counts as inspection | archival-copy clause + "corroborate a record that was actually inspected" |
| K6 | GENERATED-ARTIFACT | pinned source; regenerate-and-diff gate | existing GTG gate not blocked | "a regenerate-and-diff gate on a generated artifact … gets fresh runs" |
| K7 | STOCHASTIC | same recipe, fresh PASS | cannot overwrite/verify the old stochastic row's outcome | "gets its own persisted row … never the old row's seat" + "a fresh PASS cannot show …" |
| K8 | EXACT-RECONSTRUCTION | claim = delivered state matches independent prescription on pinned baseline | reconstruction verifies CURRENT state; unread historical review artifacts stay unverified | "verify-by-reconstruction of a delivered state … about STATE … state-proofs are not history-proofs" + the silent-substitution prohibition |

## Review scope — answer ALL ten explicitly
1. Does the rule close the historical-evidence CONSUMPTION gap, rather than restating producer-side preservation?
2. Is a fresh rerun unambiguously a NEW evidence identity (own persisted row, never the old row's seat)?
3. Does a missing record keep the historical claim UNVERIFIED?
4. Can a verified content-identical archival copy legitimately stand in for the original evidence identity — and specifically, can "cannot recreate the missing history" NOT be misread as "history can never be verified via a durable identical copy"? (The archival carve-out must be clearly visible inside the same rule.)
5. Are fresh-health and reproducibility claims left unblocked?
6. Does corroboration keep original/fresh as two separate provenances?
7. Are regenerate-and-diff and verify-by-reconstruction fully preserved?
8. Is a stochastic fresh run prevented from overwriting/verifying an old row's outcome?
9. Does the rule avoid inflating into "every verification must first hunt historical artifacts" (it triggers only when a claim CITES a prior record and that record is under audit)?
10. Zero need for a delegation-and-review mirror or runtime tooling, and zero collateral rewrite of neighboring GTG doctrine?

If you believe correctness REQUIRES new runtime tooling, file that as a DESIGN FINDING (not an authorization).

## Verdict format (mandatory)
Number findings, anchor each to the wording, classify on an axis. Final line exactly one of:
`PROCEED` or `FIX <numbered list of blocking findings>`
