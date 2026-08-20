# Bootstrap An LLM Wiki

In this starter repository, use this file to initialize a new knowledge base. The complete `references/` tree carries it to the same path in the initialized knowledge base, where it becomes an archive. Routine operation must not depend on the archived copy.

## Discovery Questions

Use the following questions in order. Ask one question at a time. Skip a question when its answer is already clear from the user's earlier answers or the inspected target, and record the inferred answer in the proposal. Ask a follow-up only when it changes files, behavior, access, or safety.

Inspect the target before asking about existing files. Preserve unrelated work, name every existing file that would change, and never overwrite one without approval.

Do not create or modify files during discovery.

1. **Purpose and material.** Ask "What do you want this knowledge base to help you with, and what kind of material should it organize? For example: business, studies, research, personal notes, a writing project, a trip, or another specific project.". From the answer, determine purpose, likely scope, and relevant material.
2. **Boundaries and terminology.** When exclusions or naming remain unclear, ask: "Is there anything this knowledge base should exclude, and are there local terms or naming conventions it should use?"
3. **Sensitive data.** Ask: "Will this knowledge base involve sensitive or restricted material? If so, what may agents read, store, quote, link to, mention in logs, and commit to Git?"
4. **Restricted material that cannot be stored.** When storage is restricted, ask: "Where will the restricted material remain, how may an agent access it, and may the knowledge base store non-sensitive identifiers, metadata, summaries, or conclusions derived from it? Do not provide credentials."
5. **Writing style.** Ask: "The default is concise reference notes that preserve useful reasoning. Keep this default (recommended), or add or change any writing preferences?"
6. **People and provenance.** Ask: "Will anyone besides you create or verify content in this knowledge base?" If yes, ask for an agreed, unique, non-secret identifier for each relevant person. Legal names are optional; stable usernames or pseudonyms are valid. Do not record identifiers for read-only users.
7. **History.** Ask: "Use Git plus the mandatory wiki log (recommended), or the wiki log only? Git adds diffs and rollback; the log alone cannot restore earlier content."
8. **Sources to retain.** Ask: "Should any approved source be retained under `raw/` during initialization?" If yes, identify each source and exact target path for the proposal. Do not copy it during discovery.
9. **External systems.** Ask this only when the purpose or sources are business, organizational, analytics, operational, research-data, or explicitly connected to a database, dataset, warehouse, CRM, or other live system: "Which external systems should this knowledge base use, and which existing approved tools already have read access? Give only non-secret names or canonical resource identifiers; do not provide credentials."
10. **Agent adapters.** Ask: "`AGENTS.md` is the shared instruction entry point. Which additional agents or editors will operate this knowledge base, such as Claude, Gemini, or Cursor?" Use `CLAUDE.md` when applicable. Propose the exact path for every other adapter before creating it.

Use OKF actor formats: `producer/version` for agents and tools, `human:id` for people, and `process:id` for automated processes. Use `human:owner` when a more specific human identifier is unnecessary. Do not invent an actor, verification event, or process.

`wiki/log.md` is mandatory in both history modes. Recommend Git and the log. If the target is already inside a Git repository, propose using it; do not create a nested repository.

Do not design a tag taxonomy during setup. Propose seed tags only when stable recurring categories already have a clear retrieval benefit.

### Deferred External Access

Core initialization must not require connector installation. When external access is relevant, document the system, permitted access, sensitive-data limits, existing tools, and any missing access first.

If access is unavailable or connector setup is postponed, propose a `Database` or `Dataset` concept that records the pending state under `# Access` and its consequences under `# Limitations`. Mention pending access in the index description and initialization log. Complete the core initialization, then offer connector setup as a separate approval-bound step that may happen immediately afterward or later.

Never ask for credentials, tokens, connection strings, or secret-bearing URLs. Never install or configure a connector without a separate proposal and approval.

## Proposal Gate

Before writing, present one concrete proposal that states:

