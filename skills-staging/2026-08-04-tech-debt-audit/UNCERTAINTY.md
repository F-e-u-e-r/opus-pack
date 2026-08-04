# UNCERTAINTY — what this library does NOT treat as settled

Everything the fix-and-review pass surfaced that could not be stated as a
verified, authoritative rule. Each item ends in a **safe default** a
zero-context reader can act on.

## Two adversarial review rounds ran, not the multi-round ladder siblings cite

Round 1 found and the author fixed a real leak in the pre-fix `mask()`
function and a self-test whose containment assertion tested an
unreachable path. Round 2 independently re-derived the fix from the
code (not from the fix description), reproduced the leak's absence with
its OWN planted secrets (a fake GitHub token, distinct from the
self-test's fixtures), and separately found two `DEP-UNUSED`
substring-boundary defects (a false positive on the `plugin:x/y` ESLint
idiom, a false negative where one dependency name is a substring of an
unrelated one) plus a `SCAN-INCOMPLETE` boundary gap (a tree with
exactly the walk cap's file count, fully covered, incorrectly flagged as
truncated). All three were fixed and re-verified against the reviewer's
own repro shapes, plus one further boundary case the fix itself
surfaced (a single very large directory can push the walk's output past
the nominal cap in one step while genuinely completing full coverage —
documented in the `walk()` function comment as a coverage-vs-size-bound
distinction, not treated as a defect). The sibling `2026-07-30-*` batches
in this directory each cite a deeper ladder (a five-screener +
three-reviewer + final-gate orchestration, or a two-family post-merge
review). This library has not been through that depth. **Safe default:**
an installer should still run at least one more independent adversarial
pass before trusting this in a workflow where the scan output reaches an
untrusted or lower-trust context than the installer's own — particularly
against real-world config-file shapes the DEP-UNUSED corpus has not
seen (see below).

## The password-assignment / test-path trade-off is a judgment call, not a proof

`SECRET_PATTERNS`' `password-assignment` regex is suppressed under
test/spec/fixture paths to kill a real false-positive rate (an ordinary
auth-test fixture was flooding findings pre-fix). The other five secret
patterns are NOT suppressed there, on the reasoning that they match a
fixed high-entropy format (an AWS key shape, a PEM header, a GitHub
token shape) a hand-written test fixture is unlikely to reproduce by
accident. That reasoning was not adversarially tested against a
counter-example — nobody tried to construct a test fixture that
legitimately trips one of the five "safe" patterns. **Safe default:**
treat all five unsuppressed classes as still-live inside test paths (do
not assume test-path exemption extends beyond `password-assignment`),
and if a false positive shows up on one of the five inside a test path,
narrow that pattern's suppression rather than widening `TEST_PATH` — the
five were deliberately left broad because the leak-containment
mechanism (the fingerprint, not the pattern match) is what makes a false
positive cheap, not free.

## DEP-UNUSED's matching is now boundary-safe, but the config-format space is untested

Round 2 found and the fix closed a real matching defect: `d` is now
matched with `(^|[^A-Za-z0-9_.-])${d}($|[^A-Za-z0-9_.-])`, verified to
correctly find `my-plugin` inside `"plugin:my-plugin/recommended"` (was
missed) and to correctly NOT count `react-native-paper` as evidence for
`react` (was miscounted as used). What remains untested is the corpus
itself — YAML-based tool configs, a `Makefile` or shell script invoking
a CLI-only dependency by name, and any config format the tool's file
extension list doesn't recognize are all still outside the scanned
corpus (the finding line already says so). **Safe default:** treat every
`DEP-UNUSED` finding as requiring the one-targeted-search confirmation
the finding line itself asks for; do not batch-remove without it.

## The no-git fallback path's cap logic has been directly exercised, not at real scale

Round 2 verified `walk()`'s truncation detection against two shapes: a
tree with exactly the cap's file count spread across two large
directories (correctly does NOT fire — nothing was actually skipped,
even though the cap logic overshoots the nominal number in that shape),
and a tree spread across many small directories that genuinely leaves
some unexplored when the cap is hit (correctly DOES fire). Both were
purpose-built fixtures at a few thousand files, not a real repository at
scale (tens of thousands of files, deep nesting, unusual permissions).
**Safe default:** if a real audit target is `.git`-less and large,
verify the `SCAN-INCOMPLETE` line actually appears (or is genuinely
absent because coverage was complete) rather than assuming the cap
logic generalizes past what was tested here.
