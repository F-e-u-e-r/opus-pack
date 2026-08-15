#!/usr/bin/env python3
"""Mechanical checks for the T5-placement concern disposition.

Every claim in DISPOSITION.md is re-derived from durable artifacts and
from git, never from a session narrative. Read-only; exits non-zero on
any failure."""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
SCORED = os.path.join(REPO, "reviews", "2026-08-15-issue115-t5p-scored")
PREREG = os.path.join(REPO, "reviews", "2026-08-14-issue115-t5-placement-probe-prereg")
SEALED_T5 = os.path.join(REPO, "reviews", "2026-08-09-issue115-scored-t5")
DOCTRINE = "skills/skill-authoring/SKILL.md"
PRE_DISPOSITION_MAIN = "66d9144a7cb49714cb2132280161c16b47924d96"   # #203 merge
FAILURES = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if not ok and detail else ""))
    if not ok:
        FAILURES.append(name)

def rd(p):
    with open(p, "rb") as f:
        return f.read()

def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout.strip()

def flatten(text):
    """Strip blockquote and list markers, THEN whitespace-normalise.
    Recurring trap this session (four times): a line-bounded or
    naively-normalised comparison cannot see a phrase that wraps across
    source lines or carries a leading `> ` / `- ` marker. Every textual
    assertion in this file goes through here."""
    text = re.sub(r"^\s*[>|-]\s?", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text)

DOC = flatten(rd(os.path.join(ROOT, "DISPOSITION.md")).decode())

# ---- 1. The scored result this disposition rests on, re-derived ----
grid = json.load(open(os.path.join(SCORED, "SCORED-GRID.json")))
outcome = json.load(open(os.path.join(SCORED, "SCORED-OUTCOME.json")))
adj = json.load(open(os.path.join(SCORED, "BLIND-ADJUDICATION.json")))
sealed_map = json.load(open(os.path.join(SCORED, "SEALED-ARM-MAP.json")))
re_grid = {}
for fx in ("P1", "P2"):
    for arm in "BCE":
        obs = [o for o in adj if adj[o]["fixture"] == fx and sealed_map[o]["arm"] == arm]
        re_grid[f"{fx}/{arm}"] = sum(1 for o in obs if adj[o]["primary_class"] == "PASS-OWNER")
check("grid recomputes to P1 = 0/2/4",
      [re_grid[f"P1/{a}"] for a in "BCE"] == [0, 2, 4], [re_grid[f"P1/{a}"] for a in "BCE"])
check("grid recomputes to P2 = 0/3/1",
      [re_grid[f"P2/{a}"] for a in "BCE"] == [0, 3, 1], [re_grid[f"P2/{a}"] for a in "BCE"])
check("recorded grid agrees with the recomputation",
      all(grid["grid"][k]["pass"] == v for k, v in re_grid.items()))
check("outcome is exactly INCONCLUSIVE(MIXED-P1+MIXED-P2)",
      outcome["outcome"] == "INCONCLUSIVE(MIXED-P1+MIXED-P2)", outcome["outcome"])
check("H1/H2/H3 recorded as undecided",
      "NONE" in outcome["hypothesis_disposition"] and outcome["ungradable_total"] == 0)
check("disposition quotes the outcome verbatim",
      "INCONCLUSIVE(MIXED-P1+MIXED-P2)" in DOC)

# ---- 2. The disposition's own semantics ----
for phrase in ("RETAIN-CONCERN-ONLY (PROBE-INCONCLUSIVE)",
               "did not distinguish H1, H2, or H3",
               "supports no doctrine recommendation",
               "execution obligation is therefore satisfied",
               "underlying concern remains unresolved",
               "Section-A path-3 settlement and the canonical T5-placement marker remain unchanged"):
    check(f"disposition states: {phrase[:52]}", phrase in DOC)
check("disposition explains `unprobed` as taxonomy, not 'no probe ever ran'",
      "not a claim that no probe was ever run" in DOC)

# ---- 3. Forbidden claims are absent ----
FORBIDDEN = [
    r"H2 is weakly supported\b(?!;)", r"weak(ly)? support(s|ed)? H2",
    r"\bE arm showed improvement\b(?!;)", r"trends? toward",
    r"favou?rs the current guidance\b(?!;)", r"likely explanation\b(?!;)",
    r"more samples would (probably )?resolve\b(?!;)",
    r"doctrine should be amended\b(?!;)",
]
# The "Claims this disposition does not make" section names each of these
# in the negative; restrict the scan to the text BEFORE that section so a
# disclaimer is never mistaken for the claim it disclaims.
body = DOC.split("## Claims this disposition does not make")[0]
for pat in FORBIDDEN:
    check(f"forbidden claim absent from the reasoning: {pat[:44]}",
          re.search(pat, body) is None, re.search(pat, body).group(0) if re.search(pat, body) else "")
