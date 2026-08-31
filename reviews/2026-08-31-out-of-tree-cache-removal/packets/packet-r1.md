REVIEW TASK — one small doctrine patch to a rules pack. Review the TEXT below
directly. Do NOT run commands or read files; everything needed is inlined.

## Context
Repo: a portable "skills pack" of rules that later AI sessions obey as doctrine.
File: skills/operational-rigor/SKILL.md, section 2 (the third-party install gate).
The rule being amended landed 3 days ago: "a source review clears executable
BEHAVIOR only when the runtime-selected bytes are bound to what was reviewed."
It offers three clearance paths (a)/(b)/(c). This patch amends ONLY path (a).

HOUSE RULE that binds this patch: pack text must stay portable. One person's
machine paths, OS, vendor builds, or tool lineup must NOT appear in rule text
(they belong in the PR trail). An earlier draft of this patch named a specific
vendor's interpreter and a `~/Library/...` path; that was removed for this reason.

## The landed text of path (a), before the patch
  "Legitimate clearance: (a) remove any competing shipped or cached artifact,
   regenerate from the exact reviewed source under a named toolchain/recipe,
   and confirm the bytes the runtime then selects match the regenerated
   artifact by digest; (b) bind the exact artifact bytes by digest to the
   reviewed source + recipe via reproducible/attested build evidence; or
   (c) review the runtime-selected artifact itself, when it is reviewable as
   source-equivalent, as the executable truth."

## The patch (unified diff)
diff --git a/skills/operational-rigor/SKILL.md b/skills/operational-rigor/SKILL.md
index 710a090..6d62315 100644
--- a/skills/operational-rigor/SKILL.md
+++ b/skills/operational-rigor/SKILL.md
@@ -415,9 +415,15 @@ When rigor conflicts with finishing sooner, rigor wins.
   runtime-selected bytes are themselves reviewed, or an independent path
   establishes those *exact* bytes were produced from the reviewed source
   under a named build/compile recipe. Legitimate clearance: (a) remove any
-  competing shipped or cached artifact, regenerate from the exact reviewed
-  source under a named toolchain/recipe, and confirm the bytes the runtime
-  then selects match the regenerated artifact by digest; (b) bind the
+  competing shipped or cached artifact — LOCATE it rather than assume its
+  conventional in-tree path, because a runtime may cache OUT of tree (a
+  central or path-mirrored cache directory, a per-user cache root) and
+  deleting the in-tree one then silently no-ops, leaving a visibly clean
+  tree that still executes stale bytes — regenerate from the exact
+  reviewed source under a named toolchain/recipe, and confirm the bytes
+  the runtime then selects match the regenerated artifact by digest; that
+  digest confirmation is what makes an incomplete removal detectable, so
+  it is load-bearing rather than a second opinion on the removal; (b) bind the
   exact artifact bytes by digest to the reviewed source + recipe via
   reproducible/attested build evidence; or (c) review the runtime-selected
   artifact itself, when it is reviewable as source-equivalent, as the

## Evidence behind the patch (all first-hand, this machine)
Environment binding: macOS 26.6.2 arm64, /usr/bin/python3 = CPython 3.9.6 as
shipped by Apple CommandLineTools. Fixtures were throwaway dirs.

E1. That interpreter reports sys.pycache_prefix = '<user cache root>/com.apple.python'
    by default. Bytecode for a module therefore lands in a PATH-MIRRORED directory
    under that root, NOT in __pycache__ beside the source.
    - `python3 -S -c "import sys;print(sys.pycache_prefix)"` -> same value (not site config)
    - `python3 -E -S -c` (ignore environment) -> None
    - No PYTHON* variable is present in the parent shell OR in the child's os.environ,
      and a full env diff between the normal and -E child shows ZERO differing keys.
      So the mechanism is INSIDE the interpreter and keyed somehow to -E; I did NOT
      establish what actually sets it. I am claiming the observed EFFECT only.

E2. The operational consequence, run end to end:
    - write m.py returning "OLD"; compile it to an UNCHECKED_HASH .pyc
    - rewrite m.py to return "NEW" (different length, different mtime)
    - `rm -rf __pycache__`   <- the conventional "clean it" move
    - `find . -name '*.pyc'` -> 0 results (tree looks clean)
    - `python3 -c "import m; print(m.v())"` -> prints OLD
    The stale bytecode came from the out-of-tree cache, which the removal never
    touched. Note the landed digest step in (a) WOULD have caught this; the removal
    step alone would not.

## What I want challenged (findings are claims — report NOT CONFIRMED unless you
## can derive it from the text and evidence above)
1. GENERALIZATION. The patch says "a runtime may cache OUT of tree (a central or
   path-mirrored cache directory, a per-user cache root)". My evidence is ONE
   interpreter on ONE OS. Is that phrasing an over-generalization for doctrine, or
   is it fairly stated as a possibility ("may") that a reviewer must rule out?
2. REDUNDANCY. Path (a) already ends in a digest confirmation that catches this
   case. Does the added clause earn its words, or is it restating a check that
   already fires? If redundant, say so plainly — dropping the patch is an
   acceptable outcome.
3. OVER-CLAIM. "that digest confirmation is what makes an incomplete removal
   detectable, so it is load-bearing rather than a second opinion on the removal"
   — is that true of ALL failure modes path (a) guards, or only of this one?
4. SCOPE / HOUSE RULE. Does any remaining wording smuggle in machine-, OS-, or
   vendor-specific content that should live in the PR trail instead?
5. INTERNAL CONSISTENCY. Does the insertion break the (a)/(b)/(c) sentence
   structure, contradict the rest of the limb, or change what (a) requires?

## Cost asymmetry
The expensive failure is shipping a FALSE or OVER-BROAD empirical claim into text
later sessions obey without re-deriving it. An over-cautious nit costs nothing.
Probe the over-claim side hard.

## Reporting format
Severity-ranked findings, each as: LOCATION (quote the phrase) + MECHANISM (why it
is wrong or unsupported) + CONCRETE FIX (minimal wording). Tag each claim
[verified: how] or [unverified]. If a check found nothing, say so explicitly.
Report failure or uncertainty honestly rather than manufacturing findings.
LAST LINE must be exactly: PROCEED   or   FIX <comma-separated list>
