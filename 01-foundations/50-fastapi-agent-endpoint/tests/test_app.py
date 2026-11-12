from fastapi.testclient import TestClient
from app import create_app
def test_health_and_success():
 c=TestClient(create_app(lambda p:"processed: "+p));assert c.get("/health").status_code==200
 r=c.post("/runs",json={"prompt":"hello"});assert r.status_code==200 and r.json()=={"result":"processed: hello"}
def test_validation_and_sanitized_failure():
 c=TestClient(create_app(lambda p:(_ for _ in ()).throw(RuntimeError("secret"))))
 assert c.post("/runs",json={"prompt":"","extra":1}).status_code==422
 r=c.post("/runs",json={"prompt":"ok"});assert r.status_code==502 and "secret" not in r.text
