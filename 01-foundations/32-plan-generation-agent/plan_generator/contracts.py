from dataclasses import dataclass
@dataclass(frozen=True)
class PlanStep:
    id:str
    action:str
    expected_outcome:str
@dataclass(frozen=True)
class Plan:
    objective:str
    steps:tuple[PlanStep,...]
