# Architecture notes

The project has two deliberately separate layers:

1. **MCP adapter** (`app/server.py`): declares tool names, argument types, descriptions, and stdio transport.
2. **Domain service** (`app/domain/orders.py`): owns validation, decimal arithmetic, and sample order lookup.

The adapter is intentionally thin. A future HTTP API, CLI, or background worker could call the same domain functions without importing the MCP SDK.

## Request lifecycle

1. An MCP host starts `python -m app.server`.
2. The MCP SDK reads JSON-RPC messages from stdin.
3. The SDK validates the published tool schema and calls the selected Python function.
4. The function delegates to the domain service, which validates again at the trust boundary.
5. The result is returned through the MCP protocol on stdout.

The server must not print diagnostics to stdout because stdout is the protocol stream. Use the MCP SDK's logging facilities or stderr for diagnostics.
