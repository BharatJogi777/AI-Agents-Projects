"""Benchmark parser implementations with repeatable input cases and correctness checks."""
import time
from dataclasses import dataclass
from typing import Callable,Any

@dataclass(frozen=True)
class BenchmarkResult:
    name:str
    iterations:int
    elapsed_seconds:float
    operations_per_second:float
    correct:bool

def benchmark_parser(name:str,parser:Callable[[str],Any],cases:list[tuple[str,Any]],*,iterations:int=100)->BenchmarkResult:
    if not name or not cases or iterations<1: raise ValueError("name, cases, and positive iterations required")
    expected=[target for _,target in cases]
    for raw,target in cases:
        if parser(raw)!=target: raise ValueError(f"parser {name} failed correctness check")
    started=time.perf_counter()
    for _ in range(iterations):
        for raw,_ in cases: parser(raw)
    elapsed=time.perf_counter()-started
    total=iterations*len(cases)
    return BenchmarkResult(name,total,elapsed,total/elapsed if elapsed else float("inf"),True)

def compare_parsers(parsers:dict[str,Callable[[str],Any]],cases:list[tuple[str,Any]],iterations:int=100)->list[BenchmarkResult]:
    results=[benchmark_parser(name,fn,cases,iterations=iterations) for name,fn in parsers.items()]
    return sorted(results,key=lambda r:r.elapsed_seconds)
