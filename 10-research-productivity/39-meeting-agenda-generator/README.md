# AG-489: Meeting agenda generator

Turn a stated meeting objective and participant-submitted topics into a timed agenda with a clear outcome for each item.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The generator validates the agenda against the meeting duration and does not send invitations or schedule meetings. Tests are authored but have not been executed in this repository workflow.
