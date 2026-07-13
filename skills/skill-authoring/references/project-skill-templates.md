# Project-skill category templates

skill-authoring §5 names the project-skill taxonomy but does not teach how to
write each category. This file does. It is the distillation of seven independent
retiring-architect runs (2026-07-13 mining pass; see the skill-authoring
provenance note) that were each told only to *name* the categories — and
independently converged on the same entry shapes. Load this when authoring or
reviewing a debugging-playbook, failure-archaeology, architecture-contract,
extension-point contract, or the library's entry/manifest/uncertainty files.

## The universal rule (applies to every category below)

A category earns a file, and an entry earns its place in that file, only with a
**real incident or an explicit recorded decision behind it**. Every entry states
an **observable trigger** (the state that means "you are about to touch this"),
not a topic label. An entry with no incident, no decision, and no observable
trigger is a "be careful" — cut it. Preventive invariants for a well-understood
catastrophic mode (data corruption, money loss) are the one allowed exception:
they may exist without a past incident, but say so in the entry ("preventive; not
observed here — this is why the rule exists") so a reader does not hunt for a
commit that isn't there.

---

## failure-archaeology (converged 7/7 — the strongest template)

Purpose: stop a future agent from re-walking a dead end. "We tried that" only
works if you can say *why it died* and *what rule it left*.

**Reconstruct it right.** Dead ends don't always appear as `revert` commits —
where a review pipeline catches failures pre-merge, the evidence instead lives in
stalled/unmerged branches, rejected-experiment reports, in-code rationales, and
deferred-by-design markers (mature repos also carry merged regressions and
fix-forward commits, so don't assume a clean history). Search whichever of git
history, issues, PRs, comments, and branches the repo actually has.

**Entry shape** (each field is load-bearing):

- **Disposition tag** in the title — one of: `dead` (tried, failed) / `rejected`
  (a design considered and declined) / `recurring-trap` / `burned` (a fixture/
  secret/asset spoiled) / `mooted` (was real, then made irrelevant by an
  environment change). The tag tells a reader in one glance what kind of corpse
  this is.
- **What was tried** — with the commit/PR/branch id, so it is checkable.
- **Why it died** — the *mechanism*, not "it didn't work". If a fix itself
  introduced a new bug, record the whole **chain** (A broke, fix B regressed C).
- **The standing rule it produced** — bolded, transferable.
- **Where the residue is now** — the branch, worktree, tmp dir, or closed PR the
  dead end left behind, explicitly tagged **"residue, not in-progress work"** so
  a future agent does not adopt-and-finish it. For a `burned` **secret**, record
  only its revocation status and an incident id — never the secret material or
  its sensitive location.
- **The tripwire** — the observable proposal-keyword that should re-load this
  entry ("any 'a bridge page is faster' / 'just stuff it in localStorage'
  proposal"). Enumerate the tripwires in the skill's frontmatter description so
  the skill loads exactly when someone reaches for a buried idea.

**Two required sub-lists:**

- **Deliberately-not-done** — things intentionally left unbuilt, each with the
  ❌ rationalization a future agent will use to "helpfully" finish them. This is
  stronger and more specific than product-roadmap's Not-now (which is about
  sequencing): its job is to prevent *re-completion* of a deliberate omission.
- **Rejected options + the evidence that killed each** — so nobody refights a
  lost battle. Distinguish "lost" from "never earned entry" ("untested — not
  beaten, just hasn't qualified yet").

**Meta-rule:** a check that looks redundant or paranoid is guilty-until-proven —
it often encodes a demonstrated attack or a paid-for lesson. Find the incident
before relaxing it, and to loosen it supply an equivalent guard (Chesterton's
fence, operationalized). If no incident or current threat model justifies it, it
can be retired — with that rationale recorded, not silently dropped.

---

## debugging-playbook (converged 6/7)

Purpose: a zero-context agent matches on *what it literally sees* — a log line,
an exit code, an error string — not on subsystem names.

**Entry shape:**

- **Trigger = the observed symptom, keyed on a stable verbatim substring** (an
  exact log fragment / exit code / the user's own words) plus a normalized pattern
  for the dynamic parts — IDs, paths, timestamps, and localized wording vary, so
  match on the invariant substring and redact the variable/sensitive bits. A
  wholly paraphrased trigger won't match what's on screen.
- **Evidence first, always.** The first step is to capture evidence, never to
  edit code. State the raw data to pull.
- **Triage branches each terminate at a named observable** — a specific field or
  log line that explains the symptom — then decide. "I changed something and it
  seems better" is not a terminated branch; "run-meta field X explains this
  defer" is.
- **Fork known-limitation from regression.** Inside an entry, split "expected
  behavior / known limitation, tracked as X — do NOT fix" from "real regression".
  Triage must not send someone to fix a deliberate constraint.
- **Done** — the observable green — plus the real incident and the **fix-version**
  it was resolved in.
- **Recurrence signature** (optional, high-value): for a fixed bug, record what a
  re-occurrence would *specifically* implicate ("if this returns, the
  UpdatePrompt stopped going through the markdown-render path"). Turns a fixed
  incident into a fast future diagnosis.

**Structure:** group by the project's own layers (e.g. env/startup, tooling,
pipeline, UI) and bisect to the layer first, then reproduce at the authoritative
layer — the specific grouping is project-specific, not a fixed list. Write one
entry per *failure direction* of a guard (fired-wrongly AND stayed-silent-wrongly
are separate symptoms). Route each entry to the deeper skill that owns the full fix.

---

## architecture-contract (converged 4/7)

Purpose: capture the invariants whose violation "breaks users you cannot see".

**Shape:**

- **Orientation line** — what this repo *fundamentally is* / what it protects,
  in the owner's words.
- **Boundary map** — a small table (path | status: published/private | role)
  before the invariants, so a reader knows what surface they are on.
- **Per-invariant block:**
  - **Trigger = the tempting change that violates it** ("any 'relax the media
    source' / 'support external URLs' / 'this check looks redundant' thought").
  - **The invariant.**
  - **Executable done-check** — a *command*, not prose ("`node build.mjs
    --strict` still rejects ...").
  - **Cited incident or ADR** proving the cost.
  - **"Don't simplify back to ___"** — name the naive implementation the
    invariant exists to forbid ("group by canonical target — do NOT collapse
    back to 'last write wins'").
  - **✅ correct pattern / ❌ the rationalization** (quote a real one).
- **Known-doc-defects** sub-section — where docs and behavior conflict, state
  which is authoritative *for this project*: often the code wins operationally,
  but a published spec, schema, pinned test, or owner decision can outrank buggy
  code — record the authority order, don't assume code always wins.
- **Re-verify command** at the end.

**Standalone additive-compatibility rule** (a useful default wherever interface
stability matters, not an absolute): adding an optional flag or new field is
*usually* safe for consumers that ignore unknown ones — but it can still break a
strict `additionalProperties:false` validator, a snapshot/signature over the
serialized bytes, an ordering assumption, or an exhaustive decoder, so add it on
both sides together and check those. Renaming, re-meaning, or deleting a
flag/key/field is breaking *unless* an alias, compat shim, version negotiation,
or a private-only surface covers it. Confirm against the actual declared
consumers; "not on the frozen list" ≠ "free to change".

---

## extension-point / adapter contract (the §5 taxonomy now names it)

Purpose: "how to add a new plugin / adapter / provider / route / model safely" is
a recurring high-value project-skill; here is the shape (record the project's
actual invariants — these are the common ones, not universals):

1. **Verify the real external shape first** — a clue about external data is a
   map, not a schema (operational-rigor §4): sample the actual field shape on a
   real instance and record it before writing the adapter, or you build a parser
   for a shape that doesn't exist.
2. **Change only the declared extension surface.** Where consumers eat a
   normalized snapshot, adding an adapter should leave the normalized-consumer /
   UI / report layers diff-free; an explicit, listed registration point (a
   registry, factory, or route table) is *expected* to change — that is the
   extension point, not a leak. The invariant to hold: no provider-specific field
   escapes past the adapter boundary.
3. **Extend the canonical conformance suite**, don't copy a sibling's tests
   wholesale — mirror the contract every adapter must meet; copying the biggest
   sibling drags in irrelevant behavior and its old bugs.
4. **Honest-capability posture** — unknown → show `—`, never a fabricated value.
5. **Structural privacy** — decode into a narrow type that omits fields you don't
   need, guarded by a sentinel test (security-architect: minimize-by-type).
6. **Done = conformance suite green + real-instance end-to-end + no
   provider-specific leak past the boundary (only the declared registration
   surface changed).**

---

## Library packaging — the entry/manifest/uncertainty trio (5/7 flagged it)

Five of the seven mined libraries independently flagged this as worth doing; all
seven in fact shipped a MANIFEST + UNCERTAINTY, but the retiring-architect prompt
asked for them, so that is not independent convergence. Treat the trio as
proven-practical *recommended* packaging for a multi-skill library, not a
mandate for every doc.

- **START-HERE / router** (`00-start-here.md` or the always-loaded index):
  orients by the **engineering core, not the domain** ("the hard part here isn't
  the domain content, it's the machine-guaranteed provenance of every answer"); a
  **canonical-source map** (what | where its source-of-truth lives | don't-touch
  caveat); a **current-state triage** of the dirty/red worktree so a fresh agent
  doesn't misread pre-existing breakage as its own; the top disciplines; and a
  reading order. Keep it short — it is a router, not content.
- **MANIFEST** — one line per skill: **what it is → what evidence backs it**
  (the exact PRs/files/incidents/live-queries). A future maintainer can re-verify
  each claim and knows what would falsify it. Prefer "read the directory" over a
  hand-kept file list where possible; pin any unavoidable list with a rule.
- **UNCERTAINTY register** — everything the library deliberately does NOT treat
  as settled, quarantined from the confident content, in labeled buckets:
  confirmed-contradiction-awaiting-owner / not-yours-to-decide / env-dependent or
  user-must-provide / will-go-stale-reverify-before-use /
  locally-unverifiable-provenance / do-not-commit-residue. **Every item ends in a
  safe default**, so a zero-context reader can act ("a deploy/publish command is
  unverified → safe default: hand it to the operator; use the CLI only if the user
  asks and the session is authed").

---

## Re-verification

These templates are a stable authoring method distilled 2026-07-13; nothing here
is environment-specific, so there is no command to re-run. Evidence basis: seven
independent `skills-staging/` libraries at mining time — a class-distilled
convergence (a shape's weight is how many of the seven independently produced
it), no single citable commit. Those staging dirs are **local scratch
(gitignored, not shipped)**, so this is historical provenance, not a
downstream-runnable reference — the templates stand on their own.
