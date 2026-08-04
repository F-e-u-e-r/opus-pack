---
name: tech-debt-audit
description: Detect technical debt across one repo or a whole workspace of them — secrets in tracked files, personal data hiding in fixtures, missing version control, committed binaries, unused dependencies, uncommitted drift — and re-audit against a recorded baseline. Load when the user asks "any technical debt in my projects?", "audit this repo", "is anything leaking in here?", or wants a periodic hygiene sweep; also before adopting or publishing a repo you did not write. Ships a runnable zero-dependency detector (scripts/debt-scan.mjs) whose output is safe to read into context. NOT a security design review (security-architect), not a test-gate builder (ground-truth-gates), not a code-quality review.
---

# Tech-Debt Audit

Find the debt that bites: leaked values, unprotected work, dead weight, and
drift — ranked, verified, and re-checkable. An audit produces findings a
skeptic can reproduce, not a vibe about code quality.

## Method

1. **Enumerate before you scan.** List the repos/surfaces that actually
   exist (every `.git` under the workspace root, plus project directories
   WITHOUT one — those are findings, not gaps in the list). Which trees
   matter is not recallable from what workspaces usually contain.

2. **Run the detector, read its output — not the raw values.**

   ```
   node scripts/debt-scan.mjs <repo-dir>
   ```

   Exit 0 = no actionable findings, 1 = findings, 2 = error. One line per
   finding: `CLASS severity path[:line] — note`. A secret match is
   reported as a one-way sha256 fingerprint plus a coarse length bucket —
   never a slice, prefix, suffix, or exact length, since even those leak
   real bits of the value. PII findings report field names and counts
   only — never values.

   **Why a script and not a grep:** grepping for secrets or personal data
   prints the values into your own context, and a value read into context
   is a value leaked into context (security-architect, behavior rule 1).
   The detector does the matching in-process and reports class + location
   + a one-way fingerprint, so the audit itself does not become the leak.
   Its self-test asserts this containment against the secret its
   CONTENT-scan path actually reaches (not a credential-named file, whose
   contents the scanner never opens at all — see `PII-SHAPE`'s sibling
   `SECRET-NAME` above), checking every run of the raw value down to 6
   characters, not just the full string, so a partial leak still fails.

