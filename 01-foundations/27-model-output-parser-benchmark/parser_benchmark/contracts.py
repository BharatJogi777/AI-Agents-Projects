from dataclasses import dataclass
@dataclass(frozen=True)
class BenchmarkResult:
    name:str
    iterations:int
    elapsed_seconds:float
    operations_per_second:float
    correct:bool
