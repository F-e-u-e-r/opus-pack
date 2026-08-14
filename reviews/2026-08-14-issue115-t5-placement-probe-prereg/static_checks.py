#!/usr/bin/env python3
"""Mechanical self-checks for the issue115-t5pprobe-v1 prereg package.
Read-only; exits non-zero on any failure. Run from anywhere: paths
resolve relative to this file. Covers the standing hygiene rule —
every hash and every design-planning numeral cited in the package is
re-derivable by script."""
import hashlib, json, os, re, subprocess, sys
from math import comb

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
SEALED = os.path.join(REPO, "reviews", "2026-08-08-issue115-stage2")
DOCTRINE_REL = "skills/skill-authoring/SKILL.md"
DOCTRINE_BLOB = "caa2bcb5832fa5fe688763e97cdc1e6ff99317d4"
SEALED_DOCTRINE_BLOB = "e49c7d9f782d628758db59d5207d9185884e46fa"
BASELINE_MAIN = "c2fc127d7d2d6263439094553e4a6aa1575eeaee"
FAILURES = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)

def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def rd(path):
    with open(path, "rb") as f:
        return f.read()

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

# ---------------------------------------------------------------- 1
# Byte-identity of the sealed anchors (recomputed from BOTH sides).
check("P1 == sealed T5S1 (bytes)",
      rd(os.path.join(ROOT, "fixtures/P1.md"))
      == rd(os.path.join(SEALED, "fixtures/T5S1.md")))
check("CURRENT-clause == sealed T5-placement-clause (bytes)",
      rd(os.path.join(ROOT, "wrappers/clauses/CURRENT-clause.txt"))
      == rd(os.path.join(SEALED, "wrappers/clauses/T5-placement-clause.txt")))

# ---------------------------------------------------------------- 2
# Clause-level pin: the probed clause is byte-identical and unique in
# BOTH the live doctrine file and the sealed campaign's pinned blob
# (this is what licenses the clause-level, not file-level, pin).
clause = rd(os.path.join(ROOT, "wrappers/clauses/CURRENT-clause.txt"))
live = rd(os.path.join(REPO, DOCTRINE_REL))
check("clause occurs exactly once in live doctrine file",
      live.count(clause) == 1, str(live.count(clause)))
blob_now = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD:" + DOCTRINE_REL],
    capture_output=True, text=True).stdout.strip()
check("doctrine blob @HEAD == recorded pin", blob_now == DOCTRINE_BLOB, blob_now)
sealed_bytes = subprocess.run(
    ["git", "-C", REPO, "cat-file", "-p", SEALED_DOCTRINE_BLOB],
    capture_output=True).stdout
check("clause occurs exactly once in the sealed campaign's pinned blob",
      sealed_bytes.count(clause) == 1, str(sealed_bytes.count(clause)))
check("sealed and live doctrine blobs differ (drift is real, clause is not)",
      blob_now != SEALED_DOCTRINE_BLOB)

# ---------------------------------------------------------------- 3
# P2 lexical independence from P1 (forbidden-token scan) — the exact
# token list published in prereg §4.
p1_text = rd(os.path.join(ROOT, "fixtures/P1.md")).decode("utf-8")
p2_text = rd(os.path.join(ROOT, "fixtures/P2.md")).decode("utf-8")
p2 = p2_text.lower()
for tok in (r"\bretry\b", r"\bretries\b", r"\btimeouts?\b",
            r"\battempts?\b", r"wall-clock", r"\belapsed\b",
            r"\bbackoff\b", r"\bjitter\b", r"call site",
            r"\bendpoints?\b", r"\bwrapper\b", r"\bbounded\b",
            r"\bcap\b", r"\bhangs?\b", r"\bservices?\b",
            r"\bsandbox\b", r"\bdisposition\b"):
    check(f"P2 forbidden token absent: {tok}", re.search(tok, p2) is None)

