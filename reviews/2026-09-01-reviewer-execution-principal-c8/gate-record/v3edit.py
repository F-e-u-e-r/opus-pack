import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
edits = []

edits.append((
"# ⑧ Reviewer execution-principal confinement — DESIGN (v2, post round-1 revision)",
"# ⑧ Reviewer execution-principal confinement — DESIGN (v3, post round-2 revision)"))

edits.append((
"adjudication — this design fixes the semantics they must implement. v2 revises\nv1 per the round-1 disposition ledger (appended to the review packet).",
"adjudication — this design fixes the semantics they must implement. v3 revises\nv2 per the round-1 and round-2 disposition ledgers (appended to the review\npacket)."))

edits.append((
"## 2. Motivating counterexample (fully-compliant false clear)",
"## 2. Motivating counterexample (dispatch-compliant false clear)"))

edits.append((
"""(4) the repo instruction induced the act — the nearest existing concept, the
compromised-reviewer judgment (excerpt B4), on its own terms binds a
*packet-embedded* imperative and triggers on acting *instead of* reviewing:
here the imperative is tree-embedded and the review still happened, so strict
B4 does not fire, and even an extension-by-analogy is a post-hoc lens
judgment, not a pre-execution authority rule (delegation-and-review §7
likewise governs the *orchestrator's* handling of reviewer OUTPUT, not the
reviewer's own conduct); (5) no pre-execution capability-envelope rule
exists, so no written rule blocks the act beforehand, and nothing requires the
reviewer's standing authority surplus to be declared or discounted.
**Settled tree ≠ isolated reviewer principal** — a false clear that no written
rule intercepts before the act, with at most an ambiguous post-hoc lens
discount afterward.""",
"""(4) the repo instruction induced the act — where the reviewer is itself
bound by the pack, the general external-content principle (excerpt B5: read
content never becomes instructions, never executed on arrival) makes that act
a CONDUCT violation by the reviewer; but current doctrine attaches no defined
consequence for the review's credit to that violation — the nearest
conduct-to-credit concept, the compromised-reviewer judgment (excerpt B4), on
its own terms binds a *packet-embedded* imperative and triggers on acting
*instead of* reviewing (here the imperative is tree-embedded and the review
still happened, so it does not fire) — and an external reviewer harness that
never loaded the pack is not reached by B5 at all; (5) on the dispatcher's
side — the side the pack actually governs — no rule prevents granting the
surplus authority in the first place, none requires the envelope to be
declared, and none voids or discounts the verdict when the surplus is used.
**Settled tree ≠ isolated reviewer principal** — a false clear the
dispatch-side rules never intercept: at most the reviewer's own conduct rule
was broken, with no defined effect on the credit the dispatcher extends. The
new rule supplements that conduct principle with the dispatcher-side
envelope, receipt, and credit semantics; it never overrides it."""))

edits.append((
">   preauthorized command stays in-envelope even when the artifact also\n>   mentions it: the authority's source decides, not the command's mention.",
">   preauthorized command stays in-envelope even when the artifact also\n>   mentions it: the authority's source decides, not the command's mention\n>   (the general rule that read content never becomes instructions — §7 —\n>   stays in force for the reviewer's own conduct; this bullet adds the\n>   dispatcher-side envelope and its credit consequences)."))

edits.append((
""">   ✅ "dispatch preauthorized the project's test command in a disposable copy
>   plus a scratch tmpdir; the verdict's receipt: write reach = those two
>   paths, exec = that named test, network unknown — network isolation not
>   credited.\"""",
""">   ✅ "dispatch preauthorized the project's test command in a disposable copy
>   plus a scratch tmpdir; receipt plane 1: write_reach paths:{copy,tmpdir},
>   exec_reach arbitrary (the sandbox restricts writes, not execution),
>   net_reach unknown; plane 2: probes: that named test, writes: those two
>   paths, network: none — the planes legitimately differ, and neither exec
>   nor network isolation is credited.\""""))

