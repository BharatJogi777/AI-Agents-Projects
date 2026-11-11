"""Backward-compatible facade; use sse_parser for new code."""
from sse_parser import ChatCompletionStreamParser,StreamEvent,StreamProtocolError
__all__=["ChatCompletionStreamParser","StreamEvent","StreamProtocolError"]
