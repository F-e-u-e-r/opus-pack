# issue115-t5pprobe-v1 — SCORED UNIT ledger (36 observations, one indivisible unit)

Grant: the 36 scored slots of the frozen SLOT-TABLE, executed as ONE
preregistered analysis unit. No optional stopping: no slot's content,
placement direction, or apparent arm difference was consulted in
deciding whether to continue. Continuation was governed solely by the
frozen slot order and the prereg's validity/stop rules.

## Execution

- executed: **36/36**, in frozen slot order, starting at slot 1 (P1/B/n=1)
- validity: **36 VALID-SCORED**, 0 INVALID-RUN, **0 UNGRADABLE**
- identity: all 36 reported `claude-haiku-4-5-20251001` (the prereg pin)
- 36 unique api_message_ids
- pre-send digest gate: 36/36 EXACT against the frozen SLOT-TABLE
- decoded wire == rendered prompt bytes: 36/36
- wire shape: single user turn, no system, 0 tools, no sampling override, 36/36
- retries: **0** (none consumed; entitlement never triggered)
- campaign exceptions: **0**; pre-send aborts: **0**; zero-request events: **0**
- verifier-only corrections in this unit: **0**

## Adjudication

Arm-blind: outputs were stripped of slot/arm labels and ordered within
each fixture by content hash before grading; the arm map stayed sealed
until every observation had been classified. Grading used the frozen
`OWNERSHIP-PREDICATE` with the pre-declared per-fixture owners; no
semantic-equivalence rule, owner, classification priority, or pooling
strategy was invented after seeing any result. Rejoin integrity was
machine-checked (each graded observation's content hash equals the
sealed map's).

**AUTHORIZED-ADJUDICATION-METHOD-DEVIATION** (owner-classified; NOT
`protocol-compliant-as-written`, NOT an exception, NOT an INVALID-RUN).
The sealed prereg §11 names `claude-fable-5` as the *proposed*
adjudicator and §12/2 records "single hypothesis-aware adjudicator" as
a limitation. Grading here was instead performed by the operator
applying the frozen mechanical predicate directly. Two facts hold
simultaneously and both are recorded rather than reconciled away:

1. The grading changed no predicate, owner, precedence, or mapping — it
   executed the procedure the prereg itself declares load-bearing, with
   every locus, host id, class and descriptive field recorded per
   observation so a second party can recompute.
2. The operator method carries a LATER owner authorization (the scored
   grant's instruction to grade arm-blind with the frozen mechanical
   predicate). That authorization does not rewrite the prereg, whose
   text still proposes a Fable adjudicator.

The predicate — not any adjudicator's judgment — remains the
load-bearing control.

## Grid (PASS-OWNER over 6 counted runs; bands HIGH>=5, LOW<=2, MID 3-4)

| fixture | B | C | E | pattern |
|---|---|---|---|---|
| P1 | 0/6 (LOW) | 2/6 (LOW) | 4/6 (MID) | **MIXED** |
| P2 | 0/6 (LOW) | 3/6 (MID) | 1/6 (LOW) | **MIXED** |

Both fixtures CLEAN (6 counted runs per arm, 0 UNGRADABLE).

## Preregistered outcome

The §8 ordered decision procedure was applied without modification.
Steps 1 and 2 did not fire; **step 3 fired (P2 pattern = MIXED)**.

**OUTCOME: `INCONCLUSIVE(MIXED-P1+MIXED-P2)`**

Per §8, INCONCLUSIVE **recommends nothing**, and MIXED patterns are
never force-fitted into O1–O4. **No hypothesis is supported: H1, H2 and
H3 all remain undecided by this unit.** The E arm never reached HIGH on
either fixture and no arm reached HIGH anywhere, so neither the
saturation branch (O4) nor the control-failed branch (R5) was reached —
the procedure terminated earlier, at the MIXED gate.

Fixture divergence is recorded, not resolved: the two fixtures'
distributions differ in shape and are reported separately; nothing is
pooled.

## Accounting

- dry-run 1 + smoke 2 + scored 36 = **39/50 consumed**
- prereg planned: 39 — **complete**
- remaining hard-cap capacity: 11 physical slots. **Hard-cap remaining
  physical capacity is not an available reserve and does not itself
  authorize execution.**
- T2 probe headroom 11: **untouched**; stage-2 reserve 18: **untouched**
- doctrine / marker / fixture / prereg / rubric mutation: **0**
- #115: **OPEN**

## Independent recomputation

Two independent recomputations (`gpt-5.6-luna` and `gpt-5.6-sol`, both
at `max`, mutually blind), run in two phases so the classification pass
stayed blind to the arm map, to the operator's rows, and to the outcome.
No behavioural run was repeated and no budget of any kind was consumed.

- Phase 1 (blind classification): **three-way unanimity on 36/36 rows,
  0 mismatches** — identical primary class AND identical fold host on
  every observation; both reviewers independently reproduced 36
  VALID-SCORED / 0 UNGRADABLE and confirmed no frozen owner was ever
  re-determined.
- Phase 2 (after unsealing): both independently reproduced the six-cell
  grid, CLEAN status, both MIXED patterns, the ordered procedure firing
  at step 3, the outcome `INCONCLUSIVE(MIXED-P1+MIXED-P2)`, the absence
  of support for H1/H2/H3, and the descriptive statistics. Each
  reviewer's per-observation arm partition was script-checked against
  the sealed map and matched cell by cell. Neither revised a phase-1
  row. Both final lines: `RECOMPUTATION CONFIRMS`.

Both reviewers also flagged, unprompted, the same misreading hazard:
P1's raw E-versus-C contrast could be mistaken for directional support
for H2, which the frozen mapping does not license. Trail in
`_recomputation/`.

## State

Halted at the scored-evidence checkpoint (STOP — not HOLD, no
exception). Not included in this grant and not done: cross-model review
of the result, commit/push/PR, doctrine amendment, marker disposition,
use of the remaining capacity, and #115 closure.
