# Wiki schema

This file defines how wiki files are structured. It is the routine source of truth for the starter kit's reusable schema. Local, user-specific settings live in [`local-settings.md`](local-settings.md).

The pinned [`okf/v0.2/SPEC.md`](okf/v0.2/SPEC.md) remains authoritative. Consult it when this schema does not cover a field or edge case, when resolving ambiguity, during a formal base-OKF audit, or when changing the schema or OKF version. Do not use this schema to override the specification.

## Knowledge-base files

The knowledge base consists of its maintained wiki and retained sources. Supporting instructions, templates, tooling, and tests operate on the knowledge base but are not part of it.

### Wiki files

Files under `wiki/` form the queryable knowledge layer. This includes all concept files, `index.md` files, and the `log.md` file. In OKF terminology, these files make up the knowledge bundle.

Every file inside `wiki/` must be UTF-8 Markdown with a `.md` filename. This wiki-schema rule is stricter than base OKF, which permits other support files. Non-Markdown evidence, computation code, and other support assets are not allowed as bundle members.

#### Index

`wiki/index.md` is mandatory and carries the bundle's `okf_version` declaration. It must list every concept exactly once, excluding reserved `index.md` and `log.md` files. Group entries under useful headings and include each concept's `description`. Mark deprecated concepts clearly.

Subdirectory indexes are optional additions for progressive disclosure; they do not replace the complete root index. Every index link must resolve relative to the index file.

#### Log

`wiki/log.md` is mandatory. It has no frontmatter, begins with `# Directory Update Log`, and groups concise operation bullets newest-first under date-only `YYYY-MM-DD` headings. Begin each bullet with a bold operation name such as `**Ingest**` or `**Maintenance**`.

Log changes to concepts or retained sources under the operation that produced them. Documentation-only, tooling-only, and no-change work has no log entry.

An ingest entry names each retained source and the concepts that use it as a subject or as evidence for created, updated, supported, or disputed knowledge.

For a raw-file deletion, record the deleted path and reason in a Maintenance entry. Preserve earlier retention entries as history.

### Raw files

Files under `raw/` preserve original evidence used by the wiki. They belong to the local knowledge base but are not part of the OKF knowledge bundle.

Every retained original under `raw/` must be used by at least one wiki concept as evidence through `sources[].resource` or as the concept's subject through `resource`. Do not retain material merely for storage. This requirement excludes `raw/.gitkeep`.


## Atomicity And Organization

Atomicity applies both within and across files. Each concept file must cover one atomic concept: the smallest useful unit that can stand alone and be sourced, linked, and maintained independently.

