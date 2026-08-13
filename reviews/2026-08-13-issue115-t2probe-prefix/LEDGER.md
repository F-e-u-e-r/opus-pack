# issue115-t2probe-v1 — execution LEDGER (prefix grant)

Grant scope: identity dry-run + frozen smoke prefix ONLY (slot 0, S1,
S2). All 36 scored slots LOCKED. No retry authorized. Budget envelope
accepted: 39 planned / 50 hard cap (NEW campaign accounting); the 11
unallocated headroom is not free reserve; old issue115-stage2-v1
reserve 18 locked and untouched throughout.

| # | slot | kind | fixture | api_message_id | reported model | digest binding | outcome |
|---|---|---|---|---|---|---|---|
| 1 | 0 | DRY-RUN | — | msg_011CdzTabYV7LmB2phKgGFbE | claude-haiku-4-5-20251001 | n/a (identity probe; prompt byte-identical to sealed campaign dry-run, sha d8adb66f…) | identity CONFIRMED; intact ('OK'); wire captured |
| 2 | S1 | SMOKE | P1 | msg_011CdzTf3XXzvV2RNGB9v7UC | claude-haiku-4-5-20251001 | EXACT (1b35c236…, pre-send + decoded wire) | SMOKE PASS 5/5; P1 CLEARED |
| 3 | S2 | SMOKE | P2 | msg_011CdzTpty82rtDDvp4fnwXw | claude-haiku-4-5-20251001 | EXACT (3a5f4c27…, pre-send + decoded wire) | SMOKE PASS 5/5; P2 CLEARED |

## Accounting at STOP (prefix complete)

- dry-run: **1**
- smoke: **2**
- scored: **0**
- total used: **3/50**
- prereg planned remaining: **36** (all scored; ALL LOCKED)
- hard-cap unallocated headroom: **11 untouched**
- old #115 reserve: **18 untouched**
- doctrine / marker mutation: **0**
- retries used: 0 (none authorized); campaign exceptions: 0;
  pre-send aborts: 0; zero-request preflight events: 1 (before slot
  0, deliberate malformed-flag parse probe, mechanically proven zero
  request — not an invocation; artifacts in session scratchpad)
- operator notes (canonical dispositions):
  1. S1 wire-verification false-FAIL = operator verification
     implementation issue; the ant CLI's JSON escaping required
     decode-then-compare rather than encoded-string comparison. The
     wire payload itself had NO mismatch; the actual request was
     correctly sent; the invocation is valid; this is NOT a campaign
     exception; it does not change the smoke outcome; and
     decode-then-compare is a verification-method correction, not a
     fixture/wrapper/campaign repair. (Detail:
     smoke-s1/smoke-checklist-result.md.)
  2. S1 usage.input_tokens: the preliminary operator-entered value
     254 was rejected by mechanical reconciliation before durable
     close; the canonical value is the machine-derived 260. 254 was
     never a valid campaign fact; the canonical receipt carries only
     260. (Reaffirms compute-and-paste for every numeral, not only
     hashes.)

## State

Campaign state: RUNNING, halted at the grant boundary (STOP — not
HOLD, no exception). Both fixtures CLEARED by smoke. The next
invocation, if ever, is scored slot 1 (P1, arm B, n=1) — it requires
a fresh owner grant deciding whether to unlock the full
36-observation scored unit or bounded sub-units.
