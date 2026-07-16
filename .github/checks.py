#!/usr/bin/env python3
"""Repo consistency checks. Run locally or in CI: python3 .github/checks.py

Scope: what the published repo carries, enumerated via `git ls-files` (the
.claude/ live-install copy and the private evals are gitignored - keeping
those in sync is a local concern, not a repo one). Fail direction: every
check fails CLOSED on what it claims to cover - a file the sweep cannot
read or decode is a failure, never a skip.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

# 1. Every skill has a CLOSED frontmatter block whose interior carries
#    exactly one name: (== directory) and exactly one single-line
#    description: long enough to be a load trigger. Single-line is a
#    deliberate house-style tripwire (skill-authoring: the description IS
#    the trigger); a folded YAML scalar failing here forces a conscious
#    decision, not an accident.
skills_dir = os.path.join(ROOT, "skills")
skill_names = sorted(
    d for d in os.listdir(skills_dir)
    if os.path.isdir(os.path.join(skills_dir, d))
)
for name in skill_names:
    rel = f"skills/{name}/SKILL.md"
    try:
        lines = read(rel).split("\n")
    except OSError as e:
        fail(f"{rel}: unreadable ({e})")
        continue
    if lines[0].strip() != "---":
        fail(f"{rel}: first line is not a frontmatter fence")
        continue
    close = next(
        (i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None
    )
    if close is None:
        fail(f"{rel}: frontmatter never closes")
        continue
    fm = lines[1:close]
    names = [l.split(":", 1)[1].strip() for l in fm if re.match(r"name:\s*\S", l)]
    descs = [l.split(":", 1)[1].strip() for l in fm if re.match(r"description:\s*\S", l)]
    if len(names) != 1 or names[0] != name:
        fail(f"{rel}: frontmatter needs exactly one name: equal to the directory (got {names})")
    elif len(descs) != 1 or len(descs[0]) < 20:
        fail(f"{rel}: frontmatter needs exactly one single-line description: substantial enough to be a trigger")
    else:
        ok(f"{rel} frontmatter valid")

# 2. Version agreement: README badges + callouts + both plugin manifests.
#    The callout patterns are a deliberate tripwire - a reword that breaks
#    them forces a conscious re-pin of all version sites.
SEMVER = r"(\d+\.\d+\.\d+)"
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
for rel, keys, required in [
    (".claude-plugin/plugin.json", ["version"], ["name", "description", "version"]),
    (".claude-plugin/marketplace.json", ["plugins", 0, "version"], ["name", "owner", "plugins"]),
]:
    try:
        data = json.loads(read(rel))
        missing = [k for k in required if k not in data]
        if missing:
            fail(f"{rel}: missing fields {missing}")
        v = data
        for k in keys:
            v = v[k]
        if not re.fullmatch(SEMVER, str(v)):
            fail(f"{rel}: version {v!r} is not X.Y.Z")
        else:
            versions.append((rel, v))
    except (OSError, KeyError, IndexError, TypeError, ValueError) as e:
        fail(f"{rel}: unreadable or malformed ({e})")
try:
    mp = json.loads(read(".claude-plugin/marketplace.json"))["plugins"][0]
    for field in ("name", "source", "description", "version"):
        if not mp.get(field):
            fail(f"marketplace.json plugins[0]: missing {field}")
except (OSError, KeyError, IndexError, ValueError) as e:
    fail(f"marketplace.json plugins[0]: {e}")
if versions and len({v for _, v in versions}) == 1:
    ok(f"version consistent across {len(versions)} sites ({versions[0][1]})")
elif versions:
    fail(f"version mismatch: {versions}")

# 3. Every skill appears as a backticked catalog token in both READMEs
#    (substring prose mentions don't count).
for rel in ("README.md", "README.zh-TW.md"):
    body = read(rel)
    missing = [n for n in skill_names if f"`{n}`" not in body]
    if missing:
        fail(f"{rel}: skills without a `backticked` catalog mention: {missing}")
    else:
        ok(f"{rel} catalogs all {len(skill_names)} skills")

# 4. Hidden-directive sweep over ALL tracked files: zero-width, bidi
#    controls, ALM, word-joiner, BOM. Fail closed: unreadable or
#    undecodable non-binary content is a failure, not a skip.
BAD = re.compile("[\\u200b-\\u200f\\u2060\\u061c\\ufeff\\u202a-\\u202e\\u2066-\\u2069]")
BINARY_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
               ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".db")
hits = 0
scanned = 0
binaries = 0
sweep_broken = False
for relp in tracked:
    p = os.path.join(ROOT, relp)
    if relp.lower().endswith(BINARY_EXTS):
        binaries += 1
        continue
    try:
        raw = open(p, "rb").read()
    except OSError as e:
        fail(f"sweep cannot read tracked file {relp}: {e}")
        sweep_broken = True
        continue
    if b"\0" in raw:
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
#    repo (reference-style and raw-HTML links are out of scope, stated).
for rel in ("README.md", "README.zh-TW.md"):
    body = read(rel)
    broken = []
    for target in re.findall(r"\]\((?!https?://|#|mailto:)([^)#\s]+)", body):
        from urllib.parse import unquote
        cleaned = unquote(target).lstrip("/")
        resolved = os.path.realpath(os.path.join(ROOT, cleaned))
        if not resolved.startswith(os.path.realpath(ROOT) + os.sep):
            fail(f"{rel}: link escapes the repo: {target}")
        elif not os.path.exists(resolved):
            broken.append(target)
    if broken:
        fail(f"{rel}: broken inline relative links: {sorted(set(broken))}")
    else:
        ok(f"{rel} inline relative markdown links resolve")

# 6. License/notices present; every hook ENTRY POINT ships with its test
#    suite - entry points are discovered, not hard-coded (helpers
#    allowlisted as libraries).
for rel in ("LICENSE", "THIRD-PARTY-NOTICES.md"):
    (ok if os.path.exists(os.path.join(ROOT, rel)) else fail)(f"{rel} present")
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

print()
if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("all checks passed")