- Purpose, scope, exclusions, terminology, and target directory.
- OKF v0.2 as the pinned format and `wiki/` as the bundle.
- History mode; sensitive-data rules for reading, storing, quoting, linking, logging, committing, and permitted derived content; writing preference; and actor identifiers.
- The exact directories and files to create or copy. Enumerate paths; do not hide them behind wildcards.
- Every existing file to change and the intended change.
- Raw-source handling, including every new raw file and confirmation that existing raw files remain unchanged.
- Normal progressive autonomy and every approval-bound exception from `references/operations.md`.
- Any approved `Dataset` or `Database` concept, its non-secret resource identifier, current access state, sensitive-data boundary, and permitted derived content.
- Any deferred connector setup, including the intended access method, allowed scope, approval still needed, and next action.
- Git initialization or existing-repository behavior, or the limitations of log-only mode.
- Exact agent-adapter paths, seed tags, top-level path exceptions, and other important assumptions.
- The archived bootstrap and its provenance record.

Approval covers only the listed files and changes. Revise the proposal when the user changes its scope.

## Complete Operating Kit

After approval, make the initialized knowledge base self-contained. Copy:

- `README.md`, `AGENTS.md`, `VERSION`, `CHANGELOG.md`, `LICENSE`, and `NOTICE`.
- The complete `references/` tree, including `references/okf/v0.2/SPEC.md` and `references/okf/v0.2/UPSTREAM.md`.
- The complete `templates/` tree.
- `CLAUDE.md` and any other existing adapter only when each is approved and applicable.

The complete `references/` tree preserves this file byte-for-byte at `references/initialization/BOOTSTRAP.md`. In the initialized knowledge base, that copy is the initialization archive.

Also create `references/initialization/PROVENANCE.md`. Begin with `# Initialization Provenance`, then record `Initialized`, `Starter source`, `Starter version or Git commit`, and `Bootstrap SHA-256` as a short Markdown list. Use the exact non-empty value from `VERSION` for the starter version. If it is unavailable, use the exact source Git commit when known; otherwise use `unavailable` rather than inventing source or version information.

Copy rules instead of recreating them from memory. Preserve the pinned specification and archived bootstrap byte-for-byte. Do not create a competing OKF summary, connector, credential file, required runtime, or background service. Routine operation must not depend on the archived bootstrap.

## Initialize

After approval:

1. Create `raw/` and `wiki/`.
2. Copy the approved operating kit to the target. Confirm that `references/initialization/BOOTSTRAP.md` was preserved byte-for-byte, then create its provenance record before tailoring any copied operating file.
3. Tailor the copied `references/local-settings.md` and `README.md` overview. Record the approved writing style, tag registry, and reusable actor identifiers in `references/local-settings.md`; do not duplicate its settings in the README or other reference files. Resolve every local-setting placeholder. Replace the template-only `Initialize A Wiki` section with a short initialization record that links to the archived bootstrap and provenance file. Preserve the versioning and license sections and their links to the copied files. The result must not depend on the archive for routine operation.
4. Create `wiki/index.md` from `templates/index.md`. Its only frontmatter key must be `okf_version: "0.2"`. Remove example entries that do not point to real concepts.
5. Create only initial concepts justified by the approved purpose, sources, or external systems. Do not create demonstration pages. Every file inside `wiki/` must be UTF-8 Markdown and follow the wiki schema. Keep non-Markdown evidence and support assets outside the bundle under approved `raw/` paths, or point to external, non-secret resources.
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

When connector setup is pending, `# Access` records the current state, intended access method when known, allowed scope, sensitive-data restrictions, approval still needed, and next action. `# Limitations` explains what cannot yet be retrieved or verified. Mention pending access in the concept's index description and in the initialization log.

Create a separate `Plan` concept only after the user decides to proceed and the setup has multiple useful actions to track. Link it to the external-resource concept.

Never store credentials or secret-bearing connection details. Do not claim access that was not confirmed. Recording a system does not authorize connecting to it, expanding access, or writing to it. Do not read an external system during core initialization unless the approved proposal separately names that read. Offer connector setup only as a separate approval-bound step after core initialization; it may be completed immediately afterward or postponed.

## Validate Before Completion

