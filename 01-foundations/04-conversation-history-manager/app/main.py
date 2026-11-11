import argparse
import json

from app.history import ConversationHistory


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Demonstrate bounded, session-scoped conversation history."
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=3,
        help="Maximum number of completed user/assistant turns to retain.",
    )
    args = parser.parse_args()

    history = ConversationHistory(
        session_id="demo-session",
        system_prompt="You are a concise programming tutor.",
        max_turns=args.max_turns,
    )

    demo_turns = [
        ("What is a Python list?", "A list is an ordered, mutable collection."),
        ("Can it contain mixed types?", "Yes. A list can contain values of different types."),
        ("How do I add an item?", "Use append() to add an item at the end."),
        ("How do I remove an item?", "Use remove(value) or pop(index)."),
    ]
    for user_text, assistant_text in demo_turns:
        history.add_user_message(user_text)
        history.add_assistant_message(assistant_text)

    print(f"Session: {history.session_id}")
    print(f"Completed turns retained: {history.completed_turns}")
    print(json.dumps(history.build_messages(), indent=2))


if __name__ == "__main__":
    main()
