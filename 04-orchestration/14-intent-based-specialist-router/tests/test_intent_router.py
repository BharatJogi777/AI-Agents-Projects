import pytest
from app.intent_router import Intent, IntentRouter

def test_dispatches_to_matching_specialist():
    router = IntentRouter({"billing": lambda text: "billing result"}, lambda text: Intent("billing", .95))
    assert router.run("invoice question").result == "billing result"

def test_low_confidence_rejected():
    router = IntentRouter({"billing": str}, lambda text: Intent("billing", .2))
    with pytest.raises(LookupError): router.run("question")

def test_unknown_intent_rejected():
    router = IntentRouter({"billing": str}, lambda text: Intent("admin", .99))
    with pytest.raises(LookupError): router.run("question")
