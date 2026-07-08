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
- Useful business functions, industries or domains, evidence forms, recurring topics, work modes, and other classification tags.
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
### Local terminology and proposed tag vocabulary
### Sensitive-data rules
### Files to create
### Existing files to modify
### Defaults and assumptions
```

End with a direct approval question. Approval applies only to the files and changes explicitly shown. If the user qualifies the approval, revise the proposal or apply only the accepted subset.

As part of the proposal, suggest a small initial vocabulary—normally 8–15 tags—based on the user's description. Group suggestions by useful dimensions, give a short meaning for each, and omit dimensions that add no value. The user should be able to approve, remove, rename, or add tags before they are written to `config.md`.

## Ownership and write protocol

Raw evidence is human-controlled. You may propose and, after the normal approval cycle, add new files under `raw/`. Once a raw file exists, modifying, overwriting, renaming, moving, or deleting it requires separate, explicit human approval that names the file and operation. General approval to ingest or update the wiki does not authorize changing existing raw material. When possible, preserve the original and add a derived or corrected version as a new file.

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

## Knowledge pages

Every file under `wiki/` has two parts: YAML frontmatter containing consistent machine-readable metadata, and a Markdown body containing the actual knowledge, contextual links, and—when needed—a final citations section. Frontmatter describes the page; the body explains the subject.

Claims and quotes belong in the body. Attachments remain under `raw/`. Indexes, logs, tags, and statuses are not page types.

## Frontmatter

Every knowledge page contains the same eight keys. The block below is a schema illustration, not copy-ready YAML. Every value inside angle brackets is a placeholder that must be replaced from the actual page context. The listed choices are allowed values, not defaults or recommendations.

```yaml
---
type: <source | subject | note | synthesis | decision | plan>
title: <human-readable display name>
description: <one-sentence summary>
status: <fragment | draft | review | current | completed | archived>
tags: [<zero or more approved tags>]
resource: <absolute URL | relative path | null>
created: <ISO 8601 datetime with timezone>
updated: <ISO 8601 datetime with timezone>
---
```

Keep every key in every knowledge page. Do not comment out or omit empty fields. Filenames are lowercase kebab-case and unique within a flat `wiki/` directory.

### `type`

Choose the value that matches the page's purpose. No type is preferred by default.

| Value | Use it for | Example tags |
|---|---|---|
| `source` | One imported piece of evidence | `book`, `research-paper`, `image`, `dataset`, `customer-interview` |
| `subject` | An enduring topic or entity | `person`, `company`, `customer`, `concept`, `event`, `project` |
| `note` | Provisional authored thinking | `idea`, `hypothesis`, `question`, `observation` |
| `synthesis` | A conclusion reasoned across evidence | `literature-review`, `comparison`, `market-analysis` |
| `decision` | A choice and its rationale | `product`, `strategy`, `research-direction` |
| `plan` | Intended action and progress | `strategy`, `roadmap`, `experiment`, `project-plan` |

Adapt a new context through tags and body sections. Do not invent another universal type unless the six-value model has failed repeatedly in actual use and the user approves a schema change.

### `title` and `description`

`title` is the human-readable display name. `description` is one plain-text sentence suitable for indexes, previews, and search results.

### `status`

Choose the value from the page's actual lifecycle state. No status is a universal default.

- `fragment`: captured but not sufficiently developed.
- `draft`: coherent but incomplete.
- `review`: awaiting human approval.
- `current`: approved and presently authoritative.
- `completed`: a fixed record or plan whose intended process has concluded.
- `archived`: retained but no longer active or authoritative.

The usual progression is `fragment → draft → review → current`, but it is not mandatory. New evidence may return a current page to draft or review.

### `tags`

Tags provide broad, cross-cutting categorization and discovery. Use short, stable, lowercase kebab-case strings.

Tags may describe several independent dimensions:

- Business function, such as `operations`, `admin`, `technology`, `marketing`, `sales`, or `finance`.
- Industry or domain, such as `circular-economy`, `climate`, `health`, or `agriculture`.
- Evidence or document form, such as `customer-interview`, `research-paper`, `dataset`, or `meeting`.
- Topic or theme, such as `pricing`, `onboarding`, `retention`, or `supply-chain`.
- Work mode, such as `hypothesis`, `experiment`, or `analysis`.

These examples are prompts, not a fixed taxonomy. Infer an initial set from the user's actual context. Record the approved vocabulary in `config.md`, grouped by useful dimensions, with one-line meanings.

Reuse approved tags before creating new ones. Avoid synonyms and near-duplicates, do not use `type` or `status` values as redundant tags, and propose vocabulary additions before first use. Multiple tags are appropriate when a page genuinely crosses dimensions. Maintenance should flag unused tags, accidental synonyms, and tags that have become too broad.

### `resource`

`resource` identifies the primary underlying asset described by the page. It may be an absolute URL or a relative path such as `../raw/customer-orders.csv`. Use `null` when the page describes an abstract idea or knowledge product—such as a synthesis, business plan, strategy, or decision—rather than one specific underlying asset. Use claim-level citations for additional supporting files and sources.

### `created` and `updated`

Both use ISO 8601 datetimes with explicit timezone offsets. `created` never changes. Update `updated` only after a meaningful content or metadata change, not for formatting or link repair alone.

## Links

Relative Markdown links express specific relationships. Put them in explanatory prose so the connection remains understandable:

```markdown
This plan implements [Adopt self-serve onboarding](adopt-self-serve-onboarding.md)
and is supported by [Onboarding friction](onboarding-friction.md).
```

Link raw evidence relatively, for example `[interview transcript](../raw/customer-12/transcript.txt)`. Use portable Markdown links rather than tool-specific wiki-link syntax. Generic relationship lists do not belong in frontmatter by default; add structured relationship fields only when filtering or maintenance genuinely needs them.

## Citations

When a page makes claims sourced from external material, add numeric markers immediately after those claims and list the sources under `## Citations` as the final section:

