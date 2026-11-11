# 04 — Conversation History Manager

**Catalogue ID:** AG-004  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local test execution pending.  
**Runtime:** Python 3.12+  
**External services:** None required

## Goal

Maintain a bounded conversation context for one session. The manager stores completed user/assistant turns, keeps the system prompt pinned, and evicts the oldest complete turns when the configured limit is exceeded.

This is **conversation history**, not long-term user memory. It is in-memory and disappears when the process exits.

## Architecture

~~~text
Session ID + system prompt
          |
          v
ConversationHistory
          |
          +--> validate message size and turn order
          +--> store complete user/assistant turns
          +--> trim oldest turns over max_turns
          |
          v
build_messages()
          |
          v
Provider-neutral chat message list
~~~

## Setup

~~~bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
~~~

## Run

~~~bash
python -m app.main
python -m app.main --max-turns 2
~~~

The demo adds four turns and prints only the most recent number of turns configured, plus the pinned system message.

## Use it in code

~~~python
from app.history import ConversationHistory

history = ConversationHistory(
    session_id="chat-123",
    system_prompt="You are a helpful backend engineering tutor.",
    max_turns=8,
)

history.add_user_message("Explain Python async.")
# Send history.build_messages() to your model adapter.
history.add_assistant_message("async lets a coroutine suspend while waiting...")
~~~

The assistant message is added only after the model returns. The next user message is rejected until the pending user turn has an assistant response, keeping the stored history structurally consistent.

## Tests

~~~bash
pytest
~~~

Tests cover message construction, complete-turn trimming, pending turns, ordering errors, message limits, clearing, configuration validation, and session isolation. No model or network is needed.

## Important design boundaries

- **Session isolation:** create a separate ConversationHistory instance per conversation. A web service must map authenticated users to authorized session IDs; never trust a client-supplied session ID without authorization.
- **Bounded context:** max_turns limits message count, not model tokens. A later token-budget component should estimate tokens for the chosen model.
- **No persistence:** this example does not survive restarts or coordinate multiple API workers.
- **No long-term memory:** do not silently carry information between sessions.
- **Tool calls:** this minimal manager stores only user/assistant turns. A production tool-calling transcript needs explicit tool-call and tool-result message types with validation.

## Production extensions

Add a persistent store with tenant/session authorization, TTL and deletion policy, token-aware trimming, concurrency control, encryption where appropriate, and observability that avoids logging sensitive conversation content.
