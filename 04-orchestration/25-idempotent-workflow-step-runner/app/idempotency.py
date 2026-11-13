import hashlib, json
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class StepOutcome:
    key: str
    result: Any
    replayed: bool

class IdempotentStepRunner:
    def __init__(self):
        self._results: dict[str, str] = {}

    @staticmethod
    def make_key(workflow_id: str, step_name: str, input_data: dict[str, Any]) -> str:
        if not workflow_id.strip() or not step_name.strip(): raise ValueError("workflow and step names required")
        raw=json.dumps(input_data,sort_keys=True,separators=(",",":"),default=str)
        return hashlib.sha256(f"{workflow_id}:{step_name}:{raw}".encode()).hexdigest()

    def run(self, workflow_id: str, step_name: str, input_data: dict[str, Any], action: Callable[[], Any]) -> StepOutcome:
        if not isinstance(input_data,dict): raise TypeError("input_data must be an object")
        key=self.make_key(workflow_id,step_name,input_data)
        if key in self._results:
            return StepOutcome(key,json.loads(self._results[key]),True)
        result=action()
        encoded=json.dumps(result,sort_keys=True,default=str)
        self._results[key]=encoded
        return StepOutcome(key,result,False)
