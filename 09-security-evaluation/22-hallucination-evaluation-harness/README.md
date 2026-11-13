# AG-422: Hallucination evaluation harness

Compare extracted answer claims with an explicitly supplied evidence set. Classifies claims as supported, contradicted, or unverified; it does not pretend to infer truth from absent evidence.

## Design

This project is deterministic and model-provider independent. Supply the model output and evidence explicitly; the evaluator never calls an LLM or treats missing evidence as proof.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

## Scope and limitations

The implementation is a focused evaluation primitive. It does not replace domain-specific review, semantic entailment models, or human approval for consequential decisions.