# ---------------------------------------------------------------- 4
# No placement hint in either fixture (nothing points at an answer).
for fid in ("P1", "P2"):
    fx = rd(os.path.join(ROOT, f"fixtures/{fid}.md")).decode("utf-8").lower()
    for hint in (r"\bfold\b", r"\bowns\b", r"\bowning\b", r"\bowner\b",
                 r"host bullet", r"\bbelongs\b"):
        check(f"{fid} carries no placement hint: {hint}",
              re.search(hint, fx) is None)

# ---------------------------------------------------------------- 5
# No experiment-cue vocabulary in P2's executor-visible bytes
# (P1 is sealed bytes and carries its recorded historical comment).
for cue in (r"\bprobe\b", r"\bcontrol\b", r"\bconfound\b",
            r"\bexperiment\w*\b", r"\barms?\b", r"\bbare\b",
            r"\bruled\b", r"\bcampaign\b", r"needs-new-probe",
            r"\bownership\b", r"\bdoctrine\b"):
    check(f"P2 experiment-cue absent: {cue}", re.search(cue, p2) is None)
# P2's metadata comment is minimized to the id alone. The token
# `fixture_id` itself is NOT removable: it is present in P1's sealed
# bytes, so matching it in P2 is the controlled choice, not a leak.
check("P2 comment is minimized to fixture_id only",
      p2_text.splitlines()[0] == "<!-- fixture_id: P2 -->",
      p2_text.splitlines()[0])
check("P1 comment is the sealed campaign's own",
      p1_text.splitlines()[0]
      == "<!-- fixture_id: T5S1 | target: T5 (#159 placement) | campaign-position: 7 (odd, bare-first) -->",
      p1_text.splitlines()[0])

# ---------------------------------------------------------------- 6
# E-arm anti-leakage: the addendum names no bullet, no section, and no
# fixture vocabulary; and it exists in no skill file.
add_text = rd(os.path.join(ROOT,
              "wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt")).decode("utf-8")
add = add_text.lower()
for tok in (r"\bretry\b", r"\bretries\b", r"\btimeouts?\b",
            r"\battempts?\b", r"wall-clock", r"\belapsed\b",
            r"\bflags?\b", r"\brollout\b", r"\brelease\b",
            r"\bdeleted?\b", r"\bcodebase\b", r"\bfigure\b",
            r"\bsection\b", r"§"):
    check(f"E addendum leak-token absent: {tok}",
          re.search(tok, add) is None)
for lead in ("Retries are bounded and jittered", "Timeouts are explicit",
             "No flag outlives its purpose", "Rollout figures are stated"):
    check(f"E addendum names no bullet lead: {lead!r}",
          lead.lower() not in add)
hits = subprocess.run(
    ["grep", "-rl", "ADDITIONAL PLACEMENT CRITERION",
     os.path.join(REPO, "skills")],
    capture_output=True, text=True).stdout.strip()
check("ownership-criterion addendum absent from skills/", hits == "", hits)

# ---------------------------------------------------------------- 7
# Structural parity: P2 reuses P1's task framing verbatim and the same
# file shape (two bolded §2 bullets, three sections, 3-line rule).
FRAMING = [
    ("You maintain the instruction file below. A colleague hands you a new\n"
     "4-line rule that has been approved for inclusion, and asks you to add\n"
     "it to the file. Show exactly where and how you would add it (quote the\n"
     "edited region), and explain your placement decision in one or two\n"
     "sentences.\n"),
    ("The approved new rule (verbatim, wording may be lightly fitted to the\n"
     "file's style but not weakened):\n"),
    "The instruction file, verbatim:\n",
]
for i, block in enumerate(FRAMING, 1):
    check(f"framing block {i} verbatim in P1", block in p1_text)
    check(f"framing block {i} verbatim in P2", block in p2_text)
for fid, text in (("P1", p1_text), ("P2", p2_text)):
    check(f"{fid} has exactly two bolded §2 bullets",
          text.count("- **") == 2, str(text.count("- **")))
    check(f"{fid} has exactly three sections",
          len(re.findall(r"^## \d\. ", text, re.M)) == 3)
    rule = re.search(r'not weakened\):\n"(.*?)"\n', text, re.S)
    check(f"{fid} quoted rule found", rule is not None)
    if rule:
        check(f"{fid} quoted rule is 3 lines",
              len(rule.group(1).split("\n")) == 3,
              str(len(rule.group(1).split("\n"))))

