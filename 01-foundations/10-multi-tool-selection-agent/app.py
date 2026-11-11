"""Compatibility facade; implementation is separated into multi_tool_agent/."""

from multi_tool_agent import MultiToolAgent, OllamaClient, build_tool_registry

__all__ = ["MultiToolAgent", "OllamaClient", "build_tool_registry"]
