from app.rollback import recommend_rollback
import pytest

def test_requires_approval_for_rollback():
    result=recommend_rollback(error_rate=.1,baseline_error_rate=.01,latency_p95_ms=500,baseline_latency_p95_ms=100,impact_minutes=10,rollback_tested=True,data_compatible=True)
    assert result.action=="consider_rollback_with_approval" and result.requires_human_approval

def test_blocks_unready_rollback():
    result=recommend_rollback(error_rate=.1,baseline_error_rate=.01,latency_p95_ms=500,baseline_latency_p95_ms=100,impact_minutes=10,rollback_tested=False,data_compatible=False)
    assert result.action=="hold_and_escalate"
