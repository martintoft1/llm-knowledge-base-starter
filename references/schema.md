# Local OKF Profile

This file narrows OKF v0.2 for this starter kit. The pinned specification remains the source of truth for OKF fields and semantics. See [`okf/v0.2/SPEC.md`](okf/v0.2/SPEC.md), especially sections 4 through 7, 10, and 11.

## Required Frontmatter

Every concept under `wiki/`, except reserved `index.md` and `log.md` files, must include:

```yaml
---
type: Note
title: Example note
status: draft
tags: []
generated:
  by: example-agent/1.0
  at: "2026-08-18T12:00:00+02:00"
---
```

Local requirements:

- `type` is a non-empty type name.
- `title` is a human-readable display name.
- `status` is `draft`, `stable`, or `deprecated`.
- `tags` is a YAML list, which may be empty.
- `generated` contains a non-empty `by` actor and an ISO 8601 `at` datetime. Change `generated.at` only after a meaningful content or metadata change.
- `description` is optional for early drafts and required before a concept becomes `stable`. Keep it to one sentence.

Omit optional fields when they do not apply. Do not add empty mappings, empty lists, or `null` placeholders for them.

## Optional OKF Fields

Use these only as defined upstream:

- `resource`: the canonical asset the concept describes. See sections 4.1 and 6.2.
- `sources` and `usage_window`: provenance and objective source signals. See section 5.1.
- `verified`: independent verification events. See sections 5.2 and 7. A bare mapping and a list are both valid OKF.
- `stale_after`: the absolute date on which the content becomes stale. See section 5.5.
- Attested Computation fields: `runtime` is required whenever `type: Attested Computation`. `parameters`, `computation`, `executor`, and `attester` retain their exact section 10 semantics.

Never invent provenance, verification, usage, access, or attestation. Preserve unknown fields when editing a concept. Unknown fields and types do not make an OKF concept invalid.

## Actors

Identity fields such as `generated.by`, `verified[].by`, and `sources[].author` use the OKF actor patterns exactly:

- Agents and tools: `<producer>/<version>`, such as `reference-agent/1.0`.
- People: `human:<id>`, such as `human:owner`.
- Automated processes: `process:<id>`, such as `process:nightly-refresh`.

Use `human:` for human-authored or human-confirmed content because OKF trust tiers depend on that prefix. Do not represent a person or process with the agent pattern.

## Sources And Claim Attribution

Each `sources` entry requires `resource`. It may also contain `id`, `title`, `author`, `usage_count`, and `last_modified` as defined in section 5.1. A shared `usage_window` belongs beside `sources`; one source may override it with its own window.

When a body attributes a specific claim, give the source a stable `id` and use the same key in a Markdown footnote:

```yaml
sources:
  - id: policy
    resource: https://example.com/policy
    title: Example policy
```

```markdown
The policy took effect in August.[^policy]

[^policy]: Example policy
```

The footnote text helps readers, but the label is the join key. Every source-linked footnote must match a `sources[].id`, and every cited `sources[].id` must have a corresponding footnote. Do not use a separate citations section.

## Links And Paths

Use standard Markdown links and explain the relationship in the surrounding prose. For links within the bundle, prefer bundle-absolute paths beginning with `/`. Relative paths and absolute URLs are also valid.

Path-valued fields follow section 6.2. A source `resource` may instead be a scope description as allowed by section 5.1.

Report broken links, but do not treat them as an OKF conformance failure. Preserve links that intentionally point to knowledge not yet written.

## Local Types

Use the smallest type that describes the concept itself:

| Type | Use |
|---|---|
| `Note` | Provisional or general knowledge that does not need a narrower type |
| `Reference` | Durable explanation, instruction, topic, entity, or procedure |
| `Source` | A concept describing one source or evidence bundle |
| `Analysis` | Comparison, investigation, synthesis, or reasoned conclusion |
| `Decision` | A settled choice and its reasoning |
| `Goal` | A desired outcome or declared priority |
| `Plan` | An approach and actions intended to reach an outcome |
| `Dataset` | A bounded dataset, its schema, meaning, and limits |
| `Database` | A database or live data system, its access boundary, schema, and limits |
| `Attested Computation` | A sanctioned computation contract that follows section 10 |

Create new concepts with one of these types. Consumers and editors must still accept and preserve unknown types found in a bundle.

## Tags

### Registry

No tags are approved yet.

Use only tags recorded in this registry. Keep the registry small and driven by real retrieval needs. Prefer links and clear titles before adding a tag.

Propose a registry change before adding, renaming, merging, narrowing, or retiring a tag. The proposal should name the affected concepts and explain the retrieval benefit. Avoid synonyms, near-duplicates, and tags that merely repeat a type or status.

## Validation

Validate the whole bundle against OKF section 11 and this local profile before finalizing a wiki operation. In particular:

- Parse every concept's frontmatter and require the local fields above.
- Validate any optional field family that appears against its upstream structure.
- Check actor patterns and source-linked footnotes.
- For every `type: Attested Computation`, require `runtime` and validate all other computation fields that appear against section 10, regardless of status.
- Preserve unknown fields and types.
- Report broken links without failing OKF conformance.

A failed required check blocks completion. Local-profile failures may block this repository's workflow even when the concept meets base OKF conformance.
