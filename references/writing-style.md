# Wiki Writing Style

Write the smallest useful page, then add structure only when it makes the content easier to retrieve or reuse.

This file defines the reusable rules for writing concept bodies. Before writing or substantially rewriting a body, read the selected local [Writing Style](local-settings.md#writing-style) and apply it throughout.

## Body Rules

- Use concise reference notes unless the approved local settings specify another style. Preserve reasoning when it will help later work.
- Start with plain prose and the smallest useful structure.
- Follow [Atomic Concepts And Links](schema.md#atomic-concepts-and-links).
- Use headings, lists, tables, and fenced code blocks when they improve human reading or agent retrieval.
- Follow the schema's [provenance and citation rules](schema.md#provenance-sources-and-usage_window).

## Expressing Claims

- Make clear whether a statement comes directly from a source or is the writer's interpretation.
- Label inferences, uncertainty, and unresolved conflict plainly. Preserve supporting reasoning without forcing separate headings.
- Preserve source wording and notation when precision matters. Show the source components behind a derived value.

## Type-Specific Structure

Use the optional YAML-fields and headings in [`schema.md`](schema.md#types-and-field-rules) and the matching files under `templates/page-bodies/` when they help. New notes normally need no body template.

For an `Analysis`, state its scope and whether it is a current assessment or an assessment as of a specified date. Put any effective date or period in the body; it may differ from when the page was written. Update a current assessment when its evidence changes. For an assessment tied to a past date, preserve what was concluded then and record later conclusions separately. Correct errors in how the dated assessment or its evidence is represented.

For historical claims, identify the evidence versions used where available and explain any limits on reconstructing the assessment.
