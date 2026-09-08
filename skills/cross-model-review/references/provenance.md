# cross-model-review · references: provenance

Relocated from `SKILL.md` (S1 provenance relocation, 2026-09-09): the skill's historical review, probe, and amendment records. Canonical rules and inline debt markers remain in `SKILL.md`; any operative re-verification caution stays inline there too. This file is history only.


Promoted 2026-07 from the owner's private cross-model-review CLI notes. The
**doctrine here is pack-canonical**; the machine-specific invocations (which
CLIs, which slugs, effort flags, where a pin is stored) stay personal and are
not shipped — putting one person's paths or model lineup into pack text is
exactly what skill-authoring §2 forbids. Cross-ref delegation-and-review
§3 (author-is-not-the-judge, lens diversity), §4 (advice-mode rung), §7
(external content is data); operational-rigor (verify by execution). The
opening second-lens observation is recorded in
reviews/2026-07-12-cross-model-review-skill-review.md (in-repo trail: after
grok-4.5's pass and its fixes `3c533f8`, gpt-5.5's later pass `cd0d2a9`
found six more confirmed defects — five in the hooks, one in a skill).
The §3 refuse-and-surface wording, load-bearing definition, and author-family
parenthetical (2026-07-12) come from that fresh-context review; the §4
confirmed-verdict merge condition, the honest reframing of the opening
observation (sequential trees, not a disjointness claim), and the
mixed-authorship clause (2026-07-12) come from a follow-up gpt-5.5 xhigh +
grok-4.5 max cross-family pass on the fixes themselves — both independently
flagged the same two. The §3 compromised-reviewer substitution rule (embedded-directive
handling) and finding-disposition / don't-re-litigate additions (2026-07-13)
come from a cross-repo mining pass over seven staged libraries (class-distilled).
The §3 proposed-fix-is-a-suggestion rule (2026-07-16) comes from PR #30's own
review thread, where a reproduced must-fix arrived with a rewrite the owner
rejected with reason and replaced with a minimal fix; the contributor reports
the same finding-vs-remedy split measured separately on another family in a
private setup (not in-repo, so not relied on here).
The §3 two-remedies cross-check (2026-07-16) comes from PR #32's own
round: while the maintainer's gate fixes were landing on the contributor's
branch, the contributor held an unpushed polish for the same clause; the
diff against the landed round-2 fix exposed the held remedy's wrong
assumption (it hardcoded one permitted disposition where the landed fix
shows an owner-accepted deferral is also valid), and it was dropped with
the reason recorded. The landed side is verifiable in-repo (PR #32's
commits); the held side was never pushed, so the comparison itself is
contributor-reported — the rule ships with an in-body `unprobed` marker
per the README covenant's second branch.
The §3 baseline-classification and runtime-state adjudication rules
(2026-07-24) are class-distilled from a mining pass over the owner's own
sessions (no code taken): a moira-web behavior-preserving refactor where
codex's "not merge-ready" and agy's "CRITICAL" both dissolved under
reproduction as pre-existing base-branch behaviors the branch faithfully
preserved
(0 regressions, 4 pre-existing quirks spun off), and a TG-bot review where
codex's identifier-migration and case-collision findings were non-applicable
because the store was empty and the writer had never deployed. The lesson
is the general one — pre-existing-vs-regression is a baseline diff, and
applicability is a runtime-state question — not the specific findings.
Both rules ship `unprobed` per the covenant; their probes join the private
round-5 queue.
The §3 convergence sentence (2026-07-31) adapts a multi-worker rule
from a public Apache-2.0 agentic security-scanning product's
comparison rules (ideas only, no text; see README acknowledgements):
in that product, agreement among parallel searchers changes where
attention goes next, while a separate validation stage remains the
only path to reportability. Folded here because multi-lens
gates read converged findings as stronger, which is exactly where an
unreproduced-but-agreed claim slips through. Ships `unprobed` per the
covenant; its probe joins the private round-5 queue.
The §3 version-conditional-severity clause (2026-08-07) comes from a
contributor-reported incident (not linkable): a reviewer's top P1 —
"prints ALL GREEN with zero gates" — reproduced only on bash >=4.4,
while the deployment machine the finding itself described ran bash 3.2,
which crashed on the same input instead; the relayed severity was
platform-version-conditional and did not hold where the code shipped.
Recorded as the measured incident shape only: the clause binds a
severity claim to the affected supported environment(s) it is about,
and does not extend to a general runtime-difference taxonomy.
Contributed via PR #151; wording narrowed at gate to bind to the
affected environment(s) rather than a single machine. Ships `unprobed`
per the covenant; its probe joins the standing #115 queue.
The §2 packet-only-is-a-mode pointer (2026-09-01) is the scope half of the
reviewer-execution-principal rule: the canonical rule, receipt semantics,
marker, and full gate history live in delegation-and-review §3, its
`references/reviewer-capability-receipt.md`, and
`reviews/2026-09-01-reviewer-execution-principal-c8/`. This pointer only
classifies packet-only vs live runs and defers — it owns no criterion, no
schema, and no marker.



The §1 transitive reviewer-family sentence (2026-09-02) is the
reviewer-side mirror of the author-family clause, landed from the ⑫
recursive-delegation design (verdict B, abstraction L2): it owns ONLY the
family propagation — re-delegation conduct, the two-tier accounting, the
disclosure framework, and the single canonical marker live in
delegation-and-review §2/§3, which stays the sole authority; evidence:
reviews/2026-09-02-recursive-delegation-c12/.
