# Bug Reproduction Planner

Turns a bug report into a structured, testable reproduction plan. It extracts environment clues, observable symptoms, and explicit reproduction steps without inventing missing details.

## Run
```bash
pip install -e ".[dev]"
python -m app.reproduction
pytest
```

## Design
The planner is deterministic and offline. It separates reported facts from proposed experiments, marks missing information, and prioritizes low-risk steps. It does not run commands or modify the user's environment.

## Limitations
Natural-language extraction is intentionally conservative. A human must validate assumptions, sanitize logs, and approve any command before execution.
