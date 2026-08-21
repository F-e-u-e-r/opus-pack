1. **Yes, narrowly.** Current §1.5 covers both sides of every “promised behavior” and says trigger-conditioned payloads surface only when executed, but it does not create a §2 read-phase hunt for unpromised dormant branches. §3 is fail-closed fallback, not explicit enumeration. `fail-dormant-exfil` demonstrates the clean default path gap.

2. **Yes.** The amendment explicitly covers date, environment, indirect, mislabeled, and deferred activation. The three fail fixtures should block, while `benign-featureflag`, `benign-authguard`, and `benign-disclosed-maintenance` are cleared because their effects are non-security-relevant, protective, or non-harmful and disclosed.

3. **No material duplication.** Existing rules identify effects or carriers—exfiltration, config propagation, and obfuscation. The new rule identifies the independent gating dimension and correctly preserves the existing data-versus-live distinction.

4. **Yes.** The examples cover representative trigger classes and explicitly include “any dormant branch.” The packet labels the fixtures as static discriminating-power evidence, not an exhaustive detector or prevalence claim.

5. **Yes.** The feature-flag fixture rejects blanket conditional scanning; the auth guard demonstrates that protective security logic is allowed; maintenance tests that disclosure clears only genuinely non-harmful in-purpose behavior.

6. **Yes, with Option A preferred.** One canonical operational-rigor clause plus a short skill-vetting pointer avoids synchronization drift and applies to both prose and code. Option B is a smaller diff but loses reusable canonical guidance.

7. **No.** The amendment adds only static reading, bounded tracing, and the existing fixture obligation. It introduces no runtime, tool, or behavioral-probe mechanism.

8. **Yes.** The packet identifies the incident family as attested rather than first-hand verified, labels the in-house fixtures `unprobed`, and limits claims to static discrimination rather than behavioral efficacy or prevalence.

Unaddressed residual risks:

- Runtime-generated callbacks, `eval`-style dispatch, remote policy, or cross-process persistent state are not illustrated explicitly. The indirect/deferred language and §3 fail-closed rule mitigate this, but a readable-yet-dynamic implementation could still be misclassified.
- “Ordinary platform conditional” is somewhat subjective; a platform-targeted malicious branch could be waved through if the materiality qualifier is ignored.
- “Harmful,” “security-relevant,” and “disclosed purpose” remain judgment calls; a reviewer who accepts a misleading benign description could misfire. The label prohibition and §3 reduce, but cannot eliminate, that risk.

PROCEED
