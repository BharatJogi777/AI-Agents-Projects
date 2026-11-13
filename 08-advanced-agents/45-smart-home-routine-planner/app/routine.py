"""Plan smart-home routines with device allowlists and conflict detection."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class RoutineAction:
    device_id: str
    command: str
    scheduled_minute: int

def validate_routine(actions: Iterable[RoutineAction], *, allowed_devices: set[str], allowed_commands: set[str]) -> tuple[RoutineAction,...]:
    items=tuple(actions)
    if not items:
        raise ValueError("routine must contain at least one action")
    seen=set()
    for action in items:
        if action.device_id not in allowed_devices:
            raise ValueError(f"device is not allowlisted: {action.device_id}")
        if action.command not in allowed_commands:
            raise ValueError(f"command is not allowlisted: {action.command}")
        if not 0 <= action.scheduled_minute < 1440:
            raise ValueError("scheduled_minute must be in [0, 1439]")
        key=(action.device_id,action.scheduled_minute)
        if key in seen:
            raise ValueError("conflicting actions for same device and minute")
        seen.add(key)
    return tuple(sorted(items,key=lambda a:(a.scheduled_minute,a.device_id)))

def approval_summary(actions: Iterable[RoutineAction], *, allowed_devices: set[str], allowed_commands: set[str]) -> list[str]:
    return [f"{a.scheduled_minute//60:02d}:{a.scheduled_minute%60:02d} {a.device_id} -> {a.command}" for a in validate_routine(actions,allowed_devices=allowed_devices,allowed_commands=allowed_commands)]
