# MCP and Tool Integration

Expose or consume typed capabilities through the Model Context Protocol (MCP). This track covers servers, clients, transports, discovery, authorization, resilience, and safe integrations.

## Catalogue scope

This track contains 50 project specifications in the root [project catalogue](../docs/PROJECT_CATALOG.md) and machine-readable [JSON catalogue](../catalogue/projects.json). Catalogue status is authoritative; a directory existing does not mean its implementation is complete.

## Implementation expectations

- Give every project a standalone purpose, explicit inputs and outputs, and a reproducible local run path.
- Keep model calls behind a small adapter; keep validation, permissions, and side effects in deterministic code.
- Add unit tests for normal behavior and important failure paths.
- Document model requirements, resource usage, limitations, and safety boundaries.
- Follow [PROJECT_STANDARD.md](../docs/PROJECT_STANDARD.md).
- Do not mark a project Implemented until its main path and basic tests have been executed successfully.

## Current implementation

| ID | Project | Status |
|---|---|---|
| AG-101 | [First MCP server with typed tools](01-first-mcp-server-with-typed-tools/) | In progress — implementation and tests authored; execution verification pending |
| AG-102 | [MCP server resource browser](02-mcp-server-resource-browser/) | In progress — implementation and tests authored; execution verification pending |
| AG-103 | [MCP prompt-template server](03-mcp-prompt-template-server/) | In progress — implementation and tests authored; execution verification pending |
| AG-104 | [MCP client tool discovery](04-mcp-client-tool-discovery/) | In progress — implementation and tests authored; execution verification pending |
| AG-105 | [MCP client tool invocation](05-mcp-client-tool-invocation/) | In progress — implementation and tests authored; execution verification pending |
| AG-106 | [MCP stdio transport client](06-mcp-stdio-transport-client/) | In progress — implementation and tests authored; execution verification pending |
| AG-107 | [MCP HTTP transport client](07-mcp-http-transport-client/) | In progress — implementation and tests authored; execution verification pending |
| AG-108 | [MCP server health inspector](08-mcp-server-health-inspector/) | In progress — implementation and tests authored; execution verification pending |
| AG-109 | [MCP tool schema validator](09-mcp-tool-schema-validator/) | In progress — implementation and tests authored; execution verification pending |
| AG-110 | [MCP tool namespace manager](10-mcp-tool-namespace-manager/) | In progress — implementation and tests authored; execution verification pending |
| AG-111 | [Multi-server MCP client](11-multi-server-mcp-client/) | In progress — implementation and tests authored; execution verification pending |
| AG-112–AG-132 | MCP integrations and resilience projects | In progress — implementation and tests authored; execution verification pending |
| AG-133 | [Cloud inventory MCP server](33-cloud-inventory-mcp-server/) | In progress — implementation and tests authored; execution verification pending |
| AG-134 | [Kubernetes read-only MCP server](34-kubernetes-read-only-mcp-server/) | In progress — implementation and tests authored; execution verification pending |
| AG-135 | [Docker inspection MCP server](35-docker-inspection-mcp-server/) | In progress — implementation and tests authored; execution verification pending |
| AG-136 | [Observability query MCP server](36-observability-query-mcp-server/) | In progress — implementation and tests authored; execution verification pending |
| AG-137 | [Prometheus MCP integration](37-prometheus-mcp-integration/) | In progress — implementation and tests authored; execution verification pending |
| AG-138 | [Grafana dashboard MCP tool](38-grafana-dashboard-mcp-tool/) | In progress — implementation and tests authored; execution verification pending |
| AG-139 | [Browser search MCP server](39-browser-search-mcp-server/) | In progress — implementation and tests authored; execution verification pending |
| AG-140 | [Internal REST API MCP adapter](40-internal-rest-api-mcp-adapter/) | In progress — implementation and tests authored; execution verification pending |
| AG-141 | [OpenAPI-to-MCP tool generator](41-openapi-to-mcp-tool-generator/) | In progress — implementation and tests authored; execution verification pending |
| AG-142 | [MCP tool contract test harness](42-mcp-tool-contract-test-harness/) | In progress — implementation and tests authored; execution verification pending |
| AG-143 | [MCP server conformance tester](43-mcp-server-conformance-tester/) | In progress — implementation and tests authored; execution verification pending |
| AG-144 | [MCP prompt-injection boundary demo](44-mcp-prompt-injection-boundary-demo/) | In progress — implementation and tests authored; execution verification pending |
| AG-145 | [MCP secret redaction middleware](45-mcp-secret-redaction-middleware/) | In progress — implementation and tests authored; execution verification pending |
| AG-146 | [MCP multi-tenant isolation demo](46-mcp-multi-tenant-isolation-demo/) | In progress — implementation and tests authored; execution verification pending |
| AG-147 | [MCP server deployment template](47-mcp-server-deployment-template/) | In progress — implementation and tests authored; execution verification pending |
| AG-148 | [MCP tool latency monitor](48-mcp-tool-latency-monitor/) | In progress — implementation and tests authored; execution verification pending |
| AG-149 | [MCP server policy simulator](49-mcp-server-policy-simulator/) | In progress — implementation and tests authored; execution verification pending |
| AG-150 | [MCP tool registry catalog](50-mcp-tool-registry-catalog/) | In progress — implementation and tests authored; execution verification pending |
| AG-148–AG-150 | Remaining MCP projects | Planned |

## How to run AG-101

See [AG-101 README](01-first-mcp-server-with-typed-tools/README.md). It uses the Python MCP SDK over stdio and keeps its order-domain logic independently testable.


| AG-115 | MCP cancellation propagation | Shared cancellation signal and task cancellation handling |
| AG-116 | MCP authorization gateway | Fail-closed principal and role authorization with audit events |
| AG-117 | Per-tool permission policy | Exact tool/action/role policy evaluation |


| AG-118 | MCP audit logging server | Allowlisted JSONL audit events and protected file creation |
| AG-119 | MCP rate-limited tool server | Per-principal/tool token bucket limiter |
| AG-120 | MCP pagination tool server | Bounded page metadata and validated offsets |
| AG-121 | MCP file metadata server | Root-confined file metadata inspection |
| AG-122 | Read-only filesystem MCP server | Confined, bounded, read-only workspace access |


| AG-123 | Safe document search MCP server | Principal-filtered retrieval with bounded snippets |
| AG-124 | PostgreSQL read-only MCP server | Conservative SQL gate; production safety relies on DB privileges |
| AG-125 | Redis diagnostics MCP server | Allowlisted INFO metrics and hit-rate calculation |
| AG-126 | Git repository MCP server | Read-only Git metadata inspection with subprocess timeout |
| AG-127 | GitHub issue MCP integration | Typed issue API client with token handling and PR filtering |


| AG-128 | GitHub pull-request MCP assistant | Read-only typed pull-request metadata |
| AG-129 | Jira MCP integration | Read-only typed Jira issue lookup |
| AG-130 | Slack MCP integration | Bounded read-only message search |
| AG-131 | Email drafting MCP server | Validated drafts; sending intentionally excluded |
| AG-132 | Calendar availability MCP server | Timezone-aware free-slot calculation |
