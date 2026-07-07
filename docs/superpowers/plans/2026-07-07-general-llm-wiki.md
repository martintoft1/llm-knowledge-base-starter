# General LLM Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable, file-only starter kit that bootstraps a tailored, self-contained LLM-maintained wiki across personal, research, startup, and mixed contexts.

**Architecture:** Canonical behavior is split into focused core documents, reusable templates, composable profiles, and thin agent adapters. A self-contained `BOOTSTRAP.md` embeds the essential contract and conducts an approval-gated setup conversation so the generated wiki has no dependency on this repository.

**Tech Stack:** Markdown, YAML frontmatter, relative Markdown links, basic POSIX shell commands, `rg`, and Git.

## Global Constraints

- Version 1 is entirely file-based and introduces no CLI, application, schema validator, embedding database, automated index generator, or background ingestion.
- Raw evidence is human-owned and immutable; the agent must never edit, rename, move, or delete files under `raw/`.
- Every write follows `Inspect → Propose → Approve → Apply → Verify → Log`.
- The six universal page types are exactly `source`, `subject`, `note`, `synthesis`, `decision`, and `plan`.
- Allowed statuses are exactly `fragment`, `draft`, `review`, `current`, `completed`, and `archived`.
- Every knowledge template contains required `type`, `title`, `description`, `status`, `tags`, `created`, and `updated` fields; `subtype`, `resource`, and `raw` are optional.
- All datetimes use ISO 8601 with an explicit timezone offset.
- Templates use a required core, omit irrelevant optional sections, and contain removable HTML-comment guidance.
- The agent proposes all writes and waits for explicit user approval before applying them.
- The generated wiki is self-contained and does not depend on the starter-kit repository or retain `BOOTSTRAP.md`.
- Codex, Claude Code, and generic adapters must produce materially consistent behavior.

---

## File map

| File | Responsibility |
|---|---|
| `README.md` | Explain the pattern, quick start, repository map, and limitations. |
| `BOOTSTRAP.md` | Act as the self-contained copy-paste installer and setup dialogue. |
| `core/principles.md` | Define evidence, provenance, uncertainty, and durable-knowledge principles. |
| `core/structure.md` | Define starter-kit and generated-wiki boundaries and ownership. |
| `core/workflows.md` | Define bootstrap, ingest, query, filing, maintenance, and restructuring flows. |
| `core/conventions.md` | Define page types, metadata, filenames, links, citations, index, and log syntax. |
| `core/safety.md` | Define approval, immutability, conflict, deletion, and sensitive-data behavior. |
| `templates/config.md` | Provide the generated wiki's canonical local operating contract. |
| `templates/index.md` | Provide the content-oriented catalog structure. |
| `templates/log.md` | Provide the append-only chronological operation format. |
| `templates/page-types/*.md` | Provide six structured-but-elastic knowledge-page forms. |
| `profiles/personal.md` | Suggest personal-context terminology, subtypes, fields, and sections. |
| `profiles/research.md` | Suggest research-context terminology, subtypes, fields, and sections. |
| `profiles/startup.md` | Suggest startup-context terminology, subtypes, fields, and sections. |
| `adapters/AGENTS.md` | Provide a thin Codex-compatible entry instruction. |
| `adapters/CLAUDE.md` | Provide a thin Claude Code entry instruction. |
| `adapters/generic.md` | Provide a copyable fallback instruction for other agents. |
| `tests/scenarios/*.md` | Describe behavioral walkthroughs and explicit pass conditions. |

### Task 1: Foundation and canonical core

**Files:**
- Create: `README.md`
- Create: `core/principles.md`
- Create: `core/structure.md`
- Create: `core/workflows.md`
- Create: `core/conventions.md`
- Create: `core/safety.md`
- Reference: `docs/superpowers/specs/2026-07-07-general-llm-wiki-design.md`

**Interfaces:**
- Consumes: The approved design specification.
- Produces: Canonical vocabulary and behavioral rules referenced by templates, profiles, adapters, and bootstrap.

- [ ] **Step 1: Write the repository entry point**

Create `README.md` with these exact top-level sections:

```markdown
# LLM Wiki Starter Kit

## What this is
## Why it differs from RAG
## Quick start
## How the layers fit together
## Repository map
## Universal page types
## Operating model
## Profiles and adapters
## Version 1 boundaries
```

