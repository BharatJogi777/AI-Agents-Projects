from app.server import readiness


def test_readiness_contract():
    assert readiness() == {"status": "ready", "transport": "stdio"}
