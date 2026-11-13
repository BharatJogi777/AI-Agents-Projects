import pytest
from app.quality import CallMetrics,analyze_quality
def test_flags_multiple_quality_issues():
 r=analyze_quality(CallMetrics(60,10,100,220,40))
 assert r["quality"]=="poor" and len(r["issues"])==3
def test_accepts_good_metrics():
 assert analyze_quality(CallMetrics(60,0,1000,50,5))["issues"]==[]
def test_rejects_invalid_packet_counts():
 with pytest.raises(ValueError): analyze_quality(CallMetrics(60,11,10,50,5))
