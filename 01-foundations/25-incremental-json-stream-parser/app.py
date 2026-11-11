"""Backward-compatible facade; use json_stream for new code."""
from json_stream import IncrementalJSONDecoder,IncrementalJSONError
__all__=["IncrementalJSONDecoder","IncrementalJSONError"]
