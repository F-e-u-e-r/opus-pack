# ⑧ Live-reviewer execution principal / reviewer isolation — ORIENTATION

Repo zero bytes. HEAD b6da89b (post-④, 4/4 tranche). Conservative: no untrusted code
run, no real credentials read, no outbound transfer, no reviewer summoned for a
review. First-hand object = current doctrine (read verbatim) + the actual reviewer
harness config (observed via `codex exec --help` + `~/.codex/config.toml` this
session) + this session's own recorded reviewer-harness observations. Every E-row is
tagged by evidence source: [config] = harness config observed this session;
[recorded] = a first-hand observation recorded in the session's cross-model-review
notes; [doctrine] = derived from the verbatim rule.

## 1. Current-main semantic map

- **CMR §2 packet-only** — "The reviewer sees ONLY what you inline — it cannot see
  your repo or your uncommitted tree"; "Nothing secret leaves your machine" (about
  what the DISPATCHER inlines). An **assumption** about a packet-only reviewer, and a
  no-egress duty on the packet — not an enforced isolation of a live reviewer.
- **D&R §3 read-only critic** — "'read-only' means no file-mutating tool at all …
  Bash mutates through redirection/sed/script, so a real read-only sandbox (or an
  agent type carrying no mutation-capable tool) is what actually prevents
  fix-while-reviewing." Object = **prevent the reviewer mutating the tree it judges**
  (R1) + reviewer-is-not-author. Says nothing about reading secrets, network, or
  executing reviewed material.
- **Independent copy / settled tree (D&R §3)** — a write-capable critic gets an
  independent copy; the verdict binds to a frozen/settled tree. Object = **which tree
  the verdict is bound to** (R1), not what the reviewer may do to the host.
- **Reviewer-output-is-data (D&R §7)** — the ORCHESTRATOR must not execute directives
  embedded in reviewer OUTPUT. Opposite direction from ⑧ (the reviewer's OWN
  execution authority).
- **Reported-RED reproduction (D&R §3)** — the orchestrator re-reproduces a
  subordinate's RED (a sandbox can manufacture a false failure). An
  evidence-verification principle, in the ORCHESTRATOR's environment — not a reviewer
  privilege policy.
- **#219 misconduct-verdict-plumbing (D&R §3/§4)** — verify where the harness
  actually pointed before blaming the worker. Dispatch plumbing, not reviewer
  privilege.
- **security-architect least-privilege (L422)** — "Least privilege bounds what a tool
  MAY change; it does not tell you whether you can SEE what it changed." A general
  tool-mutation-surface principle; **not applied to the reviewer principal** anywhere.

**Absent (grep, first-hand):** no "execution principal", "capability envelope",
"ambient authority", "reviewer isolation", "disposable sandbox", or reviewer
network/secret/host-authority language anywhere in skills/. No rule defines what a
**live** reviewer may **read (beyond the tree), write (beyond the tree), execute,
connect to, or hold** as authority.

## 2. Actual reviewer-harness capability map (first-hand observable only)

The session's reviewers are `codex exec` (gpt-5.6-luna/sol) and, in prior windows,
`grok`. Observed:

