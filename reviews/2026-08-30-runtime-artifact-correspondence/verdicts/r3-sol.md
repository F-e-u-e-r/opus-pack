The prior issues are resolved:

- Freshness wording now correctly distinguishes default `UNCHECKED_HASH` and `CHECKED_HASH` behavior, acknowledges runtime-policy overrides, and limits a match to header/source agreement—not bytecode provenance.
- Discovery covers all candidate artifacts the runtime may select, including external caches and load paths, while explicitly excluding unrelated data/config.
- Local regeneration requires the exact reviewed source, a named toolchain/recipe, and digest verification of the artifact actually selected.

Fresh review against the rubric: all ten axes pass. The install gate and vetting step provide an actionable recognition trigger; source review and runtime selection remain distinct; digests and freshness metadata are not mistaken for correspondence; all three clearance paths have the required exact-byte binding; source-only and directly reviewed artifacts remain clearable; activation analysis stays orthogonal; scope remains L2; and the vetting text is a routing pointer rather than a competing authority.

I found no internal contradiction, immediate same-shape bypass, or wording that would cause a clean source-only candidate to fail.

PROCEED
