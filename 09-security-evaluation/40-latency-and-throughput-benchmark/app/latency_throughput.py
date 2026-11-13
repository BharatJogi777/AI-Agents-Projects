"""Summarize externally measured request durations and throughput."""
from dataclasses import dataclass
from math import isfinite
from typing import Iterable
@dataclass(frozen=True)
class BenchmarkReport:
 sample_count:int; p50_ms:float; p95_ms:float; p99_ms:float; max_ms:float; throughput_rps:float
def _percentile(values:list[float],p:float)->float:
 if len(values)==1:return values[0]
 pos=(len(values)-1)*p; lo=int(pos); hi=min(lo+1,len(values)-1); frac=pos-lo
 return values[lo]+(values[hi]-values[lo])*frac
def summarize_benchmark(latencies_ms:Iterable[float],*,duration_seconds:float,completed_requests:int|None=None)->BenchmarkReport:
 values=list(latencies_ms)
 if not values or any(not isinstance(x,(int,float)) or not isfinite(x) or x<0 for x in values): raise ValueError("latencies must be non-empty finite non-negative numbers")
 if not isinstance(duration_seconds,(int,float)) or not isfinite(duration_seconds) or duration_seconds<=0: raise ValueError("duration_seconds must be positive and finite")
 count=len(values) if completed_requests is None else completed_requests
 if isinstance(count,bool) or not isinstance(count,int) or count<0: raise ValueError("completed_requests must be a non-negative integer")
 ordered=sorted(float(x) for x in values)
 return BenchmarkReport(len(ordered),_percentile(ordered,.50),_percentile(ordered,.95),_percentile(ordered,.99),ordered[-1],count/duration_seconds)
