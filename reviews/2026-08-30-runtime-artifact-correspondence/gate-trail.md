# Dual-blind design gate — trail

Reviewers: `gpt-5.6-luna` @ max + `gpt-5.6-sol` @ max (codex exec, isolated cwd
per reviewer). Identity confirmed from exec banner, not self-report. Author family
= Claude/Fable (both reviewers outside it). Family-diversity caveat: luna/sol are
two gpt-5.6 variants (owner's grok-absent lineup; sol = designated diversity lens),
not two distinct families — recorded honestly, per owner's explicit named pair.

## Round 1 (packet.md) — both FIX

Independence: both flagged the two core issues but with distinct phrasing/examples
and each a distinct third point → genuine independent review, isolation held.

| # | Finding | Raised by | Reproduced (first-hand) | Disposition |
|---|---|---|---|---|
| A | "proves up-to-dateness" overstates cache metadata | luna + sol | YES — my own D1 (UNCHECKED header not consulted), D4 (timestamp forgeable), D2 (CHECKED validates header only) | **must-fix, FIXED** — reframed to a freshness *signal*; unchecked-not-consulted, timestamp-forgeable, checked-header-only spelled out (§4a) |
| B | "shipped"-only discovery scope misses out-of-tree / installed / central-cache artifacts | luna + sol | YES — my own orientation out-of-tree central-cache observation; the exact same-shape bypass (grep candidate tree → clear → runtime loads poisoned external-cache pyc) | **must-fix, FIXED** — scope broadened to every executable artifact the runtime may select (in-tree/installed/external-cache/load-path), data/config excluded to hold L2 (§4a opening, §4b) |
| C | local-regeneration under-specified: name recipe/toolchain, remove competing artifacts, verify runtime-selected bytes by exact digest (not just recompile/behavior) | luna only (sol explicitly cleared (a) as adequate, did not object to tightening) | YES — minor under-spec: my (a) "confirm the runtime selects the regenerate" looser than my own D7 digest-match and inconsistent with (b)'s digest language | **fixed (minimal tightening)** — (a) now names toolchain/recipe, removes competing artifacts, verifies runtime-selected bytes match regenerate by digest (§4a) |
| ed | "the regenerated artifact" clearer than "the regenerate" | sol (editorial) | n/a | adopted |

Also folded (my own pre-reviewer self-review, aligned with reviewer direction):
W2 clearance-(c) "when reviewable as source-equivalent"; W5 register "not a finding
on this ground" instead of "not penalized".

Deferred to implementation (NOT a wording defect; owner STOP before implementation):
W3 — inserting sv step 4 renumbers 4/5/6→5/6/7; a call-site sweep of intra-file
step-number references (e.g. §1 step 2's "the one at step 6") is owed when the edit
lands, per op-rigor §3. Noted, not actioned now.

Remedies were NOT pasted — each fix authored minimally against the whole wording.
No thrash (all additive tightenings both reviewers should accept). → Round 2.

## Round 2 (packet_r2.md) — luna PROCEED, sol FIX (one precision item)

luna: **PROCEED** — all three R1 issues confirmed resolved; satisfies all 10 axes;
no must-fix defects.

sol: **FIX** — one new precision defect (luna did not raise it):

| # | Finding | Reproduced (first-hand) | Disposition |
|---|---|---|---|
| E | The freshness sentence's CPython hash-policy claim is imprecise: an `UNCHECKED_HASH` header IS read/classified — under the *default* policy its stored source-hash is not *compared* to the source (not "not consulted"); `--check-hash-based-pycs always` forces that comparison even for UNCHECKED; `never` disables it even for CHECKED | **YES — D11 probe, ALL_MATCH_PREDICTION=true** (gate/d11_result.json): unchecked-mismatch@default→PAYLOAD (not compared), @always→DECOY (compared→recompile), checked-mismatch@default→DECOY, @never→PAYLOAD (comparison disabled). Note: first D11 run had a flag-syntax bug (`=` form → usage error rc2, INVALID not evidence); re-run with space-separated form matched all four predictions | **must-fix, FIXED** — reframed to policy-accurate wording: timestamp forgeable; UNCHECKED source-hash not compared under default; a matching CHECKED binds header↔current-source, never bytecode↔source; and whether the comparison runs is itself a runtime policy. D1 table gloss corrected the same way. sol's security conclusion ("correct") preserved. Authored minimally, not pasted |

luna's PROCEED was on the pre-E wording → both reviewers re-see the corrected
wording at R3 (the ≤3 cap). → Round 3.

## Round 3 (packet_r3.md) — BOTH PROCEED — GATE CLOSED

Both confirmed verdicts (non-empty body, identity from exec banner, final line
`PROCEED`); distinct emphasis (luna terse, sol enumerated all ten axes) → isolation
held.

- **luna @ max: PROCEED** — E resolved; adds the trigger, separates review from
  selection, L2 preserved, digests/freshness handled correctly, digest-backed
  regeneration/provenance required, source-only + directly-reviewed clearable,
  activation orthogonal, §4b routes without duplicating. No must-fix remains.
- **sol @ max: PROCEED** — all three R1 concerns + the R2 precision item resolved;
  fresh pass, all ten rubric axes pass; no internal contradiction, no same-shape
  bypass, no source-only failure.

**Gate outcome: clean dual-PROCEED at Round 3 (R1 both FIX → R2 luna PROCEED / sol
FIX → R3 both PROCEED).** Final wording = packet_r3.md §4a (op-rigor limb) + §4b
(skill-vetting pointer).

Caveat (honest, per cross-model-review §5): luna + sol are two gpt-5.6 variants
(owner's grok-absent lineup; sol = designated diversity lens), NOT two distinct
families — both outside the author family (Claude), owner's explicitly named pair.

STOP per owner ruling: gate closing does NOT authorize marker ruling, repo bytes,
or implementation — even on a clean 2/2. Hand back to owner for marker adjudication.
Deferred to implementation (if authorized later): W3 sv step-renumber call-site
sweep.