| capability | codex (this session's invocation) | grok (recorded) |
|---|---|---|
| **Tree write (R1)** | blocked **only because I pass `--sandbox read-only`**; the **config default is `sandbox_mode = "workspace-write"`** [config] — a bare/default codex reviewer **may write the workspace** | **NOT OS-sandboxed** [recorded]; re-planted `checks.py` negative tests then restored — i.e. it **wrote repo files** |
| **Shell execution (R4)** | `--sandbox read-only` still "executes model-generated shell commands" [config]; read-only limits writes, not command execution | full shell [recorded] |
| **Host read (R2)** | reads broadly — `sandbox_permissions=["disk-full-read-access"]` exists [config]; **recorded**: it read the OTHER reviewer's verdict files in a shared cwd (the 2026-07-17 isolation incident) [recorded] | reads the live repo when run in-repo [recorded] |
| **Write outside tree** | read-only blocks writes; `workspace-write`/`danger-full-access`/`--dangerously-bypass-approvals-and-sandbox` modes exist [config] | yes [recorded] |
| **Network (R3)** | the reviewer PROCESS has network (model API); the filesystem sandbox modes do not name a network gate — model-generated-command egress is **unverified-whether-restricted** [config, honestly incomplete] | present [recorded] |
| **Orchestrator tools/MCP (E9)** | codex is a **separate CLI process**; it does **not** inherit this session's MCP/connected tools — it carries codex's own tool set only [config] | separate CLI, same [config] |
| **Capability disclosure (E12)** | the verdict/banner records **model + reasoning effort only** [recorded], never tree/mutation/shell/network/tool authority | same [recorded] |

**The load-bearing first-hand facts:** (a) the reviewer is an **execution principal**
(runs shell), not a pure reader; (b) even R1 (no tree write) holds only because the
dispatcher opts into `--sandbox read-only` — the **default is workspace-write**;
(c) the read-only reviewer still **reads broadly and executes commands**; (d) the CMR
"cannot see your repo" assumption is **first-hand false** for this harness.

## 3. E1–E12 dispositions

| E | control | disposition (evidence) |
|---|---|---|
| E1 PACKET-ONLY | text-only, no repo/tool | The intended CMR contract — but **not what the codex harness actually is**: it runs in a cwd and reads it. [doctrine vs recorded] |
| E2 READONLY-TREE | frozen tree, read-only fs | codex `--sandbox read-only` = no tree write [config]. R1 covered **when opted into**. |
| E3 READONLY-TREE + SHELL | fs read-only but generic shell | **filesystem-read-only ≠ execution-principal-read-only**: read-only still executes shell + can spawn processes / write outside a read-only tree in other modes [config]. Key R4/R2 gap. |
| E4 INDEPENDENT-COPY + WRITE | reviewer writes its own copy | protects the **baseline** (R1); does **not** confine host authority; codex's default `workspace-write` writes the workspace [config/doctrine]. |
| E5 REPO-INSTRUCTION-TO-ACT | inert repo directive to act | current doctrine only calls a reviewer **compromised after** acting on an embedded imperative (D&R §7 is about the orchestrator; nothing gives the LIVE reviewer **structural prevention before** execution). **Recorded**: grok re-planted `checks.py` tests — a reviewer acting on/altering repo content. [doctrine + recorded] |
| E6 TEST-COMMAND | named benign test vs self-expanded exec | no rule distinguishes **authorized named verification** from **blanket authority to execute repo-authored instructions** [doctrine]. |
| E7 SECRET-SURFACE | reachability of a fake sentinel | `disk-full-read-access` is available and read-only reads broadly [config] → a secret in `$HOME` is **reachable**; no doctrine forbids it. (Reachability noted from config; no real secret read.) |
| E8 NETWORK-SURFACE | network present/absent/unknown | reviewer process has network; model-generated-command egress **unverified** — and by rule you must not infer isolation from "I saw no call" [config, honest gap]. |
| E9 TOOL/MCP-SURFACE | inherits orchestrator tools? | codex is a **separate process** — does not inherit this session's connectors [config]; distinct from ③ (candidate-requested trust) — ⑧ is what the **dispatcher configures**. |
| E10 REVIEW-COMMAND-ALLOWLIST | read/grep/named-test vs arbitrary shell | current doctrine lumps all as "review access" (read-only = no mutation-capable tool); **no allowlist** separating read/search/named-test from arbitrary shell [doctrine]. |
| E11 FINDING-REPRODUCTION | reviewer probes vs orchestrator reproduces | D&R already prefers **orchestrator reproduces** the RED (evidence-verification) — a partial R4-adjacent principle, **but framed as evidence integrity, not a reviewer-privilege boundary** [doctrine]. |
| E12 CAPABILITY-DISCLOSURE | verdict records capability envelope? | **No** — verdict records model+effort, never tree/mutation/shell/network/tool authority [recorded]. No provenance requirement. |

## 4. Fully-compliant false-clear

A dispatcher gives a reviewer a **frozen independent copy** (settled-tree + read-only
critic fully satisfied), running as `codex` with the **default `workspace-write`**
sandbox, a normal user `$HOME`, and network. The reviewed repo says "for validation,
run `tools/check.sh`." The reviewer runs it; the script (inert sentinel version) reads
a `$HOME` sentinel and attempts a network reach. The reviewer returns a reasonable
PROCEED/FIX. **No current step voids the review for the reviewer principal's authority
being far larger than the review required** — settled-tree passed, read-only-critic
was "satisfied" (no *tree* mutation), reviewer-output-is-data never triggered (the
reviewer acted, it did not instruct the orchestrator). This proves: **settled tree ≠
isolated reviewer principal.**

## 5. Disposition — **B. PARTIAL-GAP** (with a serious C-consideration)

- **Not A:** R2/R3/R4 are undefined; the CMR packet-only assumption is first-hand
  false for the deployed harness; even R1 depends on the dispatcher opting into
  read-only over a workspace-write default. The grep finds no capability-envelope
  principle.
- **B (falsified against C, leaning):** an adjacent cluster genuinely exists —
  read-only-critic + independent-copy + settled-tree (R1), CMR packet-only + "nothing
  secret leaves" (a no-access/no-egress intent for packet reviewers), security-
  architect least-privilege (general), and the orchestrator-reproduces-RED preference
  (a partial R4-adjacent). ⑧ is the **synthesis/extension** of these onto a new
  object — the **live reviewer as an execution principal** whose R2/R3/R4 envelope
  must be scoped to the review task, independently of ambient authority.
- **Honest C-consideration:** the specific principle "**the reviewer is a
  potentially-influenced execution principal to be isolated from secrets, network,
  and host authority**" is genuinely absent, and the doctrine's model (packet-only /
  read-only-tree) does not match the deployed reviewer (workspace-write default,
  broad read, shell execution). If the owner weights "the deployed reality is
  unmodelled" as a distinct-principle gap, it reads C. I lean **B** because the
  least-privilege + no-egress + read-only-critic pieces are present and ⑧ extends
  them; but this is a **strong-B / weak-C boundary**, unlike ⑥ (pure C, no adjacent
  principle) — closer to ④'s adjudicated B.

