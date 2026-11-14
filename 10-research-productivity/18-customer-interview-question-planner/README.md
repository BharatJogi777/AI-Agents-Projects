# AG-468: Customer interview question planner

Create neutral, non-leading customer interview questions from validated research objectives.

## Scope

This deterministic module processes only information supplied by the caller. It does not conduct interviews, infer unstated facts, or contact customers. Review the output with product and research stakeholders before using it in a roadmap.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Example

See the module docstring and tests for the input contract and examples.
