# Rubric R-P1 (fixture P1 = sealed T5S1 bytes; single primary outcome)

Grading uses `OWNERSHIP-PREDICATE.md` VERBATIM with the inventory and
owner declaration below — no other criteria apply to the primary
outcome.

## Frozen bullet inventory (P1)

| id | lead text (match key) | section |
|---|---|---|
| 1.1 | `Prefer the versioned endpoint; the unversioned alias may repoint at any time.` | §1 Choosing an endpoint |
| 1.2 | `A sandbox endpoint never substitutes for a live smoke check.` | §1 Choosing an endpoint |
| 2.1 | `**Retries are bounded and jittered.**` | §2 Failure handling |
| 2.2 | `**Timeouts are explicit.**` | §2 Failure handling |
| 3.1 | `Every failed call series logs its final disposition (gave-up / succeeded-after-N) with the elapsed wall-clock time.` | §3 Recording outcomes |

The inventory is closed: a FOLD-INTO host that matches no row, or
more than one row, is UNGRADABLE (AMBIGUOUS-HOST).

## PRE-DECLARED semantic owner (frozen at seal)

**OWNER(P1) = 2.1 `Retries are bounded and jittered`.**

This declaration is CARRIED VERBATIM from the sealed campaign's
frozen rubric R-T5S1 (`79bdeb515ea4b769b0672304618c95cb8f81f7654cec3e9258c3e3f2607a41f1`),
which named the same bullet as the owner before any sealed run
existed. It is a FROZEN TEST TARGET for this probe and is explicitly
out of scope for re-argument here (prereg §1): the seal-time reason
of record is that the new rule bounds the retry LOOP's total elapsed
time — the quantity 2.1 already bounds by attempt count — while 2.2
scopes a per-attempt property, which the new rule's own wording cites
only as the insufficient case.

Competing candidate of record: 2.2 `Timeouts are explicit` — the
bullet the sealed runs folded into. It shares the new rule's surface
vocabulary (timeout, elapsed time) without governing the retry loop.

## Notes fixed in advance

- A fold into 2.2, 1.1, 1.2, or 3.1 is FAIL-WRONG-OWNER — the section
  the host sits in does not change the class.
- A new bullet anywhere, including inside §2 next to 2.1, is
  FAIL-STANDALONE.
- `section-correct` (does the content land in §2?) is a DESCRIPTIVE
  field only. The sealed campaign's section item saturated (6/6) and
  is not this probe's discriminator.
- This rubric does NOT re-grade the sealed campaign's conjunctive
  rubric R-T5S1, and no sealed run is re-read, re-scored, or pooled
  (prereg §13).

UNGRADABLE: per `OWNERSHIP-PREDICATE.md` step 7, which is canonical —
five codes in fixed first-match order: BLANK / NO-EDIT-SHOWN /
UNRESOLVABLE-EDIT / AMBIGUOUS-HOST / UNCOMMITTED-ALTERNATIVES.
