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

| AG-206 | Pull request review assistant | `06-pull-request-review-assistant` |
| AG-207 | Bug reproduction planner | `07-bug-reproduction-planner` |
| AG-208 | Issue triage classifier | `08-issue-triage-classifier` |
| AG-209 | Issue-to-plan agent | `09-issue-to-plan-agent` |
| AG-210 | Feature implementation planner | `10-feature-implementation-planner` |

| AG-211 | Code change proposal agent | `11-code-change-proposal-agent` |
| AG-212 | Patch generation assistant | `12-patch-generation-assistant` |
| AG-213 | Patch validation agent | `13-patch-validation-agent` |
| AG-214 | Unit test generator | `14-unit-test-generator` |
| AG-215 | Integration test planner | `15-integration-test-planner` |

| AG-216 | Property-based test generator | `16-property-based-test-generator` |
| AG-217 | Regression test selector | `17-regression-test-selector` |
| AG-218 | Flaky test investigator | `18-flaky-test-investigator` |
| AG-219 | Test failure diagnosis agent | `19-test-failure-diagnosis-agent` |
| AG-220 | Coverage gap analyst | `20-coverage-gap-analyst` |

| AG-216 | Property-based test generator | `16-property-based-test-generator` |
| AG-217 | Regression test selector | `17-regression-test-selector` |
| AG-218 | Flaky test investigator | `18-flaky-test-investigator` |
| AG-219 | Test failure diagnosis agent | `19-test-failure-diagnosis-agent` |
| AG-220 | Coverage gap analyst | `20-coverage-gap-analyst` |
| AG-221 | Static analysis explanation agent | `21-static-analysis-explanation-agent` |
| AG-222 | Linter remediation assistant | `22-linter-remediation-assistant` |
| AG-223 | Type error diagnosis agent | `23-type-error-diagnosis-agent` |
| AG-224 | Dependency upgrade planner | `24-dependency-upgrade-planner` |
| AG-225 | Dependency vulnerability explainer | `25-dependency-vulnerability-explainer` |


## Implemented projects (AG-226–AG-235)

| ID | Project | Implementation |
|---|---|---|
| AG-226 | License compliance assistant | [26-license-compliance-assistant](26-license-compliance-assistant/) |
| AG-227 | API contract drift detector | [27-api-contract-drift-detector](27-api-contract-drift-detector/) |
| AG-228 | OpenAPI spec reviewer | [28-openapi-spec-reviewer](28-openapi-spec-reviewer/) |
| AG-229 | Database migration reviewer | [29-database-migration-reviewer](29-database-migration-reviewer/) |
| AG-230 | SQL query review assistant | [30-sql-query-review-assistant](30-sql-query-review-assistant/) |
| AG-231 | Performance hotspot investigator | [31-performance-hotspot-investigator](31-performance-hotspot-investigator/) |
| AG-232 | Go code review assistant | [32-go-code-review-assistant](32-go-code-review-assistant/) |
| AG-233 | Python code review assistant | [33-python-code-review-assistant](33-python-code-review-assistant/) |
| AG-234 | TypeScript code review assistant | [34-typescript-code-review-assistant](34-typescript-code-review-assistant/) |
| AG-235 | Concurrency bug investigator | [35-concurrency-bug-investigator](35-concurrency-bug-investigator/) |
