# AG-101 — First MCP server with typed tools

A small but complete MCP server that exposes deterministic order operations as typed tools. It demonstrates the boundary between an MCP transport and business logic: MCP parses and transports requests; the domain layer validates inputs and calculates results.

## Capabilities

- `calculate_order_total`: validates quantity and unit price, then returns subtotal, tax, and total.
- `get_order_status`: returns a status from a local, read-only sample repository.
- Uses typed Python arguments so MCP can publish tool schemas to clients.
- Keeps business rules independent from the MCP SDK, making them unit-testable without a running server.

It does **not** call an LLM, access a real order database, or modify external systems.

## Architecture

```text
MCP client
   | JSON-RPC over stdio
   v
app.server (FastMCP tool adapter)
   | typed arguments
   v
app.domain.orders (validation + business rules)
   |
   +-- deterministic calculation
   +-- in-memory read-only order fixture
```

## Requirements

- Python 3.11+
- `mcp` Python SDK 1.x
- No API key, hosted model, database, or Docker required

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run the MCP server

```bash
python -m app.server
```

The server uses stdio. Do not start it in a terminal and expect a human-readable prompt; an MCP host launches it as a child process and exchanges JSON-RPC messages through stdin/stdout. Keep stdout reserved for the protocol.

Example MCP client configuration:

```json
{
  "mcpServers": {
    "orders-demo": {
      "command": "python",
      "args": ["-m", "app.server"],
      "cwd": "/absolute/path/to/01-first-mcp-server-with-typed-tools"
    }
  }
}
```

Replace `cwd` with the actual local path.

## Tool contracts

### calculate_order_total

| Argument | Type | Constraint |
|---|---|---|
| quantity | integer | 1–10,000 |
| unit_price | number | greater than 0 and at most 1,000,000 |
| tax_rate | number | 0–1; defaults to 0.18 |

Returns `quantity`, `unit_price`, `subtotal`, `tax`, and `total`, rounded to two decimal places.

### get_order_status

Accepts an order ID such as `ORD-1001`. Returns only known sample records; unknown IDs produce a clear validation error.

## Test

```bash
pytest
```

Tests exercise business logic and invalid inputs without requiring an MCP host or external service.

## Security and operational notes

- The sample order lookup is read-only and uses fixed local fixtures.
- No filesystem, shell, network, or database tools are exposed.
- Input constraints are enforced again in the domain layer; do not rely only on an MCP client honoring the published schema.
- For real integrations, add authentication/authorization at the transport boundary, request IDs, structured audit events, timeouts around downstream calls, and integration tests.
- Never put credentials in the MCP server source or committed environment files.

## Troubleshooting

- **Module not found:** activate the virtual environment and run `python -m pip install -e ".[dev]"`.
- **No visible terminal output:** expected for stdio servers; inspect the MCP host's server logs.
- **Server exits immediately:** check that the host is launching the configured interpreter and working directory.
