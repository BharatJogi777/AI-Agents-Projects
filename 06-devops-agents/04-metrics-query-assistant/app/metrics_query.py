"""Allowlisted PromQL query construction; never executes queries."""
import re

METRICS={"http_requests_total":"counter","http_request_duration_seconds_bucket":"histogram","process_resident_memory_bytes":"gauge","up":"gauge"}

def build_query(metric: str, *, operation: str = "raw", window: str = "5m", label: str | None = None) -> str:
    if metric not in METRICS: raise ValueError("metric is not in the allowlist")
    if not re.fullmatch(r"[1-9][0-9]*(s|m|h)",window): raise ValueError("window must be a positive duration such as 5m or 1h")
    if label is not None and not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*",label): raise ValueError("invalid label name")
    selector=metric + (f'{{{label}!=""}}' if label else "")
    if operation=="raw": return selector
    if operation=="rate" and METRICS[metric]=="counter": return f"sum(rate({selector}[{window}]))"
    if operation=="p95" and METRICS[metric]=="histogram": return f"histogram_quantile(0.95, sum(rate({selector}[{window}])) by (le))"
    raise ValueError("operation is not compatible with the selected metric")