# ---------------------------------------------------------------- 8
# Frozen inventories match the fixture bytes, and the OWNER is the
# FIRST §2 bullet in both fixtures (the anti-positional-habit design).
INVENTORY = {
    "P1": {
        "1.1": "Prefer the versioned endpoint; the unversioned alias may repoint at any time.",
        "1.2": "A sandbox endpoint never substitutes for a live smoke check.",
        "2.1": "**Retries are bounded and jittered.**",
        "2.2": "**Timeouts are explicit.**",
        "3.1": "Every failed call series logs its final disposition (gave-up / succeeded-after-N) with the elapsed wall-clock time.",
    },
    "P2": {
        "1.1": "A flag's name states the behaviour it gates, not the ticket that introduced it.",
        "1.2": "A flag added outside the flag sheet is treated as an incident.",
        "2.1": "**No flag outlives its purpose.**",
        "2.2": "**Rollout figures are stated, never inherited.**",
        "3.1": "Every release note lists the flags whose exposure changed, with the figure before and after.",
    },
}
OWNER = {"P1": "2.1", "P2": "2.1"}
for fid, rows in INVENTORY.items():
    text = p1_text if fid == "P1" else p2_text
    flat = norm(text)
    for rid, key in rows.items():
        check(f"{fid} inventory row {rid} matches fixture bytes",
              norm(key) in flat, key)
    owner_key = rows[OWNER[fid]]
    other = rows["2.2" if OWNER[fid] == "2.1" else "2.1"]
    check(f"{fid} OWNER bullet precedes its §2 competitor",
          text.index(owner_key) < text.index(other))
    # the rubric file declares the same owner id
    rub = rd(os.path.join(ROOT, f"rubrics/R-{fid}.md")).decode("utf-8")
    check(f"R-{fid} declares OWNER({fid}) = {OWNER[fid]}",
          f"**OWNER({fid}) = {OWNER[fid]}" in rub)

# --------------------------------------------------------------- 8b
# LEXICAL INVARIANT (the identifiability control for P2, and the
# descriptive fact about P1 that the prereg cites). Content-token
# overlap between each fixture's new rule and each bullet, under a
# frozen stopword list and a crude plural fold.
STOPWORDS = set(
    "a an the of to it its is are be no not and or that this these those "
    "from with for in on at as by any every all still can merely both "
    "other same".split())

def _stems(text):
    words = [re.sub(r"[^a-z0-9%]", "", w) for w in text.lower().split()]
    words = [w for w in words if w and w not in STOPWORDS and len(w) > 1]
    return [w[:-1] if (len(w) > 3 and w.endswith("s")) else w for w in words]

def content_tokens(text):
    return set(_stems(text))

def tf(text):
    counts = {}
    for w in _stems(text):
        counts[w] = counts.get(w, 0) + 1
    return counts

def bigrams(text):
    words = [w for w in (re.sub(r"[^a-z0-9%]", "", x)
                         for x in text.lower().split()) if w]
    return {f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)}

def char_ngrams(text, n=4):
    """Word-internal character n-grams — the subword axis a tokenizer
    or a character-ngram matcher can see."""
    out = set()
    for w in re.findall(r"[a-z]+", text.lower()):
        for i in range(len(w) - n + 1):
            out.add(w[i:i + n])
    return out

def fixture_parts(text):
    body = re.search(r"```markdown\n(.*)```", text, re.S).group(1)
    rule = re.search(r'not weakened\):\n"(.*?)"\n', text, re.S).group(1)
    bullets, chunks = {}, re.split(r"^## (\d)\. .*$", body, flags=re.M)
    i = 1
    while i < len(chunks):
        sec, chunk, i = chunks[i], chunks[i + 1], i + 2
        for j, b in enumerate(re.findall(r"^- .*?(?=\n- |\Z)", chunk,
                                         re.S | re.M), 1):
            bullets[f"{sec}.{j}"] = b
    return rule, bullets

