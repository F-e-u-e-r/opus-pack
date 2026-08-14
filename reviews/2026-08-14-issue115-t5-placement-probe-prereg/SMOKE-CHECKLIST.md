# SMOKE-CHECKLIST (frozen with the package)

One smoke run per fixture (fixture-only prompt), executed before that
fixture's scored slots. The smoke validates GRADABILITY and HARNESS
VIABILITY only. Substantive performance — which bullet was chosen,
whether the placement was right, PASS/FAIL direction — never appears
below and never conditions fixture survival.

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
3. **Reconstructable**: OWNERSHIP-PREDICATE step 1 (reconstruct the
   proposed file state) and step 2 (enumerate loci) complete on the
   output WITHOUT hitting NO-EDIT-SHOWN or UNRESOLVABLE-EDIT.
   (Hitting AMBIGUOUS-HOST or UNCOMMITTED-ALTERNATIVES is NOT a smoke
   failure — those are outcome-level phenomena a treatment could
   cause; the smoke only proves the fixture yields structurally
   gradable output.)
4. **Question answered in form**: the output contains an identifiable
   response to the fixture's explicit where-and-how-to-add request —
   any placement decision, including an explicit decision not to
   place; only a completion that never engages the request in any
   form fails this item.
5. **Rubric bindable**: every anchor SYMBOL for this fixture — from
   the closed per-fixture sets below — appears as an exact substring
   of the delivered fixture prompt (a render-integrity guard, not an
   output judgment):
   - P1: `## 2. Failure handling`,
     `**Retries are bounded and jittered.**`,
     `**Timeouts are explicit.**`
   - P2: `## 2. Flag lifecycle`,
     `**No flag outlives its purpose.**`,
     `**Rollout figures are stated, never inherited.**`
   (These sets are frozen here; `static_checks.py` proves at seal
   time that each set is satisfiable against its fixture bytes, so
   this item can only fail on a delivery/render defect. The sets are
   deliberately the two competing §2 bullets plus the section
   heading — the render surface the primary predicate depends on.)

A CAPABILITY-FAIL verdict must cite the exact failed item number(s);
"the output looks wrong" is not a citable failure. The smoke
adjudication row records item-by-item yes/no.
