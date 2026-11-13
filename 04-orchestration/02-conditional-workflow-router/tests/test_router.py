import pytest
from app.router import ConditionalRouter, Route

def test_first_matching_route_wins():
    router = ConditionalRouter([
        Route("urgent", lambda s: s["priority"] > 5, lambda s: {"queue": "fast"}),
        Route("normal", lambda s: True, lambda s: {"queue": "standard"}),
    ])
    assert router.run({"priority": 9})["state"]["queue"] == "fast"

def test_default_and_no_match():
    router = ConditionalRouter([], default=lambda s: {"handled": True})
    assert router.run({})["route"] == "default"
    with pytest.raises(LookupError):
        ConditionalRouter([]).run({})

def test_non_mapping_result_rejected():
    router = ConditionalRouter([Route("bad", lambda s: True, lambda s: None)])
    with pytest.raises(TypeError):
        router.run({})
