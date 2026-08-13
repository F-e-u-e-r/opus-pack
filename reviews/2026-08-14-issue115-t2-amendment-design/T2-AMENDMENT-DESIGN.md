# T2 doctrine-amendment DESIGN (reviews-only; no canonical mutation)

Design gate for the minimal wording change that makes the settled
STRICTLY-ORDINAL requirement explicit in the uncertain-outcome rule.
**This record designs and compares; it changes no canonical file.**
The actual mutation is a separate future owner gate. Behavioral
invocations: 0. Headroom 11 and old reserve 18: untouched. #115: OPEN.
T2 marker: untouched (remains as Section-A settled it; `unprobed`
unless separately owner-disposed).

## 0. Baseline and target pin (fresh-read, machine-derived)

- main at authoring: `327b26434222163541e38916655a1c7eded5444d`
  (#163–#191 durable).
- Target file: `skills/operational-rigor/references/external-systems.md`,
  blob `28216fd898ed7041e98d2286a824abc2147013c4` at that main.
- Target entry: the uncertain-outcome bullet, lines 123–154
  ("A side-effecting create whose outcome is unknown is never blindly
  retried…"), frozen byte-exact in `target-entry-frozen.txt`
  (sha256 `d20bdd09086458b6afeab78f4207cdbb61b548589f6364cf80cc974335acecaa`).
- Anchor sentence (verbatim, occurs exactly once in the file):
  "Run such mutations serially (one in flight), then resolve in
  this order:".
- E-arm reference bytes: `E-arm-reference.txt` (byte-identical copy
  of the sealed campaign's EXPLICIT-CONTROL-addendum.txt) — the
  experimental positive control this design must NOT copy wholesale.

## 1. Amendment contract (locked)

> **What is the smallest doctrine wording change that makes the
> already-settled STRICTLY-ORDINAL requirement explicit, without
> changing any other uncertain-outcome semantics?**

NOT questions of this gate: the authorial intent of "first"
(CLOSED, #188); whether a transmission gap exists (ANSWERED, #191
O2); whether to adopt the E-arm wholesale (NO); any change to
retry / idempotency / authoritative-read semantics (OUT OF SCOPE);
any T2 marker change (OUT OF SCOPE).

## 2. Semantic invariants (amendment-untouchable)

1. One mutation in flight (serial execution).
2. Unknown outcome is never blindly retried.
3. No destination query API / no request identity → terminal
   "uncertain" IMMEDIATELY — no probe loop, no retry.
4. (THE amendment subject) where a query exists, destination
   interrogation precedes any provider-wide health/liveness/status
   read.
5. Provider status never substitutes for destination evidence.
6. Authoritative-read rules unchanged (stale/eventually-consistent
   "not found" authorizes nothing).
7. Authoritative absence requires BOTH axes (future + past),
   unchanged.
8. Idempotency-guarantee carve-out (retention window covering
   concurrent/late arrivals) unchanged.
9. Cap / non-authoritative ambiguity / axes-open-without-guarantee →
   terminal "uncertain", unchanged.

Disqualifier: any candidate that must rewrite invariants 1–3 or 6–9
to read coherently is TOO BROAD and is rejected on that ground alone.

## 3. Candidates

All candidates insert at the same point — after "…and "it probably
failed" is not evidence." and before "Run such mutations serially…"
— leaving the anchor sentence and both branch bodies byte-identical.

### M1 — Minimal explicit ordinal (round-1 original; WITHDRAWN as
preferred after dual round-1 HOLD — superseded by M1-r2)

Inserted text (two sentences):

> Interrogate destination state before any provider-wide
> liveness/status read. Where a destination query exists, the read
> under the request identity is the first provider-side read;
> liveness/status reads may follow only afterward and never stand in
> for destination-state evidence.

Wording note: "Interrogate destination state" is deliberately used
instead of "settle destination first" — an interrogation can return
`ambiguous`; the verb names the ordinal ACTION without implying the
first read reaches final settlement.

### M2 — Short form

Inserted text (one sentence):

> Where a destination query exists, the read under the request
> identity is the first provider-side read — before any
> provider-wide liveness/status read.

### M1-r2 — Round-1 synthesis (REVISED PREFERRED)

Both round-1 reviewers independently held M1 on the same root cause
— "the first provider-side read" is STRONGER than the #188 ruling
(which orders destination interrogation before liveness/status reads
specifically, and says nothing about unrelated provider-side reads)
— plus the unconditional first sentence creating an apparent
obligation in the no-query/no-identity branch, and the dropped
"provider-wide"/keyed-read boundary. Each proposed a corrected
wording; the two proposals are semantically aligned, and M1-r2 is
their synthesis (Luna's identity-in-condition + the entry's own
"read-back" term; Sol's "separate" qualifier + stand-in guard):

> Where the destination can be queried under the request identity,
> that read-back precedes any separate provider-side liveness/status
> read — and a liveness/status read never substitutes for
> destination-state evidence.

Equivalence to #188: the ruling's ordinal is exactly
interrogation-before-any-liveness/status-read with liveness
permitted only after ("precedes any" carries only-after), and its
boundary clause (destination interrogation is itself never a
liveness/status read) is carried by "separate" plus naming the
permitted first action with the entry's own term "read-back" — the
branch-(2) operation, which cannot be misread as the thing it
precedes even when implemented via a status endpoint. The condition
quotes branch (1)'s BOTH prerequisites (query API and request
identity), so the no-query/no-identity branch acquires zero new
obligation. No first-among-all-provider-reads expansion remains.

### M3 — E-derived semantic subset

Inserted text (two sentences, re-expressed in this entry's register;
primitives extracted from E, no structural copy):

> After such a timeout the destination read-back is the first
> provider-side operation — no provider-wide liveness or status read
> precedes it, and one may follow only after the interrogation.
> Provider health is never destination evidence; this ordering is
> strict.

E-primitive extraction map (M3 ← E): (i) first-provider-side-
operation = destination interrogation; (ii) no liveness/status
before it; (iii) permitted only after; (iv) strictness marker.
Dropped from E: the imperative second-person frame ("your FIRST …
must"), the landed/did-not-land/ambiguous enumeration (already
carried by the entry's three-exit read-back), the standalone
"ADDITIONAL ORDERING REQUIREMENT" heading. The machine similarity
report (design_checks) confirms no ≥8-word verbatim run shared with
the E bytes for ANY candidate.

## 4. Candidate disposition (per owner's seven axes)

(Table as adjudicated at round 1 — the M1/M2/M3 rows carry the
ROUND-1 REVIEW verdicts, which superseded this record's original
self-assessment on the axes marked "round-1".)

| Axis | M1 | M2 | M3 |
|---|---|---|---|
| Fully expresses #188 STRICTLY-ORDINAL | NO (round-1) — OVEREXPRESSES: "the first provider-side read" constrains ALL provider-side reads, which the ruling does not | PARTIAL — ordinal only where a query exists; silent on stand-in misuse; carries the same "first provider-side read" overreach (round-1) | NO (round-1) — "first provider-side operation" overexpresses the same way, plus E-register import |
| Adds policy beyond the ruling | YES (round-1) — the first-among-all-provider-reads constraint; no new retry entitlement or mandatory liveness read though | YES (round-1) — same first-read expansion | YES (round-1) — first-operation expansion; "this ordering is strict" register import |
| Risk of misclassifying the destination read as a forbidden liveness read | MED (round-1) — sentence two drops "provider-wide"; a keyed status-endpoint interrogation can read as forbidden | LOW-MED — same naming, same dropped qualifier at the ordinal clause | LOW-MED — boundary rests on the single qualifier "provider-wide" |
| Preserves no-query terminal branch (inv. 3) | NO (round-1) — the unconditional first sentence creates an apparent competing obligation; condition also omits request identity | YES — wholly query-scoped (but omits the identity prerequisite) | YES — "the destination read-back" presupposes the query branch |
| Conflicts with subsequent authoritative-read logic (inv. 6–9) | NO — ordering only; settlement semantics untouched | NO | NO |
| Blocks "provider health ⇒ destination evidence" misreading (inv. 5) | YES — explicit "never stand in for destination-state evidence" | NO — absent; the misreading stays expressible | YES — "provider health is never destination evidence" |
| Diff size / readability | 2 sentences (~5 wrapped lines); reads in the entry's register | 1 sentence (~3 lines); smallest | 2 sentences (~5 lines); "strict" ending slightly foreign to the entry's register |

M1-r2 against the same axes: expresses #188 exactly (ordinal
relative to liveness/status only — the round-1 overreach removed);
adds no policy beyond the ruling; the keyed-read boundary is carried
by "read-back" + "separate" (no misclassification surface); the
no-query/no-identity branch is untouched by construction (condition
= branch (1)'s own two prerequisites); invariants 6–9 untouched;
stand-in misreading blocked explicitly; ONE sentence (~4 wrapped
lines) — smaller than M1 with equal-or-better coverage.

## 5. Recommendation (single candidate)

**M1-r2** (round-1 synthesis). Round 1 established — both reviewers
independently, on the same ground — that original M1's "first
provider-side read" exceeded the #188 ruling and that its
unconditional first sentence collided with the no-query branch; M1
is therefore WITHDRAWN as preferred and retained only as trail. M2
under-transmits (no stand-in guard — the exact substitution error
the #191 FAIL-ORDER runs exhibited). M3 carries the same
first-among-all overreach ("first provider-side operation") plus
E's emphasis register. M1-r2 is the smallest candidate that is
semantically EQUIVALENT to the ruling: ordinal relative to
liveness/status reads only, condition matching branch (1)'s two
prerequisites exactly, keyed-read boundary by construction
("read-back" + "separate"), and the stand-in guard — in one
sentence.

### Exact proposed patch (M1-r2; NOT applied by this gate)

Byte-exact, no free re-flow: line 127 (the single seam line, whose
bytes are enumerated below) is replaced by six lines; every other
line of the file is untouched. The anchor sentence lands on its own
line with its wording byte-identical; the deterministic seam split
is fully specified here — the future mutation gate applies exactly
these bytes, with NO "modulo re-wrap" latitude.

OLD (one line, verbatim):

```
  evidence. Run such mutations serially (one in flight), then resolve in
```

NEW (six lines, verbatim):

```
  evidence.
  Where the destination can be queried under the request identity,
  that read-back precedes any separate provider-side liveness/status
  read — and a liveness/status read never substitutes for
  destination-state evidence.
  Run such mutations serially (one in flight), then resolve in
```

Mechanical acceptance for the future mutation gate: (a) the diff is
exactly this one-line-for-six-lines replacement; (b) deleting the
four inserted sentence lines and rejoining the first and last NEW
lines with a single space reproduces the OLD line byte-exactly;
(c) the anchor text "Run such mutations serially (one in flight),
then resolve in" still occurs exactly once; (d) both branch bodies
and the SEVEN pre-existing invariant carriers (invariants 1–3 and
6–9) byte-identical — invariants 4–5 are carried by the inserted
sentence itself, not by pre-existing text; (e) the T2 marker
line in cross-model-review's SKILL.md byte-identical (Luna
round-1 addition); (f) a no-query/no-identity reading check: the
inserted sentence's condition is scoped BY PARAPHRASE to the same
two prerequisites branch (1) names (a destination query API and a
request identity to query by) — the mutation reviewers line-check
that correspondence; branch (1) acquires no obligation.

## 6. Provenance plan (for the future mutation gate; not applied now)

The eventual mutation adds, to the skill's Provenance (external-
systems entry lineage), a paragraph recording:

- #188: owner semantic determination — "settle what actually landed
  at the destination first" = STRICTLY-ORDINAL (destination
  interrogation before any provider-side liveness/status read).
- #191: preregistered transmission probe issue115-t2probe-v1 —
  campaign outcome O2; current-guidance arm LOW (1/6 · 1/6) and
  explicit-ordinal control HIGH (6/6 · 6/6) on both frozen matched
  fixtures; H2 (guidance-transmission gap) supported DIRECTIONALLY.
- Amendment purpose: **clarify transmission of an already-settled
  semantic requirement** — not a semantic change, not a response to
  a doctrine defect (none established). (This purely-clarifying
  characterization is valid precisely because M1-r2 adds no
  constraint beyond the ruling; round-1 review rejected the original
  M1 wording on exactly this test.)
- The amendment **implements #188's settled semantics; the E-arm
  served only as the experimental control** — it is not source text
  and none of its text is adopted.
- Evidence scope: claude-haiku-4-5-20251001, two matched fixtures,
  n=6 per arm; the probe supports "current wording did not reliably
  transmit" and "the tier can follow the explicit ordering" — it is
  NOT recorded as "the new wording is proven correct".
- The T2 marker (Section-A settlement) is untouched by the
  amendment; any marker change is a separate owner disposition.

## 7. Machine verification (design_checks.py; all read-only)

1. Fresh target pin: blob at HEAD == `28216fd8…`; anchor sentence
   occurs exactly once; frozen entry bytes == lines 123–154.
2. Patch simulation on a SCRATCH copy (M1-r2 exact byte patch):
   the seam line's replacement is the ONLY change; removal of the
   inserted lines and seam-rejoin reproduces the original file
   byte-exactly; the anchor sentence still occurs exactly once as a
   whole line; the SEVEN pre-existing invariant carriers
   (serial-execution, blind-retry ban, immediate-terminal no-query
   branch, authoritative-read rule, both-axes rule, idempotency
   carve-out, terminal-uncertain cap — invariants 1–3 and 6–9)
   remain present verbatim post-patch, while invariants 4–5 are
   carried by the inserted sentence itself.
3. E-similarity report: no ≥8-word verbatim run shared between any
   candidate (M1, M1-r2, M2, M3) and the E bytes. Scope honesty:
   this guard proves only the absence of verbatim copying at that
   granularity; semantic-policy import is controlled by the §4
   disposition analysis and this gate's human review, not by the
   n-gram check.
4. No canonical mutation by this gate: `git status` clean on
   `skills/` throughout.
5. Behavioral invocations 0; #115 OPEN (API); headroom/reserve
   accounting untouched (no executor call exists in this gate).
6. Future-mutation-gate obligations recorded (from round-1 review):
   the §5 mechanical acceptance list (a)–(f) — literal byte patch
   with no re-wrap latitude, T2-marker byte-check, and the
   no-query/no-identity reading line-check — binds the eventual
   mutation gate.

## 8. Review gate protocol

Luna Max + Sol Max, independent, same packet, verdicts not shared;
the ten owner questions; HOLD only for semantic correctness, scope
creep, ambiguity, or overclaim. Substantive wording disagreement →
one bounded Luna Ultra wording adjudication (never 2:1 auto-decide).
On 2/2 PROCEED (or Ultra-resolved no-blocker): reviews-only design
PR, then STOP at merge authorization. The canonical doctrine file is
not modified by this gate under any outcome.
