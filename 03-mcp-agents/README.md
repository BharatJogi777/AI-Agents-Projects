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
| AG-105–AG-150 | Remaining MCP projects | Planned |

## How to run AG-101

See [AG-101 README](01-first-mcp-server-with-typed-tools/README.md). It uses the Python MCP SDK over stdio and keeps its order-domain logic independently testable.
