# OKF v0.2 LLM Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the initializer so generated wikis follow OKF v0.2 sections 1–11, implement Karpathy's LLM Wiki workflows, and retain the approved local principles.

**Architecture:** Treat `wiki/` as the versioned OKF bundle, `raw/` as immutable native evidence, and root Markdown files as operating instructions. Vendor the exact upstream specification, keep the local profile small, and make conformance checks part of initialization and every wiki operation.

**Tech Stack:** Markdown, YAML frontmatter, Git, standard shell tools, and Ruby's standard YAML library for verification.

**Spec:** `references/2026-08-18-okf-v02-llm-wiki-design.md`

## Global Constraints

- Preserve all unrelated and uncommitted work; edit only files named by the active task.
- Use `apply_patch` for authored file changes.
- Keep `references/okf/v0.2/SPEC.md` byte-identical to upstream commit `3fcbb9f828c2f23d109c855ee403c3a4c81f3a96`.
- Do not modify, move, rename, or delete existing raw sources.
- `wiki/log.md` is mandatory; Git is strongly recommended but optional.
- Do not add executable connectors, credentials, a required runtime, background automation, or a fixed word limit.
- Do not duplicate the vendored OKF specification beyond short action-level rules and section references.
- Use plain language and the repository's existing compact documentation style.
- Stage and commit only the files listed by the current task.

---

### Task 1: Vendor And Pin OKF v0.2

**Files:**
- Create: `references/okf/v0.2/SPEC.md`
- Create: `references/okf/v0.2/UPSTREAM.md`

**Interfaces:**
- Consumes: Upstream OKF v0.2 at commit `3fcbb9f828c2f23d109c855ee403c3a4c81f3a96`.
- Produces: The authoritative local specification and provenance record used by every later task.

- [ ] **Step 1: Download the pinned upstream file to temporary storage**

Run with network approval if required:

```bash
curl -fsSL "https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/3fcbb9f828c2f23d109c855ee403c3a4c81f3a96/okf/SPEC.md" -o /private/tmp/okf-v0.2-SPEC.md
```

Expected: exit 0, and the downloaded document contains `**Version 0.2**`.

- [ ] **Step 2: Inspect the complete downloaded specification**

Run:

```bash
wc -l /private/tmp/okf-v0.2-SPEC.md
rg -n "Version 0.2|## 11\\. Conformance|## 12\\. Versioning" /private/tmp/okf-v0.2-SPEC.md
```

Expected: a non-empty document containing version, conformance, and versioning sections.

- [ ] **Step 3: Add the exact specification**

Use `apply_patch` to create `references/okf/v0.2/SPEC.md` with the downloaded content unchanged. Do not add local headings, comments, or frontmatter.

- [ ] **Step 4: Verify byte identity and calculate provenance**

Run:

```bash
cmp -s /private/tmp/okf-v0.2-SPEC.md references/okf/v0.2/SPEC.md
shasum -a 256 references/okf/v0.2/SPEC.md
```

Expected: `cmp` exits 0 and `shasum` prints one 64-character digest.

- [ ] **Step 5: Add the provenance record**

Use `apply_patch` to create `UPSTREAM.md` with:

- Version `0.2`.
- Repository `https://github.com/GoogleCloudPlatform/knowledge-catalog`.
- Source file URL pinned to commit `3fcbb9f828c2f23d109c855ee403c3a4c81f3a96`.
- Commit SHA `3fcbb9f828c2f23d109c855ee403c3a4c81f3a96`.
- Retrieval date `2026-08-18`.
- The exact SHA-256 digest printed in Step 4.
- Apache 2.0 attribution and a link to the license at the same commit.
- A note that v0.2 was the targeted version at retrieval time.

- [ ] **Step 6: Verify provenance matches the file**

Run the checksum again and compare it with the digest written in `UPSTREAM.md`:

```bash
shasum -a 256 references/okf/v0.2/SPEC.md
rg -n "3fcbb9f828c2f23d109c855ee403c3a4c81f3a96|SHA-256|Apache" references/okf/v0.2/UPSTREAM.md
```

Expected: the commit, checksum label, and license attribution are present and accurate.

