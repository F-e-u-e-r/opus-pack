
---

# ROUND-1 DISPOSITION LEDGER (part of the reviewed material)

Round 1 ran two independent reviews of the prior revision; both returned FIX.
Findings below are merged across them without attribution. Every must-fix was
adopted; the design above is the revision. Verify each disposition against the
revised text — re-raise anything unfixed or newly broken by its fix; do not
re-litigate a disposition recorded here unless the revised text still
exhibits the defect.

1. Authority-source provenance (must-fix, both reviews; also both reviews'
   nearest-failure): "authority comes from the dispatch packet / predeclared
   policy / operator grant" did not exclude artifact material embedded in the
   packet or policy-shaped repo text. ADOPTED → §3 spine authority-provenance
   sentence; §4 "operator-owned dispatch layer" definition + third ❌ example.
   Sub-claim REJECTED-WITH-REASON: a grant that answers a reviewer's proposal
   remains legitimate (the granting principal is the operator; what prompted
   the proposal does not taint it) — made explicit in §4.
2. Counterexample overclaimed "zero rule violations" against the existing
   compromised-reviewer clause (B4), and §0 overstated "principal side not at
   all". ADOPTED → §2 step (4)–(5) now walk B4's own trigger terms
   (packet-embedded + acts-instead-of-reviewing) and conclude "no
   pre-execution capability-envelope rule"; §0 reworded to the precise gap.
3. Exec axis could not represent direct process spawn without a shell,
   contradicting the claimed orthogonality. ADOPTED → `exec_reach: none |
   arbitrary | unknown`, arbitrary = shell OR direct process creation (§6
   rule 2).
4. Network field conflated model-serving transport with reviewer-directed
   egress (risk: `scoped: model-API` read as command-egress isolation; or
   every remote packet review classified live). ADOPTED → §6 rule 3
   (`net_reach` = reviewer-directed only; transport excluded and governed by
   CMR §2); §5 live-trigger reworded to reviewer-directed capabilities.
5. Disposable writes under-defined: unrelated host paths not excluded,
   independent-copy status vs "reviewed baseline" ambiguous, `none` write
   posture scope unclear, and the ✅ example said "fs read-only" while
   permitting a scratch tmpdir. ADOPTED → §4 disposable definition (created
   for this review, no unrelated state, discardable; the write-capable
   critic's copy IS such a workspace; the baseline the verdict binds to is
   not); §6 rule 2 `write_reach: none-anywhere` semantics; example corrected
   to "write reach = those two paths".
6. Breach scope operationally undefined ("affected conclusions" had no
   decision rule; B4 machinery not expressly carried). ADOPTED → §6 rule 5:
   affected = conclusions whose evidence the action could have influenced;
   unattributable influence fails closed to whole-lens-missing; retain
   artifact + missing lens + pre-fixed substitution carried verbatim from B4;
   dispatcher's own reproduction always available.
7. E5 contradicted E15 / the legitimate-execution carve-out (an independently
   preauthorized command also mentioned by the artifact). ADOPTED → E5 now
   "without dispatch preauthorization"; §4 + E15: mention is neither
   necessary nor sufficient — the authority's source decides.
8. The CMR pointer coined "nothing else leaves", stronger than the section's
   actual "Nothing secret leaves" duty (risk: transport-existence rejections,
   or a new criterion). ADOPTED → §5 pointer now tracks the section's own
   duties (inline-only + packet-minimization + no-secret-egress).
9. Effective capability vs normative authorization were conflated in one
   "envelope" concept (declaring ambient reach would legitimize it, or an
   authorization-only receipt would hide reach and earn false credit).
   ADOPTED (structural) → §6 two-plane receipt: plane 1 evidence (sole
   source of isolation credit), plane 2 operator-owned authorization (sole
   breach comparator); declaring reach never authorizes it; surplus reach =
   recorded risk, not a breach and not a license.
10. Tool/credential scope not assertable (bare connector names; task-required
   credentials vs unrelated secrets). ADOPTED → §6 rule 4: operations/
   resources required (bare name = unknown-scope); `unrelated_secret_reach`
   defined; task credentials are declared plane-2 members; carve-out viii.
11. The capability-disclosure status-quo cell was tagged historical while
   used as current. ADOPTED + corrected by re-observation: this gate's own
   probe banners record model + reasoning effort + sandbox mode —
   [FIRST-HAND CURRENT 2026-08-30]; E12 row and §6.6 updated (banner already
   asserts part of the receipt).
12. Two Appendix A cells untagged (model-API reach; MCP-config declaration).
   ADOPTED → every cell now tagged; model-API reach = FIRST-HAND CURRENT
   probe round-trips; MCP declaration = FIRST-HAND CURRENT config re-read;
   exec-mode tool loading stays UNKNOWN.

---

# ROUND-2 DISPOSITION LEDGER (part of the reviewed material)

Round 2 ran two independent reviews of revision v2; both returned FIX with
non-overlapping findings; every must-fix was adopted. The design above (v3)
is the revision. Same verification duty as the round-1 ledger.

