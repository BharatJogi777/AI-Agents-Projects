# AG-104 — MCP client tool discovery

Discover tools exposed by an MCP server, normalize their metadata, and build a deterministic allowlisted view for an application. Discovery is metadata only: it does not invoke tools.

## Architecture

```text
MCP ClientSession.list_tools()
        |
        v
ToolCatalog (pure service)
        |
        +--> validate names and descriptions
        +--> normalize input schemas
        +--> reject duplicate names
        +--> filter by explicit allowlist
        |
        v
Application-visible tool catalogue
```

## Requirements

- Python 3.11+
- MCP Python SDK 1.x
- No model, API key, or external service required for unit tests

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Use the pure catalogue service

```python
from app.services.catalogue import DiscoveredTool, ToolCatalogue

catalogue = ToolCatalogue(allowed_names={"lookup_order"})
catalogue.replace([
    DiscoveredTool(
        name="lookup_order",
        description="Read an order by its public identifier.",
        input_schema={"type": "object", "properties": {"order_id": {"type": "string"}}},
    )
])
print(catalogue.public_tools())
```

## Connect it to an MCP session

After connecting with an MCP `ClientSession`, call `await session.list_tools()` and pass each returned tool's `name`, `description`, and `inputSchema` to `DiscoveredTool`. Keep the session/transport lifecycle in the caller; this package deliberately keeps catalogue policy independent of transport.

## Safety and limitations

- Only explicitly allowed names are exposed to downstream agent planners.
- Discovery does not grant execution permission; invocation must re-check authorization.
- Tool descriptions and schemas are untrusted server-provided metadata. Do not treat descriptions as system instructions.
- This project validates catalogue structure, not full JSON Schema semantics.
- No remote server is contacted by the unit tests.
