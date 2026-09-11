#!/usr/bin/env python3
"""Integration tests for the operating-kit migration command."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("migrate.py").resolve()
REPOSITORY = "https://github.com/martintoft1/llm-knowledge-base-starter.git"


def load_migrator():
    spec = importlib.util.spec_from_file_location("migrator_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load migration script")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_manifest(self, **overrides: object) -> None:
        data: dict[str, object] = {
            "format_version": 2,
            "repository": REPOSITORY,
            "release_version": "0.2.0",
            "managed_paths": [
                "VERSION",
                "README.md",
                "references/migration-manifest.json",
            ],
            "preserved_paths": [".git", ".migration", "raw", "wiki"],
            "preserve_unknown_paths": True,
            "merged_paths": [
                {
                    "path": "references/local-settings.md",
                    "strategy": "target-structure",
                }
            ],
            "transitions": [
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": ["references/migration-manifest.json"],
                    "removed_paths": ["legacy.md"],
                }
            ],
        }
        data.update(overrides)
        path = self.root / "references/migration-manifest.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def load_manifest(self, **overrides: object):
        self.write_manifest(**overrides)
        return load_migrator().load_manifest(self.root)

    def test_manifest_v2_loads_typed_policy(self) -> None:
        self.write_manifest()
        migrator = load_migrator()

        manifest = migrator.load_manifest(self.root)

        self.assertEqual(manifest.release_version, (0, 2, 0))
        self.assertEqual(
            manifest.preserved_paths,
            (".git", ".migration", "raw", "wiki"),
        )
        self.assertTrue(manifest.preserve_unknown_paths)
        self.assertEqual(
            manifest.merged_paths,
            (
                migrator.MergeRule(
                    "references/local-settings.md",
                    "target-structure",
                ),
            ),
        )
        self.assertEqual(manifest.transitions[0].source, (0, 1, 0))
        self.assertEqual(manifest.transitions[0].target, (0, 2, 0))

    def test_manifest_requires_mandatory_preserved_paths(self) -> None:
        self.write_manifest(preserved_paths=[".git", ".migration", "raw"])
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "missing mandatory preserved paths: wiki",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_requires_unknown_path_preservation(self) -> None:
        self.write_manifest(preserve_unknown_paths=False)
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "must preserve unknown paths",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_unsupported_merge_strategy(self) -> None:
        self.write_manifest(
            merged_paths=[
                {
                    "path": "references/local-settings.md",
                    "strategy": "append",
                }
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "unsupported merge strategy: append",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_nonstring_merge_strategy_cleanly(self) -> None:
        self.write_manifest(
            merged_paths=[
                {
                    "path": "references/local-settings.md",
                    "strategy": [],
                }
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "unsupported merge strategy",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_overlapping_path_categories(self) -> None:
        self.write_manifest(
            managed_paths=[
                "VERSION",
                "references/local-settings.md",
                "references/migration-manifest.json",
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "managed and merged paths: references/local-settings.md",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_managed_content_under_preserved_path(self) -> None:
        self.write_manifest(
            managed_paths=[
                "VERSION",
                "references/migration-manifest.json",
                "wiki/topic.md",
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "protected path: wiki/topic.md",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_must_manage_version_and_itself(self) -> None:
        self.write_manifest(managed_paths=["VERSION", "README.md"])
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "must manage VERSION and references/migration-manifest.json",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_unknown_top_level_fields(self) -> None:
        self.write_manifest(unexpected=True)
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "manifest fields are invalid",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_nonstring_release_version_cleanly(self) -> None:
        self.write_manifest(release_version=2)
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "manifest release_version must be a stable semantic version",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_requires_local_settings_merger(self) -> None:
        self.write_manifest(merged_paths=[])
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "must merge references/local-settings.md",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_nonforward_transition(self) -> None:
        self.write_manifest(
            transitions=[
                {
                    "from": "0.2.0",
                    "to": "0.1.0",
                    "added_paths": [],
                    "removed_paths": [],
                }
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "transition target must be newer",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_transition_path_overlap(self) -> None:
        self.write_manifest(
            transitions=[
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": ["same.md"],
                    "removed_paths": ["same.md"],
                }
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "added and removed paths overlap",
        ):
            migrator.load_manifest(self.root)

    def test_manifest_rejects_protected_transition_path(self) -> None:
        self.write_manifest(
            transitions=[
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": [],
                    "removed_paths": ["raw/source.md"],
                }
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "transition contains protected path: raw/source.md",
        ):
            migrator.load_manifest(self.root)

    def test_v0_1_0_route_reconstructs_source_ownership_without_manifest(self) -> None:
        migrator = load_migrator()
        manifest = self.load_manifest()

        route = migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))
        source_paths = migrator.reconstruct_source_paths(manifest, route)

        self.assertEqual(len(route), 1)
        self.assertEqual(
            set(source_paths),
            {"VERSION", "README.md", "legacy.md"},
        )

    def test_skipped_release_composes_adjacent_transitions(self) -> None:
        migrator = load_migrator()
        manifest = self.load_manifest(
            release_version="0.3.0",
            managed_paths=[
                "VERSION",
                "README.md",
                "current.md",
                "references/migration-manifest.json",
            ],
            transitions=[
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": [
                        "intermediate.md",
                        "references/migration-manifest.json",
                    ],
                    "removed_paths": ["legacy.md"],
                },
                {
                    "from": "0.2.0",
                    "to": "0.3.0",
                    "added_paths": ["current.md"],
                    "removed_paths": ["intermediate.md"],
                },
            ],
        )

        route = migrator.select_route(manifest, (0, 1, 0), (0, 3, 0))
        source_paths = migrator.reconstruct_source_paths(manifest, route)

        self.assertEqual(
            [(item.source, item.target) for item in route],
            [((0, 1, 0), (0, 2, 0)), ((0, 2, 0), (0, 3, 0))],
        )
        self.assertEqual(
            set(source_paths),
            {"VERSION", "README.md", "legacy.md"},
        )

    def test_route_rejects_gap(self) -> None:
        migrator = load_migrator()
        manifest = self.load_manifest(transitions=[])

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "no transition from 0.1.0",
        ):
            migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))

    def test_route_rejects_fork(self) -> None:
        migrator = load_migrator()
        transition = {
            "from": "0.1.0",
            "to": "0.2.0",
            "added_paths": ["references/migration-manifest.json"],
            "removed_paths": ["legacy.md"],
        }
        manifest = self.load_manifest(transitions=[transition, transition])

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "multiple transitions from 0.1.0",
        ):
            migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))

    def test_route_rejects_transition_beyond_target(self) -> None:
        migrator = load_migrator()
        manifest = self.load_manifest(
            transitions=[
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": ["references/migration-manifest.json"],
                    "removed_paths": ["legacy.md"],
                },
                {
                    "from": "0.2.0",
                    "to": "0.3.0",
                    "added_paths": ["future.md"],
                    "removed_paths": [],
                },
            ]
        )

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "transition beyond target release",
        ):
            migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))

    def test_route_rejects_disconnected_transition(self) -> None:
        migrator = load_migrator()
        manifest = self.load_manifest(
            transitions=[
                {
                    "from": "0.0.1",
                    "to": "0.0.2",
                    "added_paths": [],
                    "removed_paths": [],
                },
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": ["references/migration-manifest.json"],
                    "removed_paths": ["legacy.md"],
                },
            ]
        )

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "single contiguous chain",
        ):
            migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))

    def test_ownership_reconstruction_rejects_inconsistent_addition(self) -> None:
        migrator = load_migrator()
        manifest = self.load_manifest(
            transitions=[
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": ["missing-from-target.md"],
                    "removed_paths": ["legacy.md"],
                }
            ]
        )
        route = migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "added path is absent from its target state",
        ):
            migrator.reconstruct_source_paths(manifest, route)

    def test_v0_1_0_without_manifest_uses_reconstructed_ownership(self) -> None:
        migrator = load_migrator()
        expected = ("README.md", "VERSION", "legacy.md")

        paths = migrator.load_source_paths(self.root, (0, 1, 0), expected)

        self.assertEqual(paths, expected)

    def test_nonlegacy_source_without_manifest_is_rejected(self) -> None:
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "migration manifest not found",
        ):
            migrator.load_source_paths(
                self.root,
                (0, 2, 0),
                ("README.md", "VERSION"),
            )

    def test_installed_manifest_must_match_reconstructed_ownership(self) -> None:
        self.write_manifest(
            managed_paths=[
                "VERSION",
                "unexpected.md",
                "references/migration-manifest.json",
            ]
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(
            migrator.MigrationError,
            "installed manifest differs from transition ledger",
        ):
            migrator.load_source_paths(
                self.root,
                (0, 2, 0),
                ("VERSION", "references/migration-manifest.json"),
            )


class MigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.root = self.base / "knowledge-base"
        self.remote = self.base / "upstream"
        self.root.mkdir()
        self.remote.mkdir()

        self.source_paths = [
            "VERSION",
            "README.md",
            "unchanged.md",
            "obsolete.md",
            "references/migration-manifest.json",
        ]
        self.write(self.root, "VERSION", "1.0.0\n")
        self.write(self.root, "README.md", "old readme\n")
        self.write(self.root, "unchanged.md", "same\n")
        self.write(self.root, "obsolete.md", "old managed file\n")
        self.write(self.root, "references/local-settings.md", "local values\n")
        self.write(self.root, "raw/source.txt", "retained source\n")
        self.write(self.root, "wiki/topic.md", "local knowledge\n")
        self.write(self.root, "notes.md", "unknown local file\n")
        self.write_manifest(self.root, "1.0.0", self.source_paths, [])

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    @staticmethod
    def write(root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_manifest(
        self,
        root: Path,
        release_version: str,
        managed_paths: list[str],
        transitions: list[dict[str, object]],
    ) -> None:
        self.write(
            root,
            "references/migration-manifest.json",
            json.dumps(
                {
                    "format_version": 2,
                    "repository": REPOSITORY,
                    "release_version": release_version,
                    "managed_paths": managed_paths,
                    "preserved_paths": [".git", ".migration", "raw", "wiki"],
                    "preserve_unknown_paths": True,
                    "merged_paths": [
                        {
                            "path": "references/local-settings.md",
                            "strategy": "target-structure",
                        }
                    ],
                    "transitions": transitions,
                },
                indent=2,
            )
            + "\n",
        )

    @staticmethod
    def git(root: Path, *arguments: str) -> str:
        result = subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def publish(
        self,
        version: str = "1.1.0",
        managed_paths: list[str] | None = None,
        transitions: list[dict[str, object]] | None = None,
    ) -> None:
        managed_paths = managed_paths or [
            "VERSION",
            "README.md",
            "unchanged.md",
            "new.md",
            "references/migration-manifest.json",
        ]
        transitions = transitions or [
            {
                "from": "1.0.0",
                "to": version,
                "added_paths": ["new.md"],
                "removed_paths": ["obsolete.md"],
            }
        ]
        self.write(self.remote, "VERSION", f"{version}\n")
        self.write(self.remote, "README.md", f"new {version} readme\n")
        self.write(self.remote, "unchanged.md", "same\n")
        self.write(self.remote, "new.md", "new managed file\n")
        self.write(
            self.remote,
            "references/local-settings.md",
            "target settings structure\n",
        )
        self.write_manifest(self.remote, version, managed_paths, transitions)
        if not (self.remote / ".git").exists():
            self.git(self.remote, "init", "-q")
            self.git(self.remote, "config", "user.email", "migration@example.test")
            self.git(self.remote, "config", "user.name", "Migration Test")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-qm", f"release {version}")
        self.git(self.remote, "tag", "-a", f"v{version}", "-m", f"release {version}")

    def migrate(self, target: str = "latest"):
        migrator = load_migrator()
        with contextlib.redirect_stdout(io.StringIO()):
            result = migrator.migrate(
                self.root,
                target=target,
                repository=self.remote.as_uri(),
            )
        return migrator, result

    def test_migration_overlays_target_and_removes_only_retired_owned_paths(self) -> None:
        self.publish()

        _migrator, result = self.migrate()

        self.assertEqual((self.root / "VERSION").read_text(), "1.1.0\n")
        self.assertEqual((self.root / "README.md").read_text(), "new 1.1.0 readme\n")
        self.assertEqual((self.root / "new.md").read_text(), "new managed file\n")
        self.assertFalse((self.root / "obsolete.md").exists())
        self.assertEqual((self.root / "unchanged.md").read_text(), "same\n")

    def test_migration_preserves_protected_and_unknown_paths(self) -> None:
        self.publish()

        _migrator, _result = self.migrate()

        self.assertEqual(
            (self.root / "references/local-settings.md").read_text(),
            "local values\n",
        )
        self.assertEqual((self.root / "raw/source.txt").read_text(), "retained source\n")
        self.assertEqual((self.root / "wiki/topic.md").read_text(), "local knowledge\n")
        self.assertEqual((self.root / "notes.md").read_text(), "unknown local file\n")

    def test_migration_backs_up_only_existing_modified_and_merged_files(self) -> None:
        self.publish()

        _migrator, result = self.migrate()

        self.assertEqual((result.backup / "README.md").read_text(), "old readme\n")
        self.assertEqual(
            (result.backup / "obsolete.md").read_text(),
            "old managed file\n",
        )
        self.assertEqual(
            (result.backup / "references/local-settings.md").read_text(),
            "local values\n",
        )
        self.assertFalse((result.backup / "new.md").exists())
        self.assertFalse((result.backup / "unchanged.md").exists())
        self.assertFalse((result.backup / "raw/source.txt").exists())
        self.assertFalse((result.backup / "wiki/topic.md").exists())
        self.assertFalse((result.backup / "notes.md").exists())

    def test_merge_artifact_contains_source_and_target_settings(self) -> None:
        self.publish()

        _migrator, result = self.migrate()

        self.assertEqual(len(result.merges), 1)
        merge = result.merges[0]
        self.assertEqual(merge.path, "references/local-settings.md")
        self.assertEqual(merge.source.read_text(), "local values\n")
        self.assertEqual(
            merge.target.read_text(),
            "target settings structure\n",
        )

    def test_action_record_captures_versions_commit_and_actions(self) -> None:
        self.publish()

        _migrator, result = self.migrate()
        record = json.loads(result.action_record.read_text(encoding="utf-8"))

        self.assertEqual(record["source_version"], "1.0.0")
        self.assertEqual(record["target_version"], "1.1.0")
        self.assertEqual(record["release_commit"], result.commit)
        self.assertEqual(
            record["route"],
            [{"from": "1.0.0", "to": "1.1.0"}],
        )
        self.assertIn(
            {"kind": "merge", "path": "references/local-settings.md"},
            record["actions"],
        )

    def test_latest_ignores_prerelease_tags(self) -> None:
        self.publish()
        self.git(self.remote, "tag", "v2.0.0-rc1")

        _migrator, result = self.migrate()

        self.assertEqual(result.version, "1.1.0")

    def test_new_managed_path_cannot_overwrite_an_unknown_file(self) -> None:
        self.write(self.remote, "notes.md", "upstream note\n")
        self.publish(
            managed_paths=[
                "VERSION",
                "README.md",
                "unchanged.md",
                "notes.md",
                "references/migration-manifest.json",
            ],
            transitions=[
                {
                    "from": "1.0.0",
                    "to": "1.1.0",
                    "added_paths": ["notes.md"],
                    "removed_paths": ["obsolete.md"],
                }
            ],
        )
        migrator = load_migrator()

        with self.assertRaisesRegex(migrator.MigrationError, "unowned path: notes.md"):
            migrator.migrate(
                self.root,
                target="latest",
                repository=self.remote.as_uri(),
            )

        self.assertEqual((self.root / "VERSION").read_text(), "1.0.0\n")
        self.assertEqual((self.root / "notes.md").read_text(), "unknown local file\n")

    def test_nonlegacy_source_without_manifest_is_rejected(self) -> None:
        (self.root / "references/migration-manifest.json").unlink()
        self.publish()
        migrator = load_migrator()

        with self.assertRaisesRegex(migrator.MigrationError, "migration manifest not found"):
            migrator.migrate(
                self.root,
                target="latest",
                repository=self.remote.as_uri(),
            )

        self.assertEqual((self.root / "VERSION").read_text(), "1.0.0\n")

    def test_v0_1_0_migrates_without_an_installed_manifest(self) -> None:
        self.write(self.root, "VERSION", "0.1.0\n")
        (self.root / "references/migration-manifest.json").unlink()
        self.publish(
            version="0.2.0",
            managed_paths=[
                "VERSION",
                "README.md",
                "unchanged.md",
                "new.md",
                "references/migration-manifest.json",
            ],
            transitions=[
                {
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "added_paths": [
                        "new.md",
                        "references/migration-manifest.json",
                    ],
                    "removed_paths": ["obsolete.md"],
                }
            ],
        )

        _migrator, result = self.migrate(target="0.2.0")

        self.assertEqual(result.version, "0.2.0")
        self.assertFalse((self.root / "obsolete.md").exists())
        self.assertEqual((self.root / "notes.md").read_text(), "unknown local file\n")
        self.assertEqual((self.root / "raw/source.txt").read_text(), "retained source\n")
        self.assertEqual((self.root / "wiki/topic.md").read_text(), "local knowledge\n")

    def test_skipped_release_uses_every_adjacent_transition(self) -> None:
        transitions = [
            {
                "from": "1.0.0",
                "to": "1.1.0",
                "added_paths": ["intermediate.md"],
                "removed_paths": ["obsolete.md"],
            },
            {
                "from": "1.1.0",
                "to": "1.2.0",
                "added_paths": ["new.md"],
                "removed_paths": ["intermediate.md"],
            },
        ]
        self.publish(version="1.1.0")
        (self.remote / "new.md").unlink()
        self.write(self.remote, "intermediate.md", "intermediate\n")
        self.write_manifest(
            self.remote,
            "1.1.0",
            [
                "VERSION",
                "README.md",
                "unchanged.md",
                "intermediate.md",
                "references/migration-manifest.json",
            ],
            transitions[:1],
        )
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-qm", "correct release 1.1.0")
        self.git(self.remote, "tag", "-f", "v1.1.0")
        (self.remote / "intermediate.md").unlink()
        self.write(self.remote, "VERSION", "1.2.0\n")
        self.write(self.remote, "README.md", "new 1.2.0 readme\n")
        self.write(self.remote, "new.md", "new managed file\n")
        self.write_manifest(
            self.remote,
            "1.2.0",
            [
                "VERSION",
                "README.md",
                "unchanged.md",
                "new.md",
                "references/migration-manifest.json",
            ],
            transitions,
        )
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-qm", "release 1.2.0")
        self.git(self.remote, "tag", "-a", "v1.2.0", "-m", "release 1.2.0")

        _migrator, result = self.migrate(target="1.2.0")

        self.assertEqual(
            result.route,
            (((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (1, 2, 0))),
        )
        self.assertEqual((self.root / "VERSION").read_text(), "1.2.0\n")
        self.assertEqual((self.root / "new.md").read_text(), "new managed file\n")
        self.assertFalse((self.root / "obsolete.md").exists())
        self.assertFalse((self.root / "intermediate.md").exists())

    def test_failed_write_restores_all_managed_files(self) -> None:
        self.publish()
        migrator = load_migrator()
        real_replace = migrator.replace_file

        def fail_on_new_version(source: Path, destination: Path) -> None:
            if destination.name == "VERSION" and source.read_text() == "1.1.0\n":
                raise OSError("simulated write failure")
            real_replace(source, destination)

        with mock.patch.object(migrator, "replace_file", side_effect=fail_on_new_version):
            with self.assertRaisesRegex(migrator.MigrationError, "restored from"):
                migrator.migrate(
                    self.root,
                    target="latest",
                    repository=self.remote.as_uri(),
                )

        self.assertEqual((self.root / "VERSION").read_text(), "1.0.0\n")
        self.assertEqual((self.root / "README.md").read_text(), "old readme\n")
        self.assertFalse((self.root / "new.md").exists())
        self.assertTrue((self.root / "obsolete.md").exists())


class ManifestCoverageTests(unittest.TestCase):
    def test_manifest_lists_all_distributed_operating_files(self) -> None:
        root = SCRIPT.parent.parent
        manifest = json.loads(
            (root / "references/migration-manifest.json").read_text(encoding="utf-8")
        )
        expected = {
            ".gitignore",
            "AGENTS.md",
            "CHANGELOG.md",
            "CLAUDE.md",
            "LICENSE",
            "NOTICE",
            "README.md",
            "VERSION",
        }
        for directory in (root / "references", root / "templates"):
            expected.update(
                path.relative_to(root).as_posix()
                for path in directory.rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.name != ".DS_Store"
                and path.name != "local-settings.md"
            )

        self.assertEqual(set(manifest["managed_paths"]), expected)

    def test_release_manifest_reconstructs_public_v0_1_0_ownership(self) -> None:
        root = SCRIPT.parent.parent
        migrator = load_migrator()

        manifest = migrator.load_manifest(root)
        route = migrator.select_route(manifest, (0, 1, 0), (0, 2, 0))
        source_paths = migrator.reconstruct_source_paths(manifest, route)

        self.assertEqual(manifest.release_version, (0, 2, 0))
        self.assertEqual(
            set(source_paths),
            {
                ".gitignore",
                "AGENTS.md",
                "CHANGELOG.md",
                "CLAUDE.md",
                "LICENSE",
                "NOTICE",
                "README.md",
                "VERSION",
                "references/initialization/BOOTSTRAP.md",
                "references/okf/v0.2/README.md",
                "references/okf/v0.2/SPEC.md",
                "references/okf/v0.2/UPSTREAM.md",
                "references/operations.md",
                "references/schema.md",
                "references/writing-style.md",
                "templates/index.md",
                "templates/log.md",
                "templates/page-bodies/analysis.md",
                "templates/page-bodies/attested-computation.md",
                "templates/page-bodies/database.md",
                "templates/page-bodies/dataset.md",
                "templates/page-bodies/decision.md",
                "templates/page-bodies/goal.md",
                "templates/page-bodies/plan.md",
                "templates/page-bodies/reference.md",
                "templates/page-bodies/source-record.md",
                "templates/wiki-page.md",
            },
        )


if __name__ == "__main__":
    unittest.main()
