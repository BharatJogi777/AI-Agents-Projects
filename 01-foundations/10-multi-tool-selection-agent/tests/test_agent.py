import pytest
from app import MultiToolAgent

class Fake:
    def __init__(self,rs): self.rs=iter(rs); self.calls=[]
    def chat(self,messages,tools): self.calls.append((messages,tools)); return next(self.rs)

def call(name,args):
    return {"message":{"role":"assistant","content":"","tool_calls":[{"function":{"name":name,"arguments":args}}]}}

def test_multi_tool_selection_and_execution():
    f=Fake([call("add_numbers",'{"a":2,"b":3}'),{"message":{"role":"assistant","content":"The sum is 5."}}])
    assert MultiToolAgent(f).run("Add 2 and 3")=="The sum is 5."
    assert len(f.calls[0][1])==3
    assert '"sum": 5.0' in f.calls[1][0][-1]["content"]

def test_unknown_tool_fails_closed():
    f=Fake([call("shell","{}"),{"message":{"role":"assistant","content":"Not available."}}])
    MultiToolAgent(f).run("run shell")
    assert '"ok": false' in f.calls[1][0][-1]["content"]

def test_extra_fields_rejected():
    f=Fake([call("add_numbers",'{"a":2,"b":3,"command":"id"}'),{"message":{"role":"assistant","content":"Bad arguments."}}])
    MultiToolAgent(f).run("add")
    assert '"ok": false' in f.calls[1][0][-1]["content"]

def test_empty_prompt_and_step_limit():
    with pytest.raises(ValueError): MultiToolAgent(Fake([])).run(" ")
    with pytest.raises(RuntimeError,match="exceeded"):
        MultiToolAgent(Fake([call("add_numbers",'{"a":1,"b":2}')]),max_steps=1).run("add")
