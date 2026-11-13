"""Evaluate recorded retry attempts; performs no HTTP requests."""
from dataclasses import dataclass
from math import isfinite
from typing import Iterable
@dataclass(frozen=True)
class ResponseAttempt:
 status_code:int; retry_after_seconds:float|None=None
@dataclass(frozen=True)
class RetryReport:
 succeeded:bool; attempts:int; total_wait_seconds:float; rate_limited:int; exhausted:bool
def evaluate_retries(attempts:Iterable[ResponseAttempt],*,max_attempts:int,max_retry_after_seconds:float)->RetryReport:
 if isinstance(max_attempts,bool) or not isinstance(max_attempts,int) or max_attempts<1: raise ValueError("max_attempts must be a positive integer")
 if not isinstance(max_retry_after_seconds,(int,float)) or not isfinite(max_retry_after_seconds) or max_retry_after_seconds<0: raise ValueError("retry-after bound must be finite and non-negative")
 rows=tuple(attempts)
 if not rows or len(rows)>max_attempts: raise ValueError("attempt count must be between one and max_attempts")
 wait=0.0; limited=0
 for i,row in enumerate(rows):
  if isinstance(row.status_code,bool) or not isinstance(row.status_code,int) or not 100<=row.status_code<=599: raise ValueError("invalid HTTP status")
  if row.status_code==429:
   limited+=1; delay=0 if row.retry_after_seconds is None else row.retry_after_seconds
   if not isinstance(delay,(int,float)) or not isfinite(delay) or delay<0 or delay>max_retry_after_seconds: raise ValueError("retry-after outside allowed bound")
   wait+=delay
  elif 200<=row.status_code<300: return RetryReport(True,i+1,wait,limited,False)
  elif i<len(rows)-1: raise ValueError("only rate limits may be retried by this evaluator")
 return RetryReport(False,len(rows),wait,limited,len(rows)==max_attempts)
