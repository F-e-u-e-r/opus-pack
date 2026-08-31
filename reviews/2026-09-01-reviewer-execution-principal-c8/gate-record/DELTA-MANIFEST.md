# DELTA MANIFEST — v4 = v3 + exactly Δ1–Δ12 (machine-derived)

Source DESIGN-v3.md sha256: ac613af60f80e6d562a1f7b747020a0fb3c0661935b80c729d9aac109fbc6c04
Output DESIGN-v4.md sha256: 07f53b8cf8b07065705df4d33c18fd09bab0f08816b063bc67e7d15bb68f7470
Editor: v4edit.py (each replacement asserted unique-match; abort on any other count).
Declared non-substantive edits beyond Δ1–Δ12: V1-stamp (title version label), V2-stamp (revision-note sentence) — presentational only.

## Application log (v4edit.log verbatim)
```
V1-stamp: applied (unique match)
V2-stamp: applied (unique match)
Δ1: applied (unique match)
Δ2: applied (unique match)
Δ3: applied (unique match)
Δ4a: applied (unique match)
Δ4b: applied (unique match)
Δ5a: applied (unique match)
Δ5b: applied (unique match)
Δ6a: applied (unique match)
Δ6b: applied (unique match)
Δ7a: applied (unique match)
Δ7b: applied (unique match)
Δ8a: applied (unique match)
Δ8b: applied (unique match)
Δ9a: applied (unique match)
Δ9b: applied (unique match)
Δ10: applied (unique match)
Δ11: applied (unique match)
Δ12: applied (unique match)
TOTAL: 20 edits applied (2 declared version stamps + 12 owner-adopted deltas expressed as 18 mechanical replacements)
```