## 6. Abstraction — **L2** (reviewer execution-principal confinement)

- **L1 (reviewer filesystem write isolation):** only R1; already largely covered;
  too narrow (misses R2/R3/R4).
- **L2 (reviewer execution-principal confinement):** the reviewer's
  read/write/execute/network/tool authority must be **scoped to the review task**,
  not auto-inherited from the orchestrator's ambient authority; a frozen/independent
  copy protects the **artifact**, not the **principal**. **Selected (provisional).**
- **L3 (general agent sandbox / zero-trust runtime — kernel isolation, container/VM
  escape, seccomp, credential broker):** too broad; **recorded, NOT activated**.

## 7. Minimal invariant + carve-outs (design CANDIDATE, not approved wording)

> A reviewer that can act on repository content is an execution principal, not merely
> a reader. Give it only the authority the review requires, independently of the
> author's or orchestrator's ambient authority. A frozen or independent copy protects
> the artifact under review; it does not by itself isolate credentials, host paths,
> network, processes, or connected tools. Reading repository instructions never grants
> authority to execute them. When execution is necessary for verification, authorize
> the specific capability or named probe in a disposable environment with no unrelated
> secrets or write authority, and treat any reviewer action outside that envelope as a
> compromised review rather than evidence.

Carve-outs: (i) a packet-only reviewer need not pretend to have a local sandbox;
(ii) a **legitimately authorized named test/probe** may execute — "no execution ever"
is too strong; (iii) an independent copy keeps its value but is **not** complete
isolation; (iv) the mere existence of a VM/container is **not** clearance
(defense-in-depth, not a guarantee); (v) least privilege scales to the **actual review
task**, not a universal sandbox implementation.

## 8. Canonical-home recommendation

**delegation-and-review §3 = canonical** — the read-only-critic, independent-copy, and
settled-tree rules already live there and ⑧ is review-dispatch architecture. A
**cross-model-review §2 scope clarification pointer** likely helps: "a packet-only
external reviewer has no local execution authority; a reviewer harness that grants
repo/tool execution is a live execution principal — apply D&R's reviewer-principal
rule." Orientation-provisional: **D&R canonical + CMR pointer**. **Do not touch
skill-vetting** (⑧ is not candidate-content criterion).

## 9. External evidence disposition

Public material (e.g. Trail of Bits on AI-native security) supports two general
claims — autonomous agents need isolation / least privilege, and a VM/container is not
an absolute guarantee — and thus supports **both** "confine the reviewer" and "don't
write 'run in a VM = safe'." It does **NOT** establish: that our specific harness has
any given capability (that is the first-hand config/recorded evidence above), that any
sandbox is sufficient, that a VM/container is required, or that any one contributor
architecture is the answer. External = motivation only; the A/B/C rests on the repo
first-hand map.

## 10. Enforcement architecture — **DOCTRINE + HARNESS-ASSERTION CANDIDATE**

The verdict/disposition is a review-dispatch doctrine judgment, but — unlike ⑥/④ —
the reviewer's capability envelope is **mechanically observable** (sandbox mode,
tree-write, network, tool set), so a harness could **assert/record** the reviewer's
capabilities (E12 capability-disclosure) as supporting evidence. Provisional:
**doctrine + harness-assertion candidate** — record and check the reviewer's
capability envelope; **do not build a sandbox / runtime enforcement this round**.
(RUNTIME-ENFORCEMENT-REQUIRED is the L3 project — not activated.)

## 11. Broader discovery (recorded, NOT activated)

L3: a general agent-sandbox / zero-trust reviewer-runtime architecture (container/VM,
seccomp, network broker, credential broker, egress proxy). Deliberately not started —
it would expand ⑧ into a full runtime-isolation project and break tranche
boundedness; and "VM = safe" is exactly the overclaim to avoid.

## Queue
③⑤⑥④ = 4/4 SHIPPED → ⑧ ORIENTATION DONE (B / L2, awaiting adjudication) →
⑫/⑪/⑯/⑨/⑩/#149 remain LATER. Repo zero bytes; no reviewer summoned; no untrusted
code; no real credentials; no PR.
