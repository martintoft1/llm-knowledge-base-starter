# OKF v0.2 LLM Wiki Design

## Status

Approved in conversation on 2026-08-18. This document defines the intended redesign before implementation.

## Purpose

Turn this repository into a reusable initializer for an OKF v0.2 knowledge bundle that follows Karpathy's LLM Wiki pattern and retains only deliberate local additions.

The result should remain file-based, agent-neutral, understandable to non-technical users, and useful for personal, study, research, and business knowledge bases.

## Sources Of Authority

The implemented repository will use this order of authority:

1. A pinned, unmodified copy of the upstream OKF v0.2 `SPEC.md` defines OKF terminology and semantics.
2. `references/schema.md` defines this project's stricter OKF profile and permitted local extensions.
3. `references/operations.md` defines how agents apply the format, autonomy boundaries, history, and validation.
4. `references/writing-style.md` defines local editorial guidance.
5. `AGENTS.md` and optional agent adapters provide a short entry point and required reading order.

Local documents may point to exact SPEC sections but should repeat them only when an agent needs a short instruction at the point of action. Local rules must not redefine reserved OKF fields incompatibly.

## Goals

- Make `wiki/` conformant with OKF v0.2 sections 1 through 11.
- Implement Karpathy's raw, wiki, and schema layers and the ingest, query, lint, index, and log workflows.
- Make all durable or potentially useful knowledge accumulate in the wiki rather than disappear into chat.
- Use progressive autonomy for ordinary wiki maintenance while protecting sources, structure, permissions, and sensitive operations.
- Preserve the exact pinned OKF specification locally and make future migrations deliberate.
- Keep initialization contextual and simple for non-technical users.
- Represent external databases safely without implementing connectors or storing credentials.
- Retain only local principles that are absent from OKF and Karpathy.

## Non-Goals

- Executable database connectors.
- A required SDK, application, service, or runtime.
- Background automation or scheduled maintenance.
- Credential or secret storage.
- A fixed word limit.
- A second summary that competes with the vendored OKF specification.
- Automatic migration to future OKF versions.
- Replacing raw files with Markdown conversions.

## Repository Architecture

```text
<knowledge-base>/
├── raw/                    # Immutable original sources in native formats
├── wiki/                   # OKF v0.2 bundle
│   ├── index.md            # Reserved OKF index and version declaration
│   ├── log.md              # Reserved OKF update history
│   └── *.md                # OKF concept documents
├── README.md
├── AGENTS.md
├── CLAUDE.md               # Optional adapter
├── references/             # Pinned standard and local operating rules
├── templates/              # Reusable concept and body templates
└── .git/                   # Present only when Git is selected
```

Only `wiki/` is the OKF bundle. Every knowledge concept in it is UTF-8 Markdown. `raw/` retains PDFs, images, spreadsheets, datasets, source exports, and other evidence in useful native formats.

Existing raw files are immutable to agents. An agent may add a new approved raw source but never modify, overwrite, rename, move, or delete an existing one. A correction becomes a new source. A human may manage raw material directly outside the agent workflow.

Operating instructions and templates remain outside the OKF bundle. New root paths require an explicit proposal and approval.

## Vendored OKF Specification

Store the exact upstream specification as:

```text
references/okf/v0.2/SPEC.md
references/okf/v0.2/UPSTREAM.md
```

`SPEC.md` must be byte-for-byte identical to the file retrieved from a pinned upstream commit. `UPSTREAM.md` records:

- Original repository and file URL.
- Exact upstream commit SHA.
- Retrieval date.
- SHA-256 checksum of `SPEC.md`.
- Upstream license and attribution.
- Whether a newer version was known at retrieval time.

A new OKF version is stored in a new version directory. It does not overwrite v0.2. Migration requires review of upstream changes, a conscious adoption decision, local-profile and template updates, concept migration, full validation, and an `okf_version` update in `wiki/index.md`. Old specifications remain available.

## OKF v0.2 Implementation

### Sections 1 And 2: Principles And Terminology

The README and local rules use the OKF terms bundle, concept, concept ID, source, provenance, actor, trust tier, Attested Computation, executor, receipt, and attester consistently.

The system treats knowledge as readable, parseable, diffable, portable, and continuously maintained. OKF remains a format rather than a runtime or platform.

### Section 3: Bundle Structure

`wiki/` is the bundle. `index.md` and `log.md` are reserved at every level and cannot be concept documents. Subdirectories are allowed but are introduced only when navigation has become difficult while flat.

### Section 4: Concept Documents

Every non-reserved Markdown file under `wiki/` contains parseable YAML frontmatter followed by a Markdown body. The local profile requires:

