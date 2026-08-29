# My own adversarial read of the proposed wording (pre-reviewer baseline)

Formed BEFORE reading luna/sol R1 verdicts, so convergence is meaningful and I
have my own reproduction of each candidate defect. Merge with reviewer findings at
triage; a reviewer point I already hold here = first-hand reproduced.

## Candidate wording weaknesses I can already see

- **W1 (4a density).** The op-rigor bullet is one long sentence-chain. A weaker
  executing model may lose the (a)/(b)/(c) clearers or the freshness caveat.
  Severity: readability, not correctness. Watch for a reviewer flag; a split into
  "gate / clearers / what-does-not-clear" sub-structure may help without changing
  meaning.

- **W2 (clearance path (c) scope).** "review the runtime-selected artifact itself
  as the executable truth" is realistic for a readable generated bundle, but
  infeasible for raw bytecode/minified blobs. It is one option among three, used
  when applicable — but the wording could be misread as "you may always just eyeball
  the .pyc". Consider "when it is itself reviewable as source-equivalent".

- **W3 (sv renumber sweep — IMPLEMENTATION, not wording).** Inserting a numbered
  step 4 renumbers old 4/5/6 → 5/6/7. skill-vetting §1 step 2 references the
  closing digest as "the one at step 6"; other cross-refs to step numbers exist.
  A real call-site sweep (op-rigor §3) is owed when the edit lands — NOT now
  (owner STOP before implementation). Note only. An alternative that dodges the
  sweep: place the pointer as an unnumbered limb on step 3 rather than a new
  numbered step. Design question worth a reviewer's eye (axis 10 authority /
  cleanliness).

- **W4 (axis 8 orthogonality not explicit in text).** D10 proves ⑤⟂② mechanically,
  but the *wording* does not say "distinct from the activation-gated-payload
  check". If a reviewer worries the two collapse, a half-clause may be warranted —
  but adding it risks over-coupling. Lean: leave out unless a reviewer reproduces
  a real collapse; the altitude note in Design intent already separates them.

- **W5 ("penalized" / "finding" register).** "a source-only candidate with no such
  artifact is not penalized" — is "penalized" the right register for a review gate?
  The pack uses "finding" / "fail closed". "not penalized" is slightly loose;
  "is not a finding on this ground" is tighter. Minor.

- **W6 (does 4a over-reach beyond third-party?).** The bullet attaches to the
  third-party install gate, but the correspondence principle is general. Scoped to
  third-party candidates it is correct and minimal (L2, not L3). Confirm the
  wording does not accidentally read as "audit every artifact in your own repo on
  every task" — it should bind only the vetting/install context. Current phrasing
  ("clears executable behavior") is act-scoped to a review, so OK, but watch a
  reviewer reading it as universal.

## Axes I judge already-satisfied by the current wording (my read)

- Axis 1 (trigger not restatement): YES — imperative "clear only when…", names the
  reviewer act; cross-ref is a pointer, not a paraphrase.
- Axis 2 (selection vs review separated): YES — "runtime-selected bytes" vs
  "full-source read … clears source text".
- Axis 3 (digest = identity): YES — explicit.
- Axis 4 (freshness ≠ provenance): YES — explicit, names hash-header + timestamp,
  matches D2/D3.
- Axis 5 (local rebuild verifies selection): YES — "(a) … confirm the runtime
  selects the regenerate".
- Axis 6 (exact artifact binding): YES — "(b) bind the exact artifact bytes by
  digest".
- Axis 7 (no false positive on source-only): YES — D6 + the not-penalized clause
  (see W5 register nit).
- Axis 9 (L2 not L3): YES — examples are compiled/bundled/generated/cache, not
  data/config; the §2 Abstraction section states the boundary.

Net: no correctness defect I can reproduce yet; W1/W2/W5 are wording-polish
candidates, W3 is a deferred implementation sweep, W4/W6 are watch-items.
