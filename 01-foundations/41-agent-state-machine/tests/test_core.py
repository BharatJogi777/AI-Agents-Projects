import pytest
from agent_state_machine import *
def test_valid_path_and_history():
 m=AgentStateMachine()
 for s in (State.RUNNING,State.WAITING,State.RUNNING,State.SUCCEEDED):m.transition(s)
 assert m.terminal and [e.sequence for e in m.history()]==[1,2,3,4,5]
def test_invalid_and_terminal_transitions():
 m=AgentStateMachine()
 with pytest.raises(InvalidTransition):m.transition(State.SUCCEEDED)
 m.transition(State.CANCELLED)
 with pytest.raises(InvalidTransition):m.transition(State.RUNNING)
def test_snapshot_and_reason_validation():
 m=AgentStateMachine();h=m.history();m.transition(State.RUNNING)
 assert len(h)==1
 with pytest.raises(ValueError):m.transition(State.WAITING,"x"*501)
