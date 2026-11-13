import pytest
from app.rollback import recommend_rollback

def test_customer_impact_triggers_review():
 r=recommend_rollback(error_rate_percent=5,baseline_error_rate_percent=1,latency_p95_ms=100,baseline_latency_p95_ms=90,failed_health_checks=0,customer_impact=True,rollback_available=True)
 assert r.decision=='rollback_review_urgent' and r.requires_human_approval

def test_rejects_negative_metrics():
 with pytest.raises(ValueError): recommend_rollback(error_rate_percent=-1,baseline_error_rate_percent=1,latency_p95_ms=1,baseline_latency_p95_ms=1,failed_health_checks=0,customer_impact=False,rollback_available=True)
