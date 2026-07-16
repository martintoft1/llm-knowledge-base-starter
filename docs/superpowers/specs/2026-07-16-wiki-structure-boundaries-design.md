# Wiki Structure Boundaries Design

## Purpose

Strengthen the wiki initializer based on practical use. The initialized wiki should preserve reusable templates, keep all persistent domain material inside `raw/` or `wiki/`, and leave commit authority to the user or surrounding agent system rather than treating automatic commits as a wiki setting.

## Goals

- Retain an index template so agents can create justified local indexes later.
- Make `raw/` and `wiki/` strict placement boundaries for persistent domain material.
- Prevent agents from silently creating domain folders such as `CRM/` at the wiki root.
- Allow legitimate root-level exceptions through an explicit proposal and approval process.
- Distinguish retained source material, authored knowledge, temporary work, and tool-managed data.
- Separate the wiki's history mechanism from authority to create commits.
- Keep the design documentation-only and portable across agent systems.

## Non-goals

- Add a machine-readable configuration file, validator, hook, or CLI.
- Define every possible agent or tool metadata path in advance.
- Prohibit pre-existing files belonging to a surrounding repository.
- Require local indexes before navigation actually benefits from them.
- Change knowledge-page types, frontmatter, tags, citations, or writing patterns.
- Decide how a particular Codex, Claude, or other AI installation manages commits globally.

## Chosen Approach

Use a closed, documented allowlist enforced by the initializer's proposal and verification steps and by the initialized wiki's operating instructions.

This approach is preferred over a machine-readable manifest because the project is intentionally file-only and vendor-neutral. It is preferred over advisory wording because the existing default-oriented wording allowed an agent to create a top-level domain folder.

## Persistent Structure Contract

All persistent domain material created for the knowledge base must live under one of two content roots:

- `raw/` contains retained evidence and source material, including source exports, scrape results intended for retention, attachments, transcripts, datasets, and other original or preserved inputs.
- `wiki/` contains authored knowledge, including source pages, subjects, notes, syntheses, decisions, plans, domain-oriented subdirectories, and local indexes.

The canonical root allowlist is:

```text
<wiki-root>/
├── raw/
├── wiki/
├── README.md
├── AGENTS.md
├── CLAUDE.md            # Optional
├── docs/wiki/
├── templates/
├── index.md
└── log.md               # Optional
```

Pre-existing files and directories belonging to a surrounding repository may remain. Existing or newly proposed system and tool metadata, such as `.git/`, `.gitignore`, or a tool-specific cache directory, are allowed only when already part of the approved target context or explicitly approved as a root exception. They are not domain-content locations.

The initializer must not interpret "default structure" or "smallest structure" as permission to create other persistent root entries. A new root path is a structural exception and requires explicit approval before creation.

## Placement Decision

Before proposing a new path, an agent classifies the material:

1. Retained evidence or an original external output goes under `raw/`.
2. Authored or interpreted knowledge goes under `wiki/`.
3. Temporary agent working data goes in system-managed temporary storage outside the wiki root when possible.
4. Tool-required repository-local state requires a proposed root exception when it cannot use system temporary storage or an existing approved metadata path.

For example, a requested CRM structure may become:

```text
raw/crm/                 # Exports, notes, or source records
wiki/crm/                # Authored customer and sales knowledge
wiki/crm/index.md        # Optional local navigation when justified
```

It must not silently become `<wiki-root>/CRM/`.

## Root Exception Protocol

When a path does not fit the allowlist, the agent must pause before creating it and propose an allowlist expansion. The proposal must state:

- The exact path.
- Why `raw/`, `wiki/`, system temporary storage, or an existing approved metadata path is unsuitable.
- Whether the data is temporary, cached, derived, or persistent.
- Whether the path should be version-controlled or ignored.
- Any retention or cleanup expectation that matters to the user.
- Any related file change, such as adding an entry to `.gitignore`.

Approval applies only to the named path and related changes. Approval of one tool directory does not create a general exception for other tools or future root entries.

If a CLI such as Firecrawl defaults to repository-local output, the agent should first prefer a supported temporary or `raw/` output location. If the tool requires a root-level working directory such as `.firecrawl/`, the agent proposes that directory and its version-control treatment before running the command that creates it.

## Reusable Templates And Indexes

The initialized wiki retains `templates/` as operational scaffolding. At minimum it contains the canonical reusable templates already used by the initializer:

- `templates/index.md`
- `templates/log.md`
- `templates/wiki-page.md`

