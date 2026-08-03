#!/usr/bin/env python3
"""Derived checks that enforce the ARCHITECTURE.md contract (PR 3).

Pure functions: each gate takes a repo `root` path and returns a list of
failure strings ([] == pass). No global state, no I/O beyond reading the tree,
never mutates. `checks.py` calls these on the real ROOT; `test-derived-checks.py`
calls them on temporary fixture trees to prove each gate can both pass and fail
(the two-sided proof the design note requires:
`reviews/2026-08-03-pr3-derived-checks-design.md`).

Scope + non-goals are in that design note. In particular this module does NOT
touch the `#115` `unprobed`-marker covenant scan (that stays `skills/`-only and
independent), does not change skill descriptions or policy semantics, and does
not auto-fix. Every failure names the canon, the file, and the specific
difference.
"""
import json
import os
import re

SUPPORTED_SCHEMA = 1
VALID_TIERS = ("core", "domain_adapter")
VALID_DEP_CLASSES = ("standalone", "requires", "recommended_with")
# Prose/README spelling <-> JSON canon spelling (hyphen vs underscore).
DEP_CLASS_PROSE = {"recommended_with": "recommended-with", "requires": "requires",
                   "standalone": "standalone"}


def _schema_ok(obj):
    """True iff obj['schema_version'] is a REAL integer equal to the supported
    version. bool is a subclass of int (True == 1), so a JSON boolean must be
    rejected explicitly - a boolean is not schema version 1."""
    sv = obj.get("schema_version")
    return isinstance(sv, int) and not isinstance(sv, bool) and sv == SUPPORTED_SCHEMA


# --- shared enumeration (manifest-driven, never a repo-wide SKILL.md find) ---

def _read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def _load_json(root, rel, ordered=False):
    """Return (obj, error). ordered=True detects duplicate object keys."""
    def _no_dupes(pairs):
        seen = {}
        for k, v in pairs:
            if k in seen:
                raise ValueError(f"duplicate key {k!r}")
            seen[k] = v
        return seen
    try:
        text = _read(root, rel)
    except OSError as e:
        return None, f"{rel}: unreadable ({e})"
    try:
        return json.loads(text, object_pairs_hook=_no_dupes if ordered else None), None
    except ValueError as e:
        return None, f"{rel}: not valid JSON ({e})"


def marketplace_plugins(root):
    """[(name, source_normpath)] from marketplace.json, or [] on malformed."""
    obj, err = _load_json(root, ".claude-plugin/marketplace.json")
    if err or not isinstance(obj, dict):
        return []
    out = []
    for e in obj.get("plugins", []) if isinstance(obj.get("plugins"), list) else []:
        if isinstance(e, dict) and isinstance(e.get("name"), str) and e.get("name"):
            src = e.get("source")
            if src is None:
                src = "./"  # a missing source defaults to the repo root
            if not isinstance(src, str) or not src:
                continue  # a present-but-malformed source is skipped, not coerced
                # to the base; check 2 validates the manifest shape loudly.
            out.append((e["name"], os.path.normpath(src)))
    return out


def _base_plugin_name(plugins):
    """The base/root plugin = the entry whose source is the repo root ('.')."""
    for name, src in plugins:
        if src == ".":
            return name
    return None


def published_skills(root):
    """dict skill_id -> sorted list of owning plugin names.

    A published skill is an immediate child directory of a marketplace plugin's
    `<source>/skills/` root that contains a SKILL.md. Directories under a root
    WITHOUT a SKILL.md are returned separately as orphans. Staging / fixtures /
    undeclared dirs are excluded by construction (they are under no plugin root).
    Returns (skills, orphans): skills is {id: [plugins]}, orphans is
    [(plugin, id, rel_root)].
    """
    skills, orphans = {}, []
    for name, src in marketplace_plugins(root):
        rel_root = "skills" if src == "." else f"{src}/skills"
        abs_root = os.path.join(root, rel_root)
        if not os.path.isdir(abs_root):
            continue  # missing root is reported by check_inventory
        for d in sorted(os.listdir(abs_root)):
            if not os.path.isdir(os.path.join(abs_root, d)):
                continue
            if os.path.isfile(os.path.join(abs_root, d, "SKILL.md")):
                skills.setdefault(d, []).append(name)
            else:
                orphans.append((name, d, rel_root))
    for k in skills:
        skills[k].sort()
    return skills, orphans


