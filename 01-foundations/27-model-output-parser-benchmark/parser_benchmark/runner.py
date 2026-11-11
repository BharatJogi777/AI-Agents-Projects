import time
from typing import Callable,Any
from .contracts import BenchmarkResult
def benchmark_parser(name:str,parser:Callable[[str],Any],cases:list[tuple[str,Any]],*,iterations:int=100,warmup:int=1)->BenchmarkResult:
    if not isinstance(name,str) or not name.strip() or not cases or type(iterations) is not int or iterations<1 or type(warmup) is not int or not 0<=warmup<=1000:
        raise ValueError("name, cases, positive iterations, and valid warmup are required")
    for raw,expected in cases:
        if not isinstance(raw,str): raise TypeError("benchmark input must be text")
        if parser(raw)!=expected: raise ValueError(f"parser {name} failed correctness check")
    for _ in range(warmup):
        for raw,_ in cases: parser(raw)
    started=time.perf_counter()
    for _ in range(iterations):
        for raw,_ in cases: parser(raw)
    elapsed=time.perf_counter()-started; total=iterations*len(cases)
    return BenchmarkResult(name,total,elapsed,total/elapsed if elapsed>0 else float("inf"),True)
def compare_parsers(parsers:dict[str,Callable[[str],Any]],cases:list[tuple[str,Any]],iterations:int=100)->list[BenchmarkResult]:
    if not parsers: raise ValueError("at least one parser is required")
    results=[benchmark_parser(name,fn,cases,iterations=iterations) for name,fn in parsers.items()]
    return sorted(results,key=lambda result:(result.elapsed_seconds,result.name))
