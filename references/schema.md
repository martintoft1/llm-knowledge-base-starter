# Wiki Schema

This file defines how wiki files are structured: bundle rules, atomic concepts, required and optional metadata, actor identifiers, links and paths, types, body headings, and tag rules. It is the routine source of truth for the starter kit's reusable schema. Settings that vary between knowledge bases live in [`local-settings.md`](local-settings.md).

The pinned [`okf/v0.2/SPEC.md`](okf/v0.2/SPEC.md) remains authoritative. Consult it when this schema does not cover a field or edge case, when resolving ambiguity, during a formal base-OKF audit, or when changing the schema or OKF version. Do not use this schema to override the specification.

## Bundle Files

Every file inside `wiki/` must be UTF-8 Markdown with a `.md` filename. This wiki-schema rule is stricter than base OKF, which permits other support files. Non-Markdown evidence, computation code, and other support assets are not bundle members. Keep retained evidence under `raw/` or point to an external resource.

## Reserved Files

### Index

`wiki/index.md` is mandatory and carries the bundle's `okf_version` declaration. It must list every concept exactly once, excluding reserved `index.md` and `log.md` files. Group entries under useful headings and include each concept's `description` when available. Mark deprecated concepts clearly.

Subdirectory indexes are optional additions for progressive disclosure; they do not replace the complete root index. Every index link must resolve relative to the index file.

### Log

`wiki/log.md` is mandatory. It has no frontmatter, begins with `# Directory Update Log`, and groups concise operation bullets newest-first under date-only `YYYY-MM-DD` headings. Begin each bullet with a bold operation name such as `**Ingest**`, `**Snapshot**`, or `**Maintenance**`.

An ingest entry names the retained source and the concepts created, updated, supported, or placed in conflict. When a retained source is intentionally unused, use the exact phrase `Retained but unused`, followed by the project-root-relative raw path and a short reason:

```markdown
* **Ingest**: Retained but unused `raw/report.pdf` — it repeats knowledge already covered by existing sources.
```

## Atomic Concepts And Links

Each concept file must cover one atomic concept: the smallest useful unit that can stand alone and be sourced, linked, and maintained independently.

- Split content when its parts can stand alone or change independently. Keep necessary context, evidence, reasoning, and examples with the concept. Length alone is not a reason to split.
- Give each concept one canonical file. Connect related concepts with Markdown links and explain the relationship in the surrounding text. Do not duplicate substantial content; a linking file may include the minimum summary needed to make the relationship understandable.
- Overviews, syntheses, analyses, decisions, and plans may connect several concepts, but each file must express one clear collection, comparison, conclusion, decision, or plan. Link to canonical concept files rather than reproducing them.

Use the fewest links needed for retrieval and reuse. Add a link only when it avoids repeating substantial content, connects an overview or index to its details, identifies a dependency needed to understand or use the concept, or provides required provenance or resource access. Do not link merely because concepts share a topic, repeat the same link unnecessarily, or add reciprocal links solely for symmetry. If the relationship cannot be explained clearly in the surrounding prose, omit the link.

Provenance should normally remain in `sources` and keyed footnotes rather than creating extra body links.

## Frontmatter

### Required Wiki Fields

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

Use [`templates/wiki-page.md`](../templates/wiki-page.md) as the shared starting point. It contains the five fields required for every concept:

- `type` is a non-empty type name.
- `title` is a human-readable display name.
- `status` is `draft`, `stable`, or `deprecated`. A draft may be incomplete; stable content is ready for consumption and meets the wiki schema; deprecated content is retained for links and history but is no longer current.
- `tags` is a YAML list, which may be empty.
- `generated` contains a non-empty `by` actor and an ISO 8601 `at` datetime. Change `generated.at` only after a meaningful content or metadata change.

`description` is optional for early drafts and required before a concept becomes `stable`. Keep it to one sentence. This rule is conditional, so the draft template omits the field.

### Optional And Conditional Fields

Optional fields carry real meaning when present. Omit them when they do not apply; never add empty mappings, empty lists, `null`, or invented values merely to complete a template.

#### Resource

`resource` identifies the canonical asset the concept describes. Use it when the subject is a particular source, file, dataset, database, API, dashboard, or other addressable asset. Omit it for abstract ideas and general instructions.

```yaml
resource: ../raw/customer-policy.pdf
```

