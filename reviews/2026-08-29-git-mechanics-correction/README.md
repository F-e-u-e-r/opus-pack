# Git-mechanics factual correction — landing record (#220/#225 family)

**What landed:** the shipped `operational-rigor` §2 branch-read and worktree bullets corrected to first-hand-verified Git mechanics. This was a live shipped-correctness-defect interrupt, not a routine doctrine addition: the previously landed wording contained empirical Git claims that fixture execution refuted.

## Source lineage (preserved, nothing laundered)

`#220 @ d55ceca` (4 commits; fixture-driven corrections: prune premise, merge preview, format-patch/am, materialization set) → `#225 @ d04e814` (same 4 commits + 2: the two-dot ADDITION side over-reports; `git log <base>..<branch>` and `git diff <base>...<branch>` are complementary, never interchangeable) → **owner-gate first-hand reproduction, 14/14 CONFIRMED / 0 REFUTED / 0 VERSION-SENSITIVE (git 2.50.1)** — see `REPRODUCTION.md` for the per-claim table and the exact disposition map. Both contributor PRs are never merged; #225 is the primary current semantic source, #220 is lineage. The contributor's own review rounds included findings whose remedies were wrong and a review packet that truncated results (8)–(10) — which is why contributor review could not serve as the final canonical gate and first-hand execution was required.

## The corrections (all fixture-proven before landing)

- **Prune premise (REFUTED old sentence):** `git worktree prune` drops an UNLOCKED worktree's admin entry whenever its `.git` pointer file is missing — directory fully present or not; a locked worktree survives. The old "only drops entries whose directory is already missing" was false.
- **Teardown failure shapes separated:** deleted-cwd dies with "Unable to read current working directory"; pointer-gone-outside dies with "not a git repository"; the silent rebind needs pointer-gone + path nested inside the main checkout.
- **Repair semantics + C2c owner correction:** bare `worktree repair` (entry present) restores the pointer at exit 0; `repair <path>` restores but exits 1 with an `error:` line; after prune removes the administrative entry, the bare invocation returns success while leaving the pointer unrecovered — the recovery path is gone even though the command need not fail loudly, so **exit status alone cannot prove a repair succeeded; verify the recovered pointer/state** (the sole owner-authored wording correction to #225's text).
- **`--show-toplevel` decides only when COMPARED** against the expected root — it succeeds and prints the enclosing checkout in the rebind case.
- **Merge preview = `git merge-tree --write-tree`** (exit 0 clean / 1 conflicted with OID first line + conflict info / 128 unrelated). The merge-base longhand is the branch's CONTRIBUTION, byte-identical to the three-dot form where a merge-base exists — and only the longhand silently degrades to a working-tree diff on unrelated histories.
- **Materialization set:** `reset --hard`, a deletion-aware sync (`rsync --delete`), or piping the two-dot diff into `git apply` materialize the deletions; a plain recursive copy and `format-patch --stdout … | git am` do not; a force-push is not a working-tree materializer.
- **Branch-loss reads:** the two-dot ADDITION side over-reports once the base has moved (it carries the branch's older copies of base-side edits). Use two COMPLEMENTARY reads — `git log <base>..<branch>` for unique COMMITS and `git diff <base>...<branch>` for net CONTENT — **commit identity and net content are complementary evidence, not substitutes** (a commit plus its revert leaves the log non-empty and the three-dot diff empty). `git log <base>...<branch>` is the symmetric-difference trap.

## Marker adjudication — mechanical truth verified ≠ guidance effectiveness verified

The mechanics claims above carry two independent evidence layers (contributor throwaway fixtures + this gate's first-hand reproduction) and are marked **fixture-verified (git 2.50.1)** in the landed text. What stays **`unprobed`**: both incident SHAPES (contributor-reported, not reconstructible), the squash and empty-two-dot clauses (not exercised by the 14), and — explicitly — **whether agents actually avoid these failures under the corrected guidance**: behavioral transmission/effectiveness was not probed and no mechanics fixture can substitute for that; those probes stay on the standing #115 queue.

## Review

Dual-blind exact-diff gate (Luna Max + Sol Max, mutually blind, isolated dirs, identity from tool banners), deliberately NARROW: reviewers verify fidelity to the 14/14 fixture results and scope discipline — they do not re-vote Git mechanics by prose opinion, which first-hand execution already settled.

- **r1:** both reviewers independently converged on ONE identical blocking finding — a chronology inconsistency inherited from #225 itself (its rule-text marker dated the addition-side over-report 2026-08-28 while its provenance placed results (11)–(12) under 2026-08-29, and its provenance opening over-assigned all mechanics to 08-28; the second source commit had not re-synced the date clause). Reproduced first-hand, then **MOD-DATE** authored: rule-text marker now splits 08-28/08-29 by result, provenance opens "results (1)–(10) on 2026-08-28, results (11)–(12) on 2026-08-29".
- **r2 (regenerated full diff): luna max — PROCEED · sol max — PROCEED. 2/2**, all ten axes line-anchored by both, date consistency explicitly re-verified.

Packets and all four verdicts are in this package.