# `probed in part` legitimately appears in the reasoning, but ONLY as a
# negation ("it is not promoted to ..."). Assert every occurrence is
# negated rather than banning the phrase, which would forbid the very
# sentence that states the marker was NOT promoted.
pip = [m.start() for m in re.finditer(r"probed in part", body)]
check("every `probed in part` mention in the reasoning is a negation",
      all(re.search(r"\bnot\b|\bdoes not\b", body[max(0, i - 60):i]) for i in pip),
      [body[max(0, i - 60):i + 16] for i in pip
       if not re.search(r"\bnot\b", body[max(0, i - 60):i])])
check("the disclaimer section exists and is separate from the reasoning",
      "## Claims this disposition does not make" in DOC and len(body) < len(DOC))
check("per-arm counts appear only as descriptive provenance",
      "descriptive provenance only" in DOC
      and "deliberately absent from the reasoning above" in DOC)

# ---- 4. Provenance references resolve ----
for sha, label in (("444880da4dbdf3c94531d6507252c1ad3870e71c", "#186 Section-A"),
                   ("c1ab89de42f087dc78f510da5071571ee1f5b4dc", "#187 NEEDS-NEW-PROBE"),
                   ("6fe6813bcc35edb86a8b92b4aaaa7f9ba3459ef7", "#199 prereg"),
                   ("1578bdabc9f813f780e76f2f6664a4496d85001a", "#202 prefix"),
                   ("66d9144a7cb49714cb2132280161c16b47924d96", "#203 scored")):
    check(f"provenance sha resolves and is cited: {label}",
          git("rev-parse", "--verify", sha + "^{commit}") == sha and sha in DOC)
sealed = json.load(open(os.path.join(SEALED_T5, "T5-PLACEMENT-ADJUDICATION.json")))
check("original sealed outcome cited correctly (FAIL-SIGNAL, bare 0/3 ruled 0/3)",
      sealed["sealed_D_outcome"] == "FAIL-SIGNAL"
      and sealed["per_fixture"]["T5S1"]["bare_compliant"] == 0
      and sealed["per_fixture"]["T5S1"]["ruled_compliant"] == 0
      and "FAIL-SIGNAL" in DOC and "bare 0/3, ruled 0/3" in DOC)
check("marker still undischarged in the sealed record",
      sealed["marker_discharged"] is False)
check("accounting cited as 39/50", "39/50 consumed" in DOC)
check("method deviation provenance carried",
      "AUTHORIZED-ADJUDICATION-METHOD-DEVIATION" in DOC)
# The label alone is not enough: an "as preregistered" phrase elsewhere
# could still imply protocol-compliance-as-written and contradict it.
# Require the scope note whenever that phrase appears.
# A keyword blocklist cannot bar a PARAPHRASE class — both independent
# reviewers demonstrated bypasses against the previous predicates, and
# they were right. These three invariants are structural instead:
#
#   (i)  the two repaired paragraphs are CONTENT-PINNED, so any edit to
#        them — including a semantically-equivalent rewrite that would
#        slip past any wordlist — fails this gate and forces re-review;
#   (ii) the reasoning body may not reference a per-arm COUNT or a BAND
#        NAME at all, which enforces "the counts carry no weight here"
#        structurally rather than by banning particular sentences;
#   (iii) "as preregistered" must occur EXACTLY ONCE and the scope note
#        must immediately follow it, so scoping is per-occurrence and
#        adjacency-bound rather than mere global co-presence.
#
# Each is proven able to fail: see the mutant controls at the end.
RAW = rd(os.path.join(ROOT, "DISPOSITION.md")).decode()
PINS = {
    "scope-note paragraph": ('Scope of "as preregistered"', "Reading of `unprobed`",
                             "8bc0f63c6d813091e787cde2cbedbe7037bb271875de3877d9001f6f9e354f8c"),
    "capacity-rationale paragraph": ("Adding observations now would be conditioned", "## Provenance",
                                     "29c5a053a9f53873490ab3059f13999f488ba64c0a8cd2ab620b2e73a241fd29"),
}

def pinned(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i)]

def pin_ok(text, name):
    s, e, h = PINS[name]
    try:
        return hashlib.sha256(pinned(text, s, e).encode()).hexdigest() == h
    except ValueError:
        return False

for name in PINS:
    check(f"content pin holds: {name}", pin_ok(RAW, name))

REASONING = RAW.split("## Provenance")[0]

