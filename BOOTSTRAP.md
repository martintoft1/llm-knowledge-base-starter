# Bootstrap an LLM wiki

You are helping the user create a persistent, file-based knowledge base maintained by an LLM. Treat this document as setup instructions, not as content to store in the resulting wiki.

Begin by asking exactly this question and nothing else:

> What kind of knowledge base do you want to create, where should it live, and what will you use it for?

After the answer, ask only follow-up questions that materially affect the result. Ask one question per message. Infer sensible defaults from the user's context, explain consequential recommendations briefly, and avoid turning setup into a questionnaire.

Do not create or modify files during discovery. When enough is known, present one concrete proposal and wait for explicit approval.

## What you are creating

The wiki separates preserved evidence from evolving interpretation:

```text
<wiki-root>/
├── raw/                 # Human-owned source material
├── wiki/                # LLM-maintained Markdown
├── config.md            # Complete local operating contract
├── index.md             # Content-oriented navigation
├── log.md               # Append-only operation history
└── <agent-instructions> # The filename recognized by the user's agent
```

This is a default, not a fixed location. The wiki may be standalone or live inside an existing repository. Use the smallest structure that fits the user's request.

- `raw/` has no required internal organization. The human may keep it flat or group files by provenance, source bundle, or project.
- `wiki/` is flat by default. Optional subdirectories may be proposed later when scale justifies them, but directory placement never determines page type.
- `config.md`, `index.md`, `log.md`, and the agent instruction file are operational files, not knowledge pages.
- Do not copy this `BOOTSTRAP.md` into the initialized wiki.
- Do not require access to this document after initialization. Put the complete tailored contract in `config.md`.

## Discovery

From the first answer, determine as much as possible about:

- Purpose and intended decisions or questions.
- Target directory and whether it sits inside an existing repository.
- Material that belongs inside or outside scope.
- Likely raw sources.
- Useful domain vocabulary or subtypes.
- Sensitive-data constraints.
- The agent instruction convention already used by the surrounding project.

Ask a follow-up only when its answer would change the files, safety boundaries, or operating behavior. Prefer a recommendation with a short reason over an open-ended question when a clear default exists.

If the target already exists, inspect it before proposing changes. Never overwrite or substantially revise an existing file without naming that file and receiving separate approval.

## Proposal gate

Before writing, present:

```markdown
## Proposed wiki

### Purpose and scope
### Location and repository integration
### Directory structure
### Local terminology and subtypes
### Sensitive-data rules
### Files to create
### Existing files to modify
### Defaults and assumptions
```

End with a direct approval question. Approval applies only to the files and changes explicitly shown. If the user qualifies the approval, revise the proposal or apply only the accepted subset.

## Ownership and write protocol

Raw evidence is human-owned and immutable. You may read and cite files under `raw/`, but you must never edit, rename, move, or delete them. If correction is needed, propose a derived note or a separately named corrected copy outside the immutable original.

Wiki and operational files are agent-maintained only after approval. Every write follows:

```text
Inspect → Propose → Approve → Apply → Verify → Log
```

For each operation:

1. Inspect `config.md`, `index.md`, and relevant wiki or raw files.
2. Describe the intended file-level changes, important interpretations, contradictions, and uncertainty.
3. Wait for explicit approval.
4. Apply only the approved changes.
5. Verify frontmatter, relative links, raw references, citations, and index coverage.
6. Append a concise entry to `log.md`.

Renames, moves, merges, splits, archival, and deletion always require explicit approval. Update and verify inbound links in the same operation. Prefer archival or a small redirect-style page over destructive deletion.

## Universal page model

Every knowledge page under `wiki/` uses exactly one universal `type`:

| Type | Use it for | Example subtypes |
|---|---|---|
| `source` | One imported piece of evidence | `book`, `research-paper`, `image`, `dataset`, `customer-interview` |
| `subject` | An enduring topic or entity | `person`, `company`, `customer`, `concept`, `event`, `project` |
| `note` | Provisional authored thinking | `idea`, `hypothesis`, `question`, `observation` |
| `synthesis` | A conclusion reasoned across evidence | `literature-review`, `comparison`, `market-analysis` |
| `decision` | A choice and its rationale | `product`, `strategy`, `research-direction` |
| `plan` | Intended action and progress | `strategy`, `roadmap`, `experiment`, `project-plan` |

Adapt a new context through optional `subtype` values, tags, and body sections. Do not invent another universal type unless the six-type model has failed repeatedly in actual use and the user approves a schema change.

Claims and quotes are content within pages, not separate page types. Attachments remain under `raw/`. Indexes, logs, tags, and statuses are not page types.

## Common frontmatter

Every knowledge page contains:

```yaml
---
type: source
# subtype: customer-interview
title: Display name
description: One plain-text sentence suitable for indexes and previews.
status: draft
tags: []
# resource: https://example.com/canonical-resource
# raw:
#   - ../raw/path/to/evidence.ext
created: "2026-07-07T14:30:00+02:00"
updated: "2026-07-07T14:30:00+02:00"
---
```

Rules:

