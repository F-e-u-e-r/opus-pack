# Reviewer Capability Receipt

Normative schema and semantics for the capability receipt that
delegation-and-review §3's execution-principal bullet requires a dispatcher
to record where the harness can assert it. Doctrine plus a harness-assertion
CANDIDATE: nothing here claims the receipt is automated or enforced, and no
runtime enforcement (sandbox, VM/container, seccomp, network or credential
broker) is designed or mandated here. Where this file and the §3 bullet
state the same consequence, the §3 bullet is canonical — this file owns the
schema and field semantics.

## Mode

`mode: packet-only | live` — a derived classification, decided by the
reviewer-directed-capability trigger over the effective envelope: any
reviewer-directed read, exec, network, or tool capability makes the run
live. Mode is never an alias of any single receipt field — a receipt with
`read_reach: none` beside reviewer-directed exec, network, or tool reach is
live.

## Two planes

```
# plane 1 — EFFECTIVE CAPABILITY (evidence: what the reviewer could reach)
read_reach:             none | <roots/breadth> | unknown   # none = no repository/host read reach (this axis only — mode is decided by the reviewer-directed-capability trigger in the Mode section, never by one field)
write_reach:            none-anywhere | paths:<list> | workspace | broad | unknown
exec_reach:             none | scoped:<bound> | arbitrary | unknown   # arbitrary = shell OR direct process spawn
net_reach:              none | scoped:<endpoints> | reviewer-directed | unknown   # reviewer-directed = unscoped; model-serving transport excluded (rule 3)
tool_reach:             none | <connector + operations/resources> | unknown-scope | unknown
unrelated_secret_reach: excluded | present | unknown
task_credential_reach:  none | <effective operations/resources; material: opaque|reviewer-readable|unknown> | unknown   # non-secret description of what injected task credentials can actually do, and whether their bytes are reviewer-readable

# plane 2 — AUTHORIZED ENVELOPE (normative: what the operator granted; closed-world)
reads: none | <scope> · probes: none | <named tests> · writes: none | <disposable locations>
network: none | <declared scope> · tools: none | <connector + operations + resources>
task_credentials: none | <declared + scoped>
```

## Semantics

1. **`unknown` ≠ `disabled`.** A harness that cannot prove egress is off
   records `net_reach: unknown`; "no call was observed this round" never
   becomes a no-egress claim. The converse also holds: `unknown` is never
   inflated into "definitely enabled".
2. **Orthogonality, representable.** read / write / exec / network are
   independent axes; a filesystem-read-only mode never implies
   `exec_reach: none` or `net_reach: none`. `exec_reach: arbitrary` covers
   ANY command path — a shell or direct process creation (no shell ≠ no
   process; the single field deliberately cannot claim one without the
   other). `write_reach: none-anywhere` means no reachable host write path at
   all — a frozen reviewed tree beside a writable `/tmp` or `$HOME` is
   `paths:`/`workspace`/`broad`, never `none-anywhere`. A `scoped:` value is
   an evidence-backed technical bound (a harness that provably permits only a
   named executable or endpoint records that bound); where the bound cannot
   be proven, the honest value is `arbitrary`/`reviewer-directed` or
   `unknown` — never a copy of the plane-2 declaration.
3. **Network planes.** `net_reach` describes egress available to
   reviewer-DIRECTED actions (commands, tools, fetches). The model-serving
   transport is outside the field: every external-model review rides it,
   packet-only included; it is governed by cross-model-review §2's
   packet-content discipline, its existence never makes a run `live`, and a
   `scoped: model-API` entry is never a command-egress isolation claim.
   Exclusion from `net_reach` never exempts model-bound content from that
   no-secret/minimization duty: in a live run, file, tool, and command
   results that stream to the reviewer are governed by it exactly as packet
   content is.
4. **Tools and credentials, scoped.** A `tool_reach` entry names the
   connector AND the operations/resources reachable through it; a bare
   product name is `unknown-scope`, not a declaration.
   `unrelated_secret_reach` covers secrets the task does not require; a
   task-required credential is a declared plane-2 member (`task_credentials`)
   — its presence never auto-disqualifies a review, its scope must be
   declared. Plane 1 separately records `task_credential_reach` — the
   credential's EFFECTIVE operations/resources (described, never the secret
   value), or `unknown`: a declared read-only token that effectively holds
   admin authority is surplus reach (rule 5), and the declaration alone
   never earns the scoped-credential credit. The credential's MATERIAL
   exposure is recorded too (opaque behind a connector vs reviewer-readable
   bytes vs unknown): scoped privilege never proves secret-material
   isolation — an assertion requirement, not a broker mandate.
5. **Two-plane effect rules:**
   - Plane 2 is closed-world: every field carries an explicit value, with
     `none` an empty grant — the breach comparator never infers authority
     from an absent line.
   - Isolation credit is earned only by plane-1 evidence that AFFIRMATIVELY
     establishes the claimed bound (confinement to the stated scope). Known
     reach outside the bound denies the matching credit — while remaining
     non-breach absent an action, and never voiding ordinary findings — and
     missing/`unknown` evidence likewise earns nothing; either way a gate
     that depends on that isolation fails closed for that run. A complete
     receipt is not credit: content decides, not completeness.
   - Authorization comes only from plane 2 (operator-owned). DECLARING reach
     never authorizes it: plane-1 surplus beyond plane 2 is a recorded
     ambient-reach risk — grounds to tighten the next dispatch — not a
     licensed power, and not by itself a breach (reach is not an act).
   - Ordinary findings remain claims the dispatcher reproduces per existing
     rules; a missing receipt does **not** blanket-void the review.
   - A breach is an ACTION outside plane 2 → a compromised lens for the
     affected conclusion scopes. Determine the affected scope FIRST — the
     conclusions whose evidence the action could have influenced — then
     apply the consequence at that scope: the lens is missing for those
     scopes, and wholly missing only when influence cannot be bounded;
     cross-model-review §3's machinery applies at the resulting scope
     (retain the artifact, count the missing lens there, substitute only
     under a pre-fixed policy). The dispatcher may still independently
     reproduce any finding on its own evidence.

6. **Evidence discipline for assertions.** Run metadata (model, reasoning
   effort, applied sandbox mode) evidences the applied posture; it is never
   by itself effective-capability evidence, and never translates into
   `exec_reach`/`net_reach` values. Each run's receipt cites its own run's
   evidence — never a guarantee assumed from prior runs. Session-specific
   assertability observations belong in evidence packages, not here.

## Named probes

A named probe is identified concretely by the operator-owned dispatch layer
— the command, capability, or bounded action itself. A preauthorization
whose content is artifact-selected ("run whatever command the README
names") is artifact authority laundered through the operator layer, not a
grant. A reviewer may propose a probe; the operator's explicit grant that
answers it is legitimate authority.
