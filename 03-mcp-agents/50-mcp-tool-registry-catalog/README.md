# MCP tool registry catalog

Maintain a deterministic catalog of tool metadata, ownership, versions, and input schemas. The catalog is designed to be populated from trusted server discovery results and reviewed before clients invoke tools.

## Run
`python -m pip install -e ".[dev]"`
`pytest`

This project does not execute tools or trust remote descriptions as policy. It validates metadata shape, rejects duplicate server/tool identities, supports filtering, and exports a JSON-compatible snapshot.

## Layout
- `app/registry.py`: validated registry and query operations.
- `app/server.py`: exposes a read-only catalog snapshot over MCP.
- `tests/`: duplicate, validation, filtering, and export behavior.
