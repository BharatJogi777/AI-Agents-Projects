# Voice conversation agent

## Purpose
Maintain a validated conversation turn history for a voice interface.

## Scope
This package handles transcript metadata only. Audio capture, speech recognition, speech synthesis, and transport are external adapters.

## Run
Python 3.10+.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Safety
Keep a visible mute/stop control, preserve interruption behavior, request consent before recording, and protect transcripts as sensitive user data.
