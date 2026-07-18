---
name: domain-evidence-discipline
description: Evidence discipline for non-code deliverables — marketing copy, research reports, data analyses, business/ops documents. Defines, per domain, what counts as evidence, the typed authority order, what verification-by-observation means, and the fraud table a reviewer hunts. Load when producing OR judging a non-code work product whose correctness depends on sources and claims rather than a runtime. NOT for code (operational-rigor), product direction (product-roadmap), personal plans (personal-goal-planning), or red-line professional judgment (the gate below — refuse and route to a qualified human).
---

# Domain Evidence Discipline

This skill's evidence-control loop stays constant across domains; only
the nouns change. For any non-code deliverable, name the four nouns
BEFORE producing anything — in your working notes or the report, where
a reviewer can see them — and hunt the same four afterward. Under this
skill, a deliverable whose four nouns were never named is incomplete
and unauditable.

**Red-line gate — run before anything below.** Where the deliverable
would substitute for individualized, materially high-stakes
professional or regulated judgment — a medical/clinical decision,
legal advice, a buy/sell financial call, mental-health treatment,
safety-critical engineering sign-off — refuse the deliverable and
route to a qualified human: an evidence checklist supplies structure,
never the judgment, and its presence invites trust it cannot back.
General work that merely touches money or health (a budgeting
spreadsheet, fitness copy) is not red-line; the line is substituting
for the professional's individualized call. Adjacent work that is not
substitution (compliance research, tooling for practitioners) may be
drafted under the matching instance, labeled as not the professional's
individualized call — and when the user would reasonably treat it as
professional work-product, it ships only with a qualified human's
review; unreviewed, it stays a labeled draft. This is the
execution-side sibling of skill-authoring §5's authoring gate (that
rule stops the checklist being WRITTEN and gates adjacent authoring;
this one gates the deliverable being USED as the professional's
answer).

## 1. The four nouns

1. **Minimum evidence set (binding).** The sources that must actually
   be OPENED before any output: the governing document (brand rules,
   spec, data dictionary) and the subject's own facts (the product's
   real materials, the raw dataset) — every time. Before declaring a
   governing document absent, search the workspace and the supplied
   materials for it and say where you looked; only then state the
   assumption you will work under. An OUTWARD claim — an externally
   checkable assertion about third parties or the current world state,
   even when repeated from supplied material — needs a live source
   fetched now, with enough sources to cover each materially distinct
   outward claim; a deliverable with no outward claims owes no fetch
   (evidence is claim-triggered, not ceremony). If a required source
   cannot be opened (the dataset is missing, a referenced brand guide
   was never supplied), stop and request it, or narrow the deliverable
   and label it explicitly unverified — never proceed as if verified.
2. **Authority order (typed).** Different questions have different
   owners; one flat chain does not fit all. The client/user owns
   objectives and authorized creative choices; mandatory rules (brand
   bans, legal disclaimers, policy) own compliance; current primary
   evidence owns factual assertions; the documentation owns what a
   field MEANS (raw values never redefine semantics); your taste and
   memory come last. An instruction never overrides observed facts, a
   mandatory constraint, or the red-line gate — surface the conflict
   instead of silently picking a side ("punchy copy" in a brief never
   overrides a brand rule banning superlatives).
3. **Verification by observation.** What "observed" means here: every
   factual claim traces to a source you opened; names, prices, dates,
   versions exact; arithmetic recomputed, not transcribed; rendered
   surfaces actually rendered and looked at. A claim you could not
   verify is removed or explicitly flagged — never left standing as
   fact.
4. **Fraud table.** The domain's classic fabrications, written down so
   a reviewer can hunt them by re-opening sources, re-fetching, and
   recomputing — the non-code counterpart of re-running the tests: it
   hands delegation-and-review §3's reviewer the domain's rubric.

## 2. Worked instances

**Marketing / copy.** Evidence set: brand rules (or the search-then-
assumption path above), the subject's own capability facts; live
fetches per the outward-claim rule (competitor, market-position, and
price claims are outward even when the brief asserts them). Authority
(typed): the client owns the objective and voice choices within the
brand guide; the brand guide owns compliance; the subject's materials
own capability facts; taste last. Observed: line-by-line check against
brand rules; every capability claim traces to the subject's materials;
prices/names/dates exact; the rendered page or email actually
rendered. Frauds: fabricated statistics ("studies show" with no opened
source), fake social proof (invented testimonials, counts, awards),
unverifiable superlatives ("#1", "guaranteed"), stale prices or dead
offers presented as current, missing required disclaimers, spec
betrayal (copy violating a written brand rule while claimed on-brand).

