# DISPOSITION — security-enhancement staging batch (graduation audit)

## Publication decision: DECLINED — NOT PUBLISHABLE

Assessed 2026-08-04 against `main` @ `1e38fa8` (post-PR #118). This batch was
audited as a candidate `security-pack` marketplace plugin and is **not
publishable as a public plugin**. This is a valid negative graduation result,
not a failure: the roadmap's graduation gate is allowed to conclude "this should
not ship" rather than manufacture a plugin to satisfy a roadmap name.

Reason:

- two candidates are repository-specific maintenance memory;
- two candidates contain reusable fragments but substantially overlap existing
  opus-pack core doctrine;
- no candidate currently establishes a distinct reusable routing boundary
  (trigger-disjoint from the already-shipped core skills).

This material remains **internal engineering reference** and is **not a
marketplace plugin source**.

It was **not** re-authored into a "minimal kernel" here either. Extracting the
reusable fragments into a new, generalized skill is a separate, owner-gated
skill-design decision — and one that would collide with the mining evaluation's
standing no-new-skill / fold-first ruling — not part of this graduation. The
reusable fragments may later feed an *existing-skill enhancement*, but this PR
does not disguise re-authoring as an as-is graduation.

## Per-candidate classification (so the next session need not re-audit)

| Skill | Class | Why it is not independently publishable |
|---|---|---|
| `skill-vetting-security-invariants` | repo-internal maintenance memory | Seven invariants of THIS repo's `hooks/skill_snapshot.py` + `hooks/skill-vetting-advisory.py`, anchored to ~40+ internal `file:line` sites; its done-checks `grep` this repo's hooks. An external installer gets instructions about files that do not exist in their tree. |
| `skill-vetting-hardening-archaeology` | repo-internal maintenance memory | Failure archaeology of one named campaign (PR #83). Its "owner map" indexes most dead ends into sibling skills (with explicit no-installed-owner fallbacks for config-dir scratch-write hygiene and the D1–D5 designs), and its core meta-signal restates `operational-rigor` §5. Only useful to someone about to re-edit these specific hooks. |
| `mutation-matrix-evidence-discipline` | mixed | R1–R6 are bound to this repo's `hooks/mutation_matrix.py` / `.github/checks.py`. The transferable core (R7 "a test name is not a proof", R8 "verify with the shape the code eats", "prove the tool can FAIL") restates `ground-truth-gates`, which the pack already ships. |
| `security-hardening-review-ops` | mixed | Its own taxonomy splits the 12 OPS rules into six that cite and defer to a core skill (OPS-1/3/4/5/7/12 → `cross-model-review` / `delegation-and-review` / `operational-rigor`) and six project observations with no canonical counterpart, each carrying an `(unprobed — project observation)` marker (OPS-2/6/8/9/10/11). Its own MANIFEST calls them "project observations … not pack-wide behavioral doctrine" — so the transferable orchestration overlaps shipped core review discipline and the rest is campaign-specific, not an independent public capability. |

## What this batch IS

Campaign-shaped maintenance artifacts from the Workstream-B skill-vetting
hardening campaign (PR #83, `7cd2af6`). They are useful to a maintainer about to
re-edit opus-pack's own security hooks, and are kept as internal reference. Read
`START-HERE.md` first, then `MANIFEST.md` (what each artifact claims + its
evidence), then `UNCERTAINTY.md` (the open-risk map). All three are review-only;
START-HERE and MANIFEST additionally carry the **internal-maintainer-reference,
not-for-publish** banner.

## Why no directory move was needed

These files already live outside every marketplace plugin `skills/` root, so the
derived inventory (`published_skills()` in `.github/derived_checks.py`) does not
enumerate them and cannot mis-publish them; the current gates treat them
correctly as non-published. Rather than rename or relocate the batch for form's
sake, the disposition is made durable in-place via this file plus the
not-for-publish banners in `START-HERE.md` / `MANIFEST.md`.

## Reconciliation done alongside this disposition (issue #120)

The stale doc-vs-code records that **PR #118 (`c7951bc`, the #104 fix)** already
resolved have been marked **RESOLVED in-place** — history preserved, the current
correct behavior stated, and semantic anchors (goal / rule name) preferred over
line numbers that have since drifted:

- `skill-vetting-security-invariants` INV-5's parenthetical (defect (c): advisory
  logging framed as guaranteed/auditable);
- `UNCERTAINTY.md`'s "Known live-doc defects" block (defects (a)–(d)) and the
  embedded doc-defect notes inside open items 3 and 4;
- `START-HERE.md`'s source-map caveat.

The **five genuinely open security gaps** — G3-SHELL, G3 prose-injection, the §1
procedure boundary, I11 full concurrency serialization, and the I2/I10 halves —
remain **OPEN** and were deliberately not altered by this reconciliation. The
round-8 design D1–D5 stays unimplemented.

## Out of scope for this PR

No marketplace manifest, no move into a plugin root, no change to the published
opus-pack skills, and none of #105 item 2 / #117 / round-5 probes / #123.
