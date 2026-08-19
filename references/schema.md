# Local OKF Profile

This file defines this starter kit's complete local OKF profile: bundle structure, required and optional metadata, actor identifiers, links and paths, local types and field profiles, and tag governance. It is the routine source of truth for reusable local structure and metadata rules. Settings that vary between knowledge bases live in [`local-settings.md`](local-settings.md).

The pinned [`okf/v0.2/SPEC.md`](okf/v0.2/SPEC.md) remains authoritative. Consult it when this profile does not cover a field or edge case, when resolving ambiguity, during a formal base-OKF audit, or when changing the schema or OKF version. Do not use this profile to override the specification.

## Bundle Files

Every file inside `wiki/` must be UTF-8 Markdown with a `.md` filename. This is a local restriction even where base OKF permits other support files. Non-Markdown evidence, computation code, and other support assets are not bundle members. Keep retained evidence under `raw/` or point to an external, non-secret resource.

## Frontmatter

### Required Local Fields

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
- `status` is `draft`, `stable`, or `deprecated`. A draft may be incomplete; stable content is ready for consumption and meets its local profile; deprecated content is retained for links and history but is no longer current.
- `tags` is a YAML list, which may be empty.
- `generated` contains a non-empty `by` actor and an ISO 8601 `at` datetime. Change `generated.at` only after a meaningful content or metadata change.

`description` is optional for early drafts and required before a concept becomes `stable`. Keep it to one sentence. This rule is conditional, so the draft template omits the field.

### Optional And Conditional Fields

Optional fields carry real meaning when present. Omit them when they do not apply; never add empty mappings, empty lists, `null`, or invented values merely to complete a template.

#### Resource Binding

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
    title: Customer policy
    author: human:owner
    last_modified: 2026-08-01
```

A source may also carry:

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

#### Freshness: `stale_after`

`stale_after` is the absolute date on which the concept becomes stale. Use it only when there is a defensible expiry, review, or validity date.

```yaml
stale_after: 2026-12-31
```

A concept is stale when `today >= stale_after`. Omit the field when no meaningful date is known; do not guess one. See OKF section 5.5 for normative details.

#### Attested Computation

Every Attested Computation requires `runtime`, regardless of status. Before its status may become `stable`, it also requires:

- A non-empty `parameters` list whose entries contain `name`, `type`, and `required`. Under this stricter profile, a zero-input computation remains `draft`.
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
- People: `human:<id>`, such as `human:owner`.
- Automated processes: `process:<id>`, such as `process:nightly-refresh`.

Use `human:` for human-authored or human-confirmed content because OKF trust tiers depend on that prefix. Do not represent a person or process with the agent pattern.

See OKF section 7 for the normative actor convention. Never invent provenance, verification, usage, access, or attestation. Preserve unknown fields when editing a concept; unknown fields and types do not make an OKF concept invalid.

## Links And Paths

Use standard Markdown links and explain the relationship in the surrounding prose. A link asserts a relationship; the prose explains whether that relationship means depends on, derives from, joins with, or something else.

Links and path-valued fields such as `resource`, `sources[].resource`, `computation`, `executor.resource`, and `attester.resource` accept:

- An absolute URL.
- A bundle-relative path beginning with `/`, which is preferred for internal concepts.
- A relative path resolved from the current file.

Unlike other path-valued fields, `sources[].resource` may also describe a population or scope that cannot be followed as a path, such as all queries in a named project.

Report broken links, but do not treat them as an OKF conformance failure. Preserve links that intentionally point to knowledge not yet written.

See OKF sections 5.1, 6.1, and 6.2 for normative path and relationship semantics.

## Local Types And Field Profiles

Use the smallest type that describes the concept itself. Begin with the shared page template, then add only the fields required or justified by its profile:

| Type | Use | Additional field profile | Suggested body headings |
|---|---|---|---|
| `Note` | Provisional or general knowledge that does not need a narrower type | No additional fields | None; follow the material |
| `Reference` | Durable explanation, instruction, topic, entity, or procedure | Use `resource` when bound to one canonical asset; use `sources` when derived from evidence | None; follow the material |
| `Source Record` | A concept describing one source or evidence bundle | `resource` is required from creation | Summary |
| `Analysis` | Comparison, investigation, synthesis, or reasoned conclusion | Use `sources` when conclusions depend on evidence | Conclusion, Reasoning |
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

The approved tag registry and each tag's meaning live in [`local-settings.md`](local-settings.md). Use only tags recorded there. If the registry is empty, use `tags: []`.

Keep the registry small and driven by real retrieval needs. Prefer links and clear titles before adding a tag.

Propose a registry change before adding, renaming, merging, narrowing, or retiring a tag. The proposal should name the affected concepts and explain the retrieval benefit. Avoid synonyms, near-duplicates, and tags that merely repeat a type or status.
