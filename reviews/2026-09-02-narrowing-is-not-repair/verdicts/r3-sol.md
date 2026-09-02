BLUF: FIX F1–F3 before commit; F4 is a shippable Low wording defect. The round-2 repairs introduced two over-broad doctrine claims and one done-when scope expansion. [verified: comparison of the diff, contexts, adjudication, and README in this packet]

F1 — `skills/cross-model-review/SKILL.md`, “only when the qualified claim is no wider than what was measured” — the rule applies generally, but non-empirical claims can be bounded by deduction, specifications, or other evidence rather than measurement; this also conflicts with the body’s allowance for non-probe substantiation — replace “what was measured” with “what the evidence establishes,” then specify measurement for empirical claims — severity Medium — [verified: the heading is universal while the body limits probes to empirical claims]

F2 — `skills/operational-rigor/SKILL.md`, “no command-and-output pair captured at the revision the claim is about” — command/output and repository revisions are not universal requirements for diagnostic evidence; UI observations, traces, API captures, or environment-bound procedures can establish results without either form — require a reproducible invocation or procedure plus captured observations, tied to the relevant artifact and environment identity — severity Medium — [verified: the obligation quantifies over every asserted diagnostic result but names only command- and revision-shaped evidence]

F3 — `skills/operational-rigor/SKILL.md`, “every asserted result has its invocation and output captured” — the done-when expands obligation (3) from “asserted diagnostic result” to every asserted result, broadening the rule beyond its stated scope — change to “every asserted diagnostic result has its invocation or procedure and resulting evidence captured” — severity Medium — [verified: direct comparison between obligation (3) and its done-when]

F4 — `skills/operational-rigor/SKILL.md`, “the line is weakened to what was” — the sentence is grammatically incomplete and leaves the intended evidentiary boundary implicit — change to “the line is weakened to what was observed” — severity Low — [verified: the object complement is absent in the quoted text]

axis 1: F1 and F2. [verified: both mechanisms are stated more generally than their predicates support]

axis 2: F1 and F3. [verified: heading/body and obligation/done-when comparisons]

axis 3: no finding. [verified: the new rule is distinct from check coverage and from the prohibition on fabricated observations]

axis 4: F3. [verified: the third obligation and done-when have different scopes]

axis 5: F1 and F2. [verified: both assume evidence forms that are not portable across claim and diagnostic types]

axis 6: no finding. [verified: both negative examples and the positive example preserve the README’s two-condition, located-artifact mechanism]

axis 7: no finding. [verified: packet-supported historical claims agree with the README]

axis 8: F4. [verified: the incomplete clause reduces clarity]

axis 9: no additional finding. [verified: packet-rederivable dispositions 1–6 and 8–16 are reflected in the diff; the defects above arise from the replacement wording rather than a missing adjudicated edit]

FIX F1,F2,F3