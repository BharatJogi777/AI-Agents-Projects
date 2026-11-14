# AG-488: Focus session planner

Create bounded focus blocks and breaks from task estimates and available time without scheduling outside the supplied window.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The planner is deterministic, uses caller-supplied estimates, and does not interact with calendars or timers. Tests are authored but have not been executed in this repository workflow.
