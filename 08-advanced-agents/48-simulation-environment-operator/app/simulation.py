"""Validate and sequence simulation commands as a dry-run plan."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Command:
    operation: str
    parameters: tuple[tuple[str,str], ...]

ALLOWED={"load_scenario","set_parameter","run_steps","collect_metrics","reset"}
def build_plan(commands: Iterable[Command], *, allowed_parameters: set[str], max_commands: int=25) -> list[dict[str,object]]:
    items=list(commands)
    if not items or len(items)>max_commands or max_commands<1:
        raise ValueError("command count outside permitted range")
    plan=[]
    for i,command in enumerate(items,1):
        if command.operation not in ALLOWED:
            raise ValueError(f"unsupported operation: {command.operation}")
        params=dict(command.parameters)
        if len(params)!=len(command.parameters):
            raise ValueError("duplicate command parameters")
        if command.operation=="set_parameter" and (len(params)!=1 or not set(params)<=allowed_parameters):
            raise ValueError("set_parameter requires exactly one allowlisted parameter")
        if command.operation=="run_steps":
            try: steps=int(params.get("steps",""))
            except ValueError as exc: raise ValueError("run_steps requires integer steps") from exc
            if not 1<=steps<=10000: raise ValueError("steps must be in [1, 10000]")
        plan.append({"sequence":i,"operation":command.operation,"parameters":params,"status":"not_executed"})
    return plan
