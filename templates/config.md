# Wiki configuration

## Purpose

<!-- What should this knowledge base help its user understand or do? -->

## Scope

<!-- State what belongs here. -->

## Outside scope

<!-- State nearby material that should not be incorporated. -->

## Local terminology

<!-- Record naming conventions and domain vocabulary. Do not replace the six universal page types. -->

## Tag vocabulary

<!-- Keep only dimensions useful to this wiki. Seed roughly 8–15 tags during initialization rather than trying to predict everything. -->

### Business functions

<!-- Example: `sales` — Customer acquisition and commercial relationships. -->

### Industries and domains

<!-- Example: `circular-economy` — Systems that retain material and product value. -->

### Evidence and document forms

<!-- Example: `customer-interview` — Evidence obtained through a customer conversation. -->

### Topics and themes

<!-- Example: `onboarding` — Initial adoption and setup experience. -->

### Work modes

<!-- Example: `experiment` — A bounded test intended to reduce uncertainty. -->

Tag rules:

- Use short lowercase kebab-case strings.
- Reuse an approved tag before proposing a new one.
- Avoid synonyms and near-duplicates.
- Do not repeat `type` or `status` values as tags merely for classification.
- Use several tags when a page genuinely crosses dimensions.
- Propose and approve vocabulary additions before first use, then record them here with one-line meanings.
- During maintenance, flag unused tags, accidental synonyms, and tags that have become too broad.

## Ownership

- `raw/` is human-owned and immutable. The agent may read and cite raw files but must never edit, rename, move, or delete them.
- `wiki/` is agent-maintained after explicit approval. It is flat by default, and `type` frontmatter provides semantic classification.
- Operational files are `config.md`, `index.md`, `log.md`, and the root agent instruction file.

## Approval policy

Every write follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

Before writing, describe the proposed file-level changes and wait for explicit approval. Apply only what was approved. Renames, moves, merges, archival, and deletion always require approval and link repair.

## Page model

Allowed types: `source`, `subject`, `note`, `synthesis`, `decision`, `plan`.

Allowed statuses: `fragment`, `draft`, `review`, `current`, `completed`, `archived`.

Every knowledge page keeps all eight frontmatter keys in this order:

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

`resource` identifies the primary underlying asset described by the page. Use an absolute URL or a relative path such as `../raw/customer-orders.csv`. Use `null` for abstract ideas and knowledge products—such as a synthesis, business plan, strategy, or decision—that do not describe one specific asset. Never omit the key. Use citations for additional supporting files and tags for narrower classifications.

Tags provide broad categorization across the approved dimensions above. Portable relative Markdown links explain specific relationships. Evidence-based statements should link to the relevant source page or raw file.

## Citations

Use numeric citation markers immediately after claims sourced from external material. Number sources by first appearance and reuse the same number for repeated citations. Use `[1, 2]` when several sources support one claim and add locators when useful, such as `[2, p. 14]`, `[3, 01:12:30]`, or `[4, rows 20–35]`.

Place the citation list under `## Citations` as the final section:

```markdown
## Citations

[1] [Source title](https://example.com/source)
[2] [Internal source](../raw/path/to/source.pdf)
```

Citation targets may be absolute URLs or relative paths. Prefer the closest preserved evidence. `resource` provides page-level identity for the primary underlying asset; citations provide claim-level provenance and can reference additional raw files. Omit the section when no externally sourced claims appear. Never invent missing citation details; mark unsupported claims explicitly.

## Raw intake

<!-- Where will new material arrive, and how should the agent recognize that it is ready to process? -->

## Sensitive information

<!-- Define constraints on reading, quoting, linking, retention, and generated content. Write "No additional constraints" if none apply. -->

## Local conventions

<!-- Record useful conventions learned while operating this particular wiki. -->