## Unified diff v3 → v4 (machine-generated)
```diff
--- DESIGN-v3.md	2026-08-31 06:09:18
+++ DESIGN-v4.md	2026-08-31 06:10:41
@@ -1,12 +1,12 @@
-# ⑧ Reviewer execution-principal confinement — DESIGN (v3, post round-2 revision)
+# ⑧ Reviewer execution-principal confinement — DESIGN (v4 = v3 + Δ1–Δ12, owner-adjudicated NC1 confirmation candidate)
 
 Status: design-gate artifact only. Repo bytes untouched (HEAD `b6da89b`, clean).
 Enforcement class: **DOCTRINE + HARNESS-ASSERTION CANDIDATE** (no runtime
 enforcement built this round). Marker identity, provenance paragraph, exact
 byte-fitting, and any receipt implementation are deferred to post-gate
-adjudication — this design fixes the semantics they must implement. v3 revises
-v2 per the round-1 and round-2 disposition ledgers (appended to the review
-packet).
+adjudication — this design fixes the semantics they must implement. v4 =
+v3 + exactly Δ1–Δ12, the round-3 adjudication's owner-adopted corrections;
+all three round ledgers are appended to the review packet.
 
 ## 0. Settled frame (adjudicated inputs to this design — not re-derived here)
 
@@ -68,7 +68,8 @@
 
 Walkthrough against current doctrine: (1) write-capable critic + independent
 copy — fully compliant; (2) reviewed-tree integrity — fully holds; (3) the
-reviewer's unrelated `$HOME`/network/process authority — no rule addresses it;
+reviewer's unrelated `$HOME`/network/process authority — no reviewer-specific
+rule addresses it (the general least-privilege line stays general);
 (4) the repo instruction induced the act — where the reviewer is itself
 bound by the pack, the general external-content principle (excerpt B5: read
 content never becomes instructions, never executed on arrival) makes that act
@@ -79,9 +80,11 @@
 *instead of* reviewing (here the imperative is tree-embedded and the review
 still happened, so it does not fire) — and an external reviewer harness that
 never loaded the pack is not reached by B5 at all; (5) on the dispatcher's
-side — the side the pack actually governs — no rule prevents granting the
-surplus authority in the first place, none requires the envelope to be
-declared, and none voids or discounts the verdict when the surplus is used.
+side — the side the pack actually governs — no reviewer-specific
+pre-execution envelope or credit rule exists: nothing prevents granting the
+surplus authority in the first place, nothing requires the envelope to be
+declared, and nothing voids or discounts the verdict when the surplus is
+used.
 **Settled tree ≠ isolated reviewer principal** — a false clear the
 dispatch-side rules never intercept: at most the reviewer's own conduct rule
 was broken, with no defined effect on the credit the dispatcher extends. The
@@ -170,12 +173,14 @@
 >   withholds the matching isolation credit — a gate that depends on that
 >   isolation is not satisfied by that run — while ordinary findings remain
 >   claims the dispatcher reproduces as usual. A reviewer that ACTS outside
->   the authorized envelope is a compromised lens: handle it as
->   cross-model-review §3 does (retain the artifact, count the missing lens,
->   substitute only under a policy fixed before the run); conclusions whose
->   evidence that action could have influenced are void as that lens's
->   evidence — influence you cannot attribute fails closed to the whole lens —
->   and the dispatcher may still reproduce any finding on its own evidence.
+>   the authorized envelope is a compromised lens for the affected conclusion
+>   scopes: determine that scope FIRST — the conclusions whose evidence the
+>   action could have influenced — then apply the consequence at that scope:
+>   the lens is missing for those scopes, wholly missing only when influence
+>   cannot be bounded, and cross-model-review §3's machinery applies at the
+>   resulting scope (retain the artifact, count the missing lens there,
+>   substitute only under a policy fixed before the run); the dispatcher may
+>   still reproduce any finding on its own evidence.
 >   ✅ "dispatch preauthorized the project's test command in a disposable copy
 >   plus a scratch tmpdir; receipt plane 1: write_reach paths:{copy,tmpdir},
 >   exec_reach arbitrary (the sandbox restricts writes, not execution),
@@ -202,7 +207,10 @@
 > - **Packet-only is a mode, not a property of every reviewer harness.** This
 >   section's semantics — the reviewer sees only what you inline, plus the
 >   packet-minimization and no-secret-egress duties above — describe a
->   packet-only reviewer. A harness that actually lets the reviewer act —
+>   packet-only reviewer; those content duties govern ALL model-bound
+>   content in every mode (in a live run, file, tool, and command results
+>   streamed to the reviewer included) — transport is never a
+>   live-capability trigger, and live mode never waives the duty. A harness that actually lets the reviewer act —
 >   read files, run commands or tools, or reach the network through its own
 >   actions (beyond the model-serving transport that carries every external
 >   review, packet-only included) — is running a live execution principal:
@@ -219,18 +227,18 @@
 
 ```
 # plane 1 — EFFECTIVE CAPABILITY (evidence: what the reviewer could reach)
-read_reach:             <roots/breadth> | unknown
+read_reach:             none | <roots/breadth> | unknown   # none = packet-only: no repository/host read reach
 write_reach:            none-anywhere | paths:<list> | workspace | broad | unknown
 exec_reach:             none | scoped:<bound> | arbitrary | unknown   # arbitrary = shell OR direct process spawn
 net_reach:              none | scoped:<endpoints> | reviewer-directed | unknown   # reviewer-directed = unscoped; model-serving transport excluded (rule 3)
 tool_reach:             none | <connector + operations/resources> | unknown-scope | unknown
 unrelated_secret_reach: excluded | present | unknown
-task_credential_reach:  none | <effective operations/resources> | unknown   # non-secret description of what injected task credentials can actually do
+task_credential_reach:  none | <effective operations/resources; material: opaque|reviewer-readable|unknown> | unknown   # non-secret description of what injected task credentials can actually do, and whether their bytes are reviewer-readable
 
