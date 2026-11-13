"""Generate reproducible synthetic task cases from explicit templates."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TaskCase:
    case_id: str
    prompt: str
    expected: str

def generate_tasks(templates: list[dict[str,str]], *, count: int, seed: int = 0) -> tuple[TaskCase,...]:
    import random
    if not isinstance(count,int) or isinstance(count,bool) or count < 0: raise ValueError("count must be a non-negative integer")
    if not templates or any(not isinstance(t,dict) or not all(isinstance(t.get(k),str) and t[k].strip() for k in ("prompt","expected")) for t in templates):
        raise ValueError("templates must include non-empty prompt and expected strings")
    rng=random.Random(seed); result=[]
    for i in range(count):
        template=templates[rng.randrange(len(templates))]
        result.append(TaskCase(f"synthetic-{i+1:05d}",template["prompt"],template["expected"]))
    return tuple(result)
