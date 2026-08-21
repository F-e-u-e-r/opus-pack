#!/usr/bin/env python3
"""Landing gate for the issue-115 tracker closure-state record.

Every value CLOSURE-STATE.md cites is re-derived from the repository and
from the authenticated API and compared against the frozen RECEIPTS.json —
nothing in the record is trusted because it was written down. On top of the
value checks this gate asserts the four semantic invariants the record
exists to establish (B-E terminal, A standing, T2 routing terminated
without a marker promotion, the two T4 identities kept apart), each with a
mutant control proving the invariant can fail.

Read-only. Exits non-zero on any failure."""
import glob, hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
BASELINE_MAIN = "dd052c46b27bdebb8378aa21adeab4902bc54bd6"
FAILURES = []
SKIPPED = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" - " + str(detail)) if not ok and detail else ""))
    if not ok:
        FAILURES.append(name)


def mutant(name, predicate, original, mutated):
    """A mutant control is only evidence if it is NOT vacuous: the edit must
    actually have applied, the predicate must hold on the real input, and it
    must fail on the mutated one. A needle that no longer matches the record
    would otherwise make a mutant 'pass' while testing nothing."""
    applied = mutated != original
    holds = predicate(original)
    trips = not predicate(mutated)
    check("[mutant] " + name, applied and holds and trips,
          f"applied={applied} holds_on_real={holds} trips_on_mutant={trips}")


def skip(name, why):
    print("SKIP  " + name + " - " + why)
    SKIPPED.append(name)


def flatten(text):
    """Strip blockquote/list markers, THEN whitespace-normalise - a wrapped
    or marker-prefixed phrase is invisible to a line-bounded comparison."""
    return re.sub(r"\s+", " ", re.sub(r"^\s*[>|-]\s?", "", text, flags=re.M))


def norm(s):
    return re.sub(r"\s+", " ", " ".join(l.strip() for l in s.split("\n"))).strip()


def debullet(s):
    return re.sub(r"^(?:[-*+]\s+)", "", s)


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout.strip()


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None


