# 04 — Persistent Conversation History Manager

**Catalogue ID:** AG-004  
**Difficulty:** Beginner → Intermediate  
**Status:** Implemented API and SQLite persistence; tests authored, execution pending.  
**Runtime:** Python 3.12+  
**External services:** None; SQLite ships with Python.

## What this builds

A session-scoped conversation history service. It persists conversations across process restarts, stores an application-owned system prompt, enforces user/assistant turn ordering, bounds retained history by complete turns, and exposes a versioned FastAPI API.

This is short-term transcript storage, not long-term user memory and not an LLM agent. It does not call a model.

## Architecture

    HTTP request
        |
    FastAPI route + Pydantic contract
        |
    ConversationService (business rules)
        |
    ConversationRepository (parameterized SQL)
        |
    SQLite (WAL, foreign keys, index)

## Project layout

    app/
      api/routes/conversations.py
      schemas.py
      services/conversation_service.py
      storage/database.py
      storage/repository.py
      main.py
    tests/
      conftest.py
      test_api.py
      test_persistence.py
    docs/DESIGN.md

## Setup

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e '.[dev]'

## Run

    uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload

Open http://127.0.0.1:8010/docs for interactive API documentation. The default database is ./data/conversations.db. Override it with CONVERSATION_DB_PATH=/absolute/path/chat.db.

## API examples

Create a conversation:

    curl -X POST http://127.0.0.1:8010/api/v1/conversations \
      -H 'Content-Type: application/json' \
      -d '{"system_prompt":"You are a backend tutor.","max_turns":5}'

Copy the returned id into CONVERSATION_ID:

    export CONVERSATION_ID='<returned-id>'
    curl -X POST "http://127.0.0.1:8010/api/v1/conversations/$CONVERSATION_ID/messages/user" \
      -H 'Content-Type: application/json' -d '{"content":"Explain Python async."}'

    curl -X POST "http://127.0.0.1:8010/api/v1/conversations/$CONVERSATION_ID/messages/assistant" \
      -H 'Content-Type: application/json' -d '{"content":"async lets a coroutine suspend while waiting."}'

    curl "http://127.0.0.1:8010/api/v1/conversations/$CONVERSATION_ID?limit=100&offset=0"

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | /api/v1/conversations | Create a conversation |
| GET | /api/v1/conversations | List conversations (paginated) |
| GET | /api/v1/conversations/{id} | Read system prompt and paginated messages |
| POST | /{id}/messages/user | Append a user message |
| POST | /{id}/messages/assistant | Append assistant response |
| DELETE | /{id}/messages | Clear transcript, retain system prompt |
| DELETE | /{id} | Delete conversation and messages |

Message pages use ascending insertion order. A 409 indicates invalid turn order; 404 indicates an unknown conversation; 422 indicates invalid input.

## Tests

    pytest

The suite covers API lifecycle, turn ordering, bounded complete-turn trimming, pagination, clear/delete, session isolation and persistence after service recreation. Tests are committed but have not been executed here.

## Limitations before production exposure

- No authentication/authorization or tenant ownership. UUIDs are not access control. Keep the API private until identity and ownership checks exist.
- SQLite is single-node; use PostgreSQL for multi-instance services or sustained concurrent writes.
- No encryption, retention scheduler, backup/restore workflow or token-aware context budget.
- The API accepts assistant messages from its caller. In an agent service, only the trusted orchestration layer should append assistant output.
- Add idempotency keys if clients may retry writes after network timeouts.
