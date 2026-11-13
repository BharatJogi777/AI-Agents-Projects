# Adversarial test case generator

Generate a small, bounded set of harmless text perturbations to test input robustness and normalization behavior.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

The generated cases are test inputs only; this utility does not execute tools, send requests, or perform security exploitation.
