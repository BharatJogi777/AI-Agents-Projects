# AG-011 — Typed tool registry

A reusable startup-time allowlist that binds a stable tool name to a Pydantic argument model and a trusted Python handler. It exports provider function schemas, rejects invalid or duplicate registrations, validates every invocation again, and constrains tool output before it can be sent back to a model.

## Architecture

- `tool_registry/registry.py`: registration, schema export, strict validation, dispatch, output serialization and limits.
- `tool_registry/errors.py`: distinct configuration-time and invocation-time errors.
- `tool_registry/__init__.py`: stable public package exports.
- `app.py`: compatibility facade for the first tutorial revision.
- `tests/test_registry.py`: isolated tests; no LLM or network required.

## Execution flow

1. Application startup constructs a registry and registers trusted Python handlers with Pydantic argument models.
2. The application calls `freeze()` after registration. Runtime registration is then rejected.
3. The provider receives `provider_schemas()`. These schemas help the model form calls; they are not a security boundary.
4. Model output selects a name. The registry resolves it against the local allowlist.
5. Arguments must be an object and are revalidated with Pydantic strict mode.
6. Only the registered handler runs. Exceptions are wrapped without exposing handler exception text.
7. Results must be JSON-serializable, finite JSON values and fit the configured UTF-8 byte limit.

## Example

```python
from pydantic import BaseModel, ConfigDict
from tool_registry import RegistryLimits, ToolRegistry

class AddArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    left: int
    right: int

registry = ToolRegistry(RegistryLimits(max_tools=16, max_result_bytes=4096))
registry.register("add", "Add two integers.", AddArgs, lambda args: {"sum": args.left + args.right})
registry.freeze()

provider_tools = registry.provider_schemas()
result = registry.execute("add", {"left": 20, "right": 22})
assert result == {"sum": 42}
```

## Run and test

Requires Python 3.12+.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

No model or network is required. Tests are authored; local execution remains pending.

## Security boundaries

The registry is an allowlist and validation boundary, not a sandbox. A registered handler is trusted application code. The registry does not provide user authorization, process isolation, network egress controls, deadlines, cancellation, or transactional side-effect handling. Apply those controls in the execution layer appropriate to each tool. Do not allow an LLM or user request to mutate registrations.