```markdown
The market grew by 18% during 2025 [1].

## Citations

[1] [Market report](https://example.com/market-report)
[2] [Internal data-quality runbook](../raw/data-quality-runbook.pdf)
```

Follow these rules:

- Number sources by first appearance and reuse the same number when citing a source again.
- Use `[1, 2]` when several sources support one claim.
- Add precise locators when useful: `[2, p. 14]`, `[3, 01:12:30]`, or `[4, rows 20–35]`.
- Citation targets may be absolute URLs or relative paths.
- Prefer the closest preserved evidence: a raw file, internal document, dataset, or canonical external URL.
- Keep `## Citations` as the final section and omit it when no externally sourced claims appear.
- Never invent a source or missing citation details; mark unsupported claims explicitly.

The citation section provides claim-level provenance and may reference raw files. Links between wiki pages still serve a separate purpose: explaining semantic relationships.

## Page-body templates

Generate page bodies from the heading sequences below. Treat them as structured but elastic templates: keep the sections needed to preserve each page type's meaning, add sections when the material requires them, and remove irrelevant optional headings before promoting a page to `review`, `current`, or `completed`. Add removable HTML comments explaining what belongs under each heading. When citations are required, `## Citations` is always the final section regardless of page type.

### Source

- Summary
- Key claims or observations
- Evidence, including links and precise locators when available
- Limitations
- Connections

A source page is the bridge from preserved evidence to evolving interpretation. It does not replace the original.

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
- Do not modify, overwrite, rename, move, or delete an existing raw file without separate, file-specific human approval. Offer a new derived or corrected file as the default alternative.
- Do not write when approval is ambiguous.
- Apply configured sensitive-data constraints to reading, quoting, linking, retention, and generated content.
- Keep an intelligible trail when newer knowledge supersedes an approved page.

## Files to generate after approval

Create only what the approved proposal requires. The minimal default is:

