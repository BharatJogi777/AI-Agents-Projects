from app.account_health import summarize_account_health
import pytest

def test_detects_multiple_risks():
    result=summarize_account_health(usage_trend="declining",support_trend="worsening",stakeholder_engagement="weak",renewal_days=20,payment_status="overdue")
    assert result.status=="critical" and len(result.risk_signals)>=4

def test_rejects_negative_renewal_days():
    with pytest.raises(ValueError): summarize_account_health(usage_trend=None,support_trend=None,stakeholder_engagement=None,renewal_days=-1,payment_status=None)
