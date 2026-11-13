# AG-102 — MCP server resource browser

Expose read-only operational records as MCP resources. This project demonstrates resource discovery and URI-based reads, while keeping the data access layer independent of the MCP transport.

## What it demonstrates

- Registering a URI-template resource with the MCP Python SDK.
- Resolving a resource URI to a deterministic JSON representation.
- Separating resource lookup and validation from transport code.
- Returning useful errors for malformed and unknown resource identifiers.
- Testing domain behavior without starting an MCP host.

## Architecture

```text
MCP host/client
  | resources/list + resources/read
  v
app.server (FastMCP resource adapter)
  |
  v
app.services.order_resources
  |
  v
app.repositories.orders (read-only fixture repository)
```

## Requirements and setup

Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Run

Launch from this directory:

```bash
python -m app.server
```

The server uses stdio. An MCP-compatible host should launch it as a child process. Do not print application logs to stdout; stdout is reserved for JSON-RPC messages.

## Resource contract

- URI template: `orders://{order_id}`
- Example: `orders://ORD-1001`
- Media type: `application/json`
- Content: order ID, status, item count, and currency.
- Unknown IDs are rejected; no arbitrary file, network, or database access is performed.

## Security boundaries

The fixture repository is read-only. The URI parameter is validated before lookup. In a production deployment, enforce tenant-level authorization before returning a resource, avoid placing secrets in resource contents, and audit reads at the host or transport boundary. Resource URIs are identifiers, not authorization tokens.

## Project structure

```text
app/
  repositories/orders.py
  services/order_resources.py
  server.py
tests/
  test_order_resources.py
```