def opus_pack_skill_ids(root):
    """Published skill IDs owned by the base plugin (opus-pack)."""
    plugins = marketplace_plugins(root)
    base = _base_plugin_name(plugins)
    skills, _ = published_skills(root)
    return sorted(sid for sid, owners in skills.items() if base in owners)


# --- gate 1: tier canon integrity ---

def check_tier_canon(root):
    f = []
    obj, err = _load_json(root, "metadata/skill-tiers.json", ordered=True)
    if err:
        return [f"tier canon (metadata/skill-tiers.json): {err.split(': ', 1)[-1]}"]
    if not isinstance(obj, dict):
        return ["tier canon (metadata/skill-tiers.json): top level is not an object"]
    if not _schema_ok(obj):
        f.append(f"tier canon (metadata/skill-tiers.json): schema_version {obj.get('schema_version')!r} is not "
                 f"a supported integer version ({SUPPORTED_SCHEMA})")
    tiers = obj.get("tiers")
    if not isinstance(tiers, dict):
        return f + ["tier canon (metadata/skill-tiers.json): 'tiers' is missing or not an object"]
    for sid, tier in tiers.items():
        if tier not in VALID_TIERS:
            f.append(f"tier canon (metadata/skill-tiers.json): skill {sid!r} has invalid tier {tier!r} "
                     f"(allowed: {', '.join(VALID_TIERS)})")
    canon_ids = set(tiers)
    published = set(opus_pack_skill_ids(root))
    for missing in sorted(published - canon_ids):
        f.append(f"tier canon (metadata/skill-tiers.json): published opus-pack skill {missing!r} is not "
                 f"classed in metadata/skill-tiers.json")
    for extra in sorted(canon_ids - published):
        f.append(f"tier canon (metadata/skill-tiers.json): lists {extra!r}, which "
                 f"is not a published opus-pack skill")
    return f


# --- gate 2: extension dependency contract ---

def check_plugin_dependencies(root):
    f = []
    obj, err = _load_json(root, "metadata/plugin-dependencies.json", ordered=True)
    if err:
        return [f"dependency canon (metadata/plugin-dependencies.json): "
                f"{err.split(': ', 1)[-1]}"]
    if not isinstance(obj, dict):
        return ["dependency canon (metadata/plugin-dependencies.json): top level is not an object"]
    if not _schema_ok(obj):
        f.append(f"dependency canon (metadata/plugin-dependencies.json): schema_version {obj.get('schema_version')!r} "
                 f"is not a supported integer version ({SUPPORTED_SCHEMA})")
    entries = obj.get("plugins")
    if not isinstance(entries, dict):
        return f + ["dependency canon (metadata/plugin-dependencies.json): 'plugins' is missing or not an object"]
    plugins = marketplace_plugins(root)
    names = {n for n, _ in plugins}
    base = _base_plugin_name(plugins)
    extensions = {n for n in names if n != base}
    for pname, spec in entries.items():
        if pname not in names:
            f.append(f"dependency canon (metadata/plugin-dependencies.json): entry {pname!r} is not a marketplace plugin")
            continue
        if pname == base:
            f.append(f"dependency canon (metadata/plugin-dependencies.json): base plugin {pname!r} must not carry a "
                     f"dependency class (it is the referent, not an extension)")
        if not isinstance(spec, dict):
            f.append(f"dependency canon (metadata/plugin-dependencies.json): entry {pname!r} is not an object")
            continue
        cls = spec.get("dependency_class")
        if cls not in VALID_DEP_CLASSES:
            f.append(f"dependency canon (metadata/plugin-dependencies.json): {pname!r} has invalid dependency_class "
                     f"{cls!r} (allowed: {', '.join(VALID_DEP_CLASSES)})")
        companion = spec.get("companion_plugin")
        if cls == "standalone" and companion is not None:
            f.append(f"dependency canon (metadata/plugin-dependencies.json): standalone plugin {pname!r} must not name "
                     f"a companion_plugin (got {companion!r})")
        if cls in ("requires", "recommended_with"):
            if not companion:
                f.append(f"dependency canon (metadata/plugin-dependencies.json): {pname!r} is {cls} but names no "
                         f"companion_plugin")
            elif not isinstance(companion, str):
                f.append(f"dependency canon (metadata/plugin-dependencies.json): {pname!r} companion_plugin must be a "
                         f"string (got {type(companion).__name__})")
            elif companion not in names:
                f.append(f"dependency canon (metadata/plugin-dependencies.json): {pname!r} names companion_plugin "
                         f"{companion!r}, which is not a marketplace plugin")
    declared = set(entries)
    for missing in sorted(extensions - declared):
        f.append(f"dependency canon (metadata/plugin-dependencies.json): extension plugin {missing!r} has no entry in "
                 f"metadata/plugin-dependencies.json")
    return f


