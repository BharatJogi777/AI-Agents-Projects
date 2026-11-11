"""Compatibility facade. New code should import task_decomposer."""
from task_decomposer import Task,TaskGraphError,validate_tasks,Decomposer,TaskDecompositionAgent
__all__=["Task","TaskGraphError","validate_tasks","Decomposer","TaskDecompositionAgent"]