```yaml
---
type: Note
title: Example note
status: draft
tags: []
generated:
  by: llm-wiki/<agent-version>
  at: <ISO 8601 datetime>
---
```

Local rules:

- `type`, `title`, `status`, `tags`, and `generated` are required locally.
- `description` may be omitted for an early draft and is required before a concept becomes `stable`.
- `resource`, `sources`, `usage_window`, `verified`, and `stale_after` appear only when relevant.
- Absent optional fields are omitted rather than filled with `null`.
- Unknown producer extensions are preserved.
- Reserved fields retain their OKF meanings.
- The body uses `# Schema`, `# Examples`, and `# Computation` when applicable.
- Body sections otherwise remain flexible.

The local type profile includes `Note`, `Reference`, `Source`, `Analysis`, `Decision`, `Goal`, `Plan`, `Dataset`, and `Database`. `Attested Computation` uses the exact OKF type name. Unknown types remain consumable.

### Section 5: Provenance, Trust, And Lifecycle

Implement `sources`, `usage_window`, `generated`, `verified`, `status`, and `stale_after` according to the pinned specification.

`sources` records concept-level provenance. When a specific claim needs attribution, its Markdown footnote label matches a `sources[].id`. Source entries use `resource` and may include `id`, `title`, `author`, `usage_count`, and `last_modified`. Credibility is inferred from objective signals and is never stored as a score.

`generated` records who or what produced the current content and when it last changed meaningfully. `verified` records independent checks. Status uses only `draft`, `stable`, or `deprecated`; absent status is not used locally because the local profile requires it. `stale_after` is an optional absolute date.

### Sections 6 And 7: Links, Paths, And Actors

Concept relationships use standard Markdown links. Bundle-absolute paths beginning with `/` are preferred. Relative paths and absolute URLs remain valid. Relationship meaning is stated in surrounding prose. Broken links are reported but tolerated as OKF requires.

Path-valued fields accept absolute URLs, bundle-absolute paths, or relative paths. A `references/` subdirectory inside the bundle may be used when a concept needs to point to mirrored material, instructions, or code, but it is not required.

Actors use:

- `<producer>/<version>` for agents and tools.
- `human:<id>` for people.
- `process:<id>` for automated processes.

The bootstrap may use stable local identifiers such as `human:owner` when a more specific identifier is unnecessary.

### Section 8: Index Files

The bundle-root `wiki/index.md` may contain only this frontmatter:

```yaml
---
okf_version: "0.2"
---
```

Its body groups concepts under useful headings. Each entry is a Markdown link with the concept description when available. The agent updates the index during ingest, durable query filing, and relevant maintenance. Local indexes are created only when a subdirectory benefits from progressive disclosure.

### Section 9: Log Files

`wiki/log.md` is mandatory. It has no frontmatter and groups entries newest-first under `YYYY-MM-DD` headings. Entries briefly record meaningful ingests, filed queries, maintenance, and concept changes. The log explains history but does not provide rollback.

### Section 10: Attested Computation

Add a dedicated template and operating rules. A locally stable Attested Computation requires:

- `runtime`.
- Typed `parameters`.
- An inline `# Computation` block or a `computation` path.
- An `executor` resource and declared receipt fields.
- A deterministic, non-LLM `attester` resource.
- Relevant provenance and trust fields.
- `stale_after` when the definition can expire.

The agent may provide values for declared parameters but must not author or alter the sanctioned computation during execution. Failed attestation blocks the result. A stale computation triggers a warning or refusal appropriate to risk. Document verification and per-run attestation remain distinct.

This repository does not implement executors or attesters. It may describe a contract whose resources live externally, but it must not claim that a computation is attestable unless those resources exist.

### Section 11: Conformance

After initialization and before finalizing any wiki operation, validate the complete bundle:

1. Every non-reserved `.md` file has parseable YAML frontmatter.
2. Every concept has a non-empty `type`.
3. Reserved indexes and logs follow sections 8 and 9.
4. Every optional OKF field that appears follows its specified structure.
5. Actor identifiers follow section 7.
6. Claim footnotes resolve to matching `sources[].id` entries.
7. Locally stable Attested Computation concepts contain the complete local contract.
8. Unknown fields and types are preserved.
9. Broken links are reported without failing OKF conformance.
10. Failed checks block automatic commit and are reported.

Consumers must not reject a concept merely for missing optional OKF families, unknown types or fields, broken links, or missing indexes.

## Data Concepts And External Systems

A small static dataset may be stored as a `Dataset` concept with `# Schema`, `# Data`, and `# Examples` sections. The one-concept rule still applies, but there is no numeric word limit.

