# AG-467: Product discovery interview synthesizer

Synthesize supplied customer interview notes into themes, evidence snippets, and open questions.

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
