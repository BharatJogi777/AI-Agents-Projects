import pytest
from app.team import Agent, compose_team

def test_team_covers_required_skills():
    agents = [Agent("a", frozenset({"search"}), 1), Agent("b", frozenset({"write"}), 2),
              Agent("c", frozenset({"search", "write"}), 8)]
    team = compose_team(agents, {"search", "write"}, min_size=1, max_size=2)
    assert team.covered_capabilities == frozenset({"search", "write"})
    assert len(team.members) <= 2

def test_unavailable_or_insufficient_agents():
    with pytest.raises(RuntimeError):
        compose_team([Agent("a", frozenset({"search"}), available=False)], {"search"})
    with pytest.raises(RuntimeError):
        compose_team([Agent("a", frozenset({"search"}))], {"search", "write"})

def test_invalid_bounds_and_duplicate_ids():
    with pytest.raises(ValueError): compose_team([], set(), min_size=3, max_size=2)
    a = Agent("x", frozenset())
    with pytest.raises(ValueError): compose_team([a, a], set())
