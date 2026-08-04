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

## The password-assignment / test-path trade-off — NOW MEASURED, still a judgment call

`SECRET_PATTERNS`' `password-assignment` regex is suppressed under
test/spec/fixture paths to kill a real false-positive rate (an ordinary
auth-test fixture was flooding findings pre-fix). The other five secret
patterns are NOT suppressed there. This item previously said "nobody
tried to construct a test fixture that legitimately trips one of the
five 'safe' patterns" — that gap is now closed: a fixture of hand-typed,
format-valid-but-fake test constants (fake AWS key, GitHub token, `sk-`
key, bearer token) fired 4 of 5 patterns inside a test path (the 5th, a
PEM block, wasn't exercised by the fixture's extension). The asymmetry
is confirmed real, not just plausible, and confirmed cheap: every hit
comes out masked, so the cost is a human reading one extra line, not a
leak. **Safe default (unchanged):** treat all five unsuppressed classes
as still-live inside test paths, and if a real false positive shows up
in practice, narrow that ONE pattern's suppression rather than widening
`TEST_PATH` to all six.

## DEP-UNUSED's matching is boundary-safe AND now covers extension-less config files

Round 2 closed the token-boundary matching defect (verified against
`plugin:my-plugin/recommended` and `react-native-paper`/`react`). This
round closed a second, independently confirmed gap: a dependency
referenced ONLY from an extension-less file (`Makefile`, `Dockerfile`,
etc.) was false-flagged unused, because `path.extname("Makefile")` is
empty and the corpus filter dropped it entirely — reproduced live with a
Makefile invoking `esbuild` via a recipe line, confirmed false-flagged
pre-fix, confirmed clean post-fix, and mutation-tested (reverting the
basename-match code makes the self-test's own Makefile fixture fail).
YAML-based tool configs were also probed directly (a GitHub Actions
workflow invoking `wrangler` via `npx`) and found to already work
correctly — `.yml` was already in `TEXT_EXT`. A round-3 adversarial pass
found the Makefile-basename fix itself had two naming-convention gaps —
GNU Make's own lowercase `makefile` variant, and Dockerfile's suffixed
forms (`Dockerfile.dev`, `Dockerfile.prod`) — both closed and covered by
regression fixtures. The same pass surfaced a real trade-off the corpus
widening introduces and this fixed: a dependency whose npm package name
is literally `make` (or, less exotically, `docker`/`rake`/etc.), and is
genuinely unused, can now read as "used" if the Makefile/Dockerfile/etc.
merely contains ordinary self-referential build syntax (`$(MAKE) -C
sub`, `docker build`) — the corpus match has no way to distinguish a
recipe's use of the *tool itself* from a reference to a same-named npm
package. This is judged not worth a special case: excluding one literal
string (`make`) from the corpus scan would itself be a fragile,
undocumented carve-out for what is a narrow collision (an npm package
sharing a name with a common CLI tool, declared as a dependency, and
genuinely unused). What remains genuinely untested: a build tool's own
bespoke config format not on the extension or basename list, and dynamic
string-built imports. **Safe default (unchanged, plus one addition):**
treat every `DEP-UNUSED` finding as requiring the one-targeted-search
confirmation the finding line asks for; for a dependency named after a
common build tool (`make`, `docker`, `rake`, ...) specifically, don't
treat an "unused" absence-of-finding as proof of use either — the corpus
match can be fooled by the tool's own recipe syntax.

## The no-git fallback path's cap logic — verified at real scale, plus a fixed silent-swallow defect

Round 2 verified the cap-truncation logic on purpose-built fixtures at a
few thousand files. This round ran it against a real-scale tree — 30,000
files across 300 directories plus 60 levels of nesting — with no crash
and no meaningful slowdown (68ms), and `SCAN-INCOMPLETE` fired correctly
on cap cutoff. Separately, and more seriously: an UNREADABLE directory
(`chmod 000`) inside a no-git tree was silently swallowed by `walk()`'s
`catch { continue }`, with no signal that anything was skipped — the
scan reported "clean" coverage while having read nothing under that
subtree. This is now fixed (a read failure counts toward `truncated`,
same as a cap cutoff) and mutation-tested: reverting the fix independently
makes the self-test's own unreadable-directory fixture fail. A round-3
pass found the identical silent-swallow shape one level down: `scanRepo`'s
per-file `statSync`/`readFileSync` calls had their own `catch { continue
}`, so a single unreadable FILE (permission revoked after `git ls-files`
listed it, or a race with a delete) was dropped with zero signal — same
"clean scan that read nothing from this path" failure, just scoped to one
file instead of a subtree, and applying even in a git-tracked repo (a
tracked file's permissions can change after listing, unlike the no-git
directory case). Fixed the same way (folded into `SCAN-INCOMPLETE`) and
mutation-tested the same way. Checked directly: a symlinked directory is not a cycle risk — `readdirSync`
with `withFileTypes` reports a symlink's `isDirectory()` as `false`
regardless of what it points to, so `walk()` never pushes it onto the
traversal stack; it lands in `out` as an ordinary entry, then
`fs.statSync` (which follows symlinks) sees it's not a file and skips it
via `continue`. No hang, no cycle — but also no coverage: a symlinked
directory's contents are silently never scanned, and (unlike the
unreadable-directory case) nothing currently flags this as a skip. Two
real gaps remain, unmeasured: a directory whose permissions revert
mid-scan (TOCTOU) is out of scope for a single-pass tool, and `walk()`
was not run against tens of millions of files or genuinely unusual
filesystem types (network mounts, case-insensitive filesystems).
**Safe default:** if a real audit target is `.git`-less, large, has
restricted-permission subtrees, or uses symlinked directories, verify the
`SCAN-INCOMPLETE` line appears (or is genuinely absent) and separately
confirm any symlinked directories were reviewed by hand — a clean exit
does not cover them.
