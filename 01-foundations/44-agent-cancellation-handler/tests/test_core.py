import pytest
from agent_cancellation import *
def test_first_reason_wins():
 t=CancellationToken();assert t.cancel("user stop");assert not t.cancel("timeout")
 assert t.reason=="user stop"
 with pytest.raises(AgentCancelled,match="user stop"):t.checkpoint()
def test_wait_and_injected_clock():
 t=CancellationToken(clock=lambda:123.5);assert not t.wait(0)
 t.cancel("stop");assert t.wait(0) and t.requested_at==123.5
def test_steps_check_between_operations():
 t=CancellationToken();seen=[]
 def first():seen.append(1);t.cancel("stop")
 with pytest.raises(AgentCancelled):run_steps([first,lambda:seen.append(2)],t)
 assert seen==[1]
def test_reason_validation():
 t=CancellationToken();t.cancel(" ");assert t.reason=="cancelled"
 with pytest.raises(TypeError):CancellationToken().cancel(None)
