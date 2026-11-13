"""Run independent retrieval functions concurrently and synthesize in input order."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class RetrievalResult:
    source: str
    value: Any = None
    error: str | None = None

def retrieve_parallel(retrievers: dict[str, Callable[[], Any]], *, max_workers: int = 4) -> list[RetrievalResult]:
    if max_workers < 1:
        raise ValueError("max_workers must be positive")
    if len(retrievers) != len(set(retrievers)) or any(not k for k in retrievers):
        raise ValueError("retriever names must be non-empty and unique")
    results: dict[str, RetrievalResult] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(fn): name for name, fn in retrievers.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = RetrievalResult(name, value=future.result())
            except Exception as exc:
                results[name] = RetrievalResult(name, error=f"{type(exc).__name__}: {exc}")
    return [results[name] for name in retrievers]