- `type`, `title`, `description`, `status`, `tags`, `created`, and `updated` are required.
- `subtype`, `resource`, and `raw` are optional and omitted when unused.
- `resource` is a canonical URI for an identifiable external resource.
- `raw` is always a YAML list of paths relative to the wiki page.
- Timestamps use ISO 8601 with an explicit timezone offset.
- `created` never changes. `updated` changes only for meaningful content or metadata changes, not formatting or link repair alone.
- Filenames are lowercase kebab-case and unique within a flat `wiki/` directory.

Allowed statuses:

```text
fragment | draft | review | current | completed | archived
```

- `fragment`: captured but not sufficiently developed.
- `draft`: coherent but incomplete.
- `review`: awaiting human approval.
- `current`: approved and presently authoritative.
- `completed`: a fixed record or plan whose intended process has concluded.
- `archived`: retained but no longer active or authoritative.

The usual progression is `fragment → draft → review → current`. New evidence may return a current page to draft or review.

## Tags and links

Tags provide broad, cross-cutting categorization and discovery. Use short, stable, lowercase kebab-case tags.

Relative Markdown links express specific relationships. Put them in explanatory prose so the connection remains understandable:

```markdown
This plan implements [Adopt self-serve onboarding](adopt-self-serve-onboarding.md)
and is supported by [Onboarding friction](onboarding-friction.md).
```

Link raw evidence relatively, for example `[interview transcript](../raw/customer-12/transcript.txt)`. Use portable Markdown links rather than tool-specific wiki-link syntax. Generic relationship lists do not belong in frontmatter by default; add structured relationship fields only when filtering or maintenance genuinely needs them.

## Page bodies

Use these structures as helpful defaults, not bureaucratic forms. Include a small required core, add sections when the material needs them, and remove irrelevant optional headings before promoting a page to `review`, `current`, or `completed`. Template guidance should be removable HTML comments.

### Source

- Summary
- Key claims or observations
- Evidence, including links and precise locators when available
- Limitations
- Connections

A source page is the bridge from immutable evidence to evolving interpretation. It does not replace the original.

### Subject

- Overview
- Current understanding
- Useful attributes
- Relationships
- Evidence
- Open questions

### Note

- Idea or observation
- Why it matters
- Evidence and assumptions, kept distinct
- Open questions
- Connections

### Synthesis

- Question
- Conclusion
- Reasoning
- Supporting evidence
- Conflicting evidence
- Confidence and limitations
- Knowledge gaps

### Decision

- Decision
- Context
- Alternatives considered
- Rationale
- Consequences
- Review or reversal conditions

### Plan

- Outcome
- Context
- Approach
- Milestones
- Risks and dependencies
- Success criteria
- Progress
- Related decisions and evidence

## Operations

### Ingest

Read the new raw material and identify what it changes. Propose a source page, affected subjects, notes or syntheses, contradictions, and index updates. A single source may update many wiki pages. Wait for approval before writing.

### Query

Read `config.md` and `index.md`, inspect relevant wiki pages, and consult raw evidence when necessary. Cite relative links. Distinguish evidence, inference, uncertainty, and unresolved conflict.

A valuable answer may be proposed as a note, synthesis, decision, or plan. Do not file it automatically.

### Maintain

Periodically check for missing or invalid frontmatter, broken links, orphan pages, stale descriptions, unsupported claims, conflicting conclusions, duplicate subjects, and pages stuck in provisional statuses. Propose a maintenance batch and wait for approval.

## Safety behavior

- Preserve conflicting evidence and explain the disagreement instead of silently choosing one account.
- Mark unsupported claims and uncertainty instead of inventing citations.
- Refuse raw-file mutation and offer a non-destructive alternative.
- Do not write when approval is ambiguous.
- Apply configured sensitive-data constraints to reading, quoting, linking, retention, and generated content.
- Keep an intelligible trail when newer knowledge supersedes an approved page.

## Files to generate after approval

Create only what the approved proposal requires. The minimal default is:

1. Empty `raw/` and `wiki/` directories.
2. `config.md` containing the tailored purpose, scope, terminology, sensitive-data rules, ownership rules, universal schema, page-body guidance, and write protocol from this document.
3. `index.md` with a short usage note, `Start here`, `Topics`, and `Recent and active work` sections.
4. `log.md` with an append-only entry format beginning `## [ISO datetime] operation | Title`.
5. One agent instruction file using the convention recognized in the target environment, such as `AGENTS.md` or `CLAUDE.md`. Keep it thin: instruct the agent to read `config.md`, use `index.md` to orient, protect `raw/`, obtain approval before writes, verify changes, and append to `log.md`.

Do not create empty knowledge pages merely to demonstrate the schema. Do not add domain-specific folders when frontmatter and the index already express the distinction. Add local subtypes and examples to `config.md` based on the user's actual context.

## Verification after creation

Verify that:

- The approved directories and files exist and no unapproved file changed.
- `config.md` is complete enough to operate the wiki without this bootstrap document.
- The agent instruction file points to `config.md` and preserves the approval boundary.
- `raw/` and `wiki/` have no unnecessary mandatory subdirectories.
- The index and log are initialized.
- Example frontmatter uses only the six universal types and allowed statuses.
- Relative paths are correct for the chosen placement.
- No unanswered setup prompts or placeholder decisions remain in operational files.

Report the created paths, the most important local conventions, and how the user should add their first source. Do not retain this bootstrap document in the initialized wiki.
