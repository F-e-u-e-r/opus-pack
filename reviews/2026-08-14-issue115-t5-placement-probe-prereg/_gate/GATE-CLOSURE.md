# GATE-CLOSURE — T5-placement ownership probe, preregistration v1

Package: `issue115-t5pprobe-v1`. Baseline main at authoring:
`c2fc127d7d2d6263439094553e4a6aa1575eeaee`.

**STATUS: CLOSED by owner adjudication after a bounded mechanical
repair. There was NO 2/2 PROCEED, and there was NO round 6.** This
record states that plainly rather than presenting a clean dual
approval that did not occur.

## Gate protocol as run

Two independent design reviewers, same packet, verdicts never shared
between them, each isolated in its own working directory with the
packet as the only file present. Identity confirmed per run from the
CLI banner, not from the review text.

- Reviewer A: `gpt-5.6-luna`, reasoning effort `max`
- Reviewer B: `gpt-5.6-sol`, reasoning effort `max`

HOLD was licensed only for identifiability, correctness, leakage, or
overclaim; from round 5 the owner narrowed it further to current-byte
correctness. Every HOLD finding was reproduced first-hand by the
author before any repair — none was actioned on a reviewer's
assertion alone.

## Round-by-round trail (verdict files in this directory)

| round | A (luna max) | B (sol max) | what the round settled |
|---|---|---|---|
| r1 | PROCEED | HOLD ×1 | P2's owner shared the token `codebase` with the rule; the control could not discriminate governance from surface attachment. Fixture repaired; the lexical claim moved from prose to a machine-checked type-set invariant. |
| r2 | PROCEED | HOLD ×2 | The type-set invariant was insufficient: the owner tied a competitor on a frequency-weighted score and uniquely shared two word bigrams. Also, four passages overclaimed what P2 licenses. Invariant widened to three measures; claim scoping rewritten. |
| r3 | PROCEED | HOLD ×1 | A subword route survived with no shared token at all (`alive` ↔ `outlives`). Invariant widened to four measures. |
| r4 | HOLD ×1 | HOLD ×2 | **Converged blocker:** two §8 branch texts still carried stale `token-level` terminology. **Split finding:** residual owner-exclusive features below the measured widths (`its`, `one`, and a raw-token `its` hidden by the content-token stopword filter) — B blocking, A record-only under the bounded claim. |
| r5 | PROCEED | HOLD ×3 | Design axes confirmed by both. B additionally found three record-integrity defects: a stale quoted rule sentence, a stale axis count, a stale draft count. |

## How r4 is recorded

Not as "a reviewer was wrong":

- **r4 common blocker** — stale terminology in the locked outcome
  mapping. Reproduced, fixed.
- **r4 split finding** — a residual surface feature. Rather than
  adjudicating whether it blocked, it was **removed at the source**
  and the invariant was **generalized into an exhaustive
  owner-exclusivity sweep** over a measure family (raw unfiltered word
  tokens plus word-internal character n-grams at every width 3–8), so
  the whole class is barred mechanically instead of one instance being
  patched.
- **r5** then confirmed the current bytes on every design axis, from
  both reviewers.

## r5 disposition (owner adjudication)

> r5: Luna PROCEED / Sol HOLD on three mechanically reproduced
> record-integrity findings. Owner adjudication accepted all three
> factual findings, classified #1/#2 as must-fix record correctness
> and #3 as record-only-but-fixed, authorized a bounded
> self-description repair, and prohibited further model review.
> Post-fix mechanical closure satisfied; no r6.

All three findings were verified first-hand before repair:

1. **Stale quoted rule text** — prereg §4 and `rubrics/R-P2.md` both
   quoted `"Record the clearing release beside its figure"` while the
   fixture bytes said `beside the figure`. MUST-FIX: both documents
   quote the rule in order to FIX a reading at seal, so a quotation
   that does not match the fixture would bind the durable record to
   text that does not exist. (The author's own first sweep missed the
   prereg occurrence because the document wraps it across two source
   lines — a single-line grep cannot see it. The replacement check
   normalizes whitespace BEFORE extraction for exactly this reason.)
