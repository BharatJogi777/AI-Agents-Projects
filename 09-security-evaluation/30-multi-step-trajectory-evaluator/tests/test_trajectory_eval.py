import pytest
from app.trajectory_eval import evaluate_trajectory

TRANS={("start","plan"),("plan","act"),("act","done")}

def test_valid_completed_trajectory():
    r=evaluate_trajectory(["start","plan","act","done"],terminal_states={"done"},allowed_transitions=TRANS,max_steps=4)
    assert r.score == 1 and not r.invalid_transitions

def test_invalid_transition_detected():
    r=evaluate_trajectory(["start","done"],terminal_states={"done"},allowed_transitions=TRANS,max_steps=3)
    assert r.invalid_transitions == (0,) and r.score == 0

def test_step_budget_enforced():
    assert not evaluate_trajectory(["a","b"],terminal_states={"b"},allowed_transitions={("a","b")},max_steps=1).within_step_budget

def test_negative_budget_rejected():
    with pytest.raises(ValueError): evaluate_trajectory([],terminal_states=set(),allowed_transitions=set(),max_steps=-1)
