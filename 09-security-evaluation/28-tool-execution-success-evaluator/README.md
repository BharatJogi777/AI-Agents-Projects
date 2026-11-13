# Tool Execution Success Evaluator

A deterministic, provider-independent evaluator for agent system quality. Inputs are explicit evaluation records; outputs expose metrics and failure details so regressions can be reproduced.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

## Limitations

Metrics depend on the quality of supplied labels and reference expectations. They are not a substitute for representative datasets, production monitoring, or human review of consequential decisions.
