The core design is correct: it adds the missing trigger, separates source review from runtime selection, rejects tree-digest and cache-freshness substitutes, preserves source-only/direct-artifact clearances, stays at L2, and keeps skill-vetting as a pointer.

Three wording defects need correction:

- “Proves up-to-dateness” overstates cache metadata. An `UNCHECKED_HASH` header is not runtime-validated; timestamps are forgeable; even a passing `CHECKED_HASH` check validates only the cache key, not the bytecode body. Call these “cache-validity/freshness signals,” never proofs.
- Step 4 limits discovery to “shipped” artifacts, leaving an out-of-tree or central cache/load-path artifact as a same-shape bypass. Scope it to the target runtime’s actual selected executable bytes, including relevant installed or configured external caches, while excluding unrelated data and L3 totality.
- Local regeneration should explicitly name/verify the build recipe and toolchain, remove competing artifacts, and verify that runtime selection resolves to the regenerated artifact’s exact digest—not merely that recompilation or a behavior test succeeded.

FIX freshness-metadata qualification including CHECKED_HASH versus UNCHECKED_HASH, runtime-selection coverage for out-of-tree caches and load paths, explicit trusted build-path and exact selected-artifact digest verification for local regeneration
