import pytest
from fastapi.testclient import TestClient
from agent_api import create_app
def test_health_and_success():
 c=TestClient(create_app(lambda p:p.upper()))
 assert c.get("/health/live").status_code==200
 assert c.get("/health/ready").json()=={"status":"ready"}
 r=c.post("/runs",json={"prompt":"hello"})
 assert r.status_code==200 and r.json()=={"result":"HELLO"}
def test_strict_request_validation():
 c=TestClient(create_app(lambda p:p))
 assert c.post("/runs",json={"prompt":""}).status_code==422
 assert c.post("/runs",json={"prompt":"x","extra":1}).status_code==422
 assert c.post("/runs",json={"prompt":12}).status_code==422
def test_agent_error_is_sanitized():
 def fail(p):raise RuntimeError("secret key")
 r=TestClient(create_app(fail)).post("/runs",json={"prompt":"task"})
 assert r.status_code==502 and r.json()["detail"]=="agent execution failed"
 assert "secret" not in r.text
def test_invalid_agent_and_response():
 with pytest.raises(TypeError):create_app(None)
 c=TestClient(create_app(lambda p:{"not":"text"}))
 assert c.post("/runs",json={"prompt":"x"}).status_code==502
