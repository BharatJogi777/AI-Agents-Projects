import pytest
from app.contract_drift import detect_drift

def test_detects_both_drift_directions():
    result=detect_drift([{"method":"get","path":"/a"}],[{"method":"GET","path":"/b"}])
    assert result["missing_from_runtime"]==[{"method":"GET","path":"/a"}]
    assert result["undocumented_runtime"]==[{"method":"GET","path":"/b"}]

def test_invalid_path():
    with pytest.raises(ValueError): detect_drift([], [{"method":"GET","path":"a"}])

def test_duplicate_operations_collapse():
    result=detect_drift([{"method":"GET","path":"/a"}]*2,[{"method":"GET","path":"/a"}])
    assert len(result["in_sync"])==1
