from app.certificates import check_expiry
from datetime import date
import pytest

def test_detects_expired_certificate():
    result=check_expiry([{"id":"cert-1","expires_on":"2025-12-31"}],today=date(2026,1,1))
    assert result[0].severity=="critical"

def test_rejects_bad_date():
    with pytest.raises(ValueError): check_expiry([{"id":"c","expires_on":"tomorrow"}],today=date(2026,1,1))
