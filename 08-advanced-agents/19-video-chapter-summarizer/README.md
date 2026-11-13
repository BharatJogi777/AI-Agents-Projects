# Video chapter summarizer

## Purpose
A deterministic, reviewable foundation for video chapter summarizer.

## Scope
Processes supplied structured observations or OCR/transcription output. It does not decode images or video, call vision models, or publish catalogue content.

## Run
Python 3.10+, no runtime dependencies.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
See `app/chapters.py` and `tests` for examples.

## Safety and limitations
Extraction confidence is not proof of correctness. Preserve source references, validate units and timestamps, flag uncertain data, and require human review before financial use or publication.
