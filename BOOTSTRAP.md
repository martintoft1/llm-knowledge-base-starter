# Bootstrap An LLM Wiki

Use this file only to initialize a new knowledge base from this repository. Do not copy `BOOTSTRAP.md` into the initialized knowledge base.

Begin by asking exactly this question and nothing else:

> What do you want this knowledge base to help you with, and what kind of material should it organize? For example: business, studies, research, personal notes, a writing project, a trip, or another specific project.

Ask one follow-up question at a time. Ask only when the answer changes files, behavior, or safety. Infer harmless defaults, state important assumptions, and explain consequential recommendations briefly.

Do not create or modify files during discovery.

## Discovery

Determine only what the setup needs:

- Purpose, scope, exclusions, and local terminology.
- Target directory and any files already there.
- Sensitive-data rules for reading, storing, quoting, linking, logging, and committing.
- Preferred writing style when it would materially change the wiki.
- Stable actor identifiers needed for initial content or verification.
- History mode: Git and log, or log-only.
- Likely source material and whether any approved source should be retained under `raw/` now.
- Relevant external systems and available read tools, but only under the conditional rule below.
- Agent adapters needed in addition to `AGENTS.md`.

Use OKF actor formats: `producer/version` for agents and tools, `human:id` for people, and `process:id` for automated processes. Use `human:owner` when a more specific human identifier is unnecessary. Do not invent an actor, verification event, or process.

Explain that `wiki/log.md` is mandatory in both history modes. Recommend Git because it provides diffs, attribution, and rollback. Log-only mode is valid and simpler, but its log cannot restore earlier content. If the target is already inside a Git repository, propose using it; do not create a nested repository.

Inspect an existing target before proposing changes. Preserve unrelated work. Name every existing file that would change, and never overwrite one without approval.

Do not design a tag taxonomy during setup. Propose seed tags only when stable recurring categories already have a clear retrieval benefit.

### External Databases And Data Systems

Ask about external databases, datasets, warehouses, analytics tools, or live systems only when the purpose is business, organizational, research-data, analytics, operational, or explicitly data-connected.

Skip that question for ordinary personal notes, study, and reading unless the user mentions an external system.

When the question is relevant:

- Ask for non-secret system names or canonical resource identifiers.
- Determine which existing agent tools, if any, already have read access.
- Record access limits and unavailable information honestly.
- Never ask for credentials, tokens, connection strings, or secret-bearing URLs.
- Do not install or configure connectors during initialization.

## Proposal Gate

Before writing, present one concrete proposal that states:

- Purpose, scope, exclusions, terminology, and target directory.
- OKF v0.2 as the pinned format and `wiki/` as the bundle.
- History mode, sensitive-data rules, writing preference, and actor identifiers.
- The exact directories and files to create or copy. Enumerate paths; do not hide them behind wildcards.
- Every existing file to change and the intended change.
- Raw-source handling, including every new raw file and confirmation that existing raw files remain unchanged.
- Normal progressive autonomy and every approval-bound exception from `references/operations.md`.
- Any approved `Dataset` or `Database` concept and its non-secret resource identifier.
- Git initialization or existing-repository behavior, or the limitations of log-only mode.
- Agent adapters, seed tags, root-path exceptions, and other important assumptions.

Approval covers only the listed files and changes. Revise the proposal when the user changes its scope.

## Complete Operating Kit

After approval, make the initialized knowledge base self-contained. Copy:

- `README.md` and `AGENTS.md`.
- The complete `references/` tree, including `references/okf/v0.2/SPEC.md` and `references/okf/v0.2/UPSTREAM.md`.
- The complete `templates/` tree.
- `CLAUDE.md` or another existing adapter only when approved and applicable.

Copy rules instead of recreating them from memory. Preserve the pinned specification byte-for-byte. Do not create a competing OKF summary, connector, credential file, required runtime, or background service.

Do not copy `BOOTSTRAP.md`.

## Initialize

After approval:

