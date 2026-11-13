# Learning plan coach

Deterministic reference implementation for a traceable, human-supervised workflow. It validates structured inputs and produces an advisory review artifact without taking consequential actions.

## Safety boundaries

- No external service integrations or automatic submissions/bookings.
- Human review is required for consequential decisions.
- For healthcare workflows, this is administrative support only; it does not diagnose, interpret clinical findings, or generate patient advice.

## Run tests

```bash
python -m pytest
```
