import pytest

from app.history import ConversationHistory


@pytest.fixture
def history():
    return ConversationHistory(
        session_id="session-a",
        system_prompt="You are a helpful assistant.",
        max_turns=2,
        max_message_chars=50,
    )


def add_turn(history, question, answer):
    history.add_user_message(question)
    history.add_assistant_message(answer)


def test_builds_provider_neutral_messages(history):
    add_turn(history, "Hello", "Hi there")

    assert history.build_messages() == [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]


def test_history_is_bounded_by_complete_turns(history):
    add_turn(history, "Q1", "A1")
    add_turn(history, "Q2", "A2")
    add_turn(history, "Q3", "A3")

    messages = history.build_messages()
    assert history.completed_turns == 2
    assert [message["content"] for message in messages] == [
        "You are a helpful assistant.", "Q2", "A2", "Q3", "A3"
    ]


def test_pending_user_message_can_be_included_in_context(history):
    history.add_user_message("New question")

    assert history.build_messages()[-1] == {
        "role": "user",
        "content": "New question",
    }
    assert history.completed_turns == 0


def test_next_user_message_requires_assistant_response(history):
    history.add_user_message("First question")

    with pytest.raises(ValueError, match="assistant response is required"):
        history.add_user_message("Second question")


def test_assistant_message_requires_pending_user(history):
    with pytest.raises(ValueError, match="without a pending user"):
        history.add_assistant_message("Unprompted response")


def test_blank_and_oversized_messages_are_rejected(history):
    with pytest.raises(ValueError, match="cannot be empty"):
        history.add_user_message("  ")
    with pytest.raises(ValueError, match="50-character limit"):
        history.add_user_message("x" * 51)


def test_clear_retains_system_prompt_and_resets_turns(history):
    add_turn(history, "Q", "A")
    history.clear()

    assert history.completed_turns == 0
    assert history.build_messages() == [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


def test_sessions_are_isolated():
    first = ConversationHistory(session_id="one", system_prompt="System one")
    second = ConversationHistory(session_id="two", system_prompt="System two")
    add_turn(first, "private question", "private answer")

    assert "private question" not in str(second.build_messages())


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError, match="session_id"):
        ConversationHistory(session_id=" ", system_prompt="system")
    with pytest.raises(ValueError, match="max_turns"):
        ConversationHistory(session_id="s", system_prompt="system", max_turns=0)
