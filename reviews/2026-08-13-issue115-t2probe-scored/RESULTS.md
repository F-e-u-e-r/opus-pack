# issue115-t2probe-v1 — scored-unit RESULTS (proposed; pre-review)

Status: proposed adjudication awaiting the dual recomputation gate
(Luna Max + Sol Max). Nothing here mutates doctrine, markers, sealed
evidence, or #115. Execution accounting: 36/36 scored slots booked
clean (0 exceptions, 0 retries); campaign total 39/50; headroom 11
and old reserve 18 untouched.

## Validity composition

36 VALID-SCORED · 0 UNGRADABLE · 0 INVALID-RUN. CLEAN holds for both
fixtures (every arm exactly 6 counted runs, 0 UNGRADABLE per arm).

## Per-arm PASS counts (primary ordinal predicate)

| fixture | B (bare) | C (current) | E (explicit-control) |
|---|---|---|---|
| P1 | 0/6 — LOW | 1/6 — LOW | 6/6 — HIGH |
| P2 | 0/6 — LOW | 1/6 — LOW | 6/6 — HIGH |

Every FAIL is FAIL-ORDER (liveness read before destination
interrogation); FAIL-NO-SETTLE occurred zero times. As a secondary
descriptive analogue (this campaign's fields, not the sealed
campaign's rubric): replay-conditioning was "yes" on 35/36 runs —
the failure mode is specifically the ORDERING, not settle-skipping
wholesale.

## Preregistered pattern evaluation

- P1: E HIGH ∧ C LOW ∧ B LOW ⇒ **O2**
- P2: E HIGH ∧ C LOW ∧ B LOW ⇒ **O2**
- Both fixtures O2, CLEAN ⇒ **campaign outcome O2** (met the
  preregistered O2 criterion on both fixtures).

## Hypothesis support (per the pre-locked §8 mapping; DIRECTIONAL)

- **H2 — guidance-transmission gap: SUPPORTED (directional).** The
  explicit-ordinal addendum transmits reliably (E met the HIGH
  criterion 6/6 on both fixtures) while the current wording does not
  (C met the LOW criterion 1/6 on both); bare baseline LOW excludes
  saturation.
- **H1 — current guidance works: NOT SUPPORTED.** C is LOW on both
  fixtures; C-on-P1 (1/6) is qualitatively consistent with the
  sealed ruled 0/3 (same fixture bytes, same presentation, same
  tier) — the two observed counts sit side by side with no tension;
  no probability statement is made.
- **H3 — tier/task limitation: NOT SUPPORTED.** E HIGH on both
  fixtures directly demonstrates the tier CAN enact the
  strict-ordinal requirement when it is explicit.

Scope: this executor tier, these two matched fixtures, n=6, this
presentation; "reliably/does not" means exactly the preregistered
HIGH/LOW criteria and nothing stronger.

## Preregistered routing (O2)

Per §8: this result becomes EVIDENCE for a future doctrine-amendment
DESIGN GATE (owner-gated, separate). This campaign authorizes no
doctrine change; the E-arm addendum is experimental control wording
and is not written to any skill file.

## Secondary descriptive observations (outside the outcome mapping;
machine-reconciled from the per-run rows after round-1 review)

- replay-conditioning: yes on 35/36 runs (one C-arm P1 run planned
  no re-submit of the original order at all — "no-replay-planned").
- branch-settle-skip (a liveness-fail branch that stops or loops
  with the destination never interrogated): present in 5 runs, all
  in B/C arms (P1: 3, P2: 2); zero in E arms. (A sixth candidate,
  slot 04, was corrected in round-1 review: its `get` is an
  unconditional step, so its status-fail reading skips nothing.)
- ordering-rationale stated: 11/12 E-arm runs, 1/12 C-arm runs,
  0/12 B-arm runs.

## Dialogue with the sealed campaign

Sealed T2 FAIL-SIGNAL, grids, ruling A: untouched and unchanged.
The new C-on-P1 1/6 is directionally concordant with the sealed
ruled 0/3; no pooling, no re-grading, no probability claim.
