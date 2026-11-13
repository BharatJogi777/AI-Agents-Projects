# Security, Governance, and Evaluation

Measure and improve agent security, reliability, privacy, and quality with repeatable tests and evidence.

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


## Implemented projects (AG-401–AG-405)

| ID | Project | Implementation |
|---|---|---|
| AG-401 | Agent threat modeling assistant | [Open project](../09-security-evaluation/01-agent-threat-modeling-assistant) |
| AG-402 | Prompt injection test harness | [Open project](../09-security-evaluation/02-prompt-injection-test-harness) |
| AG-403 | Indirect prompt injection evaluator | [Open project](../09-security-evaluation/03-indirect-prompt-injection-evaluator) |
| AG-404 | Jailbreak regression suite | [Open project](../09-security-evaluation/04-jailbreak-regression-suite) |
| AG-405 | Tool permission boundary tester | [Open project](../09-security-evaluation/05-tool-permission-boundary-tester) |


## Implemented projects (AG-406–AG-410)

| ID | Project | Implementation |
|---|---|---|
| AG-406 | Tool argument fuzz tester | [Open project](../09-security-evaluation/06-tool-argument-fuzz-tester) |
| AG-407 | Tool output poisoning detector | [Open project](../09-security-evaluation/07-tool-output-poisoning-detector) |
| AG-408 | Memory poisoning detector | [Open project](../09-security-evaluation/08-memory-poisoning-detector) |
| AG-409 | Sensitive data redaction middleware | [Open project](../09-security-evaluation/09-sensitive-data-redaction-middleware) |
| AG-410 | PII detection and masking agent | [Open project](../09-security-evaluation/10-pii-detection-and-masking-agent) |
