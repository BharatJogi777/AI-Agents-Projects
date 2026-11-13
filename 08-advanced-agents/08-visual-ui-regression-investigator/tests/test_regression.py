import pytest
from app.regression import VisualMetrics,investigate
def test_detects_regression():
 a=VisualMetrics("old","aaa",10,1.0); b=VisualMetrics("new","bbb",9,0.9)
 r=investigate(a,b)
 assert r["changed"] and r["element_count_delta"]==-1 and r["review_required"]
def test_identical_metrics_pass():
 a=VisualMetrics("a","hash",3,1.0)
 assert not investigate(a,a)["review_required"]
def test_rejects_invalid_score():
 with pytest.raises(ValueError): investigate(VisualMetrics("a","h",1,1),VisualMetrics("b","h",1,1.5))
