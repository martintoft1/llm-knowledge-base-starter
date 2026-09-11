# LLM Knowledge Base Starter

LLM Knowledge Base Starter is a starter kit for a file-based knowledge base that humans own and AI agents help build and maintain.

It targets Google's OKF v0.2 and follows Karpathy's LLM Wiki pattern: keep original evidence separate, let agents turn it into connected Markdown knowledge, and keep improving that knowledge through normal use.

## How the Knowledge Base Works

### Sources and Knowledge

`raw/` preserves retained originals. `wiki/` contains the knowledge that agents build from the raw files: connected Markdown pages that can be searched, reused, and updated.

Under the [source-preservation rules](references/operations.md#sources-and-claims), retained originals stay unchanged; corrections are saved as new files, and deletion requires approval. Each retained original has to be [used by a concept](references/schema.md#raw-files) as evidence or as its subject. Otherwise, it is an orphan and Maintenance proposes its removal. Approved live resources may remain external, with their location and access limits recorded.

Humans own the evidence and knowledge. Agents work within the [approval boundaries](references/operations.md#safety-and-permission) for deletions, broad reorganizations, rule changes, external connections or wider access, and external writes. [Local safety settings](references/local-settings.md#safety) govern what may be stored or shared.

### Architecture
```text
<knowledge-base-root>/
├── raw/                    # Immutable original sources
├── wiki/                   # The OKF v0.2 knowledge bundle
│   ├── index.md            # Bundle navigation and OKF version
│   ├── log.md              # Mandatory update history
│   └── *.md                # Knowledge concepts
├── README.md               # Overview, architecture, and navigation
├── VERSION                 # Current operating-kit version
├── CHANGELOG.md            # Starter release history
├── LICENSE                 # Apache License 2.0 terms
├── NOTICE                  # Copyright and upstream attribution
├── AGENTS.md               # Agent entry point
├── CLAUDE.md               # Optional Claude adapter
├── references/             # Operating rules and checkers
└── templates/              # Reusable concept and body templates
```
Files outside `wiki/` preserve evidence or operate and support the system.

### Concept Pages

A concept page combines YAML metadata with a Markdown body. Metadata describes the page and, where applicable, its sources, verification, and freshness. The body holds the knowledge and its supporting reasoning, examples, and citations.

Each concept file only covers one [atomic concept](references/schema.md#atomicity-and-organization): the smallest useful unit that can stand alone and be sourced, linked, and maintained independently. Necessary context stays with it; length alone is not a reason to split a page. An analysis or plan can bring several other concepts together around one clear conclusion or course of action.

Each concept has one canonical page. Tags group concepts for cross-cutting discovery, while links express specific relationships needed for understanding or reuse. [`wiki/index.md`](wiki/index.md) lists every concept for navigation. Pages use the [smallest suitable type](references/schema.md#concept-types-and-requirements), such as a Note, Reference, Analysis, or Decision.

The [writing style](references/writing-style.md) favors the smallest useful page, with structure added only when it helps reading or retrieval. Inferences, uncertainty, and unresolved disagreements remain explicit.

### Operations

[Ingest](references/operations.md#ingest) turns material the user has asked to add, or an accepted retention proposal, into wiki knowledge.

[Query](references/operations.md#query) answers ordinary questions and completes tasks using `wiki/` by default.

[Research](references/operations.md#research) is a knowledge-base wrapper around the strongest suitable built-in or user-requested research capability, skill, plugin, or tool.

[Maintenance](references/operations.md#maintenance) performs requested or scheduled maintenance on existing material.

[Review](references/operations.md#review) checks material without changing it. It uses two complementary methods:
- [Automated checks](references/operations.md#automated-checks) enforce rules that can be checked with code.
- [Agent review](references/operations.md#agent-review) checks meaning, writing, evidence, organization, links, and intended behavior.

Other operations cover [External Access and Connector Setup](references/operations.md#external-access-and-connector-setup) and governed, reusable [Attested Computation](references/operations.md#attested-computation). [Search](references/operations.md#search) is the shared retrieval procedure.

[Migrate](references/operations.md#migrate) installs a newer stable starter release and applies only mechanical compatibility changes while preserving local knowledge, evidence, unknown files, and target-compatible setting values.

### Operating Files

These files have separate responsibilities, not a general precedence order:

| File | Responsibility |
|---|---|
| [`references/local-settings.md`](references/local-settings.md) | Knowledge-base-specific settings and restrictions |
| [`references/schema.md`](references/schema.md) | Bundle and concept structure |
| [`references/writing-style.md`](references/writing-style.md) | Concept-body writing rules |
| [`references/operations.md`](references/operations.md) | Workflows and approvals |
| [`AGENTS.md`](AGENTS.md) | Short routing and reading instructions for agents |

The pinned [`references/okf/v0.2/SPEC.md`](references/okf/v0.2/SPEC.md) remains authoritative for reserved OKF terms and semantics. Local rules may narrow its format but never redefine those semantics. Consult the specification when the operating files do not cover an OKF field or edge case.

The pinned [`references/okf/v0.2/README.md`](references/okf/v0.2/README.md) provides upstream rationale and examples. It is explanatory, not normative; its reference-agent setup is not required here.

## Getting Started

### Prerequisites

- **Agent access:** filesystem access and either a file-search tool or command execution. Running the validation scripts also requires command execution.
- **Required for validation:** Python 3 with PyYAML installed in the Python environment used by the checkers. Install PyYAML with `python3 -m pip install PyYAML` (`py -m pip install PyYAML` on Windows).
- **Required for migration:** Git and access to the canonical release repository.
- **Recommended for search:** [ripgrep](https://github.com/BurntSushi/ripgrep#installation), which provides the `rg` command. Equivalent file-search tools may be used when it is unavailable.

### First Use

The repository includes an empty valid `wiki/` bundle and a tracked `raw/` directory. Set up the prerequisites above, then review [`references/local-settings.md`](references/local-settings.md) before adding knowledge.

You can ask an agent with filesystem access:

```text
Review references/local-settings.md with me, keep its defaults unless I ask for a change, then help me start using the knowledge base.
```

### Common Prompts

Use these examples as written or adapt them to the task:

| Task | Prompt |
|---|---|
| Ingest / Add knowledge | `Ingest <text or files>` |
| Find sources for the wiki | `Find sources for the knowledge base on <question>.` |
| Query / Ask a question | `<question>` |
| Save an analysis | `Analyze <question or comparison> and save the useful findings in the wiki.` |
| Summarize | `Summarize <text or files>` |
| Review content | `Review <text or files>` |
| Correct knowledge | `Update the wiki with this correction: <change>` |
| Review the wiki for issues | `Review the wiki.` |
| Maintain the wiki | `Maintain the knowledge base.` |
| Migrate the starter | `Migrate the knowledge base to the latest stable starter release.` |
| Connect a system or source | `Connect <system or source> to the knowledge base.` |
| Define a reusable calculation | `Define <metric>, so the same calculation is used in the future.` |

## Project Information

### About

LLM Knowledge Base Starter was created and is maintained by [Martin Toft](https://github.com/martintoft1).

### Versioning and Releases

The starter uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html). [`VERSION`](VERSION) records the current operating-kit version, and [`CHANGELOG.md`](CHANGELOG.md) records notable changes. Public releases use an annotated Git tag named `v<version>` and a matching GitHub Release. The version identifies the operating kit, not the knowledge content that a user later adds.

Before 1.0, patch releases contain corrections that do not materially change existing knowledge bases. Minor releases add capabilities or materially change the schema, templates, or operating rules. Version 1.0 will indicate that the starter's public contract is stable.

Each release includes a target-state manifest and a cumulative ledger of adjacent version transitions. The migration tool can move directly across skipped releases by composing that ledger, while downloading and installing only the selected final release. Each new release carries the prior ledger unchanged and appends one transition from the preceding stable release.

### License

The original starter-kit files are licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

Third-party material and content later added under `raw/` or `wiki/` remain subject to their applicable rights and licenses. The pinned OKF materials retain the provenance recorded in [`references/okf/v0.2/UPSTREAM.md`](references/okf/v0.2/UPSTREAM.md).


### Migration

Migration is user-initiated and uses stable Git release tags. One command downloads the selected release, composes every required adjacent transition, backs up only files it might modify, and installs the final operating kit:

```bash
python3 references/migrate.py --target latest
```

The manifest permanently protects `.git/`, `.migration/`, `raw/`, `wiki/`, and unknown files. It marks `references/local-settings.md` for a target-structured merger: the target template defines the permitted sections and fields, and only compatible existing values are retained. Removed settings stay available in the backup but are not recreated. The [Migrate operation](references/operations.md#migrate) completes that merger, applies documented mechanical frontmatter compatibility changes, and runs the automated checks once. Concept bodies are left for optional, batched Maintenance.

#### Upgrading from v0.1.0

Version 0.1.0 predates the migration command and manifest. Download and review `references/migrate.py` from the immutable `v0.2.0` release, then run that copy against the existing knowledge base:

```bash
python3 /path/to/v0.2.0/references/migrate.py --root /path/to/knowledge-base --target 0.2.0
```

The v0.2.0 manifest reconstructs v0.1.0 starter ownership from its versioned transition, so the same engine handles this bootstrap and later migrations.
