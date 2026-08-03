#!/usr/bin/env python3
"""Two-sided proofs for .github/derived_checks.py (PR 3).

Each gate is shown able to PASS on a valid minimal fixture tree AND to FAIL on a
specific violation (the matrix in reviews/2026-08-03-pr3-derived-checks-design.md).
A checker never shown able to fail is not a gate. Run: python3 .github/test-derived-checks.py
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import derived_checks as d  # noqa: E402


def _w(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def _skill(name, section="## 1. First\n", extra=""):
    return (f"---\nname: {name}\ndescription: A fixture skill whose description is "
            f"long enough to serve as a load trigger here.\n---\n# {name}\n{section}{extra}")


MARKETPLACE = ('{"name":"mp","plugins":['
               '{"name":"opus-pack","source":"./"},'
               '{"name":"design-pack","source":"./design-pack"}]}')

TIERS_OK = '{"schema_version":1,"tiers":{"alpha":"core","beta":"domain_adapter"}}'
DEPS_OK = ('{"schema_version":1,"plugins":{"design-pack":'
           '{"dependency_class":"recommended_with","companion_plugin":"opus-pack"}}}')


def _readme(tiers_rows, dep_line, link=True, notice_en=True, zh=False, arch=None):
    if arch is None:
        link_txt = "[ARCHITECTURE.md](ARCHITECTURE.md)" if link else "ARCHITECTURE (no link)"
        notice_txt = (("以它為準。" if zh else "it is authoritative.") if notice_en else "no notice.")
        arch = f"See {link_txt}; {notice_txt}"
    return (
        "# Readme\n\n"
        "<!-- BEGIN GENERATED SKILL TIERS -->\n"
        "| Tier | Skills |\n|------|--------|\n" + tiers_rows +
        "<!-- END GENERATED SKILL TIERS -->\n\n"
        "<!-- BEGIN GENERATED PLUGIN DEPENDENCIES -->\n" + dep_line +
        "\n<!-- END GENERATED PLUGIN DEPENDENCIES -->\n\n" + arch + "\n"
    )


TIERS_ROWS_OK = "| Core | `alpha` |\n| Domain adapter | `beta` |\n"
DEP_LINE_OK = "`design-pack` is `recommended-with opus-pack`."


class Base(unittest.TestCase):
    def valid(self):
        root = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(root, ignore_errors=True))
        _w(root, ".claude-plugin/marketplace.json", MARKETPLACE)
        _w(root, "skills/alpha/SKILL.md", _skill("alpha", extra="See beta §1 here.\n"))
        _w(root, "skills/beta/SKILL.md", _skill("beta"))
        _w(root, "design-pack/skills/gamma/SKILL.md", _skill("gamma"))
        _w(root, "metadata/skill-tiers.json", TIERS_OK)
        _w(root, "metadata/plugin-dependencies.json", DEPS_OK)
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK))
        _w(root, "README.zh-Hant.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK, zh=True))
        return root

    def hard(self, fn, root):
        return [r for r in fn(root) if not r.startswith("report:")]


class GreenBaseline(Base):
    def test_valid_tree_passes_every_gate(self):
        root = self.valid()
        for fn in (d.check_tier_canon, d.check_plugin_dependencies, d.check_inventory,
                   d.check_readme_projection, d.check_reference_gate):
            self.assertEqual([], self.hard(fn, root), f"{fn.__name__} should pass clean")


class TierCanon(Base):
    def test_malformed_json(self):
        root = self.valid(); _w(root, "metadata/skill-tiers.json", "{ not json")
        self.assertTrue(self.hard(d.check_tier_canon, root))

    def test_unsupported_schema(self):
        root = self.valid()
        _w(root, "metadata/skill-tiers.json", '{"schema_version":2,"tiers":{"alpha":"core","beta":"domain_adapter"}}')
        self.assertTrue(any("schema_version" in r for r in d.check_tier_canon(root)))

    def test_invalid_tier_value(self):
        root = self.valid()
        _w(root, "metadata/skill-tiers.json", '{"schema_version":1,"tiers":{"alpha":"gold","beta":"domain_adapter"}}')
        self.assertTrue(any("invalid tier" in r for r in d.check_tier_canon(root)))

    def test_missing_published_skill(self):
        root = self.valid()
        _w(root, "metadata/skill-tiers.json", '{"schema_version":1,"tiers":{"alpha":"core"}}')
        self.assertTrue(any("not classed" in r for r in d.check_tier_canon(root)))

    def test_extra_nonexistent_skill(self):
        root = self.valid()
        _w(root, "metadata/skill-tiers.json", '{"schema_version":1,"tiers":{"alpha":"core","beta":"domain_adapter","zeta":"core"}}')
        self.assertTrue(any("not a published" in r for r in d.check_tier_canon(root)))

    def test_duplicate_key(self):
        root = self.valid()
        _w(root, "metadata/skill-tiers.json", '{"schema_version":1,"tiers":{"alpha":"core","alpha":"domain_adapter","beta":"domain_adapter"}}')
        self.assertTrue(self.hard(d.check_tier_canon, root))

    def test_bool_schema_version_rejected(self):
        # bool is an int subclass (True == 1); a JSON boolean is not schema 1.
        root = self.valid()
        _w(root, "metadata/skill-tiers.json",
           '{"schema_version":true,"tiers":{"alpha":"core","beta":"domain_adapter"}}')
        self.assertTrue(any("schema_version" in r for r in d.check_tier_canon(root)))


class DependencyContract(Base):
    def test_nonexistent_plugin_entry(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":{"design-pack":{"dependency_class":"recommended_with","companion_plugin":"opus-pack"},"ghost":{"dependency_class":"standalone"}}}')
        self.assertTrue(any("not a marketplace plugin" in r for r in d.check_plugin_dependencies(root)))

    def test_invalid_class(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":{"design-pack":{"dependency_class":"maybe","companion_plugin":"opus-pack"}}}')
        self.assertTrue(any("invalid dependency_class" in r for r in d.check_plugin_dependencies(root)))

    def test_standalone_with_companion(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":{"design-pack":{"dependency_class":"standalone","companion_plugin":"opus-pack"}}}')
        self.assertTrue(any("must not name a companion" in r for r in d.check_plugin_dependencies(root)))

    def test_missing_companion(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":{"design-pack":{"dependency_class":"recommended_with"}}}')
        self.assertTrue(any("names no companion" in r for r in d.check_plugin_dependencies(root)))

    def test_nonexistent_companion(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":{"design-pack":{"dependency_class":"recommended_with","companion_plugin":"nope"}}}')
        self.assertTrue(any("not a marketplace plugin" in r for r in d.check_plugin_dependencies(root)))

    def test_extension_with_no_entry(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":{}}')
        self.assertTrue(any("has no entry" in r for r in d.check_plugin_dependencies(root)))

    def test_base_plugin_must_not_be_classed(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json",
           '{"schema_version":1,"plugins":{"opus-pack":{"dependency_class":"standalone"},'
           '"design-pack":{"dependency_class":"recommended_with","companion_plugin":"opus-pack"}}}')
        self.assertTrue(any("base plugin" in r for r in d.check_plugin_dependencies(root)))

    def test_bool_schema_version_rejected_deps(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json",
           '{"schema_version":true,"plugins":{"design-pack":'
           '{"dependency_class":"recommended_with","companion_plugin":"opus-pack"}}}')
        self.assertTrue(any("schema_version" in r for r in d.check_plugin_dependencies(root)))

    def test_nested_malformed_dependency_class_does_not_crash(self):
        # A list/dict dependency_class must fail closed in gate 2 and must not
        # crash gate 4 (which builds canon_deps from the same file).
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json",
           '{"schema_version":1,"plugins":{"design-pack":'
           '{"dependency_class":["x"],"companion_plugin":"opus-pack"}}}')
        d.check_readme_projection(root)  # must not raise
        self.assertTrue(any("invalid dependency_class" in r
                            for r in d.check_plugin_dependencies(root)))

    def test_nonstring_companion_is_clean_failure_not_crash(self):
        root = self.valid()
        _w(root, "metadata/plugin-dependencies.json",
           '{"schema_version":1,"plugins":{"design-pack":'
           '{"dependency_class":"recommended_with","companion_plugin":["opus-pack"]}}}')
        res = d.check_plugin_dependencies(root)  # must not raise
        self.assertTrue(any("must be a string" in r for r in res))


class Inventory(Base):
    def test_duplicate_global_id(self):
        root = self.valid()
        _w(root, "design-pack/skills/alpha/SKILL.md", _skill("alpha"))  # alpha now in both plugins
        self.assertTrue(any("more than one plugin" in r for r in d.check_inventory(root)))

    def test_missing_manifest_root(self):
        root = self.valid()
        _w(root, ".claude-plugin/marketplace.json",
           '{"name":"mp","plugins":[{"name":"opus-pack","source":"./"},{"name":"design-pack","source":"./design-pack"},{"name":"ghost","source":"./ghost"}]}')
        self.assertTrue(any("does not exist" in r for r in d.check_inventory(root)))

    def test_orphan_dir_without_skillmd(self):
        root = self.valid()
        os.makedirs(os.path.join(root, "skills/orphan"))
        self.assertTrue(any("orphan" in r for r in d.check_inventory(root)))

    def test_staging_shaped_dir_not_counted(self):
        root = self.valid()
        _w(root, "skills-staging/whatever/SKILL.md", _skill("whatever"))
        skills, _ = d.published_skills(root)
        self.assertNotIn("whatever", skills)
        self.assertEqual([], self.hard(d.check_inventory, root))

    def test_empty_or_malformed_marketplace_fails_closed(self):
        root = self.valid()
        _w(root, ".claude-plugin/marketplace.json", "{ not json")
        self.assertTrue(any("no marketplace plugins resolved" in r
                            for r in d.check_inventory(root)))

    def test_malformed_source_not_coerced_to_base(self):
        root = self.valid()
        _w(root, ".claude-plugin/marketplace.json",
           '{"name":"mp","plugins":[{"name":"opus-pack","source":"./"},'
           '{"name":"design-pack","source":"./design-pack"},{"name":"junk","source":[1]}]}')
        skills, _ = d.published_skills(root)
        owners = {p for os_ in skills.values() for p in os_}
        self.assertNotIn("junk", owners)  # skipped, not coerced to a base/plugin

    def test_inventory_independent_of_unprobed_covenant(self):
        # Boundary 2: the manifest-driven inventory must not couple to the #115
        # `unprobed`-marker covenant (a separate skills/-only grep this module
        # never performs). An in-body covenant marker changes nothing here.
        root = self.valid()
        before, _ = d.published_skills(root)
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="A rule (unprobed - project observation, no probe).\n"))
        after, _ = d.published_skills(root)
        self.assertEqual(set(before), set(after))
        self.assertEqual([], self.hard(d.check_inventory, root))


class ReadmeProjection(Base):
    def test_missing_skill_in_markers(self):
        root = self.valid()
        _w(root, "README.md", _readme("| Core | `alpha` |\n", DEP_LINE_OK))
        self.assertTrue(any("missing canonical skill" in r for r in d.check_readme_projection(root)))

    def test_wrong_tier(self):
        root = self.valid()
        _w(root, "README.md", _readme("| Core | `alpha` |\n| Domain adapter | `alpha` |\n", DEP_LINE_OK))
        self.assertTrue(self.hard(d.check_readme_projection, root))

    def test_wrong_dependency_class(self):
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, "`design-pack` is `requires opus-pack`."))
        self.assertTrue(any("dependency block" in r for r in d.check_readme_projection(root)))

    def test_unpaired_marker(self):
        root = self.valid()
        txt = _readme(TIERS_ROWS_OK, DEP_LINE_OK).replace("<!-- END GENERATED SKILL TIERS -->", "")
        _w(root, "README.md", txt)
        self.assertTrue(any("exactly once" in r for r in d.check_readme_projection(root)))

    def test_missing_link(self):
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK, link=False))
        self.assertTrue(any("link to ARCHITECTURE.md" in r for r in d.check_readme_projection(root)))

    def test_missing_notice(self):
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK, notice_en=False))
        self.assertTrue(any("canonical-source notice" in r for r in d.check_readme_projection(root)))

    def test_en_zh_mismatch(self):
        root = self.valid()
        _w(root, "README.zh-Hant.md", _readme("| Core | `alpha` |\n| Domain adapter | `zeta` |\n", DEP_LINE_OK, zh=True))
        self.assertTrue(self.hard(d.check_readme_projection, root))

    def test_malformed_canon_shapes_do_not_crash(self):
        root = self.valid()
        _w(root, "metadata/skill-tiers.json", '{"schema_version":1,"tiers":null}')
        _w(root, "metadata/plugin-dependencies.json", '{"schema_version":1,"plugins":[1,2]}')
        d.check_readme_projection(root)  # must not raise on malformed canon shapes
        self.assertTrue(d.check_tier_canon(root))          # canon gates still flag them
        self.assertTrue(d.check_plugin_dependencies(root))

    def test_duplicate_tier_row_id(self):
        root = self.valid()
        _w(root, "README.md", _readme(
            "| Core | `alpha` |\n| Domain adapter | `alpha` |\n| Domain adapter | `beta` |\n",
            DEP_LINE_OK))
        self.assertTrue(any("more than one tier row" in r for r in d.check_readme_projection(root)))

    def test_extra_dependency_in_readme(self):
        root = self.valid()
        _w(root, "README.md", _readme(
            TIERS_ROWS_OK,
            "`design-pack` is `recommended-with opus-pack`. `ghost-pack` is `standalone`."))
        self.assertTrue(any("not in metadata/plugin-dependencies.json" in r
                            for r in d.check_readme_projection(root)))

    def test_link_only_in_inline_code_fails(self):
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK,
            arch="`[ARCHITECTURE.md](ARCHITECTURE.md)` and the word authoritative."))
        self.assertTrue(any("link to ARCHITECTURE.md" in r
                            for r in d.check_readme_projection(root)))

    def test_notice_only_in_inline_code_fails(self):
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK,
            arch="See [ARCHITECTURE.md](ARCHITECTURE.md); `it is authoritative`."))
        self.assertTrue(any("canonical-source notice" in r
                            for r in d.check_readme_projection(root)))

    def test_link_notice_in_fenced_code_not_counted(self):
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK,
            arch="```\n[ARCHITECTURE.md](ARCHITECTURE.md) authoritative\n```"))
        res = d.check_readme_projection(root)
        self.assertTrue(any("link to ARCHITECTURE.md" in r for r in res))
        self.assertTrue(any("canonical-source notice" in r for r in res))

    def test_inline_false_hit_plus_real_outside_hit_passes(self):
        # An inline-code copy must not cause wholesale rejection when a real
        # outside-code link + notice is also present.
        root = self.valid()
        _w(root, "README.md", _readme(TIERS_ROWS_OK, DEP_LINE_OK,
            arch="`[ARCHITECTURE.md](ARCHITECTURE.md) authoritative` and really "
                 "[ARCHITECTURE.md](ARCHITECTURE.md) is authoritative here."))
        res = d.check_readme_projection(root)
        self.assertFalse(any("ARCHITECTURE.md" in r or "notice" in r for r in res))

    def test_readme_wrong_companion_flagged(self):
        root = self.valid()
        _w(root, "README.md",
           _readme(TIERS_ROWS_OK, "`design-pack` is `recommended-with ghost-pack`."))
        self.assertTrue(any("dependency block shows" in r
                            for r in d.check_readme_projection(root)))

    def test_readme_duplicate_dependency_declaration_flagged(self):
        root = self.valid()
        _w(root, "README.md", _readme(
            TIERS_ROWS_OK,
            "`design-pack` is `recommended-with opus-pack`. "
            "`design-pack` is `requires opus-pack`."))
        self.assertTrue(any("more than once in the dependency block" in r
                            for r in d.check_readme_projection(root)))


class ReferenceGate(Base):
    def test_valid_local_reference_passes(self):
        root = self.valid()  # alpha references beta §1, beta has ## 1.
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_dangling_local_section_fails(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md", _skill("alpha", extra="See beta §9 here.\n"))
        self.assertTrue(any("§9" in r and "not found" in r for r in d.check_reference_gate(root)))

    def test_cross_plugin_is_report_only(self):
        root = self.valid()
        _w(root, "design-pack/skills/gamma/SKILL.md", _skill("gamma", extra="See alpha §9 here.\n"))
        res = d.check_reference_gate(root)
        self.assertEqual([], [r for r in res if not r.startswith("report:")])  # no hard fail
        self.assertTrue(any(r.startswith("report:") for r in res))  # but a report

    def test_reference_in_code_fence_is_ignored(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```\nbeta §9\n```\n"))  # bad ref, but fenced
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_reference_in_inline_code_is_ignored(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="A dangling `beta §9` inside inline code must not count.\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_double_backtick_inline_ignored(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="A ``beta §9`` double-backtick span must not count.\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_tilde_fence_ignored(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md", _skill("alpha", extra="~~~\nbeta §9\n~~~\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_multilevel_section_ref_not_parsed(self):
        # §1.2.3 is outside the §7 grammar (N or N.M) -> not parsed, not failed.
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md", _skill("alpha", extra="See beta §1.2.3 now.\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_double_backtick_span_with_inner_single_backtick_ignored(self):
        # A double-backtick code span may itself contain a single backtick; the
        # §-reference inside it must not be flagged (delimiter-run matching).
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="Text ``foo beta §9` bar`` more.\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_mixed_length_nested_fence_does_not_close_early(self):
        # A 4-backtick block contains a 3-backtick line; the shorter inner fence
        # must NOT close the block, so a dangling ref inside stays excluded.
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="````\n```\nbeta §9\n```\n````\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_fence_closer_with_tab_is_accepted(self):
        # CommonMark 0.31.2: spaces OR tabs may follow a closing fence. A tab
        # closer must CLOSE the block, so a dangling ref AFTER it is caught.
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```\ncode\n```\t\nSee beta §9 outside.\n"))
        self.assertTrue(any("§9" in r and "not found" in r for r in d.check_reference_gate(root)))

    def test_fence_closer_with_trailing_spaces_is_accepted(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```\ncode\n```   \nSee beta §9 outside.\n"))
        self.assertTrue(any("§9" in r and "not found" in r for r in d.check_reference_gate(root)))

    def test_fence_closer_with_nbsp_is_rejected(self):
        # A non-ASCII whitespace (NBSP) after the fence is NOT a valid closer, so
        # the block stays open and a ref inside it is excluded (not a false fail).
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```\n``` \nbeta §9\n```\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_fence_line_with_trailing_text_is_not_closer(self):
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```\n``` text\nbeta §9\n```\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_multiline_inline_code_span_excluded(self):
        # A CommonMark code span may cross line endings; a §-ref on an inner line
        # of the span must not be flagged.
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="A span `foo\nbeta §9\nbar` end.\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_backtick_fence_infostring_with_backtick_is_not_fence(self):
        # A backtick fence whose info string contains a backtick is not a fence
        # opener (CommonMark); the line after it is scanned normally.
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```foo`bar\nSee beta §9 here.\n"))
        self.assertTrue(any("§9" in r and "not found" in r for r in d.check_reference_gate(root)))

    def test_vertical_tab_after_fence_is_not_a_closer(self):
        # We split on LF only (not splitlines()), so a VT after ``` stays in the
        # suffix and the closer is rejected -> the ref inside stays excluded.
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md",
           _skill("alpha", extra="```\n```\x0b\nbeta §9\n```\n"))
        self.assertEqual([], self.hard(d.check_reference_gate, root))

    def test_fenced_heading_does_not_manufacture_section(self):
        # A §9 heading that exists ONLY inside a fence in the target must not
        # satisfy a reference to §9 (false-negative guard).
        root = self.valid()
        _w(root, "skills/alpha/SKILL.md", _skill("alpha", extra="See beta §9 now.\n"))
        _w(root, "skills/beta/SKILL.md",
           _skill("beta", extra="```\n## 9. Fake heading inside a fence\n```\n"))
        self.assertTrue(any("§9" in r and "not found" in r for r in d.check_reference_gate(root)))


if __name__ == "__main__":
    unittest.main(verbosity=1)
