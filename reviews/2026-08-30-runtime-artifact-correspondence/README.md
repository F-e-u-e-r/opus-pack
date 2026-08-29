# ⑤ Runtime-selected-artifact correspondence — evidence package (2026-08-30)

Full audit trail for the operational-rigor §2 correspondence limb and its
skill-vetting §1 step-4 pointer. Branch `runtime-artifact-correspondence` from main
`5c90086`.

## What the change does

A source reviewer clears source *text*, but a runtime may execute a shipped or
out-of-tree compiled / cached / bundled artifact whose bytes were never produced
from that source — so a clean source review can clear content the interpreter never
runs. The pack already carried the binding *principle* (security-architect: "what
executes must be verifiably bound to what was reviewed") and already failed closed
on opaque dependencies; what was missing was the **recognition trigger at the
reviewer's own working point**. The limb adds it as the single canonical statement
(operational-rigor §2); skill-vetting §1 gets a bare routing pointer (new step 4).

Classification: **PARTIAL-GAP**. Abstraction: **L2** (reviewed-source ↔
runtime-selected executable-artifact correspondence) — not `.pyc`-specific L1, not
all-supply-chain L3.

## Contents

- `orientation-summary.md` — the PARTIAL-GAP orientation (P1–P8).
- `harness/` — the first-hand mechanism battery (D1–D11) and results: `run_case.py`
  + `drive.py` (D1–D10), `d11_probe.py` (hash-policy), `results.json`,
  `d11_result.json`. **Evidence, not production enforcement** — deliberately not
  wired into CI (`.github/checks.py` does not run it).
- `packets/packet-r{1,2,3}.md` — the self-contained review packets, one per round.
- `verdicts/r{1,2,3}-{luna,sol}.md` — the six reviewer verdicts.
- `gate-trail.md` — per-round finding dispositions.
- `self-review-notes.md` — the author's pre-reviewer adversarial read.
- `final-wording.md` — the R3-final canonical blocks as landed + the marker note.
- `landing-manifest.md` — declared adaptations and the faithful-reconstruction battery.
- `MANIFEST.sha256` — hashes of every file in this package.

## Key first-hand results (CPython 3.9.6, cache_tag cpython-39)

- **D2 (forged CHECKED_HASH):** a hash-based `.pyc` whose header source-hash matched
  a clean decoy while its body was an unrelated payload passed the runtime's own
  freshness validation *and executed the payload* — a checked hash binds
  header↔current-source, never bytecode↔source.
- **D11 (hash policy):** `--check-hash-based-pycs` `default`/`always`/`never`
  controls whether the source-hash is compared at all (an `UNCHECKED_HASH` header is
  not compared under the default policy; a `CHECKED_HASH` comparison can be
  disabled) — cache metadata is at most a freshness signal.
- A stable tree digest proves identity, not correspondence; a reviewed-source ↔
  runtime-artifact divergence is an actually-executable failure shape.

**Mechanism = first-hand verified. The rule's behavioral effectiveness = unprobed →
one marker → standing #115.** These are separate: the marker does not mean the
mechanism is unverified.

## Review

Dual-blind **two-variant** review (`gpt-5.6-luna` + `gpt-5.6-sol`, both at max
effort) — two variants of one GPT-5.6 family, both outside the author family;
**NOT a cross-family gate** (grok was unavailable this window; family-diversity
caveat retained). R1 both FIX → R2 one PROCEED / one FIX → R3 PROCEED × 2.