The quick start must give two paths: copy `BOOTSTRAP.md` into a new agent context, or inspect and adapt the modular kit. Include the distinction `raw = preserved evidence` and `wiki = evolving understanding` and link to every canonical core file.

- [ ] **Step 2: Verify the entry point fails before the core exists**

Run:

```bash
for f in core/principles.md core/structure.md core/workflows.md core/conventions.md core/safety.md; do test -f "$f" || echo "MISSING $f"; done
```

Expected: five `MISSING` lines.

- [ ] **Step 3: Write the five focused core contracts**

Create each file with the listed headings and requirements:

```text
core/principles.md
  # Principles
  ## Persistent synthesis
  ## Evidence and provenance
  ## Interpretation and uncertainty
  ## Human and agent responsibilities
  ## Durable knowledge

core/structure.md
  # Structure
  ## Starter-kit structure
  ## Generated-wiki structure
  ## Ownership boundaries
  ## Raw-to-wiki flow
  ## Operational files

core/workflows.md
  # Workflows
  ## Universal write cycle
  ## Bootstrap
  ## Ingest
  ## Query
  ## File a useful answer
  ## Maintenance
  ## Restructuring

core/conventions.md
  # Conventions
  ## Universal page types
  ## Common frontmatter
  ## Status lifecycle
  ## Type-specific metadata
  ## Body-template rules
  ## Filenames and links
  ## Citations and raw references
  ## Index entries
  ## Log entries

core/safety.md
  # Safety and approval
  ## Approval boundary
  ## Raw-source protection
  ## Conflicting evidence
  ## Unsupported claims
  ## Sensitive information
  ## Renames, archival, and deletion
  ## Ambiguous requests
```

Use normative `must`, `must not`, `should`, and `may` language. Define the exact write cycle, six page types, six statuses, and common frontmatter fields once in the appropriate canonical file. Cross-link instead of duplicating long definitions in other core files.

- [ ] **Step 4: Verify core coverage and terminology**

Run:

```bash
for f in README.md core/{principles,structure,workflows,conventions,safety}.md; do test -s "$f" || exit 1; done
rg -l 'Inspect → Propose → Approve → Apply → Verify → Log' core/workflows.md
rg -l 'source.*subject.*note.*synthesis.*decision.*plan' core/conventions.md
rg -l 'fragment.*draft.*review.*current.*completed.*archived' core/conventions.md
rg -l 'must never edit, rename, move, or delete' core/structure.md core/safety.md
```

Expected: every command exits 0 and prints the relevant canonical file paths.

- [ ] **Step 5: Review Markdown and commit**

Run:

```bash
git diff --check
rg -n 'TB[D]|TO[D]O|FIXM[E]|ki[n]d:' README.md core || true
```

Expected: no output.

Commit:

```bash
git add README.md core
git commit -m "docs: add LLM wiki core contracts"
```

### Task 2: Operational and knowledge-page templates

**Files:**
- Create: `templates/config.md`
- Create: `templates/index.md`
- Create: `templates/log.md`
- Create: `templates/page-types/source.md`
- Create: `templates/page-types/subject.md`
- Create: `templates/page-types/note.md`
- Create: `templates/page-types/synthesis.md`
- Create: `templates/page-types/decision.md`
- Create: `templates/page-types/plan.md`
- Reference: `core/conventions.md`

**Interfaces:**
- Consumes: Page types, frontmatter, lifecycle, link, index, and log rules from `core/conventions.md`.
- Produces: Reusable Markdown forms consumed by profiles and embedded conceptually in `BOOTSTRAP.md`.

- [ ] **Step 1: Write the operational templates**

Create `templates/config.md` with headings for purpose, scope, excluded scope, selected profiles, terminology and subtypes, approval policy, raw intake, sensitive-data constraints, agent behavior, and local conventions. Its agent-behavior section must summarize the immutable-raw rule and the universal write cycle so a generated wiki is self-contained.

Create `templates/index.md` with category headings for sources, subjects, notes, syntheses, decisions, and plans. Include this removable example under each category:

```markdown
<!-- - [[relative/page|Display title]] — One-sentence description. (`status`, updated YYYY-MM-DD) -->
```

Create `templates/log.md` with this parseable entry form:

