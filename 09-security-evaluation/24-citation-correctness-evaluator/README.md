# AG-424: Citation correctness evaluator

Check citation markers against a supplied source registry, including missing IDs and unused references. It validates traceability, not whether a source semantically proves a claim.

## Design

This project is deterministic and model-provider independent. Supply the model output and evidence explicitly; the evaluator never calls an LLM or treats missing evidence as proof.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

## Scope and limitations

The implementation is a focused evaluation primitive. It does not replace domain-specific review, semantic entailment models, or human approval for consequential decisions.
