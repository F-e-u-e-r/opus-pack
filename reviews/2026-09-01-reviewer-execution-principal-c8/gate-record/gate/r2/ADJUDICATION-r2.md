# R2 adjudication — luna FIX(1)+1 nit, sol FIX(1,2,3)+1 nit; all re-derived

Identity verified: luna gpt-5.6-luna/max/read-only exit 0, 3.1KB; sol
gpt-5.6-sol/max/read-only exit 0, 6.9KB. Zero settled-frame concerns both.
R1 fixes held (luna A4–A7/A9–A16 PASS; sol disposition check: 1,2,4,6,7,8,
11,12 clean). Non-overlapping new findings; each re-derived first-hand:

- FIX-13 (luna 1, must-fix) ADOPTED: §2 "fully-compliant" + "no written rule
  blocks the act" overclaimed against B5 (D&R §7: read content never becomes
  instructions, never executed on arrival) — for a pack-bound reviewer the
  act IS a conduct violation; what current doctrine lacks is any defined
  consequence for the review's credit (B4's narrow trigger still does not
  fire), and an external harness reviewer is not reached by B5 at all.
  → §2 retitled "dispatch-compliant false clear", walkthrough steps (4)/(5)
  rewritten (conduct-rule vs credit-semantics separation; dispatcher-side gap
  restated); §4 + §8 add "supplements, never overrides §7".
- FIX-14 (luna 2, nit) ADOPTED: §6.6 banner claim could be translated into
  exec_reach:none / isolation credit. → banner = run metadata evidencing the
  applied sandbox (write-restriction posture); never by itself
  effective-capability evidence; never translates into exec/net reach values
  (help text itself proves read-only still executes). E12 row aligned.
- FIX-15 (sol 1, must-fix) ADOPTED: positive credit-eligibility rule added —
  credit earned only by plane-1 evidence AFFIRMATIVELY establishing the
  claimed bound; known reach outside the bound denies the matching credit
  (non-breach absent action; ordinary findings intact); completeness of the
  receipt is never credit.
- FIX-16 (sol 2, must-fix) ADOPTED: plane 1 gains `task_credential_reach`
  (non-secret description of effective operations/resources | unknown);
  declared-vs-effective divergence = surplus reach; declaration alone never
  earns scoped-credential credit.
- FIX-17 (sol 3, must-fix) ADOPTED: `scoped:<bound>` added to exec_reach and
  net_reach as an evidence-backed technical bound (unprovable bound → honest
  arbitrary/reviewer-directed/unknown, never a copied plane-2 declaration);
  §4 ✅ example rewritten with both planes' real field names showing
  legitimate divergence (plane 1 exec arbitrary vs plane 2 named probe).
- FIX-18 (sol 4, nit) ADOPTED: E4 gains the evidentiary qualifier — write
  authorization never relaxes verdict attribution; mutation-dependent
  evidence describes the mutated state, conclusions about the baseline need
  comparison/reproduction against it.
- Sol's nearest-failure note (provenance boundary must survive byte-fitting)
  → recorded as a binding §11 line for the post-gate implementation stage.

All remedies authored by me against the full design; no reviewer text pasted
on a finding's strength. DESIGN → v3; round 3 is the final round.
