# Developer and Software Engineering Agents

Assist a software engineering task using repository context and controlled tools. Never apply or merge consequential changes without review.

## Catalogue scope

This track contains 50 project specifications in the root [project catalogue](../docs/PROJECT_CATALOG.md) and machine-readable [JSON catalogue](../catalogue/projects.json). Catalogue entries are not claims of completed implementations.

## Implementation expectations

- Give every project a standalone purpose, explicit inputs and outputs, and a reproducible local run path.
- Keep model calls behind a small adapter; keep validation, permissions, and side effects in deterministic code.
- Add unit tests for normal behavior and important failure paths.
- Document model requirements, resource usage, limitations, and safety boundaries.
- Use the maturity labels in [PROJECT_STANDARD.md](../docs/PROJECT_STANDARD.md).

## Project status

Projects are implemented in priority order. Check the catalogue for current status; do not infer status from a folder existing.

## Implemented projects (AG-201–AG-205)

| ID | Project | Implementation |
|---|---|---|
| AG-201 | Repository onboarding assistant | Bounded repository inventory, entrypoint and manifest discovery, generated-directory exclusions |
| AG-202 | Codebase architecture explainer | Static Python AST analysis of imports, classes, functions, and modules |
| AG-203 | Symbol and dependency explorer | Nested symbol extraction and import dependency discovery |
| AG-204 | Code search assistant | Bounded literal/regex search across source files with line references |
| AG-205 | Pull request summarizer | Unified-diff parsing, per-file change counts, binary-file detection |
