"""Estimate LLM request costs from usage counts and explicit rates."""
from dataclasses import dataclass
from math import isfinite
from typing import Iterable

@dataclass(frozen=True)
class Usage:
    request_id: str
    input_tokens: int
    output_tokens: int

@dataclass(frozen=True)
class CostReport:
    requests: int
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    over_budget: bool

def evaluate_usage(usages: Iterable[Usage], *, input_rate_per_million: float, output_rate_per_million: float, budget: float) -> CostReport:
    rates = (input_rate_per_million, output_rate_per_million, budget)
    if not all(isinstance(x, (int, float)) and isfinite(x) and x >= 0 for x in rates):
        raise ValueError("rates and budget must be finite non-negative numbers")
    rows = tuple(usages)
    ids = [u.request_id for u in rows]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("request IDs must be non-empty and unique")
    for row in rows:
        if isinstance(row.input_tokens, bool) or isinstance(row.output_tokens, bool) or not isinstance(row.input_tokens, int) or not isinstance(row.output_tokens, int) or row.input_tokens < 0 or row.output_tokens < 0:
            raise ValueError("token counts must be non-negative integers")
    input_total = sum(x.input_tokens for x in rows)
    output_total = sum(x.output_tokens for x in rows)
    cost = (input_total * input_rate_per_million + output_total * output_rate_per_million) / 1_000_000
    return CostReport(len(rows), input_total, output_total, cost, cost > budget)
