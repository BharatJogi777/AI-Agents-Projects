from fastapi.testclient import TestClient
from app.agent import ToolCallingAgent
from app.api import create_app

class FakeClient:
    def chat(self, messages, tools):
        return {"choices": [{"message": {"role": "assistant", "content": "Hello from the fake agent."}}]}

def test_liveness():
    client = TestClient(create_app(ToolCallingAgent(FakeClient())))
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_agent_endpoint_returns_answer():
    client = TestClient(create_app(ToolCallingAgent(FakeClient())))
    response = client.post("/v1/agent/run", json={"prompt": "Say hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Hello from the fake agent."}

def test_endpoint_rejects_unknown_fields_and_oversized_prompt():
    client = TestClient(create_app(ToolCallingAgent(FakeClient())))
    assert client.post("/v1/agent/run", json={"prompt": "hello", "admin": True}).status_code == 422
    assert client.post("/v1/agent/run", json={"prompt": "x" * 8001}).status_code == 422
