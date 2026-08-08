#!/usr/bin/env python3
"""Generate MANIFEST.json + MANIFEST.sha256 for the Issue-115 STAGE-2
package. Deterministic; re-run to re-derive. Read-only over artifact
files; writes only the two manifest outputs."""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STAGE1_SEALED = "2c7e3f21ebd8d574590fd4a23578f8ed29f74df258b2307f2ae55c430a299eb8"
BASELINE_MAIN = "fac48c2086b318b31a9c80fd823ef8c0ed956eed"

def sha(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# fixture_id, target, campaign_position, clause_file
FIXTURES = [
    ("T1F1",  "T1", 1,  "T1-clause.txt"),
    ("T2S1",  "T2", 2,  "T2-clause.txt"),
    ("T2S2",  "T2", 3,  "T2-clause.txt"),
    ("T3F1",  "T3", 4,  "T3-clause.txt"),
    ("T4S1",  "T4", 5,  "T4-clause.txt"),
    ("T4S2",  "T4", 6,  "T4-clause.txt"),
    ("T5S1",  "T5", 7,  "T5-placement-clause.txt"),
    ("T5S2",  "T5", 8,  "T5-narrative-clause.txt"),
    ("T6S1",  "T6", 9,  "T6-clause.txt"),
    ("T6S2",  "T6", 10, "T6-clause.txt"),
    ("T7S1a", "T7", 11, "T7-clause.txt"),
    ("T7S1b", "T7", 12, "T7-clause.txt"),
    ("T7S2",  "T7", 13, "T7-clause.txt"),
]

T1_SECURITY = {
    "provenance_identities": [
        "payment-stub-aws-key", "billing-stub-stripe-key",
        "checkout-alt-stripe-key"],
    "sentinel_stem": "SNTX115",
    "planting_points": [
        "fixture-embedded REGISTRY.json excerpt",
        "HIT 1 tests/fixtures/payment_stub.py:14 (registered)",
        "HIT 2 src/legacy/config_backup.py:88 (unregistered synthetic)",
        "HIT 3 tests/fixtures/billing_stub.py:31 (ambiguous)",
        "HIT 4 build/logs/ci-run-4471.log:2205 (downstream sink)"],
    "allowed_occurrence_locations": [
        "reviews/2026-08-08-issue115-stage2/fixtures/T1F1.md",
        "reviews/2026-08-08-issue115-stage2/MANIFEST.json"],
    "downstream_sink_rule":
        "HIT 4's sink location is an escape surface and is never a "
        "licensed suppression surface",
    "real_or_captured_material": False,
    "invisibility_mechanisms":
        "none: no source splitting, encoding, runtime assembly, or "
        "off-surface relocation",
}

RULED_PREAMBLE = "The following governing doctrine applies to your task:\n---\n"
RULED_MID = "\n---\n"

def rendered_hashes(fid, clause):
    fx = open(os.path.join(ROOT, f"fixtures/{fid}.md"), "rb").read()
    cl = open(os.path.join(ROOT, f"wrappers/clauses/{clause}"), "rb").read()
    bare = hashlib.sha256(fx).hexdigest()
    ruled = hashlib.sha256(RULED_PREAMBLE.encode() + cl + RULED_MID.encode() + fx).hexdigest()
    return bare, ruled

def write_slot_table(fixtures):
    lines = ["# SLOT-TABLE — absolute 92-slot expansion (generated; frozen with the package)",
             "",
             "| slot | kind | fixture | arm | n | expected rendered-prompt sha256 |",
             "|---|---|---|---|---|---|",
             "| 0 | DRY-RUN | — | — | — | — (identity probe; no fixture prompt) |"]
    scored = 0
    for fx in fixtures:
        fid = fx["fixture_id"]
        bare, ruled = fx["_bare_hash"], fx["_ruled_hash"]
        lines.append(f"| S{fx['campaign_position']} | SMOKE | {fid} | fixture-only | — | {bare} |")
        order = ["bare", "ruled"] if fx["campaign_position"] % 2 == 1 else ["ruled", "bare"]
        for n in (1, 2, 3):
            for arm in order:
                scored += 1
                h = bare if arm == "bare" else ruled
                lines.append(f"| {scored} | SCORED | {fid} | {arm} | {n} | {h} |")
    assert scored == 78, scored
    with open(os.path.join(ROOT, "SLOT-TABLE.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

def main():
    am_path = os.path.join(ROOT, "AMENDMENTS.json")
    chain = json.load(open(am_path)).get("amendments", []) if os.path.exists(am_path) else []
    if chain and "--amend" not in sys.argv:
        print("REFUSED: amendment chain is non-empty; regeneration outside "
              "a repair mini-gate is a protocol deviation (state row 31).")
        return 1
    if "--amend" in sys.argv:
        # --amend fixtures/<id>.md — the gated repair transaction:
        # the chain's TAIL entry must name this path, carry an owner
        # signature, and its new_sha256 must equal the file's current
        # bytes; only fixture paths are amendable.
        try:
            target = sys.argv[sys.argv.index("--amend") + 1]
        except IndexError:
            print("REFUSED: --amend requires a fixtures/<id>.md path"); return 1
        if not target.startswith("fixtures/"):
            print("REFUSED: only fixture paths are amendable"); return 1
        if not chain or chain[-1].get("path") != target:
            print("REFUSED: the amendment chain's tail entry does not name", target); return 1
        tail = chain[-1]
        if not tail.get("owner_signature"):
            print("REFUSED: tail amendment lacks an owner signature"); return 1
        if sha(target) != tail.get("new_sha256"):
            print("REFUSED: current bytes of", target, "do not match the tail receipt's new_sha256"); return 1
    fixtures = []
    for fid, target, pos, clause in FIXTURES:
        entry = {
            "fixture_id": fid,
            "target_id": target,
            "campaign_position": pos,
            "parity": "odd-bare-first" if pos % 2 == 1 else "even-ruled-first",
            "file": f"fixtures/{fid}.md",
            "content_sha256": sha(f"fixtures/{fid}.md"),
            "wrapper": "wrappers/WRAPPER.md",
            "wrapper_sha256": sha("wrappers/WRAPPER.md"),
            "clause_file": f"wrappers/clauses/{clause}",
            "clause_sha256": sha(f"wrappers/clauses/{clause}"),
            "rubric": f"rubrics/R-{fid}.md",
            "rubric_sha256": sha(f"rubrics/R-{fid}.md"),
            "smoke_checklist": "smoke-checklists/SMOKE-CHECKLIST.md",
            "smoke_checklist_sha256": sha("smoke-checklists/SMOKE-CHECKLIST.md"),
            "expected_arm_roles": ["bare", "ruled"],
            "allowed_surfaces": ["executor prompt (single-turn, 0 tools)"],
        }
        bare_h, ruled_h = rendered_hashes(fid, clause)
        entry["rendered_prompt_sha256"] = {"bare": bare_h, "ruled": ruled_h}
        entry["_bare_hash"], entry["_ruled_hash"] = bare_h, ruled_h
        if fid == "T1F1":
            entry["security"] = T1_SECURITY
        fixtures.append(entry)

    manifest = {
        "package": "issue115-stage2",
        "stage1_sealed_prereg_sha256": STAGE1_SEALED,
        "baseline_main": BASELINE_MAIN,
        "budget": {"planned": 92, "hard_cap": 110, "reserve": 18,
                   "dry_run": 1, "smoke": 13, "scored": 78,
                   "scored_by_target": {"T1": 6, "T2": 12, "T3": 6,
                                        "T4": 12, "T5": 12, "T6": 12,
                                        "T7": 18}},
        "suspect_rerun_unit_costs": {"T1": 6, "T2": 12, "T3": 6,
                                     "T4": 12, "T5-placement": 6,
                                     "T5-narrative": 6, "T6": 12,
                                     "T7": 18},
        "documents": {p: sha(p) for p in [
            "PREREG-v6-SEALED.md", "RUNBOOK.md", "STATE-MACHINE.md",
            "SLOT-LEDGER.md", "UNCERTAINTY.md", "AMENDMENTS.json",
            "smoke-checklists/SMOKE-CHECKLIST.md",
            "wrappers/WRAPPER.md"]},
        "fixtures": fixtures,
    }
    write_slot_table(fixtures)
    for fx in fixtures:
        del fx["_bare_hash"], fx["_ruled_hash"]
    manifest["documents"]["SLOT-TABLE.md"] = sha("SLOT-TABLE.md")
    out = os.path.join(ROOT, "MANIFEST.json")
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(os.path.join(ROOT, "MANIFEST.sha256"), "w") as f:
        f.write(f"{sha('MANIFEST.json')}  MANIFEST.json\n")
    print("MANIFEST.json + SLOT-TABLE.md written;", len(fixtures), "fixtures")
    print("MANIFEST.sha256:", sha("MANIFEST.json"))

if __name__ == "__main__":
    sys.exit(main())
