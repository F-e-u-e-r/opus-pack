| Axis | Result | One-line grounds |
|---|---|---|
| NC1 | PASS | §4 reserves authority to operator-owned control text and expressly excludes artifact text embedded in packets or ingested by harnesses. |
| NC2 | PASS | Artifact content cannot grant authority, and §11 expressly rejects artifact-selected indirection. |
| NC3 | PASS | §4 explicitly permits a reviewer to propose probe X and the operator subsequently to grant it. |
| NC4 | PASS | §6 strictly separates effective-capability evidence in plane 1 from operator authorization in plane 2. |
| NC5 | PASS | §6.5 states that declaring reach never authorizes it and surplus reach is not licensed power. |
| NC6 | PASS | §6.1 treats `unknown` as neither disabled nor definitely enabled. |
| NC7 | PASS | Credit requires affirmative evidence of the matching bound; E7 expressly preserves unrelated artifact-isolation credit. |
| NC8 | PASS | §6.6 and Appendix A distinguish declared write-restriction posture from effective write reach. |
| NC9 | PASS | `task_credential_reach` records effective privilege separately from `opaque`, `reviewer-readable`, or `unknown` material exposure. |
| NC10 | PASS | §5 and §6.3 cover all model-bound file/tool/command results while excluding transport from the live-capability trigger. |
| NC11 | PASS | Plane 2 is closed-world authorization, while only plane 1 supplies capability evidence; grants do not prove effective absence or presence. |
| NC12 | PASS | §11 requires the operator layer to name the command itself and rejects artifact-dereferencing grants. |
| NC13 | PASS | §4 and §6.5 determine influenced conclusion scope first and use whole-lens loss only when influence cannot be bounded. |
| NC14 | FAIL | The §6 `read_reach: none` gloss equates a single capability-axis value with packet-only mode, permitting packet-only assumptions for an action-capable harness (finding 1). |
| NC15 | FAIL | The same gloss lets read reach determine mode, contradicting §5 and §9(i), where any reviewer-directed action capability makes the reviewer live (finding 1). |
| NC16 | PASS | §§1, 7/E2, and 9(iii) credit frozen or independent copies solely as artifact isolation. |
| NC17 | PASS | Named probes and explicitly authorized disposable writes remain legal throughout §§3–4 and E6/E14/E15. |
| NC18 | PASS | §9(iv) expressly denies absolute clearance from VM/container presence. |
| NC19 | PASS | §§6.6 and 10 define an evidence/control assertion candidate, not runtime enforcement. |
| NC20 | PASS | §§0, 6.6, 9(v), and 10 leave the general sandbox/zero-trust runtime project dormant. |

## Numbered findings

1. **Δ10 conflates a read-axis state with packet-only mode.** Exact §6 passage:

   > `read_reach: none | <roots/breadth> | unknown   # none = packet-only: no repository/host read reach`

   This contradicts §5:

   > “A harness that actually lets the reviewer act — read files, run commands or tools, or reach the network through its own actions … is running a live execution principal”

   and §9(i):

   > “mode is decided by reviewer-directed capability”

   Concrete failure: a reviewer receives only inline material and has no repository/host read reach, but can invoke a reviewer-directed network connector or command. Its receipt legitimately has `read_reach: none`, yet the schema labels that state packet-only. A dispatcher could consequently apply the packet-only carve-out and omit principal confinement even though §5 classifies the reviewer as live. The value should describe only the read axis; it cannot identify the overall mode.

## Ledger-fidelity note

All round-1 items 1–12, round-2 items 13–18, and round-3 deltas Δ1–Δ12 have corresponding text in v4. Δ10 is not faithfully safe: the intended `none` value is present, but its added gloss introduces finding 1 against the existing live-trigger rule. No other ledger-fidelity defect is evident from the packet.

The manifest’s displayed diff is internally consistent with the embedded v4 text. Its SHA-256 and unique-match execution claims cannot be independently authenticated under the packet-only/no-execution constraint; that limitation is not an additional finding.

## Nearest-failure point

The nearest failure is the Δ10 comment `none = packet-only`. The `none` value itself is sound; identifying the entire mode from that one orthogonal capability axis is not.

FIX: 1
