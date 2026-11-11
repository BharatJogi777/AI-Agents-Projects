import pytest
from task_decomposer import Task,TaskDecompositionAgent,TaskGraphError,validate_tasks
class Planner:
 def decompose(self,_):return [Task("build","Build"),Task("test","Test",("build",))]
def test_agent_returns_dependency_order():
 assert [t.id for t in TaskDecompositionAgent(Planner()).run("ship feature")]==["build","test"]
def test_cycle_and_missing_dependency_rejected():
 with pytest.raises(TaskGraphError):validate_tasks([Task("a","A",("b",)),Task("b","B",("a",))])
 with pytest.raises(TaskGraphError):validate_tasks([Task("a","A",("missing",))])
def test_prompt_limit_and_duplicate_ids():
 with pytest.raises(ValueError):TaskDecompositionAgent(Planner(),max_objective_chars=2).run("long")
 with pytest.raises(TaskGraphError):validate_tasks([Task("a","A"),Task("a","B")])
