# Wiki Operations

This file defines how agents add, use, review, and record knowledge. [`local-settings.md`](local-settings.md) defines the current local context, and [`schema.md`](schema.md) defines the local OKF profile.

## Required Local Settings

Read only the settings needed for the operation:

- [Identity And Scope](local-settings.md#identity-and-scope) before ingest, query, or maintenance work.
- [Safety And History](local-settings.md#safety-and-history) before every operation. Apply its sensitive-data rules to source material, wiki content, logs, commits, and responses.
- [Actor Identifiers](local-settings.md#actor-identifiers) before recording or validating provenance, generation, or verification.
- [Tag Registry](local-settings.md#tag-registry) before adding, removing, reviewing, or validating tags.

Do not duplicate those settings here.

### History Mode Behavior

The history mode in [Safety And History](local-settings.md#safety-and-history) changes how work is recorded and what safeguards are available. A history-mode change does not require reinitialization. When the user changes it, update `local-settings.md`, record the change in `wiki/log.md`, and follow the new mode from then on. When enabling Git, use the repository that already contains the wiki or initialize one as part of the approved change; never create a nested repository.

#### Git And Log

Git is strongly recommended because it adds diffs, attribution, and rollback. Before committing, inspect the worktree, preserve unrelated changes, stage only the current operation, and create one focused local commit when host rules allow it. Never push, rewrite history, or perform a destructive rollback without authority.

#### Log Only

The wiki remains usable in log-only mode, but rollback is unavailable. Make this limitation clear when the mode is selected or changed. Without Git, get approval before substantively replacing existing content and before every structural or destructive change. Continue to record all meaningful operations in `wiki/log.md`.

## Operating Principles

### Bundle Boundaries

Every member of the `wiki/` bundle must be UTF-8 Markdown with a `.md` filename. This is a local restriction beyond base OKF. Keep non-Markdown evidence and support files outside the bundle: retain evidence under `raw/`, or point to an external, non-secret resource.

### Authority

Agents may perform ordinary, low-risk work under `wiki/` without asking each time. This includes creating and updating concepts, sources, claim footnotes, links, metadata, indexes, and logs; fixing clear formatting or conformance errors; and making focused local commits when Git is enabled and host rules allow it.

Approval is required before an agent:

- adds a raw source on the user's behalf;
- deletes a concept;
- performs broad merges, splits, moves, renames, or reorganizations;
- changes the pinned OKF version, schema, operating rules, templates, or autonomy settings;
- connects a new external system or increases existing access;
- writes to an external system;
- stores or exposes sensitive material beyond the stated settings; or
- performs an ambiguous or unusually broad action.

A direct user request is approval only for its stated scope. For approval-bound work, name the affected files, the intended result, and what happens to the originals before writing.

### Raw Evidence

Keep retained original evidence under `raw/` and authored knowledge under `wiki/`.

Existing raw files are immutable to agents. Never modify, overwrite, rename, move, or delete one. A correction or derived artifact becomes a new source. Adding a new raw source on the user's behalf requires approval, even when the source was already identified. A human may manage raw material directly outside this workflow.

Do not pretend to have read an unavailable source or external system. Record the limitation instead.

## Special Files

### Indexes

`wiki/index.md` is mandatory locally. It carries the bundle's `okf_version` declaration and groups useful entries under headings. Each entry is a Markdown link and should include the linked concept's `description` when available.

Update an index after ingest, durable query filing, or maintenance changes what readers should discover. Create a subdirectory index only when it improves progressive disclosure. Subdirectory indexes have no frontmatter. Resolve every index link relative to the index file's location.

### Log

`wiki/log.md` is mandatory in every history mode. It has no frontmatter and begins with `# Directory Update Log`. Group concise operation bullets newest-first under date-only `YYYY-MM-DD` headings. Record meaningful ingests, filed query findings, maintenance, and concept changes. Link affected concepts when useful.

The log records what happened. It is not a diff and cannot restore prior content.

## Core Operations

### Ingest

When the user supplies or identifies a source:

1. Check its relevance, provenance, conflicts, uncertainty, and sensitivity. Ask for approval if retaining it requires a new raw file.
2. Create or update the concepts that the source materially informs. Preserve conflicting evidence instead of silently choosing one account.
3. Add concept-level provenance in `sources`. When a body attributes a specific claim, give that source a stable `sources[].id` and use the same key for its Markdown footnote. Do not create a separate citations section.
4. Update related concepts, summaries, and cross-links when the source changes, supports, or contradicts them.
5. Update the affected index files and `wiki/log.md`.
6. Validate the complete bundle against OKF v0.2 and the local profile.
7. If Git is enabled and host rules allow it, create one focused local commit.
8. Report the concepts changed, important uncertainty or conflict, and the log entry or commit.

Prefer one-source-at-a-time ingest when practical so the user can guide emphasis. Do not fill the wiki with source summaries when the knowledge belongs in existing concepts.

### Query And Accumulation

Read `wiki/index.md`, follow relevant concepts and sources, and consult raw evidence when needed. Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict in the answer.

All durable or potentially useful knowledge found while answering must be filed into the wiki. Update an existing concept when the knowledge belongs there. Create a new concept only when it is a distinct unit, then update related concepts if the finding changes, supports, or contradicts them. Update the relevant index and log, validate the bundle, and commit when Git is enabled and allowed.

Do not create generic Q&A pages or chat-transcript archives. Minor procedural, temporary, or disposable answers remain in chat.

### Maintenance

Maintenance reviews the whole affected area and checks for:

- contradictions, uncertainty, and unsupported claims;
- stale or deprecated knowledge;
- broken or missing links and orphan concepts;
- missing or malformed provenance;
- duplicate, overlapping, or poorly bounded concepts;
- important missing concepts;
- invalid OKF or local-profile metadata;
- stale Attested Computations and failed attestations;
- type drift;
- tags that should be added, removed, merged, narrowed, or retired; and
- disagreement between concept tags and the approved [Tag Registry](local-settings.md#tag-registry).

Agents may apply clear, low-risk corrections automatically and record them. Applying an already approved tag to a concept, or removing one that plainly does not apply, is ordinary maintenance. Changing the tag registry requires the proposal described in `schema.md`, with the affected concepts and retrieval benefit. Broad structural, destructive, sensitive, or ambiguous changes require approval.

Keep `wiki/` flat until navigation becomes genuinely difficult. Prefer titles, links, and a small maintained tag registry before folders.

## Specialized Operations

### Attested Computation

OKF records a computation contract; it does not execute it. Treat each `Attested Computation` as its own concept.

The contract requirements for draft and stable concepts live in [`schema.md`](schema.md). Apply them through the validation procedure below; do not redefine them here.

Do not claim executable validity without a usable computation and executor. Do not claim attestable validity without a usable attester. During an attested run, an agent may supply values only for declared parameters. It must not author or alter the sanctioned computation. The consumer binds the values, the executor returns the declared receipt, and the deterministic attester checks what ran and the displayed result.

A failed attestation blocks use or display of the value and must be surfaced. When `today >= stale_after`, warn or refuse according to the risk. `verified` records a check of the stored definition; attestation checks one execution. One never replaces the other, and per-run receipts are not stored in the bundle merely as verification history.

## Validation And Conformance

Before finalizing any wiki operation, validate the complete bundle in this order:

1. **Base OKF.** Apply section 11 of the pinned OKF v0.2 specification. Every non-reserved `.md` file must have parseable YAML frontmatter and a non-empty `type`. Every reserved `index.md` and `log.md` that appears must follow its OKF structure.
2. **Local profile.** Apply every requirement in [`schema.md`](schema.md), including the bundle file kind, required frontmatter, optional and conditional field families, local type profiles, actor identifiers, source-linked footnotes, Attested Computation contract, and tag governance. Compare concept tags with the approved [Tag Registry](local-settings.md#tag-registry).
3. **Required reserved files.** Require the root `wiki/index.md` and `wiki/log.md`, and validate them against the formats described above.
4. **Compatibility.** Preserve unknown fields and types. Report broken links without failing base OKF conformance. Accept missing optional OKF families and missing non-root indexes.
5. **Result.** Report base OKF failures, local-profile failures, and warnings separately. A bundle may meet base OKF while failing this repository's stricter local profile.

If a required base or local check fails, correct it when the fix is clear and within scope. Otherwise stop: do not mark the operation complete or create its automatic commit. Report the failed check, affected files, retained changes, and the approval or information needed. Never invent provenance, verification, access, or attestation to make validation pass.
