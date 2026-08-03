# PR 3 design note — derived checks enforcing the architecture contract

Design + implementation boundaries for the `.github/checks.py` extension that
mechanically enforces the `ARCHITECTURE.md` contract landed in PR 2 (#121). This
note is written **before** the checker code, and the fixture matrix at the end is
the accept/reject spec each gate implements. It exists so the checks enforce a
real, authored canon — never "documentation validating itself" — and so no gate
over-claims (see `ARCHITECTURE.md` §8).

## Scope and non-goals

In scope (PR 3): a new authored-once dependency canon
(`metadata/plugin-dependencies.json`), stable README projection markers, and
checks.py gates for tier-canon integrity, README projection parity, extension
dependency contract, derived inventory + globally-unique skill IDs, and the
§7 normative-reference non-dangling gate — each with a red/green two-sided proof.

Out of scope / locked (this PR changes none of these):
- skill `description`s (routing contracts — a separate PR);
- merged policy **semantics** in `ARCHITECTURE.md` (only additive, non-rendering
  README markers may be added; §§1–8 wording is not rewritten);
- tier membership or the design-pack classification (already gated by canon);
- auto-fix (checks report; they never mutate);
- the `#115` marker covenant scope (`grep -rn 'unprobed' skills/`) — it stays
  `skills/`-only and MUST NOT widen because the inventory gate now walks the
  whole marketplace surface. The two enumerations are independent by design.

Every failure message names the **canon**, the **file**, and the **specific
difference** (not just "mismatch"). The final tri-lens verdict binds the exact
committed tree; any post-review edit re-verifies the affected part.

## Boundary 1 — extension dependency class needs an authored-once canon

`recommended-with` is a human architecture judgment (audit-backed, `ARCHITECTURE.md`
§4.1); it is NOT derivable from the filesystem or the READMEs. Two READMEs each
stating it once is a projection with no canon to project *from*. New canon:

`metadata/plugin-dependencies.json`
```json
{
  "schema_version": 1,
  "plugins": {
    "design-pack": { "dependency_class": "recommended_with", "companion_plugin": "opus-pack" }
  }
}
```
Records ONLY the non-derivable dependency judgment — no plugin paths, no skill
inventory, no fallback prose (all derivable/owned elsewhere). JSON enum values
use underscores (`recommended_with`) to match `skill-tiers.json`'s
`domain_adapter`; prose/README render them hyphenated (`recommended-with`); the
checker maps the two spellings in one place.

Gate `extension_dependency_contract` asserts:
- file parses; `schema_version` is a supported value (currently `1`);
- `dependency_class` ∈ {`standalone`, `requires`, `recommended_with`};
- `standalone` MUST NOT carry a `companion_plugin`;
- `requires` / `recommended_with` MUST name a `companion_plugin` that is an
  existing marketplace plugin (resolved from `marketplace.json`, not hard-coded);
- every **extension** plugin (every marketplace plugin except the base/root
  plugin — the entry whose `source` is `./`, i.e. `opus-pack`) has exactly one
  entry; the base plugin has none (it is the referent, not an extension);
- the READMEs' dependency-class line (boundary 4) matches this canon.

If any of the above cannot be implemented cleanly, the honest fallback is to
DOWNGRADE this to a file-existence + schema check and say so in `ARCHITECTURE.md`
§8 — never claim a dependency-contract guarantee the code does not deliver.

## Boundary 2 — a precise, single "published skill" definition

**Definition:** a published skill is a skill directory reachable through a
plugin's declared published-skill root, containing its required `SKILL.md`, and
included in the marketplace-distributed plugin surface. Staging, fixtures,
examples, and undeclared directories are NOT published skills.

Operationally (aligns with existing checks.py enumeration, lines ~57–92): the
published-skill root of a marketplace plugin is `<source>/skills/` where
`<source>` is that plugin's `marketplace.json` entry source. Enumeration starts
from `marketplace.json` plugins[] — never a repo-wide `find SKILL.md`. Two-sided
checks:
- every manifest-declared skills root exists (already: checks.py line 84);
- every immediate child directory of a root that is a published skill resolves
  (contains `SKILL.md`; check 1 already fails a listed dir lacking one — the
  inventory gate makes "listed but no SKILL.md" an explicit inventory failure
  with a clear message rather than only a frontmatter failure);
- each published skill belongs to exactly one plugin (a directory reachable
  through two plugins' roots is a conflict);
- `skills-staging/`, `evals/`, fixtures, and any directory not under a
  manifest-declared root are excluded — asserted by a fixture that plants a
  staging-shaped dir and proves it is NOT counted;
- the `#115` covenant grep is unchanged and independent (scope-lock above).

## Boundary 3 — one canonical skill ID

Canonical skill ID = the **directory basename**. It already must equal the
`SKILL.md` frontmatter `name` (checks.py check 1); PR 3 does not introduce a
second identity source and does not let the checker choose among basename /
frontmatter / README label. Marketplace-wide uniqueness: the set of published
skill IDs across ALL plugins has no duplicate (today opus-pack's 10 + design-pack's
3 are distinct). Normative references (boundary 5) resolve skills by this same ID.

## Boundary 4 — README projection via stable, unique markers

No fragile heuristics (e.g. "first table containing `Core`"). Add non-rendering
HTML-comment markers around the existing projected blocks in BOTH READMEs — a
narrow, render-neutral edit; policy wording, tier membership, dependency
classification, and descriptions are NOT changed:
```
<!-- BEGIN GENERATED SKILL TIERS -->
… existing tier table …
<!-- END GENERATED SKILL TIERS -->

<!-- BEGIN GENERATED PLUGIN DEPENDENCIES -->
… existing design-pack recommended-with line …
<!-- END GENERATED PLUGIN DEPENDENCIES -->
```
Gate asserts:
- each marker is unique and correctly paired (BEGIN before END, no nesting) in
  each README;
- the skill set + tier inside the TIERS markers matches `skill-tiers.json`;
- the dependency class inside the DEPENDENCIES markers matches
  `plugin-dependencies.json`;
- EN and zh-Hant may use different display prose, but the canonical **IDs** and
  **classifications** parsed from inside the markers are identical to the canon
  (parity is over IDs/classes, NOT translated prose — `ARCHITECTURE.md` §8 already
  states the checker does not verify translation semantics);
- the policy link to `ARCHITECTURE.md` and the canonical-source notice are
  present in both READMEs.

## Boundary 5 — normative-reference gate: only the landed §7 grammar

The gate implements EXACTLY the `ARCHITECTURE.md` §7 grammar and nothing broader;
it never guesses natural-language references. Precise grammar the gate parses
(this spec lives here, not hidden in a regex):

- A normative reference is `<published-skill-id> §<section-token>` with the skill
  ID and the `§` marker on the **same line**.
- `<section-token>` accepted forms: `N` and `N.M` (section, subsection) where
  N, M are digit runs — e.g. `operational-rigor §3`, `design-review-gate §4.1`.
- **Excluded from parsing** (not matched, so never flagged): anything inside a
  fenced code block (```` ``` ````), inline code (`` `…` ``), or a line the spec
  marks non-normative. Bare skill mentions with no `§` are not references.

Resolution:
- the gate matches ONLY known published skill IDs (an explicit alternation), NOT
  a broad `<kebab> §N` pattern — because `<name> §N` is ALSO the repo's
  external-source citation form (`agent-standard-oss §8`, a real false positive a
  broad pattern produced against the live tree during the build). So the gate
  verifies section existence for references to REAL skills and does NOT detect a
  reference to a non-existent skill NAME (indistinguishable from an external
  citation without a brittle allowlist); recorded in `ARCHITECTURE.md` §8;
- **local** reference (target skill in the SAME plugin as the citing file):
  the target `SKILL.md` must contain that section — section N exists iff a
  `^## N. ` heading exists; subsection N.M iff a `^### N.M ` (or documented
  heading form) exists. Missing → FAIL, message naming citing file:line, the
  reference, and the missing target section;
- **cross-plugin** reference (target in a different plugin): produce a stable
  REPORT line, do NOT fail (a plugin may be installed without its companion).

**Flagged §7 ambiguities (per the "list, don't sneak into regex" rule) — the gate
takes the narrowest sound reading and these are recorded for a possible future
§7 tightening, NOT patched into code silently:**
1. §7 prose says "section number"; real usage includes subsections (`§4.1`) and
   ranges (`§§2–3`, `§§1–3`). The gate parses single `§N` / `§N.M`. **Ranges
   `§§N–M` are NOT parsed as references in v1** — the double `§` prevents a
   match, so a range is silently not treated as a reference; nothing is counted
   or failed (no advisory is emitted). A clean range-endpoint semantics belongs
   in a §7 refinement, out of this PR.
   Code-region scanner (bounded, contract-scoped — the reference and README
   scans exclude code identically). Line endings are normalized CRLF/CR → LF and
   split on LF only (never `splitlines()`, which also breaks on NEL/LS/PS/VT/FF
   and would let a non-space/tab fence suffix slip through). Inline code spans are
   **delimiter-run matched** (a run of N backticks opens; the next run of EXACTLY
   N closes, so a double-backtick span may contain single backticks) and may be
   **multi-line**: spans are matched over a block (consecutive non-blank,
   non-fence lines) and reset at a blank line or fence, so a code span crossing
   line endings is excluded (CommonMark normalizes line endings inside a span).
   Fenced blocks track the opener's **(char, length)** and close only on a later
   fence of the same char, a length >= the opener's, and followed by only **ASCII
   spaces or tabs** (CommonMark 0.31.2); a backtick fence whose info string
   contains a backtick is not a fence opener; a shorter, different-char, or
   other-whitespace (e.g. NBSP) fence line inside a block is content, not a
   close. It is a FINITE-STATE scanner over code spans + fenced blocks, NOT a
   CommonMark parser.
   **Non-goals (explicitly out of contract):** lists, HTML blocks, emphasis,
   link parsing, 4-space indented code blocks, and any other Markdown construct —
   a `§`-reference inside those is scanned as normal text. The two round-2 cases
   (a double-backtick span containing a single backtick; a mixed-length nested
   fence) are **FIXED** by this scanner with red/green fixtures, not accepted as
   defects. One residual limit remains: an UNCLOSED fence runs to end of file (a
   rare malformed file; fails toward under-reporting, never a false failure).
   Closer-suffix adjudication: a targeted round-2 review claimed a trailing TAB
   should be rejected after a closer, but current CommonMark (0.31.2) permits
   **spaces or tabs** — that premise is invalid, so the closer accepts tabs.
   The review nonetheless half-surfaced a real bug: the original `.strip()`
   accepted ANY Unicode whitespace (NBSP, vertical tab, form feed), broader than
   the spec; the closer now accepts only ASCII space/tab
   (`all(c in " \t" ...)`), with fixtures proving TAB accepted and NBSP rejected.

   Owner-authorized TERMINAL remediation batch (2026-08-03, sol max senior lens
   flagged seven, all fixed here, each with a red/green fixture): (1) malformed
   nested canon values (e.g. a list `dependency_class`) fail closed, no crash;
   (2) a boolean `schema_version` is rejected (bool is an int subclass, so an
   exact non-bool int check); (3) README dependency parity now checks class AND
   companion and rejects a plugin declared more than once; (4) a backtick fence
   whose info string contains a backtick is not a fence opener; (5) line
   splitting normalizes CRLF/CR → LF and splits on LF only (not `splitlines()`);
   (6) §8 aligned to the actual GLOBAL link/notice check (only the tier and
   dependency blocks are marker-bound); (7) multi-line inline code spans are
   excluded (above). Scanner kept stdlib-only + bounded (code spans + fenced
   blocks); non-goals unchanged. If a future review finds a new reproducible
   in-contract defect, the pre-agreed escalation is "adopt a fixed-version
   CommonMark parser dependency" or "formally amend the public contract" — not
   another bespoke-scanner patch round.

   Closure note (sol targeted closure, 2026-08-03): Sol correctly identified that
   the link/notice projection check used the fence-only scanner view. The
   proposed parser escalation was unnecessary because the existing bounded
   scanner already supports inline-code masking. The check now uses that existing
   mode, with two-sided regression coverage.
2. The repo also uses non-§ forms like `ground-truth-gates rule 4` and bare
   skill mentions. These are OUTSIDE §7's canonical grammar, so the gate does
   NOT check them (consistent with §8: "a reference written outside this grammar
   cannot be mechanically checked"). Migrating them to canonical `§` form is a
   separate effort, not PR 3.
3. Section existence is judged against the heading form `## N.` / `### N.M`. If a
   skill uses a different heading convention, that skill's §-references would
   report as dangling — this surfaces real drift, but the design note records the
   heading convention as the assumed section-anchor form so it is explicit.

## The full check set PR 3 adds to checks.py

1. tier-canon integrity (`skill-tiers.json` — schema, valid tiers, exact match
   to published opus-pack skills, each once, no missing/extra/unpublished);
2. extension dependency contract (`plugin-dependencies.json` — boundary 1);
3. derived inventory + globally-unique published skill IDs (boundary 2 + 3);
4. README projection parity via markers (boundary 4 — tiers + dependencies +
   link + notice, EN & zh-Hant);
5. §7 normative-reference non-dangling gate (boundary 5 — local fail /
   cross-plugin report / code-fence immune).

## Fixture / test matrix (red + green two-sided proof per gate)

Every gate ships with a case that PASSES on the real tree AND a case that FAILS
when the property is violated (built as temp-tree fixtures; the checker must be
shown able to fail). Minimum matrix:

- **tier-canon:** green (real canon); red — malformed JSON; unsupported
  `schema_version`; invalid tier value; a published skill missing from the map;
  an extra/nonexistent skill in the map; a duplicate skill key.
- **dependency contract:** green (design-pack recommended_with); red — nonexistent
  plugin entry; invalid `dependency_class`; `standalone` with a `companion`;
  `requires`/`recommended_with` with a missing/nonexistent companion; an
  extension plugin with no entry.
- **inventory + IDs:** green (10+3 distinct); red — duplicate global skill ID
  across plugins; a manifest root that does not exist; an orphan published-skill
  dir with no SKILL.md; a staging-shaped dir proven NOT counted; `#115` grep
  scope proven unchanged (a fixture asserting the covenant scan still targets
  only `skills/`).
- **README parity:** green (real READMEs after markers added); red — a skill
  missing inside the markers; wrong tier inside markers; wrong dependency class;
  missing/duplicated/unpaired marker; missing policy link; missing
  canonical-source notice; EN/zh canonical-ID set mismatch.
- **reference gate:** green — a valid local `§` reference resolves; red — a
  dangling local section (known skill, missing section); a cross-plugin reference
  with a missing section is REPORTED not failed; false-positive immunity — a `§`
  reference INSIDE a code fence is NOT flagged. (Dangling-skill-NAME is NOT a
  gated case: `<name> §N` collides with external-source citation syntax, so the
  gate checks known-skill references only — see boundary 5.)

## Execution + review

Build order: (1) `metadata/plugin-dependencies.json`; (2) README markers
(narrow, render-neutral); (3) the accept/reject reference fixtures; (4) the
checks.py gates + their fixtures; (5) run checks.py green + the two-sided fixture
proofs. Then the standing cadence: grok-4.5 high solo → grok-4.5 high +
gpt-5.6-luna ultra → gpt-5.6-sol max pre-commit, the final verdict bound to the
exact committed tree. `ARCHITECTURE.md` §8's "designed to guarantee" list is
updated to past-tense only for the checks actually implemented here.
