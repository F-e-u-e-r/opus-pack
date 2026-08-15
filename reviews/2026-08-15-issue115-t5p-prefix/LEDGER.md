# issue115-t5pprobe-v1 — execution LEDGER (prefix grant)

Grant scope: identity dry-run + the two frozen smokes ONLY (slot 0,
S1, S2). All 36 scored slots LOCKED. No retry authorized. Budget
envelope: 39 planned / 50 hard cap (NEW campaign accounting). The
unallocated hard-cap space is NOT an execution entitlement; the T2
probe's headroom 11 and the sealed stage-2 reserve 18 stay locked and
untouched throughout.

Unit-start main: `6fe6813bcc35edb86a8b92b4aaaa7f9ba3459ef7` (PR #199 merge commit).

| # | slot | kind | fixture | api_message_id | reported model | digest binding | outcome |
|---|---|---|---|---|---|---|---|
| 1 | 0 | DRY-RUN | — | msg_011Ce4CjrMz7qFhHCnXK8SYW | claude-haiku-4-5-20251001 | n/a (identity probe; prompt byte-identical to the sealed and T2 dry-run prompt, sha `d8adb66f…`) | identity CONFIRMED; intact ('OK'); wire captured |
| 2 | S1 | SMOKE | P1 | msg_011Ce4CmcNfgJttF3fBwDk2s | claude-haiku-4-5-20251001 | EXACT (`9617591b…`, pre-send + decoded wire) | SMOKE PASS 5/5; P1 CLEARED |
| 3 | S2 | SMOKE | P2 | msg_011Ce4CnBqZrPpvb5szbMYMo | claude-haiku-4-5-20251001 | EXACT (`60259f5a…`, pre-send + decoded wire) | SMOKE PASS 5/5; P2 CLEARED |

## Accounting at STOP (prefix complete)

- dry-run: **1**
- smoke: **2**
- scored: **0**
- total used: **3/50**
- prereg planned remaining: **36** (all scored; ALL LOCKED)
- hard-cap space unallocated: **47 physical slots — NOT an
  entitlement.** The only planned next unit is the 36-observation
  scored unit, and it is not authorized.
  **hard-cap remaining physical capacity is not an available reserve
  and does not itself authorize execution.**
- old #115 reserve 18: **untouched**; T2 probe headroom 11:
  **untouched**
- doctrine / marker / fixture / prereg / rubric mutation: **0**
- retries used: 0 (none authorized); campaign exceptions: 0;
  pre-send aborts: 0; zero-request preflight events: 0
- operator notes (canonical dispositions):
  1. One verifier-only correction, before any request was issued: the
     unit-start `consumed == 0` predicate matched `SLOT-TABLE.md` on a
     filename substring (`slot`). Raw evidence (`git ls-files` vs the
     filesystem) proves that file is a DESIGN artifact committed in
     `62c9e77`, and that the package holds zero untracked files. The
     predicate was corrected to "untracked files in the package" and
     re-verified against the same existing evidence. No model request
     was re-sent; this is a verification-method correction, not a
     fixture/design/campaign repair, and not a campaign exception.

## State

Campaign state: RUNNING, halted at the grant boundary (STOP — not
HOLD, no exception). Both fixtures CLEARED by smoke. The next
invocation, if ever, is scored slot 1 (P1, arm B, n=1); it requires a
fresh owner grant unlocking the 36-observation scored unit as an
indivisible analysis unit.
