# Starter Changelog

This file records notable changes to LLM Knowledge Base Starter. The project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- A ready-to-use empty OKF bundle with `wiki/index.md` and `wiki/log.md`.
- A tracked `raw/.gitkeep` placeholder so the raw-source directory exists from the start.
- Common prompts for ingesting, asking, summarizing, reviewing, correcting, maintaining, and connecting sources.
- Atomic-concept and canonical-linking rules, with separate maintenance checks for overloaded, duplicate, weakly linked, and orphaned concepts.

### Changed

- Reduced local settings to writing style, tags, and storage and sharing restrictions.
- Made local settings the sole source of storage and external-sharing policy values; operating rules now only enforce them.
- Made the repository usable without setup. Purpose, scope, terminology, and other context can be inferred or stored as ordinary concepts when useful.
- Replaced automatic accumulation after ordinary questions with a brief knowledge proposal that requires acceptance before storage.

### Removed

- The initialization bootstrap and its starter-provenance workflow.
- Duplicate index and log templates.

## 0.1.0 - 2026-08-20

### Added

- A reusable starter for file-based knowledge bases targeting OKF v0.2.
- An ordered, skippable bootstrap questionnaire covering sensitive data, external access, writing style, collaborators, history, retained sources, and agent adapters.
- Deferred connector tracking through external-resource concepts, indexes, logs, and optional linked plans.
- A wiki schema with a defined tag-registry format, operating rules, writing guidance, and reusable templates.
- A pinned copy of the upstream OKF v0.2 specification with checksums and provenance.
- Progressive-autonomy, sensitive-data, source-protection, history, and validation rules.
- Apache License 2.0 licensing with copyright and upstream attribution notices.
