from app.retrieval import retrieve_parallel

def test_parallel_results_keep_input_order_and_capture_errors():
    results=retrieve_parallel({"first":lambda:1,"bad":lambda:1/0,"last":lambda:3},max_workers=3)
    assert [r.source for r in results] == ["first","bad","last"]
    assert results[0].value == 1 and "ZeroDivisionError" in results[1].error and results[2].value == 3

def test_invalid_workers():
    import pytest
    with pytest.raises(ValueError): retrieve_parallel({},max_workers=0)
