# AG-116 — MCP authorization gateway

A fail-closed policy gate between authenticated application principals and MCP tool execution.

## Request flow

1. The host authenticates the caller and constructs a `Principal`.
2. The gateway looks up an exact tool grant.
3. Access is allowed only when the principal is active, has a non-empty subject, and has at least one role in the grant.
4. Every decision emits a minimal audit event; arguments and secrets are never logged.

## Run

```bash
pip install -e '.[dev]'
pytest
```

## Security integration

Resolve identities from a verified authentication layer (for example, validated JWT claims or an internal identity service). Never trust a client-supplied subject or role. Keep grant configuration in reviewed policy files or a policy service, and deny by default when identity or policy lookup fails.

## Limitations

This example is an in-process authorization core, not a complete OAuth/OIDC gateway. Add tenant/resource-level checks, policy versioning, revocation, and durable audit delivery for production.