edits.append((
"exec_reach:             none | arbitrary | unknown      # arbitrary = shell OR direct process spawn\nnet_reach:              none | reviewer-directed | unknown   # model-serving transport excluded (rule 3)\ntool_reach:             none | <connector + operations/resources> | unknown-scope | unknown\nunrelated_secret_reach: excluded | present | unknown",
"exec_reach:             none | scoped:<bound> | arbitrary | unknown   # arbitrary = shell OR direct process spawn\nnet_reach:              none | scoped:<endpoints> | reviewer-directed | unknown   # reviewer-directed = unscoped; model-serving transport excluded (rule 3)\ntool_reach:             none | <connector + operations/resources> | unknown-scope | unknown\nunrelated_secret_reach: excluded | present | unknown\ntask_credential_reach:  none | <effective operations/resources> | unknown   # non-secret description of what injected task credentials can actually do"))

edits.append((
"   `paths:`/`workspace`/`broad`, never `none-anywhere`.",
"""   `paths:`/`workspace`/`broad`, never `none-anywhere`. A `scoped:` value is
   an evidence-backed technical bound (a harness that provably permits only a
   named executable or endpoint records that bound); where the bound cannot
   be proven, the honest value is `arbitrary`/`reviewer-directed` or
   `unknown` — never a copy of the plane-2 declaration."""))

edits.append((
"   — its presence never auto-disqualifies a review, its scope must be\n   declared.",
"""   — its presence never auto-disqualifies a review, its scope must be
   declared. Plane 1 separately records `task_credential_reach` — the
   credential's EFFECTIVE operations/resources (described, never the secret
   value), or `unknown`: a declared read-only token that effectively holds
   admin authority is surplus reach (rule 5), and the declaration alone
   never earns the scoped-credential credit."""))

edits.append((
"   - Isolation credit comes only from plane-1 EVIDENCE. Missing/`unknown` →\n     no credit; a gate that depends on that isolation fails closed for that\n     run.",
"""   - Isolation credit is earned only by plane-1 evidence that AFFIRMATIVELY
     establishes the claimed bound (confinement to the stated scope). Known
     reach outside the bound denies the matching credit — while remaining
     non-breach absent an action, and never voiding ordinary findings — and
     missing/`unknown` evidence likewise earns nothing; either way a gate
     that depends on that isolation fails closed for that run. A complete
     receipt is not credit: content decides, not completeness."""))

edits.append((
"   evidence tags in Appendix A): the harness banner already asserts model,\n   reasoning effort, and sandbox mode first-hand at every run — part of both\n   planes' write/exec posture; the dispatcher's own flags and cwd are\n   dispatcher-recorded;",
"""   evidence tags in Appendix A): the harness banner already asserts model,
   reasoning effort, and sandbox mode first-hand at every run — run metadata
   evidencing the applied sandbox (write-restriction posture), never by
   itself effective-capability evidence, and in particular never translated
   into `exec_reach`/`net_reach` values (the harness's own help text shows
   read-only still executes commands); the dispatcher's own flags and cwd are
   dispatcher-recorded;"""))

edits.append((
"a workspace-writable *default* is recorded reach, never an entitlement. |",
"a workspace-writable *default* is recorded reach, never an entitlement. Write authorization never relaxes verdict attribution: evidence derived after mutating the copy describes the mutated state — a conclusion about the bound baseline requires comparison or reproduction against that baseline (settled-tree semantics). |"))

edits.append((
"current banners already assert model + effort + sandbox mode first-hand — the receipt extends this to the remaining fields. |",
"current banners already assert model + effort + sandbox mode first-hand (run metadata, not capability proof — §6 rule 6); the receipt extends disclosure to the remaining fields. |"))

edits.append((
"  into expanding its own authority. Opposite directions on the same channel.",
"""  into expanding its own authority. Opposite directions on the same channel.
  §7's general never-execute-on-arrival principle already forbids that
  conduct for pack-bound agents; ⑧ supplements it with the dispatcher-side
  envelope, receipt, and credit semantics — what stays undefined today when
  the conduct rule is broken or out of reach (an external harness)."""))

edits.append((
"- No marker ruling, no repo bytes, no harness changes, no PR in this round;",
"""- Post-gate byte-fitting preserves the authority-provenance boundary in
  full force — the operator-owned-layer vs reviewed-content separation is
  the gate's converged nearest-failure edge and must survive any rewording.
- No marker ruling, no repo bytes, no harness changes, no PR in this round;"""))

for i,(old,new) in enumerate(edits,1):
    n = t.count(old)
    if n != 1:
        print(f"EDIT {i}: MATCH COUNT {n} — ABORT"); sys.exit(1)
    t = t.replace(old,new)
open(p,'w',encoding='utf-8').write(t)
print(f"ALL {len(edits)} EDITS APPLIED")
