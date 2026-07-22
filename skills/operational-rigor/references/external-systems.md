# operational-rigor · references: external-systems

Verify-before-trust rules for work that crosses a boundary into an external
tool, cache, fallback chain, timezone/clock, deploy target, or recurring
schedule. These are NOT
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
  constant, and never retune from old numbers alone. When an enclosing hard
  deadline (a platform's handler kill, an upstream SLA) sits BELOW the
  success tail, no timeout value fixes it — raising yours past the deadline
  only hands the abort to the platform, uncontrolled; restructure (async
  handoff, tiering) or accept-and-meter the aborted tail as a recorded
  decision.
- **Cache-write discipline: never cache a failure, an *unvalidated* empty
  result, or an unvalidated payload *as an answer*** — a long TTL converts a
  transient flake into a locked-in wrong answer. The distinction that
  resolves the apparent conflict: an unvalidated empty (a flake, a parse
  failure on read) is a miss to retry/overwrite, while a *validated*
  known-empty (the input legitimately has no answer) is cached as an
  explicit sentinel. So a cache in front of a paid producer needs **four
  entry kinds** (miss → fetch; producer failure → a short-TTL cooldown
  marker — a typed non-answer, never served as a value, retrying at a
  bounded rate and scoped to the failure domain, so a provider-wide outage
  cools the provider, not one key at a time; validated known-empty → cached
  sentinel; value), or it re-spends budget on known-empty inputs,
  permanently caches transient errors, or lets every reader amplify an
  outage against the paid producer. The cooldown bounds retries, not first
  admission: until the first failure completes, concurrent misses still
  reach the producer (traffic × producer-timeout worth of calls), so the
  money bound on a paid surface is always the atomic spend-cap chain
  (security-architect's spend/abuse bounds), and an admission bound
  (single-flight, a concurrency cap) is added when the producer cannot
  tolerate that window. Scope the key by
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
  throw — a throw skips the remaining tiers and drops the item entirely);
  where empty is itself a valid domain answer, the advance signal must be a
  *typed* failure distinguishable from a validated known-empty (mirror the
  cache rule above), or a correct "no results" from one tier gets overwritten
  by a worse tier's stale hit. A terminal all-tiers-failed result is an
  observed failure to log and meter, not a success — and it keeps its
  failure type at the chain's outward interface (return or raise the typed
  failure, never a raw empty a caller could cache or display as a validated
  "no results"); and a last-resort tier with a hard quota is invoked at
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
  least two TZ environment values, at least one DST-observing; and state an
  explicit policy for DST gap/fold instants AND execute it on at least one
  gap and one fold instant (a spring-forward 02:30, a fall-back 01:30) — a
  stated-but-untested policy is a claim, not a gate, and TZ values alone
  never exercise those instants.
- **A deploy target is a contract to verify, not a bigger laptop.** On
  response-terminates-execution platforms (serverless), fire-and-forget work
  after the response silently never runs, and in-memory state is per-instance
  and mortal — cold starts wipe it, concurrent instances multiply it; await
  side effects before responding — "await" means the *durable handoff*
  (enqueue/persist), not long-running processing, which belongs in a
  separate worker (security-architect's webhook rule; awaiting full
  processing past an ack deadline converts the deadline into platform
  retries and duplicate work) — and document each in-memory structure's
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