A large or live database is represented by a `Database` or `Dataset` concept. Its `resource` points to a canonical, non-secret identifier. Its body may describe schema, examples, access, and limitations. Credentials and live data are never stored in frontmatter.

The bootstrap asks about external systems only when purpose or expected sources make them relevant, such as business, organizational, research-data, analytics, or operational knowledge. It normally skips the question for personal notes, ordinary studying, and reading unless the user mentions such systems.

The bootstrap records which systems matter and which existing agent tools have read access. It does not install integrations or ask the user to paste credentials.

## Karpathy Workflows

### Ingest

When the user adds or identifies a source, the agent:

1. Reads it and checks relevance, provenance, conflicts, and sensitivity.
2. Creates or updates relevant wiki concepts.
3. Populates `sources` and adds keyed footnotes when individual claims require attribution.
4. Updates related concepts, summaries, and cross-links.
5. Updates `wiki/index.md` and `wiki/log.md`.
6. Runs full conformance and local-profile checks.
7. Creates a focused local commit when Git is enabled and host rules permit it.
8. Reports the concepts changed and history reference.

One-source-at-a-time ingest is preferred when practical so the user can guide emphasis without manually maintaining the wiki.

### Query And Accumulation

The agent reads the index, follows relevant concepts and sources, and answers from traceable evidence.

All durable or potentially useful knowledge must be filed into the wiki. The agent updates an existing concept when the knowledge belongs there and creates a new concept only when it represents a distinct unit. Related concepts are updated when the new knowledge changes, supports, or contradicts them.

Generic Q&A pages and chat-transcript archives are not created. Minor, procedural, temporary, or disposable responses remain in chat.

### Maintenance

Maintenance checks:

- Contradictions and unsupported claims.
- Stale or deprecated knowledge.
- Broken and missing links.
- Orphan concepts.
- Missing provenance.
- Duplicate or overlapping concepts.
- Important topics without concepts.
- Invalid OKF metadata.
- Stale computations and failed attestations.
- Type drift.
- Whether tags should be added, removed, merged, narrowed, or retired.
- Whether the local tag registry and affected concepts agree.

Clear, low-risk corrections may be applied automatically. Higher-risk changes are proposed first.

## Progressive Autonomy

The agent may autonomously:

- Create and update normal concepts under `wiki/`.
- Add links, sources, metadata, and claim attribution.
- Update indexes and logs.
- Apply clear formatting and conformance corrections.
- Perform low-risk maintenance.
- Create focused local commits when Git is enabled and host rules permit.

Approval is required for:

- Adding a new raw source on the user's behalf.
- Deleting concepts.
- Broad merges, splits, moves, renames, or reorganizations.
- Changing the pinned OKF version.
- Changing schema, operating rules, templates, or autonomy settings.
- Connecting to a new external system or increasing access.
- Writing to external systems.
- Sensitive, ambiguous, or unusually broad operations.

Agents never modify existing raw sources.

## History Modes

`wiki/log.md` is mandatory. Git is strongly recommended, not required.

During initialization, the bootstrap explains that Git provides diffs, attribution, and rollback while the log only records what happened. It offers Git when available without requiring technical knowledge from the user.

When Git is enabled, the agent checks the worktree, preserves unrelated changes, stages only its operation, and creates one focused local commit when host rules permit. It never pushes, rewrites history, or performs destructive rollback without authority.

When Git is unavailable or declined, the wiki remains usable with its log. The agent warns that rollback is unavailable and requires approval for substantive replacement of existing content and for all structural or destructive changes.

## Bootstrap Flow

The bootstrap starts with purpose and asks one follow-up question at a time only when the answer changes files, behavior, or safety. It discovers:

- Purpose, scope, exclusions, and terminology.
- Sensitive-data constraints.
- Preferred writing style when relevant.
- Agent and human actor identifiers.
- History mode.
- Likely raw sources.
- Relevant external systems.
- Optional agent adapters.

Before writing, it proposes target, settings, exact files, existing-file changes, raw handling, external-resource concepts, Git behavior, and important assumptions. Approval covers only that proposal.

After approval, it creates `raw/` and `wiki/`, copies the pinned specification and local operating documents, creates conformant index and log files, creates only justified initial concepts, initializes Git if selected, validates everything, records initialization, and reports how to add the first source or query.

`BOOTSTRAP.md` is not copied into the initialized knowledge base.

## Deliberate Local Additions

The following principles are absent as complete requirements from both OKF v0.2 and Karpathy's primary post and gist:

