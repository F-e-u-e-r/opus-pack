# Out-of-tree bytecode cache defeats the in-tree removal (op-rigor §2, path (a))

Amends ONE clearance path of the runtime-selected-artifact correspondence limb
landed by #230. Not a correction — the limb is sound, and its digest step already
catches the case below. The patch makes the *removal* half self-aware, because a
reviewer who performs it the conventional way can believe it succeeded when it
did nothing.

## What was probed

`harness/pycache_prefix_probe.py`, self-contained, prints its own verdict.
Captured run: `harness/result-macos-cltools-3.9.6.txt`. The environment claims
below are backed by `harness/env-probes-macos-cltools-3.9.6.txt`, captured on the
same interpreter — no claim here rests on an investigation that is not checked in.

Environment binding for those captures: macOS 26.6.2 arm64. `command -v python3`
is `/usr/bin/python3`; that interpreter reports `sys.executable` as
`/Library/Developer/CommandLineTools/usr/bin/python3`, CPython 3.9.6.

**Two conditions must both hold for stale bytes to execute**, and the probe now
reports them separately:

1. the cached artifact lives OUTSIDE the source tree, so deleting the in-tree
   cache directory does not remove it; and
2. that artifact is still runtime-ELIGIBLE despite the changed source.

Out-of-tree placement alone is NOT sufficient — a timestamp-validated artifact is
rejected once the source changes. The probe forces condition 2 with
`UNCHECKED_HASH`; in the wild an unchanged source or a forged header does the
same. Naming only condition 1 was an over-claim in the first round of this PR.

What the captures show: that interpreter reports `sys.pycache_prefix` set to a
per-user, path-mirrored cache root by default (`-S` prints the same value, so it
is not site configuration; `-E -S` prints `None`; no `PYTHON*` variable exists in
the child's `os.environ`, and a full env diff between the normal and `-E` child
shows zero differing keys). **The mechanism was NOT established** — only the
observed effect is claimed. End to end: compile an `UNCHECKED_HASH` `.pyc` for a
module returning `OLD`, rewrite the source, `rm -rf __pycache__`, and the import
still returns `OLD` — with the module's own `__cached__` naming the surviving
out-of-tree artifact as the one the runtime selected.

## Review

Two rounds, both codex, both read-only with a self-contained inlined packet.
Round 1 `gpt-5.6-luna` (`packets/packet-r1.md`, `verdicts/r1-luna.md`): FIX, 3
findings. Round 2 `gpt-5.6-sol` reviewing the shipped PR
(`packets/packet-r2.md`, `verdicts/r2-sol.md`): FIX, 5 findings. Every finding in
both rounds was reproduced by derivation or execution before being acted on.

**These are two variants of one model family, not a cross-family gate.** No second
family reviewed this. Recorded as a gap, not papered over.

### Round 1 (luna)

| Finding | Disposition |
|---|---|
| High — "the digest confirmation is what makes an incomplete removal detectable" over-claims | fixed by scoping to "for this failure mode" — **and that fix was insufficient; see round 2** |
| Medium — "a central or path-mirrored cache directory" generalizes past the evidence | fixed; narrowed |
| Low — the rationale clause added no clearance condition | converted rather than deleted, into the actually-selected-bytes constraint |

### Round 2 (sol)

| Finding | Disposition |
|---|---|
| High — the harness never measured the artifact's location; "ran from an out-of-tree cache" was INFERRED from "OLD printed and no in-tree `.pyc`" | fixed: the probe now captures the path `py_compile` returns, checks it survived the clean, reads back the imported module's `__cached__`, and requires that to resolve to the compiled artifact; child return codes are checked |
| High — `UNCHECKED_HASH` is a necessary, unreported co-cause; out-of-tree placement alone does not make stale bytes run | fixed in the rule text, the probe's docstring and its verdict line. This one is right and it is the more useful half of the finding |
| Medium — scoping to "this failure mode" did NOT repair round 1's over-claim: a leftover that regeneration overwrites, or one byte-identical to the regenerated artifact, leaves the digest matching while the removal failed | fixed: the text now says the confirmation detects a REMAINING mismatch and does not prove the removal worked |
| Medium — the trail asserted `-S` / `-E -S` / env-diff results and a `/usr/bin/python3` identity with no evidence checked in | fixed: `harness/env-probes-*.txt` added; both paths now recorded separately rather than asserted equal |
| Low — `sys.pycache_prefix` accessed unconditionally (AttributeError before 3.8); C4's wording is broader than what holds | fixed: `getattr(sys, 'pycache_prefix', None)`, and the PR body's claim narrowed |

Also raised and **rejected with reason**: that the PR body's "remedies were
authored here, not pasted" is unverifiable and should be removed. It is
evidenced — the round-1 verdict is checked in and its proposed wording differs
from what shipped — so the claim stays and now points at the trail.

Remedies were authored here in both rounds, not pasted. Round 1's reviewer would
have deleted the clause that round 2 relies on; round 2's proposed verdict string
was rewritten to name both conditions in the probe's own measured terms.

An earlier draft named the vendor, the OS and a `~/Library/...` path inside the
rule text. That was removed before review as a portability violation; the machine
specifics live in this trail instead. Both reviewers independently confirmed no
scope violation remained in the rule text.

## What would change the conclusion

- A demonstration that no mainstream runtime caches out of tree would make the
  clause dead weight. The modal "may" is what the evidence supports.
- One interpreter, one OS. The probe is written to run elsewhere and reports
  "not reproduced" on an interpreter that caches in-tree — but that branch has
  NOT been exercised on a real in-tree interpreter here, only derived from the
  code. No such interpreter was available on this machine.
