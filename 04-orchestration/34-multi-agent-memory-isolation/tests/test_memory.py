from app.memory import IsolatedMemory

def test_agents_and_namespaces_are_isolated():
    m=IsolatedMemory(); m.put("a","private","token","A"); m.put("b","private","token","B")
    assert m.get("a","private","token").value == "A"
    assert m.get("b","private","token").value == "B"
    assert m.list_namespace("a","private")[0].value == "A"

def test_delete_is_scoped_and_idempotent():
    m=IsolatedMemory(); m.put("a","n","k",1)
    assert m.delete("a","n","k") is True
    assert m.delete("a","n","k") is False
