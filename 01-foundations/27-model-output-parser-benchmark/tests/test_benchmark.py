import json,pytest
from app import benchmark_parser,compare_parsers
def test_benchmark_checks_correctness_and_counts():
    cases=[('{"x":1}',{"x":1}),('{"x":2}',{"x":2})]
    result=benchmark_parser("json",json.loads,cases,iterations=3)
    assert result.iterations==6 and result.correct and result.operations_per_second>0
def test_wrong_parser_fails_before_timing():
    with pytest.raises(ValueError): benchmark_parser("bad",lambda _:None,[("x",1)])
def test_compare_sorts_by_elapsed_time():
    out=compare_parsers({"json":json.loads},[('{"a":true}',{"a":True})],2)
    assert len(out)==1 and out[0].name=="json"
def test_invalid_benchmark_inputs():
    with pytest.raises(ValueError): benchmark_parser("",json.loads,[("{}",{})])
