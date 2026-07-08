# LLM Wiki

A small, portable pattern for knowledge bases that compound over time. Raw material remains untouched; an LLM maintains a linked Markdown wiki that integrates what the sources mean.

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

## Knowledge model

Every wiki page uses one of six universal types:

- `source`: one imported piece of evidence
- `subject`: an enduring topic or entity
- `note`: a provisional idea, question, or observation
- `synthesis`: a reasoned conclusion across evidence
- `decision`: a choice and its rationale
- `plan`: intended action and progress

Local vocabulary belongs in tags such as `customer-interview`, `research-paper`, `strategy`, or `roadmap`. This keeps the schema small while allowing several useful classifications on one page.

Tags provide broad, cross-cutting categorization. Relative Markdown links explain specific relationships in context.

## Frontmatter

Every knowledge page keeps the same eight keys, even when `resource` is empty:

```yaml
---
type: source
title: Display name
description: One plain-text sentence suitable for indexes and previews.
status: draft
tags: []
resource: null
created: "YYYY-MM-DDTHH:MM:SS±HH:MM"
updated: "YYYY-MM-DDTHH:MM:SS±HH:MM"
---
```

`resource` identifies the primary underlying asset described by the page. It may be an absolute URL or a relative path such as `../raw/customer-orders.csv`. Use `resource: null` for abstract ideas and knowledge products—such as a synthesis, business plan, strategy, or decision—that do not describe one specific asset. Additional supporting material belongs in claim-level citations.

Tags are short lowercase kebab-case strings. The initializer proposes a small vocabulary based on the wiki's context rather than inventing tags page by page.

Tag suggestions may cover several dimensions:

- Business function: `operations`, `admin`, `technology`, `marketing`, `sales`, `finance`
- Industry or domain: `circular-economy`, `climate`, `health`, `agriculture`
- Evidence or document form: `customer-interview`, `research-paper`, `dataset`, `meeting`
- Topic or theme: `pricing`, `onboarding`, `retention`, `supply-chain`
- Work mode: `hypothesis`, `experiment`, `analysis`

These are examples, not a universal taxonomy. Each initialized wiki records its approved vocabulary and meanings in `config.md`.

## Tags and links

Tags and links do different jobs:

- Tags place a page in broad, cross-cutting categories such as `climate`, `sales`, `customer-interview`, or `onboarding`.
- Relative Markdown links connect a page to a specific source, subject, synthesis, decision, or plan and explain that relationship in context.

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

`resource` provides page-level identity for the primary underlying asset. Citations provide claim-level provenance and can reference additional raw files. Omit the citations section when no externally sourced claims appear, and never invent missing citation details.

## Operating model

The human owns sources, scope, and approval. The agent performs the bookkeeping: summarizing, connecting, updating, checking contradictions, and maintaining navigation.

Every write follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

Raw files are immutable. The agent may read and cite them but never edit, rename, move, or delete them.

## Templates

[`templates/`](templates/) contains inspectable examples for the generated configuration, index, log, and six page types. They are reference material; `BOOTSTRAP.md` remains usable on its own.

## Version 1

This version is intentionally file-only. It has no application, CLI, database, embeddings, automated indexer, domain-profile library, or background ingestion. Start with the initializer, use the resulting wiki, and evolve its local configuration from actual needs.
