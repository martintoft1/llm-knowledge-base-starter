# Starter Changelog

This file records notable changes to LLM Knowledge Base Starter. The project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- A ready-to-use empty OKF bundle with `wiki/index.md` and `wiki/log.md`.
- A tracked `raw/.gitkeep` placeholder so the raw-source directory exists from the start.
- Common prompts for ingesting, asking, summarizing, reviewing, correcting, maintaining, and connecting sources.
- Atomic-concept and canonical-linking rules, with separate maintenance checks for overloaded, duplicate, weakly linked, and orphaned concepts.
- Test run windows for checking concept-generation timestamps and evidence-linked suite reports with separate mechanical and orchestrator judgments.

### Changed

- Reduced local settings to writing style, tags, and storage and sharing restrictions.
- Made local settings the sole source of storage and external-sharing policy values; operating rules now only enforce them.
- Made the repository usable without setup. Purpose, scope, terminology, and other context can be inferred or stored as ordinary concepts when useful.
- Replaced automatic accumulation after ordinary questions with a brief knowledge proposal that requires acceptance before storage.
- Made explicit Ingest requests authorize retaining their supplied sources and made retention decisions after ordinary questions visible.
- Clarified pending external-resource records, governed reusable calculations, and their natural-language routing and templates.
- Made `description` required for every concept and added it to the shared page template and validator.
- Required precise producer identifiers and current ISO 8601 generation times, and aligned test scenarios with those rules.
- Made the wiki the default query layer and limited raw-content access to explicit raw queries, ingestion, and scoped evidence review.
- Required every retained raw original to support or be the subject of at least one wiki concept.
- Limited evidence review to affected claims and cited sources after source-backed changes, or to existing pages when explicitly requested.

### Removed

- The initialization bootstrap and its starter-provenance workflow.
- Duplicate index and log templates.
- Persistent derived source representations; difficult formats now use disposable extraction.

## 0.1.0 - 2026-08-20

### Added

- A reusable starter for file-based knowledge bases targeting OKF v0.2.
- An ordered, skippable bootstrap questionnaire covering sensitive data, external access, writing style, collaborators, history, retained sources, and agent adapters.
- Deferred connector tracking through external-resource concepts, indexes, logs, and optional linked plans.
- A wiki schema with a defined tag-registry format, operating rules, writing guidance, and reusable templates.
- A pinned copy of the upstream OKF v0.2 specification with checksums and provenance.
- Progressive-autonomy, sensitive-data, source-protection, history, and validation rules.
- Apache License 2.0 licensing with copyright and upstream attribution notices.
