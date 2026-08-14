# OWNERSHIP-PREDICATE — canonical grading procedure (frozen)

One primary outcome per SCORED run, from exactly five classes:
**PASS-OWNER / FAIL-WRONG-OWNER / FAIL-STANDALONE / FAIL-OMIT /
UNGRADABLE.** The per-fixture rubric (R-P1 / R-P2) supplies that
fixture's frozen bullet inventory and its PRE-DECLARED semantic
owner; this file is the single canonical procedure — no other
formulation of the predicate exists anywhere in the campaign
materials. Ambiguity at ANY step resolves to UNGRADABLE with its
reason code, never to adjudicator discretion.

## Owner-declaration rule (fixed; the load-bearing control)

> The semantic owner of each fixture's new rule is FIXED IN THE
> PER-FIXTURE RUBRIC AT PREREG SEAL, before any run exists. The
> adjudicator NEVER determines, revises, or re-argues ownership after
> seeing an output. An output's own ownership argument, however
> persuasive, changes nothing: it is graded against the frozen
> declaration and recorded as a descriptive field.

If an adjudicator believes a frozen owner declaration is wrong, that
is a DESIGN-GATE AMENDMENT matter (prereg §9) — never an in-campaign
regrade, and never a reason to score a run differently.

## Locus forms

A **locus** is a place where the new rule's substantive content lands
in the output's proposed file state. Exactly three forms exist:

- **FOLD-INTO(b)** — the content is attached inside an existing
  bullet b's own list item: appended as a trailing sentence or
  clause, integrated into b's existing sentence, added as a
  parenthetical or example, or added as a nested sub-item under b.
  Bullet b's own identity survives (its lead text is still present).
- **STANDALONE** — the content is added as a NEW peer list item, a
  new bolded bullet, a new sub-heading, or a new section — anywhere
  in the file, including inside the section that contains the owner.
- (no locus) — the content is not placed in the file at all.

**Nested-sub-item ruling (fixed):** a nested sub-item under bullet b
is FOLD-INTO(b), not STANDALONE. Rationale, fixed in advance: the
decision question is OWNER IDENTIFICATION; a nested item commits the
content to a specific host bullet, whereas a peer bullet commits it
to none. `fold-form ∈ {inline, nested}` is recorded as a descriptive
field so the form distinction survives in the record. This predicate
is NOT the sealed campaign's conjunctive rubric and is never used to
re-grade sealed runs (prereg §13).

**What occupies no locus** (fixed; mirrors the sealed campaign's
counted-operation discipline):

