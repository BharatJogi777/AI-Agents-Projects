# Text-to-speech response agent

## Purpose
A deterministic, reviewable component for text-to-speech response agent workflows.

## Scope and architecture
`supplied input → validation → structured result → optional external adapter`.
No microphone, speaker, image capture, live transcription, LLM inference, or external service is invoked by this package.

## Requirements and run
Python 3.10+, no runtime dependencies.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
See `app/speech.py` and tests for usage.

## Limitations and safety
Treat transcripts and observations as untrusted. Keep recording consent explicit, redact sensitive information, preserve uncertainty, and require confirmation before any consequential action. Model-generated summaries and interpretations need human review.