- [ ] **Step 7: Commit the pinned standard**

```bash
git add references/okf/v0.2/SPEC.md references/okf/v0.2/UPSTREAM.md
git commit -m "docs: vendor OKF v0.2 specification"
```

---

### Task 2: Establish Repository Purpose And Authority

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: Vendored specification from Task 1 and the approved design.
- Produces: The human overview and agent entry points used by all later operating documents.

- [ ] **Step 1: Write failing documentation assertions**

Run:

```bash
rg -n "OKF v0.2|references/okf/v0.2/SPEC.md|Progressive autonomy|wiki/log.md" README.md AGENTS.md CLAUDE.md
```

Expected before editing: one or more required concepts are missing.

- [ ] **Step 2: Rewrite the README around the approved architecture**

Use `apply_patch` so `README.md` explains:

- `wiki/` is the OKF bundle.
- `raw/` contains immutable native evidence.
- Root files operate the system.
- The vendored specification is authoritative for OKF semantics.
- The local additions are progressive structure, simplicity-first writing, flat organization and living tags, progressive autonomy, the tailored starter kit, epistemic safeguards, and repository governance.
- `wiki/log.md` is mandatory and Git is recommended.
- The bootstrap is the initialization entry point and is not copied to generated wikis.

Keep local settings concise and remove legacy claims about fixed frontmatter, six statuses, and the 750-word limit.

- [ ] **Step 3: Rewrite AGENTS.md as a short router**

Use `apply_patch` so agents read:

1. `README.md` for purpose and local settings.
2. `references/okf/v0.2/SPEC.md` before creating, changing, or validating bundle content.
3. `references/schema.md` for the local profile.
4. `references/operations.md` for workflows and authority.
5. `references/writing-style.md` before substantial body writing.
6. `wiki/index.md` and relevant local indexes when present.

State raw immutability, progressive autonomy, conformance-before-finalization, and the prohibition on new root paths without approval.

- [ ] **Step 4: Keep CLAUDE.md as a thin adapter**

Use `apply_patch` so `CLAUDE.md` points to `AGENTS.md`, preserves the same authority boundaries, and adds no competing schema.

- [ ] **Step 5: Verify required authority and remove legacy language**

Run:

```bash
rg -n "OKF v0.2|references/okf/v0.2/SPEC.md|wiki/log.md|progressive autonomy" README.md AGENTS.md
ruby -e 'files=%w[README.md AGENTS.md CLAUDE.md]; bad=["750 words","status: fragment","created and updated"]; files.each{|f| s=File.read(f); bad.each{|x| abort("#{f}: #{x}") if s.include?(x)}}'
```

Expected: required terms are found and the Ruby check exits 0.

- [ ] **Step 6: Commit the overview and entry points**

```bash
git add README.md AGENTS.md CLAUDE.md
git commit -m "docs: define OKF wiki authority"
```

---

### Task 3: Replace The Local Schema And Concept Template

**Files:**
- Modify: `references/schema.md`
- Modify: `templates/wiki-page.md`

**Interfaces:**
- Consumes: OKF sections 2–7 and 10–11.
- Produces: The exact local field profile, type registry, tag registry, link rules, and default concept skeleton.

- [ ] **Step 1: Confirm the current schema fails the new profile**

Run:

```bash
rg -n "status: fragment|created:|updated:|## Citations" references/schema.md templates/wiki-page.md
```

Expected before editing: legacy fields or citation rules are found.

- [ ] **Step 2: Rewrite the local schema**

Use `apply_patch` to make `references/schema.md` define:

- `type`, `title`, `status`, `tags`, and `generated` as local requirements.
- `description` as optional for early drafts and required for `stable` concepts.
- Optional `resource`, `sources`, `usage_window`, `verified`, and `stale_after` fields with references to the vendored SPEC sections.
- `draft`, `stable`, and `deprecated` as the only status values.
- Exact actor patterns for agents, humans, and processes.
- `sources[].id` footnotes for claim-level attribution.
- Bundle-absolute links as preferred, with relative paths and URLs allowed.
- Broken-link tolerance and unknown-field preservation.
- The selected type registry: `Note`, `Reference`, `Source`, `Analysis`, `Decision`, `Goal`, `Plan`, `Dataset`, `Database`, and `Attested Computation`.
- A small, usage-driven tag registry with proposal-first tag changes.