Run the complete procedure in the copied `references/operations.md` section `Validation And Conformance` against the final `wiki/` state, including the truthful initialization log entry. Use the copied `references/schema.md` as the wiki-schema source and section 11 of the pinned specification as the base authority.

Also confirm that the copied `VERSION` is non-empty and matches the starter version recorded in `references/initialization/PROVENANCE.md`, the copied specification matches the checksum in `references/okf/v0.2/UPSTREAM.md`, the archived bootstrap matches the `Bootstrap SHA-256` value in `references/initialization/PROVENANCE.md`, index links resolve from each index's location, every placeholder in `references/local-settings.md` is resolved, other tailored operating files contain no unresolved local placeholders, and documented replacement markers remain in reusable templates. Treat broken links as warnings under the operations procedure. Any required failure blocks staging and commit; report it rather than inventing data.

## Verification Scenarios

Check representative initialized wikis against the copied operating kit. Do not restate field rules here; expected outcomes come from `references/schema.md` and `references/operations.md`. Do not leave test concepts in the user's wiki.

1. A personal notes, study, or reading setup completes without an external-system question when no system was mentioned.
2. A business, organizational, analytics, operational, or research-data setup can record an approved external `Database` or `Dataset` using a non-secret resource, permitted derived content, and honest access limits without requiring connector setup.
3. `references/local-settings.md` is the single source for every setting that varies between knowledge bases, including writing style, approved tags, history mode, and sensitive-data rules. Git-and-log mode records a focused local commit only after the logged final bundle passes validation; log-only mode remains usable and clearly states that rollback is unavailable. A later mode change updates local settings and the log without reinitializing the wiki.
4. Existing raw sources remain immutable, while a new raw source is added only through exact approval.
5. Minimal and metadata-rich concepts pass their applicable schema constraints without invented optional metadata.
6. Provenance, actors, lifecycle fields, source attribution, tags, unknown fields, and broken links produce the results defined by the schema and validation procedure.
7. The root index declares OKF v0.2 in the reserved format, and the mandatory log uses the reserved date-grouped format.
8. Durable or potentially useful query findings are filed into an existing or distinct concept, while disposable chat is not archived as a Q&A page.
9. Maintenance checks links, provenance, conflicts, types, tags, and the tag registry, applying only low-risk changes autonomously.
10. Complete stable and incomplete draft Attested Computations produce the results defined by the schema.
11. Failed attestation blocks the value, and stale computation warns or refuses according to risk.
12. No non-Markdown member remains in `wiki/`; approved evidence or support assets are under `raw/` or represented by external, non-secret resource references.
13. The knowledge base can be operated from its copied README, AGENTS, specification, local rules, indexes, logs, and templates without reading or relying on the archived bootstrap.
14. `VERSION`, `CHANGELOG.md`, `LICENSE`, and `NOTICE` are copied into the initialized knowledge base, and the provenance record contains the exact starter version from `VERSION`.
15. A shared setup asks about other creators and verifiers, records only approved unique non-secret actor identifiers, does not require legal names, and does not record read-only users.
16. Discovery follows the ordered question list, asks one question at a time, skips answers already established by the user or target, and records every inference in the proposal.
17. A no-storage sensitive-data setup records where the restricted source remains, how it may be accessed, what derived content may be stored, and any deferred access without storing credentials.
18. Writing-style discovery states the concise-reference default, recommends keeping it, and records any approved additions or changes.
19. Adapter discovery always retains `AGENTS.md`, includes `CLAUDE.md` only when applicable, and proposes an exact approved path before adding another adapter.
20. Deferred connector setup remains discoverable through the external-resource concept, its index description, and the initialization log; a separate `Plan` appears only after the user chooses to proceed and multiple actions need tracking.

## Finish

Report:

- Every path created or changed.
- The purpose, boundaries, actors, history mode, and external-resource decisions.
- Validation results, broken-link warnings, and any unresolved limitation.
- The initialization archive path, provenance, and verified bootstrap checksum.
- The initialization log entry and focused commit, when present.
- How to add the first approved source or ask the first substantive question.

Do not claim completion until required validation passes.
