# Wiki Operations

Select an operation through [`AGENTS.md`](../AGENTS.md). Here, a **page** means a concept in `wiki/`; a **source** means original material used as evidence.

## Operating Principles

Read only what the current step needs; reuse instructions, search results, and source text unless they change.

### Safety And Permission

Before each operation, read [Safety](local-settings.md#safety). Its restrictions apply to everything you read, save, search, or share, including responses. Never save prohibited material. Sharing restricted material outside the approved access boundary requires approval for the named audience, system, material, and purpose.

Explicit approval is required for
- deleting pages or raw files, individually or within an explicitly approved cleanup scope;
- broad merges, splits, moves, renames, or reorganizations;
- changes to local settings other than new entries added under [Tag Registry Changes](#tag-registry-changes);
- changes to schema, operating rules, templates, autonomy, or OKF version;
- new external connections or wider access;
- and external writes.

Ask when the requested outcome is materially unclear or the proposed action exceeds existing authorization. Describe the affected files or systems, intended result, and any replacement, move, or deletion of existing content.

An explicit Migrate request authorizes the selected stable release's operating-file changes, target-defined local-settings restructure, and mechanical wiki-frontmatter compatibility updates. It authorizes retaining compatible setting values and omitting values that have no destination in the target structure; it does not authorize reinterpreting those values or changing concept bodies, raw files, or other user-owned material.

### Tag Registry Changes

During an authorized operation, an agent may add a new entry to the [Tag Registry](local-settings.md#tag-registry) without separate approval when no existing tag applies. Follow the schema's [tag rules](schema.md#tags), apply the new tag only to concepts within the operation's scope, and report its name, definition, and affected concepts in the final result.

This exception covers additions only. Renaming, merging, redefining, or retiring an existing tag requires explicit approval. Suggest broader application of a new tag as Maintenance rather than retagging unrelated concepts.

### Sources And Claims

Keep saved originals in `raw/`. Do not edit, overwrite, rename, or move retained raw files; save corrections as new files. Deletion follows [Safety And Permission](#safety-and-permission). Leave `raw/.gitkeep` unchanged; it is not evidence.

Retained originals preserve provenance; they are not a second routinely searched knowledge layer. Ingest reads supplied source material before retaining it. Other operations inspect raw content only when Query has explicit raw scope or [Agent Review](#agent-review) requires source comparison.

Combine evidence only when it supports the conclusion; distinguish inference from direct source statements and cite the sources used. Remove or qualify unsupported claims. Report disagreements, missing evidence, and unreadable material. Never imply that an unavailable source or system was checked.

### Finalize Changes

After any operation other than Migrate changes knowledge-base files:

1. Update navigation and history when required by [`schema.md`](schema.md).
2. Use [Review](#review) on the final state.
3. Resolve required, in-scope findings within the originating operation. After repairs, update navigation and history again and repeat Review.
4. If a required finding cannot be resolved, report the partial result and blocker.

## Core Operations

### Ingest

**What it does:** Turn material the user has asked to add, or an accepted retention proposal, into wiki knowledge.

Process independent sources or source sets sequentially. After completing step 6 for one source or source set, return to step 1 for the next, so each uses the latest pages.

Treat multiple files as one source set only when they are alternate forms or parts of the same source, or must be understood together. Within a source set, assess the files together while preserving each source’s provenance, disagreements, and retention decision.

**Start with:** material the user has asked to add, or an accepted retention proposal.

**Steps** (repeat until all sources/source sets are ingested):
1. **Read the source.** Identify its producer, date or version when known, main points, and search terms. Extract text temporarily if the file is difficult to read, then discard the extraction after use. Note unreadable sections. Stop work on an inaccessible source, report what is needed, and continue with accessible sources.
2. **Find where it fits.** Use [Search](#search) with those topics and terms. Compare the source's actual claims with the matching pages. Decide relevance after this comparison.
3. **Choose changes.** Plan changes with the table below; apply them in step 4. Keep a short working list of pages to create or update and the source passages supporting each change. One source may affect several pages. For an approved synthesis, consider the supporting sources together, including those already recorded.

   | What the source contributes | What to do |
   |---|---|
   | Additional facts about an existing concept | Add them to that page. |
   | Useful evidence for an existing claim | Add the source and its citation; change the wording only if needed. |
   | An explicit correction or replacement of an earlier source | Update the affected claim and explain which evidence replaced it. |
   | A disagreement that the available evidence does not resolve | Keep the competing accounts and mark the disagreement. |
   | A useful subject not covered by an existing page | Create a page for the new subject. |
   | A useful synthesis across sources | Create or update a page for the synthesis when its retention is authorized. |
   | Nothing useful beyond what is already recorded | Leave the pages unchanged. |
   | Text cannot be read or a claim cannot be checked | Leave out unsupported claims and report the gap. |

   Do not create a page merely to summarize an unused source.

4. **Write the pages.** Read [`writing-style.md`](writing-style.md) and [`schema.md`](schema.md). Use [Concept Types And Requirements](schema.md#concept-types-and-requirements) to choose the page type and its additional field requirements, then use [Body Structure](schema.md#body-structure) for an optional body template. Assign at least one tag under [Tags](schema.md#tags), using the [Tag Registry](local-settings.md#tag-registry) or adding a suitable entry under [Tag Registry Changes](#tag-registry-changes). Apply the planned changes, including approved analyses and syntheses. For analyses, follow the [body guidance](writing-style.md#type-specific-structure) on scope, effective dates, and evidence versions. Add citations for new support or disagreement. Record only verification actually performed and defensible expiry dates.

5. **Retain sources used by the result.** Check the resulting concepts against the schema's [raw-evidence requirement](schema.md#raw-files). For each source they use as evidence through `sources[].resource` or as a subject through `resource`, reuse an identical retained original or save the new original unchanged under `raw/`. For an external source, preserve a permitted export or saved page; an approved live resource may remain external with its location and access limits recorded. If no resulting concept references the source, do not add it to retained evidence; report why and stop work on this source. Leave existing unreferenced raw files for a requested or scheduled Maintenance run.

6. **Finalize this source's changes.** Follow [Finalize Changes](#finalize-changes). Process the next source after finalization; report the combined results once.

**Result:** saved source locations, the pages changed or reason no page changed, any tags added, and any unresolved claims or unreadable material.

### Query

**What it does:** Answer questions and complete tasks using the knowledge retained in `wiki/`.

**Start with:** a user query.

**Steps:**
1. **Find the answer material.** Use [Search](#search) for the user's question or task. Treat `wiki/` as the default queryable knowledge layer. Do not inspect or search `raw/` unless the user explicitly asks to inspect a particular raw file or search raw material.
2. **Answer or complete the task.** Consult relevant sections of [`schema.md`](schema.md) when interpreting provenance, verification, or expiry dates. For ordinary answers, use relevant wiki passages and link the wiki pages used when their citations adequately support the answer and there are no material warnings about support or freshness. If wiki knowledge is insufficient, answer the supported portion and identify the gaps. When useful, tell the user they may ask you to search retained raw material, consult external sources, or provide a clearly labelled answer from general knowledge. If the request already calls for outside or current information, consult appropriate external sources. Seek current evidence when a time-sensitive claim depends on evidence too old for the task; if unavailable or outside scope, qualify the answer. Clearly distinguish anything found outside the wiki from knowledge recorded in it, and cite external sources used. Mention disagreements, weak evidence, unavailable sources, and stale information that affect the answer.

   For historical questions, distinguish what was recorded at the requested date from a current analysis of that period. Use historical versions for the former; identify any later evidence used for the latter. Logs and metadata dates alone do not reconstruct earlier page contents. Report missing versions and clarify the interpretation only when it is unresolved and changes the answer. A request for an overview or analysis does not by itself authorize saving it.

3. **Consider retaining new knowledge.** Propose retaining supplied or newly surfaced new knowledge if it is relevant, likely to be reused, and not already recorded. Exclude sensitive, unreliable, or temporary material. Do not propose generic Q&A pages or chat-transcript archives. Name the knowledge and any files worth keeping. A later acceptance starts [Ingest](#ingest)

**Result:** an answer or completed task with evidence and limitations; optionally, a short retention proposal.

### Research

**What it does:** The knowledge-base wrapper for requests to find outside sources.

It defines scope, evidence requirements, and the handoff to Ingest; it does not replace a research method. Use the strongest suitable research capability available, including a user-requested skill, plugin, or tool. The requirements below apply to the result regardless of the method used.

**Steps:**
1. **Set the knowledge-base scope.** State the questions, relevant period, and any source or search limits from the request. Use [Search](#search) to identify existing knowledge, gaps, or claims needing fresh evidence.
2. **Conduct the research.** Follow the selected research capability's method for discovery and synthesis. If none provides a method, search the identified gaps, read candidate sources, and look for criticism, failures, and opposing evidence. Match the depth to the request.
3. **Prepare the evidence for knowledge-base use.** Map reported claims to identifiable sources that were actually read. Assess what each source adds, who produced it, its date, its independence, whether it duplicates existing evidence, and whether relevant sources disagree. Follow the selected method's stopping rule; otherwise stop when the questions have adequate support and counterevidence has been considered, or further revised searches add no useful evidence. Report remaining gaps, and do not log rejected sources that were never saved.
4. **Deliver and hand off.** Answer the questions with citations, limitations, and disagreements. Identify any sources or synthesis worth retaining. Research does not save them directly: if retention is authorized, pass them through [Ingest](#ingest); otherwise propose them and finish. A later acceptance starts Ingest.

**Result:** findings and source recommendations, plus any approved wiki additions.

### Maintenance

**What it does:** Performs requested or scheduled maintenance on existing knowledge-base material.

**Start with:** a maintenance request and its scope.

**Steps:**
1. **Review the scope.** Use [Review](#review) to identify maintenance needs.
2. **Repair.** Resolve required, in-scope findings. Follow [`schema.md`](schema.md) for structure and metadata and [`writing-style.md`](writing-style.md) for concept bodies.
3. **Finalize the changes.** Follow [Finalize Changes](#finalize-changes).

**Result:** completed maintenance, confirmation that no changes were needed, or a partial result with blockers.

## Other Operations

### Review

**What it does:** Inspects knowledge-base material or changes without modifying them.

**Start with:** the requested scope and, for changes, their intended result.

**Steps:**
1. **Select the scope.** Review the requested material and affected dependencies. Use [Search](#search) to find relevant material. For a complete review, enumerate everything in scope. Track anything that cannot be checked.
2. **Run automated checks.** Follow [Automated Checks](#automated-checks).
3. **Perform agent review.** Follow [Agent Review](#agent-review). For changes, confirm that the final state fulfills the intended result.
4. **Report findings.** Group findings by file. Distinguish required findings from warnings and optional improvements. Include suggested corrections when clear, plus coverage and limitations.

**Result:** findings and suggested corrections, or confirmation that no issue was found within the checked scope.

#### Automated Checks

`validate-wiki.py` checks mechanically enforceable schema rules. `check-evidence.py` checks evidence references and retained-source usage without interpreting source contents.

Run both checkers for wiki content, retained sources, schema, templates, or tag rules. Use full mode for complete or broad reviews and for changes to schema, templates, checker code, or the pinned OKF document. Otherwise, use changed mode with the reviewed paths and affected dependencies. For checker code, also run relevant tests. For other documentation or tooling, run relevant automated or behavior checks; run the wiki checkers only when those files affect the wiki.

Full mode:

```bash
python3 references/validate-wiki.py --all
python3 references/check-evidence.py --all
```

Changed mode:

```bash
python3 references/validate-wiki.py --changed <path> [<path> ...]
python3 references/check-evidence.py --changed <path> [<path> ...]
```

Report the coverage shown by the tools. Agent Review covers claim truth, semantic dependencies, and instruction correctness.

#### Agent Review

Read the reviewed material and affected passages in dependent files. Apply the relevant schema, writing style, local settings, and operation-specific rules.

- For concepts, assess meaning, source support, freshness, conflicts, atomicity, organization, and links.
- When a source-backed claim, quotation, number, date, or citation changed—or the user requests evidence review—compare the affected claim with its cited source. This checks citation fidelity, not whether the source is true or current.
- For rules, templates, or tooling, assess intended behavior, examples, links, and relevant test results.

### External Access And Connector Setup

External Access And Connector Setup makes an external resource usable for the intended task within its approved access boundary. It records how to access the resource, what has been demonstrated to work, and any limits or unfinished setup.

Before writing a resource page, read [`schema.md`](schema.md), [`writing-style.md`](writing-style.md), and the [Tag Registry](local-settings.md#tag-registry). Document a live system as a `Database` and a bounded collection as a `Dataset`, using the [shared page template](../templates/wiki-page.md) and the appropriate [Database](../templates/page-bodies/database.md) or [Dataset](../templates/page-bodies/dataset.md) body. Record the method, tools, access scope, restrictions, and next action under `# Access`; put unknowns under `# Limitations`.

1. **Identify the resource and required access.** Establish the named system or collection, intended task, and smallest test that demonstrates the access needed. Use [Search](#search) to find its resource page. Distinguish what is authorized from what is known to work; a working connection alone is not authorization.
2. **Resolve missing approval.** If the required access and setup are already authorized, continue to step 3. Otherwise, recommend creating or updating a draft resource page to record the proposed setup and known access. Summarize what the draft would contain and ask for approval before creating it. Do not treat approval to draft the page as approval to establish the connection or use the access. Once drafting is approved, create or update the page and follow [Finalize Changes](#finalize-changes), with connection work still pending. Request any remaining approval under [Safety And Permission](#safety-and-permission), naming the system, integration, read/write scope, affected files or settings, and authentication method. Pause each unapproved action until it is approved; continue other authorized work where useful.
3. **Set up and test access.** Use the existing connection or establish it through the approved authentication flow. Create a separate `Plan` only when the user has chosen to proceed and several actions need tracking. Run the test from step 1 within the authorized scope. Confirm access to the required collection or action; successful authentication alone may be insufficient. Do not expand access to make a test pass.
4. **Record and finish.** Create or update the resource page with what was configured, the test and observed result, and any limitations or next actions. Distinguish successful, partial, failed, and untested access. Claim verified access only for demonstrated capabilities. Follow [Finalize Changes](#finalize-changes) for any wiki changes.

**Result:** a recommendation awaiting approval to draft, or an approved resource page describing the access, demonstrated capabilities, limitations, and any pending approval, setup, or testing.

### Attested Computation

Attested Computation keeps a reusable calculation clearly defined, supported by evidence, and checked against its declared method whenever it runs. It makes the definition's verification state and each run's outcome explicit.

The executor runs the calculation and returns a receipt; the attester is deterministic, non-LLM code that checks that receipt. OKF describes this contract but does not supply the runtime. Definition verification and run attestation are separate; do not save run receipts as definition-verification history.

Use [Search](#search) to locate the calculation, then follow only the requested branch below. Keep one concept per calculation. If a requested review, run, or test has no definition, report the gap; do not improvise one. Propose a governed definition when a recurring or consequential calculation would benefit from it.

#### Define Or Change

1. **Write the definition.** Read [`schema.md`](schema.md), [`writing-style.md`](writing-style.md), and the [Tag Registry](local-settings.md#tag-registry). Create or update the concept with the [shared template](../templates/wiki-page.md) and [Attested Computation body](../templates/page-bodies/attested-computation.md). Follow the [contract rules](schema.md#attested-computation-requirements) for the runtime, method, parameters, sources, executor, receipt, and attester.
2. **Set the verification state.** Keep the definition draft until the schema's required checks and independent verification are satisfied. Record only verification actually performed. A definition change does not authorize execution; use Run Or Explicitly Test only when requested.
3. **Finalize the definition.** Follow [Finalize Changes](#finalize-changes).

#### Review The Definition

1. **Request a definition review.** Use [Review](#review) for the concept and its [contract rules](schema.md#attested-computation-requirements). Request checks of source support and the usability of its computation, executor, and attester. A definition review does not authorize execution; distinguish inspected code from tested behavior.
2. **Report findings.** Return the findings, coverage, and missing tools or evidence. If changes are requested, use Define Or Change.

#### Run Or Explicitly Test

1. **Check readiness and inputs.** Read the existing contract and [contract rules](schema.md#attested-computation-requirements). An ordinary run requires a stable definition with a usable computation, executor, and attester. A draft may be tested only when explicitly requested and those execution requirements are met. Check freshness and applicable access approval. Supply values only for declared parameters, respecting their types and requirements. Report unmet requirements without running or altering the definition.
2. **Execute and attest.** Use the declared executor and pass its receipt to the declared attester. If either fails or is unavailable, report the failure without using or displaying the result value.
3. **Return the checked result.** After successful attestation, return the value and verdict, including any stale-definition warning. Label draft results as test results. A run or test alone does not change the wiki or its verification metadata.

**Result:** a definition with its verification state, a review with findings, or an attested result; otherwise, the unmet requirements or failure.

### Search

Return relevant page paths and passages, plus remaining gaps. For a question about one exact file, read it directly. Use search for cross-page questions and proposed changes.

1. **Choose scope and terms.** Use specific topics, names, phrases, identifiers, aliases, and synonyms from the input. Cover each distinct topic in a long source. Identify whether the task needs ordinary discovery, a complete inventory or audit, or dependency review; step 4 gives each a stopping rule.
2. **Search with a tool.** Use `rg` (ripgrep), or an equivalent full-text search tool, across Markdown page contents in `wiki/`. Searching the root or topic indexes is optional navigation help; use the search tool for those searches too. An index match does not replace searching page contents. Return matching filenames or short excerpts. Do not open every page to discover relevance.

   Search `wiki/log.md` separately for history questions. Indexes may suggest terms or candidate pages, but must not confine a cross-wiki search to one folder. If full-text search is unavailable, use available indexes to select specific pages and report incomplete coverage; do not compensate by opening every page. Tool errors and inaccessible files are not evidence of no matches.

   Run from the knowledge-base root, replacing terms:

   ```bash
   # Find candidate pages with a tool, including hidden or ignored Markdown files.
   rg -l -i -F --hidden --no-ignore -g '*.md' -g '!index.md' -g '!log.md' -e 'access control' -e 'permissions' -- wiki/

   # Optionally search the root index for navigation clues.
   rg -n -i -F -e 'access control' -e 'permissions' -- wiki/index.md
   ```

   `-F` matches literal text; repeated `-e` options mean either term. `-i` ignores case, `-l` returns filenames, and `-n` adds line numbers. `--hidden --no-ignore` includes files that default exclusions might hide.

3. **Inspect and read selected matches.** Inspect short matching excerpts to choose useful pages; filenames and tool output order are not relevance rankings. Work through candidate batches or refine broad terms. Read the selected passages with their qualifications and citations, then follow links needed to understand them.

   To inspect candidates, replace the terms and supply one or more selected paths:

   ```bash
   rg -n -i -F -C 2 -m 3 -e 'access control' -e 'permissions' -- wiki/access-policy.md
   ```

   `-C 2` adds two lines of context; `-m 3` limits matching lines per file. This is a sample for selection, not a complete evidence review. Read more of selected pages when needed.

4. **Check coverage and stop.** A search round means searching with one set of terms and reviewing the results; an optional index search is part of that round. Revise terms for unanswered topics. Use the rule for the task:

   - **Ordinary discovery:** stop when the requested points have support and relevant caveats have been checked, or two consecutive revised rounds add no useful evidence for an unresolved topic. Honor any earlier user limit. Report gaps; an empty search does not prove absence.
   - **Complete inventories and audits:** enumerate files in the requested scope with a file-listing tool and track coverage. Search helps navigate but cannot establish completeness. Finish when every in-scope item has been assessed, or report the unreviewed portion and why it remains. This may require reading every in-scope page for the review, not for discovery.
   - **Dependency review:** track candidates found from changed page paths, source paths, and claims. Check link targets in their relative or bundle-relative forms. Process newly affected pages and repeat searches for their changes until no candidates remain unchecked. The ordinary search-round limit does not truncate this work; report any inaccessible dependencies or other coverage limits.

### Migrate

**What it does:** Moves an existing knowledge base to a newer stable starter release while preserving its knowledge, evidence, unknown files, and target-compatible local setting values. Content-quality work remains separate.

**Start with:** an explicit user request to migrate and an optional target version. Never initiate Migrate automatically or as part of another operation.

**Steps:**
1. **Update the operating kit.** Run `python3 references/migrate.py --target <version-or-latest>`. For a release without this command, download and review `migrate.py` from the selected target release and run it with `--root <knowledge-base>`. The command downloads only the selected stable release, composes its cumulative adjacent transition route, and verifies the release version and ownership ledger before writing. It backs up only existing files it may modify, overlays final target-managed files, removes only retired source-owned files, and prepares declared merger sources and targets. It never changes `.git/`, `raw/`, `wiki/`, or unknown files. Stop and report any failure and its backup path.
2. **Apply declared mergers and mechanical compatibility changes.** Reread the installed Migrate instructions, changelog, and action record. For each `target-structure` merger, begin with the saved target template and carry forward a source value only when it fits a section, field, or open collection present in that template. Put retained values only in target-defined locations; do not recreate removed headings, fields, placeholders, or unknown entries. Keep the target default when no compatible source value exists. Do not reinterpret or invert a value to make it fit. Report populated source settings that were omitted; the complete source remains in the backup. Apply documented, deterministic frontmatter changes with release-provided or ordinary command-line tools, copying each affected wiki file into the same backup before modification. Do not inspect or alter concept bodies or raw files. Leave changes requiring judgment untouched and report them for later Maintenance. If frontmatter changed, back up `wiki/log.md`, then add one Migrate entry naming the affected pages.
3. **Validate once.** After all compatibility changes, run `python3 references/validate-wiki.py --all` and `python3 references/check-evidence.py --all`. Resolve mechanical migration errors only; do not perform Agent Review or content-quality repairs during Migrate.
4. **Report and hand off.** Report the composed version route, release commit, operating files changed, retained and omitted settings, frontmatter changes, validation results, unresolved compatibility issues, and backup path. When content could benefit from the new rules or templates, suggest a separate Maintenance run in user-specified batch sizes (usually around twenty to fifty files), completing and reporting each batch before starting another.

**Result:** a completed mechanical migration, or a partial result with validation failures, untouched judgment-dependent changes, and recovery information.
