import pytest

from app.token_counting import FixedTokenCounter
from app.truncation import (
    ContextMessage,
    ContextTruncator,
    InvalidConversation,
    MandatoryContextTooLarge,
    TruncationConfig,
)


def make_truncator(counts, budget=20):
    return ContextTruncator(
        FixedTokenCounter(counts),
        TruncationConfig(
            context_window_tokens=budget + 8,
            reserved_output_tokens=5,
            safety_margin_tokens=3,
        ),
    )


def sample_messages():
    return [
        ContextMessage("system", "system"),
        ContextMessage("user", "u1", "t1"),
        ContextMessage("assistant", "a1", "t1"),
        ContextMessage("user", "u2", "t2"),
        ContextMessage("assistant", "a2", "t2"),
        ContextMessage("user", "current", "t3"),
    ]


def test_preserves_system_current_user_and_newest_whole_turns():
    truncator = make_truncator({
        "system": 3, "u1": 4, "a1": 4, "u2": 4, "a2": 4, "current": 3
    }, budget=18)
    result = truncator.truncate(sample_messages())
    assert [(m.role, m.content) for m in result.messages] == [
        ("system", "system"),
        ("user", "u2"),
        ("assistant", "a2"),
        ("user", "current"),
    ]
    assert result.dropped_turn_ids == ("t1",)
    assert result.estimated_tokens == 14


def test_keeps_all_turns_when_they_fit():
    truncator = make_truncator({
        "system": 1, "u1": 1, "a1": 1, "u2": 1, "a2": 1, "current": 1
    })
    result = truncator.truncate(sample_messages())
    assert len(result.messages) == 6
    assert result.dropped_turn_ids == ()


def test_mandatory_context_overflow_is_explicit():
    truncator = make_truncator({"system": 12, "current": 9}, budget=20)
    with pytest.raises(MandatoryContextTooLarge, match="mandatory context"):
        truncator.truncate([
            ContextMessage("system", "system"),
            ContextMessage("user", "current", "t1"),
        ])


def test_never_keeps_half_a_turn():
    truncator = make_truncator({
        "system": 1, "u1": 4, "a1": 4, "u2": 4, "a2": 4, "current": 3
    }, budget=18)
    result = truncator.truncate(sample_messages())
    retained_ids = [m.turn_id for m in result.messages if m.turn_id]
    assert retained_ids.count("t2") == 2
    assert "t1" not in retained_ids


def test_rejects_unpaired_assistant_or_user_messages():
    truncator = make_truncator({"system": 1, "current": 1})
    with pytest.raises(InvalidConversation):
        truncator.truncate([
            ContextMessage("system", "system"),
            ContextMessage("assistant", "orphan", "t1"),
            ContextMessage("user", "current", "t2"),
        ])


def test_rejects_mismatched_turn_ids():
    truncator = make_truncator({"system": 1, "u": 1, "a": 1, "current": 1})
    with pytest.raises(InvalidConversation, match="share turn_id"):
        truncator.truncate([
            ContextMessage("system", "system"),
            ContextMessage("user", "u", "t1"),
            ContextMessage("assistant", "a", "different"),
            ContextMessage("user", "current", "t2"),
        ])


def test_requires_one_pending_current_user_message():
    truncator = make_truncator({"system": 1})
    with pytest.raises(InvalidConversation, match="current user"):
        truncator.truncate([ContextMessage("system", "system")])


def test_rejects_duplicate_turn_ids():
    truncator = make_truncator({"system": 1, "u": 1, "a": 1, "current": 1})
    with pytest.raises(InvalidConversation, match="unique"):
        truncator.truncate([
            ContextMessage("system", "system"),
            ContextMessage("user", "u", "t1"),
            ContextMessage("assistant", "a", "t1"),
            ContextMessage("user", "u", "t1"),
            ContextMessage("assistant", "a", "t1"),
            ContextMessage("user", "current", "t2"),
        ])


def test_config_rejects_invalid_budget():
    with pytest.raises(ValueError):
        TruncationConfig(10, reserved_output_tokens=8, safety_margin_tokens=2)