1. Create `raw/` and `wiki/`.
2. Copy the approved operating kit to the target.
3. Tailor the copied `README.md`, `references/operations.md`, `references/writing-style.md`, and approved tag registry in `references/schema.md`. Record reusable actor identifiers in the README's Local Settings. Resolve every local-setting placeholder. Replace template-only initialization text in the copied README with normal operating guidance so the result does not depend on `BOOTSTRAP.md`.
4. Create `wiki/index.md` from `templates/index.md`. Its only frontmatter key must be `okf_version: "0.2"`. Remove example entries that do not point to real concepts.
5. Create only initial concepts justified by the approved purpose, sources, or external systems. Do not create demonstration pages. Every file inside `wiki/` must be UTF-8 Markdown and follow the local profile. Keep non-Markdown evidence and support assets outside the bundle under approved `raw/` paths, or point to external, non-secret resources.
6. Add an approved raw source only when the proposal names its exact target. Never modify, overwrite, rename, move, or delete an existing raw file.
7. Initialize Git only when selected and the target is not already in a repository. Do not stage or commit yet.
8. Create mandatory `wiki/log.md` from `templates/log.md`, with no frontmatter. Remove or replace every example date, entry, and link from the template. After the approved files and settings are in place, add one truthful initialization entry under the current `YYYY-MM-DD` date.
9. Validate the final bundle, including the initialization log entry, against OKF v0.2 sections 1 through 11 and `references/schema.md`.
10. Only after validation succeeds, preserve unrelated changes, stage only initialization files, and create a focused local commit when Git is enabled and host rules allow it. Do not push. If any bundle file changes after validation, validate the final state again before staging or committing.
11. Report the initialization log entry and focused commit when one exists.

Keep `wiki/` flat until real navigation problems justify folders. Prefer clear titles, links, and a small approved tag registry. A new concept starts with the least structure its content needs, normally `status: draft`; there is no numeric word limit.

## External Resource Concepts

When an external system is relevant and approved, create a `Database` or `Dataset` concept from the normal page template. Use a canonical, non-secret `resource` such as a public console URL, catalog URI, or stable system identifier.

Add only useful body sections:

- `# Schema` for known fields, tables, or relationships.
- `# Examples` for safe examples.
- `# Access` for available read tools, permissions boundaries, and how access is requested outside the wiki.
- `# Limitations` for missing access, freshness, coverage, or uncertainty.

Never store credentials or secret-bearing connection details. Do not claim access that was not confirmed. Recording a system does not authorize connecting to it, expanding access, or writing to it. Do not read an external system during initialization unless the approved proposal separately names that read.

## Validate Before Completion

Run the complete procedure in the copied `references/operations.md` section `Validation And Conformance` against the final `wiki/` state, including the truthful initialization log entry. Use the copied `references/schema.md` as the local constraint source and section 11 of the pinned specification as the base authority.

Also confirm that the copied specification matches the checksum in `references/okf/v0.2/UPSTREAM.md`, index links resolve from each index's location, all local-setting placeholders are resolved in tailored operating files, and documented replacement markers remain in reusable templates. Treat broken links as warnings under the operations procedure. Any required failure blocks staging and commit; report it rather than inventing data.

## Verification Scenarios

Check representative initialized wikis against the copied operating kit. Do not restate field rules here; expected outcomes come from `references/schema.md` and `references/operations.md`. Do not leave test concepts in the user's wiki.

1. A personal notes, study, or reading setup completes without an external-database question when no system was mentioned.
2. A business, organizational, analytics, operational, or research-data setup can record an approved external `Database` or `Dataset` using a non-secret resource and honest access limits, without credentials or connector setup.
3. Git-and-log mode records a focused local commit only after the logged final bundle passes validation; log-only mode remains usable and clearly states that rollback is unavailable.
4. Existing raw sources remain immutable, while a new raw source is added only through exact approval.
5. Minimal and metadata-rich concepts pass their applicable schema constraints without invented optional metadata.
6. Provenance, actors, lifecycle fields, source attribution, tags, unknown fields, and broken links produce the results defined by the schema and validation procedure.
7. The root index declares OKF v0.2 in the reserved format, and the mandatory log uses the reserved date-grouped format.
8. Durable or potentially useful query findings are filed into an existing or distinct concept, while disposable chat is not archived as a Q&A page.
9. Maintenance checks links, provenance, conflicts, types, tags, and the tag registry, applying only low-risk changes autonomously.
10. Complete stable and incomplete draft Attested Computations produce the results defined by the schema.
11. Failed attestation blocks the value, and stale computation warns or refuses according to risk.
12. No non-Markdown member remains in `wiki/`; approved evidence or support assets are under `raw/` or represented by external, non-secret resource references.
13. The knowledge base can be operated from its copied README, AGENTS, specification, local rules, indexes, logs, and templates after `BOOTSTRAP.md` is absent.

## Finish

Report:

- Every path created or changed.
- The purpose, boundaries, actors, history mode, and external-resource decisions.
- Validation results, broken-link warnings, and any unresolved limitation.
- The initialization log entry and focused commit, when present.
- How to add the first approved source or ask the first substantive question.

Do not claim completion until required validation passes.
