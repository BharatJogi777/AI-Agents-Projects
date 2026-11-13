# MCP multi-tenant isolation demo

Demonstrates fail-closed tenant scoping for data access. Every query requires an authenticated principal and a tenant identifier; the repository predicate is always constructed from the principal context, never from model-provided filters alone.

## Setup
Python 3.11+: `pip install -e ".[dev]"`; run `pytest -q`.

## Run
`python -m app.server` starts an in-memory MCP demo.

## Security
This is an application-layer example. Enforce tenant isolation again in the database using row-level security or equivalent controls. Never trust a tenant ID supplied only by the model or end user.
