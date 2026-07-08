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

- `raw/` is human-controlled source storage. The agent may propose and, after normal approval, add new files. Once a raw file exists, modifying, overwriting, renaming, moving, or deleting it requires separate, explicit human approval naming the file and operation. Prefer adding a derived or corrected file while preserving the original.
- `wiki/` is agent-maintained after explicit approval. It is flat by default, and `type` frontmatter provides semantic classification.
- Operational files are `config.md`, `index.md`, `log.md`, and the root agent instruction file.

## Approval policy

Every write follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

Before writing, describe the proposed file-level changes and wait for explicit approval. Apply only what was approved. Renames, moves, merges, archival, and deletion always require approval and link repair.

## Knowledge pages

Every file under `wiki/` has YAML frontmatter followed by a Markdown body. Frontmatter provides consistent metadata. The body contains the knowledge, contextual links, and an optional final citations section.

## Frontmatter

Every knowledge page keeps all eight frontmatter keys in this order. The block below is a schema illustration, not copy-ready YAML. Angle-bracket values are placeholders to replace from the actual page context; listed choices are allowed values, not defaults.

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

### Field rules

- `type`: choose `source`, `subject`, `note`, `synthesis`, `decision`, or `plan` from the page's purpose. No value is preferred by default.
- `title`: use the human-readable display name.
- `description`: use one plain-text sentence suitable for indexes, previews, and search results.
- `status`: choose `fragment`, `draft`, `review`, `current`, `completed`, or `archived` from the page's actual lifecycle state. No value is a universal default.
- `tags`: choose from the approved vocabulary above; propose additions before first use.
- `resource`: identify the primary underlying asset with an absolute URL or relative path such as `../raw/customer-orders.csv`. Use `null` for abstract ideas and knowledge products that do not describe one specific asset. Use citations for additional supporting files.
- `created`: use an ISO 8601 datetime with an explicit timezone offset and never change it.
- `updated`: use an ISO 8601 datetime with an explicit timezone offset and change it only after a meaningful content or metadata change.

Never omit a key.

Tags provide broad categorization across the approved dimensions above. Portable relative Markdown links explain specific relationships. Evidence-based statements should link to the relevant source page or raw file.

## Citations

Use numeric citation markers immediately after claims sourced from external material. Number sources by first appearance and reuse the same number for repeated citations. Use `[1, 2]` when several sources support one claim and add locators when useful, such as `[2, p. 14]`, `[3, 01:12:30]`, or `[4, rows 20–35]`.

Place the citation list under `## Citations` as the final section:

```markdown
## Citations

[1] [Source title](https://example.com/source)
[2] [Internal source](../raw/path/to/source.pdf)
```

Citation targets may be absolute URLs or relative paths. Prefer the closest preserved evidence. Citations provide claim-level provenance and can reference raw files. Omit the section when no externally sourced claims appear. Never invent missing citation details; mark unsupported claims explicitly.

## Raw intake

<!-- Where will new material arrive, and how should the agent recognize that it is ready to process? -->

## Sensitive information

<!-- Define constraints on reading, quoting, linking, retention, and generated content. Write "No additional constraints" if none apply. -->

## Local conventions

<!-- Record useful conventions learned while operating this particular wiki. -->
