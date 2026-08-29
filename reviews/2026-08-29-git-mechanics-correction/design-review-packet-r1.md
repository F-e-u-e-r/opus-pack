# Review packet — operational-rigor Git-mechanics factual correction (exact diff)

You are one of two independent reviewers (mutually blind; you see only this packet). Review the EXACT DIFF below — a factual correction to two shipped `operational-rigor` §2 bullets whose empirical Git claims were refuted by fixture execution.

## What is settled — do NOT re-vote it
The Git mechanics themselves are SETTLED by first-hand execution: 14/14 claims CONFIRMED, 0 REFUTED, 0 VERSION-SENSITIVE, on git 2.50.1, independently reproducing a contributor's fixtures (the per-claim table is inlined below as your fidelity reference). Your job is NOT to re-adjudicate Git behavior by prose reasoning — it is to verify the LANDED WORDING is faithful to those results and the scope is clean, on the ten axes below.

## Source structure
Landed delta = contributor PR #225's current semantics (its own diff was frozen and hash-pinned) **plus exactly one owner-authored correction (MOD-C2c)**: #225's provenance said that after prune "both failed and the pointer stayed gone"; first-hand execution showed the bare repair invocation RETURNS SUCCESS (exit 0) while leaving the pointer unrecovered — a silent no-op, not a process-level failure. The landed wording states: the recovery path is gone even though the command need not fail loudly, and exit status alone cannot prove a repair succeeded — verify the recovered pointer/state. Machine-verified: the line-multiset delta vs #225 is exactly that region (5 lines replacing 1); zero other drift.

## Review scope — answer ALL ten explicitly
1. Is the landed wording faithful to the 14/14 fixture results (check each corrected claim against the table below)?
2. Does any sentence re-introduce falsified mechanics (the old prune premise; merge-base delta as a merge preview; the addition side as an authoritative branch-loss read; "not a git repository" for the dead-cwd case)?
3. Are the merge-preview / already-landed / delete-risk / materialization questions kept separate, each matched to the right command?
4. Is the commits-vs-net-content distinction stated as COMPLEMENTARY evidence, never substitutes (with the commit+revert divergence)?
5. Does the C2c wording avoid mislabeling the exit-0 no-op as a command failure, while still conveying that recovery is gone after prune?
6. Are marker upgrades limited to fixture-verified MECHANICS (dated, version-bound)?
7. Do the incident shapes and the squash/empty-two-dot clauses stay `unprobed` — and is guidance-EFFECTIVENESS (do agents avoid the failure) NOT claimed as verified anywhere?
8. Does the provenance honestly preserve the contributor→owner lineage including the falsified intermediates (nothing laundered into "was always right")?
9. Is anything smuggled in — in particular a "disposable worktree as checkpoint" prescription, or any other parked/queued candidate content?
10. Is the scope a single canonical skill file (plus its evidence package), with no collateral rewrite of other Git doctrine in this file beyond the two bullets and their provenance?

## Verdict format (mandatory)
Number findings, anchor each to a hunk/line, classify on an axis. Final line exactly one of:
`PROCEED` or `FIX <numbered list of blocking findings>`

## Fidelity reference — the first-hand reproduction table
## Per-claim verdicts — 14/14 CONFIRMED · 0 REFUTED · 0 VERSION-SENSITIVE (at 2.50.1)

