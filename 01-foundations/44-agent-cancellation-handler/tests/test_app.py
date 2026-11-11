import pytest
from app import *
def test_checkpoint():
 t=CancellationToken(); t.checkpoint(); t.cancel("user request")
 with pytest.raises(AgentCancelled,match="user request"): t.checkpoint()
def test_first_reason_wins():
 t=CancellationToken(); assert t.cancel("first") and not t.cancel("second") and t.reason=="first"
