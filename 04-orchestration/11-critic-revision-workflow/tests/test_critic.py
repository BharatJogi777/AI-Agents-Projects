import pytest
from app.critic import CriticRevision, Review

def test_revision_until_accepted():
    critic = lambda text: Review("improve" if text == "draft" else "", text == "final")
    flow = CriticRevision(critic, lambda text, review: "final", 2)
    result = flow.run("draft")
    assert result.accepted and result.artifact == "final" and len(result.reviews) == 2

def test_iteration_limit_is_enforced():
    flow = CriticRevision(lambda text: Review("more", False), lambda text, review: text + "x", 1)
    result = flow.run("draft")
    assert not result.accepted and len(result.reviews) == 2

def test_invalid_revision_rejected():
    flow = CriticRevision(lambda text: Review("fix", False), lambda text, review: "")
    with pytest.raises(ValueError): flow.run("draft")
