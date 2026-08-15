# Independent scored recomputation — closure

Two independent recomputations of the completed scored unit, run in two
phases so that the classification pass stayed blind.

Reviewers: `gpt-5.6-luna` and `gpt-5.6-sol`, both at reasoning effort
`max`, each isolated with its packet as the only file in its working
directory, neither shown the other's output at any point.

**No behavioural run was repeated.** This audit re-derives the result
from evidence already on disk: zero executor invocations, zero use of
the remaining hard-cap capacity, zero use of the T2 headroom or the
stage-2 reserve, and no change to any fixture, prereg, rubric, doctrine
or marker.

## Phase 1 — blind classification

Each reviewer received only: the 36 label-stripped completions, the
frozen `OWNERSHIP-PREDICATE.md`, `R-P1.md` and `R-P2.md` (inventories,
pre-declared owners, precedence, descriptive-field definitions), and
the locked content hashes. Deliberately withheld: the arm map, the
operator's classifications, any tally or grid, the outcome, and any
hypothesis framing — verified by a mechanical leakage scan over the
packet before it was sent.

Observation labels carry no information: within each fixture the
observations were ordered by a hash of their own content before being
numbered, so the numbering cannot leak arm or execution order.

**Result: three-way unanimity, 36/36 rows, 0 mismatches** — operator,
Luna and Sol assigned the identical primary class AND the identical
fold host on every observation. Both reviewers independently reported
36 VALID-SCORED / 0 UNGRADABLE, confirmed they never re-determined a
frozen owner, and confirmed they applied the fixed precedence
including the quoted-region-governs rule.

## Phase 2 — unsealing and derivation

Each reviewer then received its OWN phase-1 rows back verbatim, the
previously sealed arm map, and prereg §8 verbatim — still not the other
reviewer's work, and still not the operator's grid or outcome. Each was
asked to compute the grid first and only then compare it, and was
instructed that a phase-1 classification must not be silently revised:
a disagreement with one's own earlier row was to be reported as a
finding.

Neither reviewer revised any phase-1 row. Both reproduced, independently:

- the six-cell grid — P1 B 0/6, C 2/6, E 4/6; P2 B 0/6, C 3/6, E 1/6;
- CLEAN for both fixtures (6 counted runs per arm, 0 UNGRADABLE);
- pattern MIXED for both fixtures, each decided by the "any arm in MID"
  clause;
- the ordered procedure: steps 1 and 2 do not fire, **step 3 fires**;
- outcome **`INCONCLUSIVE(MIXED-P1+MIXED-P2)`**, both tags mechanically
  triggered and carried in the fixed order;
- **no support for H1, H2 or H3**;
- the descriptive statistics, including the FAIL-WRONG-OWNER
  which-bullet histogram (bullet 2.2, 7 of 7).

Each reviewer's per-observation arm partition was additionally checked
against the sealed map by script and matched exactly — not merely the
totals, but every cell.

Both final lines read `RECOMPUTATION CONFIRMS`.

## Convergent warning, recorded because it is the main misreading risk

Both reviewers, unprompted and independently, flagged the same hazard:
P1's raw contrast (E 4/6 against C 2/6) could be mistaken for
directional support for H2. Under the frozen mapping it is not. E is
MID, which makes P1 MIXED; P2 is independently MIXED; the ordered
procedure therefore terminates at step 3 with no hypothesis support,
and §8 forbids force-fitting a MIXED pattern into O1–O4. Sol added that
reporting only `MIXED-P2` would wrongly drop the independently
triggered `MIXED-P1` tag.

## What this unit established

Not which explanation is true. **This preregistered design did not
separate H1, H2 and H3 at this tier and sample size.** That is a
complete and honest empirical result, independently recomputed twice,
and it is reported as such rather than as a near-miss for any
hypothesis.
