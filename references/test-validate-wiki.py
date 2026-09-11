#!/usr/bin/env python3
"""Regression tests for incremental wiki validation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-wiki.py").resolve()


def concept(title: str, body: str = "", tags: str = "[test]") -> str:
    return f'''---
type: Note
title: {title}
description: A test concept.
status: draft
tags: {tags}
generated:
  by: test-agent/1.0
  at: "2026-08-27T12:00:00+02:00"
---

# {title}

{body}
'''


class ValidatorCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "references").mkdir()
        (self.root / "wiki").mkdir()
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\n- `test`: Used by validator fixtures.\n",
        )
        self.write("wiki/index.md", '---\nokf_version: "0.2"\n---\n\n# Knowledge Base\n')
        self.write("wiki/log.md", "# Directory Update Log\n")
        self.git("init", "-q")
        self.git("config", "user.email", "validator@example.test")
        self.git("config", "user.name", "Validator Test")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative_path: str, text: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        )

    def commit(self) -> None:
        self.sync_index()
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def sync_index(self) -> None:
        concepts = sorted(
            path.relative_to(self.root / "wiki").as_posix()
            for path in (self.root / "wiki").rglob("*.md")
            if path.name not in {"index.md", "log.md"}
        )
        entries = "".join(f"* [{path}]({path})\n" for path in concepts)
        self.write(
            "wiki/index.md",
            f'---\nokf_version: "0.2"\n---\n\n# Knowledge Base\n\n{entries}',
        )

    def run_validator(
        self,
        *arguments: str,
        root: Path | None = None,
        sync_index: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        if sync_index and root is None:
            self.sync_index()
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root or self.root), *arguments],
            capture_output=True,
            text=True,
        )

    def test_description_is_required_for_drafts(self) -> None:
        topic = concept("Topic").replace("description: A test concept.\n", "")
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/topic.md: missing required field description", result.stdout)

    def test_empty_tags_are_rejected(self) -> None:
        self.write("wiki/topic.md", concept("Topic", tags="[]"))

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/topic.md: tags must contain at least one approved tag", result.stdout)

    def test_changed_file_selects_direct_referrer_but_not_unrelated_file(self) -> None:
        self.write("wiki/target.md", concept("Target", "Original."))
        self.write("wiki/referrer.md", concept("Referrer", "See [Target](target.md)."))
        self.write("wiki/unrelated.md", concept("Unrelated", "Separate."))
        self.commit()
        self.write("wiki/target.md", concept("Target", "Changed."))

        result = self.run_validator("--changed", "wiki/target.md")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DIRECT: wiki/target.md", result.stdout)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)
        self.assertNotIn("wiki/unrelated.md", result.stdout)

    def test_changed_file_selects_frontmatter_path_referrer(self) -> None:
        self.write("wiki/target.md", concept("Target", "Original."))
        referrer = concept("Referrer").replace(
            "generated:\n",
            'resource: "target\\u002emd"\ngenerated:\n',
        )
        self.write("wiki/referrer.md", referrer)
        self.commit()
        self.write("wiki/target.md", concept("Target", "Changed."))

        result = self.run_validator("--changed", "wiki/target.md")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)

    def test_changed_file_selects_reference_style_link_with_query(self) -> None:
        self.write("wiki/target.md", concept("Target", "Original."))
        self.write(
            "wiki/referrer.md",
            concept("Referrer", "See [Target][target].\n\n[target]: target%2Emd?view=summary"),
        )
        self.commit()
        self.write("wiki/target.md", concept("Target", "Changed."))

        result = self.run_validator("--changed", "wiki/target.md")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)

    def test_changed_without_paths_discovers_worktree_changes(self) -> None:
        self.write("wiki/target.md", concept("Target", "Original."))
        self.write("wiki/referrer.md", concept("Referrer", "See [Target](target.md)."))
        self.commit()
        self.write("wiki/target.md", concept("Target", "Changed."))

        result = self.run_validator("--changed")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DIRECT: wiki/target.md", result.stdout)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)

    def test_deleted_file_selects_files_that_still_refer_to_its_old_path(self) -> None:
        self.write("wiki/target.md", concept("Target"))
        self.write("wiki/referrer.md", concept("Referrer", "See [Target](target.md)."))
        self.commit()
        (self.root / "wiki/target.md").unlink()

        result = self.run_validator("--changed", "wiki/target.md")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DIRECT: wiki/target.md", result.stdout)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)
        self.assertIn("SCHEMA: wiki/referrer.md: broken link target.md", result.stdout)

    def test_rename_selects_the_new_file_and_old_path_referrers(self) -> None:
        self.write("wiki/target.md", concept("Target"))
        self.write("wiki/referrer.md", concept("Referrer", "See [Target](target.md)."))
        self.commit()
        self.git("mv", "wiki/target.md", "wiki/renamed.md")

        result = self.run_validator("--changed", "wiki/renamed.md")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DIRECT: wiki/renamed.md", result.stdout)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)
        self.assertIn("SCHEMA: wiki/referrer.md: broken link target.md", result.stdout)

    def test_explicit_added_file_does_not_pull_unrelated_deletion_into_scope(self) -> None:
        self.write("wiki/deleted.md", concept("Deleted"))
        self.write("wiki/referrer.md", concept("Referrer", "See [Deleted](deleted.md)."))
        self.commit()
        (self.root / "wiki/deleted.md").unlink()
        self.write("wiki/new.md", concept("New"))

        result = self.run_validator("--changed", "wiki/new.md")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DIRECT: wiki/new.md", result.stdout)
        self.assertNotIn("wiki/deleted.md", result.stdout)
        self.assertNotIn("wiki/referrer.md", result.stdout)

    def test_untracked_rename_target_still_selects_old_path_referrers(self) -> None:
        self.write("wiki/target.md", concept("Target"))
        self.write("wiki/referrer.md", concept("Referrer", "See [Target](target.md)."))
        self.commit()
        (self.root / "wiki/target.md").unlink()
        self.write("wiki/renamed.md", concept("Renamed", "Entirely new content."))

        result = self.run_validator("--changed", "wiki/target.md", "wiki/renamed.md")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DIRECT: wiki/target.md", result.stdout)
        self.assertIn("DIRECT: wiki/renamed.md", result.stdout)
        self.assertIn("DEPENDENT: wiki/referrer.md", result.stdout)
        self.assertIn("SCHEMA: wiki/referrer.md: broken link target.md", result.stdout)

    def test_tag_definition_change_selects_every_file_using_the_tag(self) -> None:
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\n"
            "- `test`: Used by validator fixtures.\n"
            "- `topic`: Old meaning.\n",
        )
        self.write("wiki/tagged.md", concept("Tagged", tags="[topic]"))
        self.write("wiki/unrelated.md", concept("Unrelated"))
        self.commit()
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\n"
            "- `test`: Used by validator fixtures.\n"
            "- `topic`: New meaning.\n",
        )

        result = self.run_validator("--changed", "references/local-settings.md")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DIRECT: references/local-settings.md", result.stdout)
        self.assertIn("DEPENDENT: wiki/tagged.md", result.stdout)
        self.assertNotIn("wiki/unrelated.md", result.stdout)

    def test_tag_change_selects_yaml_escaped_tag_value(self) -> None:
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\n- `topic`: Old meaning.\n",
        )
        self.write("wiki/tagged.md", concept("Escaped tag", tags=r'["top\u0069c"]'))
        self.commit()
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\n- `topic`: New meaning.\n",
        )

        result = self.run_validator("--changed", "references/local-settings.md")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DEPENDENT: wiki/tagged.md", result.stdout)

    def test_tag_deletion_selects_users_and_reports_unapproved_tag(self) -> None:
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\n- `topic`: Use for topics.\n",
        )
        self.write("wiki/tagged.md", concept("Tagged", tags="[topic]"))
        self.commit()
        self.write(
            "references/local-settings.md",
            "# Local Settings\n\n## Tag Registry\n\nNo tags are approved yet.\n",
        )

        result = self.run_validator("--changed", "references/local-settings.md")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DEPENDENT: wiki/tagged.md", result.stdout)
        self.assertIn("SCHEMA: wiki/tagged.md: unapproved tag topic", result.stdout)

    def test_root_index_reports_a_missing_concept_entry(self) -> None:
        self.write("wiki/topic.md", concept("Topic"))

        result = self.run_validator("--all", sync_index=False)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/index.md: missing concept entry wiki/topic.md", result.stdout)

    def test_root_index_reports_a_duplicate_concept_entry(self) -> None:
        self.write("wiki/topic.md", concept("Topic"))
        self.write(
            "wiki/index.md",
            '---\nokf_version: "0.2"\n---\n\n# Knowledge Base\n\n'
            "* [Topic](topic.md)\n"
            "* [Topic again](topic.md)\n",
        )

        result = self.run_validator("--all", sync_index=False)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/index.md: duplicate concept entry wiki/topic.md", result.stdout)

    def test_root_index_reports_an_invalid_target(self) -> None:
        self.write(
            "wiki/index.md",
            '---\nokf_version: "0.2"\n---\n\n# Knowledge Base\n\n'
            "* [Missing](missing.md)\n",
        )

        result = self.run_validator("--all", sync_index=False)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/index.md: broken link missing.md", result.stdout)

    def test_broken_internal_link_is_a_local_schema_failure(self) -> None:
        self.write("wiki/topic.md", concept("Topic", "See [Missing](missing.md)."))

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/topic.md: broken link missing.md", result.stdout)

    def test_retired_snapshot_metadata_is_preserved_as_an_unknown_field(self) -> None:
        for value in ("true", "false"):
            with self.subTest(value=value):
                imported = concept("Imported").replace(
                    "type: Note\n", f"type: Note\nsnapshot: {value}\n",
                )
                self.write("wiki/imported.md", imported)

                result = self.run_validator("--all")

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((self.root / "wiki/imported.md").read_text(), imported)

    def test_dated_analysis_accepts_external_evidence_without_special_fields(self) -> None:
        analysis = concept(
            "Demand assessment",
            "Assessment as of 2026-08-01. Finding.[^report]\n\n"
            "[^report]: [Report](https://example.com/report)",
        ).replace(
            "type: Note\n",
            "type: Analysis\nsources:\n"
            "  - id: report\n    resource: https://example.com/report\n",
        )
        self.write("wiki/assessment.md", analysis)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_retired_source_representation_is_rejected(self) -> None:
        self.write("raw/report.pdf", "evidence")
        self.write("raw/report.md", "rendering")
        topic = concept(
            "Topic",
            "Claim.[^report]\n\n[^report]: [Report](../raw/report.pdf)",
        ).replace(
            "generated:\n",
            "sources:\n  - id: report\n    resource: ../raw/report.pdf\n"
            "    representation: ../raw/report.md\ngenerated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("SCHEMA: wiki/topic.md: sources[0].representation is not supported", result.stdout)

    def test_source_requires_stable_id(self) -> None:
        self.write("raw/report.pdf", "evidence")
        topic = concept("Topic").replace(
            "generated:\n",
            "sources:\n  - resource: ../raw/report.pdf\ngenerated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "SCHEMA: wiki/topic.md: sources[0].id is required",
            result.stdout,
        )

    def test_addressable_source_footnote_requires_resource_link(self) -> None:
        self.write("raw/report.pdf", "evidence")
        topic = concept("Topic", "Claim.[^report]\n\n[^report]: Report").replace(
            "generated:\n",
            "sources:\n  - id: report\n    resource: ../raw/report.pdf\ngenerated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "SCHEMA: wiki/topic.md: source report footnote must link to ../raw/report.pdf",
            result.stdout,
        )

    def test_addressable_source_footnote_accepts_resource_link(self) -> None:
        self.write("raw/report.pdf", "evidence")
        topic = concept(
            "Topic",
            "Claim.[^report]\n\n[^report]: [Report](../raw/report.pdf)",
        ).replace(
            "generated:\n",
            "sources:\n  - id: report\n    resource: ../raw/report.pdf\ngenerated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_external_source_footnote_requires_resource_link(self) -> None:
        topic = concept("Topic", "Claim.[^report]\n\n[^report]: Report").replace(
            "generated:\n",
            "sources:\n  - id: report\n    resource: https://example.com/report\ngenerated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "SCHEMA: wiki/topic.md: source report footnote must link to https://example.com/report",
            result.stdout,
        )

    def test_non_addressable_source_scope_accepts_plain_footnote(self) -> None:
        topic = concept("Topic", "Claim.[^queries]\n\n[^queries]: Product queries").replace(
            "generated:\n",
            "sources:\n  - id: queries\n    resource: all product queries\ngenerated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_verification_before_generation_is_reported(self) -> None:
        topic = concept("Topic").replace(
            "generated:\n",
            'verified: { by: test-agent/1.0, at: "2026-08-26T12:00:00+02:00" }\n'
            "generated:\n",
        )
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARNING: wiki/topic.md: verification predates latest meaningful content change",
            result.stdout,
        )

    def test_generated_at_requires_seconds_and_timezone(self) -> None:
        for value in (
            "2026-09-03",
            "2026-09-03T14:30",
            "2026-09-03T14:30:00",
        ):
            with self.subTest(value=value):
                topic = concept("Topic").replace(
                    '"2026-08-27T12:00:00+02:00"',
                    f'"{value}"',
                )
                self.write("wiki/topic.md", topic)

                result = self.run_validator("--all")

                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(
                    "generated.at must be an ISO 8601 datetime with seconds and timezone",
                    result.stdout,
                )

    def test_generated_at_accepts_seconds_and_timezone(self) -> None:
        for value in (
            "2026-09-03T14:30:00Z",
            "2026-09-03T16:30:00+02:00",
        ):
            with self.subTest(value=value):
                topic = concept("Topic").replace(
                    '"2026-08-27T12:00:00+02:00"',
                    f'"{value}"',
                )
                self.write("wiki/topic.md", topic)

                result = self.run_validator("--all")

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reached_stale_after_is_reported(self) -> None:
        topic = concept("Topic").replace("generated:\n", "stale_after: 2000-01-01\ngenerated:\n")
        self.write("wiki/topic.md", topic)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARNING: wiki/topic.md: stale since 2000-01-01", result.stdout)

    def test_unknown_type_and_field_remain_accepted(self) -> None:
        imported = concept("Imported").replace(
            "type: Note\n",
            "type: Imported Type\nfuture_field: preserved\n",
        )
        self.write("wiki/imported.md", imported)

        result = self.run_validator("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_full_modes_preserve_existing_interfaces(self) -> None:
        self.write("wiki/invalid.md", "---\ntitle: Invalid\n---\n")

        results = [
            self.run_validator("--all"),
            self.run_validator(),
            subprocess.run(
                [sys.executable, str(SCRIPT), str(self.root)],
                capture_output=True,
                text=True,
            ),
        ]

        for result in results:
            with self.subTest(arguments=result.args):
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Validation mode: all", result.stdout)
                self.assertIn("BASE: wiki/invalid.md: type must be non-empty", result.stdout)

    def test_changed_mode_without_git_history_falls_back_to_full_validation(self) -> None:
        self.write("wiki/good.md", concept("Good"))
        self.write("wiki/invalid.md", "---\ntitle: Invalid\n---\n")
        git_directory = self.root / ".git"
        for path in sorted(git_directory.rglob("*"), reverse=True):
            if path.is_file() or path.is_symlink():
                path.unlink()
            else:
                path.rmdir()
        git_directory.rmdir()

        result = self.run_validator("--changed", "wiki/good.md")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("NOTICE: Git history unavailable; running full validation.", result.stdout)
        self.assertIn("BASE: wiki/invalid.md: type must be non-empty", result.stdout)


if __name__ == "__main__":
    unittest.main()
