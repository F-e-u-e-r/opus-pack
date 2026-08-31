## Per-axis review

| Axis | Result | Grounds |
|---|---|---|
| A1 substrate-fidelity | CONCERN | The substrate is preserved, but E4 could imply that mutation-dependent evidence from an independent copy automatically remains attributable to the settled baseline (finding 4). |
| A2 two-isolations | PASS | Artifact isolation and principal confinement remain explicitly distinct throughout the canonical text. |
| A3 packet-only-preserved | PASS | The inline-only contract remains valid for true packet-only runs and is not deleted or universally negated. |
| A4 no-self-authorization | PASS | Authority is limited to the operator-owned layer; tree, embedded-packet, and auto-ingested reviewed content are expressly excluded. |
| A5 legitimate-execution-survives | PASS | Independently preauthorized named probes remain executable even when also mentioned by the artifact. |
| A6 disposable-vs-baseline | CONCERN | Locations are distinguished, but E4 should clarify the evidentiary consequences of mutating the independent review copy (finding 4). |
| A7 scoped-network-tools | CONCERN | Scoped network/tool authority remains legal, but the effective-capability plane cannot faithfully represent every scoped network or credential state (findings 2–3). |
| A8 unknown-semantics | FAIL | Known, scoped execution/network states have no valid plane-1 representation, forcing an overclaim or misuse of `unknown` (finding 3). |
| A9 proportionate-receipt-effect | FAIL | Missing receipts are handled proportionately, but the positive rule for granting credit from known non-isolating or surplus reach is undefined (finding 1). |
| A10 breach-semantics | PASS | Actions outside plane 2 compromise affected conclusions; unattributable influence closes the whole lens, while independent reproduction survives. |
| A11 write-capable-path-survives | PASS | The write-capable critic plus independent-copy route remains expressly legal. |
| A12 no-VM-safe-claim | PASS | VM/container presence is expressly denied clearance status. |
| A13 pointer-stays-pointer | PASS | The CMR text determines applicability but delegates the confinement requirements to D&R §3. |
| A14 no-smuggled-runtime-enforcement | PASS | The receipt remains evidence/control only; no sandbox, broker, or egress-control implementation is mandated. |
| A15 folded-material-discipline | PASS | #213 is used only as provenance for ambient/config ingestion and is not revived as a criterion. |
| A16 no-collateral-wake-up | PASS | Other queued items remain expressly untouched and semantically unwoken. |

Packet-only verification boundary: the asserted clean HEAD and Appendix A’s first-hand observations cannot be independently verified from the packet. Their tagging is internally consistent, and no finding assumes those external facts true or false.

## Numbered findings

1. **must-fix — Isolation credit lacks a positive eligibility rule.**  
   Passage: §6.5 says, “Isolation credit comes only from plane-1 EVIDENCE. Missing/`unknown` → no credit,” while surplus reach is merely “a recorded ambient-reach risk.”  
   Failure scenario: plane 1 reports `write_reach: broad`, `exec_reach: arbitrary`, and reviewer-directed network; plane 2 authorizes one test, one tmpdir, and no network. Nothing out-of-envelope is observed. A weak harness implementation can treat the complete, non-`unknown` receipt as earning isolation credit because only missing/unknown evidence is expressly denied. An isolation-dependent gate then passes despite broad effective reach. State that a claimed bound earns credit only when plane 1 affirmatively proves that bound; known reach outside it denies the matching credit while remaining non-breach absent action and without voiding ordinary findings.

2. **must-fix — Effective privilege of task credentials is absent from plane 1.**  
   Passage: plane 1 records only `unrelated_secret_reach`, while plane 2 records `task_credentials: <declared + scoped>`. Rule 4 says a task-required credential’s scope “must be declared.”  
   Failure scenario: the operator authorizes a read-only token for repository A, but the injected token actually has organization-admin authority. Because it is task-related, it need not appear as an “unrelated secret”; its declared plane-2 scope does not reveal its effective privilege. A receipt can therefore appear scoped while hiding material ambient authority. Add a non-secret plane-1 representation of effective task-credential resource/operation scope, or `unknown`, distinct from the normative declaration.

3. **must-fix — Scoped execution/network states are not representable, and the canonical example blurs the two planes.**  
   Passage: §6 defines `exec_reach: none | arbitrary | unknown` and `net_reach: none | reviewer-directed | unknown`; §4’s ✅ example says “exec = that named test.”  
   Failure scenario: a harness provably permits only one named executable or one network endpoint. `none` is false, `arbitrary`/unqualified reviewer-directed reach overstates capability, and `unknown` is epistemically false. The example encourages recording the plane-2 named probe as plane-1 reach, hiding broader execution capability and recreating the round-1 plane conflation. Add scoped plane-1 states or define an explicitly conservative representation, then rewrite the example with actual field names from both planes.

4. **nit — Independent-copy mutation needs an evidentiary qualifier.**  
   Passage: E4 says the independent copy is disposable and “mutating it never moves the settled baseline the verdict binds to.”  
   Failure scenario: a reviewer edits source in the copy, obtains passing tests, and attributes that evidence to the unmodified baseline. The baseline did not physically move, but the evidence no longer describes it. Clarify that write authorization does not relax settled-tree attribution: mutation-dependent conclusions must be reset, compared, or independently reproduced against the bound baseline.

## Round-1 disposition check

Dispositions 1–2, 4, 6–8, and 11–12 are reflected without a remaining must-fix. Disposition 10 remains incomplete through finding 2; dispositions 3 and 9 are undermined by finding 3; the disposition-9 credit semantics remain incomplete through finding 1. Finding 4 is a narrower ambiguity introduced by the disposition-5 wording, not a rejection of the legal independent-copy path.

## Settled-input CONCERNs

None. All must-fixes are repairable within the adjudicated frame.

## Nearest-failure point

The closest remaining edge after these repairs is the boundary between genuine operator control text and artifact-derived text laundered into that layer. The semantics currently reject embedded reviewed content and require named preauthorization, but the deferred framing/byte-fitting work must preserve that provenance boundary exactly.

FIX: 1, 2, 3