def rf(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()


R = json.load(open(os.path.join(ROOT, "RECEIPTS.json")))
DOC_RAW = open(os.path.join(ROOT, "CLOSURE-STATE.md"), encoding="utf-8").read()
DOC = flatten(DOC_RAW)

# Section-scoped views: an invariant about section D must not be satisfiable
# by wording that lives in section A.
SECTIONS = {}
for m in re.finditer(r"^## (\d+)\.[^\n]*\n(.*?)(?=^## |\Z)", DOC_RAW, re.S | re.M):
    SECTIONS[m.group(1)] = flatten(m.group(2))
SEC_A = SECTIONS.get("2", "")
SEC_BCDE = " ".join(SECTIONS.get(n, "") for n in ("3", "4", "5", "6"))
SEC_GUARDS = SECTIONS.get("8", "")
check("the record's section map parsed (A, B-E and the guards are all non-empty)",
      bool(SEC_A) and bool(SEC_BCDE) and bool(SEC_GUARDS) and len(SECTIONS) == 10, sorted(SECTIONS))

# ---- 1. Baseline and zero-mutation boundary --------------------------------
check("RECEIPTS.json baseline main matches the branch's merge base",
      R["main"] == BASELINE_MAIN and git("merge-base", "--is-ancestor", BASELINE_MAIN, "HEAD") == "",
      R["main"])
mutated = git("diff", "--name-only", BASELINE_MAIN, "--", "skills", "metadata", ".github",
              "README.md", "README.zh-Hant.md")
check("zero mutation: no skill, marker, doctrine, metadata or CI byte changed", mutated == "", mutated[:300])
hist = git("diff", "--name-only", BASELINE_MAIN, "--", "reviews")
new_only = [p for p in hist.splitlines() if p.strip()]
check("no historical review package touched (additions only, inside this record's dir)",
      all(p.startswith("reviews/2026-08-16-issue115-closure-state/") for p in new_only), new_only[:5])

# ---- 2. Historical artifacts pinned byte-unchanged --------------------------
for rel, blob in R["blobs"].items():
    check(f"blob unchanged: {rel}", git("rev-parse", f"HEAD:{rel}") == blob, git("rev-parse", f"HEAD:{rel}"))
check("PR #185 closure assessment is pinned, not edited by this record",
      git("rev-parse", "HEAD:reviews/2026-08-13-issue115-campaign-synthesis/CLOSURE-ASSESSMENT.md")
      == R["blobs"]["reviews/2026-08-13-issue115-campaign-synthesis/CLOSURE-ASSESSMENT.md"])
check("the record describes #185 as scope-limited, never as mistaken",
      "evidence-scope incomplete for tracker-wide closure adjudication" in DOC
      and "not corrected, not contradicted, and not modified" in DOC
      and not re.search(r"#185 (was |is )?(wrong|incorrect|mistaken|in error)", DOC, re.I))

# ---- 3. Section B: identity join, outcomes, settlement split ----------------
T = json.load(open(os.path.join(REPO, "reviews/2026-08-04-round5-targets.json")))
MARK = re.compile(r"\(\s*`?(unprobed|probed in part)`?\s*[—-]", re.I)


def derive_b():
    """Relocate each round-5 target heading in current main under the
    manifest's own normalisation and read that rule's marker state."""
    out = {}
    for t in T["targets"]:
        lines = rf(t["path"]).split("\n")
        nh, start = norm(t["heading"]), None
        for i in range(len(lines)):
            if not lines[i].strip():
                continue
            for w in (1, 2, 3, 4, 5):
                win = norm("\n".join(lines[i:i + w]))
                if win.startswith(nh) or debullet(win).startswith(nh):
                    start = i
                    break
            if start is not None:
                break
        if start is None:
            out[t["id"]] = {"path": t["path"], "heading_line": None, "marker": "HEADING-NOT-RELOCATED"}
            continue
        end, sec = len(lines), t["heading"].lstrip().startswith("#")
        for j in range(start + 1, len(lines)):
            if re.match(r"^#{2,4} ", lines[j]) or (not sec and re.match(r"^- \*\*", lines[j])):
                end = j
                break
        m = MARK.search(norm("\n".join(lines[start:end])))
        out[t["id"]] = {"path": t["path"], "heading_line": start + 1,
                        "marker": m.group(1).lower() if m else "NONE"}
    return out


def b_join_ok(derived, receipts):
    """The join is by target IDENTITY, not by count: every manifest id must
    relocate AND carry the marker state the receipts froze."""
    if set(derived) != set(receipts):
        return False
    return all(derived[k]["marker"] == receipts[k]["marker"]
               and derived[k]["heading_line"] == receipts[k]["heading_line"]
               and derived[k]["marker"] != "HEADING-NOT-RELOCATED" for k in derived)


B = derive_b()
check("round-5 manifest declares the section-B work-list (issues 110/111, index #114, 10 targets)",
      T["source_issues"] == [110, 111] and T["work_list_index"] == "#114" and T["target_count"] == 10)
check("section-B identity join: 10/10 targets relocate in current main with the frozen marker state",
      b_join_ok(B, R["B_targets"]) and len(B) == 10, sorted(B))
split = {"path1_probed_in_part": sum(1 for v in B.values() if v["marker"] == "probed in part"),
         "path3_unprobed": sum(1 for v in B.values() if v["marker"] == "unprobed")}
check("section-B settlement split is 3 path-1 / 7 path-3",
      split == R["B_split"] == {"path1_probed_in_part": 3, "path3_unprobed": 7}, split)
rs = flatten(rf("reviews/2026-08-04-round5-results/RESULT-SUMMARY.md"))
check("round-5 ledger records 3 SUPPORT and 7 UNCHANGED outcomes",
      rs.count("| **SUPPORT**") == 3 and rs.count("| UNCHANGED |") == 7,
      f"support={rs.count('| **SUPPORT**')} unchanged={rs.count('| UNCHANGED |')}")

# ---- 4. Section C: 11 identities and their lineage --------------------------
bodies = {}


def body(rel):
    if rel not in bodies:
        bodies[rel] = re.sub(r"\s+", " ", rf(rel))
    return bodies[rel]


c_present = {n: (re.sub(r"\s+", " ", v["anchor"]) in body(v["path"])) for n, v in R["C_items"].items()}
check("section-C identity join: 11/11 candidate anchors present in current main",
      len(c_present) == 11 and all(c_present.values()),
      [n for n, ok in c_present.items() if not ok])
lineage = sorted(f for f in git("ls-files", "skills").split()
                 if f.endswith(".md") and "#112, triaged under #115 Phase 1" in re.sub(r"\s+", " ", rf(f)))
check("section-C lineage: the #112 -> #115 Phase 1 provenance string is carried by the recorded files",
      lineage == R["C_lineage_files"] and len(lineage) == 5, lineage)
check("the shared surface between candidate 9 and the T2 amendment is recorded",
      "candidate 9's external-systems entry is the same entry the T2 chain amended" in DOC
      and "double-counted" in DOC)

# ---- 5. T2 chain and routing termination -----------------------------------
for n in ("189", "190", "191", "192", "193"):
    live = gh(f"repos/F-e-u-e-r/opus-pack/pulls/{n}")
    check(f"T2 chain PR #{n} merged, merge commit matches receipts",
          live is not None and live["merged"] is True
          and live["merge_commit_sha"] == R["prs"][n]["merge_commit_sha"],
          (live or {}).get("merge_commit_sha"))
ext = re.sub(r"\s+", " ", rf("skills/operational-rigor/references/external-systems.md"))
check("the T2 doctrine amendment sentence is present in canonical doctrine",
      "read-back precedes any separate provider-side liveness/status read" in ext
      and R["T2_amendment_present"] is True)


def t2_routing_ok(doc):
    """Routing terminated, AND no resurrection of the superseded routing as
    a live obligation, AND no marker promotion smuggled in with it."""
    terminated = ("T2 routing state: TERMINATED" in doc
                  and "no outstanding t2 execution obligation" in doc.lower())
    no_marker_promo = ("the T2 **marker** is not upgraded by this record" in doc
                       or "the T2 marker is not upgraded by this record" in doc)
    live_words = r"(T2[^.]{0,80}(remains|still)[^.]{0,40}`?NEEDS-NEW-PROBE`?" \
                 r"|`?NEEDS-NEW-PROBE`?[^.]{0,60}(remains|is still) (open|live|outstanding|in force))"
    no_resurrection = re.search(live_words, doc, re.I) is None
    return terminated and no_marker_promo and no_resurrection


check("T2 routing recorded as TERMINATED, with no marker promotion and no stale-routing resurrection",
      t2_routing_ok(DOC))
check("T2 marker settlement stated as path 3 with the marker left unprobed",
      "path 3, in-body marker `unprobed`, bytes untouched" in DOC)
live204 = gh("repos/F-e-u-e-r/opus-pack/pulls/204")
check("T5-placement terminal disposition PR #204 merged, merge commit matches receipts",
      live204 is not None and live204["merged"] is True
      and live204["merge_commit_sha"] == R["prs"]["204"]["merge_commit_sha"])
check("the T5-placement terminal record is cited as the completed form, not re-adjudicated",
      "RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)" in DOC and "No action is owed here" in DOC)

# ---- 6. Section D: exact terminal classification ---------------------------
check("section D carries the exact owner-adjudicated classification token",
      "`FAILURE-NOT-REPRODUCIBLE / ALL-REGISTERED-HYPOTHESES-FALSIFIED`" in DOC)
check("both downstream landing branches are marked NOT APPLICABLE with their shared premise named",
      "NOT APPLICABLE" in SECTIONS.get("5", "")
      and "They share one premise" in DOC and "falsified it" in DOC)
check("section D is not framed as a stale premise",
      "This is **not** a stale premise" in DOC
      and "was a real observation when it was recorded" in DOC)
check("section D records the recurrence procedure rather than closing the door",
      "the three-experiment procedure re-runs against the failing state" in DOC)

# ---- 7. Section E: contract assertions and durability honesty --------------
E = SECTIONS.get("6", "")
for phrase, label in (("resolves in exactly one place", "single resolution point"),
                      ("no default", "fail-closed, no default"),
                      ("canonicalised before any containment judgement", "canonicalisation before judgement"),
                      ("derived from the script location", "deny-roots derived not hardcoded"),
                      ("refused at launch", "repo-internal-root policy decided"),
                      ("**11/11 PASS**", "positive suite result"),
                      ("**10 FAIL / 1 PASS**", "pre-fix control result"),
                      ("demonstrably able to fail", "suite falsifiability stated")):
    check(f"section E asserts: {label}", phrase in E)
check("section E labels the harness evidence local, untracked and git-ignored",
      "git-ignored by design" in E and "local, untracked artifacts" in E
      and "They are not\nrepository bytes" in DOC_RAW.replace("\r", ""))
check("RECEIPTS.json marks the harness hashes as local-untracked, not as repo blobs",
      R["E_local_untracked"]["gitignored"] is True
      and all(k not in R["blobs"] for k in ("evals/round4/run4.sh", "evals/round4/run4.sh.pre-0a.bak")))
check("the harness really is untracked (the durability claim is verified, not asserted)",
      git("ls-files", "evals") == "")
harness = os.path.join(REPO, "evals/round4/harness/test_sandbox_root.sh")
subject = os.path.join(REPO, "evals/round4/run4.sh")
if os.path.exists(harness) and os.path.exists(subject):
    got = hashlib.sha256(open(subject, "rb").read()).hexdigest()
    check("local run4.sh sha256 matches the frozen receipt", got == R["E_local_untracked"]["run4_sh_sha256"], got)
    r = subprocess.run(["bash", harness, subject], capture_output=True, text=True, cwd=REPO)
    npass = len([l for l in r.stdout.splitlines() if l.startswith("PASS: ")])
    nfail = len([l for l in r.stdout.splitlines() if l.startswith("FAIL: ")])
    check("section E contract suite re-run: 11/11 PASS, exit 0",
          r.returncode == 0 and npass == 11 and nfail == 0, f"exit={r.returncode} pass={npass} fail={nfail}")
else:
    skip("section E contract suite re-run", "local git-ignored harness absent (expected off this machine)")

# ---- 8. Section statuses and the lifecycle statement ------------------------
def section_status_ok(sec_bcde, sec_a):
    """B-E terminal and free of STILL-OPEN; A never terminal/closed."""
    bcde = ("STILL-OPEN" not in sec_bcde) and sec_bcde.count("status: **TERMINAL.**") == 4
    a_ok = ("STILL-OPEN (BY DESIGN)" in sec_a
            and not re.search(r"Section A[^.]{0,60}(TERMINAL|CLOSED|SATISFIED)", sec_a, re.I))
    return bcde and a_ok


check("sections B, C, D and E are each stated TERMINAL and none carries STILL-OPEN",
      section_status_ok(SEC_BCDE, SEC_A))
check("section A is stated STILL-OPEN (BY DESIGN) and never terminal, closed or satisfied",
      "STILL-OPEN (BY DESIGN)" in SEC_A
      and not re.search(r"Section A[^.]{0,60}(TERMINAL|CLOSED|SATISFIED)", SEC_A, re.I))


LIFECYCLE = ("Sections B–E are terminal. Section A remains an intentionally open "
             "standing queue. Therefore #115 remains OPEN by design; its OPEN state "
             "must not be interpreted as unfinished B–E remediation.")


def lifecycle_ok(raw):
    """The one sentence a future reader must not be able to invert: pinned
    whole, so flipping any clause of it fails rather than partially matching."""
    return LIFECYCLE in flatten(raw)


check("the tracker lifecycle statement is present and complete, verbatim", lifecycle_ok(DOC_RAW))
check("closing #115 is described as re-architecture, not record repair",
      "re-architecting the tracker" in DOC and "not a repair of its records" in DOC)
check("the record does not edit, comment on or close the issue",
      "does not edit, comment on, or close issue #115" in DOC)
iss = gh("repos/F-e-u-e-r/opus-pack/issues/115")
check("#115 is still OPEN at gate time", iss is not None and iss["state"] == "open",
      (iss or {}).get("state"))
check("stale related-debt metadata (#104/#105) recorded as carrying no obligation",
      "carrying no obligation" in DOC)

# ---- 9. Namespace guards ---------------------------------------------------
def t4_guard_ok(guards):
    """Both T4 identities named with their distinct owning skills."""
    return ("subprocess-environment-minimisation" in guards
            and "cross-model-review environment-bound severity" in guards
            and "must never be joined on the bare label" in guards)


def unprobed_semantics_ok(doc):
    """Both clauses are pinned WITH their negation, so a flipped sentence
    fails instead of still matching a negation-free fragment."""
    return ("An `unprobed` marker does **not** by itself denote an outstanding "
            "execution obligation." in doc
            and "No count of `unprobed` occurrences may be translated into a count "
                "of owed probes." in doc)


check("both T4 identities are distinguished by owning skill and campaign", t4_guard_ok(SEC_GUARDS))
check("`unprobed` is defined as taxonomy, never as an outstanding execution obligation",
      unprobed_semantics_ok(DOC))

# ---- 10. Section A surface counts re-derived --------------------------------
occ = ib = files = 0
for f in sorted(glob.glob(os.path.join(REPO, "skills", "**", "*.md"), recursive=True)):
    s = open(f, encoding="utf-8").read()
    o = len(re.findall(r"unprobed", s))
    if o:
        files += 1
        occ += o
        ib += len(re.findall(r"\(\s*`unprobed`\s*[—-]", s))
check("section-A marker surface re-derives to the frozen receipt",
      {"occurrences": occ, "files": files, "in_body_markers": ib}
      == {k: R["A_surface"][k] for k in ("occurrences", "files", "in_body_markers")},
      f"{occ}/{files}/{ib}")
check("the record cites the measured surface and the issue's own earlier snapshot",
      f"{occ} `unprobed` grep occurrences across {files}" in DOC and "161 occurrences across 11 files" in DOC)
body115 = flatten((gh("repos/F-e-u-e-r/opus-pack/issues/115") or {}).get("body", ""))
check("the cited 161/11 snapshot is the issue's own recorded figure, not a transcription",
      "11 files, total 161" in body115 and "Snapshot at 097a253" in body115)
check("the record's account of #185 separates accurate observations from over-general verdicts",
      "observations are accurate**" in DOC and "verdicts are stated tracker-wide**" in DOC
      and "generalises past what that surface could settle" in DOC)
check("the gate is honest about what it does not re-run",
      "does not re-run this control, and says" in DOC)
check("the record separates first-hand re-verification from record-based sections",
      "Evidence-basis note" in DOC
      and "Section D is the one section whose underlying experiments were not re-executed here" in DOC
      and "does not claim to have performed" in DOC)

# ---- 11. Mutant controls: every invariant must be able to FAIL ---------------
_m1 = {k: dict(v) for k, v in B.items()}
_m1[sorted(_m1)[0]]["marker"] = "probed in part"
mutant("a single flipped marker state breaks the section-B identity join",
       lambda d: b_join_ok(d, R["B_targets"]), B, _m1)
_m2 = {k: dict(v) for k, v in B.items()}
_m2.pop(sorted(_m2)[0])
mutant("a dropped target breaks the join even though the remaining rows all match",
       lambda d: b_join_ok(d, R["B_targets"]), B, _m2)
mutant("inverting the lifecycle statement trips the lifecycle check", lifecycle_ok, DOC_RAW,
       DOC_RAW.replace("#115 remains OPEN by design", "#115 is now closeable", 1))
mutant("weakening the T4 guard trips the collision check", t4_guard_ok, SEC_GUARDS,
       SEC_GUARDS.replace("must never be joined on the bare label", "may be joined on the label", 1))
mutant("resurrecting the superseded T2 routing as live trips the routing check",
       t2_routing_ok, DOC,
       DOC + " The T2 concern still remains NEEDS-NEW-PROBE pending a further probe.")
mutant("smuggling a marker promotion into the T2 routing record trips the routing check",
       t2_routing_ok, DOC,
       DOC.replace("the T2 **marker** is not upgraded by this record",
                   "the T2 marker is accordingly promoted to probed in part", 1))
mutant("regressing one B-E section to STILL-OPEN trips the status check",
       lambda s: section_status_ok(s, SEC_A), SEC_BCDE,
       SEC_BCDE.replace("Section C status: **TERMINAL.**", "Section C status: **STILL-OPEN.**", 1))
mutant("declaring Section A terminal trips the status check",
       lambda s: section_status_ok(SEC_BCDE, s), SEC_A,
       SEC_A.replace("**STILL-OPEN (BY DESIGN)**", "**TERMINAL**", 1))
mutant("equating `unprobed` with outstanding execution trips the semantics check",
       unprobed_semantics_ok, DOC,
       DOC.replace("No count of `unprobed` occurrences may be translated into a count of owed probes.",
                   "Every `unprobed` occurrence is one owed probe.", 1))
mutant("dropping the shared-premise reasoning from section D trips its check",
       lambda d: "They share one premise" in d and "falsified it" in d, DOC,
       DOC.replace("They share one premise", "They are unrelated", 1))

print()
if SKIPPED:
    print("SKIPPED (declared, not counted as PASS):", SKIPPED)
if FAILURES:
    print("CLOSURE-STATE CHECKS: FAIL -", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("CLOSURE-STATE CHECKS: ALL PASS")
