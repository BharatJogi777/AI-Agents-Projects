import pytest
from app.approval import Approval, ApprovalGraph, Decision

def test_action_runs_only_after_approval():
    calls = []
    graph = ApprovalGraph(lambda: calls.append("ran") or "done")
    assert graph.request("r1").status == "pending"
    assert calls == []
    result = graph.decide(Approval("r1", Decision.APPROVE, "reviewer"))
    assert result.status == "approved" and result.value == "done" and calls == ["ran"]

def test_rejection_never_runs_action():
    calls = []
    graph = ApprovalGraph(lambda: calls.append(1))
    graph.request("r")
    assert graph.decide(Approval("r", Decision.REJECT, "human")).status == "rejected"
    assert not calls

def test_duplicate_decision_rejected():
    graph = ApprovalGraph(lambda: None)
    graph.request("r")
    graph.decide(Approval("r", Decision.REJECT, "human"))
    with pytest.raises(RuntimeError):
        graph.decide(Approval("r", Decision.APPROVE, "human"))
