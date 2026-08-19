# Wiki Agent Instructions

Keep the knowledge base simple, traceable, and conformant with OKF v0.2. Add structure only when it improves retrieval or reuse.

## Read First

Read these in order:

1. `README.md` for purpose, scope, terminology, and local settings.
2. `references/schema.md` for routine metadata decisions, local types, tags, and validation.
3. `references/operations.md` for workflows, history, validation, and authority.
4. `references/writing-style.md` before creating or substantially rewriting bodies.
5. `wiki/index.md` and relevant local indexes when they exist.

The pinned `references/okf/v0.2/SPEC.md` remains authoritative, but routine work should not require reading it in full. Read the relevant SPEC sections when the local profile does not cover a field or edge case, when resolving ambiguity, during a formal base-OKF conformance audit, or before changing the schema or OKF version.

## Boundaries

- Only `wiki/` is the OKF bundle. Keep original evidence under `raw/` and operating files at the repository root.
- Existing raw files are immutable to agents. Adding a raw source on the user's behalf requires approval.
- Use progressive autonomy for ordinary wiki work. Follow `references/operations.md` for actions that require approval.
- Validate full OKF and local-profile conformance before finalizing any wiki operation. A failed required check blocks completion.
- Preserve unknown OKF types and fields. Report broken links without treating them as an OKF conformance failure.
- Never invent sources, verification, access, or attestation. Mark uncertainty and conflict clearly.
- Do not create new root paths without an explicit proposal and approval.
- Keep `wiki/log.md` current. Follow Git rules when Git is enabled.
- Do not copy `BOOTSTRAP.md` into an initialized wiki.
