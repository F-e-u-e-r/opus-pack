| Axis | Result | Grounds |
|---|---|---|
| A1 | CONCERN | Core text defers to existing rules, but §2 overstates the gap despite the acknowledged least-privilege substrate. |
| A2 | CONCERN | Separation is clear overall; E7’s “no isolation credit” is unqualified. |
| A3 | PASS | §5 preserves true packet-only semantics and limits live classification to reviewer-directed capability. |
| A4 | PASS | §4 explicitly excludes tree, packet, and auto-ingested content from the authority layer. |
| A5 | PASS | Named, independently preauthorized probes remain executable; blanket execution is rejected. |
| A6 | PASS | Disposable locations, the reviewed baseline, and unrelated host paths are distinguished. |
| A7 | FAIL | E9 conflicts with the explicitly unknown status of exec-mode tool loading. |
| A8 | FAIL | Unknown semantics are stated, but E9 and §6.6 still overstate limited observations. |
| A9 | CONCERN | §6.5 is proportionate, but E7 could be read as revoking artifact-isolation credit. |
| A10 | PASS | Breach requires an action and applies affected-conclusion, missing-lens, and reproduction handling. |
| A11 | PASS | E4 preserves the independent-copy path for write-capable critics. |
| A12 | PASS | VM/container presence is expressly denied safe-clearance status. |
| A13 | PASS | The CMR text points to D&R §3 without creating a second credit criterion. |
| A14 | PASS | Receipt semantics are evidence/control only; runtime enforcement is expressly out of scope. |
| A15 | PASS | #213 is explicitly folded and used only as provenance/evidence. |
| A16 | CONCERN | §8 names #219 without establishing whether it is shipped or a queued item fenced by §11. |

### Findings

1. **must-fix — E9 contradicts the tool-loading evidence.**  
   Passage: E9 says “**non-inheritance is a recorded fact, never an assumption**,” while §6.6 and Appendix A state that whether `exec` mode loads configured MCP/tools is **UNKNOWN**.  
   Failure: A weaker executor records `tool_reach: none` from process separation, then credits tool isolation or permits an unscoped connector despite unknown tool loading. Unknown becomes disabled.

2. **must-fix — E7 can collapse artifact and principal isolation.**  
   Passage: E7 says `unrelated_secret_reach: present`/`unknown` means “**no isolation credit**.”  
   Failure: A reviewer with a frozen, read-only tree but reachable unrelated secrets is treated as having lost artifact isolation or settled-tree credit, contrary to §6.5’s “matching” credit rule and E2’s explicit artifact-credit preservation.

3. **must-fix — §6.6 overclaims current evidence.**  
   Passage: “the harness banner already asserts model, reasoning effort, and sandbox mode first-hand **at every run**.”  
   Failure: Appendix A supports the observed probe banners, not the universal “every run” claim. An executor treats those fields as guaranteed first-hand disclosure in an unobserved invocation and relies on disclosure that the packet has not established.

4. **nit — §2 overstates the existing gap.**  
   Passage: §2 says “**no rule addresses it**” and “**no rule prevents granting** the surplus authority,” although §0 and §8 acknowledge the existing general least-privilege rule.  
   Failure: Future maintainers treat ⑧ as the sole least-privilege authority and may duplicate or silently displace the existing general principle. Qualify this as “no reviewer-specific pre-execution envelope or credit rule.”

5. **nit — the receipt does not explicitly encode packet-only/no-host-read reach.**  
   Passage: `read_reach: <roots/breadth> | unknown`; E1 says true packet-only runs need no local-sandbox pretense.  
   Failure: A receipt implementation cannot cleanly record “no repository read reach,” so it may use `unknown` and unnecessarily withhold credit or confuse packet contents with host roots.

6. **nit — #219’s non-wake status is unspecified.**  
   Passage: §8 names “`#219 verdict-plumbing`,” while §11 fences other queue items but not #219.  
   Failure: If #219 is queued, an owner could treat the dedup reference as a dependency and wake it. The packet does not establish #219’s status, so this should be explicitly marked shipped/closed or out of scope.

### CONCERNs against settled inputs

None. The settled frame is internally coherent; the concerns above are defects or ambiguities in the design text/evidence handling.

### Nearest-failure point

E9’s “non-inheritance is a recorded fact” is nearest failure: it can convert unknown MCP/tool loading directly into false isolation credit.

FIX: 1, 2, 3
