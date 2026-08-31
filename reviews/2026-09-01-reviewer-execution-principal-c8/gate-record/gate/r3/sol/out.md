### Per-axis review

| Axis | Rating | Grounds |
|---|---|---|
| A1 substrate-fidelity | FAIL | Most substrate is correctly cross-referenced, but §5/§6 do not unambiguously carry B3’s no-secret model-transport duty into live-review tool results, and task-credential material exposure is unrepresented (findings 1–2). |
| A2 two-isolations | PASS | Artifact isolation and reviewer-principal confinement remain consistently distinct. |
| A3 packet-only-preserved | CONCERN | The inline-only mode remains intact, but §5’s grouping of security duties with packet-only semantics creates the live-mode ambiguity in finding 1. |
| A4 no-self-authorization | PASS | Authority is tied to the operator-owned layer; tree, quoted packet material, and harness-ingested content are expressly excluded. |
| A5 legitimate-execution-survives | PASS | Independently dispatch-preauthorized named probes remain executable despite artifact mention. |
| A6 disposable-vs-baseline | PASS | Disposable locations are defined, unrelated state excluded, and E4 preserves baseline attribution after copy mutation. |
| A7 scoped-network-tools | FAIL | Network scope is representable, but plane 2 cannot losslessly express connector/resource-scoped tool authorization (finding 3). |
| A8 unknown-semantics | FAIL | The normative rules handle `unknown` correctly, but Appendix A asserts effective write denial from help/banner-level evidence that §6.6 says is insufficient (finding 4). |
| A9 proportionate-receipt-effect | PASS | Missing reach evidence denies only matching isolation credit and dependent gates; ordinary findings survive reproduction. |
| A10 breach-semantics | FAIL | “Count the missing lens” is not expressly scoped to affected conclusions and conflicts with the whole-lens fallback distinction (finding 5). |
| A11 write-capable-path-survives | PASS | The independent-copy route remains expressly legal, including authorized disposable writes. |
| A12 no-VM-safe-claim | PASS | VM/container presence is explicitly denied clearance or guarantee status. |
| A13 pointer-stays-pointer | PASS | The CMR text routes live principals to D&R §3 without defining a competing authorization or credit test. |
| A14 no-smuggled-runtime-enforcement | PASS | The receipt remains an evidence/control surface; no broker, sandbox, VM, or enforcement build is mandated. |
| A15 folded-material-discipline | PASS | #213 ingestion material is used only as provenance/evidence and is expressly not revived. |
| A16 no-collateral-wake-up | PASS | Other queued items are only named as untouched and the design does not depend on changing them. |

### Findings

1. **must-fix — Live model-bound tool results fall between the packet duty and the network receipt.**  
   Passage: §5 says the inline-only semantics “plus the packet-minimization and no-secret-egress duties” describe a packet-only reviewer; §6.3 excludes model-serving transport from `net_reach` and calls it governed by CMR §2’s “packet-content discipline.”  
   Failure scenario: A live external reviewer runs an authorized local probe whose output contains PII or a token. The output necessarily travels to the reviewer over the model-serving transport. A weak harness treats the run as non-packet-only, excludes that transport from `net_reach`, and finds no rule explicitly applying B3’s minimization/no-token duty to live tool results. Sensitive data leaves while the receipt still appears compliant. State expressly that the existing duty governs all model-bound content—including live file, tool, and command results—without making model transport itself a live-capability trigger.

2. **must-fix — The receipt records task-credential privilege but not whether secret material is reachable by the reviewer.**  
   Passage: §6 records `unrelated_secret_reach`, while `task_credential_reach` contains only the credential’s effective operations/resources; rule 4 says a task credential’s presence does not auto-disqualify it.  
   Failure scenario: A correctly scoped read-only token is injected as a reviewer-readable environment variable. The receipt can report `unrelated_secret_reach: excluded` and correctly scoped `task_credential_reach`, whether the token is opaque behind a connector or directly readable and printable. A reviewer-readable token can then leak through output/model transport while earning the same credential credit as an opaque token. Add an evidence state for task-credential material exposure—such as opaque, reviewer-readable, or unknown—and state that scoped privilege does not prove secret-material isolation. This remains an assertion requirement, not a broker mandate.

3. **must-fix — Plane 2 cannot express a closed, resource-scoped tool envelope.**  
   Passage: §6 plane 2 uses `tools: <declared operations>`, while rule 4 requires connector plus operations/resources only for the plane-1 `tool_reach` field. Unlike network and task credentials, tools also lack an explicit `none` form.  
   Failure scenario: The operator intends to authorize a connector’s read operation only for resource A, but plane 2 records merely `tools: read`. A read of resource B can then be treated either as authorized or as a breach, depending on the implementer. Use a form such as `tools: none | <connector + operations/resources>` and define explicit empty-set forms for optional probes/writes/tools so the breach comparator is closed-world.

4. **must-fix — Appendix A inflates sandbox posture into proven effective write denial.**  
   Passage: Appendix A says tree writes are “blocked only when” `--sandbox read-only` is passed and writes outside the tree are “Blocked under read-only,” citing help and gate dispatches. Section 6.6 says banner/applied-sandbox metadata is “never by itself effective-capability evidence.”  
   Failure scenario: A receipt implementer maps a `read-only` banner/help description to `write_reach: none-anywhere`, despite no affirmative denial probe or proven host-wide bound in this packet. That can wrongly earn write-isolation credit even if a writable temporary or host path exists. Recast these cells as declared restriction posture, or supply expressly identified first-hand evidence establishing the effective bound; otherwise the effective value remains unknown.

5. **must-fix — Partial-conclusion breach handling and whole-lens handling are textually unresolved.**  
   Passage: §4 and §6.5 say an out-of-envelope actor is compromised “for the affected conclusions,” but immediately require “count the missing lens”; only afterward does unattributable influence “fail closed to the whole lens.”  
   Failure scenario: An unauthorized benchmark affects only a performance conclusion. One dispatcher follows B4 literally and counts the entire reviewer lens missing; another preserves unrelated conclusions because influence is attributable. Their quorum and clearance outcomes differ. Say explicitly that the lens is missing for the affected conclusion scopes, and that it becomes wholly missing only when influence cannot be bounded.

### Settled-input CONCERNs

None.

### Packet-only verification limit

The claimed clean HEAD/blob identities and first-hand harness observations cannot be independently verified from this packet. I treated B1–B5 as authoritative as instructed; finding 4 concerns only the design’s internal mismatch between its evidence claims and its own proof standard.

### Nearest-failure point

The highest-risk remaining boundary is §4’s distinction between the dispatch’s own control text and artifact text embedded or referenced by it. The named-probe requirement and E6 presently keep it on the safe side; byte-fitting must not permit an indirection such as “run whatever command the README names” to launder artifact-selected execution into an operator grant.

FIX: 1, 2, 3, 4, 5