**Research / report.** Evidence set: the sources the claims actually
rest on, opened this session with access dates — fetched live when the
claims are outward; an internal-sources-only synthesis owes no
external fetch; one counter-source deliberately sought when the report
advances a contestable outward central claim. Authority (typed):
primary source owns facts; reputable secondary > aggregator for
context; memory last and labeled. Observed: every figure carries a
link and access date; arithmetic and unit conversions recomputed;
quotes checked against the page they came from; currency of volatile
facts (prices, policies, versions) checked against the source's date,
not assumed. Frauds: uncited figures, stale figures presented as
current, phantom precision (exact-looking numbers with no computation
behind them), cherry-picked date ranges, a "sources" list whose
entries were never opened.

**Data analysis.** Evidence set: the actual dataset (not a described
version of it), its dictionary/provenance, the requester's definition
of the metric in writing. Authority (typed): the data owns the values;
the dictionary owns what a field means (raw values never redefine
semantics); the requester's written metric definition owns the metric;
recollection last. Observed: headline numbers recompute from raw in
one command; dedup, exclusions, and imputations declared
(operational-rigor §4 data-path integrity: no silent defaults,
unmatched records surfaced); the plain-language summary agrees with
the computed table it sits above. Frauds: silent data cleaning,
dropped unmatched records, totals that do not reproduce, a "verified"
label on arithmetic never recomputed, precision the data cannot
support.

**Hybrids and routing.** A deliverable claiming in several domains (a
market-research report for a campaign) takes the union: every domain
it actually makes claims in contributes its evidence set and fraud
table, and authority stays typed per claim. Business/ops documents
route by primary claim type — financial and metric claims → Data
analysis; market and external claims → Research; persuasive copy →
Marketing. Applying the four nouns task-locally, alone or in union, is
NOT minting an instance and carries no fixture duty.

## 3. Minting a new instance

- Mint a reusable instance only when at least one noun materially
  differs from every existing instance — name the differing noun in
  the instance. If none differs, the sector needs no instance: route
  to the nearest one and note the boundary.
- A sector that is coding in disguise (IaC, script logic, pipelines)
  routes to operational-rigor. An analysis PRODUCED through a runtime
  (SQL, a notebook, spreadsheet formulas) but DELIVERED as claims uses
  both skills: operational-rigor governs the execution and the data
  path; this skill governs the evidence, the claims, and the review.
- The red-line gate above applies to minting exactly as to producing:
  no instance for red-line judgment; a sector adjacent to one follows
  skill-authoring §5's qualified-reviewer requirement.
- Every regulation, policy, threshold, or figure the instance names
  carries a source and access date, fetched now (operational-rigor §4:
  a clue about external data is a map, not a schema; memory is
  labeled).
- A NEWLY minted instance without its own trap fixture is not done —
  the README covenant applies to instances exactly as to rules (the
  fixture's trap is the sector's central fraud; its safe outcome obeys
  ground-truth-gates rule 2's trap-armed clause). The three founding
  instances above carry that debt explicitly — see Provenance.

## When NOT to use this skill

- Code, infra, or pipeline deliverables → operational-rigor (+
  ground-truth-gates). An analysis produced through a runtime but
  delivered as claims uses both skills (§3).
- Substantial open-ended source discovery → the environment's research
  or deep-research tooling does the gathering; this skill is the
  evidence-control overlay on what that workflow produces, not a
  replacement for it (and it does not replace these gates).
- "What should we build next?" → product-roadmap. Personal goals →
  personal-goal-planning.
- Red-line professional judgment (the gate above) → no checklist; a
  qualified human.
- A one-off trivial lookup — quoting one number with its source needs
  no ceremony.

## Provenance

Promoted 2026-07-18 from a 2026-07-16 staging draft (owner decision
D1, option b: one condensed pattern skill, not eight ported adapters).
The four-nouns pattern, the binding minimum-evidence-set idea, the
per-domain fraud tables, and the instance-needs-its-trap rule adapt
Sahir619/fable-method's domain-adapter schema (MIT; ideas only, no
files copied; see README acknowledgements). Their round-9 result is
the external evidence, cited as shape with its grade: with the
marketing adapter a weak-tier executor found unmentioned source
documents and caught planted frauds that a bare run praised (their
measurement, their fixtures; their round-9a null — a prompt that names
the evidence pre-solves discovery — is why the evidence set binds the
OPENING and searching-out of sources, not their mention). The typed
authority order and the adjacent-deliverable review clause came out of
this PR's own dual-family review (a flat chain let an instruction
outrank facts and mandatory constraints; adjacent PRODUCING had no
runtime twin to §5's adjacent-authoring gate). The worked instances
are this pack's own compressions, cross-checked against the pack's
existing rules (operational-rigor §4; delegation-and-review §3;
skill-authoring §5's authoring-side red-line, deliberately not
duplicated verbatim — sibling gates with different jobs, each in its
own words). `unprobed` in-house per the README covenant: no probe has
run against these instances; the owed probes are three non-code trap
fixtures, one per founding instance — marketing, research, and data
analysis — each arming its instance's central fraud with the
trap-armed check.
