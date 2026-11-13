from app.redaction import redact, redact_text


def test_redacts_sensitive_keys_recursively():
    data = {"user": {"api_key": "abc123", "name": "Ada"}}
    clean = redact(data)
    assert clean["user"]["api_key"] == "[REDACTED]"
    assert clean["user"]["name"] == "Ada"
    assert data["user"]["api_key"] == "abc123"


def test_redacts_bearer_token():
    assert "[REDACTED]" in redact_text("Authorization: Bearer abc.def")


def test_redacts_key_value_secret():
    assert "supersecret" not in redact_text("password=supersecret")