13. §2 called the counterexample "fully-compliant" and claimed "no written
   rule blocks the act", overclaiming against the pack's general
   external-content principle (excerpt B5) which already forbids a
   pack-bound reviewer executing read content on arrival. ADOPTED → §2
   retitled "dispatch-compliant false clear"; steps (4)/(5) now separate
   the reviewer's conduct violation (B5, where it reaches — with no defined
   credit consequence today, and no reach onto an external harness) from
   the dispatcher-side gap (no grant-prevention, no declaration duty, no
   void/discount semantics); §4 and §8 state the new rule supplements §7,
   never overrides it.
14. §6's banner sentence could be read as effective-capability evidence
   (risk: `sandbox: read-only` translated into `exec_reach: none`).
   ADOPTED → banner = run metadata evidencing the applied sandbox; never by
   itself effective-capability evidence; never translated into
   `exec_reach`/`net_reach`; E12 row aligned.
15. Isolation credit had no positive eligibility rule (only missing/unknown
   was denied — a complete receipt showing broad reach could be misread as
   credit-eligible). ADOPTED → §6 rule 5: credit earned only by plane-1
   evidence AFFIRMATIVELY establishing the claimed bound; known
   out-of-bound reach denies the matching credit (non-breach absent action;
   ordinary findings intact); completeness is never credit.
16. Task credentials had no plane-1 effective-privilege representation (a
   declared read-only token with effective admin authority would be
   invisible). ADOPTED → plane 1 `task_credential_reach` (non-secret
   description of effective operations/resources | unknown); declared-vs-
   effective divergence = surplus reach; declaration alone earns no credit.
17. Provably-scoped exec/network states were unrepresentable (none false,
   arbitrary overstates, unknown epistemically false), and the ✅ example
   recorded a plane-2 authorization as plane-1 reach. ADOPTED →
   `scoped:<bound>` added to `exec_reach`/`net_reach` as an evidence-backed
   technical bound (unprovable → arbitrary/reviewer-directed/unknown, never
   a copied declaration); example rewritten with both planes' field names
   showing legitimate divergence.
18. E4 needed an evidentiary qualifier for copy mutation. ADOPTED → write
   authorization never relaxes verdict attribution; mutation-dependent
   evidence describes the mutated state; conclusions about the bound
   baseline need comparison or reproduction against it.

---

# ROUND-3 DISPOSITION LEDGER (part of the reviewed material)

Round 3 (the original gate's final round) ran two independent reviews of
revision v3; verdicts FIX(3 must-fix + 3 nits) and FIX(5 must-fix). Every
finding was reproduced first-hand and authored into deltas Δ1–Δ12; the
repository owner adjudicated ALL TWELVE ADOPTED, and the design above (v4) is
exactly v3 + Δ1–Δ12 (plus two declared presentational version stamps; see the
embedded delta manifest). Same verification duty as the earlier ledgers.

Δ1 E9 merged two facts (dispatcher-connector non-inheritance vs the harness's
   own tool surface), letting unknown loading read as disabled → E9 now
   separates them; `tool_reach: none` needs affirmative evidence.
Δ2 E7's unqualified "no isolation credit" could revoke artifact-isolation
   credit → now "no secret-isolation credit (matching credit only)".
Δ3 §6.6 claimed banner assertion "at every run" (universal) on observed-run
   evidence → now "every run observed this session"; each run's receipt
   cites its own banner.
Δ4 Live model-bound tool/command output fell between the packet duty and
   `net_reach` → §5 + §6 rule 3 now state the no-secret/minimization duty
   governs ALL model-bound content in every mode; transport still never a
   live-capability trigger.
Δ5 Task-credential MATERIAL exposure was unrepresented → schema records
   material: opaque | reviewer-readable | unknown; scoped privilege never
   proves secret-material isolation (assertion requirement, no broker).
Δ6 Plane 2 was not closed-world (tools lacked resources and `none`) → every
   plane-2 field carries an explicit value, `none` = empty grant; the breach
   comparator never infers authority from an absent line.
Δ7 Appendix A inflated declared read-only posture into effective write
   denial → cells recast as declared restriction posture; effective write
   bound unknown pending an affirmative denial probe.
Δ8 "Count the missing lens" could read whole-lens-always → affected scope is
   determined FIRST; the lens is missing for those scopes, wholly missing
   only when influence cannot be bounded; §3 machinery applies at the
   resulting scope.
Δ9 §2 said "no rule addresses/prevents" despite the general least-privilege
   substrate → qualified to "no reviewer-specific pre-execution envelope or
   credit rule".
Δ10 `read_reach` could not represent packet-only → `none` value added.
Δ11 #219's status was unstated → marked shipped (landed in
   delegation-and-review §4).
Δ12 §11 binding line now excludes indirection laundering: a preauthorization
   whose content is artifact-selected ("run whatever command the README
   names") is artifact authority laundered through the operator layer — a
   named probe names the command itself.