def structural_ok(reasoning):
    return (not re.findall(r"\b\d/6\b", reasoning)
            and not re.findall(r"\b(HIGH|LOW|MID)\b", reasoning))

check("reasoning body references no per-arm count and no band name",
      structural_ok(REASONING),
      re.findall(r"\b\d/6\b|\b(?:HIGH|LOW|MID)\b", REASONING))

def scoping_ok(text):
    """Per-occurrence, adjacency-bound. The phrase may appear exactly
    twice: once in the owner's ruling, once as the scope note's own
    subject. The note must be the next thing that carries it, and
    nothing after the note may re-use it unscoped."""
    flat = re.sub(r"\s+", " ", re.sub(r"^\s*>\s?", "", text, flags=re.M))
    occ = [m.start() for m in re.finditer(r"as preregistered", flat)]
    if len(occ) != 2:
        return False
    ruling = flat.find("follow-up probe completed as preregistered")
    note = flat.find('Scope of "as preregistered" in that ruling')
    if ruling == -1 or note == -1 or note < ruling:
        return False
    # the note must be the SECOND occurrence, i.e. nothing else carries
    # the phrase between the ruling and the note, or anywhere after it
    return occ[0] == ruling + len("follow-up probe completed ") and occ[1] == note + len('Scope of "')

check('"as preregistered" appears only in the ruling and its own scope note (per-occurrence, ordered)',
      scoping_ok(RAW))
check("record explicitly declines to make a closeness claim",
      "makes no claim either way about closeness" in DOC)

# ---- Mutant controls: each invariant must be able to FAIL ----
_m1 = RAW.replace("It is **not** a claim of", "It is a claim of", 1)
check("[mutant] editing the scope-note paragraph trips its pin", not pin_ok(_m1, "scope-note paragraph"))
_m2 = REASONING.replace("about closeness", "about closeness; every arm sat comfortably far from HIGH", 1)
check("[mutant] a paraphrased closeness claim naming a band trips the structural ban",
      not structural_ok(_m2))
_m3 = RAW.replace("Reading of `unprobed`",
                  "This record asserts full compliance with the protocol as preregistered.\n\nReading of `unprobed`", 1)
check("[mutant] a second unscoped 'as preregistered' sentence trips the adjacency check",
      not scoping_ok(_m3))
check("dual recomputation provenance carried",
      "dual independent recomputation" in DOC.lower()
      and "RECOMPUTATION CONFIRMS" in DOC)

# ---- 5. Nothing outside this record changed ----
check("canonical doctrine/marker blob identical to pre-disposition main",
      git("rev-parse", f"{PRE_DISPOSITION_MAIN}:{DOCTRINE}") == git("rev-parse", f"HEAD:{DOCTRINE}"),
      git("rev-parse", f"HEAD:{DOCTRINE}"))
dirty = git("diff", PRE_DISPOSITION_MAIN, "--",
            "skills", "metadata",
            "reviews/2026-08-09-issue115-scored-t5",
            "reviews/2026-08-13-issue115-doctrine-concern-adjudication",
            "reviews/2026-08-13-issue115-section-a-disposition",
            "reviews/2026-08-14-issue115-t5-placement-probe-prereg",
            "reviews/2026-08-15-issue115-t5p-prefix",
            "reviews/2026-08-15-issue115-t5p-scored")
check("historical packages, doctrine and marker byte-unchanged since #203",
      dirty == "", dirty[:200])
check("this record is additions-only (a new directory)",
      os.path.basename(ROOT) == "2026-08-15-issue115-t5-placement-disposition")

# ---- 6. Budget language ----
m = json.load(open(os.path.join(PREREG, "MANIFEST.json")))
check("prereg manifest still records both prior pools as NOT USED",
      "NOT USED" in m["budget"]["t2probe_headroom_11"]
      and "NOT USED" in m["budget"]["stage2_reserve_18"])
check("remaining capacity is never called a reserve",
      "never a reserve" in DOC and re.search(r"remaining .{0,30}\breserve\b(?! )", body) is None)
check("remaining slots recorded as closed, not spent",
      "closed to this concern's disposition" in DOC and "not spent" in DOC)
check("both prior pools recorded untouched", "untouched" in DOC)

# ---- 7. Issue state ----
check("#115 still OPEN and recorded as OPEN",
      json.loads(subprocess.run(["gh", "api", "repos/F-e-u-e-r/opus-pack/issues/115"],
                                capture_output=True, text=True).stdout)["state"] == "open"
      and "Issue #115: **OPEN**" in rd(os.path.join(ROOT, "DISPOSITION.md")).decode())

print()
if FAILURES:
    print("DISPOSITION CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("DISPOSITION CHECKS: ALL PASS")
