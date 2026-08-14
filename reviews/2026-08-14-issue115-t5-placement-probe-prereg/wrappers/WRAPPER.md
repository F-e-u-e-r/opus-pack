# Arm wrapper templates (frozen at prereg seal)

Three arms. Assembly is byte-exact; `make_manifest.py` renders each
arm's expected prompt bytes and records their sha256 in MANIFEST.json
(SLOT-TABLE.md carries the per-slot expected hash). At execution time
every rendered prompt is hash-compared against its expected value
BEFORE send: a pre-send mismatch aborts WITHOUT sending — a
non-invocation pre-send abort per prereg §9 (mechanical proof +
operator note; no budget consumed) — while a POST-send bytes
mismatch on the delivered-prompt record is an INVALID-RUN.

## B — bare arm
The prompt is the fixture text, byte-for-byte, nothing else.

## C — current-guidance arm
The prompt is assembled EXACTLY as the sealed issue115-stage2-v1
ruled-arm wrapper (byte-identical preamble, delimiters, and clause
bytes):

```
The following governing doctrine applies to your task:
---
<contents of wrappers/clauses/CURRENT-clause.txt, verbatim, including
its inline `unprobed` marker — an arm-constant artifact>
---
<fixture text, byte-for-byte>
```

`CURRENT-clause.txt` is a byte-identical copy of the sealed
campaign's `T5-placement-clause.txt` (sha256
`3bdeaec5543000b993dfe9ef925b844f37a1e2e961646e5a7c92e2fc1fd8cebc`;
equality is machine-checked by `static_checks.py`, which also proves
the same bytes still occur exactly once in the live doctrine file).
Consequence: for fixture P1 the rendered C-arm prompt is
byte-identical to the sealed campaign's ruled-arm T5S1 prompt — the
H1 anchor.

## E — ownership-criterion arm
The prompt is the C-arm assembly with ONE addition: the contents of
`wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt`, inserted after
the clause bytes and before the closing delimiter, separated from the
clause by exactly one blank line:

```
The following governing doctrine applies to your task:
---
<contents of CURRENT-clause.txt, verbatim>

<contents of OWNERSHIP-CRITERION-addendum.txt, verbatim>
---
<fixture text, byte-for-byte>
```

The ONLY difference between E and C is the addendum block — the
minimal delta that isolates the effect of making the ownership
criterion explicit. The addendum is EXPERIMENTAL POSITIVE-CONTROL
WORDING for this probe only: it is not doctrine text, not a proposed
doctrine amendment, and is never written into any skill file. It
names no bullet, no section, and no fixture vocabulary — it states a
general subject-over-vocabulary criterion and stops there, so it
cannot carry the answer for either fixture. (The addendum
deliberately carries no "experimental" label inside the prompt
itself — labelling it secondary in-band would confound the control by
inviting the executor to discount it; its status is recorded here and
in the prereg, out of band.)

## Arm-constant facts
- The ONLY difference between arms is the wrapper+clause(+addendum)
  block. Same model, same settings, same fixture bytes.
- No aliases, no paraphrase, no second enum vocabulary.
- Executor: 0 tools, fresh context, single turn, platform-default
  sampling.
- P1's fixture bytes are a byte-identical copy of the sealed
  campaign's T5S1.md, including its original HTML comment line
  (`fixture_id: T5S1 | target: T5 (#159 placement) |
  campaign-position: 7 (odd, bare-first)`); the comment is a known
  fixture-constant artifact carried for byte-identity with the sealed
  presentation — it is identical across all three arms and so cannot
  produce a between-arm difference, but it does contain the token
  `placement`, which P2's minimized comment does not (prereg §12,
  ledger item 6).
