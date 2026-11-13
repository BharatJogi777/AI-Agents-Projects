# Graph Visualization Exporter

AG-191 is a focused orchestration utility. It provides a small, dependency-light implementation that can be embedded in a larger agent runtime.

## Features

- Explicit input validation and predictable failure behavior
- Typed Python interfaces and deterministic behavior
- Unit tests for normal and invalid-input paths

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Usage

See the module docstrings and tests for executable examples. The package intentionally avoids coupling to a specific agent framework.

## Limitations

This is an in-process reference implementation. Persistence, distributed coordination, authentication, and production observability must be supplied by the integrating service.
