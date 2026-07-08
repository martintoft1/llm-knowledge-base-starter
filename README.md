# LLM Wiki

A small, portable pattern for knowledge bases that compound over time. Raw material is preserved under human control; an LLM maintains a linked Markdown wiki that integrates what the sources mean.

## Quick start

1. Open [`BOOTSTRAP.md`](BOOTSTRAP.md).
2. Copy its complete contents into an LLM agent with filesystem access.
3. Describe the knowledge base you want, where it should live, and what it is for.
4. Review the proposed files and approve only when the setup looks right.

The initializer asks only the follow-up questions it needs. It can create a standalone wiki or place one inside an existing repository.

## What gets created

A typical result is deliberately small:

```text
knowledge/
├── raw/                 # Human-owned source material
├── wiki/                # LLM-maintained Markdown
├── config.md            # Local operating contract
├── index.md             # Content-oriented navigation
├── log.md               # Append-only change history
└── AGENTS.md            # Or another agent instruction file
```

Neither `raw/` nor `wiki/` requires subdirectories. Humans may organize raw files however provenance is clearest. Wiki files are flat by default; their frontmatter—not their folder—states what they are.

## Knowledge pages

Every file under `wiki/` has two parts:

1. YAML frontmatter containing consistent machine-readable metadata.
2. A Markdown body containing the actual knowledge, contextual links, and—when needed—a final citations section.

The frontmatter describes the page. The body explains the subject. Links express relationships, while citations establish claim-level provenance.

## Frontmatter

Every knowledge page keeps the same eight keys, even when `resource` is empty:

The block below is a schema illustration, not copy-ready YAML. Every value inside angle brackets is a placeholder that the agent must replace from the actual page context. The listed choices are allowed values, not defaults or recommendations.

```yaml
---
type: <source | subject | note | synthesis | decision | plan>
title: <human-readable display name>
description: <one-sentence summary>
status: <fragment | draft | review | current | completed | archived>
tags: [<zero or more approved tags>]
resource: <absolute URL | relative path | null>
created: <ISO 8601 datetime with timezone>
updated: <ISO 8601 datetime with timezone>
---
```

### `type`

Choose the type that matches the page's purpose:

- `source`: one imported piece of evidence
- `subject`: an enduring topic or entity
- `note`: a provisional idea, question, or observation
- `synthesis`: a reasoned conclusion across evidence
- `decision`: a choice and its rationale
- `plan`: intended action and progress

No type is preferred by default. Local vocabulary belongs in tags rather than additional types.

### `title` and `description`

`title` is the human-readable display name. `description` is one plain-text sentence suitable for indexes, previews, and search results.

### `status`

- `fragment`: captured but not sufficiently developed
- `draft`: coherent but incomplete
- `review`: awaiting human approval
- `current`: approved and presently authoritative
- `completed`: a fixed record or plan whose intended process has concluded
- `archived`: retained but no longer active or authoritative

No status is a universal default. Choose it from the page's actual lifecycle state.

### `tags`

Tags are short lowercase kebab-case strings. The initializer proposes a small vocabulary based on the wiki's context rather than inventing tags page by page.

Tag suggestions may cover several dimensions:

- Business function: `operations`, `admin`, `technology`, `marketing`, `sales`, `finance`
- Industry or domain: `circular-economy`, `climate`, `health`, `agriculture`
- Evidence or document form: `customer-interview`, `research-paper`, `dataset`, `meeting`
- Topic or theme: `pricing`, `onboarding`, `retention`, `supply-chain`
- Work mode: `hypothesis`, `experiment`, `analysis`

These are examples, not a universal taxonomy. Each initialized wiki records its approved vocabulary and meanings in `config.md`.

### `resource`

`resource` identifies the primary underlying asset described by the page. It may be an absolute URL or a relative path such as `../raw/customer-orders.csv`. Use `null` for abstract ideas and knowledge products—such as a synthesis, business plan, strategy, or decision—that do not describe one specific asset. Additional supporting material belongs in claim-level citations.

### `created` and `updated`

Both use ISO 8601 datetimes with explicit timezone offsets. `created` never changes. Update `updated` only after a meaningful content or metadata change, not for formatting or link repair alone.

## Links

Relative Markdown links connect a page to a specific source, subject, synthesis, decision, or plan and explain that relationship in context.

For example:

```markdown
This plan implements [Adopt self-serve onboarding](adopt-self-serve-onboarding.md)
and is supported by [Onboarding friction](onboarding-friction.md).
```

Links to raw evidence are also relative, for example `[interview transcript](../raw/customer-12/transcript.txt)`. The wiki uses standard Markdown links rather than tool-specific wiki-link syntax.

## Citations

When a page makes claims sourced from external material, place numeric markers directly after those claims and list the sources under `## Citations` at the bottom of the page:

```markdown
The market grew by 18% during 2025 [1].

## Citations

[1] [Market report](https://example.com/market-report)
[2] [Internal data-quality runbook](../raw/data-quality-runbook.pdf)
```

Number sources by first appearance, reuse the same number when citing a source again, and use `[1, 2]` when several sources support one claim. Add a locator when useful, such as `[2, p. 14]`, `[3, 01:12:30]`, or `[4, rows 20–35]`. Citation targets may be absolute URLs or relative paths.

Citations provide claim-level provenance and can reference raw files. Omit the citations section when no externally sourced claims appear, and never invent missing citation details.

## Operating model

The human owns sources, scope, and approval. The agent performs the bookkeeping: summarizing, connecting, updating, checking contradictions, and maintaining navigation.

Every write follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

Agents may propose and, after normal approval, add new files to `raw/`. Once a raw file exists, modifying, overwriting, renaming, moving, or deleting it requires separate, explicit human approval naming the file and operation. When possible, preserve the original and add a derived or corrected version as a new file.

## Repository contents

The distributable consists of two documents:

- `README.md`: this human-facing explanation.
- `BOOTSTRAP.md`: the complete, authoritative initializer, including every generated-file and page-body template the receiving agent needs.

No companion template or design files are required.

## Version 1

This version is intentionally file-only. It has no application, CLI, database, embeddings, automated indexer, domain-profile library, or background ingestion. Start with the initializer, use the resulting wiki, and evolve its local configuration from actual needs.
