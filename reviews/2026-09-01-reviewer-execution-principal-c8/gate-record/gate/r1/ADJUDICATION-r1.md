# R1 adjudication — both verdicts FIX; all findings first-hand re-derived

Reviewer identity (verified): luna = gpt-5.6-luna @ max, sandbox read-only,
exit 0, 8.0KB body; sol = gpt-5.6-sol @ max, sandbox read-only, exit 0, 9.3KB
body. Both structured per schema; both zero settled-frame CONCERNs; both named
the SAME nearest-failure (authority-source provenance in §4). Convergence
raised priority only — every disposition below rests on my own re-derivation
against DESIGN v1 + the canonical excerpts (CMR §3).

Merged dispositions (L=luna finding #, S=sol finding #):

- FIX-1 (L1+S1, must-fix) ADOPTED: authority-source provenance boundary.
  Real defect: "comes from the dispatch packet" does not separate the
  dispatch's own control text from artifact material embedded in the packet;
  "predeclared review policy" not defined as operator-owned/content-
  independent (harness config auto-ingestion makes repo-authored
  policy-shaped text reachable). Fixed in §3 spine + §4.
  Sub-claim REJECTED-WITH-REASON (L1's "grant issued only after the artifact
  requests execution" risk): the propose→operator-grant flow is a settled
  design feature — legitimacy comes from the granting principal (operator),
  not from what prompted the proposal; fix therefore requires operator-owned
  content-independent authority, it does not forbid post-proposal grants
  (made explicit in §4).
- FIX-2 (L2+S8) ADOPTED: "zero rule violations" overclaims vs B4, and §0's
  "principal side not at all" overstates. Re-derivation: B4's own terms bind a
  PACKET-embedded imperative and trigger on acting INSTEAD OF reviewing; the
  counterexample's imperative is tree-embedded and the reviewer still reviews
  — strict B4 does not fire; even extension-by-analogy is post-hoc lens
  handling, not a pre-execution authority rule. Counterexample retained in
  corrected, stronger form; §0 now says "no pre-execution capability-envelope
  rule; existing principal-side handling is post-hoc and packet-scoped".
- FIX-3 (L3+S4a) ADOPTED: exec axis could not represent direct process spawn
  without shell. Receipt now `exec_reach: none | arbitrary | unknown` with
  arbitrary = shell OR direct process creation; orthogonality note updated.
- FIX-4 (L8+S4b+sol A3) ADOPTED: network plane split — `net_reach` covers
  reviewer-DIRECTED egress only; model-serving transport excluded (present in
  every external review, packet-only included; governed by CMR §2 packet
  discipline); `scoped: model-API` can never be read as command-egress
  isolation; §5 live-trigger reworded to reviewer-directed capabilities.
- FIX-5 (L4+S5) ADOPTED: disposable defined (created for this review, no
  unrelated state, discardable); write-capable critic's independent copy IS a
  disposable workspace; "reviewed baseline" = the settled state the verdict
  binds to; `write_reach: none-anywhere` means no reachable host write path
  at all (frozen tree + writable /tmp/$HOME is never `none`); §4 ✅ example
  corrected to show disposable write reach.
- FIX-6 (L5 + S2 breach-half) ADOPTED: breach decision rule added — affected
  conclusions = those whose evidence the out-of-envelope action could have
  influenced; unattributable influence fails closed to whole-lens-missing;
  B4 machinery (retain artifact, missing lens, pre-fixed substitution)
  explicitly carried; dispatcher's own reproduction always available.
- FIX-7 (L6+S3) ADOPTED: E5 qualified "without dispatch preauthorization";
  §4 adds: artifact mention is neither necessary nor sufficient — an
  independently preauthorized command stays in-envelope when the artifact
  also mentions it.
- FIX-8 (L7) ADOPTED: pointer no longer coins "nothing else leaves"; it
  tracks the section's actual duties (inline-only + packet-minimization +
  no-secret-egress).
- FIX-9 (S2) ADOPTED (structural): receipt split into plane 1 = effective
  capability (evidence; isolation credit source) and plane 2 = authorized
  envelope (operator-owned; breach comparator). Declaring reach never
  authorizes it; plane-1 surplus beyond plane 2 = recorded ambient-reach
  risk, not a licensed power, not itself a breach (reach ≠ act).
- FIX-10 (S6) ADOPTED: tool_reach must carry operations/resources (bare
  product name = unknown-scope); unrelated_secret_reach defined as secrets
  the task does not require; task-required credentials are declared plane-2
  members — presence never auto-disqualifies (new carve-out viii).
- FIX-11 (S7, nit→factual upgrade) ADOPTED + corrected by re-observation:
  today's probe banners record model + reasoning effort + SANDBOX MODE
  (p1.err/p2.err first-hand) — E12 row and §6 assertability updated: part of
  plane-1/2 is already banner-asserted at every run; still nothing on
  network/tool/secret reach.
- FIX-12 (L9, nit) ADOPTED: every Appendix A cell now tagged (MCP-config
  declaration = FIRST-HAND CURRENT config re-read 2026-08-30; model-API
  reach = FIRST-HAND CURRENT probe round-trips; broad-read surface =
  FIRST-HAND CURRENT help re-read; sibling-verdict read stays RECORDED
  HISTORICAL 2026-07-17).

All remedies authored by me against the full design (CMR §3 authored-fix
rule); no reviewer text pasted on a finding's strength.
