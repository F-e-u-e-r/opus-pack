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
skills_dir = os.path.join(ROOT, "skills")
skill_names = sorted(
    d for d in os.listdir(skills_dir)
    if os.path.isdir(os.path.join(skills_dir, d))
)
if not skill_names:
    fail("skills/: no skill directories discovered - the pack IS the skills")
for name in skill_names:
    rel = f"skills/{name}/SKILL.md"
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

    names = fm_values("name")
    descs = fm_values("description")
    if len(names) != 1 or names[0] != name:
        fail(f"{rel}: frontmatter needs exactly one non-empty name: equal to the directory (got {names})")
    elif len(descs) != 1 or len(descs[0]) < 20:
        fail(f"{rel}: frontmatter needs exactly one single-line description: substantial enough to be a trigger")
    else:
        ok(f"{rel} frontmatter valid")

# 2. Version agreement: README badges + callouts + both plugin manifests,
#    plus manifest shape and cross-manifest identity. The callout patterns
#    are a deliberate tripwire - a reword that breaks them forces a
#    conscious re-pin of all version sites. SemVer core is ASCII with no
#    leading zeros.
NUM = r"(?:0|[1-9][0-9]*)"
SEMVER = rf"({NUM}\.{NUM}\.{NUM})"
versions = []
for rel, pats in [
    ("README.md", [rf"version-alpha--{SEMVER}-orange", rf"Early alpha \(`alpha-{SEMVER}`\)"]),
    ("README.zh-TW.md", [rf"version-alpha--{SEMVER}-orange", rf"早期 alpha\(`alpha-{SEMVER}`\)"]),
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
    if re.fullmatch(SEMVER, plugin.get("version", "")):
        versions.append(("plugin.json", plugin["version"]))
    else:
        fail(f"plugin.json: version {plugin.get('version')!r} is not strict X.Y.Z")
except (OSError, ValueError) as e:
    fail(f"plugin.json: unreadable or malformed ({e})")
try:
    marketplace = json.loads(read(".claude-plugin/marketplace.json"))
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        fail("marketplace.json: expected exactly one plugins[] entry")
    else:
        mp = entries[0]
        for k in ("name", "source", "description", "version"):
            if not nonempty_str(mp, k):
                fail(f"marketplace.json plugins[0]: {k} missing or not a non-empty string")
        if re.fullmatch(SEMVER, mp.get("version", "")):
            versions.append(("marketplace.json", mp["version"]))
        else:
            fail(f"marketplace.json plugins[0]: version {mp.get('version')!r} is not strict X.Y.Z")
        if plugin and mp.get("name") != plugin.get("name"):
            fail(f"manifest identity mismatch: plugin.json name {plugin.get('name')!r} vs plugins[0].name {mp.get('name')!r}")
        if mp.get("source") != "./":
            fail(f"marketplace.json plugins[0]: source must be './', got {mp.get('source')!r}")
except (OSError, ValueError) as e:
    fail(f"marketplace.json: unreadable or malformed ({e})")
if versions and len({v for _, v in versions}) == 1:
    ok(f"version consistent across {len(versions)} sites ({versions[0][1]})")
elif versions:
    fail(f"version mismatch: {versions}")

# 3. Every skill has a backticked mention in both READMEs (a mention
#    check, deliberately - not a table-structure parse).
for rel in ("README.md", "README.zh-TW.md"):
    body = read(rel)
    missing = [n for n in skill_names if f"`{n}`" not in body]
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
for rel in ("README.md", "README.zh-TW.md"):
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