- Within a file, include only material needed to define, support, explain, or use the concept. Keep necessary context, evidence, reasoning, and examples; omit tangents, repetition, and unnecessary structure.
- Split a concept's content across files when its parts can stand alone or change independently. Length alone is not a reason to split.
- Give each concept one canonical file. Follow [Links Between Concepts](#links-between-concepts) when an explicit relationship is needed. Do not duplicate substantial content; a linking file may include the minimum summary needed to make the relationship understandable.
- Overviews, syntheses, analyses, decisions, and plans may connect several concepts, but each file must express one clear collection, comparison, conclusion, decision, or plan. Link to canonical concept files rather than reproducing them.

Keep `wiki/` flat until navigation becomes genuinely difficult. Prefer clear titles, a small maintained tag registry, and useful links before folders. Add subdirectories only when they materially improve navigation or progressive disclosure.

## Concept Types And Requirements

Use the smallest type that describes the concept itself. Begin with the shared page template, then add only the fields required or justified by its type rules:

| Type | What it is and when to use it | Additional frontmatter requirements |
|---|---|---|
| `Note` | Provisional or general knowledge that does not need a narrower type | None |
| `Reference` | A durable explanation, instruction, topic, entity, or procedure | Use [`resource`](#resource) when bound to one canonical asset; use [`sources`](#sources) when derived from evidence |
| `Source Record` | A concept describing one source or evidence bundle | [`resource`](#resource) is required from creation |
| `Analysis` | A comparison, investigation, synthesis, or reasoned conclusion | Use [`sources`](#sources) when conclusions depend on evidence |
| `Decision` | A settled choice and its reasoning | Use [`sources`](#sources) when evidence informed the choice |
| `Goal` | A desired outcome or declared priority | Use [`stale_after`](#stale_after) only for a real review or expiry date |
| `Plan` | An approach and actions intended to reach an outcome | Use [`stale_after`](#stale_after) only for a real review or expiry date |
| `Dataset` | A bounded dataset, its schema, meaning, and limits | [`resource`](#resource) is required before `stable` |
| `Database` | A database or live data system, its access boundary, schema, and limits | [`resource`](#resource) is required before `stable` |
| `Attested Computation` | A sanctioned computation contract | Follow [Attested Computation Requirements](#attested-computation-requirements) |

Use `Source Record` rather than `Source` so the concept type is not confused with the `sources` provenance field. Existing or imported `Source` concepts remain valid unknown types and must be preserved.

Create new concepts with one of these types. Consumers and editors must still accept and preserve any unknown type found in a bundle.

### Attested Computation Requirements

An Attested Computation combines the requirements documented under [`runtime`](#runtime), [`parameters`](#parameters), [`computation`](#computation), [`executor`](#executor), [`attester`](#attester), [`sources`](#sources), [`verified`](#verified), and [`stale_after`](#stale_after). Those field sections define when each field is required. Keep the concept `draft` until all conditions for `stable` are met. These fields retain their exact OKF section 10 structure and meaning.

## Frontmatter

Frontmatter is the YAML block between `---` markers at the top of each concept file. Its structured fields help people, agents, and tools identify, find, assess, and maintain concepts without inferring this information from their bodies.

This wiki requires six fields for every concept, although base OKF requires only `type`. Use the table below to select fields, then follow the linked field section for its meaning, structure, and rules.

### When To Use Each Field

#### Normal fields


| Field | When to use it |
|---|---|
| [`type`](#type) | Every concept |
| [`title`](#title) | Every concept |
| [`description`](#description) | Every concept |
| [`status`](#status) | Every concept |
| [`tags`](#tags) | Every concept; include at least one tag from the Tag Registry |
| [`generated`](#generated) | Every concept; update it after a meaningful content or metadata change |
| [`resource`](#resource) | When the concept describes one addressable canonical asset; some types require it |
| [`sources`](#sources) | When the concept derives claims from evidence; required before an Attested Computation becomes `stable` |
| [`usage_window`](#usage_window) | When any source records `usage_count` |
| [`verified`](#verified) | Only after a real check; required before an Attested Computation becomes `stable` |
| [`stale_after`](#stale_after) | When there is a defensible expiry, review, or validity date; required for a stable Attested Computation when its definition can expire |

#### Attested Computation fields

| Field | When to use it |
|---|---|
| [`runtime`](#runtime) | Every Attested Computation |
| [`parameters`](#parameters) | Optionally while an Attested Computation is non-stable; required and non-empty before `stable` |
| [`computation`](#computation) | Only when an Attested Computation uses the file form; use the inline body form instead when appropriate |
| [`executor`](#executor) | Optionally while an Attested Computation is non-stable; required before `stable` |
| [`attester`](#attester) | Optionally while an Attested Computation is non-stable; required before `stable` |

### Mandatory Fields

Every concept under `wiki/`, except reserved `index.md` and `log.md` files, must include:

```yaml
---
type: Note
title: Example note
description: This is a description
status: draft
tags: [example-tag]
generated:
  by: example-agent/1.0
  at: "2026-08-18T12:00:00+02:00"
---
```

Use [`templates/wiki-page.md`](../templates/wiki-page.md) as the shared starting point.

#### `type`

`type` is a non-empty name identifying the concept's kind. Use it for routing, filtering, and presentation. Choose the smallest applicable type under [Concept Types And Requirements](#concept-types-and-requirements). Consumers and editors must accept and preserve unknown types.

#### `title`

`title` is the concept's human-readable display name. Keep it specific enough to distinguish the concept from related pages.

#### `description`

`description` is a one-sentence summary used in the root index, search results, and previews. Describe the concept itself rather than how the page is organized.

#### `status`

`status` records the concept's lifecycle state:

- `draft`: may be incomplete.
- `stable`: ready for consumption and compliant with this wiki schema.
- `deprecated`: retained for links and history but no longer current.

#### `tags`

`tags` is a non-empty YAML list of approved cross-cutting retrieval labels. Every concept must have at least one tag from the [Tag Registry](local-settings.md#tag-registry).

Reuse an existing tag when its registered meaning applies. Do not add an irrelevant tag merely to satisfy the requirement.

Create a tag only when it provides a useful way to group and retrieve multiple concepts. Prefer cross-cutting topics or domains, such as `finance`, `product`, or `sales`, and useful content forms, such as `interview` or `pitch-deck`. Do not create page-specific tags, synonyms or near-duplicates, or tags that merely repeat a concept's type or status.

Record each approved registry entry in `local-settings.md` as one Markdown bullet:

```markdown
- `<tag>`: <meaning and when to use it>
```

Use the registry tag's exact spelling in concept frontmatter. Use short lowercase kebab-case names. Keep the registry small and driven by real retrieval needs. Use tags, rather than body links, for cross-cutting grouping and discovery. Reuse existing tags before adding new ones.

If no suitable tag exists, add one under [Tag Registry Changes](operations.md#tag-registry-changes) before using it. Apply it only to concepts within the current operation's scope. Changing an existing tag follows the approval rules in that workflow.

#### `generated`

`generated` records who or what produced the current content and when it last changed meaningfully. It contains a non-empty `by` actor and an `at` datetime with seconds and timezone:

```yaml
generated:
  by: example-agent/1.0
  at: "2026-08-18T12:00:00+02:00"
```

Change `generated` only after a meaningful content or metadata change. Follow [Actor Identifiers](#actor-identifiers) for `by` and [Dates And Datetimes](#dates-and-datetimes) for `at`.

### Optional And Conditional Fields

These fields are absent by default. Add them only under the conditions below or when a concept's type and status require them.

#### `resource`

`resource` identifies the single canonical asset the concept describes. Use it when the subject is a particular source, file, dataset, database, API, dashboard, or other addressable asset. Omit it for abstract ideas and general instructions.

```yaml
resource: ../raw/customer-policy.pdf
```

Top-level `resource` is the subject resource. It does not say where the concept's claims came from; `sources` records that provenance. A concept may use either field or both. Use the same asset in both only when it genuinely serves as both subject and evidence. Follow [Paths And URIs](#paths-and-uris) for allowed values. See OKF sections 4.1 and 6.2 for normative details.

#### `sources`

`sources` records internal or external evidence from which the concept derives knowledge. Use it when evidence supports, qualifies, or contradicts the concept. Add another entry when new evidence supports, qualifies, or contradicts the concept. Before an Attested Computation becomes `stable`, it must contain one or more relevant source entries.

Each entry requires a stable `id` and `resource`; `sources[].resource` is the evidence location, not the concept's subject:

```yaml
sources:
  - id: policy
    resource: ../raw/customer-policy.pdf
    title: Customer policy
    author: human:owner
    last_modified: 2026-08-01
```

A source may also carry:

- `title`: a human-readable source name.
- `author`: the source producer, following [Actor Identifiers](#actor-identifiers).
- `last_modified`: when the source itself last changed, as `YYYY-MM-DD`.
- `usage_count`: how often the source was exercised during a stated [`usage_window`](#usage_window). It is a liveness signal, not a credibility score.

Cite sourced material where it appears, but do not repeat a citation while its source and scope remain clear. Use a Markdown footnote whose label matches `sources[].id`. When `sources[].resource` is a path or URL, link the source title to that exact resource:

```markdown
The policy took effect in August.[^policy]

[^policy]: [Customer policy](../raw/customer-policy.pdf)
```

Use a plain-text footnote only when `sources[].resource` describes a non-addressable scope, such as `all product queries`. Every source ID must be cited in the body and have one matching footnote definition. Do not create a separate citations section. This follows [APA's guidance](https://apastyle.apa.org/style-grammar-guidelines/citations/appropriate-citation) to avoid both undercitation and overcitation and [Chicago's guidance](https://www.chicagomanualofstyle.org/qanda/data/faq/topics/Documentation/faq0113.html) to cite wherever attribution would otherwise be unclear.

#### `usage_window`

`usage_window` records the date range covered by source `usage_count` measurements. Add it beside `sources` whenever any source has `usage_count`:

```yaml
usage_window: { from: 2026-08-01, to: 2026-08-31 }
```

A source may carry its own window to override the shared one. Omit `usage_count` and `usage_window` when the measurement or its dates are unknown. See OKF section 5.1 for normative details and credibility semantics.

#### `verified`

`verified` records a real check of the current content against its `resource` or `sources`. It is independent of `generated`: the writer need not be the verifier.

```yaml
verified: { by: "human:owner", at: "2026-08-19T08:00:00Z" }
```

Use a list for multiple independent checks. Each event contains `by` and `at`. Omit `verified` when no check occurred; absence means unverified, not invalid. Never infer or invent verification. Before an Attested Computation becomes `stable`, it needs at least one verification event from an actor independent of `generated.by`. See OKF sections 5.2, 5.3, and 7 for normative details and derived trust tiers.

Each verification time follows [Dates And Datetimes](#dates-and-datetimes). When the latest verification predates `generated.at`, the verification remains part of the concept's trust history, but consumers should warn that it predates the latest meaningful content change. Do not change the OKF trust tier or discard the event merely because the concept changed later.

#### `stale_after`

`stale_after` is the absolute date on which the concept becomes stale. Use it only when there is a defensible expiry, review, or validity date. A stable Attested Computation requires it when its definition can expire.

```yaml
stale_after: 2026-12-31
```

A concept is stale when `today >= stale_after`. Omit the field when no meaningful date is known; do not guess one. See OKF section 5.5 for normative details.

Verification and freshness answer different questions. `verified` records a check that the concept matches its evidence. `stale_after` records when the knowledge becomes stale. Unchanged immutable evidence does not make a time-sensitive claim permanently current, and timeless knowledge does not need an arbitrary expiry.

#### `runtime`

`runtime` identifies how an Attested Computation runs, how its parameters bind, and how its executor and attester should interpret it. It is required for every Attested Computation, regardless of status. Example values include `bigquery`, `postgres`, `dbt`, `python`, and `Looker`.

#### `parameters`

`parameters` lists the typed, named values that may be supplied to an Attested Computation. Each entry contains `name`, `type`, and `required`:

```yaml
parameters:
  - { name: year, type: integer, required: true }
```

The list is optional while the concept is non-stable. Before it becomes `stable`, the list must be non-empty. Under this stricter schema, a zero-input computation remains `draft`. Binding semantics follow `runtime`.

#### `computation`

`computation` points to a file containing the sanctioned computation. Use it for the file form and omit the inline computation fence:

```yaml
computation: references/computations/revenue.sql
```

For an Attested Computation to become `stable`, it must have exactly one computation form: either `computation` or one inline fenced block under `# Computation`, but not both. The field is optional while the concept is non-stable. Follow [Paths And URIs](#paths-and-uris) for allowed values.

#### `executor`

`executor` records how an Attested Computation is run. Its `resource` names instructions or code, and its `receipt` lists the evidence fields each run must return:

```yaml
executor:
  resource: references/skills/run-on-bq.md
  receipt: [job_id, executed_sql, result]
```

The field is optional while the concept is non-stable. Before it becomes `stable`, `executor.resource` and a non-empty `executor.receipt` are required. Follow [Paths And URIs](#paths-and-uris) for the resource value.

#### `attester`

`attester` records the deterministic, non-LLM check that consumes a computation receipt and returns a verdict. Its `resource` names the checking code:

```yaml
attester:
  resource: references/attesters/revenue.py
```

The field is optional while the concept is non-stable. Before it becomes `stable`, `attester.resource` is required. Follow [Paths And URIs](#paths-and-uris) for the resource value. Do not claim executable validity without a usable computation and executor, or attestable validity without a usable attester.

### Shared Field Value Conventions

These conventions define values reused across fields; they are not separate frontmatter fields.

#### Actor Identifiers

Identity values such as `generated.by`, `verified[].by`, and `sources[].author` use these forms:

- Agents and tools: `<producer>/<version>`, such as `reference-agent/1.0`.
- People: `human:<id>`, such as `human:owner` or `human:<first name>`.
- Automated processes: `process:<id>`, such as `process:nightly-refresh`.

Actor identifiers are provenance labels. Use a unique stable identifier for each relevant actor. People who only read the knowledge base do not need identifiers.

When agents and tools create or meaningfully update a concept, they use the most specific truthful `<producer>/<version>` identifier available, such as `codex/gpt-5.6-terra`. Never ask a user to choose an agent identifier, and never invent a producer or version.

Use `human:` for human-authored or human-confirmed content. Do not represent a person or process with the agent pattern. See OKF section 7 for normative details.

#### Dates And Datetimes

Use ISO 8601 datetimes with seconds and timezone for `generated.at` and `verified[].at`. Use `YYYY-MM-DD` dates for `sources[].last_modified`, `usage_window.from`, `usage_window.to`, and `stale_after`. Record only dates and times that are known; do not invent precision.

#### Paths And URIs

Path-valued fields such as `resource`, `sources[].resource`, `computation`, `executor.resource`, and `attester.resource` accept:

- An absolute URL.
- A bundle-relative path beginning with `/`, which is preferred for internal concepts.
- A relative path resolved from the current file.

Unlike other path-valued fields, `sources[].resource` may also describe a population or scope that cannot be followed as a path, such as all queries in a named project. See OKF sections 5.1 and 6.2 for normative path semantics.

## Body Structure

Concept bodies are free-form Markdown. Use the optional structure below when it makes the concept clearer; do not add empty sections merely to match a template. The only conditional requirement is `# Computation`: an Attested Computation must use either one inline fenced block under that heading or the frontmatter `computation` path, but not both.

| Type | Body structure |
|---|---|
| `Note` | No default headings; follow the material |
| `Reference` | No default headings; follow the material |
| `Source Record` | Summary |
| `Analysis` | Conclusion, Reasoning |
| `Decision` | Decision, Rationale |
| `Goal` | Outcome, Success Measures, Progress |
| `Plan` | Approach, Actions, Progress |
| `Dataset` | Schema, Data, Examples, Access, Limitations |
| `Database` | Schema, Examples, Access, Limitations |
| `Attested Computation` | Computation, when using the inline form |

The matching files under `templates/page-bodies/` provide starting structures. Add, rename, or remove optional headings to fit the concept. Follow [`writing-style.md`](writing-style.md) when composing the body. Do not duplicate shared frontmatter across body templates; compose the base page template with the type rules so schema changes remain centralized and optional placeholders do not encourage invented metadata.

### Claim Status Blocks

When retaining a disputed or historically useful outdated claim, place a short block directly after it:

```markdown
> **Claim status: disputed**
> The sources disagree about ...
```

```markdown
> **Claim status: outdated since 2026-08-31**
> The current understanding is ...
```

### Links Between Concepts

Use standard Markdown links and explain the relationship in the surrounding prose. A link asserts a relationship; the prose explains whether that relationship means depends on, derives from, joins with, or something else.

Use tags for topical association and discovery. Use body links only when they avoid substantial duplication, connect an overview or index to its details, identify a dependency needed to understand or use a concept, or provide required provenance or resource access. Do not link merely because concepts share a topic, repeat the same link unnecessarily, or add reciprocal links solely for symmetry. If the relationship cannot be explained clearly in the surrounding prose, omit the link.

Internal Markdown links must resolve when they are added or maintained. This is a local wiki-schema rule beyond base OKF, whose consumers still tolerate broken links. Record future concept ideas in a `Plan` or maintenance report instead of creating dead links.

Provenance should normally remain in `sources` and keyed footnotes rather than creating extra body links. See OKF sections 5.1 and 6.1 for normative provenance and relationship semantics.
