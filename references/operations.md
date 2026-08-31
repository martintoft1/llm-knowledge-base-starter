# Wiki Operations

This file defines how agents add, use, review, and record knowledge. [`local-settings.md`](local-settings.md) defines the current settings, and [`schema.md`](schema.md) defines the wiki schema.

## Required Local Settings

Read only the settings needed for the operation:

- [Safety](local-settings.md#safety) before every operation. Apply its storage and sharing rules to source material, wiki content, logs, commits, and responses.
- [Tag Registry](local-settings.md#tag-registry) before adding, removing, reviewing, or validating tags.

Do not duplicate those settings here.

## Operating Principles

### Bundle Boundaries

Every member of the `wiki/` bundle must be UTF-8 Markdown with a `.md` filename. This is a local restriction beyond base OKF. Keep non-Markdown evidence and support files outside the bundle: retain evidence under `raw/`, or point to an external resource allowed by [Safety](local-settings.md#safety).

### Authority

Agents may perform ordinary, low-risk work under `wiki/` without separate approval when the user directly requests the work or accepts a suggested addition. This includes creating and updating concepts, sources, claim footnotes, links, metadata, indexes, and logs; fixing clear formatting or conformance errors; and making focused local commits when Git is enabled and host rules allow it.

Approval is required before an agent:

- adds a raw source on the user's behalf;
- deletes a concept;
- performs broad merges, splits, moves, renames, or reorganizations;
- changes local settings;
- changes the pinned OKF version, schema, operating rules, templates, or autonomy settings;
- connects a new external system or increases existing access;
- writes to an external system;
- stores or exposes sensitive material beyond the stated settings; or
- performs an ambiguous or unusually broad action.

A direct user request is approval only for its stated scope. For approval-bound work, name the affected files, the intended result, and what happens to the originals before writing.

### Information Use And Sharing

Agents with approved access may read and use material stored in the knowledge base. Never persist anything covered by `May not store` in the wiki, raw evidence, logs, or Git history. Ask before sharing anything covered by `May not share externally` with a person or system outside the knowledge base's approved access boundary. Approval applies only to the named audience, system, material, and purpose.

### Raw Evidence

Keep retained original evidence under `raw/` and authored knowledge under `wiki/`.

Existing raw files are immutable to agents. Never modify, overwrite, rename, move, or delete one. A correction or derived artifact becomes a new source. Adding a new raw source on the user's behalf requires approval, even when the source was already identified. A human may manage raw material directly outside this workflow. `raw/.gitkeep` is only a tracked placeholder, not evidence; ignore it and leave it unchanged.

Do not pretend to have read an unavailable source or external system. Record the limitation instead.

## Special Files

### Indexes

`wiki/index.md` is mandatory locally. It carries the bundle's `okf_version` declaration and groups useful entries under headings. Each entry is a Markdown link and should include the linked concept's `description` when available.

Update an index after ingest, durable query filing, or maintenance changes what readers should discover. Create a subdirectory index only when it improves progressive disclosure. Subdirectory indexes have no frontmatter. Resolve every index link relative to the index file's location.

### Log

`wiki/log.md` is mandatory in every history mode. It has no frontmatter and begins with `# Directory Update Log`. Group concise operation bullets newest-first under date-only `YYYY-MM-DD` headings. Record meaningful ingests, filed query findings, maintenance, and concept changes. Link affected concepts when useful.

## Core Operations

### Ingest

When the user explicitly asks to ingest material:

1. Check its relevance, provenance, conflicts, uncertainty, and sensitivity. Ask for approval if retaining it requires a new raw file.
2. Create or update the atomic concepts that the source materially informs. Preserve conflicting evidence instead of silently choosing one account.
3. Add concept-level provenance in `sources`. When a body attributes a specific claim, give that source a stable `sources[].id` and use the same key for its Markdown footnote. Do not create a separate citations section.
4. Update related concepts, summaries, and cross-links when the source changes, supports, or contradicts them.
5. Update the affected index files and `wiki/log.md`.
6. Validate the affected files through the procedure below.
7. If Git is enabled and host rules allow it, create one focused local commit.
8. Report the concepts changed, important uncertainty or conflict, and the log entry or commit.

Prefer one-source-at-a-time ingest when practical so the user can guide emphasis. Do not fill the wiki with source summaries when the knowledge belongs in existing concepts.

### Query And Accumulation

Read `wiki/index.md`, follow relevant concepts and sources, and consult raw evidence when needed. Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict in the answer.

Answer the user before considering a wiki update. Then decide whether information supplied by the user or surfaced by the answer is likely worth storing. It should be durable, relevant to the current work or existing wiki, likely to be reused, and not already captured.

When information is likely worth storing, briefly propose the knowledge itself. Do not require the user to review filenames, metadata, or full file contents. The user may accept, decline, or suggest changes. If the user suggests changes, present a revised proposal. Do not change the wiki until the proposal is accepted.

After acceptance, decide how to store the knowledge: update or create the appropriate atomic concepts, add justified sources, metadata, and links, then update the relevant index and log, validate the affected files through the procedure below, and commit when Git is enabled and allowed. An explicit ingest or wiki-update request already authorizes ordinary storage and skips this proposal. Broad structural, destructive, sensitive, or otherwise approval-bound work still requires its normal approval.

Do not create generic Q&A pages or chat-transcript archives. Minor procedural, temporary, or disposable answers remain in chat.

### Maintenance

Maintenance reviews the whole affected area and checks for:

- contradictions, uncertainty, and unsupported claims;
- stale or deprecated knowledge;
- broken links;
- overloaded concepts;
- duplicate concepts or duplicated content;
- missing links needed for navigation, reuse, or dependencies, and redundant links that add clutter;
- orphaned concepts;
- missing or malformed provenance;
- important missing concepts;
- metadata that violates OKF or the wiki schema;
- stale Attested Computations and failed attestations;
- type drift;
- tags that should be added, removed, merged, narrowed, or retired; and
- disagreement between concept tags and the approved [Tag Registry](local-settings.md#tag-registry).

Agents may apply clear, low-risk corrections automatically and record them. Applying an already approved tag to a concept, or removing one that plainly does not apply, is ordinary maintenance. Changing the tag registry requires the proposal described in `schema.md`, with the affected concepts and retrieval benefit. Broad structural, destructive, sensitive, or ambiguous changes require approval.

Keep `wiki/` flat until navigation becomes genuinely difficult. Prefer titles, links, and a small maintained tag registry before folders.

After maintenance changes, update affected links, indexes, and `wiki/log.md`, validate through the procedure below, and commit when Git is enabled and allowed.

## Specialized Operations

### External Access And Connector Setup

Use an approved `Database` or `Dataset` concept to keep external access discoverable. Its `# Access` section records the current access state, existing approved tools, intended method when known, allowed scope, storage and sharing restrictions, approval still needed, and next action. Its `# Limitations` section explains what cannot currently be retrieved or verified. When access is pending, say so in the concept's index description and record that fact in `wiki/log.md`.

Complete ordinary wiki work without requiring a connector when useful work remains possible. If setup is postponed, keep the external-resource concept current. Create a linked `Plan` concept only after the user chooses to proceed and the setup has multiple useful actions to track.

Connecting a new external system or increasing access requires a separate proposal and approval. The proposal names the system, integration, requested read or write scope, files or settings that will change, and how authentication will occur. Use an approved provider authentication flow and apply [Safety](local-settings.md#safety) to anything stored or shared during setup.

After approved setup, verify the actual access rather than assuming it succeeded. Update the external-resource concept, its index description, and `wiki/log.md`; preserve any remaining limitation. Validate through the procedure below and commit only when Git is enabled and host rules allow it.

### Attested Computation

OKF records a computation contract; it does not execute it. Treat each `Attested Computation` as its own concept.

The contract requirements for draft and stable concepts live in [`schema.md`](schema.md). Apply them through the validation procedure below; do not redefine them here.

Do not claim executable validity without a usable computation and executor. Do not claim attestable validity without a usable attester. During an attested run, an agent may supply values only for declared parameters. It must not author or alter the sanctioned computation. The consumer binds the values, the executor returns the declared receipt, and the deterministic attester checks what ran and the displayed result.

A failed attestation blocks use or display of the value and must be surfaced. When `today >= stale_after`, warn or refuse according to the risk. `verified` records a check of the stored definition; attestation checks one execution. One never replaces the other, and per-run receipts are not stored in the bundle merely as verification history.

## Validation And Conformance

Before finalizing an ordinary wiki operation, run the validator from the knowledge-base root with every file directly created, changed, deleted, or renamed by that operation:

```bash
python3 references/validate-wiki.py --changed <path> [<path> ...]
```

Pass deleted paths even though they no longer exist. For a rename, pass both the old and new paths; Git may not recognize a heavily edited rename. Pass `references/local-settings.md` when the Tag Registry changes. To validate all current Git changes together, omit the paths and run `python3 references/validate-wiki.py --changed`.

The changed mode uses Git to correlate old and new paths when Git recognizes a rename. It searches the current wiki and validates:

- directly changed wiki files;
- files whose Markdown links or frontmatter paths refer to a changed, deleted, or renamed wiki file;
- every concept using a tag whose registry entry was added, removed, renamed, or changed; and
- the required root index and log.

The search reads wiki files to find dependencies, but full YAML and schema validation runs only on the affected set. The output lists direct and dependent paths so the agent can check the selected scope. Bundle file kinds and required root files are always checked.

Run a complete validation with `python3 references/validate-wiki.py --all` after changing the schema, validator, templates, or pinned OKF version; during broad maintenance or reorganization; or whenever the affected set is uncertain. Running the script without a mode also performs a complete validation. Changed mode falls back to complete validation when Git history is unavailable.

Python 3 and PyYAML are required. If PyYAML is unavailable, the script prints the installation command and exits. Both modes report Base OKF failures, wiki-schema failures, and warnings separately, and preserve unknown fields and types.

Correct every Base OKF or wiki-schema failure when the fix is clear and within scope. Otherwise stop: do not mark the operation complete or create its automatic commit. Report the failed check, affected files, retained changes, and the approval or information needed. Review warnings and resolve those that are not intentional.

Then review the direct and dependent files manually. Confirm that concept boundaries are atomic, claims match their sources, uncertainty and conflicts are clear, links express the intended relationships, and any attester is deterministic and non-LLM. The script cannot determine whether a prose change alters another concept's meaning, so follow relevant links when semantic impact may extend beyond the selected structural dependencies. Never invent provenance, verification, access, or attestation to make validation pass.
