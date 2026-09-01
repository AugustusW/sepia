"""Unit tests for scripts/check_versions.py.

Each test builds a small repository in a temp directory and runs the whole
check against it, asserting on the exit code and the report text. The cases
mirror the ways the real repository could drift, including the two found in
review: a required version field disappearing, and a version edited into a
non-string value, both of which must fail rather than count as "not declared".

Standard library only, like the script:  python3 -m unittest discover -s tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_versions


def skill_md(frontmatter_lines):
    return "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# sepia\n"


BASELINE = {
    ".claude-plugin/plugin.json": {"name": "sepia", "version": "0.4.0"},
    ".codex-plugin/plugin.json": {"name": "sepia", "version": "0.4.0"},
    ".claude-plugin/marketplace.json": {"name": "sepia", "plugins": [{"name": "sepia"}]},
    "plugin.json": {"name": "sepia"},
    "skills/sepia/SKILL.md": skill_md(
        ["name: sepia", "license: MIT", "metadata:", '  version: "0.4.0"']
    ),
}


class CheckVersionsCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def write(self, files):
        for rel, content in files.items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict):
                content = json.dumps(content, indent=2) + "\n"
            path.write_text(content, encoding="utf-8")

    def run_check(self, overrides=None):
        files = dict(BASELINE)
        files.update(overrides or {})
        self.write(files)
        return check_versions.run(self.root)

    # --- the healthy repository ---------------------------------------------

    def test_agreeing_declarations_pass(self):
        code, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    def test_undeclared_files_are_listed_not_failed(self):
        code, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertIn("plugin.json", report)
        self.assertIn("(no version declared)", report)

    # --- disagreement -------------------------------------------------------

    def test_one_manifest_behind_fails_naming_both_versions(self):
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": "0.3.0"}}
        )
        self.assertEqual(code, 1)
        self.assertIn("0.3.0", report)
        self.assertIn("0.4.0", report)

    # --- the two review findings -------------------------------------------

    def test_removing_a_required_version_field_fails(self):
        # Review case: delete .codex-plugin/plugin.json's version. The two
        # remaining declarations still agree, so without the required set this
        # would pass, which is exactly the silent failure being guarded.
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia"}}
        )
        self.assertEqual(code, 1)
        self.assertIn("required to declare a version", report)
        self.assertIn(".codex-plugin/plugin.json", report)

    def test_a_non_string_version_fails_rather_than_counting_as_absent(self):
        # Review case: "version": 0.5. Present-but-wrong is an error.
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": 0.5}}
        )
        self.assertEqual(code, 1)
        self.assertIn("not a non-empty string", report)

    def test_an_empty_string_version_fails(self):
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": ""}}
        )
        self.assertEqual(code, 1)
        self.assertIn("not a non-empty string", report)

    # --- frontmatter scoping ------------------------------------------------

    def test_version_under_another_key_is_not_the_skill_version(self):
        # Review case: compatibility.version must not shadow metadata.version.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    [
                        "name: sepia",
                        "compatibility:",
                        '  version: "9.9.9"',
                        "metadata:",
                        '  version: "0.4.0"',
                    ]
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_only_a_foreign_version_means_the_skill_declares_none(self):
        # With no metadata.version at all, the skill declares nothing, and
        # since it is a required file that is a failure.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "compatibility:", '  version: "9.9.9"']
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("skills/sepia/SKILL.md: required", report)

    def test_a_top_level_frontmatter_version_does_not_count(self):
        # The Agent Skills shape puts the version under metadata; a top-level
        # version key belongs to nothing and must not be picked up.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ['version: "9.9.9"', "name: sepia", "metadata:", '  version: "0.4.0"']
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_a_nested_version_inside_metadata_is_not_the_skill_version(self):
        # Review case, round two: metadata.compatibility.version must not
        # shadow metadata's own direct child. Only the direct child counts.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    [
                        "name: sepia",
                        "metadata:",
                        "  compatibility:",
                        '    version: "9.9.9"',
                        '  version: "0.4.0"',
                    ]
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_only_a_nested_version_means_the_skill_declares_none(self):
        # With nothing but metadata.compatibility.version, the skill declares
        # no version of its own, and since it is required that fails.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "  compatibility:", '    version: "9.9.9"']
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("skills/sepia/SKILL.md: required", report)

    def test_a_blank_line_inside_metadata_does_not_close_the_block(self):
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "", '  version: "0.4.0"']
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    def test_an_empty_metadata_version_fails(self):
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "  version:"]
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("present but empty", report)

    # --- discovery of manifests that grow a version later -------------------

    def test_root_plugin_json_growing_a_matching_version_is_counted(self):
        code, report = self.run_check(
            {"plugin.json": {"name": "sepia", "version": "0.4.0"}}
        )
        self.assertEqual(code, 0)
        self.assertIn("4 declarations", report)

    def test_root_plugin_json_growing_a_different_version_fails(self):
        code, report = self.run_check(
            {"plugin.json": {"name": "sepia", "version": "0.5.0"}}
        )
        self.assertEqual(code, 1)
        self.assertIn("0.5.0", report)

    def test_a_marketplace_plugins_entry_version_is_checked_by_label(self):
        code, report = self.run_check(
            {
                ".claude-plugin/marketplace.json": {
                    "name": "sepia",
                    "plugins": [{"name": "sepia", "version": "0.9.9"}],
                }
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("plugins[0]", report)
        self.assertIn("0.9.9", report)

    # --- the guard guarding itself ------------------------------------------

    def test_an_empty_tree_fails_rather_than_passing_vacuously(self):
        self.write({})  # nothing at all
        code, report = check_versions.run(self.root)
        self.assertEqual(code, 1)

    def test_unreadable_json_fails(self):
        code, report = self.run_check({".codex-plugin/plugin.json": "{not json"})
        self.assertEqual(code, 1)
        self.assertIn("unreadable", report)


if __name__ == "__main__":
    unittest.main()
