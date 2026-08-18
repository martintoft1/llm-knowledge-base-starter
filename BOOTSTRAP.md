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

## Validate OKF And The Local Profile

Before finishing, validate the complete `wiki/` tree:

1. Only `wiki/` is treated as the OKF bundle. Every non-reserved concept is a UTF-8 Markdown file with parseable YAML frontmatter. This local profile permits no other file kind inside `wiki/`. Route non-Markdown evidence and support assets to approved `raw/` paths or external, non-secret resource references.
2. Every concept has a non-empty `type` and all locally required `title`, `status`, `tags`, and `generated` fields. Stable concepts have a one-sentence `description`.
3. Optional `resource`, `sources`, `usage_window`, `verified`, `stale_after`, and computation fields follow their exact upstream structures. Absent optional values are omitted.
4. Agent, human, and process identifiers follow the OKF actor convention.
5. Every claim footnote label resolves to the same `sources[].id`, and every cited source ID has a matching footnote. There is no separate citations section.
6. Markdown links and path-valued fields follow OKF. Report broken links, but do not fail conformance because of them.
7. `wiki/index.md` has only the permitted `okf_version: "0.2"` frontmatter and valid, relative index entries. Subdirectory indexes, if justified, have no frontmatter.
8. `wiki/log.md` has no frontmatter, begins with `# Directory Update Log`, and groups truthful entries newest-first under `YYYY-MM-DD` headings. No example date, entry, or link from the template remains.
9. Every `Attested Computation` has `runtime`, regardless of status. A draft may omit other contract families, but every field that appears must follow OKF section 10. Never permit an empty `parameters` list; omit it from an incomplete draft. Before an Attested Computation becomes `stable`, require all of the following:
   - A non-empty `parameters` list. Every entry has `name`, `type`, and `required`. A zero-input computation remains `draft`.
   - Exactly one computation form: one inline fenced block under `# Computation`, or a `computation` path, but not both.
   - `executor.resource` and a non-empty `executor.receipt` list.
   - `attester.resource` naming a deterministic, non-LLM check.
   - One or more relevant `sources` entries with stable `id` values and matching keyed footnotes.
   - At least one `verified` event from an actor independent of `generated.by`.
   - `stale_after` when the definition can expire.

   Reject `stable` when any required contract part is missing. Do not claim executable or attestable validity without the required real resources.
10. Unknown types and frontmatter fields are preserved and accepted.
11. All required OKF and local checks pass. A failure blocks completion and an automatic Git commit; report what remains wrong instead of inventing data to pass.

Also confirm that the copied specification still matches the checksum in `references/okf/v0.2/UPSTREAM.md`. Check index links from their index location and report missing targets under the broken-link rule. Resolve every local-setting placeholder in tailored operating files; keep documented replacement markers inside reusable templates.

## Verification Scenarios

Check the initialized result and its operating rules against these cases. Do not leave test concepts in the user's wiki.

1. A personal notes, study, or reading setup completes without an external-database question when no system was mentioned.
2. A business, organizational, analytics, operational, or research-data setup can record an approved external `Database` or `Dataset` using a non-secret resource and honest access limits, without credentials or connector setup.
3. Git-and-log mode records a focused local commit only after the logged final bundle passes validation; log-only mode remains usable and clearly states that rollback is unavailable.
4. Existing raw sources remain immutable, while a new raw source is added only through exact approval.
5. A minimal new concept uses the local required frontmatter, an allowed actor format, and no invented optional metadata.
6. Provenance, trust, lifecycle, and source credibility fields follow OKF when used. Source-linked claim footnotes match `sources[].id`.
7. The root index declares OKF v0.2 in the reserved format, and the mandatory log uses the reserved date-grouped format.
8. Durable or potentially useful query findings are filed into an existing or distinct concept, while disposable chat is not archived as a Q&A page.
9. Maintenance checks links, provenance, conflicts, types, tags, and the tag registry, applying only low-risk changes autonomously.
10. A stable Attested Computation has a non-empty typed parameter list, exactly one real sanctioned computation, an executor with a non-empty receipt, a deterministic non-LLM attester, keyed provenance, independent verification, and conditional `stale_after`. A runtime-only stable computation and an empty parameter list are rejected.
11. An incomplete Attested Computation may remain `draft` when it has `runtime`; any optional contract field that appears still follows OKF section 10.
12. Failed attestation blocks the value, and stale computation warns or refuses according to risk.
13. No non-Markdown member remains in `wiki/`; approved evidence or support assets are under `raw/` or represented by external, non-secret resource references.
14. Unknown types and extension fields survive a read-and-write cycle.
15. Broken links are reported without making an otherwise conformant bundle fail.
16. The knowledge base can be operated from its copied README, AGENTS, specification, local rules, indexes, logs, and templates after `BOOTSTRAP.md` is absent.

## Finish

Report:

- Every path created or changed.
- The purpose, boundaries, actors, history mode, and external-resource decisions.
- Validation results, broken-link warnings, and any unresolved limitation.
- The initialization log entry and focused commit, when present.
- How to add the first approved source or ask the first substantive question.

Do not claim completion until required validation passes.
