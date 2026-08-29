Both prior issues are resolved. The freshness sentence now correctly states that default `UNCHECKED_HASH` is not compared, matching `CHECKED_HASH` validates only the header, and runtime policy controls whether comparison occurs at all.

The revised text adds the missing install/vetting trigger, separates source review from runtime selection, preserves L2 scope, treats tree digests and freshness metadata correctly, and requires digest-backed regeneration or build provenance. Source-only candidates without such artifacts and directly reviewed artifacts remain clearable. Activation checks remain orthogonal, and §4b routes to the canonical §2 gate without duplicating its criteria.

No must-fix wording defect remains.

PROCEED
