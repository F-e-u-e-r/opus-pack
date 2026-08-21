1. Yes, narrowly. §1.5 only covers “an executable candidate” and “every promised behavior”; its note that “a read is not enough” does not create a read-phase hunt for unpromised dormant branches. §2 lacks this shape, while §3 is a general fallback. The dormant-exfil fixture demonstrates the clean promised path.

2. It catches the supplied failures: date gating, indirect environment gating, labels, and deferred effects. The benign fixtures avoid false positives. However, the clearance for “a disclosed part of the stated purpose” can also clear a harmful disclosed branch.

3. No. Obfuscation concerns concealment, exfiltration/config rules identify effects, and this amendment identifies activation control flow. It also cleanly separates §1.5’s execution requirement from static branch inspection.

4. Yes. The wording covers date/time, trigger text, environment/context, execution count, helpers, imports, configuration, deferred state, and prose. “May be” and “any dormant branch” make the examples non-exhaustive.

5. Mostly. The feature-flag fixture is security-irrelevant, and the auth guard is security-relevant but protective and disclosed. Neither tests the harmful-but-disclosed ambiguity noted above.

6. Yes, with Option A. One canonical operational-rigor clause plus a short skill-vetting pointer is a minimal semantic delta and avoids two competing rules. Option B is shorter but loses the cross-layer canonical home.

7. No unnecessary mechanism is introduced. The proposal is purely doctrinal, keeps fixtures inert, and references existing fixture requirements without adding hooks, tooling, or runtime probes.

8. Yes. The packet distinguishes an attested incident family from first-hand verification, labels the fixtures synthetic and unexecuted, and states that this gate establishes only static discriminating power—not real-world prevalence or behavioral efficacy.

Unaddressed defeat/misfire: “a disclosed part of the stated purpose” is too broad. A candidate could describe credential collection or date-gated exfiltration as part of its purpose, allowing a reviewer to clear a branch despite the earlier “harmful effect” criterion. The packet’s “never by its label” language addresses feature-flag labels, not this disclosure escape. Limit that exception to non-harmful, legitimate behavior and state that disclosure alone never clears a harmful effect.

FIX 1
