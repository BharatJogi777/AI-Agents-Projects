import pytest
from app.pod_diagnosis import diagnose_pod

def test_identifies_crash_loop_and_image_pull():
    pod={"metadata":{"name":"api"},"status":{"phase":"Running","containerStatuses":[{"name":"api","state":{"waiting":{"reason":"CrashLoopBackOff"}}},{"name":"sidecar","state":{"waiting":{"reason":"ImagePullBackOff"}}}]}}
    assert {x["reason"] for x in diagnose_pod(pod)} == {"CrashLoopBackOff","ImagePullBackOff"}

def test_rejects_missing_pod_name():
    with pytest.raises(ValueError): diagnose_pod({"metadata":{},"status":{}})

def test_healthy_pod_has_no_findings():
    assert diagnose_pod({"metadata":{"name":"api"},"status":{"phase":"Running","containerStatuses":[{"name":"api","ready":True}]}}) == []
