1. **Yes—a narrow checklist gap exists.** Current §1.5 recognizes that “a trigger-conditioned or obfuscated payload surfaces only when the behavior actually executes,” but applies only to executable candidates and tests “every promised behavior.” It does not direct reviewers to discover unpromised predicates or cover conditional prose instructions. Section 3’s “full-context human-grade read” and fail-closed rule are useful backstops, not an explicit activation-gate hunt. The packet accurately avoids claiming total absence of existing coverage.

2. **Yes.** The amendment keys the finding on a harmful or undisclosed security-relevant effect behind a predicate, expressly saying the condition itself is not the hit. It catches the dormant-exfil fixture because the clean heading-normalization path conceals a later token read and POST. Conversely, the theme/hour branches merely select presentation, while the auth fixture’s `not user.is_admin` branch denies access.

3. **No material duplication.** Obfuscation hides representation; activation gating hides reachability. The exfil rule’s “default (non-example) execution path” limitation creates the clearest delta. Config self-propagation and authorization-default-flip already use broader wording and therefore overlap somewhat, but the new instruction to enumerate predicates remains a distinct review operation.

4. **Yes.** Date, prompt, environment/context, and execution-count examples span the principal families, while “any other branch” clearly makes the list illustrative. The date-gated fixture and `$DEPLOY_REGION` example supply positive cases; the two benign controls supply negative cases. A pure-prose positive fixture and a physical ungated FLIP-1 fixture would strengthen the evidence, but their absence does not make the rule unclear or claim exhaustiveness.

5. **Yes, for the intended boundary.** `benign-featureflag.md` demonstrates that environment and time predicates are not inherently suspicious. `benign-authguard.md` tests the harder case: security-relevant conditional logic whose gated action is protective and disclosed. Together they prevent the amendment from collapsing into “conditional equals trojan,” although fixtures cannot guarantee every future application will avoid false positives.

6. **Yes; Option A is the better placement.** Option B changes fewer bytes, but `CURRENT-TEXT.md` identifies operational-rigor §2 as the canonical install-gate home, and activation gating applies to executable and instruction content generally. Option A preserves that architecture if skill-vetting references the canonical clause and adds only its checklist-specific explanation and examples; two independently maintained full paraphrases would not be minimal.

7. **No unnecessary runtime or tooling mechanism is introduced.** The amendment adds a source-review obligation—enumerate predicates and inspect their branches. It neither mandates a detector nor adds a hook, scanner, network action, or new execution framework. References to fixtures use the existing §1.5 mechanism.

8. **Yes.** The packet labels the incident family as attested rather than first-hand verified, marks it `unprobed`, and distinguishes static discriminating-power fixtures from an unperformed behavioral probe. That supports the current §2 statement that shapes have been seen in malicious skills without pretending this reviewer or author reproduced the incident.

Unaddressed defeat and misfire modes:

- A payload could distribute its activation across helper functions, dispatch tables, remote configuration, exception paths, probabilistic state, or several individually benign-looking operations, leaving no obvious local predicate “guarding security-sensitive behavior.” “Any other branch” is broad enough doctrinally, but reviewers should understand predicate enumeration to include indirect and data-driven control flow.
- “Undisclosed” could be over-read to flag benign implementation details such as scheduled migration, cache maintenance, telemetry, or credential rotation. The surrounding “security-sensitive behavior,” ordinary-conditional exclusions, and §2 rule that a hit may be explained keep this from being a blocker, though “undisclosed security-relevant effect” would be a useful editorial tightening.
- Conditional malicious pseudocode in a security playbook could be mistaken for live instructions. The existing exfil rule’s explicit data-versus-live distinction should continue to govern the new bullet as well.

PROCEED
