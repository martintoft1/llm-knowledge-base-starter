# General LLM Wiki Design

## Purpose

Build a reusable, file-based starter kit for creating persistent knowledge bases maintained by an LLM. The kit must work across personal, research, startup, and mixed contexts without requiring an application, database, embedding service, or specific agent.

The deliverable has two complementary forms:

1. A self-contained `BOOTSTRAP.md` that can be pasted into a blank agent context.
2. A modular reference kit containing canonical rules, profiles, adapters, and templates.

The bootstrap process creates a tailored, self-contained wiki only after the user approves the proposed structure and configuration.

## Design principles

- Raw evidence is immutable and human-owned.
- The wiki is an evolving interpretation layer maintained by the agent.
- Evidence, inference, uncertainty, decisions, and plans remain distinguishable.
- Knowledge should compound in durable files rather than disappear into chat history.
- The agent proposes every write operation and waits for explicit approval.
- The core remains tool-neutral and domain-neutral.
- Profiles extend the core without duplicating or replacing it.
- Templates provide consistency without forcing irrelevant empty sections.
- The generated wiki must operate independently of the starter-kit repository.

## Starter-kit architecture

```text
llm-wiki/
├── README.md
├── BOOTSTRAP.md
├── core/
│   ├── principles.md
│   ├── structure.md
│   ├── workflows.md
│   ├── conventions.md
│   └── safety.md
├── profiles/
│   ├── personal.md
│   ├── research.md
│   └── startup.md
├── adapters/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   └── generic.md
└── templates/
    ├── config.md
    ├── index.md
    ├── log.md
    └── page-types/
        ├── source.md
        ├── subject.md
        ├── note.md
        ├── synthesis.md
        ├── decision.md
        └── plan.md
```

### Bootstrap

`BOOTSTRAP.md` is the portable entry point. It contains enough of the pattern to work when none of the other starter-kit files are available. It guides an agent through discovery, proposes a tailored system, waits for approval, and then creates the wiki.

The modular files remain the canonical, maintainable source material used to develop and improve the bootstrap instructions. An instantiated wiki does not depend on them.

### Core

The `core/` directory defines behavior shared by every wiki:

- `principles.md`: evidence, provenance, uncertainty, and durable knowledge.
- `structure.md`: ownership boundaries and directory responsibilities.
- `workflows.md`: bootstrap, ingest, query, filing, maintenance, and restructuring.
- `conventions.md`: filenames, links, metadata, citations, indexing, and logging.
- `safety.md`: approval boundaries, raw-source protection, deletion, sensitive data, and unsupported claims.

### Profiles

Profiles customize vocabulary, suggested subtypes, optional metadata, and optional body sections. They never introduce a competing information model. Profiles can be combined, and local configuration overrides their suggestions.

Version 1 includes personal, research, and startup profiles.

### Adapters

Adapters provide conventional entry files for Codex-compatible agents, Claude Code, and agents without a recognized instruction filename. They point to the instantiated wiki's canonical configuration and operating instructions rather than duplicating the full rules.

### Templates

Templates define the initial shape of configuration, index, log, and knowledge pages. They use a required core plus optional sections and removable HTML comments containing writing guidance.

## Instantiated-wiki architecture

```text
wiki-root/
├── raw/
│   ├── documents/
│   ├── media/
│   ├── data/
│   └── transcripts/
├── wiki/
│   ├── sources/
│   ├── subjects/
│   ├── notes/
│   ├── syntheses/
│   ├── decisions/
│   └── plans/
├── config.md
├── index.md
├── log.md
└── <agent-adapter>
```

`raw/` contains exact source material in its original useful format. The agent may inspect and cite raw files but must never edit, rename, move, or delete them.

`wiki/` contains agent-generated Markdown and may change as understanding evolves. All changes require prior user approval.

`config.md`, `index.md`, `log.md`, and the chosen adapter are operational files. They are not knowledge page types.

## Universal page types

Every knowledge page under `wiki/` uses one of six types. File format and domain-specific vocabulary are represented separately as subtypes.

