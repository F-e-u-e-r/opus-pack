#!/usr/bin/env python3
# H1-H10 first-hand controls for the homoglyph / visible-identity-deception question.
# Inert fixtures only: no untrusted skill is run, no network request is made, no
# config is written. Every value below is a literal test datum.
#
# Core claim under test: a VISIBLE homoglyph (distinct code points, confusable
# glyphs) survives the existing invisible/control-range sweep AND the full-source
# read, because neither compares rendered-glyph identity against code-point identity.
import re, unicodedata, json

# The EXACT invisible-Unicode sweep the repo ships (op-rigor §2 / skill-vetting §2 /
# .github/checks.py check 4), built from chr() ranges so this source embeds no
# invisibles of its own. Homoglyphs must NOT fall in this class.
_BAD = [(0x200b, 0x200f), (0x2060, 0x2060), (0x061c, 0x061c), (0xFEFF, 0xFEFF),
        (0x00AD, 0x00AD), (0x202a, 0x202e), (0x2066, 0x2069), (0xE0000, 0xE007F)]
INVISIBLE = re.compile("[" + "".join(chr(lo) + "-" + chr(hi) for lo, hi in _BAD) + "]")

def scriptof(ch):
    if ch.isascii() and ch.isalpha():
        return "LATIN"
    if not ch.isalpha():
        return "COMMON"
    try:
        return unicodedata.name(ch).split()[0]     # LATIN / CYRILLIC / GREEK / CJK / ...
    except ValueError:
        return "UNNAMED"

def cps(s):
    return [f"U+{ord(c):04X}" for c in s]

def scripts(s):
    return sorted({scriptof(c) for c in s if c.isalpha()})

def mixes_scripts(s):
    return len(scripts(s)) > 1

def invisible_hit(s):
    return bool(INVISIBLE.search(s))

# Illustrative confusable -> ASCII skeleton map (a curated subset of Unicode TR39
# confusables; the authoritative table is ~6000 entries — see report). Enough to
# demonstrate collision detection first-hand.
CONF = {"а": "a", "о": "o", "е": "e", "р": "p", "с": "c", "х": "x", "у": "y",
        "і": "i", "А": "A", "Ο": "O", "ο": "o", "α": "a", "Ε": "E", "Β": "B"}
def skeleton(s):
    return "".join(CONF.get(c, c) for c in s)

def confusable_with(s, target):
    return bool(target) and s != target and not s.isascii() and skeleton(s) == target

# Same-script / ASCII visual collisions (H11): cross-script is NOT necessary.
def ascii_skeleton(s):
    s = s.replace("rn", "m").replace("vv", "w").replace("cl", "d")
    return s.translate(str.maketrans({"0": "o", "1": "l", "5": "s", "|": "l", "!": "i"}))

def impersonates(s, target):
    # a distinct identity that look-alikes the reference, cross-script OR same-script
    return bool(target) and s != target and (skeleton(s) == target or ascii_skeleton(s) == target)

def row(tag, s, target=None, note=""):
    return {"tag": tag, "text": s, "codepoints": cps(s),
            "names": [unicodedata.name(c, "?") for c in s],
            "scripts": scripts(s), "pure_ascii": s.isascii(),
            "mixes_scripts": mixes_scripts(s),
            "invisible_sweep_hit": invisible_hit(s),
            "nfkc_folds_to_target": (bool(target) and unicodedata.normalize("NFKC", s) == target),
            "skeleton": skeleton(s), "confusable_with_target": confusable_with(s, target),
            "target": target, "note": note}

R = {}
R["H1"] = [row("ascii", "paypal", "paypal"),
           row("homoglyph", "pа" + "ypal", "paypal", "one Cyrillic a U+0430")]
R["H2"] = [row("ascii_tool", "scope", "scope"),
           row("confusable_sibling", "sc" + "о" + "pe", "scope", "Cyrillic o U+043E")]
R["H3"] = [row("ascii_host", "trusted.example", "trusted.example"),
           row("confusable_host", "trust" + "е" + "d.example", "trusted.example", "Cyrillic e U+0435")]
R["H4"] = [row("ascii_key", "authToken", "authToken"),
           row("confusable_key", "а" + "uthToken", "authToken", "leading Cyrillic a")]
R["H5"] = [row("pure_cyrillic", "привет", None,
               "Russian hello; single script, impersonates no ASCII token")]
R["H6"] = [row("cafe", "café", None, "accented Latin"),
           row("strasse", "Straße", None, "eszett, Latin script")]