Do not reproduce the full OKF field definitions.

- [ ] **Step 3: Replace the default concept template**

Use `apply_patch` so `templates/wiki-page.md` contains parseable template YAML using:

```yaml
---
type: Note
title: "Replace with a human-readable title"
status: draft
tags: []
generated:
  by: template/replace-during-creation
  at: "2000-01-01T00:00:00Z"
---
```

Do not include `description`, `resource`, empty provenance families, `created`, `updated`, or a forced title heading in the body. Explain outside the YAML that template values must be replaced when creating a concept.

- [ ] **Step 4: Parse the template frontmatter**

Run:

```bash
ruby -ryaml -e 's=File.read("templates/wiki-page.md"); m=s.match(/\\A---\\n(.*?)\\n---\\n/m) or abort("missing frontmatter"); y=YAML.safe_load(m[1], aliases: false); abort("missing type") if y["type"].to_s.empty?; abort("bad status") unless %w[draft stable deprecated].include?(y["status"]); abort("missing generated.by") if y.dig("generated","by").to_s.empty?'
```

Expected: exit 0.

- [ ] **Step 5: Verify legacy schema is gone**

Run:

```bash
ruby -e 'files=%w[references/schema.md templates/wiki-page.md]; bad=["status: fragment","created:","updated:","## Citations"]; files.each{|f| s=File.read(f); bad.each{|x| abort("#{f}: #{x}") if s.include?(x)}}'
```

Expected: exit 0.

- [ ] **Step 6: Commit the schema profile**

```bash
git add references/schema.md templates/wiki-page.md
git commit -m "docs: define local OKF concept profile"
```

---

### Task 4: Implement Operations, Autonomy, Indexing, And Logging

**Files:**
- Modify: `references/operations.md`
- Modify: `templates/index.md`
- Modify: `templates/log.md`

**Interfaces:**
- Consumes: Local profile from Task 3 and OKF sections 8–11.
- Produces: Ingest, query, maintenance, history, conformance, and failure behavior plus conformant reserved-file templates.

- [ ] **Step 1: Confirm current operations lack required workflows**

Run:

```bash
rg -n "All durable|Attested Computation|log-only|sources\\[\\]\\.id|YYYY-MM-DD" references/operations.md templates/index.md templates/log.md
```

Expected before editing: one or more requirements are absent.

- [ ] **Step 2: Rewrite operations.md**

Use `apply_patch` to define:

- Raw immutability and approved additions.
- Automatic normal writes under `wiki/`.
- Approval boundaries for deletion, broad structure, standards, rules, external access, external writes, sensitive material, and unusually broad actions.
- Ingest that populates `sources`, uses keyed footnotes for claim attribution, updates related concepts, index, and log, validates, and commits when available.
- Query behavior that files all durable or potentially useful knowledge into existing concepts or new distinct concepts, never generic Q&A pages.
- Maintenance checks for contradictions, staleness, links, orphans, provenance, duplication, missing concepts, OKF validity, computations, types, tags, and the tag registry.
- Mandatory log and optional Git modes, including stricter approvals without Git.
- Full conformance checks and failure handling.
- Attested Computation execution, stale, and failure behavior.

- [ ] **Step 3: Make the index template conformant**

Use `apply_patch` so `templates/index.md` shows the bundle-root version declaration, grouped headings, Markdown list entries, and descriptions. Explain that subdirectory indexes omit frontmatter and that links are relative to the index location.

- [ ] **Step 4: Make the log template conformant**

Use `apply_patch` so `templates/log.md` has no frontmatter, uses `# Directory Update Log`, groups entries newest-first under date-only headings such as `## 2026-08-18`, and uses concise operation bullets.

- [ ] **Step 5: Verify reserved-file formats and operations**

Run:

```bash
rg -n "okf_version: \"0.2\"|# Directory Update Log|## 2026-08-18" templates/index.md templates/log.md
rg -n "All durable or potentially useful knowledge|log-only|Attested Computation|sources\\[\\]\\.id|tag registry" references/operations.md
ruby -e 's=File.read("templates/log.md"); abort("timestamp heading") if s.match?(/^## \\d{4}-\\d{2}-\\d{2}T/); abort("frontmatter") if s.start_with?("---")'
```

Expected: required rules are found and Ruby exits 0.

- [ ] **Step 6: Commit operations and reserved templates**

```bash
git add references/operations.md templates/index.md templates/log.md
git commit -m "docs: implement OKF wiki operations"
```

---

### Task 5: Retain Simplicity And Add Focused Body Templates

**Files:**
- Modify: `references/writing-style.md`
- Modify: `templates/page-bodies/analysis.md`
- Modify: `templates/page-bodies/decision.md`
- Modify: `templates/page-bodies/goal.md`
- Modify: `templates/page-bodies/plan.md`
- Modify: `templates/page-bodies/reference.md`
- Modify: `templates/page-bodies/source.md`
- Create: `templates/page-bodies/dataset.md`
- Create: `templates/page-bodies/database.md`
- Create: `templates/page-bodies/attested-computation.md`

**Interfaces:**
- Consumes: OKF section 4.2 and the approved local simplicity rules.
- Produces: Qualitative writing guidance and optional body structures for every supported local use.

- [ ] **Step 1: Confirm numeric guidance still exists**

Run:

```bash
rg -n "750|word" references/writing-style.md
```

Expected before editing: the old numeric guidance is found.

- [ ] **Step 2: Rewrite writing-style.md**

Use `apply_patch` to retain:

- Plain language and the smallest useful structure.
- One coherent concept per file, credited to OKF.
- Headings, lists, tables, and code blocks when they improve human or agent retrieval.
- Meaning-based splitting rather than numeric splitting.
- Flat organization, links before folders, and no forced empty sections.
- Separation of evidence, interpretation, inference, uncertainty, and unresolved conflict.

Remove every fixed or suggested word count.

- [ ] **Step 3: Normalize existing body templates**

Use `apply_patch` to use H1 body headings because the title lives in frontmatter. Keep templates small and optional:

- Analysis: `# Conclusion`, `# Reasoning`.
- Decision: `# Decision`, `# Rationale`.
- Goal: `# Outcome`, `# Success Measures`, `# Progress`.
- Plan: `# Approach`, `# Actions`, `# Progress`.
- Source: `# Summary`.
- Reference: no forced headings.

- [ ] **Step 4: Add the data and computation templates**

Use `apply_patch` to create:

- Dataset: `# Schema`, `# Data`, `# Examples`.
- Database: `# Schema`, `# Examples`, `# Access`, `# Limitations`.
- Attested Computation: `# Computation` with a fenced example and one sentence explaining keyed source footnotes.

The templates contain body content only; frontmatter comes from the concept template and schema rules.

- [ ] **Step 5: Verify simplicity and conventional headings**

Run:

```bash
ruby -e 's=File.read("references/writing-style.md"); abort("numeric word rule remains") if s.match?(/750|\\b\\d+ words?\\b/i)'
rg -n "^# Schema|^# Examples|^# Computation|^# Access|^# Limitations" templates/page-bodies
```

Expected: Ruby exits 0 and the conventional headings appear in the relevant templates.

- [ ] **Step 6: Commit writing rules and body templates**

```bash
git add references/writing-style.md templates/page-bodies
git commit -m "docs: add focused OKF body templates"
```

---

### Task 6: Rebuild The Bootstrap Around The Pinned Standard

**Files:**
- Modify: `BOOTSTRAP.md`

**Interfaces:**
- Consumes: All authority, schema, operations, writing, and template files from Tasks 1–5.
- Produces: A purpose-first initializer that creates a self-contained, conformant wiki.

- [ ] **Step 1: Confirm bootstrap lacks new decisions**

Run:

```bash
rg -n "OKF v0.2|external database|log-only|references/okf/v0.2|Attested Computation" BOOTSTRAP.md
```

Expected before editing: one or more required decisions are missing.