`templates/index.md` must be location-neutral. It may be adapted into the root `index.md` or a local index under `wiki/`. Examples must make clear that links are rewritten relative to the destination index rather than copied mechanically.

A local index is created only when a directory represents a distinct subject area or has enough pages that direct navigation is poor. Local indexes under `wiki/` are operational navigation files, not knowledge pages, and therefore do not use knowledge-page frontmatter. The root index links to useful local indexes.

## Version Control And Commit Authority

`docs/wiki/operations.md` continues to record the selected history mechanism, such as version control, `log.md`, or both. It no longer contains an `Automatic commits` setting.

Selecting version control as a history mechanism does not authorize an agent to run a commit. Commit timing and automation follow:

1. The user's instruction for the current task.
2. The surrounding agent system's applicable configuration or operating rules.

The wiki may still require focused history and protection of unrelated work when a commit is authorized. It must not duplicate or override host-level commit policy.

The `Record` step in the write protocol means recording through the configured mechanism when the agent has authority to do so. If version control is selected but the agent lacks commit authority, it reports the uncommitted approved changes rather than inferring permission.

## Documentation Changes

### `BOOTSTRAP.md`

- Include retained `templates/` in the target and generated structures.
- State the closed placement rule and classify persistent domain material.
- Add the root exception protocol for temporary and tool-managed data.
- Remove any implication that initialization configures automatic commits.
- Verify that no unapproved root entry was created.
- Verify that reusable templates remain available after initialization.

### `README.md`

- Show `templates/` in the initialized structure.
- State that persistent domain content belongs only under `raw/` or `wiki/`.
- Explain that new root paths require explicit approval.
- Remove `automatic commits` from the editable-settings map.

### `AGENTS.md`

- Add the placement invariant to Critical Rules.
- Require a proposal and explicit approval before creating a new persistent root path.
- Direct temporary work to system temporary storage when possible.
- Include `templates/` in the structure overview.

### `docs/wiki/operations.md`

- Remove the `Automatic commits` local setting.
- Add a structure-and-placement section containing the allowlist, classification rules, and exception protocol.
- Clarify that version-control selection does not grant commit authority.
- Add unapproved root entries to maintenance and verification concerns.

### `templates/index.md`

- Make the template explicitly reusable for root and local indexes.
- Explain relative-link adaptation for the destination path.
- Retain the threshold for creating local indexes.

No changes are required in `docs/wiki/schema.md` or `docs/wiki/writing-style.md` because placement, operational indexes, and commit authority are operational concerns rather than schema or prose-style concerns.

## Initialization Flow

1. Inspect the proposed target, including its existing root entries and repository metadata.
2. Classify requested material and directories as raw evidence, authored knowledge, temporary work, or tool-managed state.
3. Present the normal wiki proposal with the canonical root allowlist.
4. Name and justify every additional persistent root entry separately.
5. Wait for explicit approval of the wiki files and each exception.
6. Create only approved paths.
7. Verify that all created domain material is under `raw/` or `wiki/`, templates were retained, and no unapproved root entry exists.
8. Record or report the work according to the history mechanism and available commit authority.

## Failure Handling

- If requested content could plausibly be either evidence or authored knowledge, the agent proposes the placement rather than inventing a third root.
- If a tool creates an unexpected root path, the agent stops further related writes, reports the path, and asks whether it should be approved, relocated, or removed. Existing raw-file custody and deletion-approval rules still apply.
- If a non-allowlisted path already exists before initialization, the agent reports it as surrounding context and does not modify or adopt it without approval.
- If a temporary location is unavailable, the agent proposes a specific repository-local exception before creating it.
- If commit authority is unclear, the agent leaves the approved changes uncommitted and reports their state.

## Verification

Documentation review must confirm:

- The same canonical root allowlist appears consistently in the initializer and initialized operating instructions.
- `templates/` is present in both the target structure and files-to-generate instructions.
- `templates/index.md` works conceptually for both root and local destinations.
- A CRM example resolves under `raw/` and/or `wiki/`.
- Temporary and tool-managed files have an explicit decision path.
- Root exceptions require named approval.
- The phrase `Automatic commits` no longer appears as a local setting.
- Version control does not imply commit authority.
- Initialization verification detects unapproved root entries.
- Existing approval, raw ownership, schema, citation, and writing rules remain unchanged.

Because this change modifies documentation rather than executable code, verification consists of targeted searches, complete-file review, link and structure consistency checks, and inspection of the final diff.
