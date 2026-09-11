#!/usr/bin/env python3
"""Migrate the operating kit to a newer stable Git release."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = "references/migration-manifest.json"
LOCAL_SETTINGS = "references/local-settings.md"
REPOSITORY = "https://github.com/martintoft1/llm-knowledge-base-starter.git"
PROTECTED_DIRECTORIES = (".git", ".migration", "raw", "wiki")
SUPPORTED_MERGE_STRATEGIES = {"target-structure"}
STABLE_TAG = re.compile(r"^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
Version = tuple[int, int, int]


class MigrationError(RuntimeError):
    """The migration cannot be completed safely."""


@dataclass(frozen=True)
class Action:
    kind: str
    path: str


@dataclass(frozen=True)
class MergeRule:
    path: str
    strategy: str


@dataclass(frozen=True)
class Transition:
    source: Version
    target: Version
    added_paths: tuple[str, ...]
    removed_paths: tuple[str, ...]


@dataclass(frozen=True)
class Manifest:
    release_version: Version
    managed_paths: tuple[str, ...]
    preserved_paths: tuple[str, ...]
    preserve_unknown_paths: bool
    merged_paths: tuple[MergeRule, ...]
    transitions: tuple[Transition, ...]


@dataclass(frozen=True)
class MergeArtifact:
    path: str
    source: Path
    target: Path


@dataclass(frozen=True)
class MigrationResult:
    version: str
    commit: str
    route: tuple[tuple[Version, Version], ...]
    actions: tuple[Action, ...]
    backup: Path
    action_record: Path
    merges: tuple[MergeArtifact, ...]


def version(value: object, label: str) -> Version:
    if not isinstance(value, str):
        raise MigrationError(f"{label} must be a stable semantic version")
    match = STABLE_TAG.fullmatch(f"v{value.strip().removeprefix('v')}")
    if not match:
        raise MigrationError(f"{label} must be a stable semantic version")
    return tuple(int(part) for part in match.groups())


def version_text(value: Version) -> str:
    return ".".join(str(part) for part in value)


def version_tag(value: Version) -> str:
    return f"v{version_text(value)}"


def path_key(path: str) -> str:
    return unicodedata.normalize("NFC", path).casefold()


def relative_path(value: object) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise MigrationError("path must be a POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise MigrationError(f"path must stay inside the knowledge base: {value!r}")
    return path.as_posix()


def validate_paths(values: object, label: str) -> tuple[str, ...]:
    if not isinstance(values, list):
        raise MigrationError(f"{label} must be a list")
    paths = tuple(relative_path(item) for item in values)
    if len(paths) != len({path_key(path) for path in paths}):
        raise MigrationError(f"{label} contains duplicate paths")
    return paths


def path_is_within(path: str, prefix: str) -> bool:
    key = path_key(path)
    prefix_key = path_key(prefix)
    return key == prefix_key or key.startswith(f"{prefix_key}/")


def local_path(root: Path, relative: str) -> Path:
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise MigrationError(f"unsafe path: {relative}")
    return path


def file_bytes(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise MigrationError(f"{label} must be a regular file: {path}")
    return path.read_bytes()


def existing_bytes(path: Path) -> bytes | None:
    if not path.exists() and not path.is_symlink():
        return None
    return file_bytes(path, "managed file")


def load_manifest(root: Path) -> Manifest:
    path = root / MANIFEST
    if not path.exists():
        raise MigrationError(f"migration manifest not found: {path}")
    try:
        data = json.loads(file_bytes(path, "migration manifest"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise MigrationError(f"cannot read migration manifest: {error}") from error
    if not isinstance(data, dict) or data.get("format_version") != 2:
        raise MigrationError("unsupported migration manifest")
    required_fields = {
        "format_version",
        "repository",
        "release_version",
        "managed_paths",
        "preserved_paths",
        "preserve_unknown_paths",
        "merged_paths",
        "transitions",
    }
    if set(data) != required_fields:
        raise MigrationError("migration manifest fields are invalid")
    if data.get("repository") != REPOSITORY:
        raise MigrationError("migration manifest identifies another repository")
    release_version = version(data["release_version"], "manifest release_version")
    managed_paths = validate_paths(data["managed_paths"], "manifest managed_paths")
    if MANIFEST not in managed_paths or "VERSION" not in managed_paths:
        raise MigrationError(f"manifest must manage VERSION and {MANIFEST}")
    preserved_paths = validate_paths(data["preserved_paths"], "manifest preserved_paths")
    preserved_keys = {path_key(item) for item in preserved_paths}
    missing_preserved = [
        item for item in PROTECTED_DIRECTORIES if path_key(item) not in preserved_keys
    ]
    if missing_preserved:
        raise MigrationError(
            "manifest is missing mandatory preserved paths: "
            + ", ".join(missing_preserved)
        )
    if data["preserve_unknown_paths"] is not True:
        raise MigrationError("manifest must preserve unknown paths")
    for item in managed_paths:
        if any(path_is_within(item, prefix) for prefix in preserved_paths):
            raise MigrationError(f"manifest contains protected path: {item}")
    raw_merges = data["merged_paths"]
    if not isinstance(raw_merges, list):
        raise MigrationError("manifest merged_paths must be a list")
    parsed_merges: list[MergeRule] = []
    for index, item in enumerate(raw_merges):
        if not isinstance(item, dict) or set(item) != {"path", "strategy"}:
            raise MigrationError(f"manifest merged_paths[{index}] is invalid")
        strategy = item["strategy"]
        if not isinstance(strategy, str) or strategy not in SUPPORTED_MERGE_STRATEGIES:
            raise MigrationError(f"unsupported merge strategy: {strategy}")
        parsed_merges.append(MergeRule(relative_path(item["path"]), strategy))
    merged_paths = tuple(parsed_merges)
    managed_keys = {path_key(item) for item in managed_paths}
    merge_keys = [path_key(rule.path) for rule in merged_paths]
    if len(merge_keys) != len(set(merge_keys)):
        raise MigrationError("manifest merged_paths contains duplicate paths")
    for rule in merged_paths:
        if any(path_is_within(rule.path, prefix) for prefix in preserved_paths):
            raise MigrationError(f"merged path is protected: {rule.path}")
        if path_key(rule.path) in managed_keys:
            raise MigrationError(
                f"path appears in managed and merged paths: {rule.path}"
            )
    if path_key(LOCAL_SETTINGS) not in set(merge_keys):
        raise MigrationError(f"manifest must merge {LOCAL_SETTINGS}")

    raw_transitions = data["transitions"]
    if not isinstance(raw_transitions, list):
        raise MigrationError("manifest transitions must be a list")
    parsed_transitions: list[Transition] = []
    merge_key_set = set(merge_keys)
    for index, item in enumerate(raw_transitions):
        if not isinstance(item, dict) or set(item) != {
            "from",
            "to",
            "added_paths",
            "removed_paths",
        }:
            raise MigrationError(f"manifest transitions[{index}] is invalid")
        source = version(item["from"], f"manifest transitions[{index}].from")
        target = version(item["to"], f"manifest transitions[{index}].to")
        if target <= source:
            raise MigrationError("transition target must be newer than its source")
        added = validate_paths(
            item["added_paths"], f"manifest transitions[{index}].added_paths"
        )
        removed = validate_paths(
            item["removed_paths"], f"manifest transitions[{index}].removed_paths"
        )
        if {path_key(value) for value in added} & {
            path_key(value) for value in removed
        }:
            raise MigrationError("transition added and removed paths overlap")
        for transition_path in (*added, *removed):
            if any(
                path_is_within(transition_path, prefix) for prefix in preserved_paths
            ):
                raise MigrationError(
                    f"transition contains protected path: {transition_path}"
                )
            if path_key(transition_path) in merge_key_set:
                raise MigrationError(
                    f"transition contains merged path: {transition_path}"
                )
        parsed_transitions.append(Transition(source, target, added, removed))
    transitions = tuple(parsed_transitions)

    return Manifest(
        release_version,
        managed_paths,
        preserved_paths,
        data["preserve_unknown_paths"],
        merged_paths,
        transitions,
    )


def read_version(root: Path) -> Version:
    try:
        value = file_bytes(root / "VERSION", "VERSION").decode()
    except (OSError, UnicodeDecodeError) as error:
        raise MigrationError(f"cannot read VERSION: {error}") from error
    return version(value, "VERSION")


def select_route(
    manifest: Manifest, current: Version, target: Version
) -> tuple[Transition, ...]:
    if target != manifest.release_version:
        raise MigrationError("target version differs from manifest release_version")
    if not manifest.transitions:
        raise MigrationError(
            f"transition ledger has no transition from {version_text(current)}"
        )
    by_source: dict[Version, Transition] = {}
    for transition in manifest.transitions:
        if transition.target > target:
            raise MigrationError("transition ledger contains a transition beyond target release")
        if transition.source in by_source:
            raise MigrationError(
                f"transition ledger has multiple transitions from "
                f"{version_text(transition.source)}"
            )
        by_source[transition.source] = transition

    ledger_targets = {transition.target for transition in manifest.transitions}
    ledger_starts = [source for source in by_source if source not in ledger_targets]
    if len(ledger_starts) != 1:
        raise MigrationError("transition ledger must form a single contiguous chain")
    ledger_seen: set[Version] = set()
    ledger_cursor = ledger_starts[0]
    while ledger_cursor in by_source:
        if ledger_cursor in ledger_seen:
            raise MigrationError("transition ledger contains a cycle")
        ledger_seen.add(ledger_cursor)
        ledger_cursor = by_source[ledger_cursor].target
    if len(ledger_seen) != len(manifest.transitions) or ledger_cursor != target:
        raise MigrationError("transition ledger must form a single contiguous chain")

    route: list[Transition] = []
    seen: set[Version] = set()
    cursor = current
    while cursor != target:
        if cursor in seen:
            raise MigrationError("transition ledger contains a cycle")
        seen.add(cursor)
        transition = by_source.get(cursor)
        if transition is None:
            raise MigrationError(
                f"transition ledger has no transition from {version_text(cursor)}"
            )
        if transition.target > target:
            raise MigrationError("transition ledger overshoots the target version")
        route.append(transition)
        cursor = transition.target
    return tuple(route)


def reconstruct_source_paths(
    manifest: Manifest, route: tuple[Transition, ...]
) -> tuple[str, ...]:
    owned = {path_key(path): path for path in manifest.managed_paths}
    for transition in reversed(route):
        for path in transition.added_paths:
            key = path_key(path)
            if key not in owned:
                raise MigrationError(
                    f"transition added path is absent from its target state: {path}"
                )
            del owned[key]
        for path in transition.removed_paths:
            key = path_key(path)
            if key in owned:
                raise MigrationError(
                    f"transition removed path remains in its target state: {path}"
                )
            owned[key] = path

    source_paths = tuple(sorted(owned.values()))
    replay = {path_key(path): path for path in source_paths}
    for transition in route:
        for path in transition.removed_paths:
            key = path_key(path)
            if key not in replay:
                raise MigrationError(
                    f"transition removes a path absent from its source state: {path}"
                )
            del replay[key]
        for path in transition.added_paths:
            key = path_key(path)
            if key in replay:
                raise MigrationError(
                    f"transition adds a path already in its source state: {path}"
                )
            replay[key] = path
    target = {path_key(path): path for path in manifest.managed_paths}
    if replay != target:
        raise MigrationError("transition ledger does not produce target managed paths")
    return source_paths


def load_source_paths(
    root: Path, current: Version, expected: tuple[str, ...]
) -> tuple[str, ...]:
    path = root / MANIFEST
    if not path.exists():
        if current == (0, 1, 0):
            return expected
        raise MigrationError(f"migration manifest not found: {path}")
    installed = load_manifest(root)
    if installed.release_version != current:
        raise MigrationError("installed manifest release_version differs from VERSION")
    actual = {path_key(item): item for item in installed.managed_paths}
    reconstructed = {path_key(item): item for item in expected}
    if actual != reconstructed:
        raise MigrationError("installed manifest differs from transition ledger")
    return installed.managed_paths


def git(arguments: list[str], cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments], cwd=cwd, capture_output=True, text=True, check=False
        )
    except FileNotFoundError as error:
        raise MigrationError("Git is required for migration") from error
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "Git command failed"
        raise MigrationError(detail)
    return result.stdout.strip()


def available_releases(repository: str) -> list[Version]:
    output = git(["ls-remote", "--tags", "--refs", repository, "v*"])
    releases = {
        tuple(int(part) for part in match.groups())
        for line in output.splitlines()
        if len(line.split("\t", 1)) == 2
        if (match := STABLE_TAG.fullmatch(line.split("\t", 1)[1].removeprefix("refs/tags/")))
    }
    if not releases:
        raise MigrationError("no stable releases were found")
    return sorted(releases)


def select_release(repository: str, requested: str, current: Version) -> Version:
    available = available_releases(repository)
    target = max(available) if requested == "latest" else version(requested, "target")
    if target not in available:
        raise MigrationError(f"release is unavailable: {version_tag(target)}")
    if target <= current:
        raise MigrationError(
            f"{version_tag(target)} is not newer than {version_tag(current)}"
        )
    return target


def find_actions(
    root: Path,
    release: Path,
    source_paths: tuple[str, ...],
    manifest: Manifest,
) -> tuple[Action, ...]:
    current = {path_key(path): path for path in source_paths}
    target = {path_key(path): path for path in manifest.managed_paths}
    for key in current.keys() & target.keys():
        if current[key] != target[key]:
            raise MigrationError(f"managed path spelling changed: {current[key]} -> {target[key]}")

    actions: list[Action] = []
    for key, relative in sorted(target.items(), key=lambda item: item[1]):
        source = local_path(release, relative)
        destination = local_path(root, relative)
        if key not in current and (destination.exists() or destination.is_symlink()):
            raise MigrationError(f"new managed file collides with unowned path: {relative}")
        old = existing_bytes(destination)
        if file_bytes(source, "release file") != old:
            actions.append(Action("add" if old is None else "replace", relative))

    for key in sorted(current.keys() - target.keys(), key=lambda item: current[item]):
        relative = current[key]
        if existing_bytes(local_path(root, relative)) is not None:
            actions.append(Action("remove", relative))
    for rule in sorted(manifest.merged_paths, key=lambda item: item.path):
        source = local_path(root, rule.path)
        target_template = local_path(release, rule.path)
        if source.exists() or source.is_symlink():
            existing_bytes(source)
        file_bytes(target_template, "merge target")
        actions.append(Action("merge", rule.path))
    return tuple(actions)


def replace_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def make_backup(root: Path, directory: Path, actions: tuple[Action, ...]) -> Path:
    backup = directory / "backup"
    backup.mkdir(parents=True)
    for action in actions:
        source = local_path(root, action.path)
        if source.exists() or source.is_symlink():
            replace_file(source, backup / action.path)
    return backup


def prepare_merges(
    release: Path,
    directory: Path,
    backup: Path,
    rules: tuple[MergeRule, ...],
) -> tuple[MergeArtifact, ...]:
    artifacts: list[MergeArtifact] = []
    for rule in rules:
        target = directory / "targets" / rule.path
        replace_file(local_path(release, rule.path), target)
        artifacts.append(MergeArtifact(rule.path, backup / rule.path, target))
    return tuple(artifacts)


def write_action_record(
    directory: Path,
    current: Version,
    target: Version,
    commit: str,
    route: tuple[Transition, ...],
    actions: tuple[Action, ...],
) -> Path:
    path = directory / "actions.json"
    record = {
        "source_version": version_text(current),
        "target_version": version_text(target),
        "release_commit": commit,
        "route": [
            {
                "from": version_text(transition.source),
                "to": version_text(transition.target),
            }
            for transition in route
        ],
        "actions": [
            {"kind": action.kind, "path": action.path} for action in actions
        ],
    }
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return path


def apply_actions(
    root: Path,
    release: Path,
    backup: Path,
    actions: tuple[Action, ...],
) -> None:
    deterministic = tuple(action for action in actions if action.kind != "merge")
    try:
        for action in deterministic:
            destination = root / action.path
            if action.kind == "remove":
                destination.unlink()
            else:
                replace_file(release / action.path, destination)
    except (Exception, KeyboardInterrupt) as error:
        failures: list[str] = []
        for action in reversed(deterministic):
            source = backup / action.path
            try:
                if source.exists():
                    replace_file(source, root / action.path)
                else:
                    (root / action.path).unlink(missing_ok=True)
            except Exception:
                failures.append(action.path)
        if failures:
            raise MigrationError(
                f"migration failed and rollback was incomplete for: {', '.join(failures)}"
            ) from error
        raise MigrationError(f"migration failed; files were restored from {backup}") from error


def migrate(
    root: Path, target: str = "latest", repository: str = REPOSITORY
) -> MigrationResult:
    root = root.resolve()
    current = read_version(root)
    target_version = select_release(repository, target, current)
    workspace = root / ".migration"
    if workspace.is_symlink() or (workspace.exists() and not workspace.is_dir()):
        raise MigrationError(f"migration workspace is unsafe: {workspace}")
    workspace.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=".download-", dir=workspace) as temporary:
        release = Path(temporary) / "release"
        git(
            [
                "clone", "--quiet", "--depth", "1", "--branch", version_tag(target_version),
                "--single-branch", repository, str(release),
            ]
        )
        if read_version(release) != target_version:
            raise MigrationError(f"{version_tag(target_version)} contains a different VERSION")
        manifest = load_manifest(release)
        if manifest.release_version != target_version:
            raise MigrationError(
                f"{version_tag(target_version)} manifest identifies another release"
            )
        route = select_route(manifest, current, target_version)
        expected_source_paths = reconstruct_source_paths(manifest, route)
        source_paths = load_source_paths(root, current, expected_source_paths)
        actions = find_actions(root, release, source_paths, manifest)
        commit = git(["rev-parse", "HEAD"], cwd=release)
        directory = workspace / f"{version_tag(target_version)}-{commit[:12]}"
        if directory.exists():
            raise MigrationError(f"migration backup already exists: {directory}")
        directory.mkdir()
        try:
            backup = make_backup(root, directory, actions)
            merges = prepare_merges(
                release,
                directory,
                backup,
                manifest.merged_paths,
            )
            action_record = write_action_record(
                directory,
                current,
                target_version,
                commit,
                route,
                actions,
            )
        except Exception as error:
            shutil.rmtree(directory, ignore_errors=True)
            raise MigrationError(f"could not prepare migration backup: {error}") from error
        apply_actions(root, release, backup, actions)

    print(f"Updated operating kit {version_text(current)} -> {version_text(target_version)}.")
    print(
        "Route: "
        + " -> ".join(
            [version_text(current), *(version_text(item.target) for item in route)]
        )
    )
    print(f"Release commit: {commit}")
    for action in actions:
        print(f"{action.kind.upper()}: {action.path}")
    print(f"Backup: {backup}")
    print(f"Action record: {action_record}")
    for merge in merges:
        print(f"Merge source: {merge.source}")
        print(f"Merge target: {merge.target}")
    print("UNCHANGED: raw/")
    print("UNCHANGED: wiki/")
    print("UNCHANGED: unknown paths")
    print("UNCHANGED: .git/")
    return MigrationResult(
        version_text(target_version),
        commit,
        tuple((item.source, item.target) for item in route),
        actions,
        backup,
        action_record,
        merges,
    )


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--target", default="latest", help="stable version or latest")
    options = parser.parse_args(arguments)
    try:
        migrate(options.root, options.target)
    except (MigrationError, OSError) as error:
        print(f"Migration error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
