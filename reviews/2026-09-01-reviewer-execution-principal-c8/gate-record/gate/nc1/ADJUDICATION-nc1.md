# NC1 adjudication — luna PROCEED, sol FIX(1) → NC1 NOT-PASSED (1/2); gate ENDS per owner closure rule

Identity verified: luna gpt-5.6-luna/max/read-only exit 0, 2450 B — PROCEED,
NC1–NC20 all PASS, ledger-fidelity clean, nearest-failure = §4/§11
named-probe/provenance boundary. sol gpt-5.6-sol/max/read-only exit 0,
4410 B — FIX: 1 (NC14/NC15 FAIL, other 18 axes PASS), ledger-fidelity: Δ10
"present but not faithfully safe".

## Sol finding 1 — REPRODUCED FIRST-HAND (CONFIRMED)

v4 line 230: `read_reach: none | <roots/breadth> | unknown   # none =
packet-only: no repository/host read reach`. The gloss equates ONE axis value
with the overall MODE. v4 §5 defines live mode as ANY reviewer-directed
action capability (read files, run commands or tools, or reach the network),
and §9(i) says mode is decided by reviewer-directed capability. The schema
itself makes the conflict representable: read_reach: none beside exec_reach:
arbitrary / net_reach: reviewer-directed / tool_reach: <connector> is a LIVE
principal that the gloss stamps packet-only — a dispatcher could then apply
the packet-only carve-out and skip principal confinement. Correct implication
runs one way only (packet-only ⇒ read_reach none), and the gloss asserts the
converse.

Provenance of the defect: the gloss is present verbatim in Δ10 AS AUTHORED in
ADJUDICATION-r3 (authored by the dispatcher, adopted by the owner) — a
same-shape regression (axis-value/mode conflation, kin to the plane
conflations rounds 1–2 removed) introduced by a correction, i.e. exactly the
class this confirmation round existed to catch. Luna passed NC14/NC15 over
the same bytes — the second variant caught what the first missed.

## Disposition

Per the pre-committed closure rule (any FIX → gate ends): NC1 = NOT-PASSED
at 1/2 PROCEED. NO v5 authored, NO second confirmation round, NO dispatch
retry. The finding is recorded as CONFIRMED with this candidate remedy noted
for the owner's next adjudication (NOT applied anywhere): change the gloss to
describe only its own axis, e.g.
`# none = no repository/host read reach (this axis only — mode is decided by
§5's reviewer-directed-capability trigger, never by one field)`.
Everything else in v4 stands 20/20 + 18/20 confirmed across the two variants;
the sole defect is this one comment gloss.

Formal state: ⑧ ORIENTATION PASSED (B/L2) · ORIGINAL GATE CAP-REACHED /
NOT-PASSED @ v3 · v4 = owner-adjudicated candidate, NC1 NOT-PASSED (1/2;
sole confirmed defect = Δ10 gloss) · implementation LOCKED · conditional
marker pre-ruling NOT triggered (it required 2/2) · ⑧-H NOT STARTED.
