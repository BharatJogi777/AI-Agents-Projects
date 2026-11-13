from app.credential_tests import evaluate_exposure

def test_matches_corpus_without_returning_secret_values():
    result = evaluate_exposure(samples=["token=abc", "hello"], credentials=["abc"])
    assert result["exposed_samples"] == 1 and result["results"][0]["matched_labels"] == ["credential_1"]

def test_ignores_empty_credentials():
    result = evaluate_exposure(samples=["hello"], credentials=[""])
    assert result["exposed_samples"] == 0
