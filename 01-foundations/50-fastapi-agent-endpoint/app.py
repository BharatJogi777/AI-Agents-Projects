"""Compatibility facade; implementation lives in agent_api."""
from agent_api import Agent,AgentRequest,AgentResponse,HealthResponse,create_app
app=create_app(lambda prompt:f"Received task: {prompt}")
__all__=["Agent","AgentRequest","AgentResponse","HealthResponse","create_app","app"]
