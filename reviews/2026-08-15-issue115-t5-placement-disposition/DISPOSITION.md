# T5-placement concern disposition (owner ruling, post-probe)

Additions-only record. No historical artifact is rewritten: the sealed
campaign, the #186 Section-A disposition, the #187 concern
adjudication, and the #199/#202/#203 probe packages are all left
byte-untouched, and this record does not edit the canonical marker or
any doctrine text.

## Disposition

> The authorized T5-placement follow-up probe completed as
> preregistered and produced `INCONCLUSIVE(MIXED-P1+MIXED-P2)`. It did
> not distinguish H1, H2, or H3 and supports no doctrine
> recommendation. The prior `NEEDS-NEW-PROBE` execution obligation is
> therefore satisfied, while the underlying concern remains
> unresolved. Disposition: **`RETAIN-CONCERN-ONLY
> (PROBE-INCONCLUSIVE)`**. The Section-A path-3 settlement and the
> canonical T5-placement marker remain unchanged.

Scope of "as preregistered" in that ruling: it covers the EXECUTION
and the application of the frozen outcome mapping — 36/36 in frozen
slot order, frozen rendering, frozen predicate, frozen owners, frozen
precedence, frozen mapping. It is **not** a claim of
protocol-compliance as-written. The adjudication METHOD carries a
recorded `AUTHORIZED-ADJUDICATION-METHOD-DEVIATION` (see Provenance),
and nothing in this record asserts otherwise.

Reading of `unprobed`: this is the Section-A marker taxonomy's term,
not a claim that no probe was ever run. A probe WAS run — the whole
#199 → #202 → #203 chain is real, durable, and cited here. It simply
produced no affirmative evidence capable of moving the marker. This
matches the discipline already applied to T2: a post-settlement probe
does not by itself promote a marker to `probed in part`.

## Why not `NEEDS-NEW-PROBE` any longer

The execution obligation that routing created has been discharged in
full: the prereg is durable, the prefix qualified the harness, 36/36
scored observations ran CLEAN with 0 UNGRADABLE, two independent
recomputations reproduced the grading and the derivation, and the
preregistered mapping returned a definite verdict. Continuing to carry
`NEEDS-NEW-PROBE` would imply either that this probe is unfinished or
that the standing disposition demands another attempt now. Neither is
true. The precise state is: **the concern is not empirically resolved,
and the authorized probe that was meant to resolve it has completed
without identifying H1, H2, or H3.**

## Why not closed

`RESOLVED` / `NO-CONCERN` is equally unavailable. The unit supported
none of the three explanations — not current-guidance sufficiency, not
a guidance-disambiguation gap, not a lexical/tier limitation. With all
three undecided there is no evidence basis for asserting the original
placement concern does not exist. The concern therefore remains
epistemically unresolved after a completed inconclusive probe, which is
exactly what `RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)` records.

## Marker: explicitly unchanged

The canonical T5-placement marker stays `unprobed` and its bytes are
untouched. It is not promoted to `probed in part`. The contrast with
T4 is the reason: T4 was promoted because marker-specific evidence
reached PASS+SUPPORT and the owner promoted it under a path-1
disposition. Here the original evidence was FAIL-SIGNAL, the follow-up
probe was INCONCLUSIVE, all three explanations are unresolved, and the
mapping issued no recommendation. The path-3 settlement stands.

## Remaining campaign capacity: closed, not spent

The 11 unused slots inside the `issue115-t5pprobe-v1` hard cap are
**closed to this concern's disposition**. They remain what they have
always been — unused physical hard-cap capacity, never a reserve and
never an execution authority.

Adding observations now would be conditioned on counts that have
already been seen — result-driven extension, which is exactly what
preregistration exists to prevent. That holds regardless of how close
any arm sat to a band edge, and this record deliberately makes no
claim either way about closeness: the preregistered mapping returned
INCONCLUSIVE, and that is the whole of it. Any future work on this question
starts over — new decision question, new probe design, new prereg, new
budget — rather than resuming at slot 40 of a closed unit.

## Provenance

| element | reference |
|---|---|
| original sealed outcome | T5-placement = **FAIL-SIGNAL** (T5S1: bare 0/3, ruled 0/3, CLEAN); marker undischarged |
| Section-A settlement | **path-3**, PR #186 (merge `444880da4dbdf3c94531d6507252c1ad3870e71c`) |
| concern adjudication that routed here | **NEEDS-NEW-PROBE**, PR #187 (merge `c1ab89de42f087dc78f510da5071571ee1f5b4dc`) |
| probe preregistration | PR #199 (merge `6fe6813bcc35edb86a8b92b4aaaa7f9ba3459ef7`) |
| prefix execution evidence | PR #202 (merge `1578bdabc9f813f780e76f2f6664a4496d85001a`) |
| scored execution evidence | PR #203 (merge `66d9144a7cb49714cb2132280161c16b47924d96`) |
| final accounting | 1 dry-run + 2 smokes + 36 scored = **39/50 consumed**; the prereg's 39 planned invocations complete |
| verification depth | arm-blind grading; **dual independent recomputation** (two reviewers, mutually blind, two phases) with three-way unanimity on all 36 primary classes and fold hosts, both concluding `RECOMPUTATION CONFIRMS` |
| adjudication method | **`AUTHORIZED-ADJUDICATION-METHOD-DEVIATION`** — the prereg *proposed* a separate model adjudicator; grading was performed by the operator applying the frozen mechanical predicate under a later owner authorization; both facts retained, the sealed text not retro-fitted |
| final outcome | **`INCONCLUSIVE(MIXED-P1+MIXED-P2)`** — recommends nothing; H1, H2 and H3 all undecided |

The per-arm counts recorded in #203 (`P1 B/C/E = 0/6, 2/6, 4/6`;
`P2 B/C/E = 0/6, 3/6, 1/6`) are descriptive provenance only. They are
deliberately absent from the reasoning above and carry no weight in
this disposition.

## Claims this disposition does not make

Stated explicitly because each is a plausible misreading of an
inconclusive result, and two independent recomputers flagged the first
of them unprompted:

- that H2 is weakly supported;
- that the E arm showed improvement;
- that P1 trends toward a guidance gap;
- that P2 favours the current guidance;
- that a lexical/tier association is the likely explanation;
- that more samples would probably resolve the question;
- that the doctrine should be amended;
- that the marker has now been probed in part.

## Effect

- Concern disposition: **`RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)`**
- Section-A settlement: **path-3, unchanged**
- Canonical T5-placement marker: **`unprobed`, bytes unchanged**
- Doctrine: **unchanged**; no amendment is derivable from this result
- Campaign: **closed at 39/50**; the remaining 11 hard-cap slots are
  not spent and are not a reserve
- `issue115-t2probe-v1` headroom 11 and `issue115-stage2-v1` reserve
  18: **untouched**
- Issue #115: **OPEN**
