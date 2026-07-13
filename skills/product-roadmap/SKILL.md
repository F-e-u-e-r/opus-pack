---
name: product-roadmap
description: Product-owner planning partner — turns a goal plus the repo's actual state into a verdict, a Now/Next/Later/Not-now roadmap, milestones with acceptance criteria, and agent-ready tasks. Load when the user asks "what should we build next?", any roadmap/milestone/release/MVP/priority/PRD question, wants the current repo assessed for product direction, or wants similar GitHub projects mined for insight. NOT for picking today's coding task inside an already-agreed milestone, and not marketing/pricing strategy.
---

# Product Roadmap

Act as product owner + technical PM. The deliverable is **decisions, not
documents**: what to build next, why, what explicitly waits, and the smallest
version that teaches something. Most of a product owner's value is saying
"not yet" with a reason.

## 1. Evidence before opinion

Assess current state from artifacts, not from the README's aspirations:

- **Product:** does the README say who it's for and what problem it solves?
  Can a stranger run it (setup instructions actually work)? Is there a demo?
- **Engineering:** tests exist and run? CI green? Build documented? Env vars
  documented? No secrets committed? Where does `git log` show real activity?
- **Direction:** open issues/PRs — grouped or a pile? What stalled (old PRs,
  reverted work, dead branches)? Stalls and reverts are evidence of the real
  bottleneck, stronger evidence than any stated plan.
- **Risk:** security-sensitive flows, migration hazards, external API
  dependencies, bus-factor-one areas (code only one person understands).

State what could not be verified and proceed on declared assumptions — never
present an unverified guess as an observation. (Repo scanning is bulk work:
delegate it per delegation-and-review; conclusions only.)

## 2. Find the riskiest assumption

Before sequencing features, name the assumption that kills the project if
wrong ("users want this", "the API allows that rate", "sync can be
conflict-free"). The roadmap's first job is to test that assumption as
cheaply as possible — a milestone that reduces no uncertainty is decoration.

## 3. Roadmap shape: Now / Next / Later / Not-now

- **Now** — blocking the next useful release; nothing enters Now while
  something cheaper reduces more risk.
- **Next** — after the core flow is stable; sequenced, not started.
- **Later** — valuable, not blocking; parked with a one-line trigger for
  revisit ("when >N users", "when X ships").
- **Not now** — tempting but premature; *write why*, or it silently
  re-enters scope next week. This list is the roadmap's immune system.

Sequencing rules:

- **Vertical slices, not horizontal layers.** First milestone = a walking
  skeleton: the thinnest end-to-end path a real user can traverse. "All the
  backend first" is a plan to discover integration problems last.
- Order by risk burndown and dependency, not by excitement.
- Under pressure, **cut scope, never quality** — drop a feature, don't ship
  a broken one.
- Every milestone ends in something observable: shippable, demoable, or a
  measured answer to a named question.

## 4. Prioritization

Score candidates informally on user value, confidence in that value, effort,
and risk — then assign:

- **P0** — you would stop current work for it (broken core flow, data loss,
  security Critical). If everything is P0, nothing is.
- **P1** — in the next milestone.
- **P2** — worth an issue, not a slot.
- **P3** — Not-now list with the reason.

P-levels are internal scoring that feeds the §3 buckets: P0 enters Now, P1
enters Next, P2 becomes a filed issue under Later, P3 joins Not-now. The
output (§7) shows buckets, not P-labels.

Confidence caps value: "High value, Low confidence" items get a cheap probe
(prototype, mock, 5-user test), not a milestone. Distinguish evidence
("users filed 6 issues asking for X") from speculation ("users would love
X") — speculation is allowed, labeled.

## 5. Milestone block (the only template)

```markdown
## Milestone: <name>
Goal / user value:      one sentence, outcome not feature list
Scope:                  the thin slice
Out of scope:           what this milestone deliberately ignores
Riskiest assumption:    what this milestone proves or kills
Acceptance criteria:    observable checks (tie to ground-truth-gates where possible)
Dependencies / risks:
```

## 6. Mining adjacent GitHub repos for insight

When comparable projects exist, their repos are free research:

- **Their issues are user research** — recurring requests and complaints in
  a similar project are demand signals for yours, cheaper than interviews.
- **Their changelog/BREAKING CHANGES/migration guides are regret logs** —
  design decisions they had to walk back; avoid the same one-way doors
  (choices that are hard to reverse).
- **Their architecture answers feasibility questions** ("how do they handle
  sync?") before you prototype.
- Calibrate: stars ≠ quality, activity ≠ direction; a popular repo's
  *unsolved* issues are your differentiation candidates.
- **License & IP hygiene before borrowing anything beyond ideas** (a conservative
  agent default, not legal counsel — confirm the actual license and target
  compatibility, and honor each license's exact terms):
  - Preserve the source's required notices: MIT needs its copyright + permission
    notice carried along; Apache-2.0 adds redistribution duties (and NOTICE
    handling when the upstream ships one). As a safe default, treat strong
    copyleft (AGPL/GPL) and unlicensed source as *ideas only* unless the user
    clears the obligations — that is our conservative policy, not a claim the
    license forbids all use.
  - An AI rewrite/translation of copyrighted source is still a derivative — you
    cannot launder it by paraphrase. True clean-room = an independent
    implementation from an independently-written spec, not "I read it, then
    rewrote it from memory."
  - Code-license compatibility does NOT open a project's art, characters, or
    trademarks.
  - Adopt on *mechanism*, never a source's benchmark numbers — copy no metric you
    did not reproduce, or you launder an unverified claim into your docs as fact.
  - ✅ "Independent reimplementation from a spec I wrote, carrying the upstream's
    required notice." ❌ "It's AGPL, but I had the model rewrite it in a new
    style, so it's clean."

Summarize insights with links; never vendor code or copy positioning wholesale.

## 7. Output shape

**Verdict** (stage, main bottleneck, best next move, what not to do yet) →
**Now/Next/Later/Not-now** → **milestone blocks** for Now →
**tasks split three ways**:

- *Agent does* — emit as dispatch packets per delegation-and-review §2.
- *User does* — only what genuinely needs them: credentials/app setup,
  payment/legal, positioning, destructive-migration approval.
- *Needs information* — the question, why it matters, and the safe default
  if unanswered.

Keep the whole output one screen where possible; depth goes into linked
files, not the verdict.

## Provenance

Authored 2026-07 from the user's roadmap-skill reference draft (kept:
Now/Next/Later/Not-now, milestone fields, value/confidence/effort/risk lens,
P0–P3, repo checklist layers, agent/human/needs-info split, "what not to do
yet"; added: riskiest-assumption framing, vertical-slice sequencing,
cut-scope-not-quality, stalled-work-as-evidence, adjacent-repo mining with
calibration; dropped: fixed 7-section report ceremony — verdicts over
paperwork).
The 2026-07-13 license/IP-hygiene expansion (§6) —
classify-license-before-copying, AI-rewrite-doesn't-launder-a-derivative,
clean-room, code-license ≠
art/character IP, adopt-mechanism-not-unreproduced-numbers — comes from a
cross-repo mining pass over seven staged libraries (class-distilled; the pack
had no IP doctrine before).
Method is stable; nothing environment-specific to re-verify.
