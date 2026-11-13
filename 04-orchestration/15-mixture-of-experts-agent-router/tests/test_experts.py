import pytest
from app.experts import ExpertScore, MixtureOfExperts

def test_selects_top_k_and_normalizes_weights():
    router = MixtureOfExperts(
        {"a": lambda t: "A", "b": lambda t: "B", "c": lambda t: "C"},
        lambda t, names: [ExpertScore("a", .2), ExpertScore("b", .8), ExpertScore("c", .5)], 2)
    result = router.run("task")
    assert set(result.values) == {"b", "c"}
    assert sum(result.weights.values()) == pytest.approx(1)

def test_unknown_expert_rejected():
    router = MixtureOfExperts({"a": str}, lambda t, n: [ExpertScore("ghost", 1)])
    with pytest.raises(ValueError):
        router.run("task")

def test_zero_weight_rejected():
    router = MixtureOfExperts({"a": str}, lambda t, n: [ExpertScore("a", 0)])
    with pytest.raises(ValueError):
        router.run("task")

def test_duplicate_scores_rejected():
    router = MixtureOfExperts({"a": str}, lambda t, n: [ExpertScore("a", .5), ExpertScore("a", .5)])
    with pytest.raises(ValueError):
        router.run("task")
