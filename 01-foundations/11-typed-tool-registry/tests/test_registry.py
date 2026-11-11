import pytest
from pydantic import BaseModel,ConfigDict
from app import ToolRegistry,ToolRegistrationError,ToolExecutionError

class Args(BaseModel):
    model_config=ConfigDict(extra="forbid",strict=True)
    left:int
    right:int

def registry():
    r=ToolRegistry()
    r.register("multiply","Multiply integers.",Args,lambda a:{"product":a.left*a.right})
    return r

def test_schema_and_execution():
    r=registry()
    assert r.names()==("multiply",)
    assert r.provider_schemas()[0]["function"]["name"]=="multiply"
    assert r.execute("multiply",{"left":6,"right":7})=={"product":42}

def test_duplicate_and_unknown_names():
    r=registry()
    with pytest.raises(ToolRegistrationError): r.register("multiply","again",Args,lambda a:a)
    with pytest.raises(ToolExecutionError): r.execute("delete_all",{})

def test_invalid_extra_arguments():
    with pytest.raises(ToolExecutionError,match="invalid arguments"):
        registry().execute("multiply",{"left":1,"right":2,"shell":"id"})

def test_handler_failure_wrapped():
    r=ToolRegistry(); r.register("explode","Raise.",Args,lambda _:1/0)
    with pytest.raises(ToolExecutionError,match="handler failed") as err: r.execute("explode",{"left":1,"right":2})
    assert isinstance(err.value.__cause__,ZeroDivisionError)