2. **Stale axis count** — prereg §8 called the invariant
   "four-measure" while §4 enumerates five axes (i)–(v). MUST-FIX: a
   prereg may not be sealed carrying a known-false self-description,
   even one with no identifiability consequence.
3. **Stale draft count** — a `static_checks.py` comment said "Three
   successive drafts" while enumerating four and while both prose
   documents said four. SHOULD-FIX, repaired in the same unit: the
   record-only classification was reasonable, but there is no reason
   to seal a known-false line while already repairing self-description
   drift.

## Bounded repair scope (authorized; nothing else touched)

Four sites, three finding classes:

1. prereg §4 — quoted rule sentence corrected to the current bytes
2. `rubrics/R-P2.md` — same quotation corrected
3. prereg §8 — `four-measure` → `five-axis`, consistent with §4
4. `static_checks.py` comment — `Three` → `Four` successive drafts

Explicitly NOT changed under this authorization: P1/P2 fixture bytes,
owner/rule semantics, the E-arm control wording, the hypotheses and
outcome mapping, sample size and budget, the UNGRADABLE/retry/stop
rules, the lexical invariant itself, or any other design wording. The
repair touched the record's self-description only.

## Coverage gap this round exposed, and what closed it

The 164 checks in force at r5 verified hashes, invariants, and
execution-facing properties. They did **not** cover package
self-description consistency — whether the document's prose describes
the package truthfully — which is why all 164 could pass while three
stale statements stood. This is a coverage gap that r5 exposed, not a
bug in those checks.

A narrow **self-description consistency family** now closes it
(`static_checks.py` §15), taking the suite to **175 checks**:

- **quoted fixture text** — every quoted span sharing a 4-word
  shingle with a fixture rule must be a whitespace-normalized
  substring of that rule; plus the known-stale literal banned. Text is
  normalized BEFORE extraction so a line-wrapped quotation cannot
  escape.
- **axis-count consistency** — the count is DERIVED from §4's
  enumerated markers and compared against every self-description
  elsewhere, so no second hard-coded numeral can produce a false
  green.
- **draft-history consistency** — the numeral must be identical at
  all three sites, and the known-stale phrase is banned package-wide.

**Two-sided proof (the checks are shown able to fail).** Each defect
was re-injected into a copy of the real bytes and the real script was
driven against it: stale quotation → exit 1 naming the offending span;
stale axis count → exit 1 reporting `derived=5 stated=['four']`;
stale draft count → exit 1 listing the disagreeing sites. The tree was
restored and the suite returns to 175/175 PASS, exit 0.

One defect in the new checks was caught by that proof and fixed before
closure: the quoted-text check originally used the same predicate for
"is this a rule quote?" and "does it match the rule?", so a stale
quote was silently reclassified as not-a-quote and the check could
never fail. Relevance is now partial (a shared 4-word shingle) and
correctness is full containment.

## Closure state

- Behavioral invocations: **0**. No fixture was ever sent to an
  executor; this gate designed and preregistered only.
- Design axes confirmed by both reviewers at r5: invariant coverage,
  axis labelling, frozen semantics intact, identifiability preserved,
  no executable leakage, no new behavioral or design blocker.
- P1's bytes untouched throughout; the anchor stays machine-proven
  (rendered P1×C equals the sealed campaign's recorded ruled-arm
  prompt hash, P1×B its bare hash).
- Static suite: **175/175 PASS**. Repo-wide `.github/checks.py`: all
  checks passed.
- No existing budget pool used: `issue115-stage2-v1` reserve 18 and
  `issue115-t2probe-v1` headroom 11 both untouched.
- Issue #115: **OPEN**.
- All ten r1–r5 verdict files retained in this directory, including
  every HOLD.

Next step after this gate: a reviews-only PR carrying the prereg
package, stopping at merge authorization. Execution of the probe
itself requires a separate, future owner grant that this gate does
not provide.