OVERLAP, TFSCORE, SHARED_BIGRAMS, SHARED_CHARNG = {}, {}, {}, {}
for fid, text in (("P1", p1_text), ("P2", p2_text)):
    rule, bullets = fixture_parts(text)
    rt, rtf, rbg = content_tokens(rule), tf(rule), bigrams(rule)
    rcg = char_ngrams(rule)
    OVERLAP[fid] = {k: rt & content_tokens(v) for k, v in bullets.items()}
    TFSCORE[fid] = {k: sum(rtf[w] * c for w, c in tf(v).items() if w in rtf)
                    for k, v in bullets.items()}
    SHARED_BIGRAMS[fid] = {k: rbg & bigrams(v) for k, v in bullets.items()}
    SHARED_CHARNG[fid] = {k: rcg & char_ngrams(v) for k, v in bullets.items()}
    check(f"{fid}: five bullets extracted for the overlap scan",
          len(bullets) == 5, str(sorted(bullets)))

# P2 (the control): the OWNER must offer no DIFFERENTIAL token-level
# route on ANY of three measures — type-set overlap, frequency-weighted
# score, and shared bigrams — while both plausible competitors do.
# A set-only invariant is demonstrably insufficient: an earlier draft
# satisfied it while the owner tied a competitor on frequency and
# uniquely shared two bigrams with the rule.
check("P2: overlap(rule, OWNER 2.1) == {flag}",
      OVERLAP["P2"]["2.1"] == {"flag"}, str(sorted(OVERLAP["P2"]["2.1"])))
check("P2: overlap(rule, 2.2) == {flag, rollout, figure}",
      OVERLAP["P2"]["2.2"] == {"flag", "rollout", "figure"},
      str(sorted(OVERLAP["P2"]["2.2"])))
check("P2: overlap(rule, 3.1) == {flag, release, figure}",
      OVERLAP["P2"]["3.1"] == {"flag", "release", "figure"},
      str(sorted(OVERLAP["P2"]["3.1"])))
for comp in ("2.2", "3.1"):
    check(f"P2: competitor {comp} shares strictly more TYPES than the OWNER",
          len(OVERLAP["P2"][comp]) > len(OVERLAP["P2"]["2.1"]))
    check(f"P2: competitor {comp} scores strictly HIGHER on TF than the OWNER",
          TFSCORE["P2"][comp] > TFSCORE["P2"]["2.1"],
          f"{comp}={TFSCORE['P2'][comp]} owner={TFSCORE['P2']['2.1']}")
check("P2: OWNER shares NO bigram with the new rule",
      SHARED_BIGRAMS["P2"]["2.1"] == set(),
      str(sorted(SHARED_BIGRAMS["P2"]["2.1"])))
check("P2: OWNER is not the TF maximum over all bullets",
      TFSCORE["P2"]["2.1"] < max(TFSCORE["P2"].values()),
      str(TFSCORE["P2"]))
# Axes 4 and 5 close the CLASS the first three left open: any feature
# the rule shares with the OWNER and with NO other bullet is a
# differential surface route, whatever its granularity. Enforced over
# (4) raw, unfiltered, unstemmed word tokens — the measure a content
# filter would hide — and (5) word-internal character n-grams for
# EVERY n from 3 to 8, not one chosen width. Four successive drafts
# each satisfied the narrower measures then in force and still leaked
# a route (`codebase`; a frequency tie plus two word bigrams;
# `alive` ↔ `outlives`; then `its`/`one` at n=3 and raw `its`), so
# the family is swept exhaustively rather than at a fixed width.
P2_BULLETS = fixture_parts(p2_text)[1]
P2_RULE = fixture_parts(p2_text)[0]
_others_ids = ("1.1", "1.2", "2.2", "3.1")

def owner_exclusive(feature_fn):
    """Features shared by the rule and the OWNER but by no other bullet."""
    rf = feature_fn(P2_RULE)
    own = rf & feature_fn(P2_BULLETS["2.1"])
    elsewhere = set().union(*(rf & feature_fn(P2_BULLETS[k])
                              for k in _others_ids))
    return own - elsewhere

