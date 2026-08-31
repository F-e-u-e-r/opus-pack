# R3 adjudication (FINAL ROUND) — luna FIX(1,2,3)+3 nits, sol FIX(1–5); all re-derived; deltas AUTHORED, NOT APPLIED

Round cap (3) reached: v3 stays the last gate-reviewed revision. Every finding
below was reproduced by first-hand re-derivation against DESIGN v3 + canonical
excerpts; each carries an authored ready-to-apply delta. Status of all deltas:
ADJUDICATED-NOT-APPLIED — owner decides apply-into-implementation vs a narrow
confirmation round.

Identity verified: luna gpt-5.6-luna/max/read-only exit 0 (attempt 2, post
quota reset; probe P11 exact-body PASS), 4.6KB. sol gpt-5.6-sol/max/read-only
exit 0 (attempt 2; probe P12 PASS), 7.9KB. Zero settled-frame concerns, both.

## Must-fix deltas

Δ1 (luna 1 — E9 merges two facts; unknown becomes disabled). REPRODUCED: E9's
  "non-inheritance is a recorded fact" conflates dispatcher-connector
  non-inheritance (establishable by construction) with the harness's OWN tool
  surface (exec-mode loading UNKNOWN). Delta — E9 cell:
  "`tool_reach` declared per harness with operation/resource scope. Two
  separate facts, never merged: non-inheritance of the DISPATCHER's
  connectors may be recorded where established (a separate process by
  construction); the harness's OWN tool surface stays declared-or-unknown —
  `tool_reach: none` needs affirmative evidence, unknown loading stays
  `unknown` (operator-config ingestion is real cross-vendor — Appendix A)."
Δ2 (luna 2 — E7 unqualified credit denial). REPRODUCED: could revoke
  artifact-isolation credit contrary to §6.5 matching-credit + E2. Delta —
  E7: "…→ no SECRET-isolation credit (the matching credit only —
  artifact-isolation credit per E2 untouched); `excluded` needs evidence…"
Δ3 (luna 3 — §6.6 "at every run" universal overclaim). REPRODUCED: evidence
  is observed runs. Delta: "the banner asserted model, reasoning effort, and
  sandbox mode in every run OBSERVED THIS SESSION — first-hand evidence the
  fields are assertable; each run's receipt cites its own banner, never an
  assumed guarantee."
Δ4 (sol 1 — live model-bound tool results fall between B3 duty and
  net_reach). REPRODUCED: a live run's tool/command output streams to the
  reviewer over model transport; v3 ties the no-secret duty to the
  packet-only description and excludes transport from net_reach → a weak
  reading lets sensitive tool output leave "compliantly". Delta — §5: the
  content duties govern ALL model-bound content in every mode (live file/
  tool/command results included); transport is never a live-capability
  trigger, and live mode never waives the duty. §6 rule 3 append: exclusion
  from `net_reach` never exempts model-bound content from the
  no-secret/minimization duty.
Δ5 (sol 2 — task-credential MATERIAL exposure unrepresented). REPRODUCED: a
  reviewer-readable token earns the same credit as an opaque one. Delta —
  schema: `task_credential_reach: none | <effective operations/resources;
  material: opaque|reviewer-readable|unknown> | unknown`; rule 4 append:
  scoped privilege never proves secret-material isolation — an assertion
  requirement, not a broker mandate.
Δ6 (sol 3 — plane 2 not closed-world; tools lack resources + `none`).
  REPRODUCED: "tools: read" leaves resource-B reads adjudicator-dependent.
  Delta — plane 2: "reads: <scope> · probes: none | <named tests> · writes:
  none | <disposable locations> · network: none | <declared scope> · tools:
  none | <connector + operations + resources> · task_credentials: none |
  <declared + scoped>" + rule: plane 2 is closed-world — every field carries
  an explicit value, `none` = empty grant; the breach comparator never
  infers authority from an absent line.
Δ7 (sol 4 — Appendix A inflates posture into effective write denial).
  REPRODUCED against the design's own §6.6 standard: no affirmative denial
  probe was run this session. Delta — tree-write and outside-tree cells
  recast: "Declared restriction posture (help defines read-only as
  write-restricted; flag applied) [FIRST-HAND CURRENT]; effective host-wide
  write bound NOT probed → effective write_reach under read-only: unknown
  pending an affirmative denial probe."
Δ8 (sol 5 — missing-lens vs affected-scope textual conflict). REPRODUCED:
  "count the missing lens" can read as whole-lens-always. Delta — §4/§6.5:
  "…is a compromised lens for the affected conclusion scopes: the lens is
  MISSING for those scopes — wholly missing only when influence cannot be
  bounded — and cross-model-review §3's machinery applies at that scope
  (retain the artifact, count the missing lens there, substitute only under
  a pre-fixed policy)."

## Nit deltas

Δ9 (luna nit — §2 "no rule addresses it" vs least-privilege substrate):
  qualify both spots as "no reviewer-specific pre-execution envelope or
  credit rule".
Δ10 (luna nit — packet-only unrepresentable in read_reach): schema:
  `read_reach: none | <roots/breadth> | unknown` (none = packet-only: no
  repository/host read reach).
Δ11 (luna nit — #219 status): §8 line → "#219 verdict-plumbing (shipped —
  landed in delegation-and-review §4)". Verified against current main this
  session (both plumbing bullets present in repo D&R).
Δ12 (sol nearest-failure, adopted as binding-note candidate): §11
  byte-fitting line gains: a preauthorization whose content is
  artifact-selected ("run whatever command the README names") is artifact
  authority laundered through the operator layer — a named probe names the
  command itself, never a pointer the artifact dereferences.

## Round-3 verdict state

No 2/2 PROCEED within the owner's 3-round cap. Trajectory: R1 FIX(8+6 shared
core), R2 FIX(1)+FIX(3), R3 FIX(3)+FIX(5) — every axis-level FAIL traceable
to text added in the immediately prior revision or to receipt-semantics
completions; zero frame-level objections across all six verdicts; both
reviewers' nearest-failure converged on the authority-provenance boundary in
all rounds where named. All 26 must-fix findings across three rounds
reproduced; none rejected except one scoped sub-claim (R1, recorded).
