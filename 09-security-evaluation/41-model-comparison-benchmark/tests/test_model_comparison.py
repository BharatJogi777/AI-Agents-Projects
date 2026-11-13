import pytest
from app.model_comparison import compare_models
def test_paired_model_ranking():
 r=compare_models({"alpha":{"1":.9,"2":.7},"beta":{"1":.8,"2":.8}})
 assert r.rankings[0].model=="beta" and r.rankings[0].mean_score==pytest.approx(.8)
def test_mismatched_or_invalid_scores():
 with pytest.raises(ValueError): compare_models({"a":{"1":1},"b":{"2":1}})
 with pytest.raises(ValueError): compare_models({"a":{"1":1},"b":{"1":2}})
