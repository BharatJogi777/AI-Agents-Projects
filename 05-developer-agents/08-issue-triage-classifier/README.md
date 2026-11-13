# Issue Triage Classifier

A rule-based triage engine that labels issue reports by likely category, urgency, and routing hints. Every classification includes matched evidence and a confidence score so maintainers can override it.

## Run
```bash
pip install -e ".[dev]"
python -m app.triage
pytest
```

## Safety
This is decision support, not an automated close/assign bot. It does not infer user identity or make irreversible changes. Validate labels against the project's own taxonomy before integrating with an issue tracker.
