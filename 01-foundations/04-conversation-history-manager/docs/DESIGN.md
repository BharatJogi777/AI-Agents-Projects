# Architecture and design

## Responsibilities

- API routes: HTTP contracts, status codes and pagination limits.
- Pydantic schemas: reject unknown fields and constrain input sizes.
- ConversationService: session lifecycle, turn ordering and bounded-history policy.
- ConversationRepository: parameterized SQL and persistence operations.
- Database: SQLite schema, foreign keys, WAL mode and busy timeout.

## Data model

The conversations table stores a UUID identifier, application-owned system prompt, turn limit and timestamps. The messages table stores ordered user/assistant messages. A foreign key cascades deletion. An index on conversation_id and message id supports ordered history reads.

## Turn state machine

    READY -- user message --> PENDING_USER
    PENDING_USER -- assistant message --> COMPLETE
    COMPLETE -- trim oldest complete pairs --> READY

The service rejects consecutive user messages and assistant messages without a pending user. Trimming occurs after an assistant message, so a pending user turn is not evicted.

## Persistence and concurrency

SQLite keeps the project self-contained. Each repository operation opens its own connection. Foreign keys, WAL mode and a 10-second busy timeout are enabled. SQL values are parameterized. This is a local single-node design; use PostgreSQL for multi-node services or sustained concurrent writes.

## Security boundaries

- UUIDs are identifiers, not authorization.
- There is no authentication or tenant ownership. Keep the API on localhost/private networks until authorization is implemented.
- System prompts are set at conversation creation; callers cannot append system/developer roles.
- Avoid logging conversation content. Define retention, deletion, backup and encryption policies before production use.

## Context construction

History returns the system prompt separately from ordered messages. The calling agent combines them for model input. Message count is not a token budget; token-aware truncation is a separate concern.
