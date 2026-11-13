from app.autoscaling import recommend_scaling
import pytest

def test_recommends_scale_out_with_high_cpu():
    result=recommend_scaling(current_min=2,current_max=5,desired=3,cpu_percent=90,queue_depth=0)
    assert result.action=="scale_out" and result.requires_approval

def test_rejects_invalid_bounds():
    with pytest.raises(ValueError): recommend_scaling(current_min=5,current_max=2,desired=3,cpu_percent=20,queue_depth=0)
