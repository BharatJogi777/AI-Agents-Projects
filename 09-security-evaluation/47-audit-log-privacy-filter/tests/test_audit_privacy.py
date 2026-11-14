import pytest
from app.audit_privacy import filter_audit_event
def test_nested_sensitive_values_redacted():
 out=filter_audit_event({"event":"login","email":"person@example.com","meta":{"token":"abc","status":200},"message":"Bearer abc.def"})
 assert out["email"]=="[REDACTED]" and out["meta"]["token"]=="[REDACTED]" and "[REDACTED]" in out["message"] and out["meta"]["status"]==200
def test_input_type_validation():
 with pytest.raises(TypeError): filter_audit_event([])
