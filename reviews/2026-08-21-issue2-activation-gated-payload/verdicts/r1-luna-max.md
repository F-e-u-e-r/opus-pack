1. Yes, narrowly. Current §1.5 says trigger-conditioned payloads appear only when behavior executes, but applies only to executable candidates and promised paths. §2 has no activation-gating shape, while exfiltration is limited to the “default (non-example) execution path.” §3 is a fail-closed backstop, not an active hunt instruction. The dormant-exfil fixture demonstrates the gap.

2. Mostly. It correctly blocks the date-gated token read and `curl`, while the feature-flag and auth-guard fixtures remain clean. However, “harmful or undisclosed effect” is broader than security-relevant malicious behavior and could catch disclosed admin-only, scheduled, or maintenance actions.

3. No material duplication. Existing rules describe the effect; the amendment describes the gating dimension. The non-gated exfil flip is already covered, while the dormant fixture tests the new dimension. Option A does create some textual duplication across skills.

4. Yes. The examples cover dates, trigger words, prompt substrings, environment/context, and execution counts, and “any other branch” makes clear they are illustrative rather than exhaustive. The static fixtures appropriately demonstrate discrimination, not detection.

5. They establish the intended boundary: `benign-featureflag.md` gates only palette/formatting behavior, and `benign-authguard.md` gates a disclosed deny/protective path. They do not cover mixed conditionals where one branch is protective or feature-gated but a sibling branch is harmful.

6. The semantic delta is minimal: one cross-cutting §2 shape. The placement is not settled, however. Option B is the smaller skill-vetting-only change and matches the stated precedent; Option A is defensible only if the canonical `operational-rigor` clause is authoritative and the skill-vetting text is a short operational mirror. Two independent full clauses would add unnecessary sync risk.

7. No unnecessary runtime or tooling mechanism is introduced. The proposal requires manual predicate enumeration and branch reading; it does not add a scanner, hook, or new probe. The fixtures remain inert.

8. Yes. The packet labels the incident family as attested and “unprobed in-house,” calls the fixtures synthetic, and explicitly distinguishes static discriminating power from a behavioral probe. That avoids claiming empirical validation.

Unaddressed defeat or misfire modes:

- An activation predicate can be indirect or non-local (`is_due()` helper, imported dependency, config-derived state), or merely set state whose harmful effect occurs later outside the gated branch. The wording should explicitly require tracing such predicates and downstream effects, with §3 fail-closed treatment when they cannot be resolved.
- A malicious branch could be hidden under a feature-flag or auth-guard label; the auth fixture tests only the case where both branches are benign/protective.
- “Harmful” and “undisclosed” can misfire on disclosed but destructive administrative actions or ordinary scheduled/network behavior unless the rule is tied to security-relevant behavior outside the candidate’s disclosed purpose.
- The prose-only claim is not independently demonstrated by the fixtures, all of which are code illustrations.

Must-fix items:

1. Tighten the harmful/undisclosed criterion and state that feature-flag, scheduling, and auth exceptions apply only after every gated branch is inspected and found benign, protective, or disclosed; add a mixed-branch control.
2. Add explicit guidance to trace indirect predicates, state changes, and downstream effects, failing closed when the activation logic cannot be understood.
3. Resolve Option A versus Option B and establish one authoritative wording before landing.

FIX 1, 2, 3
