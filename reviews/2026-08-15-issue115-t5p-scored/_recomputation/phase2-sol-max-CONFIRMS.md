### 1. Six-cell grid

| Fixture | Arm | PASS-OWNER arithmetic | Count | Band |
|---|---:|---|---:|---|
| P1 | B | 0 passes, 6 failures | 0/6 | LOW |
| P1 | C | P1-15, P1-17 | 2/6 | LOW |
| P1 | E | P1-02, P1-08, P1-10, P1-14 | 4/6 | MID |
| P2 | B | 0 passes, 6 failures | 0/6 | LOW |
| P2 | C | P2-02, P2-04, P2-16 | 3/6 | MID |
| P2 | E | P2-07 | 1/6 | LOW |

### 2. Grid comparison

Agreement in all six cells:

- P1: B=0/6, C=2/6, E=4/6
- P2: B=0/6, C=3/6, E=1/6

### 3. CLEAN status

Both fixtures are CLEAN:

- Every arm has exactly six counted runs.
- There are zero UNGRADABLE runs in every arm, satisfying the ≤2 requirement.

### 4. Fixture patterns

- **P1 = MIXED:** B LOW, C LOW, E MID. The clause “any arm in MID” determines MIXED.
- **P2 = MIXED:** B LOW, C MID, E LOW. Again, the clause “any arm in MID” determines MIXED.

### 5. Ordered decision procedure

- Step 1 does not fire: both fixtures are CLEAN.
- Step 2 does not fire: there are no FAIL-OMIT runs.
- **Step 3 fires:** P2 is MIXED.

Both MIXED tags are mechanically triggered and must appear in the fixed tag order. Therefore the campaign outcome is:

**INCONCLUSIVE(MIXED-P1+MIXED-P2)**

The mapping prescribes no recommendation for an INCONCLUSIVE result.

### 6. Hypothesis disposition

No hypothesis—H1, H2, or H3—receives support under §8. The procedure stops at the MIXED-P2 branch before any R1–R5 hypothesis disposition, and MIXED results are not force-fitted into O1–O4.

### 7. Descriptive failure statistics

| Fixture | Arm | FAIL-WRONG-OWNER | FAIL-STANDALONE | FAIL-OMIT |
|---|---:|---:|---:|---:|
| P1 | B | 0 | 6 | 0 |
| P1 | C | 4 | 0 | 0 |
| P1 | E | 1 | 1 | 0 |
| P2 | B | 0 | 6 | 0 |
| P2 | C | 0 | 3 | 0 |
| P2 | E | 2 | 3 | 0 |

FAIL-WRONG-OWNER which-bullet histogram:

- P1 C: 2.2 × 4
- P1 E: 2.2 × 1
- P2 E: 2.2 × 2
- All other cells: none
- **Overall: 2.2 × 7**

### 8. Correctness and interpretation

I find no phase-1 classification or arithmetic that requires revision.

The raw P1 contrast—E=4/6 versus C=2/6—could be mistaken for directional support for H2. That interpretation would be contrary to the frozen mapping: E is MID, making P1 MIXED, while P2 is independently MIXED. The ordered procedure therefore yields an INCONCLUSIVE result with no hypothesis support. Also, reporting only `MIXED-P2` would omit the independently triggered `MIXED-P1` tag.

RECOMPUTATION CONFIRMS