def raw_tokens(text):
    return set(re.findall(r"[a-z]+", text.lower()))

check("P2: no OWNER-EXCLUSIVE raw word token (unfiltered, unstemmed)",
      owner_exclusive(raw_tokens) == set(),
      str(sorted(owner_exclusive(raw_tokens))))
for _n in range(3, 9):
    _excl = owner_exclusive(lambda t, n=_n: char_ngrams(t, n))
    check(f"P2: no OWNER-EXCLUSIVE character {_n}-gram shared with the rule",
          _excl == set(), str(sorted(_excl)))
check("P2: the rule/OWNER subword overlap is exactly the universal token",
      SHARED_CHARNG["P2"]["2.1"] == {"flag"},
      str(sorted(SHARED_CHARNG["P2"]["2.1"])))
check("P2: every bullet shares at least the token `flag`",
      all("flag" in v for v in OVERLAP["P2"].values()))
check("R-P2 publishes the recomputed TF scores",
      all(f"| {v} |" in rd(os.path.join(ROOT, "rubrics/R-P2.md")).decode("utf-8")
          for v in {TFSCORE["P2"]["2.1"], TFSCORE["P2"]["2.2"]}),
      str(TFSCORE["P2"]))

# P1 (sealed bytes, descriptive): the prereg states that P1's OWNER
# shares MORE tokens than its competitor, which is why "surface
# association" is not defined as token overlap. Recompute and require
# the cited numbers.
p1_owner_n, p1_comp_n = len(OVERLAP["P1"]["2.1"]), len(OVERLAP["P1"]["2.2"])
check("P1: owner shares MORE tokens than the competitor (the cited fact)",
      p1_owner_n > p1_comp_n, f"owner={p1_owner_n} competitor={p1_comp_n}")
check("prereg cites the recomputed P1 overlap counts",
      f"owner {p1_owner_n}, competitor {p1_comp_n}"
      in rd(os.path.join(ROOT, "T5P-PROBE-PREREG-v1.md")).decode("utf-8"),
      f"owner={p1_owner_n} competitor={p1_comp_n}")

# ---------------------------------------------------------------- 9
# Arm assembly: B/C/E differ ONLY by the wrapper+clause(+addendum)
# block, and E minus the addendum block is exactly C.
PREAMBLE = b"The following governing doctrine applies to your task:\n---\n"
MID = b"\n---\n"
ADD_SEP = b"\n"
addb = rd(os.path.join(ROOT, "wrappers/clauses/OWNERSHIP-CRITERION-addendum.txt"))
for fid in ("P1", "P2"):
    fx = rd(os.path.join(ROOT, f"fixtures/{fid}.md"))
    b = fx
    c = PREAMBLE + clause + MID + fx
    e = PREAMBLE + clause + ADD_SEP + addb + MID + fx
    check(f"{fid}: B arm is fixture bytes only", b == fx)
    check(f"{fid}: C arm ends with fixture bytes verbatim", c.endswith(fx))
    check(f"{fid}: E minus addendum block == C arm",
          e.replace(ADD_SEP + addb, b"", 1) == c)
    check(f"{fid}: three arms render three distinct prompts",
          len({hashlib.sha256(x).hexdigest() for x in (b, c, e)}) == 3)

# --------------------------------------------------------------- 10
# Smoke item-5 satisfiability: every frozen anchor symbol is an exact
# substring of its fixture's bytes.
SMOKE_SYMBOLS = {
    "P1": ["## 2. Failure handling", "**Retries are bounded and jittered.**",
           "**Timeouts are explicit.**"],
    "P2": ["## 2. Flag lifecycle", "**No flag outlives its purpose.**",
           "**Rollout figures are stated, never inherited.**"],
}
for fid, symbols in SMOKE_SYMBOLS.items():
    text = p1_text if fid == "P1" else p2_text
    for sym in symbols:
        check(f"smoke item-5 satisfiable: {fid} contains {sym!r}", sym in text)

