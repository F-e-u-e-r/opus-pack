# operational-rigor · references: external-systems

Verify-before-trust rules for work that crosses a boundary into an external
tool, cache, fallback chain, timezone/clock, or deploy target. These are NOT
core discipline — each is an incident-backed trap specific to one boundary,
where the boundary *reports success while lying about it* in a particular way,
and the rule names the observation that catches it. They live here, out of the
always-loaded skill, so operational-rigor §4 stays lean (skill-authoring §7:
domain-reference packs run longer than the ~150-line discipline core).

**Load this file when** the work under verification touches any boundary below;
otherwise operational-rigor §4's core "verify by observation" rules are enough.

- **A third-party tool's exit code is a contract to verify, not assume.** Some
  tools exit non-zero on success-with-warnings while writing valid output
  (qpdf exits 3); gating on `=== 0` then misclassifies success as failure — a
  shipped gate once made legitimately-owned locked files permanently
  unprocessable this way. For exit-code gates on external tools, read the
  documented exit table, and confirm success by validating the output
  artifact's integrity — not its mere existence, since a partial or corrupt
  artifact can be written on failure.
- **Never tighten a timeout below the measured success-latency tail.** Before
  setting or "tidying" a timeout constant, measure the distribution of
  *successful* runs on real payloads, over multiple runs — high-variance
  backends make one run meaningless (a 25s "tidy" once aborted a measured
  42s slow-but-successful call). A timeout under the success tail converts
  slow successes into failures; record the dated measurement beside the
  constant, and never retune from old numbers alone.
- **Cache-write discipline: never cache a failure, an *unvalidated* empty
  result, or an unvalidated payload** — a long TTL converts a transient flake
  into a locked-in wrong answer. The distinction that resolves the apparent
  conflict: an unvalidated empty (a flake, a parse failure on read) is a miss
  to retry/overwrite, while a *validated* known-empty (the input legitimately
  has no answer) is cached as an explicit sentinel. So a cache in front of a
  paid producer needs **three states** (miss/error → retry; validated
  known-empty → cached sentinel; value), or it either re-spends budget on
  known-empty inputs or permanently caches transient errors. Scope the key by
  every dimension that can fail independently (a shared key lets one path's
  failure poison the other's success), and store the producer output minimized
  and access-controlled per operational-rigor §4 (never third-party PII/secrets
  at rest by default), applying curation/policy overrides at read time — baking
  them in freezes old policy into the cache until TTL.
  ❌ "cache whatever came back — empty is a valid result and saves an API call."
- **A fallback chain is a set of unexercised dependencies that rot silently.**
  A dead or capability-mismatched leg is invisible until the primary fails —
  it errors on every call and falls through with zero visible errors, pure
  quota waste (a chain's highest-quota model once went unused for weeks this
  way). On any add/remove/reorder: live-probe every leg end-to-end with a real
  payload and record dated results. Within the fallback chain (and only there —
  not on an auth/payment/security path, where operational-rigor §4
  fail-loud/fail-closed governs), each tier helper normalizes its own failure
  to the chain's advance signal (return empty so the next tier runs, never
  throw — a throw skips the remaining tiers and drops the item entirely), but a
  terminal empty after every tier has failed is an observed failure to log and
  meter, not a success; and a last-resort tier with a hard quota is invoked at
  batch granularity, or one refresh cycle exhausts the emergency budget exactly
  when it is needed.
- **On a UTC server handling a local-wall-clock domain, expect two time
  conventions to coexist** (shifted-epoch values read via UTC accessors vs.
  raw instants plus a timezone formatter): document which convention each
  helper uses and never feed one convention's value to the other's reader —
  the failure is a silent ±offset double-shift. Validate dates by calendar
  round-trip, not component ranges alone (a day ≤ 31 still admits Feb 30):
  construct, then confirm the constructor did not silently normalize it to a
  different date (lenient constructors roll Feb 30 → Mar 2), or the scheduled
  action fires on the wrong day with no error. Run time-logic tests under at
  least two TZ environment values, and state an explicit policy for DST
  gap/fold instants (which two TZ values alone do not cover).
- **A deploy target is a contract to verify, not a bigger laptop.** On
  response-terminates-execution platforms (serverless), fire-and-forget work
  after the response silently never runs, and in-memory state is per-instance
  and mortal — cold starts wipe it, concurrent instances multiply it; await
  side effects before responding, and document each in-memory structure's
  behavior when it vanishes or multiplies. Bundler file-tracers follow only
  statically-analyzable imports, so runtime-resolved assets silently vanish
  from the deployed artifact while local dev AND local build both pass. And
  "every route 500s" points at a module-load or shared-init failure (module
  load, shared middleware, config, runtime init) rather than one route's
  logic — suspect that first, and probe a route that MATCHES (an unmatched
  route's clean 404 comes from the platform fallthrough and masks a
  fully-broken deploy); the truthful repro is building the production artifact
  and importing it — dev-mode resolvers prove nothing about production module
  loading.

## Provenance

These six rules are the 2026-07-13 external-systems batch, mined from five
private production retiring-architect libraries (a link-shortener, a market
dashboard, a Telegram bot, an engine-parity port, a learning lab), merged in
opus-pack #26 and maintainer-fixed under cross-model review; two (cache
discipline, fallback rot) were independently rediscovered by two libraries.
Split out of operational-rigor §4 into this reference on 2026-07-14 to keep the
discipline core lean — content unchanged except two `§4` cross-references
spelled out to `operational-rigor §4`.

Environment-specific facts to re-verify against current tooling: a tool's
exit-code table (qpdf's), real success-latency distributions, cache TTL/state
semantics, fallback-provider quotas, date-constructor normalization + TZ/DST
behavior, and serverless lifecycle + bundler file-tracing.
