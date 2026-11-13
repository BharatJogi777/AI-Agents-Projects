from app.redaction import redact_sensitive_text

def test_redacts_email_and_secret():
    result = redact_sensitive_text(text="Contact a@example.com api_key=abc123")
    assert "a@example.com" not in result["text"] and "abc123" not in result["text"]

def test_rejects_non_text():
    import pytest
    with pytest.raises(TypeError): redact_sensitive_text(text=42)