| # | Claim (as #225 states it) | Verdict | First-hand observation |
|---|---|---|---|
| C1 | prune drops an UNLOCKED worktree's entry when only the `.git` pointer is missing, dir fully present; locked survives | **CONFIRMED** | `Removing worktrees/wt-unlocked: gitdir file points to non-existent location`; locked entry survived; both dirs on disk. **The old canonical sentence ("prune only drops entries whose directory is already missing") is REFUTED** |
| C2 | bare `worktree repair` (entry present) restores pointer, exit 0; `repair <path>` restores but exit 1 + `error:`; after prune neither restores | **CONFIRMED** (one wording nuance) | Exactly as claimed pre-prune. Post-prune: pointer stays gone — but bare repair is an **exit-0 silent no-op**, not a visible failure; #225's provenance "both failed" is loose for the bare form (its rule text "the exit works only until prune removes the entry" is accurate) |
| C3 | two distinct LOUD failures + the nested silent rebound | **CONFIRMED** | deleted-cwd → `fatal: Unable to read current working directory`; pointer-gone-outside → `fatal: not a git repository`; pointer-gone-NESTED → `git status` silently succeeds on the MAIN checkout |
| C4 | `--show-toplevel` succeeds (exit 0) printing the enclosing checkout — decisive only when COMPARED | **CONFIRMED** | exit 0, printed the main repo root in the rebind case |
| C5 | merge-base longhand == three-dot when a merge-base exists | **CONFIRMED** | `cmp` byte-identical |
| C6 | unrelated histories: `merge-base` exits 1 printing nothing → longhand silently becomes a WORKING-TREE diff; three-dot never does | **CONFIRMED** | longhand output included a deliberately-planted unstaged edit (working-tree semantics proven); three-dot → `fatal: main...U: no merge base` |
| C7 | `merge-tree --write-tree`: exit 0 clean (OID alone) / 1 conflicted (OID first line + info) / 128 unrelated | **CONFIRMED** | all three observed, incl. `refusing to merge unrelated histories` at 128 |
| C8 | materialization: `reset --hard` ✓, `rsync -a --delete` ✓, two-dot diff piped to `git apply` ✓; plain recursive copy ✗ | **CONFIRMED** | base-only file REMOVED under first three, present under `cp -R` |
| C9 | `format-patch --stdout mb..B \| git am` leaves base-only files alone; bare `format-patch` writes `*.patch` to cwd; bare `git am` reads stdin | **CONFIRMED** | base-only PRESENT + branch file arrived; `0001-b.patch` written; `git am </dev/null` returned silently (stdin consumed) |
| C10 | two-dot ADDITION side over-reports once the base has moved (carries the branch's older copy of base-side edits) | **CONFIRMED** | addition side = `+new` (genuine) **and** `+v1` (older copy of the base-advanced file) |
| C11 | `git log <base>..<branch>` = unique COMMITS; `git diff <base>...<branch>` = net CONTENT; commit+revert makes them diverge | **CONFIRMED** | log listed 3 branch commits (incl. the revert pair); three-dot diff = branch-new.txt only; revert-pair file: log non-empty, three-dot diff 0 lines |
| C12 | `git log <base>...<branch>` (three dots) is symmetric and lists base-side commits too | **CONFIRMED** | base-advance commit appeared |
| C13 | branch-side rename of an enclosing dir: merge-base-delta diff shows nothing; `merge-tree` shows OID + relocation CONFLICT, exit 1 | **CONFIRMED** | `main...R` diff: 0 mentions of the base-only file; merge-tree: OID + stage-2 entry + `CONFLICT (file location)…`, **true exit 1** (an earlier exit-0 reading was this session's own `\| head` pipeline contamination, re-tested clean) |
| C14 | force-push updates the ref, leaves the pushing tree untouched | **CONFIRMED** | tree listing + HEAD identical before/after `push --force` |

Not re-tested (out of the 14, per #225's own marker split): the squash and empty-two-dot claims and both incident SHAPES — #225 itself keeps these `unprobed`; nothing to reproduce.

## Per-hunk table (machine-generated, EXACT)
| hunk | header | declared old,new | counted old,new | match |
|---|---|---|---|---|
| 1 | `@@ -281,21 +281,68 @@` | 21,68 | 21,68 | EXACT |
| 2 | `@@ -308,9 +355,12 @@` | 9,12 | 9,12 | EXACT |
| 3 | `@@ -1424,11 +1474,64 @@` | 11,64 | 11,64 | EXACT |

## THE EXACT DIFF UNDER REVIEW
```diff
diff --git a/skills/operational-rigor/SKILL.md b/skills/operational-rigor/SKILL.md
index 63cd099..1072055 100644
--- a/skills/operational-rigor/SKILL.md
+++ b/skills/operational-rigor/SKILL.md
@@ -281,21 +281,68 @@ When rigor conflicts with finishing sooner, rigor wins.
   be READ — but never as a merge preview: a three-way merge applies the
   branch's changes from the MERGE-BASE, so base-side work the branch
   never touched survives the merge even though the two-dot shows it as
-  deletions (those deletions materialize only under `reset --hard`,
-  re-applying the branch as a patch, or otherwise overwriting the base
-  with the branch tip — which is why non-empty never justifies
-  re-applying). Match the read to the action: what a merge would
-  actually change is the branch's own delta from the merge-base
-  (`git diff $(git merge-base <base> <branch>) <branch>`); what
-  deleting the branch would lose is its unlanded work — the two-dot
-  ADDITION side, or `git log <base>..<branch>` (`unprobed` —
-  contributor incident as shape; see Provenance).
+  deletions. Survives is not untouched — a branch-side rename of an
+  enclosing directory still relocates such a file or conflicts on it.
+  Those deletions materialize under `git reset --hard <branch>`, a
+  DELETION-AWARE sync of the tip tree (`rsync --delete`; a plain
+  recursive copy leaves base-only files in place), or piping the two-dot
+  diff itself into `git apply` — which is why non-empty never justifies
+  re-applying. They do NOT materialize under
+  `git format-patch --stdout $(git merge-base <base> <branch>)..<branch>
+  | git am` onto the base, which replays the branch's own commits and
+  leaves base-only files alone (that pipeline is the runnable form:
+  bare `format-patch` writes `*.patch` into cwd and bare `git am` then
+  waits on stdin). Match the read to the action: a real merge preview is
+  `git merge-tree --write-tree <base> <branch>`. Read its EXIT STATUS
+  first — 0 clean, 1 conflicted, anything else an error whose output is
+  unspecified (it refuses unrelated histories outright). On 0 and 1 its
+  first stdout line is the OID of the merged tree, written either way,
+  with conflicted-file info following on 1. Diff that OID against the
+  base to read the merge's net change. `git diff
+  $(git merge-base <base> <branch>) <branch>` is the branch's
+  CONTRIBUTION,
+  not the merge result — where a merge-base exists it is the same
+  computation as the three-dot form rejected above, but only the
+  longhand degrades: on unrelated histories `git merge-base` prints
+  nothing, the substitution empties, and the command silently becomes a
+  working-tree diff, which `<base>...<branch>` never does. What deleting
+  the branch would lose is its unlanded work, and the two-dot ADDITION
+  side does not measure it: once the base has moved on, that side also
+  carries the branch's older copy of base-side edits, which deleting the
+  branch does not lose — inconclusive for the same tip-to-tip reason as
+  the deletion side. Use two COMPLEMENTARY reads instead, never as
+  equivalents: `git log <base>..<branch>` enumerates the branch's unique
+  COMMITS, and `git diff <base>...<branch>` shows its net CONTENT since
+  the merge-base. They diverge — a commit plus its revert leaves the log
+  non-empty and the three-dot diff empty. Mind the dots on the log: the
+  two-dot `<base>..<branch>` (or `^<base> <branch>`) is the one you
+  want; `git log <base>...<branch>` is the SYMMETRIC difference and
+  lists base-side commits too, recreating the very over-report this
+  paragraph exists to stop (the materialization set, the merge-tree
+  preview, the addition-side over-report and the merge-base longhand
+  were verified against
+  fixtures 2026-08-28; the squash and empty-two-dot claims above and the
+  incident shape stay `unprobed` — contributor incident; see
+  Provenance).
 - **A torn-down worktree can make git act on the ENCLOSING repo instead
-  of failing** (`unprobed` — contributor incident as shape; see
-  Provenance). The usual teardown fails LOUDLY: a removed linked
-  worktree is a dead cwd, sibling paths stop resolving, and commands
-  there die with "not a git repository" (`git worktree prune` itself
-  only drops admin entries whose directory is already missing). The
+  of failing** (prune, repair, and the `--show-toplevel` rebind case
+  verified against fixtures 2026-08-28; the incident shape stays
+  `unprobed` — contributor incident; see Provenance). Teardown normally
+  fails LOUDLY, in one of two ways: delete the worktree directory while
+  it is still your cwd and git dies with "Unable to read current working
+  directory" before it looks for a repository at all; delete only the
+  `.git` pointer somewhere OUTSIDE the main checkout and the walk-up
+  finds nothing, so it dies with "not a git repository". `git worktree
+  prune` does not
+  create the silent case below, but it does CLOSE the exit from it: it
+  drops the admin entry of any UNLOCKED worktree whose `.git` pointer
+  file is missing — its directory still fully present or not ("gitdir
+  file points to non-existent location"); `git worktree lock` is what
+  holds an entry through a prune. A bare `git worktree repair` run from
+  the main checkout rewrites the missing pointer from that admin entry,
+  so the exit works only until prune removes the entry; the
+  `repair <path>` form also restores it but exits 1 with an `error:`
+  line, so its status reads as a failure it is not. The
   silent case is narrower and worse: the worktree's `.git` pointer file
   is gone while its directory path still resolves INSIDE the main
   checkout's tree — git resolves its repository by walking up from cwd,
@@ -308,9 +355,12 @@ When rigor conflicts with finishing sooner, rigor wins.
   notice. So the trigger is positional, not observational: from any
   long-lived session working in a linked worktree that cleanup could
   have touched, before the first commit, push, or PR after a merge or
-  cleanup event, re-verify identity. `git rev-parse --show-toplevel` is
-  the decisive check — a rebound checkout can be sitting on the very
-  branch name you expect, so `--abbrev-ref HEAD` alone can false-pass.
+  cleanup event, re-verify identity. Decide it on `git rev-parse
+  --show-toplevel` COMPARED against the worktree path you expect: it
+  does not error in this failure, it succeeds and prints the enclosing
+  checkout, so reading it without comparing proves nothing. And a
+  rebound checkout can be sitting on the very branch name you expect,
+  so `--abbrev-ref HEAD` alone can false-pass.
   ❌ a create-PR command issued from a session's own already-torn-down
   worktree directory would have acted on the main checkout — wrong
   tree, wrong branch — under this session's name; the staged-diff read
@@ -1424,11 +1474,64 @@ shipped after the branch's base. The incident's original reading — "a
 late merge would have silently regressed them" — was REFUTED on
 2026-08-28 pre-merge review by execution (a three-way merge preserves
 base-side work the branch never touched; the two-dot deletion side
-materializes only under reset/re-apply/overwrite), which is why the
-amendment now reads the two-dot as a re-apply hazard and routes merge
-and delete decisions to the merge-base delta and the addition side
-respectively. Both bullets ship `unprobed` per the covenant; their
-probes join the standing #115 queue.
+materializes when the base checkout is overwritten by the tip or the
+two-dot diff is itself applied, not under `format-patch` + `am`), which
+is why the amendment now reads the two-dot as a re-apply hazard, routes
+the merge preview to `git merge-tree --write-tree`, and reads delete
+risk off `git log <base>..<branch>` plus `git diff <base>...<branch>` —
+treating the two-dot ADDITION side as inconclusive for the same
+tip-to-tip reason as its deletion side (result 11).
+
+Both bullets' GIT MECHANICS were probed on 2026-08-28 against throwaway
+fixtures (git 2.50.1), after a two-family prose review of the same text
+returned findings but ran nothing. Results, each corrected above:
+(1) `git worktree prune -v` removed the admin entry of an UNLOCKED
+worktree whose directory was fully populated and whose `.git` pointer
+file alone was deleted ("gitdir file points to non-existent location");
+a locked worktree in the same state survived. The old text said prune
+only drops entries whose directory is already missing. (2) `git diff
+$(git merge-base A B) B` was byte-identical (`cmp`) to `git diff A...B`;
+on unrelated histories `git merge-base` exited 1 printing nothing; and on
+a branch that renamed an enclosing directory the merge conflicted and
+relocated a base-only file, which that diff did not show and
+`git merge-tree --write-tree` did (merged-tree OID on the first stdout
+line, then the conflicted path and a CONFLICT message, exit 1; a clean
+pair printed the OID alone and exited 0). (3) `format-patch
+$(git merge-base A B)..B` + `am`
+onto the base left the base-only file in place. (4) A force-push updated
+the ref and left the pushing tree untouched, so it is not a materializing
+action. (5) `git rev-parse --show-toplevel` exited 0 printing the
+enclosing checkout in the rebind case. (6) With the pointer file deleted
+and the admin entry present, a bare `git worktree repair` from the main
+checkout restored the pointer and exited 0, and `repair <path>` restored
+it too but exited 1 with an `error:` line; after `prune` removed the
+administrative entry, the bare repair invocation returned success while
+leaving the pointer unrecovered and the path form errored — the recovery
+path is gone even though the command need not fail loudly, so exit
+status alone cannot prove a repair succeeded; verify the recovered
+pointer/state. (7) Of the overwrite
+actions, `git reset --hard <branch>` and `rsync -a --delete` of the tip
+tree each removed the base-only file, and piping `git diff <base>
+<branch>` into `git apply` did too, but a plain `cp -R` of the tip tree
+left it in place — so only a deletion-aware overwrite materializes.
+(8) Deleting a linked worktree directory while it was the cwd produced
+"fatal: Unable to read current working directory", not "not a git
+repository". (9) `format-patch --stdout ... | git am` is the runnable
+form; bare `format-patch` wrote `0001-*.patch` into cwd and bare
+`git am` read stdin. (10) `merge-tree --write-tree` on unrelated
+histories exited 128 ("refusing to merge unrelated histories"), outside
+its documented 0/1. Probed 2026-08-29: (11) with the base moved on (a
+base-side edit the branch predates), the two-dot ADDITION side carried
+the branch's older copy of that file alongside its genuine new work,
+while `git log <base>..<branch>` contained only the branch's unique
+commit and `git diff <base>...<branch>` only its net new content — so
+the addition side over-reports what deleting the branch loses, by the
+same mechanism that makes the deletion side inconclusive. The two reads
+are not equivalent: a commit plus its revert left the log listing two
+commits and the three-dot diff empty. (12) `git log <base>...<branch>`
+(three dots) listed the BASE-side commit as well.
+The incident SHAPE of both bullets remains contributor-reported
+and ships `unprobed`; those probes stay on the standing #115 queue.
 
 Stable behavioral rules; the environment-specific facts to re-verify now travel
 with the rules that cite them — the external-systems set in
```
