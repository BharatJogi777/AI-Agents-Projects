# AG-421: Model output schema conformance suite

Validate model-produced JSON-like values against a deliberately bounded schema subset. Reports every path-level violation without coercing or mutating the input.

## Design

This project is deterministic and model-provider independent. Supply the model output and evidence explicitly; the evaluator never calls an LLM or treats missing evidence as proof.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

## Scope and limitations

The implementation is a focused evaluation primitive. It does not replace domain-specific review, semantic entailment models, or human approval for consequential decisions.