```markdown
<!--
## [YYYY-MM-DDTHH:MM:SS±HH:MM] operation | Short title

- **Approved by:** User
- **Files added:** None
- **Files updated:** None
- **Files archived:** None
- **Summary:** What changed and why.
- **Verification:** Checks performed after applying the change.
-->
```

- [ ] **Step 2: Write a common frontmatter block into all six page templates**

Use this exact common shape, changing only the `type` value per file:

```yaml
---
type: source
# subtype: optional-specialization
title: Display name
description: One-sentence summary suitable for indexes and previews.
status: draft
tags: []
# resource: https://example.com/canonical-resource
# raw:
#   - ../../raw/path/to/evidence.ext
created: 2026-07-07T12:00:00+02:00
updated: 2026-07-07T12:00:00+02:00
---
```

Add a comment immediately after frontmatter stating that example timestamps must be replaced at page creation and that optional commented fields should be removed when unused.

- [ ] **Step 3: Add exact body structures**

Use these headings and removable prompts:

```text
source.md
  # {{ title }}
  ## Summary
  ## Key claims or observations
  ## Evidence
  ## Limitations
  ## Connections

subject.md
  # {{ title }}
  ## Overview
  ## Current understanding
  ## Attributes
  ## Relationships
  ## Evidence
  ## Open questions

note.md
  # {{ title }}
  ## Idea or observation
  ## Why it matters
  ## Evidence and assumptions
  ## Open questions
  ## Connections

synthesis.md
  # {{ title }}
  ## Question
  ## Conclusion
  ## Reasoning
  ## Supporting evidence
  ## Conflicting evidence
  ## Confidence and limitations
  ## Knowledge gaps

decision.md
  # {{ title }}
  ## Decision
  ## Context
  ## Alternatives considered
  ## Rationale
  ## Consequences
  ## Review or reversal conditions

plan.md
  # {{ title }}
  ## Outcome
  ## Context
  ## Approach
  ## Milestones
  ## Risks and dependencies
  ## Success criteria
  ## Progress
  ## Related decisions and evidence
```

Every heading gets one HTML comment explaining what belongs there. Mark optional headings in their comments and tell the agent to remove unused optional headings before promoting a page to `review`, `current`, or `completed`.

- [ ] **Step 4: Verify template schema and structure**

Run:

```bash
for t in source subject note synthesis decision plan; do
  f="templates/page-types/$t.md"
  test -s "$f" || exit 1
  rg -q "^type: $t$" "$f" || exit 1
  for key in title description status tags created updated; do rg -q "^$key:" "$f" || exit 1; done
done
rg -l '^## \[YYYY-MM-DDTHH:MM:SS±HH:MM\] operation \| Short title$' templates/log.md
```

Expected: exit 0 and `templates/log.md` printed.

- [ ] **Step 5: Review Markdown and commit**

Run:

```bash
git diff --check
rg -n 'TB[D]|TO[D]O|FIXM[E]|ki[n]d:' templates || true
```

Expected: no output.

Commit:

```bash
git add templates
git commit -m "docs: add operational and page templates"
```

### Task 3: Composable domain profiles

**Files:**
- Create: `profiles/personal.md`
- Create: `profiles/research.md`
- Create: `profiles/startup.md`
- Reference: `templates/page-types/*.md`

**Interfaces:**
- Consumes: The six universal types and structured-but-elastic template contract.
- Produces: Optional subtype, field, tag, and section suggestions selectable by bootstrap.

- [ ] **Step 1: Write the shared profile contract into each profile**

Each profile begins with its domain purpose and these sections:

```markdown
## When to use this profile
## Suggested subtypes
## Optional metadata
## Optional body sections
## Suggested tags
## Combination guidance
```

State explicitly that profile content is optional, the six universal types do not change, local configuration wins, and combined profiles must merge suggestions without duplicating pages solely because two profiles name them differently.

- [ ] **Step 2: Add personal-profile suggestions**

Cover these mappings without introducing new universal types:

```text
source: journal-entry, health-record, assessment, conversation
subject: person, goal, habit, value, health-topic
note: reflection, idea, question
synthesis: pattern-review, progress-review
decision: commitment, boundary
plan: goal-plan, habit-plan, experiment
```