`resource` binds the concept to its subject. It does not say where the concept's claims came from; use `sources` for provenance. The allowed URL and path forms are described under [Links And Paths](#links-and-paths). See OKF sections 4.1 and 6.2 for normative details.

#### Provenance: `sources` And `usage_window`

Use `sources` when a concept derives material knowledge from internal or external evidence. Each entry requires `resource`. Add a stable `id` when the body attributes a claim to that source.

```yaml
sources:
  - id: policy
    resource: ../raw/customer-policy.pdf
    representation: ../raw/_derived/customer-policy.md
    title: Customer policy
    author: human:owner
    last_modified: 2026-08-01
```

A source may also carry:

- `representation`: a local Markdown or text rendering used to inspect a retained source that is difficult to read directly. It must resolve inside `raw/_derived/`. The canonical evidence remains `resource`; omit `representation` when no durable rendering is needed.
- `title`: a human-readable source name.
- `author`: the source producer, using the actor convention below.
- `last_modified`: when the source itself last changed, as `YYYY-MM-DD`.
- `usage_count`: how often the source was exercised during a stated window. It is a liveness signal, not a credibility score.

When any source uses `usage_count`, add a dated window beside `sources`, such as `usage_window: { from: 2026-08-01, to: 2026-08-31 }`. A source may provide its own window to override the shared one. Omit usage fields when the measurements or dates are not known. See OKF section 5.1 for normative details and credibility semantics.

For claim-level attribution, use a Markdown footnote whose label matches `sources[].id`:

```markdown
The policy took effect in August.[^policy]

[^policy]: Customer policy
```

Every source-linked footnote must resolve to a matching source ID, and every cited source ID must have a footnote. Do not create a separate citations section.

#### Trust: `verified`

`generated` records who or what produced the current content. `verified` records a real check of that content against its `resource` or `sources`. They are independent: the writer need not be the verifier.

```yaml
verified: { by: "human:owner", at: "2026-08-19T08:00:00Z" }
```

Use a list for multiple independent checks. Each event contains `by` and `at`. Omit `verified` when no check occurred; absence means unverified, not invalid. Never infer or invent verification. See OKF sections 5.2, 5.3, and 7 for normative details and derived trust tiers.

`verified` and `generated.at` remain independent. When the latest verification predates `generated.at`, the verification remains part of the concept's trust history, but consumers should warn that it predates the latest meaningful content change. Do not change the OKF trust tier or discard the event merely because the concept changed later.

#### Freshness: `stale_after`

`stale_after` is the absolute date on which the concept becomes stale. Use it only when there is a defensible expiry, review, or validity date.

```yaml
stale_after: 2026-12-31
```

A concept is stale when `today >= stale_after`. Omit the field when no meaningful date is known; do not guess one. See OKF section 5.5 for normative details.

Verification and freshness answer different questions. `verified` records a check that the concept matches its evidence. `stale_after` records when the knowledge becomes stale. Unchanged immutable evidence does not make a time-sensitive claim permanently current, and timeless knowledge does not need an arbitrary expiry.

#### Snapshot

An `Analysis` may set `snapshot: true` when it records an explicitly requested point-in-time synthesis. Omit the field for ordinary analyses and all other concept types. A snapshot requires one or more `sources` whose `resource` values resolve to internal concepts; `generated.at` records when the synthesis was made.

#### Attested Computation

Every Attested Computation requires `runtime`, regardless of status. Before its status may become `stable`, it also requires:

- A non-empty `parameters` list whose entries contain `name`, `type`, and `required`. Under this stricter schema, a zero-input computation remains `draft`.
- Exactly one computation form: one inline fenced block under `# Computation`, or a `computation` path, but not both.
- `executor.resource` and a non-empty `executor.receipt` list.
- `attester.resource` that names a deterministic, non-LLM check.
- One or more relevant `sources` entries with stable `id` values and matching keyed footnotes.
- At least one `verified` event from an actor independent of `generated.by`.
- `stale_after` when the definition can expire.

For non-stable concepts, `parameters`, `computation`, `executor`, and `attester` remain optional. When present, they keep their exact OKF section 10 structure and meaning. Do not claim executable validity without a usable computation and executor, or attestable validity without a usable attester.

### Actor Identifiers

Identity fields such as `generated.by`, `verified[].by`, and `sources[].author` use these forms:

- Agents and tools: `<producer>/<version>`, such as `reference-agent/1.0`.
- People: `human:<id>`, such as `human:owner` or `human:<first name>`.
- Automated processes: `process:<id>`, such as `process:nightly-refresh`.

