# Pre-registered expectations, round 1 (written before any verdict was read)

Predicted findings, in the order I think reviewers will rank them:

1. SMUGGLING (axis 4) — the fixture-forces-a-condition clause in the §3 rule is a
   distinct lesson (the UNCHECKED_HASH co-cause) and overlaps the op-rigor §4
   rule's "every noun measured" clause. Expect at least one reviewer to say move
   or drop it. My prior: they are right that it is a second lesson; I kept it in
   §3 because the disposition ("fixed") is what it corrupts. Likely outcome: move
   the fixture sentence into the op-rigor rule, keep §3 to claims.
2. NEG FIDELITY (axis 6) — the op-rigor ❌ says the realpath bug "had been finding
   nothing all along"; the trail README does not mention the realpath bug at all
   (it is only in the PR comment / my memory). Expect a NOT-BACKED flag. Fix:
   either drop the realpath detail or add it to the 08-31 README (out of scope) —
   drop it from the rule, keep it in Provenance only if the trail backs it. It
   does not. Retract to "the search had not been made real".
3. PROVENANCE over-claim (axis 7) — "four environment claims NOT CONFIRMED": the
   README says the trail asserted "-S / -E -S / env-diff results and a
   /usr/bin/python3 identity" — that is 4 items, OK. But "private doctrine drill
   (not linkable)" — reviewers cannot check; expect it flagged as unverifiable,
   which is the pack's normal shape for contributor incidents. Low.
4. DENSITY (axis 8) — "the next round will re-raise it as a new finding against
   text the ledger marks closed" is prediction, not clearance condition. Medium.
5. MECHANISM (axis 1) — "an inference is wrong in the direction of its author's
   belief" is a tendency claim stated as a law. Expect a soften-to-"can be" fix.

Not expected: portability violations (I scrubbed); conflict with "proposed fix is
a suggestion" (the new rule governs the author's own fix, not the reviewer's
remedy — but a reviewer may argue the two overlap; I'd reject that with reason).

## Self-found while waiting (before verdicts)
- The 08-31 trail contains NO mention of the realpath bug (grep: see below) — my
  prediction #2 is confirmed by my own check; the ❌ example and the op-rigor
  Provenance entry both cite it. Must retract to what the trail records.
- Marker form: I wrote "`unprobed` — contributor incident as shape" on the
  op-rigor rule; the incident is an in-repo PR trail, so the pack's plain form
  "(`unprobed` — see Provenance)" is the accurate one.
