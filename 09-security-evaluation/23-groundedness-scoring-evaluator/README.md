# AG-423: Groundedness scoring evaluator

Compute a transparent lexical evidence-coverage score over answer sentences. Returns sentence-level support indicators and makes clear that lexical overlap is only a heuristic.

## Design

This project is deterministic and model-provider independent. Supply the model output and evidence explicitly; the evaluator never calls an LLM or treats missing evidence as proof.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

## Scope and limitations

The implementation is a focused evaluation primitive. It does not replace domain-specific review, semantic entailment models, or human approval for consequential decisions.
