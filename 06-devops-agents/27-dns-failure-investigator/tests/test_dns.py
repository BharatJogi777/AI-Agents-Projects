from app.dns import investigate_dns
import pytest

def test_detects_servfail():
    assert investigate_dns([{"hostname":"api.example.test","status":"SERVFAIL"}])[0].severity=="high"

def test_rejects_unknown_status():
    with pytest.raises(ValueError): investigate_dns([{"hostname":"x.test","status":"BROKEN"}])
