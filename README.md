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

Every knowledge page keeps the same nine keys, even when some values are empty:

```yaml
---
type: source
title: Display name
description: One plain-text sentence suitable for indexes and previews.
status: draft
tags: []
resource: null
raw: []
created: "YYYY-MM-DDTHH:MM:SS±HH:MM"
updated: "YYYY-MM-DDTHH:MM:SS±HH:MM"
---
```

Use `resource: null` when there is no canonical URI and `raw: []` when no preserved source file applies. Tags are short lowercase kebab-case strings. The initializer proposes a small vocabulary based on the wiki's context rather than inventing tags page by page.

Tag suggestions may cover several dimensions:

- Business function: `operations`, `admin`, `technology`, `marketing`, `sales`, `finance`
- Industry or domain: `circular-economy`, `climate`, `health`, `agriculture`
- Evidence or document form: `customer-interview`, `research-paper`, `dataset`, `meeting`
- Topic or theme: `pricing`, `onboarding`, `retention`, `supply-chain`
- Work mode: `hypothesis`, `experiment`, `analysis`

These are examples, not a universal taxonomy. Each initialized wiki records its approved vocabulary and meanings in `config.md`.

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