- [ ] **Step 2: Rewrite discovery and conditional questions**

Use `apply_patch` so the bootstrap:

- Starts with purpose and material.
- Asks one follow-up question at a time only when it changes files, behavior, or safety.
- Determines scope, exclusions, terminology, sensitive-data rules, writing preference, actor identifiers, history mode, sources, and adapters.
- Asks about external databases only for business, organizational, research-data, analytics, operational, or explicitly data-connected uses.
- Skips the database question for ordinary personal notes, study, and reading unless external systems are mentioned.
- Never requests credentials.

- [ ] **Step 3: Rewrite the proposal and initialization contract**

Require the proposal to name target, existing-file changes, exact files, OKF version, raw handling, autonomy, external-resource concepts, Git choice, and assumptions. Approval covers only that proposal.

Initialization must:

1. Create `raw/` and `wiki/`.
2. Copy the complete `references/`, `templates/`, README, AGENTS, and approved adapters.
3. Create `wiki/index.md` with `okf_version: "0.2"`.
4. Create mandatory `wiki/log.md`.
5. Create only justified initial concepts.
6. Initialize Git only when selected.
7. Validate OKF sections 1–11 and the local profile.
8. Record and report initialization.

Do not copy `BOOTSTRAP.md`.

- [ ] **Step 4: Add external-resource initialization behavior**

When relevant and approved, create `Database` or `Dataset` concepts with canonical non-secret resource identifiers and optional `# Schema`, `# Examples`, `# Access`, and `# Limitations` sections. Record available read tools but do not install or configure connectors.

- [ ] **Step 5: Add explicit verification scenarios**

The bootstrap's verification section must cover personal initialization without database questions, business or research initialization with a safe external reference, both history modes, immutable raw sources, actor formats, sources and footnotes, index and log formats, Attested Computation contracts, unknown fields, broken-link tolerance, and operation without BOOTSTRAP.

- [ ] **Step 6: Verify bootstrap completeness**

Run:

```bash
rg -n "OKF v0.2|references/okf/v0.2|wiki/index.md|wiki/log.md|external databases|credentials|Git|log-only|Attested Computation|Do not copy.*BOOTSTRAP" BOOTSTRAP.md
ruby -e 's=File.read("BOOTSTRAP.md"); abort("legacy word limit") if s.include?("750"); abort("legacy status") if s.include?("status: fragment"); abort("optional log") if s.match?(/log\\.md.*optional/i)'
```

Expected: required concepts are found and Ruby exits 0.

- [ ] **Step 7: Commit the bootstrap**

```bash
git add BOOTSTRAP.md
git commit -m "docs: rebuild OKF v0.2 bootstrap"
```

---

### Task 7: Run Full Repository And Initialization Verification

**Files:**
- Modify only files from Tasks 1–6 when verification finds a concrete defect.
- Do not create persistent test fixtures in the repository.

**Interfaces:**
- Consumes: The complete redesigned initializer.
- Produces: Evidence that the repository is internally consistent and that two representative initialized wikis satisfy the design.

- [ ] **Step 1: Run repository-wide legacy checks**

Run:

```bash
ruby -e 'files=Dir.glob("{README.md,AGENTS.md,CLAUDE.md,BOOTSTRAP.md,references/{schema,operations,writing-style}.md,templates/**/*.md}"); bad=["status: fragment","created:","updated:","## Citations","750 words"]; files.each{|f| s=File.read(f); bad.each{|x| abort("#{f}: #{x}") if s.include?(x)}}'
```

Expected: exit 0.

- [ ] **Step 2: Verify the vendored source and authority links**

Run:

```bash
test -f /private/tmp/okf-v0.2-SPEC.md || curl -fsSL "https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/3fcbb9f828c2f23d109c855ee403c3a4c81f3a96/okf/SPEC.md" -o /private/tmp/okf-v0.2-SPEC.md
cmp -s /private/tmp/okf-v0.2-SPEC.md references/okf/v0.2/SPEC.md
rg -n "references/okf/v0.2/SPEC.md" README.md AGENTS.md references/schema.md references/operations.md BOOTSTRAP.md
```

