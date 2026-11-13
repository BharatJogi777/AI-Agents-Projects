import pytest
from app.workspace import KnowledgeWorkspace

def test_publish_revision_and_search():
    w=KnowledgeWorkspace()
    first=w.publish("k1","deployment",{"rollback":"blue"},"ops",.9,expected_revision=0)
    second=w.publish("k1","deployment",{"rollback":"green"},"ops",.95,expected_revision=1)
    assert first.revision == 1 and second.revision == 2
    assert w.search("deployment",.9)[0].content["rollback"] == "green"

def test_conflict_and_validation():
    w=KnowledgeWorkspace(); w.publish("k","topic","value","agent",.5)
    with pytest.raises(RuntimeError): w.publish("k","topic","new","agent",.6,expected_revision=0)
    with pytest.raises(ValueError): w.publish("x","topic","v","agent",1.5)

def test_remove():
    w=KnowledgeWorkspace(); w.publish("k","t","v","a",.5)
    assert w.remove("k") is True
    assert w.remove("k") is False
