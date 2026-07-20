#!/usr/bin/env python3
"""Repo consistency checks. Run locally or in CI: python3 .github/checks.py

Scope: what the published repo carries, enumerated via `git ls-files` (the
.claude/ live-install copy and the private evals are gitignored - keeping
those in sync is a local concern, not a repo one). Fail direction: every
check fails CLOSED on what it claims to cover - a tracked file the sweep
cannot open, decode, or classify is a failure, never a skip.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL_ROOT = os.path.realpath(ROOT)
failures = []


def fail(msg):
    failures.append(msg)
    print(f"FAIL  {msg}")


def ok(msg):
    print(f"ok    {msg}")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


tracked = [
    p for p in subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode("utf-8").split("\0") if p
]

# 1. Every skill has a CLOSED frontmatter block (byte-exact fences) whose
#    interior carries exactly one name: (== directory) and exactly one
#    single-line description: long enough to be a load trigger. A trailing
#    " #" comment is stripped before judging the value (YAML semantics);
#    a bare "name:" counts as a duplicate entry, not nothing. Single-line
#    description is a deliberate house-style tripwire (skill-authoring:
#    the description IS the trigger).
# Skill roots are DISCOVERED from marketplace.json plugins[] sources, not
# hand-kept: every entry's <source>/skills/ is a root. A malformed
# marketplace file falls back to the root plugin's skills/ so this check
# still runs; check 2 fails loudly on the manifest itself.
try:
    _mp = json.loads(read(".claude-plugin/marketplace.json"))
    _pl = _mp.get("plugins") if isinstance(_mp, dict) else None
    if not isinstance(_pl, list):
        _pl = []  # null/number/etc: check 2 emits the structured failure
    _mp_sources = [
        s
        for s in (e.get("source", "") for e in _pl if isinstance(e, dict))
        if isinstance(s, str) and s
    ]
except (OSError, ValueError):
    _mp_sources = []
if not _mp_sources:
    _mp_sources = ["./"]  # fallback so check 1 still covers the root pack
skill_roots = []
for _src in _mp_sources:
    _norm = os.path.normpath(_src) if _src else "."
    _rel_root = "skills" if _norm == "." else f"{_norm}/skills"
    if _rel_root not in [r for r, _ in skill_roots]:
        skill_roots.append((_rel_root, os.path.join(ROOT, _rel_root)))
skill_names = []  # (rel_root, name) pairs across every plugin
for _rel_root, _abs_root in skill_roots:
    if not os.path.isdir(_abs_root):
        fail(f"{_rel_root}/: skills root named by marketplace.json does not exist")
        continue
    _names = sorted(
        d for d in os.listdir(_abs_root)
        if os.path.isdir(os.path.join(_abs_root, d))
    )
    if not _names:
        fail(f"{_rel_root}/: no skill directories discovered - the pack IS the skills")
    skill_names.extend((_rel_root, n) for n in _names)
# Tolerant of quoted/spaced YAML key spellings ("hooks":, hooks :) - a
# literal-spelling match is a bypass, not a check. Exotic YAML beyond this
# (block-scalar keys) is outside plausible authoring and stays a known gap.
HOOKS_KEY = re.compile(r"""\s*["']?hooks["']?\s*:""")


def fm_block(rel):
    """Frontmatter lines of a markdown file, [] if none/unreadable (caller fails on read elsewhere)."""
    try:
        lines = read(rel).split("\n")
    except OSError:
        return []
    if not lines or lines[0] != "---":
        return []
    close = next((i for i, l in enumerate(lines[1:], 1) if l == "---"), None)
    return lines[1:close] if close else []


for _rel_root, name in skill_names:
    rel = f"{_rel_root}/{name}/SKILL.md"
    try:
        lines = read(rel).split("\n")
    except OSError as e:
        fail(f"{rel}: unreadable ({e})")
        continue
    if lines[0] != "---":
        fail(f"{rel}: first line is not exactly '---'")
        continue
    close = next((i for i, l in enumerate(lines[1:], 1) if l == "---"), None)
    if close is None:
        fail(f"{rel}: frontmatter never closes with an exact '---' line")
        continue
    fm = lines[1:close]

    def fm_values(key, fm=fm):
        vals = []
        for l in fm:
            if re.match(rf"{key}:(\s|$)", l):
                v = l.split(":", 1)[1]
                vals.append(v.split(" #", 1)[0].strip())
        return vals

    if any(HOOKS_KEY.match(l) for l in fm):
        fail(f"{rel}: frontmatter declares hooks - plugins must never register hooks (standing invariant)")
    names = fm_values("name")
    descs = fm_values("description")
    if len(names) != 1 or names[0] != name:
        fail(f"{rel}: frontmatter needs exactly one non-empty name: equal to the directory (got {names})")
    elif len(descs) != 1 or len(descs[0]) < 20:
        fail(f"{rel}: frontmatter needs exactly one single-line description: substantial enough to be a trigger")
    else:
        ok(f"{rel} frontmatter valid")

# 1b. Hooks may also ride other loadable markdown surfaces (a root
#     <source>/SKILL.md, command files) - sweep their frontmatter too.
for _rel_root, _abs_root in skill_roots:
    _srcdir = _rel_root[: -len("/skills")] if _rel_root.endswith("/skills") else "."
    _extras = ["SKILL.md" if _srcdir == "." else f"{_srcdir}/SKILL.md"]
    _cmd_dir = os.path.join(ROOT, _srcdir, "commands")
    if os.path.isdir(_cmd_dir):
        _extras.extend(
            (f"commands/{f}" if _srcdir == "." else f"{_srcdir}/commands/{f}")
            for f in sorted(os.listdir(_cmd_dir))
            if f.endswith(".md")
        )
    for _extra in _extras:
        if os.path.isfile(os.path.join(ROOT, _extra)) and any(
            HOOKS_KEY.match(l) for l in fm_block(_extra)
        ):
            fail(f"{_extra}: frontmatter declares hooks - plugins must never register hooks (standing invariant)")

# 2. Version agreement: README badges + callouts track the ROOT plugin
#    (opus-pack); every marketplace entry is shape-checked and must agree
#    with its own source's plugin.json (name and version), so sibling
#    plugins version independently. The callout patterns are a deliberate
#    tripwire - a reword that breaks them forces a conscious re-pin of all
#    version sites. SemVer core is ASCII with no leading zeros.
NUM = r"(?:0|[1-9][0-9]*)"
SEMVER = rf"({NUM}\.{NUM}\.{NUM})"
versions = []
for rel, pats in [
    ("README.md", [rf"version-alpha--{SEMVER}-orange", rf"Early alpha \(`alpha-{SEMVER}`\)"]),
    ("README.zh-Hant.md", [rf"version-alpha--{SEMVER}-orange", rf"早期 alpha\(`alpha-{SEMVER}`\)"]),
]:
    body = read(rel)
    for pat in pats:
        m = re.search(pat, body)
        if not m:
            fail(f"{rel}: version site not found: {pat}")
        else:
            versions.append((rel, m.group(1)))


def nonempty_str(d, key):
    v = d.get(key)
    return isinstance(v, str) and v.strip() != ""


plugin = marketplace = None
try:
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    for k in ("name", "description", "version"):
        if not nonempty_str(plugin, k):
            fail(f"plugin.json: {k} missing or not a non-empty string")
    if isinstance(plugin.get("version"), str) and re.fullmatch(SEMVER, plugin["version"]):
        versions.append(("plugin.json", plugin["version"]))
    else:
        fail(f"plugin.json: version {plugin.get('version')!r} is not strict X.Y.Z")
except (OSError, ValueError) as e:
    fail(f"plugin.json: unreadable or malformed ({e})")
try:
    marketplace = json.loads(read(".claude-plugin/marketplace.json"))
    if not isinstance(marketplace, dict):
        fail("marketplace.json: top level is not a JSON object")
        marketplace = {}
    if marketplace and marketplace.get("name") != "opus-pack":
        fail(f"marketplace.json: marketplace name must stay 'opus-pack' (the documented install commands depend on it), got {marketplace.get('name')!r}")
    _owner = marketplace.get("owner") if marketplace else None
    if marketplace and (not isinstance(_owner, dict) or not nonempty_str(_owner, "name")):
        fail("marketplace.json: owner.name missing or not a non-empty string")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        fail("marketplace.json: plugins[] must be a non-empty list")
        entries = []
    seen_names, seen_sources = set(), set()
    for i, mp in enumerate(entries):
        ctx = f"marketplace.json plugins[{i}]"
        if not isinstance(mp, dict):
            fail(f"{ctx}: entry is not an object")
            continue
        for k in ("name", "source", "description", "version"):
            if not nonempty_str(mp, k):
                fail(f"{ctx}: {k} missing or not a non-empty string")
        pname, src = mp.get("name", ""), mp.get("source", "")
        if not isinstance(pname, str) or not isinstance(src, str):
            continue  # non-string name/source: the nonempty_str failures above already recorded it
        if pname in seen_names:
            fail(f"{ctx}: duplicate plugin name {pname!r}")
        if src in seen_sources:
            fail(f"{ctx}: duplicate source {src!r}")
        seen_names.add(pname)
        seen_sources.add(src)
        if pname and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", pname):
            fail(f"{ctx}: plugin name {pname!r} is not kebab-case")
        if not isinstance(mp.get("version"), str) or not re.fullmatch(SEMVER, mp["version"]):
            fail(f"{ctx}: version {mp.get('version')!r} is not strict X.Y.Z")
        if not src.startswith("./"):
            fail(f"{ctx}: source must be a './'-prefixed relative path, got {src!r}")
            continue
        norm = os.path.normpath(src)
        resolved = os.path.realpath(os.path.join(ROOT, norm))
        if norm.split(os.sep)[0] == ".." or not (
            resolved == REAL_ROOT or resolved.startswith(REAL_ROOT + os.sep)
        ):
            fail(f"{ctx}: source {src!r} escapes the repo")
            continue
        pj_rel = (".claude-plugin/plugin.json" if norm == "."
                  else f"{norm}/.claude-plugin/plugin.json")
        try:
            pj = json.loads(read(pj_rel))
        except (OSError, ValueError) as e:
            fail(f"{pj_rel}: unreadable or malformed ({e})")
            continue
        if not isinstance(pj, dict):
            fail(f"{pj_rel}: top level is not a JSON object")
            continue
        for k in ("name", "description", "version"):
            if not nonempty_str(pj, k):
                fail(f"{pj_rel}: {k} missing or not a non-empty string")
        if pj.get("name") != pname:
            fail(f"manifest identity mismatch: {pj_rel} name {pj.get('name')!r} vs {ctx}.name {pname!r}")
        if pj.get("version") != mp.get("version"):
            fail(f"per-plugin version mismatch: {pj_rel} {pj.get('version')!r} vs {ctx} {mp.get('version')!r}")
        if "hooks" in pj:
            fail(f"{pj_rel} declares a hooks field - plugins must never register hooks (standing invariant)")
        if "hooks" in mp:
            fail(f"{ctx}: declares a hooks component - plugins must never register hooks (standing invariant)")
        if "skills" in mp or "skills" in pj:
            fail(f"{ctx}: a skills path override is declared - keep skills under <source>/skills/ so the frontmatter sweep (check 1) covers them")
        hooks_file = "hooks/hooks.json" if norm == "." else f"{norm}/hooks/hooks.json"
        if os.path.exists(os.path.join(ROOT, hooks_file)):
            fail(f"{hooks_file} exists - plugins must never register hooks (standing invariant)")
        if pname == "opus-pack":
            if src != "./":
                fail(f"{ctx}: the root opus-pack plugin's source must be './', got {src!r}")
            if isinstance(mp.get("version"), str) and re.fullmatch(SEMVER, mp["version"]):
                versions.append(("marketplace.json[opus-pack]", mp["version"]))
    if entries and "opus-pack" not in seen_names:
        fail("marketplace.json: root plugin entry 'opus-pack' is missing")
except (OSError, ValueError) as e:
    fail(f"marketplace.json: unreadable or malformed ({e})")
if versions and len({v for _, v in versions}) == 1:
    ok(f"version consistent across {len(versions)} sites ({versions[0][1]})")
elif versions:
    fail(f"version mismatch: {versions}")

# 2b. Reverse completeness: every TRACKED sibling plugin manifest must be
#     reachable from a marketplace entry (an unreferenced plugin escapes
#     every per-plugin check above), and the design-pack README version
#     callouts must match the manifests - the alpha-badge tripwire, sibling
#     edition.
_seen_src_norm = set()
if isinstance(marketplace, dict) and isinstance(marketplace.get("plugins"), list):
    for _e in marketplace["plugins"]:
        if isinstance(_e, dict) and isinstance(_e.get("source"), str) and _e["source"]:
            _seen_src_norm.add(os.path.normpath(_e["source"]))
for _p in tracked:
    if not _p.endswith("/.claude-plugin/plugin.json"):
        continue
    _d = os.path.normpath(_p[: -len("/.claude-plugin/plugin.json")])
    if _d not in _seen_src_norm:
        fail(f"{_p}: no marketplace.json entry points at {_d!r} - an unreferenced plugin escapes validation")
    else:
        ok(f"{_p} is reachable from marketplace.json")
_dp = None
if isinstance(marketplace, dict) and isinstance(marketplace.get("plugins"), list):
    _dp = next((e for e in marketplace["plugins"] if isinstance(e, dict) and e.get("name") == "design-pack"), None)
if _dp and isinstance(_dp.get("version"), str):
    for rel, pat in [
        ("README.md", rf"currently {re.escape(_dp['version'])}"),
        ("README.zh-Hant.md", rf"目前 {re.escape(_dp['version'])}"),
    ]:
        if re.search(pat, read(rel)):
            ok(f"{rel} design-pack version callout matches {_dp['version']}")
        else:
            fail(f"{rel}: design-pack version callout missing or stale (expected a 'currently/目前 {_dp['version']}' mention)")

# 3. Every skill has a backticked mention in both READMEs (a mention
#    check, deliberately - not a table-structure parse).
for rel in ("README.md", "README.zh-Hant.md"):
    body = read(rel)
    missing = [f"{r}/{n}" for r, n in skill_names if f"`{n}`" not in body]
    if missing:
        fail(f"{rel}: skills without a `backticked` mention: {missing}")
    else:
        ok(f"{rel} carries a backticked mention of all {len(skill_names)} skills")

# 4. Hidden-directive sweep over ALL tracked files: zero-width, bidi
#    controls, ALM, word-joiner, BOM. Every tracked path is OPENED first
#    (a missing tracked file is a failure, whatever its extension); known
#    TEXT extensions may not hide behind an embedded NUL; only unknown
#    extensions may classify as binary via NUL.
BAD = re.compile("[\\u200b-\\u200f\\u2060\\u061c\\ufeff\\u202a-\\u202e\\u2066-\\u2069]")
BINARY_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
               ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".db")
