# Arm wrapper templates (frozen)

## bare arm
The prompt is the fixture text, byte-for-byte, nothing else.

## ruled arm
The prompt is assembled EXACTLY as:

```
The following governing doctrine applies to your task:
---
<contents of the target's clause file from wrappers/clauses/, verbatim,
including its inline `unprobed` marker(s) — an arm-constant artifact>
---
<fixture text, byte-for-byte>
```

Clause-file binding (per-marker injection, sealed §C): T1F1 →
T1-clause.txt; T2S1/T2S2 → T2-clause.txt; T3F1 → T3-clause.txt;
T4S1/T4S2 → T4-clause.txt; T5S1 → T5-placement-clause.txt (ONLY);
T5S2 → T5-narrative-clause.txt (ONLY); T6S1/T6S2 → T6-clause.txt;
T7S1a/T7S1b/T7S2 → T7-clause.txt.

The ONLY difference between arms is this wrapper+clause block. No
aliases, no paraphrase, no second enum vocabulary. Executor: 0 tools,
fresh context, single turn, platform-default sampling.
