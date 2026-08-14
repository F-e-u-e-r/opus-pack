#!/usr/bin/env python3
"""Generate MANIFEST.json + MANIFEST.sha256 + SLOT-TABLE.md for the
issue115-t5pprobe-v1 prereg package. Deterministic; re-run to
re-derive. Read-only over artifact files; writes only the three
generated outputs.

Same immutability model as issue115-stage2-v1 / issue115-t2probe-v1:
once an OWNER-APPROVAL.json binds this package id as APPROVED,
regeneration is refused — a new version means a new PACKAGE_ID."""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ID = "issue115-t5pprobe-v1"
BASELINE_MAIN = "c2fc127d7d2d6263439094553e4a6aa1575eeaee"
DOCTRINE_BLOB = "caa2bcb5832fa5fe688763e97cdc1e6ff99317d4"
SEALED_DOCTRINE_BLOB = "e49c7d9f782d628758db59d5207d9185884e46fa"
SEALED_STAGE2_DIR = "../2026-08-08-issue115-stage2"

def sha_path(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def read(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return f.read()

PREAMBLE = b"The following governing doctrine applies to your task:\n---\n"
MID = b"\n---\n"
ADD_SEP = b"\n"  # clause file ends with \n; one more \n = one blank line

# fixture_id, campaign_position, rubric file
FIXTURES = [("P1", 1, "rubrics/R-P1.md"), ("P2", 2, "rubrics/R-P2.md")]

# Preregistered arm rotation (six rounds of three slots per fixture).
ROUNDS = {
    "P1": [("B","C","E"),("C","E","B"),("E","B","C"),
           ("B","C","E"),("C","E","B"),("E","B","C")],
    "P2": [("E","C","B"),("B","E","C"),("C","B","E"),
           ("E","C","B"),("B","E","C"),("C","B","E")],
}

def rendered_bytes(fid):
    fx = read(f"fixtures/{fid}.md")
    cl = read("wrappers/clauses/CURRENT-clause.txt")
    add = read("wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt")
    b = fx
    c = PREAMBLE + cl + MID + fx
    e = PREAMBLE + cl + ADD_SEP + add + MID + fx
    return {"B": b, "C": c, "E": e}

def rendered(fid):
    return {k: hashlib.sha256(v).hexdigest()
            for k, v in rendered_bytes(fid).items()}

def write_slot_table(fixture_entries):
    lines = ["# SLOT-TABLE — absolute 39-slot expansion (generated; frozen with the package)",
             "",
             "| slot | kind | fixture | arm | n | expected rendered-prompt sha256 |",
             "|---|---|---|---|---|---|",
             "| 0 | DRY-RUN | — | — | — | — (identity probe; no fixture prompt) |"]
    scored = 0
    for fx in fixture_entries:
        fid = fx["fixture_id"]
        h = fx["rendered_prompt_sha256"]
        lines.append(f"| S{fx['campaign_position']} | SMOKE | {fid} | fixture-only | — | {h['B']} |")
        seen = {"B": 0, "C": 0, "E": 0}
        for rnd in ROUNDS[fid]:
            for arm in rnd:
                scored += 1
                seen[arm] += 1
                lines.append(f"| {scored} | SCORED | {fid} | {arm} | {seen[arm]} | {h[arm]} |")
        assert all(v == 6 for v in seen.values()), (fid, seen)
    assert scored == 36, scored
    with open(os.path.join(ROOT, "SLOT-TABLE.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

def main():
    ap_path = os.path.join(ROOT, "OWNER-APPROVAL.json")
    if os.path.exists(ap_path):
        ap = json.load(open(ap_path))
        if (ap.get("status") == "APPROVED"
                and ap.get("package_id") == PACKAGE_ID):
            print("REFUSED: package version", PACKAGE_ID, "is owner-approved "
                  "and immutable; author a NEW version instead.")
            return 1
    entries = []
    for fid, pos, rubric in FIXTURES:
        entries.append({
            "fixture_id": fid,
            "campaign_position": pos,
            "file": f"fixtures/{fid}.md",
            "content_sha256": sha_path(f"fixtures/{fid}.md"),
            "wrapper": "wrappers/WRAPPER.md",
            "wrapper_sha256": sha_path("wrappers/WRAPPER.md"),
            "clause_file": "wrappers/clauses/CURRENT-clause.txt",
            "clause_sha256": sha_path("wrappers/clauses/CURRENT-clause.txt"),
            "addendum_file": "wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt",
            "addendum_sha256": sha_path("wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt"),
            "rubric": rubric,
            "rubric_sha256": sha_path(rubric),
            "predicate": "rubrics/OWNERSHIP-PREDICATE.md",
            "predicate_sha256": sha_path("rubrics/OWNERSHIP-PREDICATE.md"),
            "expected_arm_roles": ["B", "C", "E"],
            "rounds": [list(r) for r in ROUNDS[fid]],
            "allowed_surfaces": ["executor prompt (single-turn, 0 tools)"],
            "rendered_prompt_sha256": rendered(fid),
        })
    manifest = {
        "package_id": PACKAGE_ID,
        "status": "PROPOSAL — design gate only; no execution authorized",
        "baseline_main": BASELINE_MAIN,
        "doctrine_file": "skills/skill-authoring/SKILL.md",
        "doctrine_blob_sha1": DOCTRINE_BLOB,
        "sealed_campaign_doctrine_blob_sha1": SEALED_DOCTRINE_BLOB,
        "probed_clause_pin": {
            "clause_sha256": sha_path("wrappers/clauses/CURRENT-clause.txt"),
            "note": "clause-level pin is load-bearing; the containing "
                    "file blob changed between the sealed campaign and "
                    "this baseline while the clause bytes did not "
                    "(machine-checked by static_checks.py)",
        },
        "sealed_anchors": {
            "T5S1_content_sha256": sha_path("fixtures/P1.md"),
            "T5_placement_clause_sha256":
                sha_path("wrappers/clauses/CURRENT-clause.txt"),
            "R_T5S1_rubric_sha256":
                sha_path(os.path.join(SEALED_STAGE2_DIR,
                                      "rubrics/R-T5S1.md")),
            "note": "P1.md and CURRENT-clause.txt are byte-identical "
                    "copies of the sealed issue115-stage2-v1 files; "
                    "equality machine-checked by static_checks.py",
        },
        "budget": {"planned": 39, "hard_cap": 50,
                   "dry_run": 1, "smoke": 2, "scored": 36,
                   "contingency_headroom": 11,
                   "stage2_reserve_18": "NOT USED — locked, untouched",
                   "t2probe_headroom_11": "NOT USED — closed, untouched"},
        "documents": {p: sha_path(p) for p in [
            "T5P-PROBE-PREREG-v1.md", "SMOKE-CHECKLIST.md",
            "rubrics/OWNERSHIP-PREDICATE.md", "rubrics/R-P1.md",
            "rubrics/R-P2.md", "wrappers/WRAPPER.md",
            "make_manifest.py", "static_checks.py"]},
        "fixtures": entries,
    }
    write_slot_table(entries)
    manifest["documents"]["SLOT-TABLE.md"] = sha_path("SLOT-TABLE.md")
    with open(os.path.join(ROOT, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(os.path.join(ROOT, "MANIFEST.sha256"), "w") as f:
        f.write(f"{sha_path('MANIFEST.json')}  MANIFEST.json\n")
    print("MANIFEST.json + SLOT-TABLE.md written;", len(entries), "fixtures")
    print("MANIFEST.sha256:", sha_path("MANIFEST.json"))

if __name__ == "__main__":
    sys.exit(main())
