## 1. Per-axis table

| Axis | Status | Grounds |
|---|---|---|
| A1 | FAIL | §2 claims “zero rule violations,” contradicting B4’s existing compromised-reviewer/missing-lens handling. |
| A2 | PASS | Artifact isolation and principal confinement are repeatedly and explicitly separated. |
| A3 | CONCERN | The packet-only route is retained, but “nothing else leaves” and API transport are not precisely scoped. |
| A4 | FAIL | “Dispatch packet,” “predeclared policy,” and “operator grant” are not defined as external, content-independent authorization. |
| A5 | CONCERN | Named preauthorized probes survive, but E5’s unqualified wording can reject one. |
| A6 | FAIL | “Never the reviewed baseline” is stated, but unrelated host paths and independent-copy status remain ambiguous. |
| A7 | CONCERN | Required/scoped/declared network access is allowed, but the network field’s scope is unclear. |
| A8 | FAIL | Unknown semantics are correct, but the receipt has no explicit process axis despite claiming four independent axes. |
| A9 | PASS | Missing receipts withhold isolation credit while preserving ordinary findings. |
| A10 | FAIL | “Affected conclusions” is undefined and does not expressly carry forward B4’s full missing-lens procedure. |
| A11 | CONCERN | E4 preserves the independent-copy path, but “reviewed baseline” can be read to prohibit its writes. |
| A12 | PASS | VM/container presence is expressly denied clearance value. |
| A13 | CONCERN | The pointer defers live criteria to D&R §3, but its “nothing else leaves” wording risks adding a criterion. |
| A14 | PASS | The design expressly limits the harness surface to evidence/control, not runtime enforcement. |
| A15 | PASS | #213 is explicitly confined to provenance/evidence and not revived as a criterion. |
| A16 | PASS | §11 explicitly keeps all other queued items untouched. |

## 2. Findings

1. **Severity: must-fix — authorization sources can be populated by reviewed content.**

   Passage (§4): “execution authority comes from the dispatch packet, a predeclared review policy, or the operator's explicit grant.”

   The design never says these must be external control-plane authority, fixed before exposure to reviewed content, and immutable during the run. A weaker executor can treat a README, `AGENTS.md`, or an imperative embedded in the dispatch packet as the “predeclared review policy,” or accept an operator grant issued only after the artifact requests execution. It then runs arbitrary commands or probes while believing the no-self-authorization rule was satisfied.

2. **Severity: must-fix — the motivating counterexample contradicts B4.**

   Passage (§2): “no capability-envelope gate exists, so nothing voids or discounts the review ... a false clear with zero rule violations.”

   B4 already says that acting on embedded imperative text makes the reviewer compromised, requiring retention of the artifact and missing-lens accounting. If the reviewer runs the repo-requested script, the dispatcher cannot describe the result as a clear with “zero rule violations.” The current doctrine may lack a capability-envelope gate, but it still imposes an after-the-fact compromised-lens consequence.

3. **Severity: must-fix — receipt orthogonality is asserted but not representable.**

   Passage (§6 schema): `exec_authority: none | named:<probes> | shell | unknown`; §6.2: “no shell ≠ no process ... four independent axes.”

   There is no process-authority field or rule explaining how direct process creation without a shell is recorded. A harness could report `exec_authority: none` because no shell exists while the reviewer can launch processes directly, or infer “no process” from filesystem read-only status. The receipt must either add a process axis or explicitly define how `exec_authority` covers it.

4. **Severity: must-fix — disposable writes are not clearly separated from unrelated host paths or the independent copy.**

   Passage (§4): “writes only to explicitly authorized disposable locations (never the reviewed baseline).”

   “Disposable” is not defined as excluding unrelated host paths, and the design does not resolve whether the independent copy is the reviewed baseline or an authorized disposable workspace. One executor may permit writes to `$HOME/review-tmp` or a sibling repository because they were declared disposable; another may reject the legal write-capable-critic path because it treats the independent copy as the reviewed baseline. This conflicts with E4 and E14.

5. **Severity: must-fix — breach scope is operationally undefined.**

   Passage (§4/§6.3): “a compromised lens for the affected conclusions ... not a blanket void of every finding.”

   “Affected conclusions” has no decision rule, and the text does not expressly require B4’s retain-artifact, missing-lens, and pre-run substitution handling. After an unauthorized helper reads a secret and influences a verdict, a weaker dispatcher may accept all supposedly unrelated findings or void the entire review. Both outcomes can violate the intended proportionate treatment.

6. **Severity: must-fix — E5 contradicts E15 and the legitimate-execution carve-out.**

   Passages: E5 says “acting on it = out-of-envelope”; E15 says the same helper “preauthorized in dispatch → runs.”

   If a README requests `tools/check.sh` and dispatch independently preauthorizes that exact probe, the run is in-envelope under E6/E15. E5’s unqualified wording can nevertheless label it a breach and discard a legitimate test result, undermining A5.

7. **Severity: must-fix — the packet-only pointer changes the existing egress wording ambiguously.**

   Passage (§5): “the reviewer sees only what you inline, nothing else leaves.”

   B3 says “Nothing secret leaves your machine,” not that literally nothing else leaves. Read strictly, the new sentence creates a stronger packet-egress criterion; read loosely, it is an imprecise paraphrase. A weaker executor could reject packet-only operation because model/API transport exists, or treat the pointer as a new independent CMR criterion.

8. **Severity: must-fix — the network receipt does not distinguish model transport from reviewer-directed egress.**

   Passages (§6.4): “The reviewer process has network (model API)”; “command egress ... [UNKNOWN].” Receipt: `network: disabled | scoped:<declaration> | unknown`.

   The design does not define whether `network` covers the model API transport, commands launched by the reviewer, or both. An executor may record `scoped:model API` and falsely credit arbitrary-command network isolation, or classify every packet-only run as live merely because the model API uses a network connection.

9. **Severity: nit — Appendix A tag scope is not consistently explicit.**

   Passages (Appendix A): “The reviewer process has network (model API)” and “Its own config declares MCP servers/plugins” are untagged, while related command egress and tool loading remain `UNKNOWN`. The present-tense “a broad-read permission surface exists” is also adjacent to a historical tag.

   The packet does not independently establish these observations. Historical Grok events are correctly labeled historical, and explicit unknowns are not inflated, but the post-gate owner should tag these statements or keep them as unverified evidence.

## 3. Concerns against settled inputs

None. The settled L2 abstraction, canonical home split, partial-gap classification, and doctrine-plus-harness-assertion enforcement class are internally usable; the defects are in the design wording and receipt semantics.

## 4. Nearest-failure point

The nearest failure is §4’s authorization-source sentence. Without an explicit external, pre-run control-plane boundary, a weaker executor can treat reviewed imperative text as dispatch authority and execute with ambient capabilities.

FIX: 1, 2, 3, 4, 5, 6, 7, 8
