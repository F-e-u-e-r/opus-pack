# Final wording — R3-reviewed blocks as landed

Extracted verbatim from the landed skill files on branch
`runtime-artifact-correspondence`. Both are byte-faithful (whitespace-normalized)
to the R3-reviewed blocks; the only substantive-adjacent change is the single inline
marker on 4a's opening sentence.

## operational-rigor §2 — canonical correspondence limb (4a, as landed)

- **A source review clears executable *behavior* only when the
  runtime-selected bytes are bound to what was reviewed** (`unprobed` —
  see Provenance). The full-source read above clears source *text*; a
  runtime can load a compiled, bundled, generated, or cached artifact that
  it selects in preference to — or in the absence of — that source,
  whether that artifact is shipped in the candidate tree, installed
  elsewhere, or resolved from an external/central cache or load path (a
  `.pyc`, a minified bundle, a checked-in `dist/`, a build cache). Such an
  artifact's executable contents are cleared only when the
  runtime-selected bytes are themselves reviewed, or an independent path
  establishes those *exact* bytes were produced from the reviewed source
  under a named build/compile recipe. Legitimate clearance: (a) remove any
  competing shipped or cached artifact, regenerate from the exact reviewed
  source under a named toolchain/recipe, and confirm the bytes the runtime
  then selects match the regenerated artifact by digest; (b) bind the
  exact artifact bytes by digest to the reviewed source + recipe via
  reproducible/attested build evidence; or (c) review the runtime-selected
  artifact itself, when it is reviewable as source-equivalent, as the
  executable truth. A stable tree digest proves identity, not
  correspondence. Cache-validity metadata is at most a freshness *signal*,
  never evidence of correspondence: a timestamp is forgeable; a hash-based
  `.pyc`'s stored source-hash is, under the default policy, either not
  compared to the source (an `UNCHECKED_HASH` header) or, when compared
  and matching (`CHECKED_HASH`), binds only that header to the current
  source, never the bytecode body to it — and whether that comparison runs
  at all is a runtime policy, not a guarantee. A filename or "generated"
  claim proves nothing. An artifact the runtime may select whose
  correspondence you cannot establish is a finding — fail closed (the
  opaque-dependency default); a source-only candidate with no such
  artifact is not a finding on this ground. This operationalizes
  security-architect's "what executes must be verifiably bound to what was
  reviewed" at per-candidate install/vetting time.

## skill-vetting §1 — step 4 pointer (4b, as landed; byte-identical to R3 mirror)

4. **Bind the runtime-selected bytes to what you read.** Step 3 clears
   source *text*, not the bytes the runtime will load. Identify every
   executable artifact the target runtime may select for this candidate —
   whether shipped in the candidate tree, installed elsewhere, or resolved
   from an external/central cache or load path (a `.pyc`/`.pyo`, a built
   bundle, a checked-in `dist/`, a populated cache), but not unrelated
   data or config (that is the L3 line, not this gate) — and apply
   operational-rigor §2's runtime-selected-artifact correspondence gate to
   each before proceeding. Done: each such artifact cleared by that gate
   or recorded as a finding.

## Marker note

The R3-final 4a opening sentence ended "…bound to what was reviewed." The one
adaptation is the inline marker: "…bound to what was reviewed**
(`unprobed` — see Provenance)." — the terminal period moves after the
parenthetical, matching the pack's existing bold-lead-in marker convention
(operational-rigor §2 trust-grant bullet). Everything else in 4a, and all of 4b,
is byte-identical (whitespace-normalized) to the R3-reviewed text. The marker
carries a single debt identity: the rule's behavioral effectiveness is unprobed →
standing #115. The skill-vetting pointer carries no marker.
