# Design review (ROUND 2) — a correspondence limb for the source-review install gate

You are reviewing a **proposed wording change** to an agent-discipline doctrine
pack (terse, imperative instruction files a weaker model must execute). This is a
**wording/design review, not a code diff** — there is no unified diff to count;
judge the proposed text against the rubric at the end. Everything you need is
inlined; you cannot see the repository.

Return your review ending with a final line that is exactly `PROCEED` or
`FIX <comma-separated list of must-fix items>`.

## 0. Review history and what changed (read this first)

**Round 1** (independent luna + sol pass) raised three issues, all resolved in the
current text: freshness metadata no longer stated as proof (§4a freshness
sentence); discovery scope broadened from "shipped" to every runtime-selected
artifact including out-of-tree/central caches, with data/config excluded (§4a
opening, §4b step 4); local-regeneration clearance made digest-explicit under a
named toolchain (§4a clearer (a)).

**Round 2**: one reviewer PROCEEDed; the other raised a single precision defect in
the freshness sentence's CPython hash-policy claim — now corrected (§4a freshness
sentence, §5 D1 gloss). Under the default hash-`.pyc` policy an `UNCHECKED_HASH`
header's stored source-hash is not *compared* to the source (the header is still
read/classified); `--check-hash-based-pycs` can force that comparison for UNCHECKED
or disable it for CHECKED; a matching `CHECKED_HASH` binds only the header to the
current source, never the bytecode body. First-hand verified: unchecked-mismatch
runs the payload under the default policy but recompiles under `always`;
checked-mismatch recompiles under the default policy but runs the payload under
`never`.

Confirm these are resolved, and review the whole afresh.

---

## 1. The gap being closed

A source-code reviewer, following the pack's existing install/vetting gate, reads
the **source text** of a candidate and clears it. But a Python (or JS, or native)
runtime does not necessarily execute that source — it may load a **shipped or
out-of-tree compiled / cached / bundled artifact** (a `.pyc` in a central cache, a
minified bundle, a checked-in `dist/`) whose bytes were never produced from the
reviewed source. The reviewer clears clean source while the interpreter executes
different, unreviewed bytes.

The pack **already** has the underlying *principle* (security-architect, verbatim):

> **What executes must be verifiably bound to what was reviewed.** For
> compiled/bundled/generated code that means a provenance chain from reviewed
> source + build recipe to the running artifact; …

…and it already fails closed on opaque dependencies. What is **missing** is the
**recognition/verification trigger at the reviewer's actual working point** — the
install gate and the vetting procedure never tell the reviewer to find the
artifact the runtime will select and establish its correspondence to the reviewed
source. This is a PARTIAL-GAP: principle present, consequence present, trigger
absent.

## 2. Abstraction level (locked by the owner as L2)

- **L2 (chosen):** *reviewed-source ↔ runtime-selected executable-artifact
  correspondence.* The core question: **is what the reviewer read actually the
  executable truth the runtime last selects?**
- **NOT L1** (`.pyc`-specific): too narrow — `.pyo`, other `cache_tag` pycs,
  shipped `.so`, a source-less `dist/bundle.js`, a compiled hook all bypass a
  `.pyc`-only rule immediately.
- **NOT L3** (all runtime-reachable unanalyzed artifacts, incl. data/config):
  overbroad — converges on all-supply-chain, overlaps the existing
  opaque-dependency + full-source rules. Recorded as a broader-generalization
  candidate; deliberately **not** activated.

## 3. Existing doctrine context (verbatim, so the review is self-contained)

**operational-rigor §2 — the install gate the limb attaches to:**

> - **Third-party executable content** (hooks, scripts, plugins) installs only
>   after: provenance check (owner/age/fork metadata), full source read, one
>   written sentence stating why it is inert or safe here, and a fixture test of
>   its load-bearing behavior — for hooks/gates, both the allow path and the
>   block path. For security-critical parsers/gates … add a cross-family
>   adversarial review of the source … and re-gate on any upstream update — a
>   passed gate certifies the version read, not the file path.
> - **Instruction files are executable content.** …

**skill-vetting §1 — the vetting procedure the pointer attaches to:**

