import pytest
from app.trace_investigation import Span, investigate_trace

def test_finds_errors_slow_spans_and_missing_parent():
    result=investigate_trace([Span("a","root",0,1000),Span("b","db",10,900,"missing","error")])
    assert {x["kind"] for x in result["findings"]} == {"slow","error","missing-parent"}

def test_rejects_duplicate_ids_and_negative_duration():
    with pytest.raises(ValueError): investigate_trace([Span("a","x",0,1),Span("a","y",0,1)])
    with pytest.raises(ValueError): investigate_trace([Span("a","x",2,1)])
