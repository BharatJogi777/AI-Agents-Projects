"""Backward-compatible facade; use result_normalizer for new code."""
from result_normalizer import NormalizationPolicy, SENSITIVE_KEYS, normalize_tool_result
__all__=["NormalizationPolicy","SENSITIVE_KEYS","normalize_tool_result"]
