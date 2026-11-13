import pytest
from app.consensus import ConsensusWorkflow, Position

def agent(name, choice):
    return lambda question: Position(name, choice, "reason")

def test_majority_consensus():
    workflow = ConsensusWorkflow({"a": agent("a", "yes"), "b": agent("b", "yes"), "c": agent("c", "no")}, quorum=2)
    result = workflow.run("decide")
    assert result.reached and result.choice == "yes"
    assert result.votes == {"yes": 2, "no": 1}

def test_tie_has_no_consensus():
    workflow = ConsensusWorkflow({"a": agent("a", "yes"), "b": agent("b", "no")}, quorum=1)
    assert workflow.run("decide").choice is None

def test_invalid_quorum_rejected():
    with pytest.raises(ValueError):
        ConsensusWorkflow({"a": agent("a", "yes")}, quorum=2)

def test_agent_identity_must_match_registry_key():
    workflow = ConsensusWorkflow({"alice": agent("bob", "yes")})
    with pytest.raises(ValueError):
        workflow.run("decide")