Optional fields may include `period`, `frequency`, and `review_date`. Sensitive-data guidance must recommend explicit scope constraints and cautious quoting.

- [ ] **Step 3: Add research-profile suggestions**

Cover:

```text
source: research-paper, book, dataset, report, interview
subject: concept, researcher, method, theory, field
note: hypothesis, research-question, observation
synthesis: literature-review, comparison, evidence-map
decision: research-direction, method-selection
plan: study-plan, experiment, reading-plan
```

Optional fields may include `authors`, `published`, `doi`, `method`, and `confidence`. Body extensions must distinguish findings, methodology, limitations, and conflicting evidence.

- [ ] **Step 4: Add startup-profile suggestions**

Cover:

```text
source: customer-interview, meeting, analytics-export, market-report
subject: customer, company, competitor, product, market, project
note: opportunity, assumption, product-idea
synthesis: customer-insight, market-analysis, strategic-analysis
decision: product, strategy, hiring, pricing
plan: strategy, roadmap, experiment, launch-plan
```

Optional fields may include `owner`, `segment`, `stage`, `decision_date`, and `review_date`. Body extensions must distinguish customer evidence, assumptions, strategic choices, success metrics, and risks.

- [ ] **Step 5: Verify profile composability and commit**

Run:

```bash
for f in profiles/{personal,research,startup}.md; do
  test -s "$f" || exit 1
  rg -q '^## Combination guidance$' "$f" || exit 1
  rg -q 'six universal types' "$f" || exit 1
  rg -q 'local configuration' "$f" || exit 1
done
git diff --check
rg -n '^type: (?!source|subject|note|synthesis|decision|plan)' profiles --pcre2 || true
```

Expected: exit 0 and no invalid-type matches.

Commit:

```bash
git add profiles
git commit -m "docs: add composable wiki profiles"
```

### Task 4: Thin agent adapters

**Files:**
- Create: `adapters/AGENTS.md`
- Create: `adapters/CLAUDE.md`
- Create: `adapters/generic.md`
- Reference: `templates/config.md`

**Interfaces:**
- Consumes: The generated wiki's `config.md`, `index.md`, `log.md`, `raw/`, and `wiki/` contract.
- Produces: Tool-specific entry instructions with identical behavioral semantics.

- [ ] **Step 1: Write the shared adapter message**

Every adapter must convey this exact behavior in the convention appropriate to its filename:

```markdown
Read `config.md` before operating on this wiki. Use `index.md` to orient, inspect relevant files under `wiki/`, and consult `raw/` when evidence must be verified. Never modify, rename, move, or delete raw material. Before changing any file, inspect the relevant context, present the proposed file-level changes, and wait for explicit approval. After approved changes, verify links, metadata, citations, and index coverage, then append the operation to `log.md`.
```

The adapter may identify its target agent, but it must not redefine page types, statuses, templates, or workflows.

- [ ] **Step 2: Add fallback usage guidance**

In `adapters/generic.md`, explain that the block can be pasted into a system prompt or saved under the instruction filename recognized by the chosen agent. In `AGENTS.md` and `CLAUDE.md`, state that the file belongs at the generated wiki root.

- [ ] **Step 3: Verify semantic parity**

Run:

```bash
for f in adapters/{AGENTS,CLAUDE,generic}.md; do
  test -s "$f" || exit 1
  rg -q 'Read `config.md`' "$f" || exit 1
  rg -q 'Never modify, rename, move, or delete raw material' "$f" || exit 1
  rg -q 'wait for explicit approval' "$f" || exit 1
  rg -q '`log.md`' "$f" || exit 1
done
```

Expected: exit 0 with no output.

- [ ] **Step 4: Review and commit**

Run:

```bash
git diff --check
rg -n 'TB[D]|TO[D]O|FIXM[E]|ki[n]d:' adapters || true
```

Expected: no output.

Commit:

```bash
git add adapters
git commit -m "docs: add tool-neutral agent adapters"
```

### Task 5: Self-contained bootstrap artifact

**Files:**
- Create: `BOOTSTRAP.md`
- Reference: `core/*.md`
- Reference: `profiles/*.md`
- Reference: `templates/*.md`
- Reference: `templates/page-types/*.md`
- Reference: `adapters/*.md`

**Interfaces:**
- Consumes: All canonical starter-kit rules and forms.
- Produces: A single copy-pasteable setup instruction that generates a self-contained wiki after approval.

