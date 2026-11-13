# Orchestration and Multi-Agent Systems

Coordinate bounded steps and specialist workers with explicit state, retries, cancellation, and human approval where needed.

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

## Implemented project batches

| ID | Project | Status |
|---|---|---|
| AG-151 | [Sequential workflow agent](01-sequential-workflow-agent/) | In progress — implementation and tests authored; execution verification pending |
| AG-152 | [Conditional workflow router](02-conditional-workflow-router/) | In progress — implementation and tests authored; execution verification pending |
| AG-153 | [Parallel task executor](03-parallel-task-executor/) | In progress — implementation and tests authored; execution verification pending |
| AG-154 | [Fan-out fan-in research workflow](04-fan-out-fan-in-research-workflow/) | In progress — implementation and tests authored; execution verification pending |
| AG-155 | [Planner-executor graph](05-planner-executor-graph/) | In progress — implementation and tests authored; execution verification pending |
| AG-156 | [Plan-and-replan workflow](06-plan-and-replan-workflow/) | In progress — implementation and tests authored; execution verification pending |
| AG-157 | [Supervisor-worker team](07-supervisor-worker-team/) | In progress — implementation and tests authored; execution verification pending |
| AG-158 | [Hierarchical agent team](08-hierarchical-agent-team/) | In progress — implementation and tests authored; execution verification pending |
| AG-159 | [Researcher-writer-editor team](09-researcher-writer-editor-team/) | In progress — implementation and tests authored; execution verification pending |
| AG-160 | [Debate and consensus workflow](10-debate-and-consensus-workflow/) | In progress — implementation and tests authored; execution verification pending |
