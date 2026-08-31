BLUF: **FIX.** [verified: control-flow and textual derivation] The rule contains one false diagnostic claim, and the harness proves only a conjunction of out-of-tree placement plus unchecked-hash acceptance—not the broader causal story stated in its verdict and C2.

## Findings

### High — Harness verdict claims an artifact location it never measures

**LOCATION:** `VERDICT: REPRODUCED (stale bytes ran from an out-of-tree cache)`

**MECHANISM:** [verified: walked script control flow] The verdict depends only on `got == "OLD"` and finding no `.pyc` beneath the temporary source tree. The script never:

- records the path returned by `py_compile.compile`;
- confirms that artifact exists outside the tree;
- records `m.__cached__`, `m.__file__`, or its loader in the child;
- confirms the child selected the compiled artifact;
- checks the subprocess return code or stderr.

Consequently, “OLD was printed while no in-tree `.pyc` was found” is measured, but “those stale bytes ran from the out-of-tree cache” is inferred rather than demonstrated. [verified: script inspection]

**CONCRETE FIX:** Capture the path returned by `py_compile.compile`, assert it is outside `d` and exists, and have the child print both `m.v()` and `m.__cached__`; require the reported cache path to resolve to the compiled path. Also require `returncode == 0` before issuing `REPRODUCED`.

### High — `UNCHECKED_HASH` is a necessary unreported co-cause

**LOCATION:** `invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH`; C2: “a runtime may cache out of tree, so deleting … can … still execute stale bytes”

**MECHANISM:** [verified: Python invalidation semantics and script control flow] Out-of-tree placement explains why deleting `__pycache__` fails to remove the artifact. It does not by itself explain why changed source is ignored. The script deliberately makes the artifact acceptable regardless of the rewritten source by using `UNCHECKED_HASH`. Thus it demonstrates:

`out-of-tree artifact survives removal` **and** `unchecked artifact remains eligible` → stale result.

It does not demonstrate the broader causal implication that out-of-tree caching alone makes stale bytes execute. [verified: the source is changed before import, while unchecked-hash mode suppresses source validation]

**CONCRETE FIX:** Qualify both rule text and C2: “can leave a stale artifact in place and, where that artifact remains runtime-eligible, allow stale bytes to execute.” Change the verdict to name both conditions, such as: `REPRODUCED (out-of-tree UNCHECKED_HASH artifact survived the in-tree removal and was selected)`.

### Medium — Digest comparison does not necessarily “expose the failed removal”

**LOCATION:** “for this failure mode that confirmation is what exposes the failed removal”

**MECHANISM:** [verified: counterexample by derivation] A failed removal is not necessarily observable through the digest comparison. If regeneration overwrites the leftover artifact, or the leftover is byte-identical to the regenerated artifact, the runtime-selected digest matches even though removal failed. The digest establishes byte correspondence; it detects a remaining mismatch, not the historical fact that removal failed. Scoping the sentence to “this failure mode” does not eliminate those cases. [verified: both counterexamples satisfy an unsuccessful removal followed by a matching selected artifact]

**CONCRETE FIX:** Replace the clause with: “for this failure mode, that confirmation detects any remaining mismatch, so compare against the bytes the runtime actually selects, never against the tree’s appearance.”

### Medium — Several trail evidence claims are not supported by the supplied capture

**LOCATION:** Trail claims that `python3 -S -c` preserves the prefix, `python3 -E -S -c` returns `None`, no `PYTHON*` variable exists, and an environment diff has zero differing keys.

**MECHANISM:** [unverified] None of these checks appears in the harness or captured run. The capture establishes only the reported executable/version, a non-null prefix, changed source text, zero in-tree `.pyc` files, and output `OLD`. The additional investigations may have happened, but they are **NOT CONFIRMED** from this review packet.

The trail’s statement that `/usr/bin/python3` equals the captured `/Library/Developer/CommandLineTools/usr/bin/python3` is likewise **NOT CONFIRMED**; no resolution evidence is included. [unverified]

**CONCRETE FIX:** Check in the command/output capture for those probes, or narrow the trail to the observations present in the supplied capture. Record the invoked path and resolved `sys.executable` separately instead of asserting equality without evidence.

### Low — C4 is only conditionally true

**LOCATION:** C4: “reports ‘not reproduced’ on interpreters without a cache prefix, so it is runnable as a check elsewhere”

**MECHANISM:** [verified: control-flow derivation] On an interpreter where `sys.pycache_prefix` exists and equals `None`, the script compiles into `__pycache__`, deletes that directory, imports the new source, and ordinarily prints `not reproduced`. That narrow claim is supported.

However, “interpreters without a cache prefix” can also mean an interpreter lacking the `sys.pycache_prefix` attribute; the script then raises `AttributeError` before producing a verdict. Portability to other Python implementations and platforms is otherwise **NOT CONFIRMED**. [verified: unconditional attribute access; unverified: untested environments]

**CONCRETE FIX:** Use `prefix = getattr(sys, "pycache_prefix", None)` and phrase C4 as “runnable on compatible Python versions; reports ‘not reproduced’ when `pycache_prefix` is unset.”

## Claims and checks with no additional finding

- **A:** Path (a)’s core clearance condition remains sound: comparing the regenerated artifact with the bytes actually selected by the runtime detects a byte mismatch. [verified: direct logical comparison] The claim that this necessarily exposes failed removal is the exception identified above.
- **C1:** “the digest step already catches the case” is supportable only as “catches an unsafe mismatch in the case”; it does not prove that removal failed. [verified: derivation]
- **C3:** The trail expressly declines to identify what sets the prefix. That limitation is accurate and appropriately stated. [verified: trail text] Its ancillary environment investigations remain unsupported by the included capture.
- **C5:** Paths (b) and (c) are textually unchanged, and the insertion remains within path (a). [verified: supplied diff] The added `LOCATE` and actually-selected-bytes imperatives clarify how existing conditions are performed; they do not introduce a distinct fourth clearance path. [verified: grammatical comparison]
- **C6:** “Remedies were authored here, not pasted” is an authorship/provenance assertion and is **NOT CONFIRMED** by the supplied material. [unverified] Remove it unless provenance matters and can be evidenced.
- **D:** No machine path, named OS, vendor build, or specific tool lineup remains in the rule text. [verified: inspected shipped rule insertion] Those details occur only in the trail.
- **E:** The `(a)/(b)/(c)` grammar remains parseable and (b)/(c) retain their original requirements. [verified: supplied diff] The very long parenthetical reduces readability but is not itself a correctness defect.
- **Captured result:** The shown output is consistent with the script on the described interpreter, but the capture’s authenticity and reproducibility are **NOT CONFIRMED** because execution was prohibited and no independent artifact-path measurement is included. [unverified]

FIX harness artifact-selection proof, UNCHECKED_HASH causal qualification, failed-removal digest overclaim, unsupported trail probes, C4 portability wording