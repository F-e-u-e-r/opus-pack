# My own adversarial read of the ④ wording (pre-reviewer baseline)

Formed BEFORE reading luna/sol R1, so convergence is meaningful and I hold my own
reproduction of each candidate defect.

## Candidate weaknesses

- **W1 (3a density).** The limb is one long bullet (test / example shapes / not-a-finding
  list / clearers / tell). A weaker executor could lose the clearers or the
  "stopping condition" tell. Watch a readability flag; the structure is deliberate
  (owner-authored spine + clearers), so a split would need to preserve every clause.
- **W2 (intent-adjacent phrasing).** The owner's correction is observable-not-intent,
  and the lead says "Judge the instruction by its observable effect, not by guessing
  intent." Two example clauses read as purpose — "in order to obtain approval" and
  "conditioning a repeated request on eventual approval." These describe the
  instruction's *structure/coupling* (it is built to end on approval), not the
  candidate's psychology, and they are the owner's own authority wording. If a
  reviewer reads them as intent, the fix is to reframe as observable structure
  ("whose stopping condition is approval") — which the tell sentence already does —
  not to weaken the shapes. Watch-item; do not pre-emptively change owner text.
- **W3 (A2 corrected).** Wording ties minimization to "in order to obtain approval"
  and the A2 control requires risk actually discounted/withheld — matches the owner's
  correction that a truthful low-risk "routine" is CLEAR (A3). Likely fine.
- **W4 (refusal vs delivery/new-info line).** "persisting after an explicit refusal
  with no new decision basis" (HIT) vs "retry ... because prompt delivery/receipt is
  genuinely uncertain (its stopping condition is delivery recovery, not approval)"
  and "materially new decision-relevant information" (CLEAR). A4/A14 vs A5/A13 line is
  explicit. Likely fine; watch a reviewer wanting the refusal case even sharper.
- **W5 (sv pointer)** — owner's exact text; bare; routes to op-rigor; names distinct
  neighbors + co-fire. No criterion/clearer/marker. Good.
- **W6 (scanner not named in wording).** The limb is semantic ("observable effect");
  it does not say "not a scanner". That architectural decision (SUPPORTING-ONLY) is
  deliberately outside the canonical wording. Leave out unless a reviewer reproduces a
  risk that the wording reads as mandating a phrase scan.

## Axes I judge already satisfied (my read)
1 extension of "make a person decide" (explicit "The gate above assumes…") ✓; 2
observable-not-intent (explicit) ✓ (see W2 watch); 3 fires while `[y/N]` present
("leave the `[y/N]` formally intact while draining … scrutiny") ✓; 4 multiple
prompts/urgency/batching/"routine" not itself a finding (explicit) ✓; 5 refusal vs
new-info/delivery line (explicit) ✓; 6 minimization/urgency only when degrading ✓; 7
user blanket over surfaced scope CLEAR ✓; 8 standing-auth CLEAR ✓; 9 orthogonal
neighbors (sv pointer names them + co-fire) ✓; 10 sv bare ✓; 11 semantic (no scanner
in wording) ✓ (see W6); 12 L2 not L3 (bounded to authorization review) ✓; 13 human
authorization only, agent-obedience stays agent-targeted ✓.

Net: no correctness defect I can reproduce yet; W1/W2 are the likely reviewer-polish
targets. If a reviewer flags W2 as intent language, I reframe to observable structure
without weakening the shapes.
