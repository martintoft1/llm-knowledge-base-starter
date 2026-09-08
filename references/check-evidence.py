#!/usr/bin/env python3
"""Check evidence references and raw inventory without reading raw contents.

This checker never edits files and never replaces evidence review. Missing or
malformed local evidence is an error. External evidence is reported as not
locally checkable. Every retained raw original must be used by a wiki concept.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ModuleNotFoundError:
    print(
        "PyYAML is required. Install it with: python3 -m pip install PyYAML",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

EVIDENCE_ERRORS: list[str] = []
WARNINGS: list[str] = []

SKIP_WIKI_FILES = {"index.md", "log.md"}


def add_unique(messages: list[str], message: str) -> None:
    if message not in messages:
        messages.append(message)


def configure_root(root: Path) -> None:
    global ROOT, WIKI, RAW
    ROOT = root.resolve()
    WIKI = ROOT / "wiki"
    RAW = ROOT / "raw"


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    if not text.startswith("---\n"):
        return None, "missing frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, "unterminated frontmatter"
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as error:
        return None, f"invalid YAML: {error}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a mapping"
    return data, None


def read_utf8(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return None


def is_inside(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def local_target(source_file: Path, value: str) -> Path | None:
    cleaned = unquote(value.strip().strip("<>"))
    cleaned = cleaned.split("#", 1)[0].split("?", 1)[0]
    if not cleaned or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", cleaned):
        return None
    if cleaned.startswith("/"):
        return (WIKI / cleaned.lstrip("/")).resolve()
    return (source_file.parent / cleaned).resolve()


def local_resource_target(source_file: Path, value: object) -> Path | None:
    if not nonempty_string(value):
        return None
    if not any(mark in value for mark in ("/", "\\", ".")):
        return None
    return local_target(source_file, value)


def concept_paths() -> list[Path]:
    return sorted(
        path
        for path in WIKI.rglob("*.md")
        if path.name not in SKIP_WIKI_FILES
    )


def source_entries(data: dict) -> list[dict]:
    sources = data.get("sources")
    if not isinstance(sources, list):
        return []
    return [source for source in sources if isinstance(source, dict)]


def check_concept(path: Path) -> None:
    text = read_utf8(path)
    if text is None:
        add_unique(EVIDENCE_ERRORS, f"{relative(path)}: concept is not readable UTF-8 text")
        return
    data, error = parse_frontmatter(text)
    if error:
        add_unique(EVIDENCE_ERRORS, f"{relative(path)}: {error}")
        return
    assert data is not None

    for index, source in enumerate(source_entries(data)):
        label = f"{relative(path)}: sources[{index}]"
        resource_value = source.get("resource")
        if not nonempty_string(resource_value):
            add_unique(EVIDENCE_ERRORS, f"{label}.resource must be non-empty")
            continue
        resource = local_resource_target(path, resource_value)
        if resource is None:
            add_unique(
                WARNINGS,
                f"{label}.resource is external or not locally checkable: {resource_value}",
            )
            continue
        if not is_inside(resource, ROOT):
            add_unique(EVIDENCE_ERRORS, f"{label}.resource escapes the knowledge-base root: {resource_value}")
        elif not resource.is_file():
            add_unique(EVIDENCE_ERRORS, f"{relative(path)}: missing sources[{index}].resource {resource_value}")


def paths_from_frontmatter(path: Path, data: dict) -> list[Path]:
    paths: list[Path] = []
    resource = local_resource_target(path, data.get("resource"))
    if resource is not None:
        paths.append(resource)
    for source in source_entries(data):
        target = local_resource_target(path, source.get("resource"))
        if target is not None:
            paths.append(target)
    return paths


def concept_targets(path: Path) -> list[Path]:
    text = read_utf8(path)
    if text is None:
        return []
    data, error = parse_frontmatter(text)
    if error or data is None:
        return []
    return paths_from_frontmatter(path, data)


def referenced_raw_originals() -> set[Path]:
    referenced: set[Path] = set()
    for path in concept_paths():
        for target in concept_targets(path):
            if is_inside(target, RAW):
                referenced.add(target.resolve())
    return referenced


def raw_originals() -> list[Path]:
    if not RAW.is_dir():
        return []
    return sorted(
        path
        for path in RAW.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    )


def check_inventory(candidates: list[Path]) -> None:
    referenced = referenced_raw_originals()
    removed_directory = RAW / "_derived"
    for path in candidates:
        resolved = path.resolve()
        if is_inside(resolved, removed_directory):
            add_unique(EVIDENCE_ERRORS, f"{relative(path)}: raw/_derived is not supported")
        elif resolved not in referenced:
            add_unique(
                EVIDENCE_ERRORS,
                f"{relative(path)}: retained raw source is not referenced by a wiki concept",
            )


def git_command(*arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )


def has_git_history() -> bool:
    return git_command("rev-parse", "--verify", "HEAD^{commit}").returncode == 0


def git_changes() -> list[tuple[str, tuple[str, ...]]]:
    result = git_command("diff", "--name-status", "-z", "--find-renames", "HEAD", "--")
    if result.returncode != 0:
        raise RuntimeError("could not read Git changes")
    parts = result.stdout.split(b"\0")
    if parts and not parts[-1]:
        parts.pop()
    changes: list[tuple[str, tuple[str, ...]]] = []
    index = 0
    while index < len(parts):
        status = parts[index].decode("utf-8", errors="surrogateescape")
        index += 1
        path_count = 2 if status.startswith(("R", "C")) else 1
        paths = tuple(
            parts[index + offset].decode("utf-8", errors="surrogateescape")
            for offset in range(path_count)
        )
        index += path_count
        changes.append((status, paths))

    untracked = git_command("ls-files", "--others", "--exclude-standard", "-z")
    if untracked.returncode != 0:
        raise RuntimeError("could not read untracked files")
    for raw_path in untracked.stdout.split(b"\0"):
        if raw_path:
            changes.append(("A", (raw_path.decode("utf-8", errors="surrogateescape"),)))
    return changes


def root_relative(value: str) -> str | None:
    path = Path(value)
    absolute = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        return absolute.relative_to(ROOT).as_posix()
    except ValueError:
        return None


def relevant_change(path: str) -> bool:
    return path in {"raw", "wiki"} or path.startswith(("raw/", "wiki/"))


def changed_inputs(requested: list[str], changes: list[tuple[str, tuple[str, ...]]]) -> set[str]:
    if requested:
        direct: set[str] = set()
        for value in requested:
            normalized = root_relative(value)
            if normalized is None:
                raise ValueError(f"changed path is outside the knowledge base: {value}")
            direct.add(normalized)
        for _status, paths in changes:
            if direct.intersection(paths):
                direct.update(paths)
    else:
        direct = {path for _status, paths in changes for path in paths}

    expanded = set(direct)
    for path in direct:
        absolute = ROOT / path
        if absolute.is_dir():
            expanded.update(
                candidate.relative_to(ROOT).as_posix()
                for candidate in absolute.rglob("*")
                if candidate.is_file()
            )
    return {path for path in expanded if relevant_change(path)}


def incremental_selection(requested: list[str]) -> tuple[set[str], set[Path], set[Path], list[Path]]:
    changes = git_changes()
    direct = changed_inputs(requested, changes)
    direct_targets = {(ROOT / path).resolve() for path in direct}
    concepts = set(concept_paths())
    direct_concepts = {target for target in direct_targets if target in concepts}
    dependents = {
        concept
        for concept in concepts - direct_concepts
        if any(target.resolve() in direct_targets for target in concept_targets(concept))
    }
    inventory = [
        target
        for target in direct_targets
        if target.is_file() and is_inside(target, RAW) and target.name != ".gitkeep"
    ]
    return direct, dependents, direct_concepts | dependents, inventory


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", action="store_true", help="check changed concepts and evidence references")
    mode.add_argument("--all", action="store_true", dest="check_all", help="check all concepts and raw inventory")
    parser.add_argument("--root", type=Path, help="knowledge-base root; defaults to the script's parent directory")
    parser.add_argument("paths", nargs="*", help="directly changed paths, used with --changed")
    parsed = parser.parse_args(arguments)
    if parsed.paths and not parsed.changed:
        parser.error("changed paths require --changed")
    return parsed


def main(arguments: list[str] | None = None) -> int:
    parsed = parse_arguments(arguments)
    configure_root(parsed.root or Path(__file__).resolve().parent.parent)
    EVIDENCE_ERRORS.clear()
    WARNINGS.clear()

    if not WIKI.is_dir() or not RAW.is_dir():
        print(f"Knowledge-base root must contain wiki/ and raw/: {ROOT}", file=sys.stderr)
        return 2

    changed_mode = parsed.changed
    notice = ""
    direct: set[str] = set()
    dependents: set[Path] = set()
    selected: set[Path]
    inventory: list[Path]
    if changed_mode and not has_git_history():
        notice = "NOTICE: Git history unavailable; running complete evidence check."
        changed_mode = False

    if changed_mode:
        try:
            direct, dependents, selected, inventory = incremental_selection(parsed.paths)
        except (RuntimeError, ValueError) as error:
            print(f"Incremental evidence check failed: {error}", file=sys.stderr)
            return 2
    else:
        selected = set(concept_paths())
        inventory = raw_originals()

    for path in sorted(selected):
        check_concept(path)
    check_inventory(sorted(inventory))

    if notice:
        print(notice)
    if changed_mode:
        print("Evidence check mode: changed")
        for path in sorted(direct):
            print(f"DIRECT: {path}")
        direct_paths = {(ROOT / path).resolve() for path in direct}
        for path in sorted(dependents):
            if path.resolve() not in direct_paths:
                print(f"DEPENDENT: {relative(path)}")
    else:
        print("Evidence check mode: all")

    count = len(selected)
    noun = "concept file" if count == 1 else "concept files"
    print(f"Checked {count} {noun}.")
    print(f"Evidence errors: {len(EVIDENCE_ERRORS)}")
    print(f"Warnings: {len(WARNINGS)}")
    for message in EVIDENCE_ERRORS:
        print(f"ERROR: {message}")
    for message in WARNINGS:
        print(f"WARNING: {message}")
    return 1 if EVIDENCE_ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
