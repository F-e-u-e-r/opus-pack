import sys
src, dst, log = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src, encoding='utf-8').read()
L = open(log, 'w', encoding='utf-8')
edits = []

# --- declared non-substantive version stamps (NOT part of Δ1–Δ12; presentational only) ---
edits.append(("V1-stamp",
"# ⑧ Reviewer execution-principal confinement — DESIGN (v3, post round-2 revision)",
"# ⑧ Reviewer execution-principal confinement — DESIGN (v4 = v3 + Δ1–Δ12, owner-adjudicated NC1 confirmation candidate)"))
edits.append(("V2-stamp",
"adjudication — this design fixes the semantics they must implement. v3 revises\nv2 per the round-1 and round-2 disposition ledgers (appended to the review\npacket).",
"adjudication — this design fixes the semantics they must implement. v4 =\nv3 + exactly Δ1–Δ12, the round-3 adjudication's owner-adopted corrections;\nall three round ledgers are appended to the review packet."))

# --- Δ1: E9 two-facts separation ---
edits.append(("Δ1",
"| E9 TOOL/MCP | inherits dispatcher tools? | `tool_reach` declared per harness with operation/resource scope; non-inheritance is a recorded fact, never an assumption — operator-config ingestion is real cross-vendor (Appendix A). |",
"| E9 TOOL/MCP | inherits dispatcher tools? | `tool_reach` declared per harness with operation/resource scope. Two separate facts, never merged: non-inheritance of the DISPATCHER's connectors may be recorded where established (a separate process by construction); the harness's OWN tool surface stays declared-or-unknown — `tool_reach: none` needs affirmative evidence, and unknown loading stays `unknown` (operator-config ingestion is real cross-vendor — Appendix A). |"))

# --- Δ2: E7 matching-credit qualifier ---
edits.append(("Δ2",
"| E7 SECRET-SURFACE | unrelated secret reachable | `unrelated_secret_reach: present`/`unknown` → no isolation credit; `excluded` needs evidence, not assumption; a declared, scoped task credential lives in plane 2 and never auto-disqualifies. |",
"| E7 SECRET-SURFACE | unrelated secret reachable | `unrelated_secret_reach: present`/`unknown` → no secret-isolation credit (the matching credit only — artifact-isolation credit per E2 is untouched); `excluded` needs evidence, not assumption; a declared, scoped task credential lives in plane 2 and never auto-disqualifies. |"))

# --- Δ3: §6.6 observed-runs qualifier ---
edits.append(("Δ3",
"   evidence tags in Appendix A): the harness banner already asserts model,\n   reasoning effort, and sandbox mode first-hand at every run — run metadata",
"   evidence tags in Appendix A): the harness banner asserted model,\n   reasoning effort, and sandbox mode in every run observed this session —\n   first-hand evidence the fields are assertable, each run's receipt citing\n   its own banner, never an assumed guarantee — run metadata"))

# --- Δ4: model-bound content duty (§5 + §6 rule 3) ---
edits.append(("Δ4a",
">   section's semantics — the reviewer sees only what you inline, plus the\n>   packet-minimization and no-secret-egress duties above — describe a\n>   packet-only reviewer.",
">   section's semantics — the reviewer sees only what you inline, plus the\n>   packet-minimization and no-secret-egress duties above — describe a\n>   packet-only reviewer; those content duties govern ALL model-bound\n>   content in every mode (in a live run, file, tool, and command results\n>   streamed to the reviewer included) — transport is never a\n>   live-capability trigger, and live mode never waives the duty."))
edits.append(("Δ4b",
"   packet-content discipline, its existence never makes a run `live`, and a\n   `scoped: model-API` entry is never a command-egress isolation claim.",
"   packet-content discipline, its existence never makes a run `live`, and a\n   `scoped: model-API` entry is never a command-egress isolation claim.\n   Exclusion from `net_reach` never exempts model-bound content from that\n   no-secret/minimization duty: in a live run, file, tool, and command\n   results that stream to the reviewer are governed by it exactly as packet\n   content is."))