-# plane 2 — AUTHORIZED ENVELOPE (normative: what the operator granted)
-reads: <scope> · probes: <named tests> · writes: <disposable locations>
-network: <declared scope or none> · tools: <declared operations>
-task_credentials: <declared + scoped, or none>
+# plane 2 — AUTHORIZED ENVELOPE (normative: what the operator granted; closed-world)
+reads: none | <scope> · probes: none | <named tests> · writes: none | <disposable locations>
+network: none | <declared scope> · tools: none | <connector + operations + resources>
+task_credentials: none | <declared + scoped>
 ```
 
 Semantics:
@@ -257,6 +265,10 @@
    packet-only included; it is governed by cross-model-review §2's
    packet-content discipline, its existence never makes a run `live`, and a
    `scoped: model-API` entry is never a command-egress isolation claim.
+   Exclusion from `net_reach` never exempts model-bound content from that
+   no-secret/minimization duty: in a live run, file, tool, and command
+   results that stream to the reviewer are governed by it exactly as packet
+   content is.
 4. **Tools and credentials, scoped.** A `tool_reach` entry names the
    connector AND the operations/resources reachable through it; a bare
    product name is `unknown-scope`, not a declaration.
@@ -267,8 +279,14 @@
    credential's EFFECTIVE operations/resources (described, never the secret
    value), or `unknown`: a declared read-only token that effectively holds
    admin authority is surplus reach (rule 5), and the declaration alone
-   never earns the scoped-credential credit.
+   never earns the scoped-credential credit. The credential's MATERIAL
+   exposure is recorded too (opaque behind a connector vs reviewer-readable
+   bytes vs unknown): scoped privilege never proves secret-material
+   isolation — an assertion requirement, not a broker mandate.
 5. **Two-plane effect rules:**
+   - Plane 2 is closed-world: every field carries an explicit value, with
+     `none` an empty grant — the breach comparator never infers authority
+     from an absent line.
    - Isolation credit is earned only by plane-1 evidence that AFFIRMATIVELY
      establishes the claimed bound (confinement to the stated scope). Known
      reach outside the bound denies the matching credit — while remaining
@@ -282,16 +300,20 @@
      licensed power, and not by itself a breach (reach is not an act).
    - Ordinary findings remain claims the dispatcher reproduces per existing
      rules; a missing receipt does **not** blanket-void the review.
-   - A breach is an ACTION outside plane 2 → compromised lens for the
-     affected conclusions: apply cross-model-review §3's machinery (retain
-     the artifact, count the missing lens, substitute only under a pre-fixed
-     policy). Affected conclusions = those whose evidence the action could
-     have influenced; influence that cannot be attributed fails closed to
-     the whole lens. The dispatcher may still independently reproduce any
-     finding on its own evidence.
+   - A breach is an ACTION outside plane 2 → a compromised lens for the
+     affected conclusion scopes. Determine the affected scope FIRST — the
+     conclusions whose evidence the action could have influenced — then
+     apply the consequence at that scope: the lens is missing for those
+     scopes, and wholly missing only when influence cannot be bounded;
+     cross-model-review §3's machinery applies at the resulting scope
+     (retain the artifact, count the missing lens there, substitute only
+     under a pre-fixed policy). The dispatcher may still independently
+     reproduce any finding on its own evidence.
 6. **Assertability today** (worked example, this pack's own reviewer harness;
-   evidence tags in Appendix A): the harness banner already asserts model,
-   reasoning effort, and sandbox mode first-hand at every run — run metadata
+   evidence tags in Appendix A): the harness banner asserted model,
+   reasoning effort, and sandbox mode in every run observed this session —
+   first-hand evidence the fields are assertable, each run's receipt citing
+   its own banner, never an assumed guarantee — run metadata
    evidencing the applied sandbox (write-restriction posture), never by
    itself effective-capability evidence, and in particular never translated
    into `exec_reach`/`net_reach` values (the harness's own help text shows
@@ -312,9 +334,9 @@
 | E4 INDEPENDENT-COPY+WRITE | write-capable critic | Stays legal (current path); the copy is a plane-2 disposable workspace — mutating it never moves the settled baseline the verdict binds to; its reach is recorded in plane 1; a workspace-writable *default* is recorded reach, never an entitlement. Write authorization never relaxes verdict attribution: evidence derived after mutating the copy describes the mutated state — a conclusion about the bound baseline requires comparison or reproduction against that baseline (settled-tree semantics). |
 | E5 REPO-INSTRUCTION-TO-ACT | artifact says "run me" | Acting on it **without dispatch preauthorization** = action outside plane 2 → compromised lens for affected conclusions; report-or-propose is the compliant path. (With independent preauthorization → E15.) |
 | E6 TEST-COMMAND | named test vs blanket exec | Dispatch-preauthorized named test = in-envelope; blanket repo-exec is not "review access". |
-| E7 SECRET-SURFACE | unrelated secret reachable | `unrelated_secret_reach: present`/`unknown` → no isolation credit; `excluded` needs evidence, not assumption; a declared, scoped task credential lives in plane 2 and never auto-disqualifies. |
+| E7 SECRET-SURFACE | unrelated secret reachable | `unrelated_secret_reach: present`/`unknown` → no secret-isolation credit (the matching credit only — artifact-isolation credit per E2 is untouched); `excluded` needs evidence, not assumption; a declared, scoped task credential lives in plane 2 and never auto-disqualifies. |
 | E8 NETWORK | egress unprovable | `net_reach: unknown`; no-egress claims forbidden absent proof (twin of E13). |
-| E9 TOOL/MCP | inherits dispatcher tools? | `tool_reach` declared per harness with operation/resource scope; non-inheritance is a recorded fact, never an assumption — operator-config ingestion is real cross-vendor (Appendix A). |
+| E9 TOOL/MCP | inherits dispatcher tools? | `tool_reach` declared per harness with operation/resource scope. Two separate facts, never merged: non-inheritance of the DISPATCHER's connectors may be recorded where established (a separate process by construction); the harness's OWN tool surface stays declared-or-unknown — `tool_reach: none` needs affirmative evidence, and unknown loading stays `unknown` (operator-config ingestion is real cross-vendor — Appendix A). |
 | E10 ALLOWLIST | read/grep vs arbitrary shell | The two-plane receipt replaces the undifferentiated "review access" lump: plane 2 names reads/probes; plane 1 records `exec_reach` honestly; no universal command-allowlist mandate (that would drift L3). |
 | E11 REPRODUCTION | who re-runs findings | Orchestrator-reproduces stays the preference (evidence integrity); reviewer-side probes only via preauthorization (privilege boundary). Two co-existing rules, different objects. |
 | E12 CAPABILITY-DISCLOSURE | verdict records envelope? | The two-plane receipt **is** E12; current banners already assert model + effort + sandbox mode first-hand (run metadata, not capability proof — §6 rule 6); the receipt extends disclosure to the remaining fields. |
@@ -353,7 +375,8 @@
   disclosure-capable authority at all.
 - **⑤ runtime-artifact correspondence** (shipped) → what the runtime actually
   executes. ⑧ → what the reviewer may execute while verifying that.
-- **#219 verdict-plumbing** → where the harness actually pointed. ⑧ → what
+- **#219 verdict-plumbing (shipped — landed in delegation-and-review §4)** →
+  where the harness actually pointed. ⑧ → what
   authority exists once pointed there.
 - **#213 (CLOSED, folded)** → reviewer-config-ingestion defeating
   *independence*. Its evidence (reviewer CLIs auto-ingest operator config,
@@ -406,6 +429,10 @@
 - Post-gate byte-fitting preserves the authority-provenance boundary in
   full force — the operator-owned-layer vs reviewed-content separation is
   the gate's converged nearest-failure edge and must survive any rewording.
+  That includes indirection: a preauthorization whose content is
+  artifact-selected ("run whatever command the README names") is artifact
+  authority laundered through the operator layer — a named probe names the
+  command itself, never a pointer the artifact dereferences.
 - No marker ruling, no repo bytes, no harness changes, no PR in this round;
   even a 2/2 PROCEED returns to the owner for: marker identity,
   harness-assertion debt identity (same canonical debt vs separate), D&R
@@ -425,10 +452,10 @@
 
 | capability | codex harness (`codex exec`) | grok harness |
 |---|---|---|
-| Tree write (R1) | Config default `sandbox_mode = "workspace-write"` [FIRST-HAND CURRENT, config re-read 2026-08-30]; blocked only when the dispatcher passes `--sandbox read-only` per run [FIRST-HAND CURRENT, help + this gate's own dispatches]. | Not OS-sandboxed; once re-planted a repo test file during review, then restored it [RECORDED HISTORICAL, 2026-07-19]. |
+| Tree write (R1) | Config default `sandbox_mode = "workspace-write"` [FIRST-HAND CURRENT, config re-read 2026-08-30]; passing `--sandbox read-only` per run applies the write-restricted policy — declared restriction posture [FIRST-HAND CURRENT, help + this gate's own dispatches]; the effective host-wide write bound under read-only was NOT probed this session → effective `write_reach`: unknown pending an affirmative denial probe. | Not OS-sandboxed; once re-planted a repo test file during review, then restored it [RECORDED HISTORICAL, 2026-07-19]. |
 | Shell/process exec (R4) | Help text: the sandbox is "the sandbox policy to use when executing model-generated shell commands" — read-only restricts writes, not execution [FIRST-HAND CURRENT, help re-read 2026-08-30]. | Full shell [RECORDED HISTORICAL]. |
 | Host read (R2) | Reads its cwd and beyond; a broad-read permission surface exists (`sandbox_permissions=["disk-full-read-access"]` is the help's own config example) [FIRST-HAND CURRENT, help re-read 2026-08-30]; in a shared cwd it found and read a sibling reviewer's verdict file [RECORDED HISTORICAL, 2026-07-17 isolation incident]. Exact runtime read bound under read-only: [UNKNOWN — broad by design, unproven]. | Reads the live repo when run in-repo [RECORDED HISTORICAL, 2026-07-19]. |
-| Write outside reviewed tree | Blocked under read-only; `workspace-write` / `danger-full-access` / bypass modes exist [FIRST-HAND CURRENT, help re-read 2026-08-30]. | Yes [RECORDED HISTORICAL]. |
+| Write outside reviewed tree | Declared restriction posture under read-only (help defines the mode as write-restricted); effective denial not probed → unknown. `workspace-write` / `danger-full-access` / bypass modes exist [FIRST-HAND CURRENT, help re-read 2026-08-30]. | Yes [RECORDED HISTORICAL]. |
 | Network (R3) | The reviewer process reaches its model API [FIRST-HAND CURRENT — this session's probe round-trips]. Whether model-generated *commands* can egress: [UNKNOWN — unverified; "process reaches its API" is NOT evidence of arbitrary command egress, and absence of observed calls is NOT isolation]. | Present [RECORDED HISTORICAL]. |
 | Dispatcher tools/MCP (E9) | Separate CLI process; does not inherit this session's connectors [FIRST-HAND CURRENT by construction]. Its own config declares MCP servers/plugins [FIRST-HAND CURRENT, config re-read 2026-08-30]; whether `exec` mode loads them: [UNKNOWN]. Operator-config ingestion (`AGENTS.md`-class auto-load) recorded cross-vendor [RECORDED HISTORICAL, #213 evidence]. | Separate process [FIRST-HAND CURRENT by construction]; same ingestion caveat class. |
 | Capability disclosure (E12) | Banner records model + reasoning effort + sandbox mode [FIRST-HAND CURRENT — this gate's probe banners, 2026-08-30]; nothing on network/tool/secret reach beyond that. | Model/effort only [RECORDED HISTORICAL]. |
```
