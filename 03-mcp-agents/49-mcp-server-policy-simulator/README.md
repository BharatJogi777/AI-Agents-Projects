# MCP server policy simulator

Evaluate tool access against explicit allow/deny rules before invoking a handler.

## Run
`python -m pip install -e ".[dev]"`
`pytest`

The simulator is deterministic and fail-closed: unknown principals, unknown tools, and missing grants are denied. Rules can constrain principals, tool names, and required scopes. This is an educational policy engine, not a substitute for identity verification, transport security, or enforcement at every downstream resource.

## Layout
- `app/policy.py`: immutable request and policy models plus evaluator.
- `app/server.py`: example MCP tool showing where authorization belongs.
- `tests/`: allow, deny, scope, and malformed-policy cases.
