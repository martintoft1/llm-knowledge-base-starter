# General LLM Wiki Design

## Purpose

Build a minimal, reusable initializer for creating an LLM-maintained knowledge base in any context. A user pastes `BOOTSTRAP.md` into an agent, describes the wiki they need, reviews the proposed setup, and approves creation.

The initializer must adapt to personal, research, startup, and mixed contexts without shipping a framework of domain-specific files.

## Deliverables

```text
llm-wiki/
├── README.md
├── BOOTSTRAP.md
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

- `BOOTSTRAP.md` is the complete copy-paste initializer and authoritative operating model.
- `templates/` provides inspectable examples for users who want to understand or manually adapt the generated files.
- `README.md` explains the idea and the two-minute quick start.

There are no separate core, profile, or adapter libraries in version 1. The bootstrap generates the appropriate agent instruction file and domain-specific conventions directly from the user's answers.

## Initialization experience

The receiving agent starts with one broad question:

> What kind of knowledge base do you want to create, where should it live, and what will you use it for?

It then asks only the follow-up questions necessary to resolve material choices, one at a time. It should infer reasonable defaults and avoid turning setup into a questionnaire.

Before writing, the agent proposes:

- Purpose and scope.
- Target location and interaction with an existing repository.
- Directory and operational files.
- Useful local tags or terminology.
- Sensitive-data constraints.
- Files it will create or modify.

The agent waits for explicit approval, creates only the approved files, verifies the result, and reports what it made. It must not overwrite an existing file without separate approval.

## Generated wiki

A typical initialized wiki contains:

```text
knowledge/
├── raw/
├── wiki/
├── config.md
├── index.md
├── log.md
└── <agent instruction file>
```

The location and root name are user-defined. A wiki may live on its own or inside an existing monorepo.

### Data ownership

- `raw/` contains exact source material. Its internal organization is human-chosen. The agent may read and cite raw files but must never edit, rename, move, or delete them.
- `wiki/` contains agent-maintained Markdown. It is flat by default, with unique filenames. Optional subdirectories may be introduced later with approval, but directory placement never determines page type.
- `config.md`, `index.md`, `log.md`, and the agent instruction file are operational files rather than knowledge pages.

Every write follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

## Universal page types

Every knowledge page uses one of six values in `type`:

| Type | Purpose | Example tags |
|---|---|---|
| `source` | Describe and evaluate imported evidence | `book`, `research-paper`, `image`, `dataset`, `customer-interview` |
| `subject` | Maintain knowledge about a topic or entity | `person`, `company`, `concept`, `event`, `project` |
| `note` | Capture provisional authored thinking | `idea`, `hypothesis`, `question`, `observation` |
| `synthesis` | Combine evidence into a reasoned conclusion | `literature-review`, `comparison`, `market-analysis` |
| `decision` | Record a choice and its rationale | `product`, `strategy`, `research-direction` |
| `plan` | Describe intended action and progress | `strategy`, `roadmap`, `experiment`, `project-plan` |

New contexts customize tags rather than adding universal page types.

## Common frontmatter

Every knowledge page contains:

```yaml
---
type: source
title: Customer 12 Interview
description: Interview covering onboarding friction and purchasing criteria.
status: review
tags:
  - customer-research
  - onboarding