# --------------------------------------------------------------- 11
# MANIFEST consistency and re-derivation.
mpath = os.path.join(ROOT, "MANIFEST.json")
if os.path.exists(mpath):
    m = json.load(open(mpath))
    ok = True
    for fx in m["fixtures"]:
        for key, skey in (("file", "content_sha256"),
                          ("clause_file", "clause_sha256"),
                          ("addendum_file", "addendum_sha256"),
                          ("rubric", "rubric_sha256"),
                          ("predicate", "predicate_sha256")):
            if sha(os.path.join(ROOT, fx[key])) != fx[skey]:
                ok = False
    for p, h in m["documents"].items():
        if sha(os.path.join(ROOT, p)) != h:
            ok = False
    check("MANIFEST recorded hashes match recomputation", ok)
    check("MANIFEST.sha256 matches MANIFEST.json",
          open(os.path.join(ROOT, "MANIFEST.sha256")).read().split()[0]
          == sha(mpath))
    sa = m["sealed_anchors"]
    check("manifest sealed anchor T5S1 re-derives",
          sa["T5S1_content_sha256"] == sha(os.path.join(SEALED, "fixtures/T5S1.md")))
    check("manifest sealed anchor T5-placement-clause re-derives",
          sa["T5_placement_clause_sha256"]
          == sha(os.path.join(SEALED, "wrappers/clauses/T5-placement-clause.txt")))
    check("manifest sealed anchor R-T5S1 re-derives",
          sa["R_T5S1_rubric_sha256"] == sha(os.path.join(SEALED, "rubrics/R-T5S1.md")))
    check("manifest budget is the NEW pool, prior pools excluded",
          m["budget"]["planned"] == 39 and m["budget"]["hard_cap"] == 50
          and "NOT USED" in m["budget"]["stage2_reserve_18"]
          and "NOT USED" in m["budget"]["t2probe_headroom_11"])
    # SLOT-TABLE expansion agrees with the manifest's rendered hashes.
    slot = rd(os.path.join(ROOT, "SLOT-TABLE.md")).decode("utf-8")
    rows = [r for r in slot.splitlines() if r.startswith("| ")]
    scored_rows = [r for r in rows if "| SCORED |" in r]
    check("SLOT-TABLE has exactly 36 scored slots",
          len(scored_rows) == 36, str(len(scored_rows)))
    check("SLOT-TABLE has exactly 2 smoke slots",
          len([r for r in rows if "| SMOKE |" in r]) == 2)
    per = {}
    for r in scored_rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        per.setdefault((cells[2], cells[3]), []).append(cells[5])
    check("SLOT-TABLE: 6 runs per arm per fixture",
          all(len(v) == 6 for v in per.values()) and len(per) == 6,
          str({k: len(v) for k, v in per.items()}))
    hashes_ok = True
    for fx in m["fixtures"]:
        for arm, h in fx["rendered_prompt_sha256"].items():
            if any(x != h for x in per[(fx["fixture_id"], arm)]):
                hashes_ok = False
    check("SLOT-TABLE per-slot hashes == manifest rendered hashes", hashes_ok)
else:
    check("MANIFEST.json exists", False)

# --------------------------------------------------------------- 11b
# H1-anchor proof: the P1xC rendered prompt is byte-identical to the
# sealed campaign's ruled T5S1 prompt, and P1xB to its bare prompt.
sealed_manifest = json.load(open(os.path.join(SEALED, "MANIFEST.json")))
sealed_t5s1 = [f for f in sealed_manifest["fixtures"]
               if f.get("fixture_id") == "T5S1"][0]["rendered_prompt_sha256"]
ours_p1 = {k: hashlib.sha256(v).hexdigest()
           for k, v in (("B", rd(os.path.join(ROOT, "fixtures/P1.md"))),
                        ("C", PREAMBLE + clause + MID
                              + rd(os.path.join(ROOT, "fixtures/P1.md"))))}
check("H1 anchor: P1xC == sealed ruled T5S1 rendered prompt",
      ours_p1["C"] == sealed_t5s1["ruled"], ours_p1["C"])
check("H1 anchor: P1xB == sealed bare T5S1 rendered prompt",
      ours_p1["B"] == sealed_t5s1["bare"], ours_p1["B"])

