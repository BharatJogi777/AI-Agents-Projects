import pytest
from app.judge_calibration import calibrate_judge

def test_perfect_agreement():
    r=calibrate_judge([1,0.5],[1,0.5])
    assert r.mean_absolute_error == 0 and r.agreement_rate == 1

def test_error_and_tolerance():
    r=calibrate_judge([0.9,0.2],[0.5,0.2],tolerance=0.1)
    assert r.within_tolerance == 1 and r.mean_absolute_error == pytest.approx(0.2)

def test_mismatched_lengths_rejected():
    with pytest.raises(ValueError): calibrate_judge([1],[1,0])

def test_boolean_scores_rejected():
    with pytest.raises(ValueError): calibrate_judge([True],[1])
