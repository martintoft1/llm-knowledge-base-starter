# Wiki configuration

## Purpose

<!-- What should this knowledge base help its user understand or do? -->

## Scope

<!-- State what belongs here. -->

## Outside scope

<!-- State nearby material that should not be incorporated. -->

## Local terminology

<!-- List useful subtypes, tags, naming conventions, and domain vocabulary. Do not replace the six universal page types. -->

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

Tags provide broad categorization. Portable relative Markdown links explain specific relationships. Evidence-based statements should link to the relevant source page or raw file.

## Raw intake

<!-- Where will new material arrive, and how should the agent recognize that it is ready to process? -->

## Sensitive information

<!-- Define constraints on reading, quoting, linking, retention, and generated content. Write "No additional constraints" if none apply. -->

## Local conventions

<!-- Record useful conventions learned while operating this particular wiki. -->
