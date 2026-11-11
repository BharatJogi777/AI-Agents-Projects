# Project Implementation Standard

Every project should be understandable, reproducible, testable, and safe by default. The exact architecture can vary; avoid forcing unnecessary infrastructure into small examples.

## Required project README

1. Problem statement and intended user.
2. What the agent can and cannot do.
3. Architecture diagram or sequence flow.
4. Prerequisites and hardware/model expectations.
5. Environment variables with a safe `.env.example`.
6. Exact installation and run commands.
7. API/tool examples and expected output.
8. Test commands and what the tests cover.
9. Failure modes, limitations, and troubleshooting.
10. Security considerations and licence/attribution.

## Suggested Python layout

```text
project-name/
├── app/
│   ├── api/              # HTTP interface, if needed
│   ├── agent/            # orchestration and state transitions
│   ├── llm/              # provider adapters
│   ├── tools/            # typed tools and policy enforcement
│   ├── schemas/          # Pydantic input/output models
│   ├── services/         # deterministic business logic
│   └── core/             # config, logging, errors
├── tests/
│   ├── unit/
│   └── integration/
├── examples/
├── docs/
├── .env.example
├── .gitignore
├── pyproject.toml
├── Dockerfile            # when containerization adds value
├── compose.yaml          # when multiple services are required
└── README.md
```

Small teaching projects may use a simpler layout, but should still separate model calls from deterministic business logic.

## Agent execution contract

- Use explicit typed input and output schemas.
- Keep the agent loop bounded by maximum steps, time, and token/cost budgets.
- Validate every model-proposed tool call before execution.
- Never execute arbitrary model-generated Python, shell, SQL, or URLs without a strict policy boundary.
- Enforce tool-specific permissions and argument validation.
- Use timeouts and classify retryable versus non-retryable errors.
- Make side-effecting tools idempotent where possible.
- Require human approval for destructive, financial, externally visible, or otherwise consequential actions.
- Keep tool results and retrieved content separate from trusted system instructions.
- Return a clear final state: success, needs-approval, partial, or failed.

## Security baseline

- No secrets in source, tests, fixtures, logs, or committed environment files.
- Use least privilege for filesystem, database, cloud, Git, browser, and MCP tools.
- Use allowlists for commands, paths, hosts, and SQL operations.
- Apply request size limits, rate limits, and execution timeouts at service boundaries.
- Treat prompt injection in documents, web pages, issues, and tool output as untrusted input.
- Avoid exposing chain-of-thought; log concise decisions, tool arguments after redaction, and outcomes.
- Add audit records for sensitive tool invocations.
- Document data retention and privacy assumptions.

## Testing baseline

- Unit-test deterministic services, schemas, policies, and tool adapters.
- Mock LLM and external tool responses for deterministic tests.
- Test malformed structured output and unexpected tool names.
- Test timeouts, connection failures, rate limits, and partial failures.
- Test permission-denied and approval-required cases.
- Add integration tests for real local dependencies when applicable.
- Keep tests runnable without paid API credentials by default.

## Observability baseline

- Structured logs with request/run IDs.
- Metrics for latency, errors, retries, token usage, tool calls, and budget exhaustion where available.
- Trace model and tool spans without logging secrets or full sensitive prompts.
- Expose health/readiness endpoints for services.
- Document useful dashboards and alerts for larger projects.

## Configuration and dependencies

- Pin or lock dependencies for reproducible installs.
- Validate configuration at startup.
- Provide safe defaults and fail clearly for missing required settings.
- Keep provider-specific configuration behind adapters where reasonable.
- Document Python/framework compatibility.

## Maturity labels

- **Planned:** concept only.
- **In progress:** implementation underway.
- **Implemented:** main path works and basic tests pass.
- **Verified:** reproducible setup and meaningful failure-path tests pass.
- **Production-oriented:** security, observability, deployment, operations, and resource controls are documented and tested.

Do not use "production-ready" as a marketing label without operational evidence.
