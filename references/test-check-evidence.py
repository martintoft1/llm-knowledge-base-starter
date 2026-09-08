#!/usr/bin/env python3
"""Regression tests for structural evidence checking."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-evidence.py").resolve()


def concept(title: str, sources: str = "", resource: str = "") -> str:
    resource_field = f"resource: {resource}\n" if resource else ""
    sources_field = f"sources:\n{sources}" if sources else ""
    return f'''---
type: Reference
title: {title}
status: draft
tags: []
{resource_field}{sources_field}generated:
  by: test-agent/1.0
  at: "2026-08-31T12:00:00+02:00"
---

# {title}

Knowledge.[^report]

[^report]: Source
'''


def source(resource: str) -> str:
    return f"  - resource: {resource}\n"


class EvidenceCheckerCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "raw").mkdir()
        (self.root / "wiki").mkdir()
        self.write("raw/.gitkeep", "")
        self.write("wiki/index.md", '---\nokf_version: "0.2"\n---\n\n# Knowledge Base\n')
        self.write("wiki/log.md", "# Directory Update Log\n")
        self.git("init", "-q")
        self.git("config", "user.email", "evidence@example.test")
        self.git("config", "user.name", "Evidence Test")

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
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def run_checker(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *arguments],
            capture_output=True,
            text=True,
        )

    def test_routine_check_does_not_read_or_compare_raw_content(self) -> None:
        (self.root / "raw/report.txt").write_bytes(b"\xff\xfeunreadable source")
        self.write("wiki/topic.md", concept("Topic", source("../raw/report.txt")))

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Evidence errors: 0", result.stdout)
        self.assertIn("Warnings: 0", result.stdout)
        self.assertNotIn("Fidelity suspects", result.stdout)

    def test_missing_local_original_is_an_evidence_error(self) -> None:
        self.write("wiki/topic.md", concept("Topic", source("../raw/missing.txt")))

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "ERROR: wiki/topic.md: missing sources[0].resource ../raw/missing.txt",
            result.stdout,
        )

    def test_external_source_is_reported_as_not_locally_checkable(self) -> None:
        self.write("wiki/topic.md", concept("Topic", source("https://example.com/report")))

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARNING: wiki/topic.md: sources[0].resource is external or not locally checkable",
            result.stdout,
        )

    def test_referenced_raw_original_is_accepted(self) -> None:
        self.write("raw/report.txt", "Evidence.")
        self.write("wiki/topic.md", concept("Topic", source("../raw/report.txt")))

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Evidence errors: 0", result.stdout)

    def test_concept_resource_counts_as_a_raw_reference(self) -> None:
        self.write("raw/catalog.pdf", "Evidence.")
        self.write("wiki/catalog.md", concept("Catalog", resource="../raw/catalog.pdf"))

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_retained_but_unused_log_entry_does_not_resolve_inventory(self) -> None:
        self.write("raw/report.txt", "Evidence.")
        self.write(
            "wiki/log.md",
            "# Directory Update Log\n\n## 2026-08-31\n\n"
            "* **Ingest**: Retained but unused `raw/report.txt` — duplicate.\n",
        )

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "ERROR: raw/report.txt: retained raw source is not referenced by a wiki concept",
            result.stdout,
        )

    def test_unreferenced_raw_original_is_an_error(self) -> None:
        self.write("raw/forgotten.txt", "Evidence.")

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "ERROR: raw/forgotten.txt: retained raw source is not referenced by a wiki concept",
            result.stdout,
        )

    def test_gitkeep_is_excluded_from_inventory(self) -> None:
        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("raw/.gitkeep", result.stdout)

    def test_removed_derived_directory_is_rejected(self) -> None:
        self.write("raw/_derived/report.md", "Derived copy.")
        self.write("wiki/topic.md", concept("Topic", source("../raw/_derived/report.md")))

        result = self.run_checker("--all")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "ERROR: raw/_derived/report.md: raw/_derived is not supported",
            result.stdout,
        )

    def test_changed_mode_checks_only_selected_concepts(self) -> None:
        self.write("raw/good.txt", "Evidence.")
        self.write("wiki/good.md", concept("Good", source("../raw/good.txt")))
        self.write("wiki/bad.md", concept("Bad", source("../raw/missing.txt")))
        self.commit()

        changed = self.run_checker("--changed", "wiki/good.md")
        complete = self.run_checker("--all")

        self.assertEqual(changed.returncode, 0, changed.stdout + changed.stderr)
        self.assertIn("Evidence check mode: changed", changed.stdout)
        self.assertIn("DIRECT: wiki/good.md", changed.stdout)
        self.assertNotIn("wiki/bad.md", changed.stdout)
        self.assertEqual(complete.returncode, 1, complete.stdout + complete.stderr)
        self.assertIn("ERROR: wiki/bad.md: missing sources[0].resource", complete.stdout)

    def test_changed_raw_path_selects_concepts_that_reference_it(self) -> None:
        self.write("raw/report.txt", "Original evidence.")
        self.write("wiki/topic.md", concept("Topic", source("../raw/report.txt")))
        self.commit()
        self.write("raw/report.txt", "Changed evidence.")

        result = self.run_checker("--changed", "raw/report.txt")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DIRECT: raw/report.txt", result.stdout)
        self.assertIn("DEPENDENT: wiki/topic.md", result.stdout)
        self.assertIn("Checked 1 concept file.", result.stdout)


if __name__ == "__main__":
    unittest.main()