Expected: byte comparison exits 0 and every operating layer points to the pinned specification.

- [ ] **Step 3: Create a disposable personal-wiki fixture**

Run:

```bash
mktemp -d -t llm-wiki-personal | tee /private/tmp/llm-wiki-personal-path.txt
```

Use the printed directory and follow `BOOTSTRAP.md` with these answers:

- Purpose: personal study notes about machine learning.
- Material: articles and handwritten notes.
- Sensitive data: none.
- History: log only.
- Adapter: AGENTS.md and CLAUDE.md.

Expected: the initializer does not ask about databases, creates no database concept, creates mandatory `wiki/index.md` and `wiki/log.md`, copies the pinned specification, and does not copy `BOOTSTRAP.md`.

- [ ] **Step 4: Validate all concepts in the personal fixture**

Run this command with the fixture path as its argument:

```bash
PERSONAL_FIXTURE_PATH=$(sed -n '1p' /private/tmp/llm-wiki-personal-path.txt)
ruby -ryaml -rdate -e 'root=ARGV.fetch(0); Dir.glob(File.join(root,"wiki","**","*.md")).each{|f| next if %w[index.md log.md].include?(File.basename(f)); s=File.read(f); m=s.match(/\\A---\\n(.*?)\\n---\\n/m) or abort("#{f}: missing frontmatter"); y=YAML.safe_load(m[1], permitted_classes:[Date,Time], aliases:false); abort("#{f}: missing type") if y["type"].to_s.strip.empty?}' "$PERSONAL_FIXTURE_PATH"
```

Expected: exit 0.

- [ ] **Step 5: Create a disposable business-wiki fixture**

Run:

```bash
mktemp -d -t llm-wiki-business | tee /private/tmp/llm-wiki-business-path.txt
```

Use the printed directory and follow `BOOTSTRAP.md` with:

- Purpose: company operations and analytics.
- Material: policies, meeting notes, and a PostgreSQL analytics database.
- External resource: the non-secret URI `postgresql://analytics.example.internal/product`.
- Existing access: read-only through an already configured agent tool.
- Sensitive data: never retain credentials or customer personal data.
- History: Git and log.

Expected: the bootstrap asks the contextual database question, creates a `Database` concept without credentials, initializes Git, and creates conformant index and log files.

- [ ] **Step 6: Exercise provenance and computation contracts**

In the business fixture, create:

- One `stable` concept with `sources`, a matching keyed footnote, `generated`, `verified`, and `stale_after`.
- One `stable` `Attested Computation` with runtime, typed parameters, computation, executor receipt fields, deterministic attester resource, provenance, verification, and staleness.

Run the local conformance procedure from `references/operations.md`.

Expected: both concepts pass. Then remove one footnote source ID in the disposable fixture and confirm the local check fails; restore it and confirm the check passes.

- [ ] **Step 7: Exercise tolerant OKF consumption**

In the disposable fixture, add an unknown frontmatter extension and an unknown type, then add one broken Markdown link.

Expected: the local check preserves the extension and type, reports the broken link, and does not classify the bundle as nonconformant.

- [ ] **Step 8: Review repository diffs and run formatting checks**

Run:

```bash
git diff --check
git status --short
git diff -- README.md BOOTSTRAP.md AGENTS.md CLAUDE.md references/schema.md references/operations.md references/writing-style.md templates
```

Expected: no whitespace errors, no unexpected files, and only approved repository changes.

- [ ] **Step 9: Commit verification fixes only when needed**

If verification required corrections, stage only those corrected files and commit:

```bash
git add -- README.md BOOTSTRAP.md AGENTS.md CLAUDE.md references/okf/v0.2 references/schema.md references/operations.md references/writing-style.md templates
git commit -m "docs: fix OKF integration verification"
```

If no corrections were needed, do not create an empty commit.

- [ ] **Step 10: Report final evidence**

Report:

- Pinned upstream commit and checksum.
- Files added and modified.
- Legacy checks result.
- Personal and business initialization results.
- Provenance, computation, and tolerant-consumption results.
- Git status and any unrelated pre-existing changes left untouched.
