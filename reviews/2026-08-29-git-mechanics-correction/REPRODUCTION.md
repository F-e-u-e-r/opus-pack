# #220/#225 Git-mechanics first-hand reproduction (READ-ONLY gate, 2026-08-29)

Baseline: main = 85d3629 · frozen heads: #220 = d55ceca (4 commits), #225 = d04e814 (6 commits; first 4 == #220's — lineage CONFIRMED commit-by-commit) · frozen diffs sha256: 220 = 9baa821e…, 225 = 3c27312b… · **git version 2.50.1 (Apple Git-155)** — all verdicts bound to this version; #225's own fixtures also cite 2.50.1. Throwaway fixtures only (scratchpad/gitfx); zero canonical bytes touched.

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

## Exact disposition map (current main 85d3629 → what changes)

**Branch bullet (residue-rule amendment landed by #218):**
1. "materialize only under `reset --hard`, re-applying the branch as a patch, or otherwise overwriting the base with the branch tip" → **REPLACE** (C8+C9: the precise set is reset-hard / deletion-aware sync / two-dot-diff-into-apply; plain copy and `format-patch|am` do NOT — "re-applying as a patch" is ambiguous and half-wrong)
2. "what a merge would actually change is the branch's own delta from the merge-base (`git diff $(git merge-base …) <branch>`)" → **REPLACE — factually wrong as a merge preview** (C13: misses relocation/conflict; C7: the real preview is `merge-tree --write-tree` with its 0/1/128 contract; C5/C6: the longhand equals three-dot but silently degrades to a working-tree diff on unrelated histories)
3. "what deleting the branch would lose is its unlanded work — the two-dot ADDITION side, or `git log <base>..<branch>`" → **REPLACE** (C10: addition side over-reports; C11/C12: the two complementary reads, non-equivalent, with the three-dot-log trap)
4. Branch-bullet marker → **SPLIT**: verified-mechanics phrasing for the materialization set, merge-tree preview, addition-side over-report, merge-base longhand (fixture-verified, git 2.50.1, now independently reproduced first-hand 2026-08-29); incident shape + squash/empty-two-dot stay `unprobed`

**Worktree bullet:**
5. "The usual teardown fails LOUDLY … die with 'not a git repository'" → **REPLACE** (C3: two distinct loud modes with different messages; the old sentence conflates them and misattributes the dead-cwd message)
6. "(`git worktree prune` itself only drops admin entries whose directory is already missing)" → **REPLACE — REFUTED by C1**; the corrected content adds lock-protection and the repair-before/after-prune exit semantics (C2)
7. "`git rev-parse --show-toplevel` is the decisive check" → **AMEND** (C4: decisive only when COMPARED against the expected path — it succeeds and prints the enclosing checkout) 
8. Worktree-bullet marker → **SPLIT** (prune/repair/toplevel/loud-modes = fixture-verified; incident shape stays `unprobed`)

**Provenance (the #218-landed paragraph):**
9. "materializes only under reset/re-apply/overwrite" inside the REFUTED-history recap → **AMEND** to the corrected materialization statement (as #225 does)
10. #225's new 12-result provenance paragraph → **LAND with one wording adjustment**: result 6's "both failed and the pointer stayed gone" → state that bare repair silently no-ops (exit 0) while the path form errors (exit 1), pointer stays gone — the only place my first-hand results diverge from #225's phrasing (mechanism identical, wording precision only)

**Marker upgrades owner asked about:** every mechanics claim listed CONFIRMED above is eligible for the fixture-verified framing (now doubly evidenced: contributor fixtures + this gate's independent first-hand reproduction on 2.50.1); the two incident shapes and the untested squash/empty-two-dot clauses must remain `unprobed`.

## STOP
Zero canonical bytes; no reviewers engaged; no PR. #225 remains the primary current source (KEEP-AS-LINEAGE for #220). Awaiting owner adjudication → owner-curated landing gate. #224 queued next.
