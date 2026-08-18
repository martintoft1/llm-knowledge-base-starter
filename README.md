# LLM Wiki

LLM Wiki is a starter kit for a file-based knowledge base that humans own and AI agents help build and maintain.

It targets OKF v0.2 and follows Karpathy's LLM Wiki pattern: keep original evidence separate, let agents turn it into connected Markdown knowledge, and keep improving that knowledge through normal use.

## Architecture

```text
<knowledge-base-root>/
├── raw/                    # Immutable original sources in native formats
├── wiki/                   # The OKF v0.2 knowledge bundle
│   ├── index.md            # Bundle navigation and OKF version
│   ├── log.md              # Mandatory update history
│   └── *.md                # Knowledge concepts
├── README.md               # Purpose, scope, and local settings
├── AGENTS.md               # Agent entry point
├── CLAUDE.md               # Optional Claude adapter
├── references/             # Standard and local operating rules
└── templates/              # Reusable concept and body templates
```

Only `wiki/` is the OKF bundle. Every concept in it is UTF-8 Markdown with OKF frontmatter. `raw/` keeps PDFs, images, spreadsheets, exports, and other evidence in their useful native formats. Existing raw files are immutable to agents.

Root files operate the system. They are not part of the bundle. New root paths require approval.

## Sources Of Authority

Use these sources in order:

1. [`references/okf/v0.2/SPEC.md`](references/okf/v0.2/SPEC.md) is the pinned, unmodified OKF v0.2 specification. It defines OKF terms and semantics.
2. [`references/schema.md`](references/schema.md) defines this starter kit's stricter local profile.
3. [`references/operations.md`](references/operations.md) defines workflows, history, validation, and authority.
4. [`references/writing-style.md`](references/writing-style.md) defines local editorial guidance.
5. `AGENTS.md` and optional adapters provide short entry points.

Local rules may narrow the format, but they must not redefine reserved OKF fields incompatibly.

## Local Settings

- **Purpose:** <what this knowledge base helps with>
- **Scope:** <material and questions that belong here>
- **Outside scope:** <material and questions that do not belong here>
- **Local terminology:** <domain terms or naming conventions>
- **Sensitive data:** <what must not be stored or exposed>
- **History mode:** <Git and log, or log only>

## How Knowledge Grows

Agents ingest approved sources into useful concepts, answer questions from traceable evidence, and file all durable or potentially useful findings back into the wiki. Minor procedural or disposable answers stay in chat. New concepts are created only when the knowledge is distinct; generic Q&A files are not used.

The starter kit adds these choices around OKF and the LLM Wiki pattern:

- **Progressive structure:** Start with the least structure needed. Add types, tags, headings, and folders only when they improve retrieval or reuse.
- **Simplicity-first writing:** Use plain language and only as much structure as the material needs.
- **Flat organization and living tags:** Prefer links and maintained tags over early folder hierarchies.
- **Progressive autonomy:** Let agents handle ordinary wiki work while reserving risky actions for human approval.
- **Tailored setup:** Discover the purpose, boundaries, sources, history mode, and useful templates during initialization.
- **Epistemic safeguards:** Separate evidence, interpretation, inference, uncertainty, and unresolved conflict. Never invent provenance.
- **Repository governance:** Keep a controlled root, protect sensitive data, and ask about external systems only when relevant.

The one-concept-per-document rule, raw/wiki separation, Markdown, provenance, links, indexes, logs, and agent neutrality come from OKF or Karpathy's pattern rather than these local additions.

## Authority And History

Under progressive autonomy, agents may create and update normal concepts, links, sources, indexes, and logs. Approval is required for destructive or broad structural work, changing the pinned standard or local rules, adding raw sources on the user's behalf, and new or increased external access. Agents never modify existing raw sources.

`wiki/log.md` is mandatory. Git is strongly recommended because it adds diffs, attribution, and rollback, but it is not required. In log-only mode, rollback is unavailable and substantive replacement or structural changes need stricter approval.

## Initialize A Wiki

Ask an agent with filesystem access to follow `BOOTSTRAP.md`. It gathers only decisions that affect the result, proposes the exact initialization, writes after approval, and validates the complete bundle before finishing.

`BOOTSTRAP.md` is the initialization entry point. It is not copied into generated knowledge bases.

## Editable Settings

- Purpose, scope, exclusions, terminology, sensitive-data rules, and history mode: this `README.md`.
- Format profile and local types: `references/schema.md`.
- Workflows and approval boundaries: `references/operations.md`.
- Writing guidance: `references/writing-style.md`.
- Reusable bodies: `templates/page-bodies/`.
- Navigation and history: `wiki/index.md` and `wiki/log.md`, when initialized.
