# Orientation summary — ⑤ runtime-artifact correspondence

## Disposition: PARTIAL-GAP

The binding **principle** exists (security-architect: "what executes must be
verifiably bound to what was reviewed" — a provenance chain from reviewed source +
build recipe to the running artifact, framed as an ingestion-pipeline concern). The
fail-closed **consequence** exists (operational-rigor's opaque-dependency default).
What was missing is the **per-candidate recognition/verification trigger** at the
reviewer's own working point — the install gate (op-rigor §2) and the vetting
procedure (skill-vetting §1) never told the reviewer to find the artifact the
runtime will actually select and establish its correspondence to the reviewed
source. Principle present + consequence present + trigger absent = PARTIAL-GAP (not
a wholly new principle, not a mere consequence tweak).

## Abstraction: L2

**L2 = reviewed-source ↔ runtime-selected executable-artifact correspondence.**
The core question: is what the reviewer read actually the executable truth the
runtime last selects?

- **Not L1** (`.pyc`-specific): too narrow — `.pyo`, other cache tags, a shipped
  `.so`, a source-less `dist/bundle.js`, a compiled hook all bypass a `.pyc`-only
  rule at once.
- **Not L3** (all runtime-reachable unanalyzed artifacts, incl. data/config):
  overbroad — converges on all-supply-chain and overlaps existing rules. Recorded
  as a broader-generalization candidate, **deliberately NOT activated**.

## P1–P8 orientation (prior session; mechanism re-verified first-hand this session)

The original P1–P8 probe harness ran in an earlier session and its artifacts were
not carried into this session's workspace. The mechanism it established is
independently re-verified first-hand this session by the D1–D11 battery in
`harness/`, which is the primary evidence; P1–P8 is summarized here for the record:

- **P1 UNCHECKED-DECOY** — an unchecked-hash pyc executes its payload without
  validating the clean decoy source.
- **P2 CHECKED-HASH mismatch** — a checked-hash pyc whose header ≠ current source is
  invalidated and recompiled (a real freshness control).
- **P3 TIMESTAMP-INVALIDATION** — the normal timestamp invalidation control holds.
- **P4 TIMESTAMP-COLLISION** — forging a pyc's stored mtime+size to match the source
  runs the stale payload; carries a **filesystem-granularity caveat** (mtime
  integer-second resolution is FS/ENV-sensitive).
- **P5 SOURCE-ONLY** — a source-only candidate clears normally (the rule must not
  degrade to "Python is dangerous").
- **P6 DIGEST-NOT-SEMANTICS** — a whole-tree digest is stable and non-anomalous over
  a source/pyc-divergent tree; only a byte-flip moves it. Digest proves identity,
  not correspondence.
- **Source-less / in-tree payload** — a bare `mod.pyc` (no source) and a committed
  `__pycache__` payload are runtime-reachable executable content with no source to
  review.
- **Out-of-tree central cache** — the Apple system Python's baked
  `sys.pycache_prefix` routes a sourced import's pyc to a central cache **outside**
  the candidate tree. This is **environment-specific supporting evidence, not a
  universal premise**: it motivated the out-of-tree discovery scope (correspondence
  must be established at the runtime-selection point, not the tree-identity point).

## Environment

CPython **3.9.6**, **macOS 26.5.2 arm64**, **Apple system Python**
(`/usr/bin/python3`, `cache_tag = cpython-39`). `sys.pycache_prefix` is baked to
`~/Library/Caches/com.apple.python`; `-X pycache_prefix=<dir>` reroutes it
deterministically (used to keep the D1–D11 harness self-contained).