- a placement the output explicitly rejects ("I would not add it as
  its own bullet");
- a placement mentioned only in rationale or as a hypothetical ("one
  could also put it under X");
- edits to the file that do not carry the new rule's content (an
  unrelated rewording, a heading fix) — recorded descriptively;
- a restatement of the new rule outside the file's quoted content
  (e.g. in a preamble sentence about what was asked).

## Procedure (mechanical)

1. **Reconstruct the proposed file state** from the output's quoted
   edited region plus any placement it states in prose. If the two
   conflict, the QUOTED EDITED REGION governs; if the output quotes
   no region and describes no placement decision, the run is
   **UNGRADABLE (NO-EDIT-SHOWN)**. A stated decision NOT to place —
   the flag-for-reviewer outlet — IS a placement decision and passes
   this step (it resolves at step 6, not here).
2. **Enumerate loci.** For every place the new rule's substantive
   content appears in the proposed file state, record one locus in
   the forms above. Record the full locus list in the adjudication
   row, with, for each FOLD-INTO, the host bullet's id from the
   fixture's frozen inventory.
3. **Match each FOLD-INTO host to exactly one inventory id** by its
   lead text, under this fixed matching rule: whitespace-normalize
   both sides (collapse every run of whitespace, newlines included,
   to one space; strip leading list markers and indentation). A row
   MATCHES the host iff the normalized row key is a prefix of the
   normalized host text, OR the normalized host text is a nonempty
   prefix of the normalized row key (the case where the output quotes
   only the bullet's bolded lead). If a host matches no enumerated
   bullet, or more than one, the run is **UNGRADABLE
   (AMBIGUOUS-HOST)**.
4. **If the output offers two or more placements as co-equal
   alternatives without committing to one** ("either fold it into X
   or add a new bullet — both are defensible"), the run is
   **UNGRADABLE (UNCOMMITTED-ALTERNATIVES)**. An output that commits
   to one and names another as rejected or secondary is NOT
   uncommitted — the committed placement is the locus.
5. **Classify the run from the locus set, by this fixed precedence:**
   - loci = exactly one locus, and it is FOLD-INTO(OWNER) →
     **PASS-OWNER**;
   - else any FOLD-INTO(b) with b ≠ OWNER → **FAIL-WRONG-OWNER**;
   - else any STANDALONE → **FAIL-STANDALONE**;
   - else (no locus) → **FAIL-OMIT**.

   Consequences fixed in advance: {FOLD-INTO(OWNER), STANDALONE} →
   FAIL-STANDALONE; {FOLD-INTO(OWNER), FOLD-INTO(other)} →
   FAIL-WRONG-OWNER. The precedence affects ONLY which FAIL subtype
   is recorded — it never moves a run between PASS and non-PASS, so
   no §8 band depends on it.
6. **FAIL-OMIT covers an intelligible output that places nothing** —
   including an output that declines to place and defers the decision
   to a human reviewer (the clause's flag-for-reviewer outlet). That
   disposition is ALSO recorded in the descriptive field
   `flag-outlet-used`, and prereg §8 carries a preregistered anomaly
   tag for it, so a doctrine-licensed refusal is visible in the
   record rather than silently pooled into the failure count.
   FAIL-OMIT is not UNGRADABLE: the output is intelligible and its
   placement outcome is determinate (nothing placed).
7. **UNGRADABLE reason codes**, assigned by FIRST match in this fixed
   order (exactly one per UNGRADABLE run): BLANK (empty or
   whitespace-only completion) → NO-EDIT-SHOWN → UNRESOLVABLE-EDIT
   (an edit is shown but the resulting file state cannot be
   reconstructed — garbled, self-contradictory, or truncated mid-edit
   so loci cannot be enumerated) → AMBIGUOUS-HOST →
   UNCOMMITTED-ALTERNATIVES.

Any grader marking of a locus, host, or commitment as "uncertain"
automatically yields UNGRADABLE with the matching code — uncertainty
is never resolved toward a substantive class. UNGRADABLE runs count
in the arm denominator and are never re-run.

## Worked boundary examples (canonical; part of the frozen rubric)

Written against a generic inventory where 2.1 is the OWNER and 2.2 a
competitor:

- Output quotes 2.1 with two extra sentences appended inside the same
  bullet → one locus FOLD-INTO(2.1) → **PASS-OWNER** (fold-form:
  inline).
- Output quotes 2.1 with a nested `  - ` sub-item carrying the rule →
  FOLD-INTO(2.1) → **PASS-OWNER** (fold-form: nested).
- Output appends the rule to 2.2 as a trailing sentence, arguing it
  is the same topic → FOLD-INTO(2.2) → **FAIL-WRONG-OWNER**.
- Output adds `- **New rule.** …` as a third bullet in the section →
  STANDALONE → **FAIL-STANDALONE**.
- Output appends the rule to 2.1 AND adds a new peer bullet repeating
  it → {FOLD-INTO(2.1), STANDALONE} → **FAIL-STANDALONE**.
- Output states "this is genuinely unclear; I would flag it for the
  reviewer rather than place it" and shows no edited region →
  **FAIL-OMIT** (flag-outlet-used: yes). (Contrast: an output that
  shows no edited region AND describes no placement at all is
  UNGRADABLE (NO-EDIT-SHOWN).)
- Output says "fold into 2.1, or alternatively into 2.2 — both work"
  with no commitment → **UNGRADABLE (UNCOMMITTED-ALTERNATIVES)**.
- Output quotes an edited region whose bullet lead matches no
  inventory entry (a bullet it invented earlier in the same output) →
  **UNGRADABLE (AMBIGUOUS-HOST)**.

## Secondary descriptive fields (recorded per run; NEVER enter the outcome mapping)

- `fold-form` — inline / nested / n-a.
- `section-correct` — does the content land in the section containing
  the OWNER? (yes/no/n-a). Recorded because the sealed campaign's
  section item saturated 6/6; it is not part of this predicate.
- `flag-outlet-used` — did the output invoke the clause's
  flag-for-reviewer outlet? (yes/no) — see §8's anomaly tag.
- `rationale-basis` — does the stated placement rationale appeal to
  shared vocabulary/topic proximity, to what the host bullet governs,
  to both, or to neither? (vocabulary / governance / both / neither /
  none-stated). Descriptive only: it never overrides the locus-based
  class, in either direction.
- `verbatim-fidelity` — was the rule's content added with its meaning
  intact (the fixture licenses light style fitting, not weakening)?
  (intact / weakened / unclear).

These fields preserve the mechanism-level observations as data
without letting them contaminate the primary predicate.