# --- gate 3: derived inventory + globally-unique skill IDs ---

def check_inventory(root):
    f = []
    if not marketplace_plugins(root):
        return ["inventory: no marketplace plugins resolved - "
                ".claude-plugin/marketplace.json is missing or malformed "
                "(fail closed; check 2 reports the manifest itself)"]
    for name, src in marketplace_plugins(root):
        rel_root = "skills" if src == "." else f"{src}/skills"
        if not os.path.isdir(os.path.join(root, rel_root)):
            f.append(f"inventory: plugin {name!r} skills root {rel_root}/ does not exist")
    skills, orphans = published_skills(root)
    for sid, owners in sorted(skills.items()):
        if len(owners) > 1:
            f.append(f"inventory: skill id {sid!r} is published by more than one "
                     f"plugin ({', '.join(owners)}) - IDs must be marketplace-wide unique")
    for plugin, d, rel_root in orphans:
        f.append(f"inventory: {rel_root}/{d}/ (plugin {plugin!r}) has no SKILL.md "
                 f"- an orphan directory under a published-skill root")
    return f


# --- gate 4: README projection parity ---

_MARKER = "<!-- {} GENERATED {} -->"


def _between_markers(text, block):
    """Return (content, error). Requires exactly one paired BEGIN/END."""
    begin = _MARKER.format("BEGIN", block)
    end = _MARKER.format("END", block)
    nb, ne = text.count(begin), text.count(end)
    if nb != 1 or ne != 1:
        return None, f"marker '{block}' must appear exactly once each (BEGIN={nb}, END={ne})"
    bi, ei = text.index(begin), text.index(end)
    if bi > ei:
        return None, f"marker '{block}' END precedes BEGIN"
    return text[bi + len(begin):ei], None


_TIER_ROW = re.compile(r"^\|\s*(Core|Domain adapter)\b.*?\|\s*(.*?)\s*\|\s*$")
_BACKTICKED = re.compile(r"`([^`]+)`")
_ROW_TIER = {"Core": "core", "Domain adapter": "domain_adapter"}


def _parse_readme_tiers(content):
    """({skill_id: tier}, [duplicate_ids]) from a marker-bounded tier table.
    Duplicates (a skill listed in more than one tier row) are surfaced rather
    than silently collapsed by dict assignment."""
    out, dups = {}, []
    for line in content.splitlines():
        m = _TIER_ROW.match(line.strip())
        if not m:
            continue
        tier = _ROW_TIER[m.group(1)]
        for sid in _BACKTICKED.findall(m.group(2)):
            if sid in out:
                dups.append(sid)
            out[sid] = tier
    return out, dups


def _parse_readme_deps(content):
    """({plugin: (class_prose, companion_or_None)}, [duplicate_plugins]) parsed
    from a marker-bounded dependency block. Recognizes `<plugin>` ...
    `<class> <companion>` where class is a known prose dependency-class spelling;
    a plugin declared more than once is surfaced, not silently overwritten."""
    out, dups = {}, []
    prose = set(DEP_CLASS_PROSE.values())
    plugin = None
    for tok in _BACKTICKED.findall(content):
        parts = tok.split()
        if parts and parts[0] in prose:
            if plugin is not None:
                companion = parts[1] if len(parts) > 1 else None
                if plugin in out:
                    dups.append(plugin)
                out[plugin] = (parts[0], companion)
                plugin = None
        else:
            plugin = tok
    return out, dups


