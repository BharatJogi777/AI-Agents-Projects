import pytest
from app import parse_function_call,dispatch_function_call,FunctionCallError
def payload(args): return {"id":"call_1","function":{"name":"lookup","arguments":args}}
def test_parse_json_and_dict_arguments():
    assert parse_function_call(payload('{"query":"x"}'),allowed_names={"lookup"}).arguments=={"query":"x"}
    assert parse_function_call(payload({"query":"y"}),allowed_names={"lookup"}).arguments=={"query":"y"}
def test_reject_invalid_or_unapproved_calls():
    for item,allowed in [(payload("{"),{"lookup"}),(payload("[]"),{"lookup"}),(payload("{}"),set()),({"id":"","function":{}},{"lookup"})]:
        with pytest.raises(FunctionCallError): parse_function_call(item,allowed_names=allowed)
def test_argument_size_limit():
    with pytest.raises(FunctionCallError): parse_function_call(payload('{"x":"'+("a"*50)+'"}'),allowed_names={"lookup"},max_argument_chars=10)
def test_dispatch_is_allowlisted():
    call=parse_function_call(payload({"query":"x"}),allowed_names={"lookup"})
    assert dispatch_function_call(call,{"lookup":lambda a:a["query"]})=="x"
    with pytest.raises(FunctionCallError): dispatch_function_call(call,{})
