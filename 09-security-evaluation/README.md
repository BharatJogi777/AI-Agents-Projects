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


## Implemented projects (AG-411–AG-415)

| ID | Project | Implementation |
|---|---|---|
| AG-411 | Secret leakage scanner for prompts | [Open project](../09-security-evaluation/11-secret-leakage-scanner-for-prompts) |
| AG-412 | Credential exposure test suite | [Open project](../09-security-evaluation/12-credential-exposure-test-suite) |
| AG-413 | Policy-as-code tool gateway | [Open project](../09-security-evaluation/13-policy-as-code-tool-gateway) |
| AG-414 | Human approval policy engine | [Open project](../09-security-evaluation/14-human-approval-policy-engine) |
| AG-415 | High-impact action classifier | [Open project](../09-security-evaluation/15-high-impact-action-classifier) |

## Implemented projects (AG-416–AG-420)

| ID | Project | Implementation |
|---|---|---|
| AG-416 | Least-privilege tool planner | [Open](./16-least-privilege-tool-planner/) |
| AG-417 | Tenant isolation test harness | [Open](./17-tenant-isolation-test-harness/) |
| AG-418 | Cross-tenant memory leakage test | [Open](./18-cross-tenant-memory-leakage-test/) |
| AG-419 | Agent identity and authorization demo | [Open](./19-agent-identity-and-authorization-demo/) |
| AG-420 | Audit trail integrity verifier | [Open](./20-audit-trail-integrity-verifier/) |

## Implemented projects (AG-421–AG-425)

| ID | Project | Implementation |
|---|---|---|
| AG-421 | Model output schema conformance suite | [Project](21-model-output-schema-conformance-suite/) |
| AG-422 | Hallucination evaluation harness | [Project](22-hallucination-evaluation-harness/) |
| AG-423 | Groundedness scoring evaluator | [Project](23-groundedness-scoring-evaluator/) |
| AG-424 | Citation correctness evaluator | [Project](24-citation-correctness-evaluator/) |
| AG-425 | Answer relevance evaluator | [Project](25-answer-relevance-evaluator/) |

## Implemented projects (AG-426–AG-430)

| ID | Project | Implementation |
|---|---|---|
| AG-426 | Retrieval quality benchmark | [Project](26-retrieval-quality-benchmark/) |
| AG-427 | Tool selection accuracy evaluator | [Project](27-tool-selection-accuracy-evaluator/) |
| AG-428 | Tool execution success evaluator | [Project](28-tool-execution-success-evaluator/) |
| AG-429 | Agent task completion evaluator | [Project](29-agent-task-completion-evaluator/) |
| AG-430 | Multi-step trajectory evaluator | [Project](30-multi-step-trajectory-evaluator/) |

## Implemented projects (AG-431–AG-435)

| ID | Project | Implementation |
|---|---|---|
| AG-431 | LLM-as-judge calibration harness | [Project](31-llm-as-judge-calibration-harness/) |
| AG-432 | Human evaluation review queue | [Project](32-human-evaluation-review-queue/) |
| AG-433 | Golden dataset regression runner | [Project](33-golden-dataset-regression-runner/) |
| AG-434 | Synthetic task dataset generator | [Project](34-synthetic-task-dataset-generator/) |
| AG-435 | Adversarial test case generator | [Project](35-adversarial-test-case-generator/) |

## Implemented projects (AG-436–AG-440)

| ID | Project | Implementation |
|---|---|---|
| AG-436 | Agent red-team scenario runner | [Project](36-agent-red-team-scenario-runner/) |
| AG-437 | Model drift monitor | [Project](37-model-drift-monitor/) |
| AG-438 | Prompt version regression tester | [Project](38-prompt-version-regression-tester/) |
| AG-439 | Cost and token usage evaluator | [Project](39-cost-and-token-usage-evaluator/) |
| AG-440 | Latency and throughput benchmark | [Project](40-latency-and-throughput-benchmark/) |

## Implemented projects (AG-441–AG-445)

| ID | Project | Implementation |
|---|---|---|
| AG-441 | Model comparison benchmark | [Project](41-model-comparison-benchmark/) |
| AG-442 | Small-model capability benchmark | [Project](42-small-model-capability-benchmark/) |
| AG-443 | Fallback behavior test suite | [Project](43-fallback-behavior-test-suite/) |
| AG-444 | Timeout and cancellation test suite | [Project](44-timeout-and-cancellation-test-suite/) |
| AG-445 | Rate limit resilience test suite | [Project](45-rate-limit-resilience-test-suite/) |

## Implemented projects (AG-446–AG-450)

| ID | Project | Implementation |
|---|---|---|
| AG-446 | Data retention policy checker | [Project](46-data-retention-policy-checker/) |
| AG-447 | Audit log privacy filter | [Project](47-audit-log-privacy-filter/) |
| AG-448 | Model risk register generator | [Project](48-model-risk-register-generator/) |
| AG-449 | Agent deployment readiness assessor | [Project](49-agent-deployment-readiness-assessor/) |
| AG-450 | Agent incident response playbook | [Project](50-agent-incident-response-playbook/) |