resource: https://example.com/canonical-resource
created: 2026-07-07T14:30:00+02:00
updated: 2026-07-07T16:10:00+02:00
---
```

- `type` is required and uses one of the six universal values.
- `title` is required for agent-created pages.
- `description` is required and contains one plain-text sentence.
- `status` is required.
- `tags` is required and may be an empty YAML list.
- `resource` is required and identifies the primary underlying asset using an absolute URL or relative path. It is `null` for abstract ideas and knowledge products that do not describe one specific asset.
- `created` and `updated` are required ISO 8601 datetimes with explicit timezone offsets.
- `created` never changes. `updated` changes only after a meaningful content or metadata change.

Allowed statuses are:

```text
fragment | draft | review | current | completed | archived
```

The normal progression is `fragment → draft → review → current`. New evidence may return a current page to draft or review.

## Tags and links

Tags provide broad, cross-cutting categorization and discovery. Relative Markdown links express specific relationships between documents.

During initialization, the agent infers relevant dimensions from the user's context and proposes a seed vocabulary of roughly 8–15 tags for approval. Useful dimensions may include business function, industry or domain, evidence or document form, topic or theme, and work mode. The approved tags and one-line meanings are stored in `config.md`.

Tags use lowercase kebab-case. The agent reuses approved tags, avoids synonyms, does not redundantly copy type or status values into tags, and proposes additions before first use. Maintenance checks for unused tags, near-duplicates, and tags that have become too broad. The seed vocabulary is intentionally extensible rather than exhaustive.

Links normally appear in explanatory prose:

```markdown
This plan implements [Adopt self-serve onboarding](adopt-self-serve-onboarding.md)
and is supported by [Onboarding friction](onboarding-friction.md).
```

Links to evidence are also relative, such as `[interview transcript](../raw/customer-12-interview/transcript.txt)`. Templates include `Connections` or a type-specific equivalent. Generic relationship lists are not duplicated in frontmatter unless structured filtering is genuinely needed.

Renames and moves require approval, inbound-link updates, and link verification.

## Citations

Externally sourced claims use numeric markers in the body and a final `## Citations` section. Sources are numbered by first appearance and numbers are reused. Multiple supporting sources use a marker such as `[1, 2]`; precise locators may be included as `[2, p. 14]`, `[3, 01:12:30]`, or `[4, rows 20–35]`.

Each entry uses `[n] [Title](target)`, where the target is an absolute URL or relative path. Prefer the closest preserved evidence. `resource` identifies the primary underlying asset at page level, citations express claim-level provenance and additional evidence, and ordinary relative links express semantic relationships. Pages without externally sourced claims omit the section. Missing citation details must never be invented.

## Body templates

Templates are structured but elastic. They contain useful default headings and removable HTML-comment guidance. Optional empty sections are removed before a page reaches `review`, `current`, or `completed`. When present, `## Citations` is always the final section.

- `source`: summary, key claims or observations, evidence, limitations, connections.
- `subject`: overview, current understanding, attributes, relationships, evidence, open questions.
- `note`: idea or observation, why it matters, evidence and assumptions, open questions, connections.
- `synthesis`: question, conclusion, reasoning, supporting and conflicting evidence, confidence, limitations, gaps.
- `decision`: decision, context, alternatives, rationale, consequences, review or reversal conditions.
- `plan`: outcome, context, approach, milestones, risks, success criteria, progress, related decisions and evidence.

## Operations

### Ingest

Inspect new raw material, identify affected pages, propose additions and updates, wait for approval, apply approved changes, verify metadata and links, update the index, and append to the log.

### Query and filing

Read `config.md` and `index.md`, inspect relevant wiki pages, and consult raw evidence when needed. Distinguish evidence, inference, uncertainty, and conflict. A useful answer may be proposed as a note, synthesis, decision, or plan, but is never filed automatically.

### Maintenance

Check missing or invalid metadata, broken links, orphans, stale descriptions, unsupported claims, conflicts, duplicates, and lifecycle status. Propose a maintenance batch before changing files.

### Safety

- Preserve conflicting evidence rather than silently selecting a side.
- Label unsupported claims rather than inventing provenance.
- Refuse raw-file modification and offer a derived alternative.
- Do not write when approval is ambiguous.
- Prefer archival or redirects over destructive wiki deletion.
- Apply user-defined sensitive-data constraints to reading, quoting, linking, and generated content.

## Validation approach

Version 1 is validated by using the completed `BOOTSTRAP.md` to initialize one realistic startup knowledge base in a temporary directory. The trial request is:

> Create a knowledge base for my startup inside an existing software monorepo. It should hold customer interviews, product ideas, strategic analyses, decisions, and plans without mixing generated knowledge into the application code.

The trial passes when the agent proposes a minimal placement, waits for approval, creates a self-contained wiki, uses the universal schema with startup-specific tags, preserves raw ownership, and does not depend on this starter repository.

## Version 1 boundaries

Version 1 contains no application, CLI, schema validator, embedding database, automated index generator, background ingestion, domain-profile library, or exhaustive scenario suite. We will refine the initializer after using it on real wikis.
