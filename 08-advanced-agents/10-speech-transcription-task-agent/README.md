# Speech transcription task agent

## Purpose
Validate timestamped transcription segments and create a reviewable transcript artifact.

## Scope
No audio decoding or speech-to-text model is bundled. Supply segments from a trusted transcription adapter.

## Run
Python 3.10+.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Safety and limitations
Confidence is an adapter-provided estimate, not a guarantee of correctness. Flag low-confidence segments for human review and obtain consent before recording or retaining audio.