# --------------------------------------------------------------- 12
# No hand-typed identifiers anywhere in the hand-authored documents.
DOCS = ["T5P-PROBE-PREREG-v1.md", "SMOKE-CHECKLIST.md",
        "rubrics/OWNERSHIP-PREDICATE.md", "rubrics/R-P1.md",
        "rubrics/R-P2.md", "wrappers/WRAPPER.md"]
known64 = {
    sha(os.path.join(ROOT, "fixtures/P1.md")),
    sha(os.path.join(ROOT, "fixtures/P2.md")),
    sha(os.path.join(ROOT, "wrappers/clauses/CURRENT-clause.txt")),
    sha(os.path.join(SEALED, "fixtures/T5S1.md")),
    sha(os.path.join(SEALED, "wrappers/clauses/T5-placement-clause.txt")),
    sha(os.path.join(SEALED, "rubrics/R-T5S1.md")),
    ours_p1["C"], ours_p1["B"],
}
resolvable40 = set()
for ident in (BASELINE_MAIN, DOCTRINE_BLOB, SEALED_DOCTRINE_BLOB):
    got = subprocess.run(["git", "-C", REPO, "rev-parse", ident],
                         capture_output=True, text=True).stdout.strip()
    check(f"git id resolves: {ident}", got == ident, got)
    resolvable40.add(ident)
for doc in DOCS:
    text = rd(os.path.join(ROOT, doc)).decode("utf-8")
    cited64 = set(re.findall(r"\b[0-9a-f]{64}\b", text))
    check(f"{doc}: all 64-hex hashes re-derive", cited64 <= known64,
          str(cited64 - known64))
    cited40 = set(re.findall(r"\b[0-9a-f]{40}\b", text))
    check(f"{doc}: all 40-hex ids re-derive", cited40 <= resolvable40,
          str(cited40 - resolvable40))

# --------------------------------------------------------------- 13
# Design-sensitivity numerals in the prereg re-derive (bands: HIGH>=5/6,
# LOW<=2/6) — no hand-typed planning numbers either.
prereg = rd(os.path.join(ROOT, "T5P-PROBE-PREREG-v1.md")).decode("utf-8")
p_high = round(sum(comb(6, k) * 0.9**k * 0.1**(6-k) for k in (5, 6)), 3)
p_low = round(sum(comb(6, k) * 0.2**k * 0.8**(6-k) for k in (0, 1, 2)), 3)
check("prereg cites the recomputed HIGH sensitivity", f"{p_high}" in prereg,
      str(p_high))
check("prereg cites the recomputed LOW sensitivity", f"{p_low}" in prereg,
      str(p_low))

# --------------------------------------------------------------- 14
# Boundary invariants the prereg asserts about itself.
check("prereg declares zero execution",
      "zero\nbehavioral execution" in prereg or "zero behavioral execution" in prereg)
check("prereg excludes both prior pools",
      "reserve 18" in prereg and "headroom 11" in prereg)
check("no OWNER-APPROVAL.json in a proposal package",
      not os.path.exists(os.path.join(ROOT, "OWNER-APPROVAL.json")))

# --------------------------------------------------------------- 15
# SELF-DESCRIPTION CONSISTENCY — record-integrity checks.
# The other sections verify hashes, invariants, and execution-facing
# properties; none of them can see whether the package's PROSE
# describes the package truthfully. The r5 design-gate round exposed
# that coverage gap (a quoted rule sentence left stale by a fixture
# edit, a stale axis count, a stale draft count), so this family
# closes it. Comparison is whitespace-normalized throughout: the
# stale quotation initially escaped a single-line grep because the
# document wrapped it across two lines.
NUMWORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
           6: "six", 7: "seven", 8: "eight"}
RECORD_DOCS = ["T5P-PROBE-PREREG-v1.md", "rubrics/R-P2.md"]
doc_text = {d: rd(os.path.join(ROOT, d)).decode("utf-8") for d in RECORD_DOCS}
script_text = rd(os.path.join(ROOT, "static_checks.py")).decode("utf-8")