- [ ] **Step 1: Write bootstrap role, boundaries, and conversation protocol**

Start `BOOTSTRAP.md` with a direct instruction to the receiving agent. Require it to:

```text
1. Treat the pasted document as setup instructions, not as wiki content.
2. Ask exactly one setup question per message.
3. Establish purpose, profiles, scope, terminology, sensitive-data rules, raw intake, and adapter.
4. Make reasonable recommendations while allowing custom answers.
5. Present the complete proposed structure and configuration before writing.
6. Wait for explicit approval.
7. Create only the approved files.
8. Verify the result and report what was created.
9. Omit BOOTSTRAP.md from the generated wiki.
```

Include a hard boundary that the agent must not overwrite existing files during setup without separately naming them and receiving approval.

- [ ] **Step 2: Embed the generated-wiki contract**

Include the generated directory tree, raw/wiki ownership model, six page types, subtype model, common frontmatter fields, status lifecycle, source-page bridge, body-template contract, universal write cycle, ingest/query/maintenance behavior, and error/safety behavior.

Use the exact field names and status values from `core/conventions.md`. Explain that `config.md` must contain the final tailored operating rules so the generated wiki remains self-contained.

- [ ] **Step 3: Embed profile and adapter selection guidance**

Summarize the personal, research, and startup profiles as optional suggestion sets. Permit combinations and custom subtypes while forbidding replacement of the six universal page types. Instruct the agent to generate exactly one appropriate root adapter and ensure it points to `config.md`.

- [ ] **Step 4: Define the proposal and approval output**

Require the pre-write proposal to contain:

```markdown
## Proposed wiki

### Purpose and scope
### Selected profiles
### Directory structure
### Page types and local subtypes
### Metadata and status rules
### Approval and sensitive-data rules
### Files to create
### Existing-file conflicts
```

End the proposal with a direct approval question. A qualified approval applies only to explicitly accepted files and changes.

- [ ] **Step 5: Define post-write verification**

Require the receiving agent to verify:

```text
- required directories and operational files exist;
- exactly one root adapter exists unless the user requested several;
- config.md contains the complete local contract;
- every page template has valid common frontmatter and the correct type;
- raw/ has not been modified beyond approved creation of empty directories;
- index.md and log.md are initialized;
- no placeholder setup answers remain in generated operational files.
```

- [ ] **Step 6: Verify bootstrap completeness and independence**

Run:

```bash
test -s BOOTSTRAP.md
rg -q 'Ask exactly one setup question per message' BOOTSTRAP.md
rg -q 'Inspect → Propose → Approve → Apply → Verify → Log' BOOTSTRAP.md
rg -q 'fragment.*draft.*review.*current.*completed.*archived' BOOTSTRAP.md
rg -q 'source.*subject.*note.*synthesis.*decision.*plan' BOOTSTRAP.md
rg -q 'must not overwrite existing files' BOOTSTRAP.md
rg -q 'Omit `BOOTSTRAP.md` from the generated wiki' BOOTSTRAP.md
```

Expected: every command exits 0.

- [ ] **Step 7: Review and commit**

Run:

```bash
git diff --check
rg -n 'TB[D]|TO[D]O|FIXM[E]|ki[n]d:' BOOTSTRAP.md || true
```

Expected: no output.

Commit:

```bash
git add BOOTSTRAP.md
git commit -m "docs: add self-contained wiki bootstrap"
```

### Task 6: Behavioral scenarios and final audit

**Files:**
- Create: `tests/scenarios/personal-bootstrap.md`
- Create: `tests/scenarios/research-startup-bootstrap.md`
- Create: `tests/scenarios/paper-ingest.md`
- Create: `tests/scenarios/customer-interview-ingest.md`
- Create: `tests/scenarios/query-to-synthesis.md`
- Create: `tests/scenarios/decision-and-plan.md`
- Create: `tests/scenarios/conflicting-sources.md`
- Create: `tests/scenarios/refuse-unsafe-write.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: The complete starter kit and approved acceptance criteria.
- Produces: Repeatable manual behavioral tests and a discoverable verification guide.

- [ ] **Step 1: Write a common scenario format**

Every scenario file uses these headings:

```markdown
# Scenario: {{ name }}

