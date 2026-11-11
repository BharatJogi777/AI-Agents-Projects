"""Backward-compatible facade; use stop_policy for new code."""
from stop_policy import InvalidAgentState,LoopDetector,StopDecision,evaluate_stop,fingerprint_state
__all__=["InvalidAgentState","LoopDetector","StopDecision","evaluate_stop","fingerprint_state"]