| Type | Purpose | Example subtypes |
|---|---|---|
| `source` | Describes and evaluates imported evidence | `book`, `research-paper`, `image`, `dataset`, `customer-interview` |
| `subject` | Maintains knowledge about an identifiable topic or entity | `person`, `company`, `customer`, `concept`, `event`, `project` |
| `note` | Captures provisional authored thinking | `idea`, `hypothesis`, `question`, `observation` |
| `synthesis` | Combines evidence into a reasoned conclusion | `literature-review`, `comparison`, `market-analysis` |
| `decision` | Records an approved choice and its rationale | `product`, `strategy`, `research-direction` |
| `plan` | Describes intended action and progress | `strategy`, `roadmap`, `experiment`, `project-plan` |

Claims and quotes remain content within pages rather than separate page types. Attachments remain in `raw/`. Tags, statuses, indexes, logs, and configuration are not page types.

### Source pages as the bridge

A source page links evolving interpretation to immutable evidence. It summarizes the source, records important claims and limitations, and connects it to affected subjects, syntheses, decisions, and plans. It does not replace the original.

Example relationship:

```text
raw/transcripts/customer-12.txt
              ↓
wiki/sources/customer-12-interview.md
              ↓
wiki/subjects/customer-12.md
wiki/syntheses/onboarding-friction.md
wiki/decisions/simplify-onboarding.md
wiki/plans/onboarding-redesign.md
```

## Common frontmatter

Every knowledge page must contain:

```yaml
---
type: source
subtype: customer-interview
title: Customer 12 Interview
description: Interview covering onboarding friction and purchasing criteria.
status: review
tags:
  - customer-research
  - onboarding
resource: https://example.com/canonical-resource
raw:
  - ../../raw/transcripts/customer-12.txt
created: 2026-07-07T14:30:00+02:00
updated: 2026-07-07T16:10:00+02:00
---
```

### Common-field rules

- `type` is required and must be one of the six universal types.
- `subtype` is optional and contains a profile-defined or locally defined specialization such as `research-paper` or `customer-interview`.
- `title` is required for agent-created pages. Consumers may derive it from the filename when processing imported or legacy pages.
- `description` is required and contains one plain-text sentence suitable for indexes, search snippets, and previews.
- `status` is required and uses the controlled lifecycle below.
- `tags` is required and is a YAML list of short strings. Use `tags: []` when there are none.
- `resource` is optional and contains the canonical URI for an external or identifiable resource. Abstract subjects generally omit it.
- `raw` is optional and is always a YAML list of relative paths to locally preserved evidence.
- `created` is required, uses an ISO 8601 datetime with timezone, and never changes after creation.
- `updated` is required, uses an ISO 8601 datetime with timezone, and changes only after a meaningful content or metadata change. Formatting-only edits and link repair do not advance it.

### Status lifecycle

Allowed values are:

```text
fragment | draft | review | current | completed | archived
```

- `fragment`: captured but not sufficiently developed.
- `draft`: coherent but incomplete.
- `review`: awaiting human approval.
- `current`: approved and presently authoritative.
- `completed`: a fixed record whose intended work or process has concluded.
- `archived`: retained but no longer active or authoritative.

The normal progression is `fragment → draft → review → current`. Pages may move from `current` to `completed` or `archived` when appropriate. New evidence may return a page from `current` to `draft` or `review`.

### Type-specific metadata

Templates may add fields that enable navigation, filtering, provenance, or maintenance. Examples include `author` and `published` for sources; `decided`, `supersedes`, and `superseded_by` for decisions; `start`, `due`, and `owner` for plans; and `question` and `confidence` for syntheses.

Information used only for reading belongs in the body rather than frontmatter.

## Body-template contract

Body templates are structured but elastic:

- Each type has a small set of expected structural concerns.
- Optional sections appear only when they add value.
- HTML comments provide removable prompts, examples, and writing guidance.
- Pages promoted to `review`, `current`, or `completed` must not retain irrelevant empty headings.
- Agents may add sections when the material requires them.
- Profiles may extend templates but must preserve each type's core meaning.

### Source

Expected concerns: provenance, summary, key claims or observations, limitations, and connections.

### Subject

Expected concerns: overview, current understanding, relevant attributes, relationships, evidence, and open questions.

### Note

Expected concerns: idea or observation, why it matters, evidence and assumptions, open questions, and connections.

