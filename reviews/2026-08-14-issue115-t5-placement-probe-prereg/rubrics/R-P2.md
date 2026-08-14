# Rubric R-P2 (fixture P2 = documented-owner case; single primary outcome)

Grading uses `OWNERSHIP-PREDICATE.md` VERBATIM with the inventory and
owner declaration below — no other criteria apply to the primary
outcome.

## Frozen bullet inventory (P2)

| id | lead text (match key) | section |
|---|---|---|
| 1.1 | `A flag's name states the behaviour it gates, not the ticket that introduced it.` | §1 Naming and registration |
| 1.2 | `A flag added outside the flag sheet is treated as an incident.` | §1 Naming and registration |
| 2.1 | `**No flag outlives its purpose.**` | §2 Flag lifecycle (OWNER) |
| 2.2 | `**Rollout figures are stated, never inherited.**` | §2 Flag lifecycle |
| 3.1 | `Every release note lists the flags whose exposure changed, with the figure before and after.` | §3 Reporting |

The inventory is closed: a FOLD-INTO host that matches no row, or
more than one row, is UNGRADABLE (AMBIGUOUS-HOST).

## PRE-DECLARED semantic owner (frozen at seal)

**OWNER(P2) = 2.1 `No flag outlives its purpose`.**

Seal-time reason of record (fixed before any run exists; never
re-argued after seeing an output):

- The new rule's governed object is the FLAG's end of life — it
  states the condition under which a flag *is deleted*, and what may
  not stand in for that deletion.
- 2.1 is the only bullet in the file that governs that object: it
  declares the flag's span in so many words — "Each flag exists from
  the change that introduces it until the day no path in the source
  can still reach it" (its own words) — and assigns a steward over
  that whole span. The
  new rule further constrains exactly the endpoint 2.1 already
  governs; 2.1 does not yet state WHEN that endpoint arrives, which
  is the gap the new rule fills.
- 2.2 governs a different object: how a flag's exposure figure is
  stated and where it is recorded. Nothing in 2.2 governs whether or
  when a flag leaves the codebase.
- 3.1 governs release-note contents, not flag lifetime.
- 1.1 / 1.2 govern naming and registration at introduction.

**Documented-owner property (design intent), with the lexical
invariant MACHINE-CHECKED.** P2 is the probe's capability control:
ownership here is stated in the owning bullet's own words, so a
reader attaching by GOVERNED OBJECT has an explicit target — while
the rule's shared vocabulary points AWAY from that target.
`static_checks.py` recomputes the rule-to-bullet surface similarity
on a MEASURE FAMILY, not one metric: (i) content-token type overlap
(stopword-filtered, plural-stemmed — the filter is named here because
it hides function words, which the raw axis then catches); (ii) a
frequency-weighted score (stemmed term-frequency dot product); (iii)
shared word bigrams; (iv) RAW word tokens, unfiltered and unstemmed;
and (v) word-internal character n-grams for EVERY n from 3 to 8. The
binding property across (iv) and (v) is OWNER-EXCLUSIVITY: no feature
may be shared by the rule and the OWNER while being absent from every
other bullet, at any granularity in the family.

| bullet | content-token types | TF score | shared bigrams | owner-exclusive features |
|---|---|---|---|---|
| 1.1 | {flag} | 1 | — | n/a |
| 1.2 | {flag} | 2 | `a flag` | n/a |
| **2.1 (OWNER)** | **{flag}** | **2** | **— (none)** | **NONE, on every axis** |
| 2.2 | {flag, rollout, figure} | 4 | — | n/a |
| 3.1 | {flag, release, figure} | 4 | — | n/a |

The owner shares exactly the one content-token type every bullet in
the file carries, scores strictly BELOW both plausible competitors on
the frequency-weighted measure, shares NO bigram with the rule, and —
the class-closing property — has NO owner-exclusive feature on the
raw-token axis or at any character n-gram width from 3 to 8. A reader
attaching by surface proximity is therefore pulled toward 2.2/3.1 and
has no DIFFERENTIAL route to 2.1 anywhere in the measured family; a
reader attaching by governance lands on 2.1. Every axis is enforced
by script, not asserted in prose, and fixed here at seal, not after
any result.

(No single measure is relied on alone, because four successive drafts
each satisfied the measures then in force and still leaked a route: a
shared token (`codebase`); a frequency tie plus two shared word
bigrams; a shared subword (`alive` ↔ `outlives`) with no shared token
at all; then `its` and `one` at n=3 plus raw `its` that the
content-token filter had hidden. Each time the measure FAMILY was
widened rather than the wording patched, until the family became an
exhaustive owner-exclusivity sweep.)

Residual, stated at seal: no scan of this kind can exclude SYNONYM or
purely conceptual proximity (`deleted` ↔ `retired`; `source` ↔ the
idea of code), nor position, nor a mechanism no listed axis measures.
P2 therefore EXCLUDES the measured surface routes to its owner; it
does NOT isolate
governance-based attachment from conceptual proximity, and no claim
in this campaign asserts that it does (prereg §8, §12/12).

**Two-clause structure (fixed reading).** Like P1's rule, P2's rule
carries a governing statement plus a subordinate record-keeping
instruction ("Record the clearing release beside the figure"), and
that instruction touches the competitor's object. The subordinate
clause does NOT move ownership: it says where to note a fact about
the event the main clause governs, exactly as P1's "Declare both …
at the call site" says where to note facts about the retry wrapper
without moving that rule out of 2.1. The reading is fixed here, at
seal, for both fixtures alike.

Competing candidate of record: 2.2 `Rollout figures are stated, never
inherited`.

## Notes fixed in advance

- A fold into 2.2, 3.1, 1.1, or 1.2 is FAIL-WRONG-OWNER.
- A new bullet anywhere, including inside §2 next to 2.1, is
  FAIL-STANDALONE.
- `section-correct` (does the content land in §2?) is DESCRIPTIVE
  only.
- Owner position is deliberately the FIRST bullet of §2, matching
  P1's owner position, so that a PASS-OWNER cannot be manufactured by
  a "pick the later/nearest bullet" habit — the habit that would have
  produced the sealed campaign's observed folds. The cost is that
  this design does not separate vocabulary attraction from positional
  preference; both are non-semantic surface cues and the prereg
  treats them jointly (prereg §12, ledger item 5).

UNGRADABLE: per `OWNERSHIP-PREDICATE.md` step 7, which is canonical —
five codes in fixed first-match order: BLANK / NO-EDIT-SHOWN /
UNRESOLVABLE-EDIT / AMBIGUOUS-HOST / UNCOMMITTED-ALTERNATIVES.
