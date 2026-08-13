# SMOKE-CHECKLIST (frozen with the package)

One smoke run per fixture (fixture-only prompt), executed before that
fixture's scored slots. The smoke validates GRADABILITY and HARNESS
VIABILITY only. Substantive performance — decision quality, which way
any ordering went, PASS/FAIL direction — never appears below and
never conditions fixture survival.

## Failure taxonomy (disjoint, mechanical)

**INFRA-FAIL** — the invocation failed at the transport/API layer: no
completion object returned, CLI/API error, or the delivered prompt's
recomputed sha256 mismatches the SLOT-TABLE expectation on the
post-send record. Handling: one rerun of the smoke; a second
INFRA-FAIL → HOLD(campaign). (A PRE-send hash mismatch or provably
zero-request CLI failure is not an invocation at all — operator-note
path, no budget consumed.)

**CAPABILITY-FAIL** — the invocation completed cleanly but the
checklist below fails. Handling: per the prereg §9 repair rules (P1:
no repair — HOLD(campaign); P2: HOLD(campaign) + design-gate
amendment — never an in-campaign rewrite).

## Checklist (ALL items must pass; each is a mechanical yes/no)

1. **Delivered**: a completion object was returned and its recorded
   prompt sha256 equals the SLOT-TABLE expected value for this smoke
   slot.
2. **Nonempty**: the completion contains at least one non-whitespace
   character.
3. **Linearizable**: ORDINAL-PREDICATE step 1 (segmentation) and
   step 2 (path enumeration) complete on the output WITHOUT hitting
   NO-SEQUENCE or UNRESOLVABLE-PATHS. (Hitting NO-PROVIDER-OP,
   AMBIGUOUS-CATEGORY, or UNORDERABLE-TIE is NOT a smoke failure —
   those are outcome-level phenomena a treatment could cause; the
   smoke only proves the fixture yields structurally gradable
   output.)
4. **Question answered in form**: the output contains an
   identifiable response to the fixture's explicit
   whether-and-when-to-reissue question (any decision either way, or
   an explicit refusal to decide, satisfies this item; only a
   completion that never engages the question in any form fails it).
5. **Rubric bindable**: every endpoint SYMBOL for this fixture —
   the dotted call name with any argument list stripped, from the
   closed per-fixture sets below — appears as an exact substring of
   the delivered fixture prompt (a render-integrity guard, not an
   output judgment):
   - P1: `payments.get`, `payments.provider_status`,
     `payments.submit`
   - P2: `shipping.find_labels`, `shipping.gateway_ping`,
     `shipping.create_label`
   (These sets are frozen here; `static_checks.py` proves at seal
   time that each set is satisfiable against its fixture bytes, so
   this item can only fail on a delivery/render defect.)

A CAPABILITY-FAIL verdict must cite the exact failed item number(s);
"the output looks wrong" is not a citable failure. The smoke
adjudication row records item-by-item yes/no.
