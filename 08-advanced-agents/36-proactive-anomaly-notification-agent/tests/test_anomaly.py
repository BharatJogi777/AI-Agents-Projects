import pytest
from app.anomaly import Metric, detect_anomalies, notification_candidates

def test_detects_spike_and_deduplicates():
    data=[Metric("cpu",10,str(i)) for i in range(4)]+[Metric("cpu",100,"4")]
    alerts=detect_anomalies(data,threshold=3)
    assert len(alerts)==1 and alerts[0].value==100
    assert notification_candidates(alerts,[alerts[0].dedupe_key])==[]

def test_rejects_bad_threshold():
    with pytest.raises(ValueError):
        detect_anomalies([],threshold=0)
