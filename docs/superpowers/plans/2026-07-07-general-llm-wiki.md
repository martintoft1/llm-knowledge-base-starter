# General LLM Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and dogfood a minimal, portable initializer for LLM-maintained wikis.

**Architecture:** `BOOTSTRAP.md` contains the complete setup and operating contract. `templates/` provides inspectable examples of the generated files, while `README.md` explains the two-minute workflow. No separate core, profile, adapter, or scenario framework is introduced.

**Tech Stack:** Markdown, YAML frontmatter, relative Markdown links, basic shell checks, and Git.

## Constraints

- Raw evidence is immutable and human-owned.
- Wiki pages use six universal types and six controlled statuses.
- Tags categorize broadly; relative Markdown links explain specific relationships.
- Initialization proposes roughly 8–15 context-relevant tags across useful dimensions and records the approved vocabulary with meanings in `config.md`.
- `raw/` and `wiki/` have no mandatory subdirectories; `wiki/` is flat by default.
- Every write follows `Inspect → Propose → Approve → Apply → Verify → Log`.
- The bootstrap asks only necessary questions, one at a time, and waits for approval before writing.
- The generated wiki is self-contained.

### Task 1: Create the templates and README

**Files:**
- Create: `README.md`
- Create: `templates/config.md`
- Create: `templates/index.md`
- Create: `templates/log.md`
- Create: `templates/page-types/source.md`
- Create: `templates/page-types/subject.md`
- Create: `templates/page-types/note.md`
- Create: `templates/page-types/synthesis.md`
- Create: `templates/page-types/decision.md`
- Create: `templates/page-types/plan.md`

- [ ] Write a concise README covering the pattern, quick start, generated structure, nine-key frontmatter, tag initialization, six types, approval model, and version 1 boundaries.
- [ ] Write a self-contained config template containing purpose, scope, tag vocabulary, sensitive-data constraints, ownership rules, schema, and the write cycle.
- [ ] Write index and append-only log templates using portable relative Markdown links.
- [ ] Write six page templates with the agreed frontmatter, structured-but-elastic headings, and removable guidance.
- [ ] Verify every expected file exists, each page template has the correct `type`, and no tool-specific wiki links or stale `kind` fields appear.
- [ ] Commit the template set.

### Task 2: Create the self-contained bootstrap

**Files:**
- Create: `BOOTSTRAP.md`

- [ ] Start with the broad question: “What kind of knowledge base do you want to create, where should it live, and what will you use it for?”
- [ ] Instruct the receiving agent to ask only necessary follow-ups, one at a time, while inferring reasonable defaults.
- [ ] Embed the raw/wiki ownership model, universal types, frontmatter, statuses, context-driven tag initialization, links, templates, operations, and safety rules.
- [ ] Require a file-level proposal and explicit approval before creation or overwrite.
- [ ] Require post-write verification and a concise creation report.
- [ ] Verify the bootstrap contains the complete contract and does not rely on other repository files.
- [ ] Commit the bootstrap.

### Task 3: Dogfood the initializer

**Files:**
- Create temporarily: `/tmp/llm-wiki-startup-trial/`
- Modify if needed: `BOOTSTRAP.md`
- Modify if needed: `templates/*.md`
- Modify if needed: `templates/page-types/*.md`
- Modify if needed: `README.md`

- [ ] Use the startup-in-monorepo request from the design specification as the trial input.
- [ ] Simulate the minimal follow-up conversation and proposed generated structure.
- [ ] Materialize the approved proposal under `/tmp/llm-wiki-startup-trial/` without copying starter-repository dependencies.
- [ ] Verify the trial is self-contained, raw remains protected, wiki files are flat, startup terminology uses tags, links are relative, every page template contains all nine required frontmatter keys, and operational files explain approval-gated maintenance.
- [ ] Correct only issues revealed by the trial, then rerun the checks.
- [ ] Remove the temporary trial after inspection.
- [ ] Commit any refinements and report the finished initializer.
