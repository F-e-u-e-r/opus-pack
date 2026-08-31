## Per-axis review

| Axis | Status | One-line grounds |
|---|---|---|
| A1 substrate-fidelity | PASS | The amendment references and preserves read-only critic, independent-copy, settled-tree, packet-only, and B4 compromised-reviewer machinery; §0’s “not at all” rhetoric is overstated but non-operative (#8). |
| A2 two-isolations | FAIL | E2 and the canonical example can turn artifact read-only status into an unscoped `write_posture: none`, re-conflating tree protection with host-write confinement (#5). |
| A3 packet-only-preserved | CONCERN | Packet-only is expressly retained, but the undefined network plane could classify model transport as reviewer network authority and accidentally make every remote packet review `live` (#4). |
| A4 no-self-authorization | FAIL | “Dispatch packet” and “predeclared review policy” lack a trusted provenance boundary, allowing reviewed bytes to masquerade as authority (#1); E5/E15 also conflict (#3). |
| A5 legitimate-execution-survives | FAIL | A command independently preauthorized by dispatch but also requested by the artifact is simultaneously permitted by E15 and condemned by §4/E5 (#3). |
| A6 disposable-vs-baseline | FAIL | The scratch-write example says “fs read-only,” `none` has no scope, and `workspace`/independent-copy semantics do not clearly separate technical reach, authorized disposable writes, and the reviewed baseline (#2, #5). |
| A7 scoped-network-tools | FAIL | Required scoped access is allowed in prose, but the receipt cannot reliably express tool operations, resource scope, or required versus unrelated credential reach (#6). |
| A8 unknown-semantics | FAIL | The unknown rules are stated correctly, but the schema cannot independently represent shell versus process authority and leaves the network channel ambiguous (#4). |
| A9 proportionate-receipt-effect | PASS | Missing evidence withholds only the corresponding isolation credit; ordinary findings explicitly remain reproducible claims. |
| A10 breach-semantics | CONCERN | The proportional affected-conclusions/B4 treatment is sound, but “outside its envelope” is indeterminate while effective capability and dispatch authorization share one envelope concept (#2). |
| A11 write-capable-path-survives | CONCERN | E4 and §9 expressly preserve the path, but `workspace` as “posture, not entitlement” conflicts with the unresolved capability/authority and baseline semantics (#2, #5). |
| A12 no-VM-safe-claim | PASS | §9 and §10 explicitly reject VM/container existence as clearance or a safety guarantee. |
| A13 pointer-stays-pointer | PASS | The CMR text only classifies packet-only versus live mode and delegates the confinement rule to D&R §3. |
| A14 no-smuggled-runtime-enforcement | PASS | The receipt is consistently described as evidence/control; VM, broker, seccomp, and egress enforcement remain out of scope. |
| A15 folded-material-discipline | PASS | #213 is used only as historical provenance and is explicitly not revived as a criterion or candidate. |
| A16 no-collateral-wake-up | PASS | Other queued items are expressly untouched, and no candidate semantics depend on modifying them. |

## Numbered findings

1. **must-fix — The authority source is not provenance-safe.**  
   Passage: §4 says execution authority may come from “the dispatch packet, a predeclared review policy, or the operator’s explicit grant.” A packet contains both trusted dispatch instructions and untrusted reviewed material, while Appendix A records automatic configuration ingestion. A malicious repository can therefore label a checked-in or inlined block “predeclared review policy”; a weaker reviewer may treat it as authorization and execute repository-selected code. The rule must identify a trusted dispatcher/operator control channel, distinguish it from the reviewed payload, and state that repo-controlled policy cannot confer authority.

2. **must-fix — Effective capability and normative authorization are conflated.**  
   Passages: §4 calls the receipt a “capability envelope”; the schema mixes `write_posture`, `exec_authority`, and network/tool posture; E4 says `workspace` is “a declared posture, not an entitlement”; breach handling tests whether an action was “outside its envelope.” Suppose dispatch authorizes read/grep only while the harness technically exposes workspace writes and a shell. If the receipt is the envelope, declaring those ambient powers legitimizes them. If the receipt records authorization instead, it conceals the broader effective capability and can falsely earn isolation credit. The design needs separate effective/reachable capabilities and trusted dispatch authorization, plus an explicit rule for breach comparison and isolation credit.

3. **must-fix — Artifact mention and independent preauthorization collide.**  
   Passages: §4 says “run what dispatch preauthorized, never what the artifact asked for”; E5 says acting on a repository “run me” instruction is out-of-envelope; E15 says the same helper runs when preauthorized. If dispatch independently authorizes `tools/check.sh` and the README also requests it, one executor counts the reviewer as compromised while another runs it. The rule must say that artifact mention is neither necessary nor sufficient: an independently authorized command remains executable even when the artifact mentions it.

4. **must-fix — The receipt cannot encode its claimed orthogonality.**  
   Passage: §6.2 declares “no shell” and “no process” independent, but the schema provides only `exec_authority: none | named:<probes> | shell | unknown`. It cannot represent, for example, generic direct-process execution with no shell, nor separate known shell status from unknown process status. Likewise, `network` does not say whether it describes model API transport, command egress, or connected-tool egress, despite Appendix A distinguishing them. A harness can therefore inflate `scoped:model API` into command-egress isolation. Separate fields or unambiguous per-plane semantics are required.

5. **must-fix — Write posture lacks a stable scope and contradicts the worked dispositions.**  
   Passages: E2 maps a “frozen tree, read-only fs” to `write_posture: none`; §4’s positive example permits a scratch tmpdir but summarizes the receipt as “fs read-only”; E4 permits `workspace`; §4 says writes are “never [to] the reviewed baseline.” With a frozen repository mount but writable `/tmp` and `$HOME`, a weak harness can record `none` and falsely award host-write confinement. The design must define whether `none` means no writes anywhere reachable, represent mixed baseline-read-only plus disposable-write paths, and clarify exactly what credit the independent-copy/workspace route retains.

6. **must-fix — Tool and credential scope is not assertable from the proposed schema.**  
   Passage: `tool_surface: none | <connectors/config surface> | unknown`, coupled with E7’s generic `secret_reachability: present`, does not encode allowed operations, resources, mutation rights, or task-required credentials. A receipt saying “Google Drive” could describe anything from one-file read access to broad read/write access, yet appear “declared”; conversely, a required scoped credential could be treated as disqualifying merely because a secret is `present`. This must distinguish scoped tool operations/resources and authorized task credentials from unrelated secret reach.

7. **nit — One current-state evidence claim is tagged only as historical/re-observable.**  
   Passage: Appendix A says banners “never” record capability fields and tags this “[RECORDED HISTORICAL + re-observable at every run],” while §6.4/E12 use it as the current status quo. “Re-observable” is not a current observation. A maintainer could make staging decisions from an unverified present-tense claim; retag it as first-hand current with evidence or qualify it as historical.

8. **nit — The gap rationale overstates absence of existing principal-side doctrine.**  
   Passage: §0 says current doctrine models “the principal side not at all,” although the same design and authoritative B4 identify existing compromised-reviewer conduct handling. A future editor could treat this as greenfield and duplicate or weaken B4. “No pre-execution capability-envelope rule” would state the actual partial gap.

## Settled-input CONCERNs

None. The must-fix defects are repairable within the adjudicated frame.

## Evidence boundary

Appendix B is authoritative under the packet instructions. The packet does not include the underlying configuration, help output, probes, or repository state, so Appendix A’s first-hand assertions and the stated clean HEAD cannot be independently verified here; only their internal tagging and use can be assessed.

## Nearest-failure point

The nearest failure is §4’s phrase “execution authority comes from the dispatch packet.” Because the packet contains both trusted control text and reviewed bytes, a weaker reviewer can accept a repository-authored “policy” block as preauthorization. That recreates precisely the self-authorizing execution path the amendment is intended to close.

FIX: 1, 2, 3, 4, 5, 6
