# Wiki Agent Instructions

Keep the knowledge base simple, traceable, and conformant with OKF v0.2. Add structure only when it improves retrieval or reuse.

## Rule Ownership

Keep each rule in its owning file and link to it elsewhere instead of restating it: `schema.md` owns structure, `writing-style.md` owns concept bodies, `operations.md` owns workflows, and `local-settings.md` owns knowledge-base-specific choices.

## Select The Operation

Read [Operating Principles](references/operations.md#operating-principles), then select and read the appropriate operation below.

### Core Operations

- Use [Ingest](references/operations.md#ingest) when the user asks to add material or knowledge to the wiki, or accepts an agent's suggestion.
- Use [Query](references/operations.md#query) for ordinary questions and tasks, including hypothetical setup questions and one-off calculations.
- Use [Research](references/operations.md#research) only when the user asks the agent to find sources for the knowledge base.
- Use [Maintenance](references/operations.md#maintenance) for user-requested or scheduled maintenance of existing material.

### Other Operations

- Use [Review](references/operations.md#review) to inspect knowledge-base material or changes without modifying them.
- Use [External Access And Connector Setup](references/operations.md#external-access-and-connector-setup) when the user asks to establish or change external access.
- Use [Attested Computation](references/operations.md#attested-computation) for a governed, reusable calculation.
