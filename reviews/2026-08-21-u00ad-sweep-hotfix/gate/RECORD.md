# Cross-model gate record - round 1 (2026-08-21)

Configuration (owner-locked): gpt-5.6-luna at max + gpt-5.6-sol at max,
mutually blind, one round, exact-diff packet (identical packet-r1.md placed
in isolated per-reviewer working dirs containing only the packet). Both
slugs dry-run probed immediately before the round (READY, exit 0).
Same-provider pair = two independent lenses, both cross-family vs the
author model (Claude); recorded per standing lineup practice.

Identity evidence (tool banner, not self-report):
  luna: model: gpt-5.6-luna; reasoning effort: max
  sol:  model: gpt-5.6-sol; reasoning effort: max

Verdicts (final line, verbatim):
  luna-r1.md: PROCEED (findings: none; Q1-Q8 all clean)
  sol-r1.md: PROCEED (findings: none; Q1-Q8 all clean)

Outcome: PROCEED x2 -> owner pre-authorized landing chain applies
(pathspec stage -> commit -> push -> PR -> STOP at merge authorization).

Reviewed-bytes check: packet-pinned sha256 of all three carriers matched
both the committed blobs (git show HEAD:<path>) and the working tree at
landing time - verified by script, 3/3 OK.

File hashes (sha256, script-generated):
    e1856e1134cbcff1cd652e052e505b0a2d36ab37ed63df73d91f03dee46418ca  reviews/2026-08-21-u00ad-sweep-hotfix/gate/packet-r1.md
    a79d7016d57d75e6742c69dffa8240936a8214bb5871fa356d8b786b73cfbf0a  reviews/2026-08-21-u00ad-sweep-hotfix/gate/luna-r1.md
    6bf7e62c157d98bf65e8829f3158618deb8d092cf873495a5dede365d2039200  reviews/2026-08-21-u00ad-sweep-hotfix/gate/sol-r1.md
