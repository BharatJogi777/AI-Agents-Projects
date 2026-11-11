# Design notes

## Invariants

1. A session has one application-owned system prompt.
2. User and assistant messages are stored in complete pairs.
3. A new user turn cannot begin until the previous turn receives an assistant response.
4. Only the oldest complete turns are evicted.
5. The system prompt is never evicted.
6. Message length and history length are bounded.

## Why trim complete turns?

Removing an arbitrary message can leave an assistant response without its question or leave an unanswered user message in the retained history. Trimming whole pairs preserves a simpler transcript invariant.

## Why not call this memory?

Conversation history is the recent transcript used to continue one interaction. Long-term memory is a separate capability with explicit extraction, consent, retention, retrieval, and deletion policies. This project intentionally implements neither persistent storage nor cross-session memory.
