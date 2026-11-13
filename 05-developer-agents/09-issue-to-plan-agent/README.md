# Issue-to-Plan Agent

Converts a software issue into a traceable implementation plan with acceptance criteria, impacted-area clues, test ideas, risks, and unresolved questions. It distinguishes statements present in the issue from recommendations.

## Run
```bash
pip install -e ".[dev]"
python -m app.issue_plan
pytest
```

## Safety
No repository files are changed and no commands are executed. The generated plan is a proposal; engineers must confirm scope, architecture, and acceptance criteria before implementation.
