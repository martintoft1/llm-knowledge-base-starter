# Starter Changelog

This file records notable changes to LLM Knowledge Base Starter. The project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.2.0 - 2026-09-11

v0.2.0 substantially redesigns the starter's operating model. Agent routing, workflows, schema, writing guidance, and validation now form a clearer end-to-end system for producing consistent, traceable, and reusable knowledge with less unnecessary work.

### Added

- Dedicated Research and Review operations, a shared Search procedure, and clearer workflows for external access and attested computations.
- A user-initiated migration system with a cumulative transition ledger, direct skipped-release upgrades, scoped backups, collision protection, action records, rollback, and a v0.1.0 bootstrap path.
- Deterministic schema and evidence checkers with complete and changed-file modes.
- A ready-to-use empty knowledge base with `wiki/index.md`, `wiki/log.md`, a tracked `raw/` directory, sensible defaults, and common prompts.

### Changed

- Reworked the agent entry point and operating instructions into focused, step-based workflows with explicit starting conditions, results, approval boundaries, review, and handoffs.
- Reorganized the schema around knowledge-base files, atomic and canonical concepts, concept-type selection, frontmatter requirements, optional body structures, tags, links, provenance, verification, and freshness.
- Clarified body-writing rules for evidence, interpretation, inference, uncertainty, disagreements, and historical analysis.
- Required every concept to have a one-sentence `description`, at least one registered tag, a truthful producer identifier, and an ISO 8601 generation time with seconds and timezone.
- Strengthened source attribution by requiring stable source IDs and exact resource links in footnotes for addressable evidence.
- Made `wiki/` the default query layer and limited raw-source access to ingestion, explicit raw queries, and scoped evidence review.
- Required every retained raw original to support or be the subject of at least one concept.
- Replaced automatic knowledge accumulation after ordinary questions with a retention proposal that requires user acceptance.
- Reduced local settings to writing style, tag definitions, and storage and sharing restrictions. Purpose, scope, terminology, and other useful context can now be stored as ordinary concepts when needed.
- Clarified the separation between defining, reviewing, running, and attesting reusable computations and between authorizing, configuring, and verifying external access.

### Removed

- The initialization questionnaire and starter-provenance workflow.
- Duplicate index and log templates.
- Persistent derived source representations; difficult formats now use temporary extraction.

### Migration

Existing v0.1.0 knowledge bases can use the v0.2.0 migration tool. It preserves Git history, raw evidence, wiki knowledge, unknown files, and local-setting values that fit the new settings structure. Values without a destination remain available in the backup but are not recreated.

Because v0.2.0 strengthens the concept schema, existing concepts may require a separate Maintenance pass to add descriptions, registered tags, precise producer identifiers, or compatible timestamps.

## 0.1.0 - 2026-08-20

### Added

- A reusable starter for file-based knowledge bases targeting OKF v0.2.
- An ordered, skippable bootstrap questionnaire covering sensitive data, external access, writing style, collaborators, history, retained sources, and agent adapters.
- Deferred connector tracking through external-resource concepts, indexes, logs, and optional linked plans.
- A wiki schema with a defined tag-registry format, operating rules, writing guidance, and reusable templates.
- A pinned copy of the upstream OKF v0.2 specification with checksums and provenance.
- Progressive-autonomy, sensitive-data, source-protection, history, and validation rules.
- Apache License 2.0 licensing with copyright and upstream attribution notices.