R["H7"] = [row("user_name_jp", "user" + "名前", None,
               "Latin+CJK legit mixed content, impersonates no trusted token")]
R["H8"] = [row("zero_width", "ad" + chr(0x200B) + "min", None, "ZWSP -> existing sweep owns it"),
           row("bidi_override", "user" + chr(0x202E) + "nimda", None, "RLO -> existing sweep owns it")]
R["H9"] = [row("ligature_fi", chr(0xFB01) + "le", "file", "fi ligature -> NFKC folds to file"),
           row("cyrillic_a", "а", "a", "Cyrillic a: NFC/NFKC do NOT fold to Latin a")]
R["H10"] = [row("prose_decorative", "а" + "pp", "app", "confusable token in decorative prose - low security relevance"),
            row("grant_token", "sc" + "о" + "pe", "scope", "same confusable mechanism in a trustedCommands grant entry - high security relevance")]
# H11 SAME-SCRIPT / ASCII-VISUAL-COLLISION: cross-script must NOT be a necessary condition
R["H11"] = [row("ascii_collision_ref", "rnicrosoft", "microsoft", "rn->m, single-script Latin/ASCII, impersonates trusted brand"),
            row("digit_collision_ref", "paypa1", "paypal", "digit 1 for l, pure ASCII, impersonates trusted brand"),
            row("no_reference_typo", "teh", None, "same-script typo with NO trusted reference identity")]

summary = {
    "runtime_unicode": unicodedata.unidata_version,
    "H1-H4 any homoglyph caught by invisible sweep (EXPECT [])":
        [(t, r["tag"]) for t in ["H1", "H2", "H3", "H4"] for r in R[t]
         if not r["pure_ascii"] and r["invisible_sweep_hit"]],
    "H1-H4 all homoglyphs confusable_with_target (EXPECT True)":
        all(r["confusable_with_target"] for t in ["H1", "H2", "H3", "H4"] for r in R[t] if not r["pure_ascii"]),
    "H1-H4 all homoglyphs mix scripts within token (EXPECT True)":
        all(r["mixes_scripts"] for t in ["H1", "H2", "H3", "H4"] for r in R[t] if not r["pure_ascii"]),
    "H5 pure-cyrillic mixes_scripts (EXPECT False)": R["H5"][0]["mixes_scripts"],
    "H5 confusable_with_target (EXPECT False)": R["H5"][0]["confusable_with_target"],
    "H6 accented-latin mixes_scripts (EXPECT [False,False])": [r["mixes_scripts"] for r in R["H6"]],
    "H6 accented-latin invisible_hit (EXPECT [False,False])": [r["invisible_sweep_hit"] for r in R["H6"]],
    "H7 mixes_scripts True but confusable_with_target False":
        [R["H7"][0]["mixes_scripts"], R["H7"][0]["confusable_with_target"]],
    "H8 invisible_sweep_hit (EXPECT [True,True] = existing rule owns)":
        [r["invisible_sweep_hit"] for r in R["H8"]],
    "H9 ligature folds under NFKC (EXPECT True)": R["H9"][0]["nfkc_folds_to_target"],
    "H9 cyrillic-a folds under NFKC (EXPECT False)": R["H9"][1]["nfkc_folds_to_target"],
    "H10 same skeleton both, security-relevance differs (codepoints identical class)":
        {"prose_cps": R["H10"][0]["codepoints"], "grant_cps": R["H10"][1]["codepoints"],
         "both_confusable": [R["H10"][0]["confusable_with_target"], R["H10"][1]["confusable_with_target"]]},
    "H11a rnicrosoft impersonates microsoft (EXPECT True)": impersonates("rnicrosoft", "microsoft"),
    "H11a mixes_scripts (EXPECT False = NOT cross-script)": R["H11"][0]["mixes_scripts"],
    "H11a cross-script skeleton alone MISSES it (confusable_with_target EXPECT False)": R["H11"][0]["confusable_with_target"],
    "H11b paypa1 impersonates paypal (EXPECT True)": impersonates("paypa1", "paypal"),
    "H11c teh has NO reference identity -> CLEAR (impersonates None EXPECT False)": impersonates("teh", None),
}
# ensure_ascii=True: the committed evidence must carry NO literal invisible/control
# code points (H8 fixtures etc.) — they are emitted as \uXXXX escapes, safe for the
# repo's Unicode-hygiene sweep while the codepoints[] fields keep the U+XXXX record.
print(json.dumps({"rows": R, "summary": summary}, ensure_ascii=True, indent=1))