def check_readme_projection(root):
    f = []
    tiers_obj, terr = _load_json(root, "metadata/skill-tiers.json")
    deps_obj, derr = _load_json(root, "metadata/plugin-dependencies.json")
    # Guard canon SHAPES: a malformed canon (tiers not a dict, plugins a list,
    # etc.) is already failed by the canon gates above; here it must not crash
    # the projection check - degrade to an empty canon and let those gates report.
    canon_tiers = {}
    if isinstance(tiers_obj, dict) and isinstance(tiers_obj.get("tiers"), dict):
        canon_tiers = tiers_obj["tiers"]
    canon_deps = {}  # {plugin: (class_prose, companion_or_None)}
    _plugins = deps_obj.get("plugins") if isinstance(deps_obj, dict) else None
    if isinstance(_plugins, dict):
        for p, spec in _plugins.items():
            if not isinstance(spec, dict):
                continue  # malformed nested shape: gate 2 reports it; don't crash
            dc = spec.get("dependency_class")
            if isinstance(dc, str) and dc in DEP_CLASS_PROSE:
                comp = spec.get("companion_plugin")
                canon_deps[p] = (DEP_CLASS_PROSE[dc], comp if isinstance(comp, str) else None)
    readmes = ["README.md", "README.zh-Hant.md"]
    parsed_tiers = {}
    for rel in readmes:
        try:
            text = _read(root, rel)
        except OSError as e:
            f.append(f"README projection: {rel} unreadable ({e})")
            continue
        # Scan markers on fence-stripped text so a marker shown INSIDE a
        # documentation code fence is not mistaken for a live one.
        stripped = "\n".join(l for _i, l in _lines_outside_fences(text, blank_inline=False))
        # Marker/table parsing needs the backticks (blank_inline=False). The
        # link + canonical-notice presence check must be OUTSIDE code - fenced AND
        # inline (ARCHITECTURE.md §8) - so it uses the inline-blanking view.
        no_code = "\n".join(l for _i, l in _lines_outside_fences(text, blank_inline=True))
        tc, terr2 = _between_markers(stripped, "SKILL TIERS")
        if terr2:
            f.append(f"README projection: {rel}: {terr2}")
        else:
            got, dups = _parse_readme_tiers(tc)
            parsed_tiers[rel] = got
            for sid in sorted(set(dups)):
                f.append(f"README projection: {rel} lists skill {sid!r} in more "
                         f"than one tier row")
            for sid in sorted(set(canon_tiers) - set(got)):
                f.append(f"README projection: {rel} tier table is missing "
                         f"canonical skill {sid!r}")
            for sid in sorted(set(got) - set(canon_tiers)):
                f.append(f"README projection: {rel} tier table lists {sid!r}, "
                         f"not in metadata/skill-tiers.json")
            for sid in sorted(set(got) & set(canon_tiers)):
                if got[sid] != canon_tiers[sid]:
                    f.append(f"README projection: {rel} classes {sid!r} as "
                             f"{got[sid]!r}; metadata/skill-tiers.json says "
                             f"{canon_tiers[sid]!r}")
        dc, derr2 = _between_markers(stripped, "PLUGIN DEPENDENCIES")
        if derr2:
            f.append(f"README projection: {rel}: {derr2}")
        else:
            gotd, ddups = _parse_readme_deps(dc)
            for pl in sorted(set(ddups)):
                f.append(f"README projection: {rel} declares plugin {pl!r} more "
                         f"than once in the dependency block")
            for p, expected in sorted(canon_deps.items()):
                if gotd.get(p) != expected:
                    f.append(f"README projection: {rel} dependency block shows "
                             f"{p!r}={gotd.get(p)!r}; metadata/plugin-dependencies.json "
                             f"says {expected!r} (class, companion)")
            for p in sorted(set(gotd) - set(canon_deps)):
                f.append(f"README projection: {rel} dependency block lists {p!r}, "
                         f"not in metadata/plugin-dependencies.json")
        # Link + notice checked on fence-stripped text so a link/notice shown
        # only inside a code example does not satisfy the requirement; the link
        # must be a real markdown link (closing paren included).
        if "](ARCHITECTURE.md)" not in no_code:
            f.append(f"README projection: {rel} has no markdown link to "
                     f"ARCHITECTURE.md (outside code)")
        if "authoritative" not in no_code and "為準" not in no_code:
            f.append(f"README projection: {rel} has no canonical-source notice")
    if len(parsed_tiers) == 2 and parsed_tiers.get("README.md") != parsed_tiers.get("README.zh-Hant.md"):
        f.append("README projection: EN and zh-Hant tier tables disagree on "
                 "canonical skill IDs/classes (display prose may differ, IDs/classes may not)")
    return f


