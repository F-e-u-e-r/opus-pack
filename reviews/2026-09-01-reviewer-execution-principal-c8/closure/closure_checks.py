#!/usr/bin/env python3
"""MOD-AXIS-MODE mechanical closure gate — owner-authorized, one-shot.

Core invariant under test: MODE is a property of the effective
reviewer-directed capability envelope, never an alias for any individual
receipt field. Runs against a design file given as argv[1].

Exit 0 = ALL PASS. Any failure -> nonzero, with the failing check named.
"""
import re, sys

path = sys.argv[1]
t = open(path, encoding="utf-8").read()
lines = t.splitlines()
results = []

def check(cid, desc, ok):
    results.append((cid, desc, bool(ok)))
    return ok

# --- C-series: repair + anti-conflation sweep ---
NEW_GLOSS = "this axis only — mode is decided by §5's reviewer-directed-capability trigger, never by one field"
OLD_GLOSS = "= packet-only: no repository/host read reach"
check("C1", "repaired gloss present on read_reach line",
      any(l.startswith("read_reach:") and NEW_GLOSS in l for l in lines))
check("C2", "old axis=mode gloss absent everywhere", OLD_GLOSS not in t)

AXIS_FIELDS = ["read_reach:", "write_reach:", "exec_reach:", "net_reach:",
               "tool_reach:", "unrelated_secret_reach:", "task_credential_reach:"]
axis_lines = [l for l in lines if any(l.startswith(f) for f in AXIS_FIELDS)]
check("C3", "schema exposes all 7 plane-1 axis fields", len(axis_lines) == 7)
check("C4", "no plane-1 axis line mentions packet-only (mode words stay off axis lines)",
      all("packet-only" not in l for l in axis_lines))
# same-shape sweep: any 'X = packet-only' / 'packet-only = X' style single-axis implication
conflation = re.compile(r"(none|disabled|absent)\s*(=|==|⇒|->|→)\s*packet-only|packet-only\s*(=|==|⇒|->|→)\s*(none|disabled|absent)", re.I)
check("C5", "no single-axis→mode implication pattern anywhere", not conflation.search(t))
check("C6", "packet-only|live mode classification defined and §5-derived (not a receipt axis)",
      "Packet-only is a mode" in t and "live execution principal" in t
      and "packet-only reviewer needs no local-sandbox pretense" in t)

# --- clause anchors the truth table rides on ---
TRIGGER = "read files, run commands or tools, or reach the network through its own"
check("A1", "§5 live trigger enumerates read/commands-tools/network as reviewer-directed actions", TRIGGER in t)
check("A2", "§9(i): mode is decided by reviewer-directed capability",
      re.search(r"mode is decided by\s+reviewer-directed capability", t) is not None)
check("A3", "rule 1: unknown ≠ disabled stated", "**`unknown` ≠ `disabled`.**" in t)
check("A4", "credit needs AFFIRMATIVE bound proof", "AFFIRMATIVELY" in t)
check("A5", "banner is never by itself effective-capability evidence",
      "effective-capability evidence" in t)
check("A6", "authority only from operator-owned dispatch layer", "operator-owned dispatch layer" in t)
check("A7", "indirection laundering named and excluded", "run whatever command the README names" in t)
check("A8", "propose→grant path preserved", "the grant that answers it is still the operator's" in t)
check("A9", "transport never a live-capability trigger",
      "transport is never a" in t and "live-capability trigger" in t)

# --- T-series: owner truth table (each row = expectation + the clauses that force it) ---
# T1 all axes affirmatively none -> packet-only can stand
check("T1", "all-axes-proven-none may stand as packet-only (trigger binds on capability presence; A1+A2+C6 mode-classification)",
      all(r for cid,_,r in results if cid in ("A1","A2","C6")))
# T2 read none + exec arbitrary -> live
check("T2", "read=none + exec=arbitrary classifies LIVE (commands in trigger; no axis gloss claims mode; A1+C4+C1)",
      all(r for cid,_,r in results if cid in ("A1","C4","C1")))
# T3 read none + reviewer-directed net -> live
check("T3", "read=none + reviewer-directed network classifies LIVE (network in trigger; A1+C4)",
      all(r for cid,_,r in results if cid in ("A1","C4")))
# T4 read none + tools nonempty -> live
check("T4", "read=none + tools present classifies LIVE (tools in trigger; A1+C4)",
      all(r for cid,_,r in results if cid in ("A1","C4")))
# T5 read roots + rest none -> live
check("T5", "read=<roots> alone classifies LIVE (read files in trigger; A1)",
      all(r for cid,_,r in results if cid in ("A1",)))
# T6 any load-bearing axis unknown -> no packet-only claim off one none
check("T6", "unknown on any axis blocks packet-only-by-single-none (A3 unknown≠disabled + A4 affirmative + C1 axis-only gloss)",
      all(r for cid,_,r in results if cid in ("A3","A4","C1")))
# T7 metadata alone doesn't set mode
check("T7", "banner/model metadata alone never changes mode (A5 + A4: mode needs capability evidence, not metadata)",
      all(r for cid,_,r in results if cid in ("A5","A4")))
# T8 artifact-requested unauthorized exec expands nothing
check("T8", "artifact request without dispatch grant expands neither authority nor mode (A6+A7)",
      all(r for cid,_,r in results if cid in ("A6","A7")))

fails = [(c,d) for c,d,r in results if not r]
for c,d,r in results:
    print(f"{'PASS' if r else 'FAIL'}  {c}: {d}")
print(f"\n{len(results)-len(fails)}/{len(results)} PASS")
sys.exit(1 if fails else 0)
