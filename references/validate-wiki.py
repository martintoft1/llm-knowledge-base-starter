#!/usr/bin/env python3
"""Validate the wiki bundle against OKF v0.2 and the local wiki schema."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, datetime, timezone
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
LOCAL_SETTINGS = ROOT / "references" / "local-settings.md"
BASE_FAILURES: list[str] = []
SCHEMA_FAILURES: list[str] = []
WARNINGS: list[str] = []

STATUSES = {"draft", "stable", "deprecated"}
RESOURCE_REQUIRED = {"Source Record"}
RESOURCE_REQUIRED_WHEN_STABLE = {"Dataset", "Database"}
ACTOR_PATTERN = re.compile(r"^(?:human:.+|process:.+|[^\s/:]+/[^\s/]+)$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
FOOTNOTE_DEFINITION = re.compile(r"^\[\^([^\]]+)\]:", re.MULTILINE)
FOOTNOTE_DEFINITION_TEXT = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$", re.MULTILINE)
FOOTNOTE_REFERENCE = re.compile(r"\[\^([^\]]+)\]")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_REFERENCE_DEFINITION = re.compile(
    r"^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))",
    re.MULTILINE,
)
TAG_ENTRY = re.compile(r"^- `([^`]+)`: (.+)$", re.MULTILINE)


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    if not text.startswith("---\n"):
        return None, text, "missing frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text, "unterminated frontmatter"
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        return None, body, f"invalid YAML: {error}"
    if not isinstance(data, dict):
        return None, body, "frontmatter must be a mapping"
    return data, body, None


def valid_actor(value: object) -> bool:
    return nonempty_string(value) and bool(ACTOR_PATTERN.fullmatch(value))


def valid_date(value: object) -> bool:
    if isinstance(value, datetime):
        return False
    if isinstance(value, date):
        return True
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def valid_datetime(value: object) -> bool:
    if isinstance(value, datetime):
        return value.tzinfo is not None and value.utcoffset() is not None
    if not isinstance(value, str) or not DATETIME_PATTERN.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.utcoffset() is not None
    except ValueError:
        return False


def parsed_date(value: object) -> date | None:
    if not valid_date(value):
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def parsed_datetime(value: object) -> datetime | None:
    if not valid_datetime(value):
        return None
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError:
        SCHEMA_FAILURES.append(f"{relative(path)}: file is not valid UTF-8")
        return None


def approved_tags() -> set[str]:
    text = read_text(LOCAL_SETTINGS)
    if text is None:
        return set()
    registry = tag_registry(text)
    if registry is None:
        SCHEMA_FAILURES.append("references/local-settings.md: missing Tag Registry section")
        return set()
    return set(registry)


def tag_registry(text: str) -> dict[str, str] | None:
    match = re.search(r"^## Tag Registry\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    if not match:
        return None
    return dict(TAG_ENTRY.findall(match.group(1)))


def local_target(source_file: Path, value: str) -> Path | None:
    value = unquote(value.strip().strip("<>")).split("#", 1)[0].split("?", 1)[0]
    if not value or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return None
    if value.startswith("/"):
        return WIKI / value.lstrip("/")
    return (source_file.parent / value).resolve()


def is_inside(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def markdown_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        value = match.group(1).strip()
        if value.startswith("<") and ">" in value:
            value = value[1 : value.index(">")]
        else:
            value = value.split(maxsplit=1)[0] if value else ""
        if value:
            targets.append(value)
    for match in MARKDOWN_REFERENCE_DEFINITION.finditer(text):
        label, angled, plain = match.groups()
        if not label.startswith("^"):
            targets.append(angled or plain)
    return targets


def addressable_resource(value: object) -> bool:
    if not nonempty_string(value):
        return False
    value = value.strip().strip("<>")
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value)) or any(
        mark in value for mark in ("/", "\\", ".")
    )


def footnote_links_to_resource(definition: str, resource: str) -> bool:
    expected = resource.strip().strip("<>")
    return expected in {target.strip().strip("<>") for target in markdown_targets(definition)}


def check_path(source_file: Path, value: object, field: str, allow_scope: bool = False) -> None:
    if not nonempty_string(value):
        SCHEMA_FAILURES.append(f"{relative(source_file)}: {field} must be a non-empty path or URL")
        return
    target = local_target(source_file, value)
    if target is None:
        return
    if allow_scope and not any(mark in value for mark in ("/", "\\", ".")):
        return
    if not target.exists():
        WARNINGS.append(f"{relative(source_file)}: unresolved {field} {value}")


def check_links(path: Path, body: str) -> None:
    for value in markdown_targets(body):
        target = local_target(path, value)
        if target is not None and not target.exists():
            SCHEMA_FAILURES.append(f"{relative(path)}: broken link {value}")


def check_usage_window(path: Path, value: object, field: str) -> bool:
    if not isinstance(value, dict):
        SCHEMA_FAILURES.append(f"{relative(path)}: {field} must be a mapping")
        return False
    valid = True
    for key in ("from", "to"):
        if not valid_date(value.get(key)):
            SCHEMA_FAILURES.append(f"{relative(path)}: {field}.{key} must be YYYY-MM-DD")
            valid = False
    return valid


def check_verified(path: Path, value: object) -> list[dict]:
    events = [value] if isinstance(value, dict) else value
    if not isinstance(events, list) or not events:
        SCHEMA_FAILURES.append(f"{relative(path)}: verified must be a non-empty mapping or list")
        return []
    valid_events = []
    for index, event in enumerate(events):
        label = f"verified[{index}]"
        if not isinstance(event, dict):
            SCHEMA_FAILURES.append(f"{relative(path)}: {label} must be a mapping")
            continue
        if not valid_actor(event.get("by")):
            SCHEMA_FAILURES.append(f"{relative(path)}: {label}.by is not a valid actor")
        if not valid_datetime(event.get("at")):
            SCHEMA_FAILURES.append(
                f"{relative(path)}: {label}.at must be an ISO 8601 datetime with seconds and timezone"
            )
        valid_events.append(event)
    return valid_events


def check_sources(path: Path, data: dict, body: str) -> list[dict]:
    if "sources" not in data:
        return []
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        SCHEMA_FAILURES.append(f"{relative(path)}: sources must be a non-empty list")
        return []

    definition_text = dict(FOOTNOTE_DEFINITION_TEXT.findall(body))
    definitions = set(definition_text)
    body_without_definitions = FOOTNOTE_DEFINITION.sub("", body)
    references = set(FOOTNOTE_REFERENCE.findall(body_without_definitions))
    ids: set[str] = set()
    shared_window = data.get("usage_window")

    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            SCHEMA_FAILURES.append(f"{relative(path)}: {label} must be a mapping")
            continue
        check_path(path, source.get("resource"), f"{label}.resource", allow_scope=True)
        if "representation" in source:
            SCHEMA_FAILURES.append(f"{relative(path)}: {label}.representation is not supported")
        source_id = source.get("id")
        if source_id is None:
            SCHEMA_FAILURES.append(f"{relative(path)}: {label}.id is required")
        elif not nonempty_string(source_id):
            SCHEMA_FAILURES.append(f"{relative(path)}: {label}.id must be non-empty")
        elif source_id in ids:
            SCHEMA_FAILURES.append(f"{relative(path)}: duplicate source id {source_id}")
        else:
            ids.add(source_id)
            if source_id not in references:
                SCHEMA_FAILURES.append(f"{relative(path)}: source {source_id} is not cited in the body")
            if source_id not in definitions:
                SCHEMA_FAILURES.append(f"{relative(path)}: source {source_id} lacks a footnote definition")
            elif addressable_resource(source.get("resource")) and not footnote_links_to_resource(
                definition_text[source_id], source["resource"]
            ):
                SCHEMA_FAILURES.append(
                    f"{relative(path)}: source {source_id} footnote must link to {source['resource']}"
                )
        if "author" in source and not valid_actor(source["author"]):
            SCHEMA_FAILURES.append(f"{relative(path)}: {label}.author is not a valid actor")
        if "last_modified" in source and not valid_date(source["last_modified"]):
            SCHEMA_FAILURES.append(f"{relative(path)}: {label}.last_modified must be YYYY-MM-DD")
        if "usage_count" in source:
            count = source["usage_count"]
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                SCHEMA_FAILURES.append(f"{relative(path)}: {label}.usage_count must be a non-negative integer")
            if "usage_window" in source:
                check_usage_window(path, source["usage_window"], f"{label}.usage_window")
            elif shared_window is None:
                SCHEMA_FAILURES.append(f"{relative(path)}: {label}.usage_count requires a usage window")

    return [source for source in sources if isinstance(source, dict)]


def computation_section(body: str) -> str:
    match = re.search(r"^# Computation\s*$([\s\S]*?)(?=^# |\Z)", body, re.MULTILINE)
    return match.group(1) if match else ""


def check_attested_computation(path: Path, data: dict, body: str, sources: list[dict], verified: list[dict]) -> None:
    if not nonempty_string(data.get("runtime")):
        SCHEMA_FAILURES.append(f"{relative(path)}: Attested Computation requires runtime")

    parameters = data.get("parameters")
    if parameters is not None:
        if not isinstance(parameters, list) or not parameters:
            SCHEMA_FAILURES.append(f"{relative(path)}: parameters must be a non-empty list when present")
        else:
            for index, parameter in enumerate(parameters):
                if not isinstance(parameter, dict):
                    SCHEMA_FAILURES.append(f"{relative(path)}: parameters[{index}] must be a mapping")
                    continue
                if not nonempty_string(parameter.get("name")) or not nonempty_string(parameter.get("type")):
                    SCHEMA_FAILURES.append(f"{relative(path)}: parameters[{index}] requires name and type")
                if not isinstance(parameter.get("required"), bool):
                    SCHEMA_FAILURES.append(f"{relative(path)}: parameters[{index}].required must be boolean")

    section = computation_section(body)
    fences = re.findall(r"^```[^\n]*\n[\s\S]*?^```\s*$", section, re.MULTILINE)
    inline = len(fences) == 1
    if len(fences) > 1:
        SCHEMA_FAILURES.append(f"{relative(path)}: # Computation contains more than one fenced block")
    file_form = "computation" in data
    if file_form:
        check_path(path, data.get("computation"), "computation")
    if inline and file_form:
        SCHEMA_FAILURES.append(f"{relative(path)}: computation must be inline or file-based, not both")

    executor = data.get("executor")
    if executor is not None:
        if not isinstance(executor, dict):
            SCHEMA_FAILURES.append(f"{relative(path)}: executor must be a mapping")
        else:
            check_path(path, executor.get("resource"), "executor.resource")
            receipt = executor.get("receipt")
            if not isinstance(receipt, list) or not receipt or not all(nonempty_string(item) for item in receipt):
                SCHEMA_FAILURES.append(f"{relative(path)}: executor.receipt must be a non-empty list")

    attester = data.get("attester")
    if attester is not None:
        if not isinstance(attester, dict):
            SCHEMA_FAILURES.append(f"{relative(path)}: attester must be a mapping")
        else:
            check_path(path, attester.get("resource"), "attester.resource")

    if data.get("status") == "stable":
        if not isinstance(parameters, list) or not parameters:
            SCHEMA_FAILURES.append(f"{relative(path)}: stable Attested Computation requires parameters")
        if not (inline ^ file_form):
            SCHEMA_FAILURES.append(f"{relative(path)}: stable Attested Computation requires exactly one computation form")
        if not isinstance(executor, dict):
            SCHEMA_FAILURES.append(f"{relative(path)}: stable Attested Computation requires executor")
        if not isinstance(attester, dict):
            SCHEMA_FAILURES.append(f"{relative(path)}: stable Attested Computation requires attester")
        if not sources or not any(nonempty_string(source.get("id")) for source in sources):
            SCHEMA_FAILURES.append(f"{relative(path)}: stable Attested Computation requires a source with an id")
        generated_by = data.get("generated", {}).get("by") if isinstance(data.get("generated"), dict) else None
        if not any(event.get("by") != generated_by for event in verified):
            SCHEMA_FAILURES.append(f"{relative(path)}: stable Attested Computation requires independent verification")


def check_concept(path: Path, text: str, tags: set[str]) -> None:
    data, body, error = parse_frontmatter(text)
    if error:
        BASE_FAILURES.append(f"{relative(path)}: {error}")
        return
    assert data is not None

    if not nonempty_string(data.get("type")):
        BASE_FAILURES.append(f"{relative(path)}: type must be non-empty")

    for field in ("type", "title", "description", "status", "tags", "generated"):
        if field not in data:
            SCHEMA_FAILURES.append(f"{relative(path)}: missing required field {field}")
    if "title" in data and not nonempty_string(data["title"]):
        SCHEMA_FAILURES.append(f"{relative(path)}: title must be non-empty")
    if data.get("status") not in STATUSES:
        SCHEMA_FAILURES.append(f"{relative(path)}: status must be draft, stable, or deprecated")
    if "description" in data and not nonempty_string(data["description"]):
        SCHEMA_FAILURES.append(f"{relative(path)}: description must be non-empty")

    concept_tags = data.get("tags")
    if not isinstance(concept_tags, list):
        SCHEMA_FAILURES.append(f"{relative(path)}: tags must be a YAML list")
    elif not concept_tags:
        SCHEMA_FAILURES.append(f"{relative(path)}: tags must contain at least one approved tag")
    else:
        for tag in concept_tags:
            if not nonempty_string(tag):
                SCHEMA_FAILURES.append(f"{relative(path)}: every tag must be a non-empty string")
            elif tag not in tags:
                SCHEMA_FAILURES.append(f"{relative(path)}: unapproved tag {tag}")

    generated = data.get("generated")
    if not isinstance(generated, dict):
        SCHEMA_FAILURES.append(f"{relative(path)}: generated must be a mapping")
    else:
        if not valid_actor(generated.get("by")):
            SCHEMA_FAILURES.append(f"{relative(path)}: generated.by is not a valid actor")
        if not valid_datetime(generated.get("at")):
            SCHEMA_FAILURES.append(
                f"{relative(path)}: generated.at must be an ISO 8601 datetime with seconds and timezone"
            )

    if "resource" in data:
        check_path(path, data["resource"], "resource")
    if "stale_after" in data:
        stale_after = parsed_date(data["stale_after"])
        if stale_after is None:
            SCHEMA_FAILURES.append(f"{relative(path)}: stale_after must be YYYY-MM-DD")
        elif date.today() >= stale_after:
            WARNINGS.append(f"{relative(path)}: stale since {stale_after.isoformat()}")
    if "usage_window" in data:
        check_usage_window(path, data["usage_window"], "usage_window")

    sources = check_sources(path, data, body)
    verified = check_verified(path, data["verified"]) if "verified" in data else []

    generated_at = parsed_datetime(generated.get("at")) if isinstance(generated, dict) else None
    verification_times = [
        checked_at
        for event in verified
        if (checked_at := parsed_datetime(event.get("at"))) is not None
    ]
    if generated_at is not None and verification_times and max(verification_times) < generated_at:
        WARNINGS.append(f"{relative(path)}: verification predates latest meaningful content change")

    concept_type = data.get("type")
    if concept_type in RESOURCE_REQUIRED and not nonempty_string(data.get("resource")):
        SCHEMA_FAILURES.append(f"{relative(path)}: {concept_type} requires resource")
    if concept_type in RESOURCE_REQUIRED_WHEN_STABLE and data.get("status") == "stable" and not nonempty_string(data.get("resource")):
        SCHEMA_FAILURES.append(f"{relative(path)}: stable {concept_type} requires resource")
    if concept_type == "Attested Computation":
        check_attested_computation(path, data, body, sources, verified)

    check_links(path, body)


def check_index(path: Path, text: str) -> None:
    root_index = path == WIKI / "index.md"
    data = None
    body = text
    if text.startswith("---\n"):
        data, body, error = parse_frontmatter(text)
        if error:
            BASE_FAILURES.append(f"{relative(path)}: {error}")
            return
        if not root_index:
            BASE_FAILURES.append(f"{relative(path)}: only the root index may have frontmatter")
    elif root_index:
        SCHEMA_FAILURES.append("wiki/index.md: root index requires okf_version frontmatter")

    if root_index and (not isinstance(data, dict) or data.get("okf_version") != "0.2"):
        SCHEMA_FAILURES.append('wiki/index.md: okf_version must be "0.2"')
    if not re.search(r"^#{1,6}\s+\S", body, re.MULTILINE):
        BASE_FAILURES.append(f"{relative(path)}: index requires at least one section heading")
    if root_index:
        concepts = {
            candidate.resolve()
            for candidate in WIKI.rglob("*.md")
            if candidate.name not in {"index.md", "log.md"}
        }
        counts = dict.fromkeys(concepts, 0)
        for value in markdown_targets(body):
            target = local_target(path, value)
            if target is not None and target.resolve() in counts:
                counts[target.resolve()] += 1
        for concept, count in sorted(counts.items(), key=lambda item: relative(item[0])):
            if count == 0:
                SCHEMA_FAILURES.append(f"{relative(path)}: missing concept entry {relative(concept)}")
            elif count > 1:
                SCHEMA_FAILURES.append(f"{relative(path)}: duplicate concept entry {relative(concept)}")
    check_links(path, body)


def check_log(path: Path, text: str) -> None:
    if text.startswith("---\n"):
        BASE_FAILURES.append(f"{relative(path)}: log files may not have frontmatter")
    if not text.startswith("# Directory Update Log\n"):
        BASE_FAILURES.append(f"{relative(path)}: invalid log heading")
    headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
    dates = []
    for heading in headings:
        if not DATE_PATTERN.fullmatch(heading):
            BASE_FAILURES.append(f"{relative(path)}: invalid date heading {heading}")
        else:
            dates.append(heading)
    if dates != sorted(dates, reverse=True):
        SCHEMA_FAILURES.append(f"{relative(path)}: date groups must be newest first")
    check_links(path, text)


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", action="store_true", help="validate changed wiki files and their dependents")
    mode.add_argument("--all", action="store_true", dest="validate_all", help="validate the complete wiki bundle")
    parser.add_argument("--root", type=Path, help="knowledge-base root; defaults to the script's parent directory")
    parser.add_argument("paths", nargs="*", help="directly changed paths, used with --changed")
    parsed = parser.parse_args(arguments)

    if parsed.paths and not parsed.changed:
        legacy_root = Path(parsed.paths[0]) if len(parsed.paths) == 1 and parsed.root is None else None
        if legacy_root is not None and (legacy_root / "wiki").is_dir():
            parsed.root = legacy_root
            parsed.paths = []
        else:
            parser.error("changed paths require --changed")
    return parsed


def configure_root(root: Path) -> None:
    global ROOT, WIKI, LOCAL_SETTINGS
    ROOT = root.resolve()
    WIKI = ROOT / "wiki"
    LOCAL_SETTINGS = ROOT / "references" / "local-settings.md"


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


def git_file_at_head(relative_path: str) -> str:
    result = git_command("show", f"HEAD:{relative_path}")
    if result.returncode != 0:
        return ""
    return result.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n")


def root_relative(value: str) -> str | None:
    path = Path(value)
    absolute = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        return absolute.relative_to(ROOT).as_posix()
    except ValueError:
        return None


def relevant_change(path: str) -> bool:
    return (
        path == "references/local-settings.md"
        or path in {"raw", "wiki"}
        or path.startswith(("raw/", "wiki/"))
    )


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
            prefix = path.rstrip("/") + "/"
            expanded.update(
                changed_path
                for _status, paths in changes
                for changed_path in paths
                if changed_path.startswith(prefix)
            )
    return {path for path in expanded if relevant_change(path)}


def selection_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return None


def frontmatter_paths(data: dict) -> list[str]:
    values: list[str] = []
    for field in ("resource", "computation"):
        value = data.get(field)
        if nonempty_string(value):
            values.append(value)
    sources = data.get("sources")
    if isinstance(sources, list):
        for source in sources:
            if isinstance(source, dict):
                if nonempty_string(source.get("resource")):
                    values.append(source["resource"])
    for field in ("executor", "attester"):
        value = data.get(field)
        if isinstance(value, dict) and nonempty_string(value.get("resource")):
            values.append(value["resource"])
    return values


def referenced_targets(path: Path, text: str) -> set[Path]:
    data, body, error = parse_frontmatter(text)
    values = markdown_targets(body)
    if error is None and data is not None:
        values.extend(frontmatter_paths(data))
    return {
        target.resolve()
        for value in values
        if (target := local_target(path, value)) is not None
    }


def refers_to_changed_target(path: Path, text: str, changed_targets: set[Path]) -> bool:
    if not changed_targets:
        return False
    for target in referenced_targets(path, text):
        if target in changed_targets or (target / "index.md").resolve() in changed_targets:
            return True
    return False


def affected_tags(direct: set[str]) -> set[str]:
    if "references/local-settings.md" not in direct:
        return set()
    old_registry = tag_registry(git_file_at_head("references/local-settings.md")) or {}
    current_text = selection_text(LOCAL_SETTINGS) or ""
    current_registry = tag_registry(current_text) or {}
    return {
        tag
        for tag in old_registry.keys() | current_registry.keys()
        if old_registry.get(tag) != current_registry.get(tag)
    }


def uses_affected_tag(text: str, tags: set[str]) -> bool:
    if not tags:
        return False
    data, _body, error = parse_frontmatter(text)
    if error is not None or data is None:
        return True
    concept_tags = data.get("tags")
    return isinstance(concept_tags, list) and any(tag in tags for tag in concept_tags)


def incremental_selection(
    requested: list[str],
    all_files: list[Path],
) -> tuple[set[str], set[Path], set[Path]]:
    changes = git_changes()
    direct = changed_inputs(requested, changes)
    current_markdown = {path for path in all_files if path.suffix == ".md"}
    direct_targets = {
        (ROOT / path).resolve()
        for path in direct
    }
    tags = affected_tags(direct)
    dependents: set[Path] = set()

    for path in current_markdown:
        if path.resolve() in direct_targets:
            continue
        text = selection_text(path)
        if text is None:
            continue
        if refers_to_changed_target(path, text, direct_targets) or uses_affected_tag(text, tags):
            dependents.add(path)

    direct_current = {
        path
        for path in direct_targets
        if is_inside(path, WIKI) and path.is_file() and path.suffix == ".md"
    }
    reserved = {path for path in (WIKI / "index.md", WIKI / "log.md") if path.is_file()}
    selected = direct_current | dependents | reserved
    return direct, dependents, selected


def main(arguments: list[str] | None = None) -> int:
    parsed = parse_arguments(arguments)
    configure_root(parsed.root or Path(__file__).resolve().parent.parent)
    BASE_FAILURES.clear()
    SCHEMA_FAILURES.clear()
    WARNINGS.clear()

    if not WIKI.is_dir():
        print(f"Wiki directory not found: {WIKI}", file=sys.stderr)
        return 2
    if not LOCAL_SETTINGS.is_file():
        print(f"Local settings not found: {LOCAL_SETTINGS}", file=sys.stderr)
        return 2

    files = sorted(path for path in WIKI.rglob("*") if path.is_file())
    changed_mode = parsed.changed
    notice = ""
    direct: set[str] = set()
    dependents: set[Path] = set()
    selected: set[Path]
    if changed_mode and not has_git_history():
        notice = "NOTICE: Git history unavailable; running full validation."
        changed_mode = False

    if changed_mode:
        try:
            direct, dependents, selected = incremental_selection(parsed.paths, files)
        except (RuntimeError, ValueError) as error:
            print(f"Incremental validation failed: {error}", file=sys.stderr)
            return 2
    else:
        selected = {path for path in files if path.suffix == ".md"}

    tags = approved_tags()
    for path in files:
        if path.suffix != ".md":
            SCHEMA_FAILURES.append(f"{relative(path)}: every bundle member must be Markdown")
    for path in sorted(selected):
        text = read_text(path)
        if text is None:
            continue
        if path.name == "index.md":
            check_index(path, text)
        elif path.name == "log.md":
            check_log(path, text)
        else:
            check_concept(path, text, tags)

    for required in (WIKI / "index.md", WIKI / "log.md"):
        if not required.is_file():
            SCHEMA_FAILURES.append(f"missing required file {relative(required)}")

    if notice:
        print(notice)
    if changed_mode:
        print("Validation mode: changed")
        for path in sorted(direct):
            print(f"DIRECT: {path}")
        direct_current = {(ROOT / path).resolve() for path in direct if path.startswith("wiki/")}
        for path in sorted(dependents):
            if path.resolve() not in direct_current:
                print(f"DEPENDENT: {relative(path)}")
    else:
        print("Validation mode: all")

    markdown_count = len(selected)
    print(f"Validated {markdown_count} Markdown files.")
    print(f"Base OKF failures: {len(BASE_FAILURES)}")
    print(f"Wiki-schema failures: {len(SCHEMA_FAILURES)}")
    print(f"Warnings: {len(WARNINGS)}")
    for message in BASE_FAILURES:
        print(f"BASE: {message}")
    for message in SCHEMA_FAILURES:
        print(f"SCHEMA: {message}")
    for message in WARNINGS:
        print(f"WARNING: {message}")
    return 1 if BASE_FAILURES or SCHEMA_FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
