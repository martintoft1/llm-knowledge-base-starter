# Wiki Writing Style

Keep the knowledge base intentionally flat and simple. Write the smallest useful page, then add structure only when it makes the content easier to retrieve or reuse.

This file defines the reusable rules for writing concept bodies.

## Required Local Settings

Before writing or substantially rewriting a body, read:

- [Identity And Scope](local-settings.md#identity-and-scope) for purpose, boundaries, and terminology.
- [Writing Style](local-settings.md#writing-style) for the selected local style.

## Body Rules

- Start with plain prose and the smallest useful structure.
- Follow OKF's one-concept-per-document rule. Keep one coherent idea, topic, outcome, or record in each file.
- Use headings, lists, tables, and fenced code blocks when they improve human reading or agent retrieval.
- Split by meaning, not length. First shorten without losing meaning, then split independent concepts or link to focused supporting pages.
- Merge concepts only when their information repeatedly belongs together.
- Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict when relevant. Do not force these into headings.
- Attribute specific claims with footnotes keyed to `sources[].id`. Do not add a separate citations section.

Use tags and links before creating folders. A shared topic alone is not a reason for a directory.

## Type-Specific Structure

Use the optional headings in [`schema.md`](schema.md#local-types-and-field-profiles) and the matching files under `templates/page-bodies/` when they help. New notes normally need no body template.
