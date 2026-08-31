# Out-of-tree bytecode cache defeats the in-tree removal (op-rigor §2, path (a))

Amends ONE clearance path of the runtime-selected-artifact correspondence limb
landed by #230. Not a correction — the limb is sound, and its digest step already
catches the case below. The patch makes the *removal* half self-aware, because a
reviewer who performs it the conventional way can believe it succeeded when it
did nothing.

## What was probed

`harness/pycache_prefix_probe.py`, self-contained, prints its own verdict and
reports "not reproduced" on interpreters that do not set a cache prefix.
Captured run: `harness/result-macos-cltools-3.9.6.txt`.

Environment binding for that capture: macOS 26.6.2 arm64, `/usr/bin/python3` =
CPython 3.9.6 as shipped by Apple CommandLineTools.

1. That interpreter reports `sys.pycache_prefix` set to a per-user, path-mirrored
   cache root by default. Bytecode never lands in `__pycache__` beside the source.
   - `python3 -S -c` prints the same value, so it is not site configuration.
   - `python3 -E -S -c` prints `None`.
   - No `PYTHON*` variable exists in the parent shell or the child's `os.environ`,
     and a full env diff between the normal and `-E` child shows zero differing
     keys. **The mechanism was NOT established** — only the observed effect is
     claimed here.
2. End to end: compile an `UNCHECKED_HASH` `.pyc` for a module returning `OLD`,
   rewrite the source to return something of a different length, `rm -rf
   __pycache__`, confirm `find . -name '*.pyc'` returns nothing — and the import
   still prints `OLD`.

## Review

One round, one reviewer: codex `gpt-5.6-luna`, read-only, self-contained inlined
packet (`packets/packet-r1.md`), verdict `verdicts/r1-luna.md`. **FIX**, three
findings, all reproduced by derivation from the packet's own evidence and all
fixed. Single-lens: this did not get a second model family, which is a recorded
gap, not a claimed dual gate.

| Finding | Disposition |
|---|---|
| **High, over-claim.** "that digest confirmation is what makes an incomplete removal detectable" is not true of every incomplete removal — a byte-identical leftover leaves nothing to detect. | fixed; scoped to "for this failure mode" |
| **Medium, generalization.** "a central or path-mirrored cache directory, a per-user cache root" — the evidence establishes one cache that is both path-mirrored and per-user; "central" is unevidenced. | fixed; narrowed to "path-mirrored, or under a per-user cache root" |
| **Low, redundancy.** The rationale clause added no clearance condition the landed digest step lacked. | fixed by conversion, not deletion: the clause now carries an operational constraint (run the digest against the bytes the runtime actually selects, not against the tree's appearance) — which also closes the second mechanism named in the High finding |

Remedies were authored here, not pasted: the reviewer's proposed wording for the
Low finding deleted the clause outright, which would have dropped the
actually-selected-bytes constraint that the High finding's own mechanism argues
for.

An earlier draft named the vendor, the OS and a `~/Library/...` path inside the
rule text. That was removed before review as a portability violation; the machine
specifics live in this trail instead. The reviewer independently confirmed no
scope violation remained.

## What would change the conclusion

- An interpreter or runtime where the conventional in-tree removal is always
  sufficient would not falsify the "may" — but a demonstration that no mainstream
  runtime caches out of tree would make the clause dead weight.
- The capture is one interpreter on one OS. The probe is written to be run
  elsewhere; more captures would widen the evidence base.