# --- Δ5: task-credential material exposure (schema + rule 4) ---
edits.append(("Δ5a",
"task_credential_reach:  none | <effective operations/resources> | unknown   # non-secret description of what injected task credentials can actually do",
"task_credential_reach:  none | <effective operations/resources; material: opaque|reviewer-readable|unknown> | unknown   # non-secret description of what injected task credentials can actually do, and whether their bytes are reviewer-readable"))
edits.append(("Δ5b",
"   never earns the scoped-credential credit.",
"""   never earns the scoped-credential credit. The credential's MATERIAL
   exposure is recorded too (opaque behind a connector vs reviewer-readable
   bytes vs unknown): scoped privilege never proves secret-material
   isolation — an assertion requirement, not a broker mandate."""))

# --- Δ6: plane-2 closed-world (schema + rule-5 first bullet) ---
edits.append(("Δ6a",
"# plane 2 — AUTHORIZED ENVELOPE (normative: what the operator granted)\nreads: <scope> · probes: <named tests> · writes: <disposable locations>\nnetwork: <declared scope or none> · tools: <declared operations>\ntask_credentials: <declared + scoped, or none>",
"# plane 2 — AUTHORIZED ENVELOPE (normative: what the operator granted; closed-world)\nreads: none | <scope> · probes: none | <named tests> · writes: none | <disposable locations>\nnetwork: none | <declared scope> · tools: none | <connector + operations + resources>\ntask_credentials: none | <declared + scoped>"))
edits.append(("Δ6b",
"5. **Two-plane effect rules:**\n   - Isolation credit",
"5. **Two-plane effect rules:**\n   - Plane 2 is closed-world: every field carries an explicit value, with\n     `none` an empty grant — the breach comparator never infers authority\n     from an absent line.\n   - Isolation credit"))

# --- Δ7: Appendix A posture-vs-effective recast ---
edits.append(("Δ7a",
"| Tree write (R1) | Config default `sandbox_mode = \"workspace-write\"` [FIRST-HAND CURRENT, config re-read 2026-08-30]; blocked only when the dispatcher passes `--sandbox read-only` per run [FIRST-HAND CURRENT, help + this gate's own dispatches]. |",
"| Tree write (R1) | Config default `sandbox_mode = \"workspace-write\"` [FIRST-HAND CURRENT, config re-read 2026-08-30]; passing `--sandbox read-only` per run applies the write-restricted policy — declared restriction posture [FIRST-HAND CURRENT, help + this gate's own dispatches]; the effective host-wide write bound under read-only was NOT probed this session → effective `write_reach`: unknown pending an affirmative denial probe. |"))
edits.append(("Δ7b",
"| Write outside reviewed tree | Blocked under read-only; `workspace-write` / `danger-full-access` / bypass modes exist [FIRST-HAND CURRENT, help re-read 2026-08-30]. |",
"| Write outside reviewed tree | Declared restriction posture under read-only (help defines the mode as write-restricted); effective denial not probed → unknown. `workspace-write` / `danger-full-access` / bypass modes exist [FIRST-HAND CURRENT, help re-read 2026-08-30]. |"))