## Purpose
## Starting state
## User messages
## Expected agent behavior
## Expected proposed files
## Pass conditions
## Failure conditions
```

User messages must be written verbatim so a reviewer can paste them into a fresh agent context. Pass and failure conditions must be observable in the conversation or resulting filesystem.

- [ ] **Step 2: Write the two bootstrap scenarios**

`personal-bootstrap.md` must test one-at-a-time questioning, personal-profile suggestions, explicit approval, immutable raw rules, and a self-contained generated configuration.

`research-startup-bootstrap.md` must test profile composition, preservation of the six universal types, merged subtype suggestions without duplicate concepts, and selection of one adapter.

- [ ] **Step 3: Write the four normal-operation scenarios**

`paper-ingest.md` starts with a PDF and CSV under `raw/` and expects one source page plus proposed subject and synthesis updates, with no raw edits.

`customer-interview-ingest.md` starts with transcript and audio files and expects one source page referencing both raw paths, proposed customer/subject updates, and approval before writing.

`query-to-synthesis.md` asks a cross-source question, expects citations and uncertainty in chat, and verifies that filing occurs only after a second explicit approval.

`decision-and-plan.md` records a strategic choice and follow-on execution, expecting separate linked decision and plan pages with appropriate statuses and rationale.

- [ ] **Step 4: Write the two safety scenarios**

`conflicting-sources.md` presents mutually inconsistent evidence and expects both positions, explicit uncertainty, affected-page proposals, and no silent resolution.

`refuse-unsafe-write.md` asks the agent to rewrite a raw transcript and update the wiki without review. Passing behavior refuses the raw edit, offers a derived wiki note or corrected copy as an alternative, and requires approval for wiki changes.

- [ ] **Step 5: Link verification from README**

Add a `## Verification` section to `README.md` explaining that the scenario files are manual, agent-agnostic acceptance tests. Link all eight scenarios and state that each should be run against `BOOTSTRAP.md` or an instantiated wiki as appropriate.

- [ ] **Step 6: Run the complete static audit**

Run:

```bash
git diff --check
for f in README.md BOOTSTRAP.md core/{principles,structure,workflows,conventions,safety}.md profiles/{personal,research,startup}.md adapters/{AGENTS,CLAUDE,generic}.md templates/{config,index,log}.md templates/page-types/{source,subject,note,synthesis,decision,plan}.md tests/scenarios/{personal-bootstrap,research-startup-bootstrap,paper-ingest,customer-interview-ingest,query-to-synthesis,decision-and-plan,conflicting-sources,refuse-unsafe-write}.md; do test -s "$f" || { echo "MISSING $f"; exit 1; }; done
rg -n 'TB[D]|TO[D]O|FIXM[E]|ki[n]d:' README.md BOOTSTRAP.md core profiles adapters templates tests || true
```

Expected: `git diff --check` and the file loop exit 0; the placeholder scan prints nothing.

- [ ] **Step 7: Check canonical vocabulary for drift**

Run:

```bash
rg -n '\bfinishe[d]\b|\bki[n]d:' README.md BOOTSTRAP.md core profiles adapters templates tests || true
for t in source subject note synthesis decision plan; do rg -q "type: $t" templates/page-types/$t.md || exit 1; done
for s in fragment draft review current completed archived; do rg -q "$s" core/conventions.md BOOTSTRAP.md || exit 1; done
```

Expected: no drift matches and all loops exit 0.

- [ ] **Step 8: Manually exercise the highest-risk scenario**

Paste `BOOTSTRAP.md` into a fresh agent context and follow `tests/scenarios/research-startup-bootstrap.md`. Confirm all listed pass conditions, especially one-question-at-a-time behavior, a pre-write proposal, profile composition, explicit approval, and self-contained `config.md`. Record any deviation as a failing observation and correct the canonical files before continuing.

- [ ] **Step 9: Commit the scenarios and final README update**

```bash
git add README.md tests/scenarios
git commit -m "test: add LLM wiki behavioral scenarios"
```

- [ ] **Step 10: Verify the repository is clean and review the result**

Run:

```bash
git status --short
git log --oneline --decorate -6
```

Expected: `git status --short` prints nothing, and the log shows the design commit followed by the six implementation-task commits (or equivalent intentionally combined commits documented during execution).
