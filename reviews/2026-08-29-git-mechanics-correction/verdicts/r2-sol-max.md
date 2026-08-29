1. **Axis 1 — Fidelity: PASS.** H1–H3 faithfully cover C1–C14: prune/lock and repair behavior; loud and silent worktree failures; compared `--show-toplevel`; merge-base equivalence and unrelated-history degradation; merge-tree statuses; materializing actions; `format-patch`/`am`; addition-side over-report; complementary commit/content reads; symmetric log; rename conflict; and force-push non-materialization.

2. **Axis 2 — Falsified mechanics: PASS.** H1 explicitly says the merge-base delta is “CONTRIBUTION, not the merge result,” rejects the addition side as a loss measure, corrects prune behavior, and distinguishes dead-cwd’s “Unable to read current working directory” from the outside-pointer “not a git repository” case.

3. **Axis 3 — Question separation: PASS.** In H1, the limited two-dot already-landed/re-apply read remains non-dispositive; materialization is tied to reset/deletion-aware sync/apply; merge preview goes through `merge-tree --write-tree`; and delete risk uses complementary `log <base>..<branch>` plus `diff <base>...<branch>` reads.

4. **Axis 4 — Commits versus content: PASS.** H1 says “COMPLEMENTARY reads … never as equivalents” and includes the commit-plus-revert divergence. H3 result (11) preserves the same distinction.

5. **Axis 5 — C2c: PASS.** H3 result (6) accurately records that post-prune bare repair returns success while leaving the pointer unrecovered. It calls this a lost recovery path and requires state verification, without misclassifying the exit-0 invocation as a command failure.

6. **Axis 6 — Verification markers and dates: PASS.** H1 assigns the materialization, merge-tree, and longhand fixtures to 2026-08-28 and the addition-side/complementary-read fixtures to 2026-08-29. H3 consistently assigns results (1)–(10) to 08-28 and (11)–(12) to 08-29, bounded to Git 2.50.1.

7. **Axis 7 — Unprobed scope: PASS.** H1 explicitly leaves squash, empty-two-dot, and both incident shapes `unprobed`; H3 repeats the incident-shape status. Verification is claimed only for Git mechanics, never for guidance effectiveness.

8. **Axis 8 — Provenance: PASS.** H3 retains the contributor incident, the refuted merge-regression reading, the old false prune premise, the prose-only intermediate review, and the later execution corrections. Nothing is presented as having been correct all along.

9. **Axis 9 — No smuggled content: PASS.** No disposable-worktree checkpoint prescription or parked candidate appears. “Throwaway fixtures” in H3 describes the evidence method, not operational guidance.

10. **Axis 10 — Scope: PASS.** The diff touches only `skills/operational-rigor/SKILL.md`: the two canonical §2 bullet regions (H1–H2) and their provenance (H3). No collateral Git doctrine is rewritten.

PROCEED
