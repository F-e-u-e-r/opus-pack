---
name: domain-evidence-discipline
description: Evidence discipline for non-code deliverables — marketing copy, research reports, data analyses, business/ops documents. Defines, per domain, what counts as evidence, the authority order, what verification-by-observation means, and the fraud table a reviewer hunts. Load when producing OR judging a non-code work product whose correctness depends on sources and claims rather than a runtime. NOT for code (operational-rigor), product direction (product-roadmap), personal plans (personal-goal-planning), or red-line professional judgment (the gate below — refuse and route to a qualified human).
---

# Domain Evidence Discipline

The working loop never changes across domains; only the nouns do. For any
non-code deliverable, name four things BEFORE producing anything, and hunt
the same four as a reviewer afterward. A deliverable whose four nouns were
never named is opinion wearing a work product's costume.

**Red-line gate — run before anything below.** Where the deliverable would
substitute for individualized, materially high-stakes professional or
regulated judgment — a medical/clinical decision, legal advice, a buy/sell
financial call, mental-health treatment, safety-critical engineering
sign-off — refuse the deliverable and route to a qualified human: an
evidence checklist supplies structure, never the judgment, and its
presence invites trust it cannot back. General work that merely touches
money or health (a budgeting spreadsheet, fitness copy) is not red-line;
the line is substituting for the professional's individualized call. This
is the execution-side sibling of skill-authoring §5's authoring gate
(that rule stops the checklist being WRITTEN; this one stops it being
USED as the professional's answer).

## 1. The four nouns

1. **Minimum evidence set (binding).** The sources that must actually be
   OPENED before any output: the governing document (brand rules, spec,
   data dictionary) and the subject's own facts (the product's real
   materials, the raw dataset) — every time; plus, when the deliverable
   makes claims about the world outside those sources (competitors,
   market facts, current prices, regulations), one live external
   reference fetched now, not recalled. A deliverable with no
   outward-facing claims owes no external fetch — evidence is
   claim-triggered, not ceremony. If a governing document does not
   exist, say so and state the assumption you will work under.
2. **Authority order.** One ordered chain from explicit client/user
   instruction down to your own taste or memory, with the domain's
   classic conflict named and adjudicated in advance ("punchy copy" in a
   brief never overrides a brand rule banning superlatives — surface the
   conflict instead of silently picking a side).
3. **Verification by observation.** What "observed" means here: every
   factual claim traces to a source you opened; names, prices, dates,
   versions exact; arithmetic recomputed, not transcribed; rendered
   surfaces actually rendered and looked at. A claim you could not
   verify is removed or explicitly flagged — never left standing as
   fact.
4. **Fraud table.** The domain's classic fabrications, written down so a
   reviewer can hunt them by re-opening sources, re-fetching, and
   recomputing — the non-code counterpart of re-running the tests: it
   hands delegation-and-review §3's reviewer the domain's rubric.

## 2. Worked instances

**Marketing / copy.** Evidence set: brand rules (or state the voice
assumption), the subject's own capability facts; an external fetch when
the copy claims anything about competitors, market position, or current
prices. Authority: client instruction > brand guide > campaign brief >
past approved copy > your taste. Observed: line-by-line check against
brand rules; every capability claim traces to the subject's materials;
prices/names/dates exact; the rendered page or email actually rendered.
Frauds: fabricated statistics ("studies show" with no opened source),
fake social proof (invented testimonials, counts, awards), unverifiable
superlatives ("#1", "guaranteed"), stale prices or dead offers presented
as current, missing required disclaimers, spec betrayal (copy violating
a written brand rule while claimed on-brand).

**Research / report.** Evidence set: primary sources fetched this
session with access dates; the question's own scope constraints; one
counter-source deliberately sought for the report's central claim.
Authority: primary source > reputable secondary > aggregator > memory
(memory is labeled as such in the output). Observed: every figure
carries a link and access date; arithmetic and unit conversions
recomputed; quotes checked against the page they came from; currency of
volatile facts (prices, policies, versions) checked against the
source's date, not assumed. Frauds: uncited figures, stale figures
presented as current, phantom precision (exact-looking numbers with no
computation behind them), cherry-picked date ranges, a "sources" list
whose entries were never opened.

**Data analysis.** Evidence set: the actual dataset (not a described
version of it), its dictionary/provenance, the requester's definition of
the metric in writing. Authority: the data > the data's documentation >
the requester's recollection of the data. Observed: headline numbers
recompute from raw in one command; dedup, exclusions, and imputations
declared (operational-rigor §4 data-path integrity: no silent defaults,
unmatched records surfaced); the plain-language summary agrees with the
computed table it sits above. Frauds: silent data cleaning, dropped
unmatched records, totals that do not reproduce, a "verified" label on
arithmetic never recomputed, precision the data cannot support.

## 3. Minting a new instance

- Fill the four nouns for the sector. If they do not genuinely differ
  from an existing instance or from the coding defaults (evidence =
  files and tracebacks, authority = the spec, frauds = fake-pass
  shapes), the sector needs no instance — route to the nearest one and
  note the boundary. A sector that is coding in disguise (IaC, script
  logic, pipelines) routes to operational-rigor, not here.
- The red-line gate above applies to minting exactly as to producing:
  no instance for red-line judgment; a sector adjacent to one (tooling
  FOR practitioners, compliance research) follows skill-authoring §5's
  qualified-reviewer requirement.
- Every regulation, policy, threshold, or figure the instance names
  carries a source and access date, fetched now (operational-rigor §4:
  a clue about external data is a map, not a schema; memory is
  labeled).
- An instance without its own trap fixture is not done — the README
  covenant applies to instances exactly as to rules (the fixture's trap
  is the sector's central fraud; its safe outcome obeys
  ground-truth-gates rule 2's trap-armed clause).

## When NOT to use this skill

- Code, infra, or anything with a runtime to observe → operational-rigor
  (+ ground-truth-gates for the gates).
- "What should we build next?" → product-roadmap. Personal goals →
  personal-goal-planning.
- Red-line professional judgment (the gate above) → no checklist; a
  qualified human.
- A one-off trivial lookup — quoting one number with its source needs no
  ceremony.

## Provenance

Promoted 2026-07-18 from a 2026-07-16 staging draft (owner decision D1,
option b: one condensed pattern skill, not eight ported adapters). The
four-nouns pattern, the binding minimum-evidence-set idea, the
per-domain fraud tables, and the instance-needs-its-trap rule adapt
Sahir619/fable-method's domain-adapter schema (MIT; ideas only, no
files copied; see README acknowledgements). Their round-9 result is the
external evidence, cited as shape with its grade: with the marketing
adapter a weak-tier executor found unmentioned source documents and
caught planted frauds that a bare run praised (their measurement, their
fixtures; their round-9a null — a prompt that names the evidence
pre-solves discovery — is why the evidence set here binds the OPENING
of sources, not their mention). The worked instances are this pack's
own compressions, cross-checked against the pack's existing rules
(operational-rigor §4 data-path integrity and external-data discipline;
delegation-and-review §3; skill-authoring §5's authoring-side red-line,
deliberately not duplicated verbatim — the two gates are siblings with
different jobs, each in its own words). `unprobed` in-house per the
README covenant: no probe has run against these instances; the owed
probe is one non-code trap fixture (marketing-style, per the private
suite's protocol) with the trap-armed check.
