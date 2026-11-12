import pytest
from app.token_counting import FixedTokenCounter
from app.truncation import ContextMessage, ContextTruncator, InvalidConversation, TruncationConfig

def planner(counts, budget=100):
    return ContextTruncator(FixedTokenCounter(counts), TruncationConfig(budget + 20, 10, 10))

def test_keeps_tool_call_and_all_results_as_one_atomic_turn():
    messages = [
        ContextMessage("system", "policy"),
        ContextMessage("user", "question", "t1"),
        ContextMessage("assistant", "", "t1", tool_call_ids=("call-a", "call-b")),
        ContextMessage("tool", "result-a", "t1", tool_call_id="call-a"),
        ContextMessage("tool", "result-b", "t1", tool_call_id="call-b"),
        ContextMessage("assistant", "final", "t1"),
        ContextMessage("user", "next", "t2"),
    ]
    result = planner({m.content: 1 for m in messages}).truncate(messages)
    assert result.messages == tuple(messages)

def test_drops_whole_tool_turn_when_result_is_too_large():
    messages = [
        ContextMessage("system", "policy"),
        ContextMessage("user", "question", "t1"),
        ContextMessage("assistant", "", "t1", tool_call_ids=("call-a",)),
        ContextMessage("tool", "large-result", "t1", tool_call_id="call-a"),
        ContextMessage("assistant", "final", "t1"),
        ContextMessage("user", "current", "t2"),
    ]
    counts = {"policy": 1, "question": 2, "large-result": 100, "final": 2, "current": 1, "": 0}
    result = planner(counts, budget=10).truncate(messages)
    assert [m.role for m in result.messages] == ["system", "user"]
    assert result.dropped_turn_ids == ("t1",)
    assert result.estimated_tokens <= result.input_budget

def test_rejects_tool_result_without_matching_call():
    messages = [ContextMessage("user", "question", "t1"), ContextMessage("tool", "result", "t1", tool_call_id="unknown"), ContextMessage("assistant", "final", "t1"), ContextMessage("user", "current", "t2")]
    with pytest.raises(InvalidConversation, match="matching pending tool call"):
        planner({m.content: 1 for m in messages}).truncate(messages)

def test_rejects_unresolved_tool_call():
    messages = [ContextMessage("user", "question", "t1"), ContextMessage("assistant", "", "t1", tool_call_ids=("call-a",)), ContextMessage("assistant", "final", "t1"), ContextMessage("user", "current", "t2")]
    with pytest.raises(InvalidConversation, match="resolve"):
        planner({m.content: 1 for m in messages}).truncate(messages)
