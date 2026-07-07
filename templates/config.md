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

Every knowledge page keeps all nine frontmatter keys in this order:

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

Use a canonical URI for `resource`, or `null` when absent. Use relative paths from the wiki page in `raw`, or `[]` when no raw file applies. Never omit these keys and do not add a `subtype` field; use tags for narrower classifications.

Tags provide broad categorization across the approved dimensions above. Portable relative Markdown links explain specific relationships. Evidence-based statements should link to the relevant source page or raw file.

## Raw intake

<!-- Where will new material arrive, and how should the agent recognize that it is ready to process? -->

## Sensitive information

<!-- Define constraints on reading, quoting, linking, retention, and generated content. Write "No additional constraints" if none apply. -->

## Local conventions

<!-- Record useful conventions learned while operating this particular wiki. -->
