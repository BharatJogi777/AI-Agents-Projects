# Interactive data exploration agent

Deterministic Python reference implementation for **AG-390**. The module works only on explicitly supplied inputs; it does not call external services or perform unattended actions.

## Run

```bash
python -m pytest
```

## Scope and safety

- Validates input before producing results.
- Produces inspectable outputs for a human or downstream workflow.
- Does not send notifications, modify source spreadsheets, publish presentations, or execute generated content.
