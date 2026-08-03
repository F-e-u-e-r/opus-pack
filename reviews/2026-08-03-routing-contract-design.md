# Routing-contract design note — regression corpus + structural gate

Independent routing-contract PR (the roadmap's unordered item), built on the
landed PR 2 / PR 3 foundation. It operationalizes `ARCHITECTURE.md §6`
(routing-contract changes) by shipping the **regression corpus §6 already calls
for** plus a **structural gate** that keeps the corpus complete and
self-consistent. The schema below folds in an owner review of the first
walking-skeleton draft (five corrections, recorded in "Schema decisions").

## Scope and non-goals

**In scope**
- `metadata/routing-intent.json` — per opus-pack skill, an authored routing
  `intent` sentence + a **symmetric** `neighbors` graph (the skills whose trigger
  scope is adjacent, per §5). Authored-once, same family as `metadata/skill-tiers.json`.
- `metadata/routing-corpus.jsonl` — the regression prompts, one per line, each a
  human-adjudicated case with a stable `id` and a `rationale`.
- `check_routing_corpus()` in `.github/derived_checks.py` + two-sided proofs in
  `.github/test-derived-checks.py`, wired into `.github/checks.py` beside the PR 3
  gates.
- Minimal `ARCHITECTURE.md` wiring: §6 points at the corpus; §8 lists the
  structural gate **with its explicit non-guarantee**.

**Non-goals (deliberately excluded)**
- **No model run / no live routing check.** Per §8 the gate must not claim to
  verify that a description actually routes as authored — that is the manual
  routing-contract review. The gate is *structural only*.
- **No description edits.** Descriptions are the routing surface this corpus
  protects; changing them is a *later* routing-contract change gated by this
  corpus, not this PR.
- **opus-pack (10 skills) only.** The gate scopes to `opus_pack_skill_ids`
  (parallel to `check_tier_canon`), consistent with the `skills/`-only covenant
  (#115) and design-pack's separate-scope treatment. Cross-plugin routing is a
  larger boundary (new neighbour taxonomy + regression procedure); it gets its own
  corpus if/when design-pack descriptions are changed — not pulled in here.
- **No live selection-baseline probe.** The corpus ships with the human
  adjudication baseline; capturing a live skill-selection baseline is round-5 probe
  work. A one-off *procedure smoke test* on two skills (below) proves the manual
  procedure yields a comparable artifact keyed by case id, without becoming a CI
  gate or a routing-correctness claim.
- Not security-pack, not #123, not any other content change.

## The two authored sources

`routing-intent.json` (schema_version 1):
```
{ "schema_version": 1,
  "skills": { "<skill-id>": { "intent": "<one sentence>", "neighbors": ["<skill-id>", ...] } } }
```
`neighbors` is an **undirected** relation: the gate requires A∈neighbors(B) ⇔
B∈neighbors(A). The undirected pairs are the routing "edges".

`routing-corpus.jsonl` (one JSON object per non-blank line):
- line 1 is `meta`: `{ "kind":"meta", "schema_version":1, "expectation_source":"human-adjudication" }`
  — it records only schema + where the expectations come from. It must **not**
  carry an aggregate `probe_status` (see decision 2).
- every other line is a case:
```
{ "id": "<for>.<kind>.<slug>.NNN", "for": "<anchor skill-id>",
  "kind": "positive|neighbor-negative|out-of-scope|ambiguous",
  "prompt": "<user request>",
  "expected": "<skill-id>" | "none",          # positive / neighbor-negative / out-of-scope
  "acceptable_any_of": ["<id>","<id>", ...],  # ambiguous ONLY (>=2 distinct)
  "rationale": "<one sentence of adjudication basis>" }
```
`kind` semantics: `positive` → `expected` == the anchor (§6's "intended positive"
and "previously-supported that must remain supported"). `neighbor-negative` →
`expected` a declared neighbour of the anchor. `out-of-scope` → `expected` is
`"none"` or an unrelated (non-anchor, non-neighbour) skill. `ambiguous` →
`acceptable_any_of` including the anchor (§6's "ambiguous/overlapping"; a
description edit must not silently collapse it).

## Schema decisions (owner review of the walking skeleton)

1. **Stable per-case `id`** (`<for>.<kind>.<slug>.NNN`) so probe results, findings,
   and history bind by id, never by prompt text. The gate checks uniqueness, the
   format, and that the id's subject/kind match the record.
2. **No aggregate `probe_status`.** A hand-written corpus-level status repeats the
   `probe_status: partial` information-loss failure and the derive-don't-hand-author
   covenant. Real status is *derived* per-case from run artifacts (below); the gate
   fails if `meta` carries `probe_status`.
3. **`expected` is never overloaded.** Single-value `expected` for the definite
   kinds; a separate `acceptable_any_of` for ambiguous. (`required_all_of` is
   reserved for a future "must co-load" need — not this schema.)
4. **Edge-based coverage + symmetric neighbours.** Per skill: ≥2 positive, ≥1
   out-of-scope, and a neighbour-negative for **every** declared neighbour. Per
   edge: ≥1 ambiguous. Case count grows with neighbour degree, not a fixed
   per-skill number. `neighbors` is symmetric and the gate enforces it.
5. **Per-case `rationale`** — one sentence preserving the human-adjudication basis
   so a later reviewer cannot silently rewrite `expected`. It is evidence, not
   model input; the gate requires it non-empty.

## Derived probe status + run-artifact model

Probe status is never authored. A routing-regression run writes a separate
artifact, one record per case, keyed by `id`:
```
{ "case_id": "operational-rigor.positive.refactor.001", "model": "<slug/version>",
  "observed": "operational-rigor", "result": "match|miss|ambiguous-ok" }
```
"probed / unprobed / partial" is then *computed* by joining case ids against the
run artifact — the corpus itself asserts only the human expectation. Run artifacts
are not committed as a CI gate here (they belong to the round-5 probe track).

## The structural gate — what `check_routing_corpus` guarantees

Against the real tree (opus-pack published skills = `opus_pack_skill_ids`): both
files parse and are schema-supported; intent skill set == published set; every
`intent` non-empty; neighbours are real, non-self, de-duplicated, and **symmetric**;
each case has a unique well-formed `id` consistent with its `for`/`kind`, a
non-empty unique `prompt`, a non-empty `rationale`, and a kind-appropriate
`expected`/`acceptable_any_of` naming published skills; neighbour-negatives point
at a declared neighbour; out-of-scope points at `none`/an unrelated skill; and the
edge-based coverage minimum (decision 4) is met.

### What it explicitly does NOT guarantee (mirrors §8)
- It does **not** run the model or a selector; a green corpus is complete and
  self-consistent, **not** proof that routing is correct or unchanged.
- It does not judge prompt quality/realism; a weak-but-well-formed prompt passes.

## Manual regression procedure (what a future description change runs)

When a PR changes a skill's `description`/`when_to_use`:
1. Take the changed skill and its `neighbors`; select their corpus cases by id.
2. Run each `prompt` through skill selection (fixed model/version, clean session);
   record the observed skill into a run artifact keyed by `case_id`.
3. Compare to the authored expectation: no `positive` may stop selecting the anchor;
   no `neighbor-negative` may start selecting it; `ambiguous` must not collapse to a
   single arm silently; `out-of-scope` must select nothing. Char count is **not** a
   success metric.
4. Any divergence is a routing-contract finding, reviewed per §6.

## Two-sided test matrix (red + green per structural rule)

`test-derived-checks.py::RoutingCorpus` proves the valid fixture passes and that
each rule can fail: duplicate id, malformed id, id/for mismatch, id/kind mismatch,
unknown `for`, unknown `expected`, positive expecting a non-anchor, out-of-scope
expecting a neighbour, ambiguous using `expected`, duplicate prompt, missing
rationale, meta with `probe_status`, missing meta, self-neighbour, unknown
neighbour, asymmetric graph, intent missing/extra skill, missing neighbour-negative
per neighbour, missing ambiguous per edge, a skill under-covered, malformed JSON,
unsupported schema.

## Execution + review

Local: `python3 .github/checks.py` and `python3 .github/test-derived-checks.py`
green. Then the escalating cross-model gate (grok-4.5 high → + gpt-5.6-luna ultra &
gpt-5.6-luna max → + gpt-5.6-sol max), per-invocation probe, single active PR, final
verdict bound to the exact frozen tree. No new behavioral doctrine rule ships here
(fixture + mechanical gate), so no in-body skill `unprobed` marker is added; the
corpus's human-adjudication baseline and deferred live probe are recorded here and
in `ARCHITECTURE.md §6/§8`.