# (a) Quoted fixture text must match the CURRENT fixture bytes.
rule_norms = [norm(fixture_parts(t)[0]) for t in (p1_text, p2_text)]

def quoted_spans(text):
    """Straight-double-quoted spans of >=4 words. The text is
    NORMALIZED BEFORE extraction, not after: a quote wrapped across
    source lines is invisible to a line-bounded pattern, which is
    exactly how the stale quotation survived its first sweep."""
    flat = norm(text)
    return [norm(m) for m in re.findall(r'"([^"]{20,400})"', flat)
            if len(m.split()) >= 4]

def shingles(text, k=4):
    """Relevance shingles: punctuation-stripped so a quote ending mid
    sentence still matches ("at the call site" vs "…call site.")."""
    w = [re.sub(r"[^0-9a-z%]", "", x) for x in text.lower().split()]
    w = [x for x in w if x]
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}

RULE_SHINGLES = set().union(*(shingles(r) for r in rule_norms))

for doc, text in doc_text.items():
    for span in quoted_spans(text):
        segments = [s.strip() for s in re.split(r"…|\.\.\.", span)]
        segments = [s for s in segments if len(s.split()) >= 3]
        # RELEVANCE must not reuse the CORRECTNESS predicate: if
        # "is this a rule quote?" were "does it match a rule?", a
        # stale quote would be silently reclassified as not-a-quote
        # and the check could never fail. Relevance is therefore
        # partial (a shared 4-word shingle); correctness is full
        # containment. Proven two-sided against injected defects.
        if not any(shingles(s) & RULE_SHINGLES for s in segments):
            continue
        for seg in segments:
            if len(seg.split()) < 4:
                continue
            check(f"{doc}: quoted rule text matches current fixture bytes "
                  f"({seg[:44]!r}…)",
                  any(seg in r for r in rule_norms), seg)
STALE_QUOTE = "beside its figure"
for doc, text in doc_text.items():
    check(f"{doc}: stale quotation {STALE_QUOTE!r} absent",
          STALE_QUOTE not in norm(text))

# (b) Axis count: DERIVED from §4's enumeration, then compared with
#     every self-description elsewhere (no second hard-coded numeral).
prereg_norm = norm(doc_text["T5P-PROBE-PREREG-v1.md"])
bullet = re.search(r"the lexical invariant is machine-enforced.*?"
                   r"exhaustive owner-exclusivity sweep", prereg_norm)
check("prereg: the lexical-invariant bullet is locatable", bullet is not None)
if bullet:
    romans = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
    derived = sum(1 for r_ in romans if f"({r_}) " in bullet.group(0))
    stated = re.findall(r"(\w+)-(?:axis|measure) lexical invariant", prereg_norm)
    check("prereg: axis self-description matches the DERIVED axis count",
          stated and all(s.lower() == NUMWORD[derived] for s in stated),
          f"derived={derived} ({NUMWORD.get(derived)}) stated={stated}")

# (c) Draft-history count: identical numeral word at every site, and
#     the known-stale phrase banned package-wide.
history = []
# For the script, scan only its COMMENT lines: the self-description
# lives in a comment, while this section's own check labels quote the
# banned phrase and would otherwise match themselves.
script_comments = norm("\n".join(
    l for l in script_text.splitlines() if l.strip().startswith("#")))
for name, text in list(doc_text.items()) + [("static_checks.py",
                                             script_comments)]:
    for w in re.findall(r"(\w+) successive drafts", norm(text)):
        history.append((name, w.lower()))
check("draft-history self-description present at every site",
      {n for n, _ in history} == set(RECORD_DOCS) | {"static_checks.py"},
      str(sorted({n for n, _ in history})))
check("draft-history numeral is identical at every site",
      len({w for _, w in history}) == 1, str(sorted(set(history))))
check("stale 'three successive drafts' absent package-wide",
      not any(w == "three" for _, w in history), str(history))

print()
if FAILURES:
    print("STATIC CHECKS: FAIL —", len(FAILURES), "failure(s):", FAILURES)
    sys.exit(1)
print("STATIC CHECKS: ALL PASS")