> 1. **Provenance.** …
> 2. **Take the opening digest.** …
> 3. **Read the FULL source** — every SKILL.md, command file, hook, script, and
>    referenced doc, not a sample. … Skip only files that demonstrably cannot
>    carry instructions (images, fonts, archives …).
> 4. **Hunt the trojan-shape checklist (§2)** against what you read. …
> 5. **For an executable candidate** … run a fixture test … both sides …
> 6. **Write the fail-closed verdict** …

## 4. The proposed change (revised)

### 4a. operational-rigor §2 — NEW bullet (canonical home), placed immediately after "Third-party executable content", adjacent to "Instruction files are executable content"

> - **A source review clears executable *behavior* only when the
>   runtime-selected bytes are bound to what was reviewed.** The full-source read
>   above clears source *text*; a runtime can load a compiled, bundled,
>   generated, or cached artifact that it selects in preference to — or in the
>   absence of — that source, whether that artifact is shipped in the candidate
>   tree, installed elsewhere, or resolved from an external/central cache or load
>   path (a `.pyc`, a minified bundle, a checked-in `dist/`, a build cache). Such
>   an artifact's executable contents are cleared only when the runtime-selected
>   bytes are themselves reviewed, or an independent path establishes those
>   *exact* bytes were produced from the reviewed source under a named
>   build/compile recipe. Legitimate clearance: (a) remove any competing shipped
>   or cached artifact, regenerate from the exact reviewed source under a named
>   toolchain/recipe, and confirm the bytes the runtime then selects match the
>   regenerated artifact by digest; (b) bind the exact artifact bytes by digest to
>   the reviewed source + recipe via reproducible/attested build evidence; or (c)
>   review the runtime-selected artifact itself, when it is reviewable as
>   source-equivalent, as the executable truth. A stable tree digest proves
>   identity, not correspondence. Cache-validity metadata is at most a freshness
>   *signal*, never evidence of correspondence: a timestamp is forgeable; a
>   hash-based `.pyc`'s stored source-hash is, under the default policy, either
>   not compared to the source (an `UNCHECKED_HASH` header) or, when compared and
>   matching (`CHECKED_HASH`), binds only that header to the current source, never
>   the bytecode body to it — and whether that comparison runs at all is a runtime
>   policy, not a guarantee. A filename or "generated" claim proves nothing. An artifact the runtime may select whose
>   correspondence you cannot establish is a finding — fail closed (the
>   opaque-dependency default); a source-only candidate with no such artifact is
>   not a finding on this ground. This operationalizes security-architect's "what
>   executes must be verifiably bound to what was reviewed" at per-candidate
>   install/vetting time.

### 4b. skill-vetting §1 — NEW step inserted between step 3 (Read FULL source) and step 4 (Hunt checklist); following steps renumber 4→5, 5→6, 6→7 (bare pointer, NOT a §2 checklist item)

> 4. **Bind the runtime-selected bytes to what you read.** Step 3 clears source
>    *text*, not the bytes the runtime will load. Identify every executable
>    artifact the target runtime may select for this candidate — whether shipped
>    in the candidate tree, installed elsewhere, or resolved from an
>    external/central cache or load path (a `.pyc`/`.pyo`, a built bundle, a
>    checked-in `dist/`, a populated cache), but not unrelated data or config
>    (that is the L3 line, not this gate) — and apply operational-rigor §2's
>    runtime-selected-artifact correspondence gate to each before proceeding.
>    Done: each such artifact cleared by that gate or recorded as a finding.

**Design intent:** op-rigor §2 is the single canonical home (full statement +
clearers + caveats + fail-closed). skill-vetting carries only a bare routing
pointer (identify → apply op-rigor gate → continue), NOT a restatement, and does
NOT go into §2's lexical trojan-shape checklist (wrong altitude: that checklist is
content-pattern matching; this is an artifact-correspondence obligation).

## 5. First-hand mechanical evidence (run on CPython 3.9.6, cache_tag cpython-39)

A 10-case harness drove the real import machinery. Each "HIT" case ships a **clean
decoy `.py`** a source reviewer would clear, while the runtime executes a
**payload**. All 10 cases matched pre-registered expectations.

