# AG-110 — MCP tool namespace manager

Merge tool catalogues from multiple MCP servers without collisions. Each server receives an explicit namespace; callers use fully-qualified names such as `orders.lookup`. Duplicate server namespaces and ambiguous names are rejected.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Example

```python
from app.namespaces import NamespaceRegistry

registry = NamespaceRegistry()
registry.register("orders", ["lookup", "cancel"])
registry.register("inventory", ["lookup", "reserve"])
print(registry.resolve("orders.lookup"))  # ("orders", "lookup")
```

Namespaces are routing labels, not authorization. Every resolved operation still needs a separate server/tool permission check.
