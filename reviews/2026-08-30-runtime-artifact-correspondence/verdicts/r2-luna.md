All three round-1 issues are resolved:

- Freshness metadata is explicitly limited to a signal, not correspondence.
- Discovery includes in-tree, installed, out-of-tree, and central-cache artifacts.
- Local regeneration names the toolchain/recipe, removes competing artifacts, and verifies the runtime-selected digest.

The wording satisfies all ten rubric axes. It creates an actionable trigger, clearly separates source reading from runtime selection, rejects tree digests and cache metadata as provenance, requires exact artifact binding for builds, permits source-only and directly reviewed artifacts, and keeps activation findings orthogonal.

The L2 boundary is preserved by limiting the step to executable artifacts selected for the candidate and excluding unrelated data/configuration. Operational-rigor §2 remains the sole authority; skill-vetting §1 routes to it without duplicating its criteria. The “recorded as a finding” branch does not weaken fail-closed behavior because §2 explicitly requires failure and the pointer applies that gate before proceeding.

No must-fix wording defects remain.

PROCEED
