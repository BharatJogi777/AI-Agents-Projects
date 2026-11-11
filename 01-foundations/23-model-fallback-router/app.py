"""Backward-compatible facade; registry remains a separate project dependency."""
from model_router import ChatProvider,ModelFallbackRouter,NoModelAvailable,RouteResult
__all__=["ChatProvider","ModelFallbackRouter","NoModelAvailable","RouteResult"]