TEXT_EXTS = (".md", ".py", ".sh", ".mjs", ".js", ".yml", ".yaml", ".json",
             ".txt", ".toml", ".csv", ".ps1")
hits = 0
scanned = 0
binaries = 0
sweep_broken = False
for relp in tracked:
    p = os.path.join(ROOT, relp)
    low = relp.lower()
    try:
        raw = open(p, "rb").read()
    except OSError as e:
        fail(f"sweep cannot read tracked file {relp}: {e}")
        sweep_broken = True
        continue
    if low.endswith(BINARY_EXTS):
        binaries += 1
        continue
    if b"\0" in raw:
        if low.endswith(TEXT_EXTS):
            fail(f"sweep: {relp} has a text extension but embeds a NUL byte - inspect it")
            sweep_broken = True
        else:
            binaries += 1
        continue
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail(f"sweep: {relp} is neither binary (no NUL byte) nor valid UTF-8 - inspect it")
        sweep_broken = True
        continue
    scanned += 1
    if BAD.search(text):
        fail(f"hidden-directive/zero-width char in {relp}")
        hits += 1
if hits == 0 and not sweep_broken:
    ok(f"no zero-width/bidi/joiner/BOM chars in {scanned} tracked text files ({binaries} binaries skipped)")

# 5. Inline relative markdown links in both READMEs resolve inside the
#    repo (reference-style and raw-HTML links are out of scope, stated;
#    leading whitespace inside the parens is legal CommonMark and covered).
for rel in ("README.md", "README.zh-Hant.md"):
    body = read(rel)
    broken = []
    link_bad = False
    for target in re.findall(r"\]\(\s*(?!https?://|#|mailto:)([^)#\s]+)", body):
        from urllib.parse import unquote
        cleaned = unquote(target).lstrip("/")
        resolved = os.path.realpath(os.path.join(ROOT, cleaned))
        if resolved != REAL_ROOT and not resolved.startswith(REAL_ROOT + os.sep):
            fail(f"{rel}: link escapes the repo: {target}")
            link_bad = True
        elif not os.path.exists(resolved):
            broken.append(target)
    if broken:
        fail(f"{rel}: broken inline relative links: {sorted(set(broken))}")
    elif not link_bad:
        ok(f"{rel} inline relative markdown links resolve")

