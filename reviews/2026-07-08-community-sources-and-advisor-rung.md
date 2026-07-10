# 2026-07-08 — Community-source evaluation + advisor-rung change review

## Context

Owner supplied 8 sources (official advisor-tool docs + 7 community repos) and asked
whether the pack needs new skills or enhancements. Constraint supplied mid-review:
Fable 5 subscription access ends **2026-07-12 PT** — after that, subscription plans
top out at Opus 4.8, so any stronger-tier rule must be conditional, not assumed.

## Source verdicts

| Source | Verdict |
|---|---|
| Anthropic advisor tool docs (beta `advisor-tool-2026-03-01`) | Pattern adopted (idea only) — validates "stronger tier recommends, current tier executes" |
| echo-of-machines/fable-advisor (17★) | Adopted tier-relative into delegation-and-review §4 rung 3 |
| TheColliny/FableClaudeMDForOpus (166★) | One rule adopted: state-phrased triggers → skill-authoring §5; always-loaded playbook architecture not adopted (same reasoning as dropped-item 5) |
| mrtooher/fable-mode (701★) | Skipped — staged execution + per-stage failable checks already covered by operational-rigor §2/§4/§5 + ground-truth-gates |
| duolahypercho/fusion-fable (443★) | Skipped — same-model panel = §4 high-stakes panel rule; external-model phase stays deliberately dropped (item 3) |
| baskduf/FableCodex (414★) | Skipped — goal ledger / findings gate covered by task contract + files-are-state + honest completion; **AGPL-3.0: never take code** |
| Miguok/fable-harness (164★) | Skipped — already upstream of verify-before-stop hook (via curtischoutw); two-critic + lens-diversity covers the three-persona panel |
| Anil-matcha/awesome-claude-fable-5 (320★) | Skipped — use-case catalog, not a method source |

## Changes landed (alpha-0.1.2 working tree)

1. `skills/delegation-and-review/SKILL.md` §4 rung 3 — conditional advice-mode
   consult at a stronger tier (tier-relative, self-skips when the session already
   runs the top tier; recommendation comes back, current tier remains executor).
   Provenance note extended.
2. `skills/skill-authoring/SKILL.md` §5 — "states fire; labels drift" trigger rule.
   Provenance note extended.
3. `README.md` + `README.zh-TW.md` — dropped-item 4 narrowed (not reversed: "top
   rung hangs in air" stays true for top-tier-driven sessions); two acknowledgement
   entries added (ideas only, no code).
4. All three skill copies synced (`skills/`, `.claude/skills/`, `~/.claude/skills/`),
   `diff -rq` clean.

## Independent review trail (owner-directed: two reviewers)

- **GPT-5.5 @ xhigh via codex exec (read-only sandbox), full packet** — 1 should-fix:
  README parenthetical "it self-skips otherwise / 否則此級自動跳過" readable as
  skipping the whole retry rung. Counterexample valid. **Fixed** in both languages
  ("otherwise the retry stays plain same-tier" / 「否則維持同階重試」). All other
  lenses pass; links verified live.
- **Opus 4.8 @ max effort, pass 1** — packet failed to reach the agent (workflow
  args bug; prompt arrived as `undefined`); agent recovered the diff itself and
  verified citations (WebSearch), section refs, en/zh mirror, internal consistency —
  clean, but treated as degraded coverage.
- **Opus 4.8 @ max effort, pass 2 (final state, packet via file)** — contract items
  1–5 all satisfied; reword confirmed to resolve the ambiguity in both languages
  with no en/zh drift; advisor tool + both repos verified against live sources.
  **No blockers, no should-fixes.**

## Logged, not fixed (reviewer-judged not worth an edit)

- nit: `README.md` item 4 reflow puts `patterns get "downgraded"` on its own line
  (renders fine; rejoin next time the file is touched).
- nit: `delegation-and-review/SKILL.md` rung 3 pronoun "make it advice-mode" — the
  colon-list disambiguates; if ever revised, "make that fresh context advice-mode".
- watch-point: README item 4 ↔ SKILL §4 rung 3 have no written sync contract
  (judged rationale-vs-rule, not a §3 violation) — a future rung edit should touch
  item 4 too.