### Synthesis

Expected concerns: question, conclusion, reasoning, supporting evidence, conflicting evidence, confidence, limitations, and knowledge gaps.

### Decision

Expected concerns: decision, status or effective date, context, alternatives, rationale, consequences, and review or reversal conditions.

### Plan

Expected concerns: intended outcome, context, approach, milestones, risks and dependencies, success criteria, progress, and related decisions or evidence.

## Operating workflows

Every write operation follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

### Ingest

1. Inspect new material in `raw/`.
2. Identify its relevance, subtype, and affected wiki pages.
3. Propose new pages, updates, connections, and contradictions.
4. Wait for explicit approval.
5. Apply only the approved changes.
6. Verify metadata, links, raw references, citations, and index coverage.
7. Append a structured entry to `log.md`.

### Query and synthesis

The agent reads `config.md` and `index.md`, searches relevant wiki pages, and follows citations into raw evidence when necessary. Answers distinguish evidence, inference, uncertainty, and unresolved conflict.

The agent may propose filing a useful answer as a note, synthesis, decision, or plan. It never files an answer automatically.

### Maintenance

A lint pass checks for:

- Missing or invalid frontmatter.
- Broken raw references and wiki links.
- Orphan pages.
- Stale descriptions and index entries.
- Unsupported claims.
- Conflicting conclusions.
- Duplicate subjects.
- Pages stuck in `fragment`, `draft`, or `review`.
- Completed or superseded material that should be archived.

The agent presents a proposed maintenance batch and waits for approval before applying it.

### Restructuring

Renames, moves, merges, splits, archival, and deletion require explicit approval. Raw files are never modified. Wiki deletion should normally use archival or a small redirect-style page so existing links and history remain intelligible.

## Bootstrap flow

The bootstrap agent asks one setup question at a time and establishes:

1. The wiki's purpose.
2. Applicable profiles.
3. Included and excluded scope.
4. Useful terminology and subtypes.
5. Sensitive-data constraints.
6. The raw-material intake location.
7. The required agent adapter.

It then proposes the complete structure, configuration, selected conventions, and initial templates. It must receive explicit approval before creating files. The generated wiki must contain all instructions needed for future operation without retaining `BOOTSTRAP.md` or accessing the starter-kit repository.

## Error and safety behavior

- When evidence conflicts, preserve both positions, identify the conflict, and request guidance rather than silently selecting one.
- When provenance is missing, label the claim unsupported or uncertain rather than inventing a citation.
- When a requested action would modify raw material, refuse that part and propose a non-destructive alternative.
- When approval is ambiguous, do not write.
- When a page does not fit the current taxonomy, propose a subtype or template extension before adding a universal type.
- When sensitive-data rules are configured, treat them as constraints on reading, quoting, linking, and generated content.
- When a change supersedes approved knowledge, retain an intelligible trail through status, links, decision records, or log entries.

## Acceptance criteria

Version 1 is complete when:

- `BOOTSTRAP.md` works when pasted into a blank agent context with no companion files.
- The bootstrap asks questions one at a time and waits for approval before creating files.
- The generated wiki is self-contained, file-based, and tool-neutral.
- Raw files remain untouched.
- Every knowledge page uses a universal type and valid common frontmatter.
- Body templates implement the required-core, optional-module, removable-guidance model.
- Evidence-based wiki content can be traced to raw evidence where applicable.
- All writes follow `Inspect → Propose → Approve → Apply → Verify → Log`.
- Codex, Claude Code, and generic adapters produce materially consistent behavior.

Verification scenarios cover:

1. Bootstrapping an empty personal wiki.
2. Bootstrapping a combined research and startup wiki.
3. Ingesting a paper with a PDF and dataset.
4. Ingesting a customer interview with transcript and audio.
5. Filing an exploratory answer as a synthesis.
6. Recording a decision and connected plan.
7. Detecting conflicting sources during maintenance.
8. Refusing unapproved changes and attempted raw-file edits.

## Version 1 boundaries

Version 1 does not include a CLI, application, schema validator, embedding database, automated index generator, or background ingestion. Basic filesystem operations and text search are sufficient. Optional tooling may be added later without changing the core information model.
