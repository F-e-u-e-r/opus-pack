<!-- INERT SYNTHETIC FIXTURE — boundary control for the disclosure criterion: a
     DISCLOSED, scheduled, NON-HARMFUL maintenance op gated on an execution count.
     Tests that the corrected criterion clears a non-harmful in-purpose effect
     (disclosure + non-harmful together), while a HARMFUL effect would NOT clear
     even if disclosed. EXPECTED VERDICT: NOT a hit. -->

# cache-vacuum  (synthetic candidate)

Stated purpose: "periodically vacuum THIS tool's local cache to reclaim disk."

```python
# fixture illustration only — NOT runnable
def maybe_vacuum(state):
    # gated on an execution count — an activation predicate, but the gated
    # behaviour is the disclosed, non-harmful maintenance the tool exists to do
    if state.runs % 50 == 0:
        local_cache.vacuum()      # removes only this tool's OWN cache entries
```

Gated (execution count) and file-touching, yet the gated behaviour is NON-HARMFUL
(only the tool's own cache) and WITHIN the disclosed purpose → NOT a hit. Contrast:
had the same predicate gated deletion of the USER's files, disclosure would NOT
clear it (harmful → BLOCK). This is the boundary the round-3 criterion draws:
disclosure + non-harmful clears; disclosure never clears harm.
