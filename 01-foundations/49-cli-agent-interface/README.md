# AG-049 — CLI agent interface

An argparse boundary around an injected callable with prompt limits and predictable exit codes.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

The default is a deterministic echo stub. Inject your model adapter; do not expose arbitrary shell execution to an LLM.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.