3. **What each class means, and the fix that closes it:**

   - `VCS-MISSING` — no `.git`, but ignore rules or credential-shaped
     files present. A `.gitignore` protects nothing in an unversioned
     tree, and the work has no recovery history. Fix: `git init`, stage
     with the ignore rules in place, VERIFY the staged list is clean
     before the first commit (`git ls-files` vs the secret names).
   - `SECRET-NAME` — a credential-named file is tracked. The finding is
     metadata-only; do not open the file to "check". Fix: untrack, ignore,
     and ROTATE whatever it held — a secret that ever reached history is
     burned regardless of later deletion (security-architect, "Leaked /
     committed secret").
   - `SECRET-CONTENT` — a secret-shaped string in a tracked text file
     (reported masked). Same fix: rotate first, then remove.
   - `PII-SHAPE` — personal-data field co-occurrence in a data file. The
     scan sees shape, not provenance: an untagged hit is PRESUMED REAL and
     goes to the owner, who may confirm it synthetic or have the fixture
     sentinel-tagged (ground-truth-gates, sentinel-tagged fixtures) so the
     next audit is one grep instead of a conversation. Do not clear a hit
     because the path says `examples/` — a name is not provenance
     (security-architect, threat-model bullet).
   - `BIG-BINARY` — a file over the size threshold, tracked or (in an
     unversioned tree) simply sitting on disk. Fix: `git rm --cached` +
     ignore; note history still carries a tracked one (shrinking history
     is a separate, destructive decision for the owner).
   - `SCAN-INCOMPLETE` — only in a `.git`-less tree: the fallback file
     walk hit its cap before covering the whole directory. The scan you
     just read is partial, not clean — `git init` and re-scan for full
     coverage, or treat any absence of other findings as unproven.
   - `DEP-UNUSED` — a declared dependency with zero import/require hits.
     Confirm with one targeted search before removing (dynamic loading,
     CLI-only use, and non-JS consumers are the false-positive routes).
   - `DRIFT` — uncommitted changes. Informational; old drift on an
     otherwise-idle repo usually marks abandoned or unlanded work worth
     asking about.

4. **A detector finding is a claim.** Before relaying any high-severity
   finding, reproduce it by an independent route (for a tracked credential:
   `git ls-files | grep`, not a re-run of the same tool; for PII-SHAPE:
   field names via a JSON parse, still never values). Rate what survives
   on security-architect's severity ladder — severity binds to the
   evidenced path, not to the class name.

5. **Re-audit as a delta, not a fresh start.** Record the audit's findings
   and fixes (paths, classes, the verification used) somewhere durable.
   The next audit reports three lists against that baseline: **HELD** (fix
   intact — one line), **REGRESSED** (old finding back — lead with these),
   **NEW**. A finding absent from the new scan is not thereby resolved —
   scan bounds moved, files moved, or the scanner changed; close a
   baseline item only by pointing at the fix that closed it
   (delegation-and-review, "absence is not resolution").

6. **Fixing is a separate task.** The audit ends at ranked, verified
   findings. A fix batch is normal multi-repo mutating work — task
   contract, scope containment, per-item commits sized so a single item
   can be reverted independently (operational-rigor §1, §3). If the user
   later reports breakage and orders a revert, the rollback-order rule
   applies (operational-rigor §3): honor the order, scope by causal
   reachability, name what you hold back.

## Declared bounds — say these when relaying results

The detector is verbatim-pattern, tracked-files, single-revision: it does
NOT scan git history (a secret only in history is invisible to it and
still burned — check history separately with `git log -S` on the names it
DID flag), does not decode encoded or derived copies, cannot rate
reachability or exploitability (that is a security review), and its
PII-SHAPE class cannot distinguish real from synthetic — by design, that
judgment is the owner's. `DEP-UNUSED`'s corpus covers source AND common
config files, but not every consumption route (dynamic string-built
imports, a build tool's own config format the tool doesn't recognize) —
its finding line says so and asks for one targeted confirm before
removing. The `password-assignment` secret pattern is suppressed under
test/spec/fixture paths (real false-positive rate there); the other five
secret patterns are not suppressed anywhere, because they match a fixed
high-entropy format ordinary code is unlikely to reproduce by accident —
that asymmetry is a judgment call, not a proof, and a real credential
pasted into a test fixture would be missed by this one suppression. The
fingerprint in a `SECRET-CONTENT`/`SECRET-NAME` finding is a plain,
unsalted sha256 of the matched value: for the five high-entropy patterns
this discloses nothing practical, but for a low-entropy or common
guessable value under `password-assignment`, a reader who already
suspects a candidate can hash their guess and compare — the fingerprint
is one-way, not immune to a confirmation attack against a small guess
space. A clean exit 0 means "none of these classes, in this tree, at this
revision, within these bounds", never "no debt".

## Sources

Distilled from a contributor's five-repo audit-and-fix session (2026-07-14,
contributor-reported, not linkable) whose incidents seeded the classes: an
unversioned automation tree whose `.gitignore` guarded nothing
(VCS-MISSING), a live agent password in a tracked `credentials.json`
(SECRET-NAME), meeting credentials recoverable from git history (the
history bound above), a real family's data in an `examples/*.json`
presumed placeholder (PII-SHAPE — the same incident behind
security-architect's untagged-example clause), 559 MB of committed release
binaries (BIG-BINARY), and framework dependencies with zero imports
(DEP-UNUSED). `scripts/debt-scan.mjs` ran green two-sided on 2026-08-04
(`--self-test`: clean tree 0 actionable, planted tree all 6 classes fired,
no-git tree fired, containment held down to any 6-character run of the
planted secret) and, historically-valid but not independently
re-checkable here, was run against two of the incident's real repos
read-only: the fixed automation tree scanned clean; the `examples/` repo
re-fired PII-SHAPE on the redaction's own untagged same-shape stand-ins,
which is the escalation working as specified rather than a false
positive — an installer without access to that private repo cannot
re-verify this pair directly. Ships `unprobed` per the covenant.

## Review status

One fresh-context adversarial round before this delivery. Round 1
verdict: DO-NOT-SHIP — the top finding, reproduced live, was that the
original `mask()` sliced and printed real leading/trailing characters
plus the exact length of every matched secret, which falsified the
skill's central claim, and the self-test's own containment check tested
a value the content-scan path could never reach (a credential-NAMED
file's contents are never opened), so it would have passed regardless.
Fixed: `mask()` now emits a one-way sha256 fingerprint and a coarse
length bucket only — zero characters, zero exact length; the self-test
now checks 6-char-run containment against the secret the content-scan
path actually processes. Also applied from the same round:
`password-assignment` suppressed under test/spec/fixture paths (was
flooding auth-test fixtures with masked-but-still-partial findings before
the mask fix, and remains a documented gap after it — see Declared
bounds), `DEP-UNUSED`'s corpus widened to config files (was missing a
dependency referenced only from `.eslintrc.json`-shaped config, not
source), `BIG-BINARY` extended to the no-git path, and a new
`SCAN-INCOMPLETE` class added so the no-git fallback's file-count cap is
never silent. Re-verified after fixes: `--self-test` green, the original
manual leak repro no longer leaks (confirmed byte-for-byte — the fixed
output carries a fingerprint, not `AKI...OP`), both false-positive repros
confirmed fixed, both real-repo re-validations (bluecross, zoom) unchanged
from before the fix.

**Round 2** independently re-derived every round-1 fix from the code
(not from its description) and reproduced the leak's absence with its
OWN planted secrets, distinct from round 1's and the self-test's
fixtures — confirming both round-1 BLOCKING findings genuinely fixed, not
just described as fixed. It also found two new defects in the
`DEP-UNUSED` matching the round-1 fix had introduced: a false positive on
the `plugin:x/y` ESLint idiom (the dependency name doesn't immediately
follow a quote) and a false negative where one dependency's name is a
plain substring of an unrelated one (`react` inside
`react-native-paper`). Fixed with a token-boundary regex, verified
against both exact repros. It also found `SCAN-INCOMPLETE` could
misfire on a tree whose file count happened to equal the walk cap while
still being fully covered; fixed by checking whether the walk's stack
still holds unexplored directories rather than comparing a count,
verified against both the false-positive shape (two large directories,
exactly at the cap, fully covered — does not fire) and a genuine
truncation shape (many small directories, cap hit mid-walk — fires).
Round 2 verdict: SHIP-AFTER-FIXES; all findings applied and re-verified.
See UNCERTAINTY.md for what remains outside what either round tested.
