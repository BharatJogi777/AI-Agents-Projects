import pytest
from app import *
class P:
 def decompose(self,o):return [Task("a","Inspect"),Task("b","Deliver",("a",))]
def test_agent():assert len(TaskDecompositionAgent(P()).run("goal"))==2
@pytest.mark.parametrize("ts",[[Task("a","A",("x",))],[Task("a","A",("b",)),Task("b","B",("a",))],[Task("a","A"),Task("a","B")]])
def test_invalid(ts):
 with pytest.raises(ValueError):validate_tasks(ts)
