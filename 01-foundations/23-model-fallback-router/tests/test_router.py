import pytest
from app import ModelFallbackRouter,NoModelAvailable
from registry import CapabilityRegistry,ModelCapabilities
class Provider:
    def __init__(self,result=None,fail=False): self.result=result; self.fail=fail; self.calls=[]
    def chat(self,model,prompt):
        self.calls.append(model)
        if self.fail: raise ConnectionError()
        return self.result
def setup():
    r=CapabilityRegistry(); r.register(ModelCapabilities("first",("p1",),8000,1000)); r.register(ModelCapabilities("second",("p2",),4000,1000)); return r
def test_fallback():
    p1,p2=Provider(fail=True),Provider("answer")
    result=ModelFallbackRouter(setup(),{"p1":p1,"p2":p2}).generate("question")
    assert result.model_id=="second" and result.attempts==("p1:first","p2:second")
def test_capability_and_provider_order():
    r=CapabilityRegistry(); r.register(ModelCapabilities("tool",("p2",),10000,2000,True))
    result=ModelFallbackRouter(r,{"p2":Provider("ok")}).generate("x",tools=True,provider_order=("p2",),min_context=9000)
    assert result.model_id=="tool"
def test_no_route_and_empty_prompt():
    with pytest.raises(NoModelAvailable): ModelFallbackRouter(setup(),{}).generate("x")
    with pytest.raises(ValueError): ModelFallbackRouter(setup(),{}).generate(" ")
