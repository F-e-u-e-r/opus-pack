# ④ Meaningful confirmation / approval-fatigue degradation — evidence package (2026-08-30)

Full audit trail for the operational-rigor §2 meaningful-confirmation limb and its
skill-vetting §2 pointer. Branch `meaningful-approval-review` from main `297d8ed`.

## What the change does

The pack already requires that a consequential confirmation gate is decided by the
human ("it exists to make a person decide"), with per-invocation grants, a
standing-authorization carve-out, a bounded blanket-go, and destructive-one-at-a-time.
**What was missing** is a candidate-side rule: an instruction can leave the formal
`[y/N]` intact while draining the human's decision of scrutiny — by re-asking until
yes, steering toward blanket approval, minimizing decision-relevant risk so the
operator decides without an informed view, or hiding a consequential action inside a
benign-looking batch.

Disposition: **PARTIAL-GAP** (C was considered at orientation; the owner adjudicated
B). Abstraction: **L2 — meaningful-authorization degradation**. The criterion is
judged by **observable effect, not by guessing intent**: a finding is an instruction
that materially degrades the operator's independent, informed scrutiny of a
consequential authorization.

The canonical rule lives in operational-rigor §2 (immediately after the
confirmation-gate bullet); skill-vetting §2 carries a bare routing pointer.

## Key distinctions (established by the inert A1–A14 controls + the doctrine walk-through)

- A formal confirmation can be present while the review is degraded.
- Repeated prompting, urgency, batching, and words like "routine" are **not**
  themselves findings.
- **Explicit-refusal persistence** with no materially new decision-relevant
  information is a finding; a **materially-new-information re-prompt** and a **genuine
  delivery-recovery retry** are not.
- Risk minimization fires only when it leaves the operator without an informed view.
- A user's own blanket grant over a fully surfaced scope, independently scoped
  standing authorization, and ordinary distinct sequential confirmations are cleared.
- Same phrase, different context flips the verdict (no keyword is a verdict).

**No human was subjected to high-frequency approval prompting.** The first-hand object
was the current doctrine (read verbatim), inert candidate texts, and a procedure
walk-through. **Semantic discrimination = first-hand reviewed; the rule's behavioral
effectiveness = unprobed → one canonical marker → standing #115.**

## MOD-CONSISTENCY (the one owner-authorized operative landing correction)

The R3 limb's post-refusal shape read "persisting after an explicit refusal with no
new decision basis." Because "no new decision basis" could be read as "any tiny new
information," it was aligned to the limb's own controlling boundary (used by the
clearer and the tell): **"persisting after an explicit refusal without materially new
decision-relevant information."** This is the only operative change beyond the single
marker; the landed reconstruction is **R3 canonical + one marker + MOD-CONSISTENCY**
(not "adaptations none").

## Contents

- `orientation-report.md` — the PARTIAL-GAP orientation, A1–A12 controls, false-clear,
  and current-rule semantic map. (A13/A14 + the meta-control were added in the design
  packets.)
- `packets/packet-r{1,2,3}.md` — the review packets (A1–A14 discrimination table +
  meta-control).
- `verdicts/r{1,2,3}-{luna,sol}.md` — the six reviewer verdicts.
- `gate-trail.md` — per-round finding dispositions (R1 both FIX → R2 split → R3 2/2).
- `self-review-notes.md` — the author's pre-reviewer adversarial read.
- `final-wording.md` — the landed canonical limb + pointer, and the marker /
  MOD-CONSISTENCY note.
- `landing-manifest.md` — declared adaptations, the MOD-CONSISTENCY record, and the
  faithful-reconstruction battery.
- `atr-provenance-note.md` — how ATR-2026-00118 was used and what was NOT tested.
- `MANIFEST.sha256` — hashes of every file here.

## Review

Dual-blind **two-variant** review (two variants of one GPT-5.6 family, both at max
effort) — both outside the author family; **NOT a cross-family gate** (grok
unavailable this window). R1 both FIX → R2 one PROCEED / one FIX → R3 PROCEED × 2, all
thirteen review axes.

## Scanner architecture

**SUPPORTING-ONLY.** The legitimate/attack split turns on context a phrase list cannot
decide (it would false-positive on exactly the cleared cases). No `.github/checks.py`
change, no CI gate, no runtime scanner. L3 general HITL / social-engineering taxonomy
discovered and deliberately **not activated**.