# 6. License/notices are non-empty regular files; every hook ENTRY POINT
#    ships with its test suite (discovered, helpers allowlisted); and the
#    standing packaging invariant is GATED: the plugin must never declare
#    or register hooks.
for rel in ("LICENSE", "THIRD-PARTY-NOTICES.md"):
    p = os.path.join(ROOT, rel)
    if os.path.isfile(p) and os.path.getsize(p) > 0:
        ok(f"{rel} present (non-empty regular file)")
    else:
        fail(f"{rel} missing, empty, or not a regular file")
HELPER_LIBS = {"parse-commit-command.py"}
hook_entries = sorted(
    f for f in os.listdir(os.path.join(ROOT, "hooks"))
    if f.endswith((".sh", ".py")) and not f.startswith("test-")
    and f not in HELPER_LIBS
)
if not hook_entries:
    fail("hooks/: no entry points discovered - discovery is broken")
for entry in hook_entries:
    stem = entry.rsplit(".", 1)[0]
    test = f"hooks/test-{stem}.sh"
    if not os.path.exists(os.path.join(ROOT, test)):
        fail(f"hooks/{entry} has no test suite ({test} missing)")
    else:
        ok(f"hooks/{entry} + its test suite present")
if os.path.exists(os.path.join(ROOT, "hooks", "hooks.json")):
    fail("hooks/hooks.json exists - the plugin must never register hooks (standing invariant)")
if isinstance(plugin, dict) and "hooks" in plugin:
    fail("plugin.json declares a hooks field - the plugin must never register hooks (standing invariant)")
if isinstance(plugin, dict) and "hooks" not in plugin and not os.path.exists(os.path.join(ROOT, "hooks", "hooks.json")):
    ok("plugin registers no hooks (standing invariant holds)")

print()
if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("all checks passed")
