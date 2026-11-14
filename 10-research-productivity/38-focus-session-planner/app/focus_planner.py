"""Build a deterministic focus schedule within a supplied time budget."""
from dataclasses import dataclass

@dataclass(frozen=True)
class FocusBlock:
    task: str
    minutes: int
    break_after: int

def plan_focus_sessions(tasks: list[tuple[str, int]], available_minutes: int, session_minutes: int = 25, break_minutes: int = 5) -> list[FocusBlock]:
    if available_minutes <= 0 or session_minutes <= 0 or break_minutes < 0:
        raise ValueError("available/session minutes must be positive and breaks non-negative")
    if not tasks:
        return []
    if any(not name.strip() or estimate <= 0 for name, estimate in tasks):
        raise ValueError("each task needs a name and positive estimate")
    blocks, remaining = [], available_minutes
    for name, estimate in tasks:
        while estimate > 0 and remaining > 0:
            duration = min(session_minutes, estimate, remaining)
            estimate -= duration
            remaining -= duration
            pause = break_minutes if estimate > 0 and remaining > 0 else 0
            if pause and remaining > pause:
                remaining -= pause
            else:
                pause = 0
            blocks.append(FocusBlock(name, duration, pause))
        if remaining <= 0:
            break
    return blocks
