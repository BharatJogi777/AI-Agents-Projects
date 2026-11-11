import pytest
from app import *
def test_valid_path():
 m=AgentStateMachine()
 for s in [State.RUNNING,State.WAITING,State.RUNNING,State.SUCCEEDED]: m.transition(s)
 assert m.terminal and len(m.history)==5
def test_invalid_and_terminal_transitions():
 m=AgentStateMachine()
 with pytest.raises(InvalidTransition): m.transition(State.SUCCEEDED)
 m.transition(State.CANCELLED)
 with pytest.raises(InvalidTransition): m.transition(State.RUNNING)
