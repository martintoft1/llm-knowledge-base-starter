# Wiki Agent Instructions

Keep the knowledge base simple, traceable, and conformant with OKF v0.2. Add structure only when it improves retrieval or reuse.

## Read First

Read these in order:

1. `README.md` for the overview, architecture, and source map.
2. `references/local-settings.md` for purpose, scope, terminology, writing style, approved tags, sensitive-data rules, history mode, and actor identifiers.
3. `references/schema.md` for the wiki schema: bundle structure, frontmatter, actors, links and paths, types, body headings, and tag rules.
4. `references/operations.md` for operating principles, core and specialized operations, approval boundaries, history-mode behavior, and validation.
5. `references/writing-style.md` for reusable body-writing rules before creating or substantially rewriting bodies.
6. `wiki/index.md` and relevant local indexes when they exist.

After this initial orientation, use each reference file's direct section links to revisit only the local settings needed for the current task.

The pinned `references/okf/v0.2/SPEC.md` remains authoritative, but routine work should not require reading it in full. Read the relevant SPEC sections when the wiki schema does not cover a field or edge case, when resolving ambiguity, during a formal base-OKF conformance audit, or before changing the schema or OKF version.

## Boundaries

- Only `wiki/` is the OKF bundle. Keep original evidence under `raw/` and operating files in the approved root and `references/` paths.
- Existing raw files are immutable to agents. Adding a raw source on the user's behalf requires approval.
- Use progressive autonomy for ordinary wiki work. Follow `references/operations.md` for actions that require approval.
- Validate base OKF and wiki-schema conformance before finalizing any wiki operation. A failed required check blocks completion.
- Preserve unknown OKF types and fields. Report broken links without treating them as an OKF conformance failure.
- Never invent sources, verification, access, or attestation. Mark uncertainty and conflict clearly.
- Do not add top-level files or directories outside the approved repository layout without a scoped proposal and approval.
- Keep `wiki/log.md` current. Follow Git rules when Git is enabled.
- Treat `references/initialization/BOOTSTRAP.md` as an archive, not active operating instructions. Routine operation must not depend on the archived bootstrap.
