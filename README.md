# LLM Knowledge Base Starter

LLM Knowledge Base Starter is a starter kit for a file-based knowledge base that humans own and AI agents help build and maintain.

It targets Google's OKF v0.2 and follows Karpathy's LLM Wiki pattern: keep original evidence separate, let agents turn it into connected Markdown knowledge, and keep improving that knowledge through normal use.

## About

LLM Knowledge Base Starter was created and is maintained by [Martin Toft](https://github.com/martintoft1).

## Architecture

```text
<knowledge-base-root>/
├── raw/                    # Immutable original sources in native formats
│   └── .gitkeep            # Tracked placeholder; not evidence
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
├── references/             # Local settings, standard, and operating rules
└── templates/              # Reusable concept and body templates
```

Only `wiki/` is the OKF bundle. Every concept in it is UTF-8 Markdown with OKF frontmatter. `raw/` keeps PDFs, images, spreadsheets, exports, and other evidence in their useful native formats. Existing raw files are immutable to agents. Its tracked `.gitkeep` file only preserves the empty directory and is not evidence.

Files outside `wiki/` operate or support the system. They are not part of the bundle. Adding top-level files or directories outside this layout requires a scoped proposal and approval.

## Sources Of Authority

Use these sources in order:

1. [`references/okf/v0.2/SPEC.md`](references/okf/v0.2/SPEC.md) is the pinned, unmodified OKF v0.2 specification. It defines OKF terms and semantics.
2. [`references/local-settings.md`](references/local-settings.md) defines the writing style, tag registry, and storage and sharing restrictions.
3. [`references/schema.md`](references/schema.md) defines the wiki schema used by this starter kit.
4. [`references/operations.md`](references/operations.md) defines operating principles, procedures, approval boundaries, history-mode behavior, and validation.
5. [`references/writing-style.md`](references/writing-style.md) defines reusable editorial and body-writing rules.
6. `AGENTS.md` and optional adapters provide short entry points.

Local rules may narrow the format, but they must not redefine reserved OKF fields incompatibly.

The pinned [`references/okf/v0.2/README.md`](references/okf/v0.2/README.md) provides upstream rationale and examples. It is explanatory, not normative; its reference-agent setup is not required here.

## Local Settings

The authoritative settings for this knowledge base live in [`references/local-settings.md`](references/local-settings.md). Its defaults work immediately. Change them only when the knowledge base needs different writing, tags, or storage or sharing restrictions.

## How Knowledge Grows

Agents ingest approved sources into useful concepts and answer questions from traceable evidence. After an ordinary question, an agent may suggest durable knowledge that is likely worth keeping, but it stores that knowledge only after the user accepts. An explicit ingest or update request authorizes ordinary wiki changes. Minor procedural or disposable answers stay in chat.

The starter kit adds these choices around OKF and the LLM Wiki pattern:

- **Progressive structure:** Start with the least structure needed. Add types, tags, headings, and folders only when they improve retrieval or reuse.
- **Simplicity-first writing:** Use plain language and only as much structure as the material needs.
- **Atomic concepts:** Keep independently maintainable knowledge in canonical concept files and connect related concepts with explained links.
- **Flat organization and living tags:** Prefer links and maintained tags over early folder hierarchies.
- **Progressive autonomy:** Let agents handle ordinary wiki work while reserving risky actions for human approval. Consider giving agents more autonomy after they prove that they can work well on their own.
- **Ready to use:** Start with sensible defaults and define purpose, scope, terminology, or other context in ordinary knowledge files only when useful.
- **Epistemic safeguards:** Separate evidence, interpretation, inference, uncertainty, and unresolved conflict. Never invent provenance.
- **Repository governance:** Keep a controlled root, follow the local storage and sharing settings, and ask about external systems only when relevant.

The base one-concept-per-document rule, raw/wiki separation, Markdown, provenance, links, indexes, logs, and agent neutrality come from OKF or Karpathy's pattern. This starter makes the concept boundary more explicit through its atomic-concept rules.

## Authority And History

Under progressive autonomy, agents may create and update normal concepts, links, sources, indexes, and logs when the user directly requests the work or accepts a suggested addition. Approval is required for destructive or broad structural work, changing the pinned standard or local rules, adding raw sources on the user's behalf, and new or increased external access. Agents never modify existing raw sources.

`wiki/log.md` is mandatory. Git is strongly recommended because it adds diffs, attribution, and rollback, but it is not required. In log-only mode, rollback is unavailable and substantive replacement or structural changes need stricter approval.

## Versioning

The starter uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html). [`VERSION`](VERSION) records the current operating-kit version, and [`CHANGELOG.md`](CHANGELOG.md) records notable changes. Public releases use an annotated Git tag named `v<version>` and a matching GitHub Release. The version identifies the operating kit, not the knowledge content that a user later adds.

Before 1.0, patch releases contain corrections that do not materially change existing knowledge bases. Minor releases add capabilities or materially change the schema, templates, or operating rules. Version 1.0 will indicate that the starter's public contract is stable.

## First Use

The repository works immediately. It already includes an empty valid `wiki/` bundle and a tracked `raw/` directory. Before adding knowledge, review [`references/local-settings.md`](references/local-settings.md) and change only what you need.

You can ask an agent with filesystem access:

```text
Review references/local-settings.md with me, keep its defaults unless I ask for a change, then help me start using the knowledge base.
```

## Common Prompts

Use these examples as written or adapt them to the task:

| Task | Prompt |
|---|---|
| Add knowledge | `Ingest the following into the wiki: <text or files>` |
| Ask a question | `Using the knowledge base, answer: <question>` |
| Summarize | `Summarize the following content: <text or files>` |
| Review content | `Review the following content: <text or files>` |
| Correct knowledge | `Update the wiki with this correction: <change>` |
| Review the wiki | `Review the wiki for maintenance issues and propose any changes.` |
| Connect a source | `Help me connect <system or source> to the knowledge base.` |

Summarizing or reviewing does not change the wiki unless the user accepts a suggested addition. Ingesting or updating explicitly authorizes ordinary wiki changes. Other approval boundaries still apply.

## License

The original starter-kit files are licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

Third-party material and content later added under `raw/` or `wiki/` remain subject to their applicable rights and licenses. The pinned OKF materials retain the provenance recorded in [`references/okf/v0.2/UPSTREAM.md`](references/okf/v0.2/UPSTREAM.md).