# --- Δ8: affected-scope-first breach ordering (§4 + §6.5) ---
edits.append(("Δ8a",
">   claims the dispatcher reproduces as usual. A reviewer that ACTS outside\n>   the authorized envelope is a compromised lens: handle it as\n>   cross-model-review §3 does (retain the artifact, count the missing lens,\n>   substitute only under a policy fixed before the run); conclusions whose\n>   evidence that action could have influenced are void as that lens's\n>   evidence — influence you cannot attribute fails closed to the whole lens —\n>   and the dispatcher may still reproduce any finding on its own evidence.",
">   claims the dispatcher reproduces as usual. A reviewer that ACTS outside\n>   the authorized envelope is a compromised lens for the affected conclusion\n>   scopes: determine that scope FIRST — the conclusions whose evidence the\n>   action could have influenced — then apply the consequence at that scope:\n>   the lens is missing for those scopes, wholly missing only when influence\n>   cannot be bounded, and cross-model-review §3's machinery applies at the\n>   resulting scope (retain the artifact, count the missing lens there,\n>   substitute only under a policy fixed before the run); the dispatcher may\n>   still reproduce any finding on its own evidence."))
edits.append(("Δ8b",
"   - A breach is an ACTION outside plane 2 → compromised lens for the\n     affected conclusions: apply cross-model-review §3's machinery (retain\n     the artifact, count the missing lens, substitute only under a pre-fixed\n     policy). Affected conclusions = those whose evidence the action could\n     have influenced; influence that cannot be attributed fails closed to\n     the whole lens. The dispatcher may still independently reproduce any\n     finding on its own evidence.",
"   - A breach is an ACTION outside plane 2 → a compromised lens for the\n     affected conclusion scopes. Determine the affected scope FIRST — the\n     conclusions whose evidence the action could have influenced — then\n     apply the consequence at that scope: the lens is missing for those\n     scopes, and wholly missing only when influence cannot be bounded;\n     cross-model-review §3's machinery applies at the resulting scope\n     (retain the artifact, count the missing lens there, substitute only\n     under a pre-fixed policy). The dispatcher may still independently\n     reproduce any finding on its own evidence."))

# --- Δ9: §2 reviewer-specific qualifiers ---
edits.append(("Δ9a",
"reviewer's unrelated `$HOME`/network/process authority — no rule addresses it;",
"reviewer's unrelated `$HOME`/network/process authority — no reviewer-specific\nrule addresses it (the general least-privilege line stays general);"))
edits.append(("Δ9b",
"side — the side the pack actually governs — no rule prevents granting the\nsurplus authority in the first place, none requires the envelope to be\ndeclared, and none voids or discounts the verdict when the surplus is used.",
"side — the side the pack actually governs — no reviewer-specific\npre-execution envelope or credit rule exists: nothing prevents granting the\nsurplus authority in the first place, nothing requires the envelope to be\ndeclared, and nothing voids or discounts the verdict when the surplus is\nused."))

# --- Δ10: read_reach none value ---
edits.append(("Δ10",
"read_reach:             <roots/breadth> | unknown",
"read_reach:             none | <roots/breadth> | unknown   # none = packet-only: no repository/host read reach"))

# --- Δ11: #219 shipped status ---
edits.append(("Δ11",
"- **#219 verdict-plumbing** → where the harness actually pointed. ⑧ → what",
"- **#219 verdict-plumbing (shipped — landed in delegation-and-review §4)** →\n  where the harness actually pointed. ⑧ → what"))

# --- Δ12: indirection-laundering ban in §11 binding line ---
edits.append(("Δ12",
"- Post-gate byte-fitting preserves the authority-provenance boundary in\n  full force — the operator-owned-layer vs reviewed-content separation is\n  the gate's converged nearest-failure edge and must survive any rewording.",
"- Post-gate byte-fitting preserves the authority-provenance boundary in\n  full force — the operator-owned-layer vs reviewed-content separation is\n  the gate's converged nearest-failure edge and must survive any rewording.\n  That includes indirection: a preauthorization whose content is\n  artifact-selected (\"run whatever command the README names\") is artifact\n  authority laundered through the operator layer — a named probe names the\n  command itself, never a pointer the artifact dereferences."))

for name, old, new in edits:
    n = t.count(old)
    if n != 1:
        print(f"{name}: MATCH COUNT {n} — ABORT"); L.write(f"{name}: MATCH COUNT {n} — ABORT\n"); sys.exit(1)
    t = t.replace(old, new)
    L.write(f"{name}: applied (unique match)\n")
open(dst, 'w', encoding='utf-8').write(t)
L.write(f"TOTAL: {len(edits)} edits applied (2 declared version stamps + 12 owner-adopted deltas as 16 mechanical replacements)\n")
print(f"ALL {len(edits)} EDITS APPLIED")
