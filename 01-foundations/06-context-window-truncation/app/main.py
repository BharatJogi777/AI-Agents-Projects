import json

from app.token_counting import HeuristicTokenCounter
from app.truncation import ContextMessage, ContextTruncator, TruncationConfig


def main() -> None:
    messages = [
        ContextMessage("system", "You are a concise backend engineering assistant."),
        ContextMessage("user", "What is a database index?", "turn-1"),
        ContextMessage("assistant", "An index speeds up lookups by maintaining an additional data structure.", "turn-1"),
        ContextMessage("user", "What is a B-tree?", "turn-2"),
        ContextMessage("assistant", "A B-tree is a balanced tree commonly used by database indexes.", "turn-2"),
        ContextMessage("user", "When should I add a composite index?", "turn-3"),
        ContextMessage("assistant", "When queries commonly filter or sort by multiple columns in a useful order.", "turn-3"),
        ContextMessage("user", "How do I inspect whether PostgreSQL uses it?", "turn-4"),
    ]

    truncator = ContextTruncator(
        HeuristicTokenCounter(chars_per_token=4),
        TruncationConfig(
            context_window_tokens=100,
            reserved_output_tokens=20,
            safety_margin_tokens=8,
            per_message_overhead_tokens=2,
        ),
    )
    result = truncator.truncate(messages)
    print(json.dumps({
        "counting_mode": "heuristic_estimate",
        "warning": "Character-based counts are approximate, not model-tokenizer exact.",
        "input_budget": result.input_budget,
        "estimated_tokens": result.estimated_tokens,
        "remaining_tokens": result.remaining_tokens,
        "retained_messages": [
            {"role": item.role, "turn_id": item.turn_id, "content": item.content}
            for item in result.messages
        ],
        "dropped_turn_ids": list(result.dropped_turn_ids),
    }, indent=2))


if __name__ == "__main__":
    main()