Actor identifiers are provenance labels. Use a unique stable identifier for each relevant actor. People who only read the knowledge base do not need identifiers.

When agents and tools create or meaningfully update a concept, they use their own truthful `<producer>/<version>` identifier in `generated.by`. Never ask a user to choose an agent identifier, and never invent a producer or version.

Use `human:` for human-authored or human-confirmed content. Do not represent a person or process with the agent pattern.

See OKF section 7 for normative details.

## Links And Paths

Use standard Markdown links and explain the relationship in the surrounding prose. A link asserts a relationship; the prose explains whether that relationship means depends on, derives from, joins with, or something else.

Links and path-valued fields such as `resource`, `sources[].resource`, `computation`, `executor.resource`, and `attester.resource` accept:

- An absolute URL.
- A bundle-relative path beginning with `/`, which is preferred for internal concepts.
- A relative path resolved from the current file.

Unlike other path-valued fields, `sources[].resource` may also describe a population or scope that cannot be followed as a path, such as all queries in a named project.

Internal Markdown links must resolve when they are added or maintained. This is a local wiki-schema rule beyond base OKF, whose consumers still tolerate broken links. Record future concept ideas in a `Plan` or maintenance report instead of creating dead links.

See OKF sections 5.1, 6.1, and 6.2 for normative path and relationship semantics.

## Types And Field Rules

Use the smallest type that describes the concept itself. Begin with the shared page template, then add only the fields required or justified by its type rules:

| Type | Use | Additional field rules | Suggested body headings |
|---|---|---|---|
| `Note` | Provisional or general knowledge that does not need a narrower type | No additional fields | None; follow the material |
| `Reference` | Durable explanation, instruction, topic, entity, or procedure | Use `resource` when bound to one canonical asset; use `sources` when derived from evidence | None; follow the material |
| `Source Record` | A concept describing one source or evidence bundle | `resource` is required from creation | Summary |
| `Analysis` | Comparison, investigation, synthesis, or reasoned conclusion | Use `sources` when conclusions depend on evidence; use `snapshot: true` only for an explicit point-in-time synthesis | Conclusion, Reasoning |
| `Decision` | A settled choice and its reasoning | Use `sources` when evidence materially informed the choice | Decision, Rationale |
| `Goal` | A desired outcome or declared priority | Use `stale_after` only for a real review or expiry date | Outcome, Success Measures, Progress |
| `Plan` | An approach and actions intended to reach an outcome | Use `stale_after` only for a real review or expiry date | Approach, Actions, Progress |
| `Dataset` | A bounded dataset, its schema, meaning, and limits | `resource` is required before `stable` | Schema, Data, Examples |
| `Database` | A database or live data system, its access boundary, schema, and limits | `resource` is required before `stable` | Schema, Examples, Access, Limitations |
| `Attested Computation` | A sanctioned computation contract | Follow the conditional contract above | Computation |

Use `Source Record` rather than `Source` so the concept type is not confused with the `sources` provenance field. Existing or imported `Source` concepts remain valid unknown types and must be preserved.

Create new concepts with one of these types. Consumers and editors must still accept and preserve any unknown type found in a bundle.

The suggested headings and matching files under `templates/page-bodies/` are optional body structure. Add, rename, or remove headings to fit the concept. Do not duplicate shared frontmatter across body templates; compose the base page template with this table so schema changes remain centralized and optional placeholders do not encourage invented metadata.

## Tags

The approved [Tag Registry](local-settings.md#tag-registry) and each tag's meaning live in `local-settings.md`. Use only tags recorded there. If the registry is empty, use `tags: []`.

Record each approved registry entry as one Markdown bullet:

```markdown
- `<tag>`: <meaning and when to use it>
```

For example:

```markdown
- `customer-research`: Use for customer interviews, surveys, and related findings.
```

Use the registry tag's exact spelling in concept frontmatter. Prefer short lowercase kebab-case names for new tags unless the domain requires another stable form. The description should explain both what the tag means and when to use it.

Keep the registry small and driven by real retrieval needs. Prefer links and clear titles before adding a tag.

Propose a registry change before adding, renaming, merging, narrowing, or retiring a tag. The proposal should name the affected concepts and explain the retrieval benefit. Avoid synonyms, near-duplicates, and tags that merely repeat a type or status.
