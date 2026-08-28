# Final-delta reconstruction — landed exfil bullet vs R3-reviewed wording

Proves: **landed `skill-vetting §2` exfil bullet = R3-reviewed bullet + named
reproduced precision fixes + owner Option-X ratification**, with zero unaccounted
wording drift. R3-reviewed source = the exact packet Luna and Sol saw in round 3.

## Current-bullet preimage pin (the bytes replaced)
Exact pre-edit bullet (`skill-vetting §2`, "Exfiltration-shaped commands"),
sha256 `66bff37d083a0f70a042f1f690a8ebc848e9f8ad231133ca51c90847c6cafa1b`:

```
- **Exfiltration-shaped commands.** `curl`/`wget`/`nc` to a non-placeholder external
  host, or reads of `~/.ssh`, browser credential stores, `.env`, or keychains, in a
  default (non-example) execution path. Distinguish a documented attack technique in
  a security-testing playbook (data) from a command the skill itself runs (live).
```

## R3-reviewed → landed (word-level; every hunk accounted)

- **Option X — explicit layering** (owner-adjudicated; keep `curl/wget/nc` +
  credential reads as findings-to-explain):
  - added the framing sentence "Judge the data flow and the disclosure, not the
    transport name";
  - relabelled clause (a) as **"Legacy high-signal triggers"** and clause (b) as
    **"The generalized criterion"**;
  - added "each a §2 finding that must be explained (a hit is not automatic proof — it
    blocks unless the disclosed purpose explains it) and that need NOT first be shown to
    carry a secret";
  - added "A legacy (a) `curl`/`wget`/`nc` with no secret in view stays a finding —
    explained by the disclosed purpose and cleared, not silently ignored."
- **Sol-1 — predicate keys on the DISCLOSURE, not the path**: "private/secret data
  leaving on a path the purpose does not need" → "a private-data disclosure the
  disclosed purpose does not need, over any outbound path (needed or not)"; and the tell
  "private data is disclosed on a channel the purpose doesn't need" → "the private-data
  disclosure is one the purpose doesn't need".
- **Sol-2 — reconcile the safe harbor with the legacy trigger**: "Not a channel hit: a
  remote image, a **library HTTP call**, or a DNS lookup that carries NO secret ..."
  (library calls are not blanket-flagged; only clause-(a) CLIs are), plus "a disclosed
  purpose never launders an unnecessary private-data export".
- **Named renderer-live clarification** (raised R2/R3, both lenses): the
  "emitting content that makes the renderer/client fetch IS the skill opening the
  channel (live)" clause moved inline to the markdown-image example.
- Minor rephrases within the above (piggybacked-onto / required-authentication) carry no
  new threat content.

No hunk introduces a threat shape or example beyond R3 + the named deltas.

## Conclusion
Landed = R3-reviewed + Sol-1 + Sol-2 + Option-X layering + the named renderer-live
clarification. **Zero unaccounted wording drift.** Marker count unchanged (skill-vetting
still carries exactly one `unprobed` covenant; the new bullet adds none). op-rigor and
security-architect bytes unchanged.
