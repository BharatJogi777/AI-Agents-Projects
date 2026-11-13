from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class TaskResult:
    name: str
    value: Any = None
    error: str | None = None

class ParallelExecutor:
    def __init__(self, max_workers: int = 4):
        if max_workers < 1:
            raise ValueError("max_workers must be positive")
        self.max_workers = max_workers

    def run(self, tasks: dict[str, Callable[[], Any]]) -> list[TaskResult]:
        if len(tasks) != len(set(tasks)) or any(not name.strip() for name in tasks):
            raise ValueError("task names must be non-empty and unique")
        results: dict[str, TaskResult] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {pool.submit(fn): name for name, fn in tasks.items()}
            for future in as_completed(futures):
                name = futures[future]
                try:
                    results[name] = TaskResult(name, value=future.result())
                except Exception as exc:
                    results[name] = TaskResult(name, error=str(exc))
        return [results[name] for name in tasks]