# --- gate 5: normative-reference non-dangling (ARCHITECTURE.md section 7 grammar) ---

# A bounded, contract-scoped lexical scanner for excluding code regions from the
# reference/README scans. It handles exactly two CommonMark lexical structures —
# inline code spans (delimiter-run matched) and fenced code blocks (char + length
# aware) — and NOTHING else (no lists, HTML blocks, emphasis, or link parsing).
# It is deliberately not a full CommonMark parser; see the design note's non-goals.
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_SECTION_HEADING = re.compile(r"^#{2,3}\s+(\d+(?:\.\d+)?)\.\s")  # N or N.M only (§7)


def _blank_code_spans(s):
    """Blank inline code spans in `s`, which MAY contain newlines - a CommonMark
    code span can cross line endings (they normalize to spaces). Delimiter-run
    matched: a run of N backticks opens; the next run of EXACTLY N closes; a
    double-backtick span may itself contain single backticks; an opening run with
    no equal-length closer is literal. Newlines are PRESERVED (so the caller can
    split back into lines); every other character inside a span becomes a space."""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] != "`":
            out.append(s[i])
            i += 1
            continue
        j = i
        while j < n and s[j] == "`":
            j += 1
        run = j - i  # opening backtick-run length
        k, closed = j, False
        while k < n:
            if s[k] == "`":
                m = k
                while m < n and s[m] == "`":
                    m += 1
                if m - k == run:              # a closing run of EXACTLY `run`
                    out.append("".join("\n" if c == "\n" else " " for c in s[i:m]))
                    i = m
                    closed = True
                    break
                k = m                          # a different-length run: content
            else:
                k += 1
        if not closed:                         # no matching closer: literal ticks
            out.append(s[i:j])
            i = j
    return "".join(out)


def _is_fence_line(line):
    """(char, run_length, suffix) if `line` is a fenced-code delimiter, else None.
    A backtick fence's info string may NOT contain a backtick (CommonMark), so
    such a line is not a fence delimiter."""
    m = _FENCE.match(line)
    if not m:
        return None
    run, suffix = m.group(1), m.group(2)
    if run[0] == "`" and "`" in suffix:
        return None
    return run[0], len(run), suffix


