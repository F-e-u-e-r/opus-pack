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


# --- gate 6: routing-contract corpus (ARCHITECTURE.md §6) ---
#
# STRUCTURAL only. Verifies the routing regression corpus is well-formed and
# covers every published opus-pack skill on an EDGE basis. It does NOT run the
# model or verify that a description actually routes as authored: per
# ARCHITECTURE.md §8 that is the manual routing-contract review, not a mechanical
# check. Green means the corpus is complete and self-consistent, nothing about
# routing being correct or unchanged.

_CASE_KINDS = ("positive", "neighbor-negative", "out-of-scope", "ambiguous")
_ID_RE = re.compile(r"^[a-z0-9-]+\.[a-z-]+\.[a-z0-9-]+\.[0-9]{3}$")


def check_routing_corpus(root):
    P = "routing intent (metadata/routing-intent.json)"
    C = "routing corpus (metadata/routing-corpus.jsonl)"
    f = []
    published = set(opus_pack_skill_ids(root))

    # --- intent map + symmetric neighbor graph ---
    intent, err = _load_json(root, "metadata/routing-intent.json", ordered=True)
    if err:
        return [f"{P}: {err.split(': ', 1)[-1]}"]
    if not isinstance(intent, dict):
        return [f"{P}: top level is not an object"]
    if not _schema_ok(intent):
        f.append(f"{P}: schema_version {intent.get('schema_version')!r} is not a supported "
                 f"integer version ({SUPPORTED_SCHEMA})")
    skills = intent.get("skills")
    neighbors = {}
    if not isinstance(skills, dict):
        f.append(f"{P}: 'skills' is missing or not an object")
        skills = {}
    intent_ids = set(skills)
    for missing in sorted(published - intent_ids):
        f.append(f"{P}: published opus-pack skill {missing!r} has no routing-intent entry")
    for extra in sorted(intent_ids - published):
        f.append(f"{P}: lists {extra!r}, which is not a published opus-pack skill")
    for sid, entry in skills.items():
        if not isinstance(entry, dict):
            f.append(f"{P}: entry for {sid!r} is not an object")
            neighbors[sid] = set()
            continue
        if not str(entry.get("intent", "")).strip():
            f.append(f"{P}: skill {sid!r} has an empty 'intent'")
        nbrs = entry.get("neighbors")
        if not isinstance(nbrs, list):
            f.append(f"{P}: skill {sid!r} 'neighbors' is missing or not a list")
            nbrs = []
        seen_n, clean = set(), set()
        for n in nbrs:
            if n == sid:
                f.append(f"{P}: skill {sid!r} lists itself as a neighbor")
            elif n not in published:
                f.append(f"{P}: skill {sid!r} neighbor {n!r} is not a published opus-pack skill")
            else:
                clean.add(n)
            if n in seen_n:
                f.append(f"{P}: skill {sid!r} lists neighbor {n!r} twice")
            seen_n.add(n)
        neighbors[sid] = clean
    # symmetry: A lists B iff B lists A
    for a in sorted(neighbors):
        for b in sorted(neighbors[a]):
            if a not in neighbors.get(b, set()):
                f.append(f"{P}: neighbor graph not symmetric: {a!r} lists {b!r} but "
                         f"{b!r} does not list {a!r}")
    # undirected edges over confirmed-symmetric entries
    edges = set()
    for a in neighbors:
        for b in neighbors[a]:
            if a in neighbors.get(b, set()):
                edges.add(tuple(sorted((a, b))))

    # --- corpus lines ---
    try:
        text = _read(root, "metadata/routing-corpus.jsonl")
    except OSError as e:
        return f + [f"{C}: unreadable ({e})"]
    positives, oos = {}, {}          # sid -> count
    neg_edges = set()                # (for, neighbor) ordered pairs seen
    ambig_edges = set()              # (a, b) sorted, covered by an ambiguous case
    ids_seen, prompts_seen = {}, {}
    saw_meta = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except ValueError as e:
            f.append(f"{C}:{lineno}: invalid JSON ({e})")
            continue
        if not isinstance(obj, dict):
            f.append(f"{C}:{lineno}: line is not an object")
            continue
        kind = obj.get("kind")
        if kind == "meta":
            saw_meta = True
            if not _schema_ok(obj):
                f.append(f"{C}:{lineno}: meta schema_version {obj.get('schema_version')!r} is not "
                         f"a supported integer version ({SUPPORTED_SCHEMA})")
            if "probe_status" in obj:
                f.append(f"{C}:{lineno}: meta must not carry a hand-written aggregate 'probe_status' "
                         f"(status derives per-case from run artifacts, never authored here)")
            if not str(obj.get("expectation_source", "")).strip():
                f.append(f"{C}:{lineno}: meta must record a non-empty 'expectation_source'")
            continue
        if kind not in _CASE_KINDS:
            f.append(f"{C}:{lineno}: invalid kind {kind!r} (allowed: meta, {', '.join(_CASE_KINDS)})")
            continue
        cid = obj.get("id")
        if not isinstance(cid, str) or not _ID_RE.match(cid):
            f.append(f"{C}:{lineno}: 'id' {cid!r} missing or malformed "
                     f"(expected <for>.<kind>.<slug>.NNN, lowercase)")
            cid = None
        elif cid in ids_seen:
            f.append(f"{C}:{lineno}: duplicate case id {cid!r} (also line {ids_seen[cid]})")
        if cid:
            ids_seen[cid] = lineno
        anchor = obj.get("for")
        if anchor not in published:
            f.append(f"{C}:{lineno}: 'for' {anchor!r} is not a published opus-pack skill")
            anchor = None
        if cid and anchor:
            parts = cid.split(".")
            if parts[0] != anchor:
                f.append(f"{C}:{lineno}: id subject {parts[0]!r} != 'for' {anchor!r}")
            if parts[1] != kind:
                f.append(f"{C}:{lineno}: id kind {parts[1]!r} != 'kind' {kind!r}")
        prompt = obj.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            f.append(f"{C}:{lineno}: empty or non-string 'prompt'")
        else:
            key = prompt.strip()
            if key in prompts_seen:
                f.append(f"{C}:{lineno}: duplicate prompt text (also line {prompts_seen[key]})")
            prompts_seen[key] = lineno
        if not str(obj.get("rationale", "")).strip():
            f.append(f"{C}:{lineno}: missing 'rationale' (one sentence of adjudication basis required)")
        has_exp, has_any = "expected" in obj, "acceptable_any_of" in obj
        if kind == "ambiguous":
            if has_exp:
                f.append(f"{C}:{lineno}: ambiguous case must NOT use 'expected' (use 'acceptable_any_of')")
            aoa = obj.get("acceptable_any_of")
            if not isinstance(aoa, list) or len(aoa) < 2 or len(set(aoa)) != len(aoa):
                f.append(f"{C}:{lineno}: ambiguous 'acceptable_any_of' must be a list of >=2 distinct skill ids")
                aoa = []
            for e in aoa:
                if e not in published:
                    f.append(f"{C}:{lineno}: acceptable_any_of {e!r} is not a published opus-pack skill")
            if anchor is not None and anchor not in aoa:
                f.append(f"{C}:{lineno}: ambiguous case for {anchor!r} must include {anchor!r} in acceptable_any_of")
            if anchor is not None:
                for other in aoa:
                    if other != anchor and tuple(sorted((anchor, other))) in edges:
                        ambig_edges.add(tuple(sorted((anchor, other))))
        else:
            if has_any:
                f.append(f"{C}:{lineno}: only ambiguous cases may use 'acceptable_any_of'")
            exp = obj.get("expected")
            if kind == "out-of-scope":
                if exp == "none":
                    pass
                elif isinstance(exp, str) and exp in published:
                    if anchor is not None and (exp == anchor or exp in neighbors.get(anchor, set())):
                        f.append(f"{C}:{lineno}: out-of-scope 'expected' {exp!r} must be 'none' or an "
                                 f"UNRELATED skill (not {anchor!r} or a declared neighbor)")
                else:
                    f.append(f"{C}:{lineno}: out-of-scope 'expected' must be 'none' or a published skill")
                if anchor is not None:
                    oos[anchor] = oos.get(anchor, 0) + 1
            elif kind == "positive":
                if not isinstance(exp, str) or exp not in published:
                    f.append(f"{C}:{lineno}: positive 'expected' {exp!r} is not a published opus-pack skill")
                elif anchor is not None and exp != anchor:
                    f.append(f"{C}:{lineno}: positive for {anchor!r} must expect {anchor!r}, not {exp!r}")
                elif anchor is not None:
                    positives[anchor] = positives.get(anchor, 0) + 1
            else:  # neighbor-negative
                if not isinstance(exp, str) or exp not in published:
                    f.append(f"{C}:{lineno}: neighbor-negative 'expected' {exp!r} is not a published skill")
                elif anchor is not None:
                    if exp not in neighbors.get(anchor, set()):
                        f.append(f"{C}:{lineno}: neighbor-negative for {anchor!r} expects {exp!r}, "
                                 f"not a declared neighbor")
                    else:
                        neg_edges.add((anchor, exp))

    if not saw_meta:
        f.append(f"{C}: no meta line (first record must be kind 'meta' with schema_version + expectation_source)")

    # --- edge-based coverage minimum ---
    for sid in sorted(published):
        if positives.get(sid, 0) < 2:
            f.append(f"{C}: skill {sid!r} needs >=2 positive cases (has {positives.get(sid, 0)})")
        if oos.get(sid, 0) < 1:
            f.append(f"{C}: skill {sid!r} needs >=1 out-of-scope case")
        for n in sorted(neighbors.get(sid, set())):
            if (sid, n) not in neg_edges:
                f.append(f"{C}: skill {sid!r} needs a neighbor-negative expecting neighbor {n!r}")
    for (a, b) in sorted(edges):
        if (a, b) not in ambig_edges:
            f.append(f"{C}: neighbor edge {a!r}<->{b!r} needs >=1 ambiguous case covering both")
    return f
