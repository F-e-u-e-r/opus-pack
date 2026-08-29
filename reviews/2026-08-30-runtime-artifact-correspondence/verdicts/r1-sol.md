The design is sound on axes 1–3 and 5–10, but two phrases need correction:

- “Proves up-to-dateness” contradicts D2/D4. Hash headers and timestamps are attacker-controlled metadata; even an accepted match is only a cache-invalidation/freshness signal. Say: “may satisfy the runtime’s freshness check, but does not establish correspondence.”
- Skill-vetting’s “every shipped … artifact” misses installed, materialized, or pre-existing out-of-tree caches. Require identifying every executable artifact the target runtime may select for the candidate, whether shipped in-tree, installed elsewhere, or cached. This remains L2 because it concerns candidate executable selection, not arbitrary reachable data/config.

The local-regeneration path otherwise covers exact reviewed source, the named/observed build path, and runtime selection. “The regenerated artifact” would also be clearer than “the regenerate,” but that is editorial.

FIX freshness-metadata proof claim, shipped-only artifact discovery scope
