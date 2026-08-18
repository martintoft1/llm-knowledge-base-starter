# Wiki Operations

This file defines how agents add, use, review, and record knowledge. The pinned OKF specification defines the format; [`schema.md`](schema.md) defines the stricter local profile.

## Local Settings

- **History mode:** <Git and log, or log only>
- **Sensitive data:** <what may be read, quoted, linked, or retained>

Apply the sensitive-data rules to source material, wiki content, logs, commits, and responses.

## Authority

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

## Raw Evidence

Keep retained original evidence under `raw/` and authored knowledge under `wiki/`.

Existing raw files are immutable to agents. Never modify, overwrite, rename, move, or delete one. A correction or derived artifact becomes a new source. Adding a new raw source on the user's behalf requires approval, even when the source was already identified. A human may manage raw material directly outside this workflow.

Do not pretend to have read an unavailable source or external system. Record the limitation instead.

## Ingest

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

## Query And Accumulation

Read `wiki/index.md`, follow relevant concepts and sources, and consult raw evidence when needed. Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict in the answer.

All durable or potentially useful knowledge found while answering must be filed into the wiki. Update an existing concept when the knowledge belongs there. Create a new concept only when it is a distinct unit, then update related concepts if the finding changes, supports, or contradicts them. Update the relevant index and log, validate the bundle, and commit when Git is enabled and allowed.

Do not create generic Q&A pages or chat-transcript archives. Minor procedural, temporary, or disposable answers remain in chat.

## Maintenance

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
- disagreement between concept tags and the tag registry in `schema.md`.

Agents may apply clear, low-risk corrections automatically and record them. Applying an already approved tag to a concept, or removing one that plainly does not apply, is ordinary maintenance. Changing the tag registry requires the proposal described in `schema.md`, with the affected concepts and retrieval benefit. Broad structural, destructive, sensitive, or ambiguous changes require approval.

Keep `wiki/` flat until navigation becomes genuinely difficult. Prefer titles, links, and a small maintained tag registry before folders.

## Indexes

`wiki/index.md` is mandatory locally. It carries the bundle's `okf_version` declaration and groups useful entries under headings. Each entry is a Markdown link and should include the linked concept's `description` when available.

Update an index after ingest, durable query filing, or maintenance changes what readers should discover. Create a subdirectory index only when it improves progressive disclosure. Subdirectory indexes have no frontmatter. Resolve every index link relative to the index file's location.

## Log

`wiki/log.md` is mandatory in every history mode. It has no frontmatter and begins with `# Directory Update Log`. Group concise operation bullets newest-first under date-only `YYYY-MM-DD` headings. Record meaningful ingests, filed query findings, maintenance, and concept changes. Link affected concepts when useful.

The log records what happened. It is not a diff and cannot restore prior content.

## History Modes

### Git And Log

Git is strongly recommended because it adds diffs, attribution, and rollback. Before committing, inspect the worktree, preserve unrelated changes, stage only the current operation, and create one focused local commit when host rules allow it. Never push, rewrite history, or perform a destructive rollback without authority.

### Log Only

The wiki remains usable in log-only mode, but rollback is unavailable. Explain this limitation during initialization. Without Git, get approval before substantively replacing existing content and before every structural or destructive change. Continue to record all meaningful operations in `wiki/log.md`.

## Attested Computation

OKF records a computation contract; it does not execute it. Treat each `Attested Computation` as its own concept.

`runtime` is the only computation-specific field required for every Attested Computation. `parameters`, `computation`, `executor`, and `attester` are optional and retain their exact OKF section 10 meanings. Use them only when they apply:

- Add `parameters` only when the computation has typed, named inputs. Omit it when there are no inputs; never add an empty optional list.
- When a computation is provided, use either one inline fenced block under `# Computation` or a `computation` path, never both.
- An `executor` describes how to run the computation and which receipt fields a run returns.
- An `attester` identifies a deterministic, non-LLM check of a receipt.

Do not claim executable validity without a usable computation and executor. Do not claim attestable validity without a usable attester. During an attested run, an agent may supply values only for declared parameters. It must not author or alter the sanctioned computation. The consumer binds the values, the executor returns the declared receipt, and the deterministic attester checks what ran and the displayed result.

A failed attestation blocks use or display of the value and must be surfaced. When `today >= stale_after`, warn or refuse according to the risk. `verified` records a check of the stored definition; attestation checks one execution. One never replaces the other, and per-run receipts are not stored in the bundle merely as verification history.

## Conformance

Before finalizing any wiki operation, validate the complete bundle against OKF v0.2 and the local profile:

1. Every non-reserved `.md` file has parseable YAML frontmatter and all locally required fields.
2. Every concept has a non-empty `type`.
3. Every `index.md` and `log.md` follows the reserved format. The root index and root log are present.
4. Every optional provenance, trust, lifecycle, path, and computation field that appears has the upstream structure.
5. Actor identifiers follow the patterns in `schema.md`.
6. Every source-linked footnote label resolves to a matching `sources[].id`, and every cited source ID has a footnote.
7. Every Attested Computation passes the type-specific checks in `schema.md` and OKF section 10.
8. Unknown fields and types are preserved.
9. Broken links are reported but do not fail OKF conformance.
10. Local tag use agrees with the tag registry.

Consumers must accept missing optional OKF families, unknown fields and types, broken links, and missing non-root indexes as the specification requires. Local-profile checks may still be stricter for this repository.

If a required check fails, correct it when the fix is clear and within scope. Otherwise stop: do not mark the operation complete or create its automatic commit. Report the failed check, affected files, retained changes, and the approval or information needed. Never invent provenance, verification, access, or attestation to make validation pass.