def _lines_outside_fences(text, blank_inline):
    """Yield (lineno, line) for lines OUTSIDE fenced code blocks. Line endings are
    normalized per CommonMark (CRLF/CR -> LF) and split on LF ONLY - not
    str.splitlines(), which also breaks on NEL/LS/PS/VT/FF and would let a
    non-space/tab fence suffix slip through. A fenced block closes only on a later
    fence of the same char, length >= the opener, and an ASCII-space/tab-only
    suffix (CommonMark 0.31.2). When blank_inline is set, inline code spans -
    INCLUDING multi-line ones - are blanked, grouped by block: consecutive
    non-blank, non-fence lines form a block over which spans are delimiter-run
    matched, and a blank line or fence resets span state (a code span cannot cross
    a block boundary). Bounded to fenced blocks + code spans only - no
    lists/HTML/emphasis/link/indented-code (the design note's non-goals)."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    fence = None  # (char, length) of the open fence, or None
    block = []    # accumulated (lineno, raw) for the current paragraph block

    def flush():
        if not block:
            return
        blanked = _blank_code_spans("\n".join(raw for _, raw in block)).split("\n")
        for (ln, _), bl in zip(block, blanked):
            yield ln, bl
        block.clear()

    for i, raw in enumerate(lines, 1):
        fl = _is_fence_line(raw)
        if fl is not None:
            yield from flush()  # a fence line ends any open block
            ch, ln, suffix = fl
            if fence is None:
                fence = (ch, ln)  # opener (info string allowed; no backtick above)
            elif ch == fence[0] and ln >= fence[1] and all(c in " \t" for c in suffix):
                fence = None      # valid closer (ASCII spaces/tabs only after)
            continue
        if fence is not None:
            continue  # inside a fenced block: not normative
        if not blank_inline:
            yield i, raw
            continue
        if raw.strip() == "":
            yield from flush()  # blank line: block boundary, resets span state
            yield i, raw
            continue
        block.append((i, raw))
    yield from flush()


def _iter_normative_lines(text):
    """Reference-scan view: lines outside fences, with inline code blanked."""
    return _lines_outside_fences(text, blank_inline=True)


def _skill_sections(root, skill_id, owner_plugin_root):
    """Set of section tokens ('3', '4.1') from a skill's SKILL.md headings,
    EXCLUDING headings inside fenced code (an example heading in a fence must not
    manufacture a section that lets a dangling reference pass)."""
    rel = f"{owner_plugin_root}/{skill_id}/SKILL.md"
    try:
        text = _read(root, rel)
    except OSError:
        return None
    out = set()
    for _i, line in _lines_outside_fences(text, blank_inline=False):
        m = _SECTION_HEADING.match(line)
        if m:
            out.add(m.group(1))
    return out


def check_reference_gate(root):
    """Local dangling -> FAIL; cross-plugin -> report (returned separately).

    Returns a list of failure strings; report-only lines are prefixed 'report:'
    and are informational (the caller prints them, they do not fail the build).
    """
    f = []
    plugins = marketplace_plugins(root)
    # skill_id -> (plugin_name, rel_root)
    skills, _ = published_skills(root)
    root_of = {}
    for name, src in plugins:
        rel_root = "skills" if src == "." else f"{src}/skills"
        root_of[name] = rel_root
    owner = {}
    for sid, owners in skills.items():
        if len(owners) == 1:
            owner[sid] = owners[0]
    known = set(skills)
    if not known:
        return f
    # A normative reference is <known-skill-id> §<section> on one line. Only
    # KNOWN published skill names are matched: `<name> §N` is ALSO how external
    # sources are cited in this repo (e.g. `agent-standard-oss §8`), so an
    # unknown kebab name is a citation, not a dangling skill - matching it would
    # false-positive (proven against the real tree). The gate therefore verifies
    # section existence for references to real skills; it does NOT detect a
    # reference to a non-existent skill NAME (design note + ARCHITECTURE.md §8
    # record this limit). Section: N or N.M; ranges §§N-M are NOT parsed
    # (silently unmatched by the single-§ regex; nothing counted or failed).
    id_alt = "|".join(re.escape(s) for s in sorted(known, key=len, reverse=True))
    ref_re = re.compile(r"(?<![\w-])(" + id_alt + r")\s+§\s*(\d+(?:\.\d+)?)\b(?!\.\d)")
    # Files to scan: every published skill's SKILL.md + references/*.md, per owning plugin.
    for citing_sid, owners in sorted(skills.items()):
        if len(owners) != 1:
            continue
        citing_plugin = owners[0]
        base_dir = f"{root_of[citing_plugin]}/{citing_sid}"
        files = [f"{base_dir}/SKILL.md"]
        refs_dir = os.path.join(root, base_dir, "references")
        if os.path.isdir(refs_dir):
            files += [f"{base_dir}/references/{n}" for n in sorted(os.listdir(refs_dir))
                      if n.endswith(".md")]
        for rel in files:
            try:
                text = _read(root, rel)
            except OSError:
                continue
            for lineno, line in _iter_normative_lines(text):
                for m in ref_re.finditer(line):
                    tgt, section = m.group(1), m.group(2)
                    tgt_plugin = owner.get(tgt)
                    cross = tgt_plugin is not None and tgt_plugin != citing_plugin
                    secs = _skill_sections(root, tgt, root_of.get(tgt_plugin, "")) \
                        if tgt_plugin else None
                    if secs is not None and section not in secs:
                        msg = (f"{rel}:{lineno}: normative reference {tgt} §{section} "
                               f"names a section not found in {tgt}'s SKILL.md")
                        if cross:
                            f.append("report: " + msg + " (cross-plugin; report-only)")
                        else:
                            f.append(msg)
    return f