1. **Progressive structure:** Capture with the least structure needed, then add types, tags, headings, and folders only when they improve retrieval or reuse.
2. **Simplicity-first writing:** Use plain language and only as much structure as the material requires. One concept per document is inherited from OKF, not claimed as local.
3. **Flat organization and living tags:** Prefer links and a maintained tag registry over premature folders.
4. **Progressive autonomy:** Automate ordinary wiki maintenance while reserving high-risk actions for human control.
5. **A complete tailored starter kit:** Package purpose discovery, the local OKF profile, concept types, writing rules, safety rules, workflows, and optional templates.
6. **Stricter epistemic safeguards:** Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict; never invent provenance.
7. **Additional repository governance:** Use a closed root model, sensitive-data settings, controlled structural exceptions, and conditional external-system discovery.

The following are inherited and must not be presented as local additions: one concept per document, raw/wiki separation, LLM wiki ownership, agent and tool neutrality, contradiction checks, Markdown, YAML frontmatter, provenance, links, indexes, logs, and Git compatibility.

## Legacy Migration Decisions

- Replace eight fixed frontmatter keys with the OKF v0.2 local profile.
- Replace `created` and `updated` with `generated.at` and optional Git history.
- Replace six custom status values with `draft`, `stable`, and `deprecated`.
- Replace body `## Citations` lists with `sources` and keyed footnotes.
- Move root index and log behavior into reserved files under `wiki/`.
- Remove numeric word guidance and retain qualitative simplicity plus one concept per document.
- Replace proposal-only maintenance with automatic low-risk maintenance and guarded high-risk actions.
- Replace mandatory Git with mandatory log and strongly recommended Git.
- Replace local summaries of OKF semantics with the exact vendored specification and a small local profile.

Before implementation, classify every current rule as upstream, retained local behavior, adapted legacy behavior, removal, or unresolved. Rewrite around the pinned specification and Karpathy workflow, then reapply only approved local additions. Preserve unrelated and uncommitted work.

## Failure Handling

- Invalid YAML, missing type, or malformed optional fields block completion.
- Missing provenance leaves the concept unverified or draft and is reported.
- Conflicting sources are preserved and identified.
- Broken links are reported without failing OKF conformance.
- Failed attestation blocks the value and surfaces the failure.
- Stale computations warn or refuse according to risk.
- Unavailable external systems are recorded as limitations; access is never pretended.
- Without Git, rollback limitations and stricter approvals are explicit.
- Dirty Git worktrees preserve unrelated changes and stage only in-scope files.
- New OKF releases are reported but never adopted automatically.

## Verification Scenarios

1. Initialize a personal wiki without irrelevant database questions.
2. Initialize a business or research wiki with an external database reference and no credentials.
3. Create a minimal conformant concept.
4. Create a concept using supported provenance, trust, lifecycle, and actor fields.
5. Attribute claims through `sources[].id` footnotes.
6. Create conformant index and log files.
7. Store durable query results in existing or new distinct concepts.
8. Run maintenance covering links, provenance, contradictions, types, tags, and the tag registry.
9. Create a valid Attested Computation contract.
10. Reject failed or stale attestation.
11. Preserve unknown types and extensions.
12. Report broken links without failing conformance.
13. Operate correctly in Git-and-log and log-only modes.
14. Refuse agent modification of existing raw sources.
15. Confirm that an initialized wiki works without `BOOTSTRAP.md`.

## Planned Repository Changes

Update:

- `README.md`
- `BOOTSTRAP.md`
- `AGENTS.md`
- `CLAUDE.md`
- `references/schema.md`
- `references/operations.md`
- `references/writing-style.md`
- Existing page, index, log, and body templates

Add:

- `references/okf/v0.2/SPEC.md`
- `references/okf/v0.2/UPSTREAM.md`
- Body templates for `Dataset`, `Database`, and `Attested Computation`
- Only the smallest local conformance reference needed to apply the pinned standard

Do not add connectors, credentials, a required runtime, a background service, a fixed word limit, or a competing OKF summary.

## Acceptance Criteria

- The vendored specification is exact, pinned, attributed, and checksummed.
- `wiki/` produced by the bootstrap conforms to OKF v0.2 sections 1 through 11.
- All optional OKF families used by the local profile follow their upstream structure.
- Karpathy's ingest, query, lint, index, and log pattern is implemented.
- Durable useful knowledge is filed without creating generic Q&A pages.
- Progressive autonomy and both history modes behave as specified.
- Existing raw sources remain immutable to agents.
- Conditional external discovery works without secrets or connectors.
- Local additions are documented without claiming upstream ideas as original.
- Legacy rules named for replacement no longer conflict with the new profile.
- All verification scenarios pass through documentation review and targeted validation.