1. Empty `raw/` and `wiki/` directories.
2. `config.md` containing the tailored purpose, scope, approved tag vocabulary with one-line meanings, citation contract, sensitive-data rules, ownership rules, universal schema, page-body guidance, and write protocol from this document.
3. `index.md` with a short usage note, `Start here`, `Topics`, and `Recent and active work` sections.
4. `log.md` with an append-only entry format beginning `## [ISO datetime] operation | Title`.
5. One agent instruction file using the convention recognized in the target environment, such as `AGENTS.md` or `CLAUDE.md`. Keep it thin: instruct the agent to read `config.md`, use `index.md` to orient, allow approved additions to `raw/` while requiring separate file-specific approval to change existing raw files, obtain approval before writes, verify changes, and append to `log.md`.

Do not create empty knowledge pages merely to demonstrate the schema. Do not add domain-specific folders when frontmatter, tags, and the index already express the distinction. Add local tag vocabulary and examples to `config.md` based on the user's actual context.

### `config.md` template

Generate `config.md` with this structure and fill every section from the approved setup conversation:

```markdown
# Wiki configuration

## Purpose
## Scope
## Outside scope
## Local terminology
## Frontmatter
### Type
### Title and description
### Status
### Tags and approved vocabulary
### Resource
### Created and updated
## Links
## Citations
## Ownership and approval
## Raw intake
## Sensitive information
## Local conventions
```

Include the complete approved rules from this bootstrap rather than references back to it. Under the approved tag vocabulary, group only useful dimensions and give each tag a one-line meaning.

### `index.md` template

```markdown
# Wiki index

Use this file for content-oriented navigation. Each entry links to a page, gives its one-sentence description, and shows status and update date.

## Start here

## Topics

## Recent and active work
```

Organize entries for the reader rather than mechanically by page type. An entry uses:

```markdown
- [Display title](wiki/page-name.md) — One-sentence description. (`status`, updated YYYY-MM-DD)
```

### `log.md` template

Append new entries at the top and do not rewrite history except to correct an objective formatting error:

```markdown
# Wiki log

## [YYYY-MM-DDTHH:MM:SS±HH:MM] operation | Short title

- **Approved by:** User
- **Files added:** None
- **Files updated:** None
- **Files archived:** None
- **Summary:** What changed and why.
- **Verification:** Metadata, links, citations, index coverage, and other checks performed.
```

### Agent-instruction template

Use the filename recognized by the target agent. Adapt names to the approved wiki location while preserving this behavior:

```markdown
# Wiki instructions

Read `config.md` before operating on this wiki. Use `index.md` to orient, inspect relevant pages under `wiki/`, and consult `raw/` when evidence must be verified.

Before changing files, present the proposed file-level changes and wait for explicit approval. Agents may add new files under `raw/` after normal approval. Modifying, overwriting, renaming, moving, or deleting an existing raw file requires separate, file-specific human approval. After approved changes, verify metadata, relative links, citations, resource paths, and index coverage, then append the operation to `log.md`.
```

## Verification after creation

Verify that:

- The approved directories and files exist and no unapproved file changed.
- `config.md` is complete enough to operate the wiki without this bootstrap document.
- `config.md` contains the approved initial tag vocabulary and its meanings.
- `config.md` defines the numeric citation format and distinguishes citations from links and frontmatter provenance.
- The agent instruction file points to `config.md` and preserves the approval boundary.
- `config.md` and the agent instruction file allow approved raw additions while protecting existing raw files from unapproved changes or removal.
- `raw/` and `wiki/` have no unnecessary mandatory subdirectories.
- The index and log are initialized.
- Example frontmatter uses only the six universal types and allowed statuses and includes all eight required keys.
- Relative paths are correct for the chosen placement.
- No unanswered setup prompts or placeholder decisions remain in operational files.

Report the created paths, the most important local conventions, and how the user should add their first source. Do not retain this bootstrap document in the initialized wiki.