| Case | Setup | Result | What it proves |
|---|---|---|---|
| D1 UNCHECKED-DECOY | clean decoy `.py` + UNCHECKED hash `.pyc` = payload | HIT (executed PAYLOAD) | unchecked pyc runs without validating its stored source-hash against the source under the default policy (the header is still read/classified) |
| **D2 FORGED-CHECKED-HASH** | clean decoy `.py` + **CHECKED** hash `.pyc` whose header source-hash = hash(decoy) but body = payload | **HIT; freshness check PASSES** (`recomputed_source_hash == header == 98802ca4…`), yet `executed_marker=PAYLOAD`, payload side effect ran | **checked-hash validates *freshness*, never *correspondence*** — the runtime's own source-hash check passed on the real clean source while executing bytes never produced from it |
| D3 CHECKED-HASH-MISMATCH | header hash = hash(other), body = payload | recompiled → DECOY; payload did NOT run | control: checked-hash *does* fire on header≠source — a real invalidation control, but only of freshness |
| D4 TIMESTAMP-COLLISION | timestamp `.pyc`, header mtime+size forged = decoy's | HIT | mtime/size are forgeable metadata (caveat: int-second granularity is FS/ENV-sensitive; forged deterministically here) |
| D5 SOURCELESS | bare `mod.pyc`, no `.py` | HIT | a source-less compiled artifact is runtime-reachable with no source to review |
| D6 SOURCE-ONLY | clean `.py`, no pyc | CLEAR (executed CLEAN) | rule must NOT degrade to "Python is dangerous" |
| D7 LOCAL-REBUILD | ship D2 forge, then remove + `py_compile` from exact source | CLEAR (executed DECOY; `regen_digest == honest_digest`) | legitimate clearance (a): regenerate from exact source + verify selection by digest |
| D8 VERIFIED-BUILD-PROVENANCE | reproduce artifact from reviewed source; compare digests | good `.pyc` digest == reproduction (CLEAR); forge digest ≠ reproduction (finding) | legitimate clearance (b): digest binding; a "generated" claim alone cannot separate good from forge |
| D9 DIGEST-IDENTITY | divergent tree (clean source + payload pyc) | stable, non-anomalous whole-tree digest; changes only on byte-flip | digest proves IDENTITY, not correspondence — a divergent tree hashes clean and stable |
| D10 ACTIVATION-CROSS | (a) decoy src + ungated payload pyc; (b) clean src w/ dormant env-gated branch, source-only; (c) decoy src + gated payload pyc | (a) diverges, no gate → pure artifact-finding; (b) no divergence, gate present → pure activation-finding; (c) both | artifact-correspondence and activation-gated-payload are **orthogonal axes** — neither folds into the other |

Prior orientation (P1–P8, same interpreter): unchecked-decoy → payload;
checked-hash mismatch → recompile; timestamp invalidation control holds; timestamp
collision → stale payload; source-only → source; digest proves identity not
semantics; plus a source-less case and an **out-of-tree central-cache** observation
(the runtime resolved a sourced import's pyc to a central cache outside the
candidate tree — motivating §4's out-of-tree discovery scope: correspondence must
be established at the runtime-selection point, not the tree-identity point).

## 6. Rubric — judge the proposed wording (4a + 4b) against these axes

1. Does it add a **recognition/correspondence trigger at the reviewer's working
   point**, rather than merely restating security-architect's principle?
2. Are **runtime selection** and **source review** clearly separated as distinct
   acts?
3. Is a **tree digest** treated as identity only (never correspondence)?
4. Are **CHECKED_HASH / timestamp** freshness signals kept as freshness evidence,
   never elevated to provenance/correspondence?
5. Does the **local-regeneration** clearance require verifying source AND build
   path AND runtime selection (by digest, not just recompilation/behavior)?
6. Does **trusted build provenance** require *exact artifact binding* (by digest),
   not a "generated" claim?
7. Are **source-only** candidates and a **directly-reviewed** runtime-selected
   artifact NOT penalized (no "all compiled code is bad")?
8. Do artifact-correspondence (this rule) and activation-gated-payload (the
   existing §2 check) stay **orthogonal** — neither folded into the other?
9. Is the rule kept at **L2** (candidate executable selection) and NOT expanded
   into an L3 all-supply-chain / all-runtime-reachable-artifact / data-config
   totality?
10. Do op-rigor §2 (canonical, full statement) and skill-vetting §1 (bare pointer)
    maintain a **single source of authority** — no drift, no duplicated criteria?

Also flag: internal contradictions, wording a weaker executing model could
misread, over-narrow phrasings with an immediate same-shape bypass, or anything
that would make a clean source-only review fail.

End with `PROCEED` (wording is sound to adopt as-is) or `FIX <list>` (specific
must-fix wording defects).