- **A recurring schedule's own "completed" report is not evidence its side
  effects landed — verify at the destinations, attributed to the
  invocation** (`unprobed` — see the skill's Provenance). (Motivating
  incident: a weekly task reported success for roughly three months
  while its write step silently never executed; a second output channel
  on the same task was separately dead on a stale hardcoded credential —
  contributor-reported shape.) Gates first — and two branches exit here before any fire: reviewing
  without authorization to run it goes straight to the inspection-only
  arm at the end of this entry, and a schedule with no authorizable
  alert path cannot complete arming — record that gap and stop before
  any test fire. Otherwise every consequential supervised or test
  invocation — the repeat run below included — carries its own
  per-invocation authorization
  (destructive / spending / publishing / credential — operational-rigor
  §2's confirmation gate governs: its per-invocation grant, plus its
  AUTH: artifact for the outward or irreversible steps), and a
  schedule whose unattended fires are themselves consequential needs §2's
  project-policy-scoped standing authorization before running unattended —
  that standing authorization is the canonical exception covering the
  unattended fires themselves; a request to arm covers the arming, not
  those future fires; a permission or credential in place is not
  authorization. Verify the
  credentials the work actually needs under the schedule's principal;
  minting or broadening one is itself gated; session-only credentials do
  not travel to headless runs. Drive and attribute: read the configured
  entry (command, arguments, trigger, enabled/disabled state) and confirm
  it invokes what you test, then trace the invoked task's own config,
  code, or runbook into a channel inventory — each destination, emission
  condition, deadline, and credential; the scheduler entry names the
  script, not the channels, and the incident's second channel (with its
  stale hardcoded credential) lived in the task's own config. Recurrence
  stays disabled while arming — fire the entry once yourself, headless,
  under the schedule's execution context, meaning principal AND
  environment AND working directory (running interactively as the right
  user can carry a session credential the real schedule lacks — a
  related trap, distinct from the incident's); "watch one real fire"
  establishes scheduler binding only on an already-enabled schedule you
  hold observation authority over. Verify each inventoried channel with
  its emission condition driven TRUE at least once: destination evidence
  carrying that invocation's identifier where the channel supports one,
  else a before/after transition plus exclusion of every other
  producer AND of earlier invocations' still-outstanding effects (an
  effect queued before the window can land inside it — asynchronous
  delivery without an identifier stays unverified when that exclusion
  cannot be established) (a fresh artifact another writer
  or run could have produced proves nothing; an async 2xx acceptance is
  not delivery) — a condition-matched absence verifies only the
  suppression branch, never the channel. Consequential outbound channels
  are driven in separately authorized fires, never batched (§2's
  one-at-a-time rule). Repeat the run (its own grant if consequential)
  against stated existing-output and lock expectations; a hung run
  overlaps the next fire regardless of average runtime, so where overlap
  is possible the second entry must traverse the real lock-acquisition
  path while the first holds the guard — "impossible" means
  scheduler-enforced non-concurrency, not short runtime. Armed means:
  every inventoried channel emission-positive-verified; no human cleared
  a prompt mid-run; overlap guarded or scheduler-excluded; the absence
  alarm below armed, its firing proven once per independently configured
  alarm path (one channel's alert does not prove another's mapping; a
  synthetic destination proves a path only when its routing matches the
  production configuration), and its alert channel's standing
  authorization in place — the §2 project-policy-scoped kind, covering
  exactly the automated alert (no authorized alert path → the alarm
  is unarmed and that gap is the report; no automated outward action
  invents itself). Anything short stays unarmed — and enabling is not
  the end: scheduler binding stays an open claim until the first
  scheduler-originated fire lands its attributed effects by its deadline
  (the alarm's first cycle checks exactly that). Ongoing: a dead task
  cannot report its own death, and a watcher that can die silently moves
  the problem one layer down — terminate the chain in a mechanism whose
  alarm fires on ABSENCE by construction (an externally enforced
  missed-deadline alert), outside the schedule's failure domain
  (scheduler, host, principal; where full independence is unavailable,
  the nearest different trigger path, with the shared-fate residue
  named). Its signal derives from destination-observed state or
  receipts, never from a ping the task itself writes — a live task with
  a dead write step keeps pinging green; key it to each channel's
  documented emission condition and deadline, and a conditional channel
  needs an independently observed condition signal or a periodic
  positive canary, else it stays explicitly unverified in the alarm's
  coverage. Prove the alarm once by withholding a destination effect
  while the task runs — the suppression is its own consequential
  action: use a synthetic or test destination where one exists, a
  separately authorized suppression where not, and re-drive the channel
  emission-positive after the fault. A task-written health line shows
  the task ran, not that anything arrived; stale, uncheckable, or a
  missed check is unhealthy and gets the response documented and
  authorized at arming time — disarming or escalating needs its own
  authorization, and with no authorized response the gap itself is the
  report, never a shrug. Relying on an armed schedule mid-flight uses the ongoing
  destination-and-deadline checks above plus the asymmetric evidence
  rules below as the evidence — and "after the invocation" stays
  necessary but never sufficient: the identifier-or-exclusion procedure
  above applies unchanged. Reviewing an
  existing schedule without authorization to run it: inspect existing
  evidence asymmetrically — stale evidence refutes only when an
  independently established emission was due and its deadline passed (a
  conditional channel whose condition never fired is not stale); fresh
  evidence
  proves only when tied to the invocation under review (an established
  exclusive writer narrows the author, not the run — its artifact still
  needs an invocation identifier, or a transition bounded BEFORE the
  next eligible invocation with every other invocation excluded —
  merely "after" credits a later run's success to an earlier failed
  one); otherwise it stays unverified.

## Provenance

The first six rules are the 2026-07-13 external-systems batch, mined from five
private production retiring-architect libraries (a link-shortener, a market
dashboard, a Telegram bot, an engine-parity port, a learning lab), merged in
opus-pack #26 and maintainer-fixed under cross-model review; two (cache
discipline, fallback rot) were independently rediscovered by two libraries.
Split out of operational-rigor §4 into this reference on 2026-07-14 to keep the
discipline core lean — content unchanged except two `§4` cross-references
spelled out to `operational-rigor §4`.

On 2026-07-16 a fresh two-family post-merge review (grok-4.5 +
gpt-5.6-sol; effort tiers per round in the trail) tightened five clauses
here — timeout-vs-enclosing-deadline,
error-cooldown cache state, typed advance-signal vs. valid empty, executed
DST gap/fold cases, and the durable-handoff scope of "await side effects" —
trail in `reviews/2026-07-16-post-merge-validation-pr25-29.md`.

Sync contract: the §4 scheduled-process bullet's opening claim quotes
this entry's headline verbatim — change the headline here → update that
quote (this entry wins on disagreement).
The scheduled-process entry (2026-07-22; one addition with its §4 rule,
which carries the contributor's 2026-07-21 date — the entry records its
placement during review) is the protocol body of the §4
scheduled-process rule added in opus-pack #49 — placed here per the
2026-07-14 split precedent (boundary-specific protocols out of the lean
core); its incident provenance and `unprobed` marker live with that rule in
the skill's Provenance.

Environment-specific facts to re-verify against current tooling: a tool's
exit-code table (qpdf's), real success-latency distributions, cache TTL/state
semantics, fallback-provider quotas, date-constructor normalization + TZ/DST
behavior, serverless lifecycle + bundler file-tracing, and scheduler
concurrency/one-shot semantics.
