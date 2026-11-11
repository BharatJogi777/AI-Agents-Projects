from fastapi.testclient import TestClient

from app.agent import ToolCallingAgent
from app.api import create_app


class FakeClient:
    def chat(self, messages, tools):
        return {"choices": [{"message": {"role": "assistant", "content": "Hello from the fake agent."}}]}


def test_liveness_is_independent_of_provider_readiness():
    client = TestClient(create_app(ToolCallingAgent(FakeClient()), readiness_check=lambda: False))
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_returns_503_when_provider_is_unavailable():
    client = TestClient(create_app(ToolCallingAgent(FakeClient()), readiness_check=lambda: False))
    assert client.get("/health/ready").status_code == 503


def test_readiness_returns_200_when_dependencies_are_ready():
    client = TestClient(create_app(ToolCallingAgent(FakeClient()), readiness_check=lambda: True))
    assert client.get("/health/ready").json() == {"status": "ready"}


def test_agent_endpoint_returns_answer():
    client = TestClient(create_app(ToolCallingAgent(FakeClient())))
    response = client.post("/v1/agent/run", json={"prompt": "Say hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Hello from the fake agent."}


def test_endpoint_rejects_unknown_fields_and_oversized_prompt():
    client = TestClient(create_app(ToolCallingAgent(FakeClient())))
    assert client.post("/v1/agent/run", json={"prompt": "hello", "admin": True}).status_code == 422
    assert client.post("/v1/agent/run", json={"prompt": "x" * 8001}).status_code == 422
