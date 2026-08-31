# Wiki Operations

This file defines how agents add, use, review, and record knowledge. [`local-settings.md`](local-settings.md) defines the current settings, and [`schema.md`](schema.md) defines the wiki schema.

## Global Prerequisite: Safety

Before every operation, read [Safety](local-settings.md#safety) and keep it in effect throughout the work. Apply its storage and sharing rules to source material, search queries, wiki content, logs, commits, responses, and external systems.

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

Apply [Safety](local-settings.md#safety) whenever information is read, stored, or shared. Agents with approved access may read and use material stored in the knowledge base. Never persist anything covered by `May not store` in the wiki, raw evidence, logs, or Git history. Ask before sharing anything covered by `May not share externally` with a person or system outside the knowledge base's approved access boundary. Approval applies only to the named audience, system, material, and purpose.

### Raw Evidence

Apply [Safety](local-settings.md#safety) before retaining evidence. Keep retained original evidence under `raw/` and authored knowledge under `wiki/`.

Existing raw files are immutable to agents. Never modify, overwrite, rename, move, or delete one. A correction or derived artifact becomes a new source. Adding a new raw source on the user's behalf requires approval, even when the source was already identified. A human may manage raw material directly outside this workflow. `raw/.gitkeep` is only a tracked placeholder, not evidence; ignore it and leave it unchanged.

Preserve each source in its useful native format. When repeated reading or evidence checking needs searchable text, an approved durable rendering may be added under `raw/_derived/` and recorded in `sources[].representation` as defined by [`schema.md`](schema.md#provenance-sources-and-usage_window). The rendering is an immutable aid, not a replacement for the original. Temporary extractions do not need to be retained.

Do not pretend to have read an unavailable source or external system. Record the limitation instead.

## Shared Completion

After an operation changes the wiki:

1. Update the complete root index and add one concise log entry using the rules in [`schema.md`](schema.md#reserved-files).
2. Validate every directly changed path and the dependencies selected by the validator.
3. Review the affected concepts manually. Confirm that boundaries remain atomic, claims match their sources, inference and uncertainty are clear, links express the intended relationships, and cascade effects were handled.
4. Resolve unintended warnings. Stop and report any required check that cannot be corrected within scope.
5. If Git is enabled and host rules allow it, create one focused local commit.
6. Report the concepts changed, important uncertainty or conflict, and the log entry or commit.

## Core Operations

### Ingest

Use Ingest when the user explicitly asks to add supplied or identified material to the wiki. Prefer one source at a time when practical.

#### Intake

Apply [Safety](local-settings.md#safety) while accessing and assessing the source. Check its relevance, provenance, sensitivity, uncertainty, and storage restrictions. Ask for approval before retaining a new raw file. Preserve an approved source in its useful native format and create a durable representation only when justified.

#### Triage

Read `wiki/index.md`, then search the complete wiki using the source's key terms, names, aliases, synonyms, identifiers, and material claims. Decide whether the source should create a concept, update a concept, add supporting evidence, record a conflict, or be retained but unused. The first four results may be combined; retained but unused is exclusive.

#### Compile

Create or update the atomic concepts that the source materially informs. Before adding or changing tags, read the [Tag Registry](local-settings.md#tag-registry) and use only approved tags. Add provenance in `sources`; use stable source IDs and matching footnotes for attributed claims. Do not create a source summary when the knowledge belongs in existing concepts. Preserve useful conflict instead of silently choosing one account.

#### Check

Check exact quotations, dates, numbers, and identifiers against accessible evidence. Review every material claim and distinguish direct support, synthesis, inference, dispute, unsupported content, and unavailable evidence. Correct or remove unsupported content.

Record `verified` only after a real check against `resource` or `sources`. Assess freshness separately and add `stale_after` only when a defensible review or expiry date exists.

#### Cascade

Search the complete wiki for affected concepts, aliases, claims, sources, summaries, links, and index descriptions. Update every live concept whose meaning changed. Do not rewrite snapshots; note when their source concepts changed so Maintenance can review them.

#### Finish

Follow [Shared Completion](#shared-completion). If the retained source was not used, record it with the exact `Retained but unused` log form and explain why.

### Research

Use Research only when the user asks the agent to find sources for the knowledge base. Ordinary knowledge questions use Query and do not start autonomous source gathering.

Apply [Safety](local-settings.md#safety) to search queries, candidate sources, retained files, and research reports.

1. Define the question, scope, and useful search angles.
2. Search with official names, aliases, abbreviations, and synonyms. Deliberately look for criticism, failures, and opposing evidence.
3. Assess candidates for relevance, authority, independence, recency, and duplication.
4. Propose the sources worth retaining and obtain batch approval when adding raw files requires it.
5. Pass each selected source through the full Ingest flow. Discovery may run in parallel, but compilation remains sequential because concepts, indexes, logs, and cascade updates share state.
6. Report coverage, gaps, and unresolved conflict. Create a sourced `Analysis` only when a durable cross-source synthesis is useful and authorized.

Do not log rejected candidates that were never retained.

### Query And Accumulation

Read the complete `wiki/index.md`, then search the wiki using the question's key terms, aliases, and synonyms. Do not conclude that the wiki lacks relevant knowledge until both the index and full-text search are empty; say when that search found nothing.

Follow relevant concepts and sources, and consult raw evidence when needed. Prefer wiki knowledge, link the concepts used in the answer, and label any outside knowledge clearly. Surface stale, disputed, inaccessible, or weakly supported knowledge instead of hiding the limitation. Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict.

Answer the user before considering a wiki update. Then decide whether information supplied by the user or surfaced by the answer is likely worth storing. It should be durable, relevant to the current work or existing wiki, likely to be reused, and not already captured.

When information is likely worth storing, briefly propose the knowledge itself. Do not require the user to review filenames, metadata, or full file contents. The user may accept, decline, or suggest changes. If the user suggests changes, present a revised proposal. Do not change the wiki until the proposal is accepted.

After acceptance, update or create the appropriate atomic concepts and add justified sources, metadata, and links. An explicit ingest or wiki-update request already authorizes ordinary storage and skips this proposal. Broad structural, destructive, sensitive, or otherwise approval-bound work still requires its normal approval.

Do not create generic Q&A pages or chat-transcript archives. Minor procedural, temporary, or disposable answers remain in chat.

After an accepted addition, follow [Shared Completion](#shared-completion).

### Snapshot

Create a snapshot only when the user explicitly asks to preserve a point-in-time synthesis.

1. Create a focused `Analysis` with `snapshot: true`.
2. Use the canonical internal concepts it derives from in `sources`, with keyed footnotes for material claims.
3. State that the result is a point-in-time synthesis and avoid copying its source concepts extensively.
4. Do not cascade-update the snapshot when its sources change; Maintenance should surface the change.
5. Follow [Shared Completion](#shared-completion).

### Maintenance

Maintenance may review a selected area or the complete wiki. It has three parts.

Before reviewing or changing tags, read the [Tag Registry](local-settings.md#tag-registry).

#### Validate

Run the required mechanical checks for OKF and wiki-schema conformance, complete index coverage, metadata, paths, links, freshness, trust signals, provenance, snapshots, types, tags, and Attested Computations.

#### Audit

Review contradictions, unsupported or overstated claims, unjustified inference, stale or deprecated knowledge, missing conflict annotations, overloaded or duplicate concepts, weak or redundant links, orphaned concepts, missing provenance, important missing concepts, changed snapshot sources, extraction limitations, type drift, and tag drift.

#### Repair

Apply deterministic, low-risk corrections automatically. Report ambiguous or semantic problems with a recommendation. Ask before structural, destructive, broad, sensitive, or otherwise approval-bound changes.

Repair a broken link automatically only when one intended moved target is unambiguous. Remove dead index and navigational links. Never silently remove evidence, computation, provenance, or another load-bearing link; report it when the correct repair is unclear.

Applying an approved tag to a concept, or removing one that plainly does not apply, is ordinary maintenance. Changing the [Tag Registry](local-settings.md#tag-registry) requires the proposal described in `schema.md`, with the affected concepts and retrieval benefit.

Keep `wiki/` flat until navigation becomes genuinely difficult. Prefer titles, links, and a small maintained tag registry before folders. After repairs, repeat the affected checks and follow [Shared Completion](#shared-completion).

## Specialized Operations

### External Access And Connector Setup

Use an approved `Database` or `Dataset` concept to keep external access discoverable. Its `# Access` section records the current access state, existing approved tools, intended method when known, allowed scope, storage and sharing restrictions, approval still needed, and next action. Its `# Limitations` section explains what cannot currently be retrieved or verified. When access is pending, say so in the concept's index description and record that fact in `wiki/log.md`.

Complete ordinary wiki work without requiring a connector when useful work remains possible. If setup is postponed, keep the external-resource concept current. Create a linked `Plan` concept only after the user chooses to proceed and the setup has multiple useful actions to track.

Connecting a new external system or increasing access requires a separate proposal and approval. The proposal names the system, integration, requested read or write scope, files or settings that will change, and how authentication will occur. Use an approved provider authentication flow and apply [Safety](local-settings.md#safety) to anything stored or shared during setup.

After approved setup, verify the actual access rather than assuming it succeeded. Update the external-resource concept and preserve any remaining limitation, then follow [Shared Completion](#shared-completion).

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
- wiki files whose Markdown links or frontmatter paths refer to a changed, deleted, or renamed wiki or raw file;
- every concept using a tag whose registry entry was added, removed, renamed, or changed; and
- the required root index and log.

The search reads wiki files to find dependencies, but full YAML and schema validation runs only on the affected set. The output lists direct and dependent paths so the agent can check the selected scope. Bundle file kinds and required root files are always checked.

Run a complete validation with `python3 references/validate-wiki.py --all` after changing the schema, validator, templates, or pinned OKF version; during broad maintenance or reorganization; or whenever the affected set is uncertain. Running the script without a mode also performs a complete validation. Changed mode falls back to complete validation when Git history is unavailable.

Python 3 and PyYAML are required. If PyYAML is unavailable, the script prints the installation command and exits. Both modes report Base OKF failures, wiki-schema failures, and warnings separately, and preserve unknown fields and types.

Correct every Base OKF or wiki-schema failure when the fix is clear and within scope. Otherwise stop: do not mark the operation complete or create its automatic commit. Report the failed check, affected files, retained changes, and the approval or information needed. Review warnings and resolve those that are not intentional.

Then review the direct and dependent files manually. Confirm that concept boundaries are atomic, claims match their sources, uncertainty and conflicts are clear, links express the intended relationships, and any attester is deterministic and non-LLM. The script cannot determine whether a prose change alters another concept's meaning, so follow relevant links when semantic impact may extend beyond the selected structural dependencies. Never invent provenance, verification, access, or attestation to make validation pass.
