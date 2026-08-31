# Wiki Writing Style

Keep the knowledge base intentionally flat and simple. Write the smallest useful page, then add structure only when it makes the content easier to retrieve or reuse.

This file defines the reusable rules for writing concept bodies.

## Required Local Settings

Before writing or substantially rewriting a body, read:

- [Writing Style](local-settings.md#writing-style) for the selected local style.

## Body Rules

- Use concise reference notes unless the approved local settings specify another style. Preserve reasoning when it will help later work.
- Start with plain prose and the smallest useful structure.
- Follow [Atomic Concepts And Links](schema.md#atomic-concepts-and-links).
- Use headings, lists, tables, and fenced code blocks when they improve human reading or agent retrieval.
- Distinguish evidence, interpretation, inference, uncertainty, and unresolved conflict when relevant. Do not force these into headings.
- Attribute specific claims with footnotes keyed to `sources[].id`. Do not add a separate citations section.

Use tags and links before creating folders. A shared topic alone is not a reason for a directory.

## Claims And Evidence

- Locate exact quotations, dates, numbers, and identifiers in the source before writing them. Preserve the source's form when it matters. Show the source components behind a derived value.
- Present a direct source statement as evidence, not as the writer's conclusion.
- A synthesis may combine compatible evidence from several sources. Cite the material sources.
- Identify an inference when the sources do not state the conclusion directly, and preserve the reasoning that supports it.
- Remove or qualify claims that the available evidence does not support. Mark inaccessible evidence and unresolved conflict clearly.

When retaining a disputed or historically useful outdated claim, place a short block directly after it:

```markdown
> **Claim status: disputed**
> The sources disagree about ...
```

```markdown
> **Claim status: outdated since 2026-08-31**
> The current understanding is ...
```

Do not retain every superseded claim. Update the live concept and rely on Git and `wiki/log.md` when the old wording has no continuing value.

An explicitly requested snapshot should state that it is a point-in-time synthesis and link to its canonical source concepts instead of copying them extensively.

## Type-Specific Structure

Use the optional YAML-fields and headings in [`schema.md`](schema.md#types-and-field-rules) and the matching files under `templates/page-bodies/` when they help. New notes normally need no body template.
