import pytest
from app.canary import analyze_canary

def test_detects_regression():
 r=analyze_canary({'errors':1},{'errors':3},limits={'errors':10})
 assert r.decision=='hold_or_rollback_review'

def test_rejects_different_metric_sets():
 with pytest.raises(ValueError): analyze_canary({'a':1},{'b':2})
